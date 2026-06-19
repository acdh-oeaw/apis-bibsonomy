import httpx
import hashlib
import json
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

import logging
from .utils import get_bibtex_from_url

logger = logging.getLogger(__name__)


class Reference(models.Model):
    """Model that holds the reference to a bibsonomy entry"""

    bibs_url = models.URLField()
    pages_start = models.PositiveIntegerField(blank=True, null=True)
    pages_end = models.PositiveIntegerField(blank=True, null=True)
    bibtex = models.JSONField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    attribute = models.CharField(blank=True, null=True, max_length=255)
    last_update = models.DateTimeField(auto_now=True)
    folio = models.CharField(
        max_length=255, help_text="String to add the folio.", blank=True, null=True
    )
    notes = models.CharField(
        max_length=255,
        help_text="Use to additionally define the location of the information",
        blank=True,
        null=True,
    )
    referenced_object = GenericForeignKey()

    def __str__(self):
        title = self.get_bibtex.get("title")
        desc = [title, self.pages_start, self.pages_end, self.folio, self.notes]
        desc = ", ".join(map(str, filter(None, desc)))
        return desc

    @property
    def get_bibtex(self):
        if isinstance(self.bibtex, str):
            return json.loads(self.bibtex)
        return self.bibtex or {}

    def get_absolute_url(self):
        return reverse("apis_bibsonomy:referencedetail", kwargs={"pk": self.pk})

    @property
    def similar_references(self, with_self=False):
        similarity_fields = getattr(
            settings,
            "BIBSONOMY_REFERENCE_SIMILARITY",
            ["bibs_url"],
        )
        similarity = Q()
        for field in similarity_fields:
            similarity &= Q(**{field: getattr(self, field)})
        if not with_self:
            return Reference.objects.exclude(pk=self.pk).filter(similarity)
        return Reference.objects.filter(similarity)

    def save(self, *args, **kwargs):
        if self.bibs_url:
            try:
                zoteroentry = ZoteroEntry.objects.get(url=self.bibs_url)
                self.bibtex = zoteroentry.data["csljson"]
            except ZoteroEntry.DoesNotExist:
                self.bibtex = get_bibtex_from_url(self.bibs_url)
        super().save(*args, **kwargs)


class ZoteroEntry(models.Model):
    url = models.URLField()
    version = models.IntegerField(null=True)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.data.get("data", {}).get("title", self.url)

    @property
    def bibtex(self):
        return self.data.get("csljson", {})

    @classmethod
    def _iterate_zotero(cls, endpoint: str, headers: dict = {}) -> list:
        items = []
        with httpx.Client(timeout=20.0) as client:
            while endpoint:
                response = client.get(endpoint, headers=headers)
                response.raise_for_status()

                items.extend(response.json())

                link = response.headers.get("link")
                endpoint = None
                for item in link.split(","):
                    if item.split(";")[1] == ' rel="next"':
                        endpoint = item.split(";")[0].strip()[1:-1]
        return items

    @classmethod
    def fetch_new(cls, config):
        config_hash = hashlib.md5(str(config).encode()).hexdigest()[:9]
        cache_key = f"ZoteroEntry_{config_hash}.fetch_new"
        last_run = cache.get(cache_key)
        max_update_delta = getattr(config, "update_delta_minutes", 30)
        if last_run is None or timezone.now() - last_run > timedelta(
            minutes=max_update_delta
        ):
            cache.set(cache_key, timezone.now(), timeout=600)
            group = config.get("group", None)
            user = config.get("user", None)
            api_key = config.get("API key")
            if (user is None and group is None) or api_key is None:
                logger.error("ZoteroEntry configuration is incomplete: %s", config)
                return
            path = f"user/{user}"
            if group:
                path = f"groups/{group}"
            headers = {"Zotero-API-Key": api_key}
            last_version = (
                cls.objects.aggregate(models.Max("version"))["version__max"] or 0
            )
            endpoint = f"https://api.zotero.org/{path}/items?include=data,bib,bibtex,csljson&since={last_version}&includeTrashed=1"

            new_items = cls._iterate_zotero(endpoint, headers)
            for item in new_items:
                obj, _ = cls.objects.get_or_create(url=item["links"]["self"]["href"])
                obj.version = item["version"]
                obj.data = item
                obj.save()

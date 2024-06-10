from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from .utils import get_bibtex_from_url

import json


class Reference(models.Model):
    """Model that holds the reference to a bibsonomy entry"""

    bibs_url = models.URLField()
    pages_start = models.PositiveIntegerField(blank=True, null=True)
    pages_end = models.PositiveIntegerField(blank=True, null=True)
    bibtex = models.TextField(blank=True, null=True)
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

    def __str__(self):
        title = self.bibtexjson.get("title")
        desc = [title, self.pages_start, self.pages_end, self.folio, self.notes]
        desc = ", ".join(map(str, filter(None, desc)))
        return desc

    @property
    def bibtexjson(self):
        return json.loads(self.bibtex or "{}")

    def get_absolute_url(self):
        return reverse("apis_bibsonomy:referencedetail", kwargs={"pk": self.pk})

    @property
    def referenced_object(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

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

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if update_fields is not None and "bibtex" in update_fields:
            self.bibtex = None
        if self.bibtex is None and self.bibs_url is not None:
            self.bibtex = get_bibtex_from_url(self.bibs_url)

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

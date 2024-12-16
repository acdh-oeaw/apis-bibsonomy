import json
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from .utils import get_bibtex_from_url


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
            self.bibtex = get_bibtex_from_url(self.bibs_url)
        super().save(*args, **kwargs)

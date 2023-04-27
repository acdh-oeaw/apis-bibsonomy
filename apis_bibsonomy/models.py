from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

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
    folio = models.CharField(max_length=255, help_text="String to add the folio.", blank=True, null=True)
    notes = models.CharField(max_length=255, help_text="Use to additionally define the location of the information", blank=True, null=True)

    def __str__(self):
        title = self.bibtexjson.get('title')
        desc = [title, self.pages_start, self.pages_end, self.folio, self.notes]
        desc = ", ".join(map(str, filter(None, desc)))
        return desc

    @property
    def bibtexjson(self):
        return json.loads(self.bibtex or "{}")

    def get_absolute_url(self):
        return reverse("apis_bibsonomy:referencedetail", kwargs={"pk": self.pk})

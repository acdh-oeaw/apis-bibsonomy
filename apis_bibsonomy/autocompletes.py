import json

from django import http
from dal import autocomplete
from django.conf import settings
from django.core.paginator import Paginator

from .models import ZoteroEntry


class BibsonomyAutocomplete(autocomplete.Select2ListView):
    def get(self, request, *args, **kwargs):
        choices = []
        more = False
        q = self.request.GET.get("q")
        if len(self.q) < 3:
            choices = []
        else:
            for idx, c in enumerate(self.conf):
                if c["type"] == "zotero":
                    ZoteroEntry.fetch_new(c)
                    pagenr = self.request.GET.get("page", 1)
                    paginator = Paginator(
                        ZoteroEntry.objects.filter(
                            data__data__title__icontains=q
                        ).order_by("data__data__title"),
                        self.page_size,
                    )
                    page = paginator.get_page(pagenr)
                    more = page.has_next()
                    for result in page:
                        choices.append(
                            {
                                "id": result.url,
                                "text": result.data["bib"],
                            }
                        )

        return http.HttpResponse(
            json.dumps({"results": choices + [], "pagination": {"more": more}}),
            content_type="application/json",
        )

    def __init__(self, page_size=20, group=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = page_size
        self.conf = getattr(settings, "APIS_BIBSONOMY", None)

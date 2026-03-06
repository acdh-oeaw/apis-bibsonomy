import requests
import json

from django import http
from dal import autocomplete
from django.conf import settings


def query_zotero(q, conf, page_size=20, offset=0):
    # TODO: Implement possibility that user puts in a full url referencing a specific item. Similiar to logic in `query_bibsonomy` above.
    if "group" in conf.keys():
        add = f"groups/{conf['group']}"
    else:
        add = f"users/{conf['user']}"
    url = f"https://api.zotero.org/{add}/items"
    headers = {"Zotero-API-Key": conf["API key"], "Zotero-API-Version": "3"}
    params = {
        "q": q,
        "qmode": "titleCreatorYear",
        "include": "bib",
        "start": offset,
        "limit": page_size,
    }
    res = requests.get(url, headers=headers, params=params)
    return res


class BibsonomyAutocomplete(autocomplete.Select2ListView):
    def get(self, request, *args, **kwargs):
        choices = []
        offset = (int(self.request.GET.get("page", 1)) - 1) * self.page_size
        more = False
        q = self.request.GET.get("q")
        if len(self.q) < 3:
            choices = []
        else:
            for idx, c in enumerate(self.conf):
                if c["type"] == "zotero":
                    res = query_zotero(q, c, self.page_size, offset)
                    if int(res.headers["Total-Results"]) > (self.page_size + offset):
                        more = True
                    for r in res.json():
                        choices.append(
                            {"id": r["links"]["self"]["href"], "text": r["bib"]}
                        )
        return http.HttpResponse(
            json.dumps({"results": choices + [], "pagination": {"more": more}}),
            content_type="application/json",
        )

    def __init__(self, page_size=20, group=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = page_size
        self.conf = getattr(settings, "APIS_BIBSONOMY", None)

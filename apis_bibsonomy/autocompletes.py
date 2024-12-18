import requests
from requests.auth import HTTPBasicAuth

from django import http
from dal import autocomplete
from django.conf import settings
from .utils import BibsonomyEntry


def query_bibsonomy(q, conf, page_size=20, offset=0):
    bibsonomy_bibtex_root_url = "https://www.bibsonomy.org/bibtex/"
    if q.startswith(bibsonomy_bibtex_root_url):
        hash = q.split(bibsonomy_bibtex_root_url)[1].split("/")[0]
        params = {"resource": hash, "resourcetype": "bibtex"}
    else:
        params = {
            "search": q,
            "resourcetype": "bibtex",
            "start": offset,
            "end": offset + page_size,
        }
        if "group" in conf.keys():
            params["group"] = conf["group"]
    url = f'{conf["url"]}api/posts'
    headers = {"accept": "application/json"}
    auth = HTTPBasicAuth(conf["user"], conf["API key"])
    res = requests.get(url, params=params, auth=auth, headers=headers)
    return res


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
    def __init__(self, page_size=20, group=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = page_size

    def get(self, request, *args, **kwargs):
        choices = []
        offset = (int(self.request.GET.get("page", 1)) - 1) * self.page_size
        more = False
        q = self.request.GET.get("q")
        if len(self.q) < 3:
            choices = []
        else:
            for config in getattr(settings, "APIS_BIBSONOMY", []):
                match config.get("type", None):
                    case "bibsonomy":
                        response = query_bibsonomy(q, config, self.page_size, offset)
                        data = response.json()
                        for r in data["posts"].get("post", []):
                            ent = BibsonomyEntry(bib_entry={"post": r})
                            choices.append(
                                {"id": ent.bib_hash, "text": ent.autocomplete}
                            )
                        more = data["posts"].get("next", False)
                    case "zotero":
                        res = query_zotero(q, config, self.page_size, offset)
                        total_results = res.headers["Total-Results"]
                        more = int(total_results) > (self.page_size + offset)
                        for result in res.json():
                            id = result["links"]["self"]["href"]
                            text = result["bib"]
                            choices.append({"id": id, "text": text})
        response = {"results": choices + [], "pagination": {"more": more}}
        return http.JsonResponse(response)

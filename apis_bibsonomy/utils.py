import requests
from django.conf import settings
import json
import logging
from functools import cache

logger = logging.getLogger(__name__)


@cache
def get_bibtex_from_url(url):
    sources = getattr(settings, "APIS_BIBSONOMY", [])
    sources = [s for s in sources if s.get("url") and s.get("url") in url]
    source = sources[-1]
    btype = source.get("type", None)
    bibtex = None
    try:
        if btype == "zotero":
            headers = {
                "Zotero-API-Key": source.get("API key", None),
                "Zotero-API-Version": "3",
            }
            params = {"include": "csljson"}
            res = requests.get(url, headers=headers, params=params)
            bibtex = json.dumps(res.json()["csljson"])
    except Exception as e:
        logger.warning(f"Could not fetch bibtex from {url}: {e}")
    return bibtex

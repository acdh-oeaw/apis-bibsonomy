import requests
from .models import SourceObject


class Source:
    def __init__(self, settings=dict()):
        self.url = settings["url"]
        self.user = settings["user"]
        self.apikey = settings["API key"]
        self.group = settings["group"]

    def update(self):
        raise NotImplementedError


class Zotero(Source):
    def update(self):
        lmv = 0 or SourceObject.objects.filter(source_type="zotero").order_by("last_modified_version").first()
        print(lmv)



class Bibsonomy(Source):
    pass

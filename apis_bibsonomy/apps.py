from django.apps import AppConfig
from django.conf import settings


class EntitiesConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = 'apis_bibsonomy'

    def ready(self):
        from .source import Zotero, Bibsonomy
        for source in getattr(settings, "APIS_BIBSONOMY", []):
            match source["type"]:
                case "bibsonomy":
                    s = Bibsonomy(*source)
                case "zotero":
                    s = Zotero(source)
                    s.update()
                case _:
                    print(f"Found unusable source {source['type']}")

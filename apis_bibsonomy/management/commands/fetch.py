from django.core.management.base import BaseCommand
from apis_bibsonomy.models import ZoteroEntry
from django.conf import settings


class Command(BaseCommand):
    help = "Fetch new Zotero entries from the Zotero API"

    def handle(self, *args, **options):
        conf = getattr(settings, "APIS_BIBSONOMY", None)
        for idx, c in enumerate(conf):
            if c["type"] == "zotero":
                ZoteroEntry.fetch_new(c)

from django.core.management.base import BaseCommand
from apis_bibsonomy.models import ZoteroEntry
from django.conf import settings


class Command(BaseCommand):
    help = "Fetch new Zotero entries from the Zotero API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--refetch",
            action="store_true",
            help="Delete & refetch *all* search entries.",
        )

    def handle(self, *args, **options):
        if options.get("refetch"):
            deleted, _ = ZoteroEntry.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} cached Zotero entries")
        for c in getattr(settings, "APIS_BIBSONOMY", []):
            if c["type"] == "zotero":
                ZoteroEntry.fetch_new(c)

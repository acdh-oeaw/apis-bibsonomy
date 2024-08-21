from django.core.management.base import BaseCommand
from apis_bibsonomy.models import Reference
from apis_bibsonomy.utils import get_bibtex_from_url


class Command(BaseCommand):
    help = "Update bibtex fields for all references"

    def handle(self, *args, **options):
        for obj in Reference.objects.all():
            obj.bibtex = get_bibtex_from_url(obj.bibs_url)
            obj.save()

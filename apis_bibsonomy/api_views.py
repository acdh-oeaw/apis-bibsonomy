from rest_framework.views import APIView
from rest_framework.response import Response
import json

from .utils import BibsonomyEntry
from .models import Reference


class SaveBibsonomyEntry(APIView):

    def post(self, request, format=None):
        bib_ref = request.data['bib_ref']
        obj_id = request.data['obj_id']
        entity_type = request.data['entity_type']
        field_name = request.data['field_name']
        page_range = request.data['page_range']
        bib_e = BibsonomyEntry(bib_hash=bib_ref) 



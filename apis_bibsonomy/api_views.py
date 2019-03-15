from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import status
import re

from .utils import BibsonomyEntry
from .models import Reference


class SaveBibsonomyEntry(APIView):

    def post(self, request, format=None):
        bib_ref = request.data['bib_ref']
        obj_id = request.data.get('obj_id', None)
        entity_type = request.data.get('entity_type', None)
        field_name = request.data.get('field_name', None)
        page_range = request.data.get('page_range', None)
        bib_e = BibsonomyEntry(bib_hash=bib_ref)
        r = {'bibs_url': bib_ref}
        if obj_id is not None:
            r['object_id'] = obj_id
        else:
            m = {'message': 'You need to specify the object id'}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        if entity_type is not None:
            r['content_type'] = entity_type
        else:
            m = {'message': 'You need to specify the content type of the object'}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        if field_name is not None:
            r['attribute'] = field_name
        if page_range is not None:
            mtch = re.match(r'^(\d)+\-?(\d+)?$', page_range)
            if mtch:
                if mtch.group(1):
                    r['pages_start'] = mtch.group(1)
                if mtch.group(2):
                    r['pages_end'] = mtch.group(2)
        r['bibtex'] = json.dumps(bib_e.bibtex)
        ref = Reference.objects.create(**r)
        m = {'status': 'success', 'ref_id': ref.pk}
        return Response(data=json.dumps(m), status=status.HTTP_201_CREATED)

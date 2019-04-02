from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import status
import re
from django.contrib.contenttypes.models import ContentType

from .utils import BibsonomyEntry
from .models import Reference
from .forms import ReferenceForm


class SaveBibsonomyEntry(APIView):

    def post(self, request, format=None):
        bib_ref = request.data['bibs_url']
        obj_id = request.data.get('object_id', None)
        entity_type = request.data.get('content_type', None)
        field_name = request.data.get('attribute', None)
        page_range = request.data.get('page_range', None)
        bib_e = BibsonomyEntry(bib_hash=bib_ref)
        r = {'bibs_url': bib_ref}
        if obj_id is not None:
            r['object_id'] = obj_id
        else:
            m = {'message': 'You need to specify the object id'}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        if entity_type is not None:
            r['content_type'] = ContentType.objects.get(model=entity_type)
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
        r['bibtex'] = bib_e.bibtex.replace('\\', '')
        ref = Reference.objects.create(**r)
        m = {'status': 'success', 'ref_id': ref.pk}
        return Response(data=json.dumps(m), status=status.HTTP_201_CREATED)

    def get(self, request):
        ct = request.query_params.get('contenttype', None)
        ob_pk = request.query_params.get('object_pk', None)
        attrb = request.query_params.get('attribute', None)
        if ct is None:
            m = {'message': 'You need to specify the content type of the object'}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        else:
            ct = ContentType.objects.get(model=ct).pk
        if ob_pk is None:
            m = {'message': 'You need to specify the primary key of the object'}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        qd = {'content_type': ct, 'object_id': ob_pk}
        if attrb is not None:
            qd['attribute'] = attrb
        res = Reference.objects.filter(**qd)
        r2 = [json.loads(x) for x in res.values_list('bibtex', flat=True)]
        return Response(data=r2)

import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import status
import re
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from .utils import BibsonomyEntry
from .models import Reference
from .forms import ReferenceForm


class SaveBibsonomyEntry(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get_str(entry, key):
        if not isinstance(entry, str) and key == 'author':
            res = []
            for x in entry:
                res.append(f"{x['family']}, {x['given']}")
            return (' and '.join(res), 'author')
        if not isinstance(entry, str) and key == 'issued':
            if "date-parts" in entry.keys():
                return ('-'.join([str(x) for x in entry['date-parts'][0]]), 'year')
        return (entry, key)

    def post(self, request, format=None):
        bib_ref = request.data.get('bibs_url', None)
        obj_id = request.data.get('object_id', None)
        entity_type = request.data.get('content_type', None)
        field_name = request.data.get('attribute', None)
        page_range = request.data.get('page_range', None)
        kind = None
        sett = getattr(settings, 'APIS_BIBSONOMY', [])
        for s in sett:
            if 'url' in s.keys():
                if s['url'] in bib_ref:
                    sett1 = s
                    kind = s['type']
        if bib_ref is not None:
            r = {'bibs_url': bib_ref}
            if kind == 'bibsonomy':
                bib_e = BibsonomyEntry(bib_hash=bib_ref, base_set=sett1)
                r['bibtex'] = json.dumps(bib_e.bibtex)
            elif kind == 'zotero':
                for s in sett:
                    if s['type'] == 'zotero':
                        headers = {'Zotero-API-Key': s['API key'], 'Zotero-API-Version': '3'}
                        params = {'include': 'csljson'}
                        res = requests.get(bib_ref, headers=headers, params=params)
                        r['bibtex'] = json.dumps(res.json()['csljson'])
            else:
                m = {'message': 'You need to select a publication.'}
                return Response(data=m, status=status.HTTP_400_BAD_REQUEST)
        if obj_id is not None:
            r['object_id'] = obj_id
        else:
            m = {'message': 'You need to specify the object id'}
            return Response(data=m, status=status.HTTP_400_BAD_REQUEST)
        if entity_type is not None:
            r['content_type'] = ContentType.objects.get(model=entity_type)
        else:
            m = {'message': 'You need to specify the content type of the object'}
            return Response(data=m, status=status.HTTP_400_BAD_REQUEST)
        if field_name is not None:
            r['attribute'] = field_name
        if page_range is not None:
            mtch = re.match(r'^(\d)+\-?(\d+)?$', page_range)
            if mtch:
                if mtch.group(1):
                    r['pages_start'] = mtch.group(1)
                if mtch.group(2):
                    r['pages_end'] = mtch.group(2)
        ref = Reference.objects.create(**r)
        m = {'message': 'Saved', 'ref_id': ref.pk}
        return Response(data=m, status=status.HTTP_201_CREATED)

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
        else:
            qd['attribute'] = ""
        res = Reference.objects.filter(**qd)
        r2 = [json.loads(x) for x in res.values_list('bibtex', flat=True)]
        for idx2, res2 in enumerate(res):
            r2[idx2]['pk'] = res2.pk
        for idx1, v1 in enumerate(r2):
            pre = dict()
            for k, v in v1.items():
                v2, k2 = self._get_str(v, k)
                pre[k2] = v2
            r2[idx1] = pre
        return Response(data=r2)

    def delete(self, request, format=None):
        ref = Reference.objects.get(pk=request.data.get('pk'))
        ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

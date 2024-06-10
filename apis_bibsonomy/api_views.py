import json

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import Reference
from .serializers import ReferenceSerializer
from .utils import get_bibtex_from_url


class SaveBibsonomyEntry(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # g.pirgie : this fixes incombatability with projects defining default-drf-permission as 'DjangoObjectPermissions' in settings.py

    @staticmethod
    def _get_str(entry, key):
        if not isinstance(entry, str) and key == "author":
            res = []
            for x in entry:
                res.append(f"{x['family']}, {x['given']}")
            return (" and ".join(res), "author")
        if not isinstance(entry, str) and key == "issued":
            if "date-parts" in entry.keys():
                return ("-".join([str(x) for x in entry["date-parts"][0]]), "year")
        return (entry, key)

    def post(self, request, format=None):
        bib_ref = request.data.get("bibs_url", None)
        obj_id = request.data.get("object_id", None)
        entity_type = request.data.get("content_type", None)
        field_name = request.data.get("attribute", None)
        pages_start = request.data.get("pages_start", None)
        pages_end = request.data.get("pages_end", None)
        folio = request.data.get("folio", None)
        notes = request.data.get("notes", None)
        if bib_ref is not None:
            r = {"bibs_url": bib_ref}
            r["bibtex"] = get_bibtex_from_url(bib_ref)
            if r["bibtex"] is None:
                m = {"message": "You need to select a publication."}
                return Response(data=m, status=status.HTTP_400_BAD_REQUEST)
        if obj_id is not None:
            r["object_id"] = obj_id
        else:
            m = {"message": "You need to specify the object id"}
            return Response(data=m, status=status.HTTP_400_BAD_REQUEST)
        if entity_type is not None:
            r["content_type"] = ContentType.objects.get(model=entity_type)
        else:
            m = {"message": "You need to specify the content type of the object"}
            return Response(data=m, status=status.HTTP_400_BAD_REQUEST)
        if field_name is not None:
            if len(field_name) > 0:
                r["attribute"] = field_name
        if pages_start is not None and pages_start != "":
            r["pages_start"] = pages_start
        if pages_end is not None and pages_end != "":
            r["pages_end"] = pages_end
        if folio is not None and folio != "":
            r["folio"] = folio
        if notes is not None and notes != "":
            r["notes"] = notes
        ref = Reference.objects.create(**r)
        m = {"message": "Saved", "ref_id": ref.pk}
        return Response(data=m, status=status.HTTP_201_CREATED)

    def get(self, request):
        ct = request.query_params.get("contenttype", None)
        ob_pk = request.query_params.get("object_pk", None)
        attrb = request.query_params.get("attribute", None)
        if ct is None:
            m = {"message": "You need to specify the content type of the object"}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        else:
            ct = ContentType.objects.get(model=ct).pk
        if ob_pk is None:
            m = {"message": "You need to specify the primary key of the object"}
            return Response(data=json.dumps(m), status=status.HTTP_400_BAD_REQUEST)
        qd = {"content_type": ct, "object_id": ob_pk}
        if attrb is not None and (attrb == "*" or attrb == "all" or attrb == ""):
            qd["attribute__isnull"] = False
        elif attrb is not None and attrb == "include":
            pass
        elif attrb is not None:
            qd["attribute"] = attrb
        else:
            qd["attribute__isnull"] = True
        res = Reference.objects.filter(**qd)
        r2 = [json.loads(x) for x in res.values_list("bibtex", flat=True)]
        for idx2, res2 in enumerate(res):
            r2[idx2]["pk"] = res2.pk
            r2[idx2]["attribute"] = res2.attribute

            r2[idx2]["pk"] = res2.pk
            if res2.pages_start is None:
                r2[idx2]["pages_start"] = ""
            else:
                r2[idx2]["pages_start"] = res2.pages_start
            if res2.pages_end is None:
                r2[idx2]["pages_end"] = ""
            else:
                r2[idx2]["pages_end"] = res2.pages_end
            if res2.folio is None:
                r2[idx2]["folio"] = ""
            else:
                r2[idx2]["folio"] = res2.folio
            if res2.notes is None:
                r2[idx2]["notes"] = ""
            else:
                r2[idx2]["notes"] = res2.notes
        for idx1, v1 in enumerate(r2):
            pre = dict()
            for k, v in v1.items():
                v2, k2 = self._get_str(v, k)
                pre[k2] = v2
            r2[idx1] = pre
        return Response(data=r2)

    def delete(self, request, format=None):
        ref = Reference.objects.get(pk=request.data.get("pk"))
        ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

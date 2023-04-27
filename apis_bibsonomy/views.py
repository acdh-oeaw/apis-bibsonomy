from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.db.models import Q

from .models import Reference


class ReferenceDetailView(DetailView):
    model = Reference

    def get_similar_objects(self):
        # we collect a list of other references instances, that point to the
        # same reference, and add that to the context
        obj = self.get_object()
        similarity_fields = getattr(
            settings,
            "REFERENCE_SIMILARITY",
            ["bibs_url"],
        )
        similarity = Q()
        for field in similarity_fields:
            similarity &= Q(**{field: getattr(obj, field)})
        return Reference.objects.filter(similarity)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        similar_references = self.get_similar_objects()
        context["referenced_objects"] = [
            (ref, ref.content_type.get_object_for_this_type(id=ref.object_id))
            for ref in similar_references
        ]
        return context


class ReferenceDeleteView(DeleteView):
    model = Reference

    def get_success_url(self):
        red = self.request.GET.get(
            "redirect", reverse_lazy("apis_bibsonomy:referencelist")
        )
        return red


class ReferenceListView(ListView):
    model = Reference

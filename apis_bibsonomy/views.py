from django.contrib.contenttypes.models import ContentType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.http import Http404

from .models import Reference


class ReferenceDetailView(DetailView):
    model = Reference

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_references"] = self.get_object().similar_references
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

class ReferenceOnListView(ReferenceListView):
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        contenttype = self.kwargs.get("contenttype")
        try:
            contenttype = ContentType.objects.get_for_id(contenttype)
        except ContentType.DoesNotExist:
            raise Http404
        return self.model.objects.filter(content_type=contenttype, object_id=pk)

    def get_template_names(self):
        # return only a partial if the request is ajax or htmx
        partial = "HX-Request" in self.request.headers or self.request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if partial:
            return "apis_bibsonomy/partials/reference_list.html"
        return super().get_template_names()

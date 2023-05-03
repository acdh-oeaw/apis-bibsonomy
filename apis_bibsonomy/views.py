from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

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

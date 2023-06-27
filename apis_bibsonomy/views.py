from django.contrib.contenttypes.models import ContentType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormMixin, ProcessFormView
from django.urls import reverse_lazy, reverse
from django.http import Http404

from .models import Reference
from .forms import ReferenceNewForm


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

class ReferenceOnListView(ReferenceListView, FormMixin, ProcessFormView):
    form_class = ReferenceNewForm

    def dispatch(self, *args, **kwargs):
        self.pk = self.kwargs.get("pk")
        try:
            contenttype = self.kwargs.get("contenttype")
            self.contenttype = ContentType.objects.get_for_id(contenttype)
        except ContentType.DoesNotExist:
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(content_type=self.contenttype, object_id=self.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.contenttype.model_class()(self.pk)
        return context

    def get_template_names(self):
        # return only a partial if the request is ajax or htmx
        partial = "HX-Request" in self.request.headers or self.request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if partial:
            return "apis_bibsonomy/partials/reference_list.html"
        return super().get_template_names()

    def get_success_url(self):
        return reverse('apis_bibsonomy:referenceonlist', kwargs=self.request.resolver_match.kwargs)

    def form_valid(self, form):
        args = form.cleaned_data
        args['content_type'] = ContentType.objects.get_for_id(self.request.resolver_match.kwargs['contenttype'])
        args['object_id'] = self.request.resolver_match.kwargs['pk']
        ref = Reference.objects.create(**args)
        return super().form_valid(form)

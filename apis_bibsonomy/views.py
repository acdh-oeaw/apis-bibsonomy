from django.contrib.contenttypes.models import ContentType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormMixin, ProcessFormView
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Reference
from .forms import ReferenceNewForm


class ReferenceDetailView(DetailView):
    model = Reference

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_references"] = self.get_object().similar_references
        return context


class ReferenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Reference

    def get_success_url(self):
        red = self.request.GET.get(
            "redirect", reverse_lazy("apis_bibsonomy:referencelist")
        )
        return red

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        # we set the status code to 200 for HTMX requests, so they don't get redirected
        if "HX-Request" in request.headers:
            resp.status_code = 200
        return resp


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
        return self.model.objects.filter(
            content_type=self.contenttype, object_id=self.pk
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contenttype"] = self.contenttype
        context["object"] = self.contenttype.get_object_for_this_type(id=self.pk)
        if not self.request.user.is_authenticated:
            del context["form"]
        return context

    def get_success_url(self):
        return reverse(
            "apis_bibsonomy:referenceonlist", kwargs=self.request.resolver_match.kwargs
        )

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return super().form_invalid(form)
        args = form.cleaned_data
        # we store the data about the last entered entry in the session
        # so we can automatically fill the form with the last reference
        self.request.session["last_bibsonomy_reference"] = form.cleaned_data.copy()

        args["content_type"] = ContentType.objects.get_for_id(
            self.request.resolver_match.kwargs["contenttype"]
        )
        args["object_id"] = self.request.resolver_match.kwargs["pk"]
        ref = Reference.objects.create(**args)
        self.request.session["last_bibsonomy_reference_title"] = ref.bibtexjson.get(
            "title"
        )
        return super().form_valid(form)


class ReferenceOnListViewModal(ReferenceOnListView):
    template_name = "apis_bibsonomy/reference_list_modal.html"

    def get_success_url(self):
        return reverse(
            "apis_bibsonomy:referenceonlistmodal",
            kwargs=self.request.resolver_match.kwargs,
        )


class ReferenceOnListViewPartial(ReferenceOnListView):
    template_name = "apis_bibsonomy/partials/reference_list.html"

    def get_success_url(self):
        return reverse(
            "apis_bibsonomy:referenceonlistpartial",
            kwargs=self.request.resolver_match.kwargs,
        )

from django.forms.widgets import Input
from django.urls import reverse_lazy

from .models import ZoteroEntry


class ZoteroEntryAutocomplete(Input):
    template_name = "apis_bibsonomy/widgets/zoteroentry_autocomplete.html"

    class Media:
        css = {"all": ["css/apis_bibsonomy/widgets/zoteroentry_autocomplete.css"]}

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["url"] = reverse_lazy("apis_bibsonomy:zoteroentryautocomplete")
        if value := ctx["widget"]["value"]:
            ctx["widget"]["object"] = ZoteroEntry.objects.filter(url=value).first()
        return ctx

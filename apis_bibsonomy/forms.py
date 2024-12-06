from django.forms import ModelForm
from .models import Reference
from dal.autocomplete import ListSelect2
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Div
from django.urls import reverse


class ReferenceNewForm(ModelForm):
    class Media:
        css = {"all": ["css/apis_bibsonomy.css"]}
        js = ["js/apis_bibsonomy.js"]

    class Meta:
        model = Reference
        exclude = ["content_type", "object_id", "bibtex", "attribute"]
        attrs = {"data-placeholder": "Type to get suggestions", "data-html": True}
        widgets = {
            "bibs_url": ListSelect2(url="bibsonomy:bibsonomyautocomplete", attrs=attrs)
        }
        help_texts = {"folio": None, "notes": None}

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk", None)
        content_type = kwargs.pop("content_type", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        if "instance" in kwargs:
            self.fields["bibs_url"].widget.choices = [
                (self.initial.get("bibs_url"), self.instance.get_bibtex.get("title"))
            ]
        self.helper.layout = Layout(
            Row(
                Div("bibs_url", css_class="col"),
            ),
            Row(
                Column("pages_start", css_class="col-auto col-md-2"),
                Column("pages_end", css_class="col-auto col-md-2"),
                Column("folio", css_class="col"),
                Column("notes", css_class="col"),
            ),
        )
        self.helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))

        if pk and content_type:
            self.helper.attrs = {
                "hx-post": reverse(
                    "apis_bibsonomy:referenceonlistmodal", args=[content_type.id, pk]
                ),
                "hx-target": f"#referenceon{content_type.id}_{pk}dlg",
            }

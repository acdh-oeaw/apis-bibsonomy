from django.forms import ModelForm
from django import forms
from .models import Reference
from dal.autocomplete import ListSelect2
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Div
from django.urls import reverse
from django.conf import settings


class ReferenceNewForm(ModelForm):
    class Media:
        js = ["js/apis_bibsonomy.js"]

    class Meta:
        model = Reference
        exclude = ["content_type", "object_id", "bibtex"]
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

        natural_key = f"{content_type.app_label}.{content_type.model}"
        if not getattr(settings, "REFERENCE_PER_FIELD", {}).get(natural_key, False):
            del self.fields["attribute"]
        else:
            choices = [
                (field.name, field.name)
                for field in content_type.model_class()._meta.get_fields()
            ]
            choices.insert(0, (None, ""))
            self.fields["attribute"] = forms.ChoiceField(
                required=False, choices=choices
            )

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
            Row(
                Column("attribute", css_class="col"),
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

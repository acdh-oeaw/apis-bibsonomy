from django.forms import ModelForm, HiddenInput
from django.urls import reverse
from .models import Reference
from apis_core.apis_entities.fields import ListSelect2
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Div


class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = "__all__"
        attrs = {"data-placeholder": "Type to get suggestions", "data-html": True}
        widgets = {
            "bibs_url": ListSelect2(url="bibsonomy:bibsonomyautocomplete", attrs=attrs)
        }

    def __init__(
        self,
        content_type=None,
        object_pk=None,
        attribute_name=None,
        hidden=False,
        *args,
        **kwargs,
    ):
        ModelForm.__init__(self, *args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
        self.helper.form_id = "bibs-form"
        self.helper.form_class = "bibs-forms"
        self.helper.form_action = reverse("bibsonomy:savegetbibsonomyentry")
        self.fields["pages_start"].widget.attrs["class"] = "form-control"
        self.fields["pages_end"].widget.attrs["class"] = "form-control"
        self.fields["bibtex"].widget = HiddenInput()
        self.fields["content_type"].widget = HiddenInput()
        self.fields["attribute"].widget = HiddenInput()
        self.fields["object_id"].widget = HiddenInput()
        if content_type is not None:
            self.fields["content_type"].initial = content_type
        if object_pk is not None:
            self.fields["object_id"].initial = object_pk
        if attribute_name is not None:
            self.fields["attribute"].initial = attribute_name


class ReferenceNewForm(ModelForm):
    class Meta:
        model = Reference
        exclude = ["content_type", "object_id", "bibtex", "attribute"]
        attrs = {"data-placeholder": "Type to get suggestions", "data-html": True}
        widgets = {
            "bibs_url": ListSelect2(url="bibsonomy:bibsonomyautocomplete", attrs=attrs)
        }
        help_texts = {"folio": None, "notes": None}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
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

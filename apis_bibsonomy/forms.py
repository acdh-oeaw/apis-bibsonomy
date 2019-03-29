from django.forms import ModelForm, HiddenInput
from .models import Reference
from .autocompletes import BibsonomyAutocomplete
from apis_core.apis_entities.fields import ListSelect2


class ReferenceForm(ModelForm):

    class Meta:
        model = Reference
        fields = '__all__'
        attrs = {'data-placeholder': 'Type to get suggestions',
                 'data-html': True}
        widgets = {'bibs_url': ListSelect2(url='bibsonomy:bibsonomyautocomplete', attrs=attrs)}

    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        print(self.fields)
        self.fields["pages_start"].widget.attrs['class'] = "form-control"
        self.fields["pages_end"].widget.attrs['class'] = "form-control"
        self.fields['bibtex'].widget = HiddenInput()
        self.fields['content_type'].widget = HiddenInput()
        self.fields['attribute'].widget = HiddenInput()
        self.fields['object_id'].widget = HiddenInput()

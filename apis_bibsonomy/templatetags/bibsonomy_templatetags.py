from django import template
from apis_bibsonomy.forms import ReferenceForm

register = template.Library()


@register.inclusion_tag('apis_bibsonomy/form_tag.html', takes_context=False)
def bibsonomy_form(content_type=None, object_pk=None, attribute_name=None, hidden=False):
    c_dict = {'content_type': content_type, 'object_pk': object_pk, 'attribute_name': attribute_name}
    form = ReferenceForm(**c_dict)
    return {"form": form, "hidden": hidden}


@register.inclusion_tag('apis_bibsonomy/list_tag.html', takes_context=False)
def bibsonomy_list(content_type=None, object_pk=None, attribute_name=None):
    c_dict = {'content_type': content_type, 'object_pk': object_pk, 'attribute_name': attribute_name}
    form = ReferenceForm(**c_dict)
    return {"form": form}

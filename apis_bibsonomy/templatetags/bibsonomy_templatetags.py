from django import template
from apis_bibsonomy.forms import ReferenceForm
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.inclusion_tag("apis_bibsonomy/form_tag.html", takes_context=False)
def bibsonomy_form(
    content_type=None, object_pk=None, attribute_name=None, hidden=False
):
    c_dict = {
        "content_type": content_type,
        "object_pk": object_pk,
        "attribute_name": attribute_name,
    }
    form = ReferenceForm(**c_dict)
    return {"form": form, "hidden": hidden}


@register.inclusion_tag("apis_bibsonomy/list_tag.html", takes_context=False)
def bibsonomy_list(content_type=None, object_pk=None, attribute_name=None):
    c_dict = {
        "content_type": content_type,
        "object_pk": object_pk,
        "attribute_name": attribute_name,
    }
    form = ReferenceForm(**c_dict)
    return {"form": form}


@register.inclusion_tag(
    "apis_bibsonomy/link_to_reference_on_tag.html", takes_context=False
)
def link_to_reference_on(obj=None, modal=False):
    return {
        "modal": modal,
        "object_pk": obj.pk,
        "content_type": ContentType.objects.get_for_model(obj).id,
    }

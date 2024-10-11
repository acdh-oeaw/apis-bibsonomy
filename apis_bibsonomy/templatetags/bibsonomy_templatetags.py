from django import template
from django.contrib.contenttypes.models import ContentType
from apis_bibsonomy.models import Reference
from apis_bibsonomy.forms import ReferenceNewForm

register = template.Library()


@register.inclusion_tag(
    "apis_bibsonomy/link_to_reference_on_tag.html", takes_context=False
)
def link_to_reference_on(obj=None, modal=False):
    return {
        "modal": modal,
        "object_pk": obj.pk,
        "content_type": ContentType.objects.get_for_model(obj).id,
    }


@register.inclusion_tag("apis_bibsonomy/link_to_reference_on_tag2.html", takes_context=True)
def link_to_reference_on2(context):
    return {
        "object": context["object"],
        "content_type": ContentType.objects.get_for_model(context["object"]),
    }


@register.simple_tag()
def list_references_on(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Reference.objects.filter(content_type=content_type, object_id=obj.id)


@register.simple_tag()
def reference_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return ReferenceNewForm(initial={"content_type": content_type, "object_id": obj.id})

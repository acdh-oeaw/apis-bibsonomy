from django import template
from django.contrib.contenttypes.models import ContentType

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

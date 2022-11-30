from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_menu_item_class(context, url_name):
    return "active" if reverse(url_name) == context["request"].path else ""

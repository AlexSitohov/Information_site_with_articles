from django import template
from django.contrib.auth.models import User

from main.models import *

register = template.Library()


@register.simple_tag()
def get_author():
    return CustomUser.objects.all().order_by('-subscribers')[:10]


@register.simple_tag()
def get_tags():
    return Tag.objects.all()[:100]

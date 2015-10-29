from django.template.defaultfilters import stringfilter
from django import template
from settings import *

register = template.Library()

@register.filter
def correct_float_format(value):
   return str(value).replace(',','.')

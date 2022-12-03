from django import template
import datetime
from django.forms.boundfield import BoundField
from django.forms.formsets import BaseFormSet
from django.utils.safestring import SafeString
from django.forms import CharField

register = template.Library()


@register.simple_tag
def tag_s():
    return 4


@register.simple_tag
def yesterDay():
    date = datetime.date.today() + datetime.timedelta(days=-1)
    return date


@register.filter()
def olderDay(date):
    # print(date < datetime.date.today())
    return date < datetime.date.today()


@register.filter()
def addAttr(field: BoundField, classes):
    data = eval(classes)
    # print()
    field = field.as_widget(attrs=data)
    return field


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    # for k in [k for k, v in d.items() if not v]:
    #     del d[k]
    return d.urlencode()

from django.forms.models import model_to_dict
from django import template
import json

register = template.Library()

@register.filter
def get_item(lista, indice):
    try:
        return lista[indice]
    except (IndexError, TypeError):
        return None

@register.filter
def toJson(queryset):
    listaCommenti = []
    for oggetto in queryset:
        listaCommenti.append(model_to_dict(oggetto))

    return json.dumps(listaCommenti).replace('"', "'")
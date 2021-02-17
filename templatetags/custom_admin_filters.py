from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
    if hasattr(field, "field") and field.field:
        return field.field.__class__.__name__.lower()
    return ""

@register.filter(name='to_class_name')
def to_class_name(value):
    return "{}.{}".format(value.__class__._meta.app_label, value.__class__._meta.model_name)

@register.filter(name='field_class_name')
def field_class_name(value):
    return "{}".format(value.__class__.__name__)
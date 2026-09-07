from django import template

register = template.Library()


@register.filter
def get_item(obj, field_name):
    """
    Accede a atributos de un objeto de forma dinámica.
    
    Uso en templates:
    {{ item|get_item:"nombre" }}
    """
    if not field_name:
        return ""
    
    # Soporta anidación con puntos
    fields = field_name.split('.')
    value = obj
    
    for field in fields:
        try:
            value = getattr(value, field, None)
            if value is None:
                return ""
        except (AttributeError, TypeError):
            return ""
    
    return value if value is not None else ""
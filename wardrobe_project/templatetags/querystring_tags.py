from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    request = context.get('request')
    if not request:
        return ""

    # Копируем текущие GET-параметры
    query_params = request.GET.copy()

    # Обновляем или добавляем переданные параметры (например, page)
    for key, value in kwargs.items():
        if value is not None:
            query_params[key] = value
        elif key in query_params:
            del query_params[key]

    return f"?{query_params.urlencode()}"
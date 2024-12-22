from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, class_name):
    try:
        return value.as_widget(attrs={"class": class_name})
    except AttributeError:
        # Вернуть исходное значение, если это не поле формы
        return value
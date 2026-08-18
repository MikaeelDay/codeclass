import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdownify")
def markdownify(text):
    html = md.markdown(text, extensions=["fenced_code", "tables", "nl2br"])
    return mark_safe(html)
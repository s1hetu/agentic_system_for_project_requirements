from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['fenced_code']))


@register.filter(name='markdown_to_html')
def markdown_to_html(text):
    """
    Converts Markdown text to HTML, including tables.
    """
    # extensions=['tables'] enables GitHub-style tables
    html = markdown.markdown(text, extensions=['tables'])
    return html

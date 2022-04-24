import markdown2
from django import template


register = template.Library()

@register.filter(name='markdowntohtml')
def markdowntohtml(markdown_text):
    htmlfile = markdown2.markdown(markdown_text)
    return htmlfile

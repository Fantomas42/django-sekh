"""Tags and filters for django-sekh"""
import re

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.template.defaultfilters import stringfilter

from sekh.utils import highlight
from sekh.utils import remove_duplicates

RE_SPLIT = re.compile(r' |;|,')
register = template.Library()


class HighLightNode(template.Node):

    def __init__(self, nodelist, terms):
        self.nodelist = nodelist
        self.terms = terms
        self.terms_var = template.Variable(terms)

    def render(self, context):
        output = self.nodelist.render(context)

        terms = self.terms
        if terms[0] == terms[-1] and terms[0] in ("'", '"'):
            terms = terms[1:-1]
        else:
            terms = self.terms_var.resolve(context)

        return highlight(output,
                         remove_duplicates(RE_SPLIT.split(terms)))


@register.tag(name='highlight')
def highlight_tag(parser, token):
    try:
        tag_name, terms = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'highlight tag requires exactly one argument')

    nodelist = parser.parse(('endhighlight',))
    parser.delete_first_token()
    return HighLightNode(nodelist, terms)


@register.filter(name='highlight', needs_autoescape=True)
@stringfilter
def highlight_filter(value, terms, autoescape=None):
    esc = autoescape and conditional_escape or (lambda x: x)
    return mark_safe(highlight(esc(value),
                               remove_duplicates(RE_SPLIT.split(terms))))

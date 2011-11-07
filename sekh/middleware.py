"""Middleware for highlighing the keywords
of an user's search in a HTML page,
based on http://www.djangosnippets.org/snippets/197/"""
import re
import cgi
import urlparse

from BeautifulSoup import BeautifulSoup

from django.conf import settings
from django.utils.encoding import smart_str


HIGHLIGHT_PATTERN = '<span class="highlight term-%s">%s</span>'
HIGHLIGHT_GET_VARNAMES = getattr(settings, 'HIGHLIGHT_GET_VARNAMES',
                                 ['highlight', 'hl', 'q', 'query', 'pattern'])


def remove_duplicates(seq):
    """Remove duplicates elements in a list
    preserving the order"""
    seen = {}
    result = []
    for item in seq:
        if item in seen:
            continue
        seen[item] = True
        result.append(item)
    return result


class BaseSearchReferrer(object):

    SEARCH_PARAMS = {
        'AltaVista': 'q',
        'Ask': 'q',
        'Google': 'q',
        'Live': 'q',
        'Lycos': 'query',
        'MSN': 'q',
        'Yahoo': 'p',
        }

    NETWORK_RE = r"""^
    (?P<subdomain>[-.a-z\d]+\.)?
    (?P<engine>%s)
    (?P<top_level>(?:\.[a-z]{2,3}){1,2})
    (?P<port>:\d+)?
    $(?ix)"""

    def parse_search(self, url):
        """
        Extract the search engine, domain, and search term from `url`
        and return them as (engine, domain, term). For example,
        ('Google', 'www.google.co.uk', ['django, 'framework']). Note that
        the search term will be converted to lowercase and have normalized
        spaces.

        The first tuple item will be None if the referrer is not a
        search engine.
        """
        try:
            parsed = urlparse.urlsplit(url)
            network = parsed[1]
            query = parsed[3]
        except (AttributeError, IndexError):
            return (None, None, [])
        for engine, param in self.SEARCH_PARAMS.iteritems():
            match = re.match(self.NETWORK_RE % engine, network)
            if match and match.group(2):
                terms = cgi.parse_qs(query).get(param)
                if terms:
                    terms = [term.lower() for term in terms[0].split()]
                    return (engine, network, terms)
        return (None, network, [])


class KeywordsHighlightingMiddleware(BaseSearchReferrer):
    """Middleware highlighting keywords on a html page
    by adding a span markup with a class"""

    def process_response(self, request, response):
        """Using BeautifulSoup to modify the HTML
        rendered by the view"""
        if not '<html' in response.content:
            return response

        referrer = request.META.get('HTTP_REFERER')
        engine, domain, terms = self.parse_search(referrer)

        for GET_varname in HIGHLIGHT_GET_VARNAMES:
            if request.GET.get(GET_varname):
                terms.extend(request.GET[GET_varname].split())

        if not terms:
            return response

        index = 1
        update_content = False
        soup = BeautifulSoup(smart_str(response.content))
        for term in remove_duplicates(terms):
            pattern = re.compile(re.escape(term), re.I | re.U)

            for text in soup.body.findAll(text=pattern):
                if text.parent.name in ('code', 'script', 'pre'):
                    continue

                def highlight(match):
                    match_term = match.group(0)
                    return HIGHLIGHT_PATTERN % (index, match_term)

                new_text = pattern.sub(highlight, text)
                text.replaceWith(new_text)
                update_content = True
            # Reload the entire soup, because substituion
            # doesn't rebuild the document tree
            soup = BeautifulSoup(str(soup))
            index += 1

        if update_content:
            response.content = str(soup)

        return response

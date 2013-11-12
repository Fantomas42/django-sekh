"""
Middleware for highlighing the keywords
of an user's search in a HTML page based on
http://www.djangosnippets.org/snippets/197/
"""
import re
try:
    from urllib.parse import urlsplit
    from urllib.parse import parse_qs
except ImportError:  # Python 2
    from urlparse import urlsplit
    from urlparse import parse_qs

from sekh.settings import GET_VARNAMES
from sekh.highlighting import highlight
from sekh.utils import remove_duplicates


class BaseSearchReferrer(object):

    SEARCH_PARAMS = {
        'Ask': 'q',
        'Baidu': 'wd',
        'Bing': 'q',
        'Google': 'q',
        'Hotbot': 'q',
        'Lycos': 'query',
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
            parsed = urlsplit(url)
            network = parsed[1]
            query = parsed[3]
        except (AttributeError, IndexError):
            return (None, None, [])
        if not network:
            return (None, None, [])
        for engine, param in self.SEARCH_PARAMS.items():
            match = re.match(self.NETWORK_RE % engine, network)
            if match and match.group(2):
                terms = parse_qs(query).get(param)
                if terms:
                    terms = [term.lower() for term in terms[0].split()]
                    return (engine, network, terms)
        return (None, network, [])


class KeywordsHighlightingMiddleware(BaseSearchReferrer):
    """
    Middleware highlighting keywords on a html page
    by adding a markup with classes.
    """

    def process_response(self, request, response):
        """
        Transform the HTML if keywords are present.
        """
        if (response.status_code != 200 or
                not 'text/html' in response['Content-Type']):
            return response

        referrer = request.META.get('HTTP_REFERER')
        engine, domain, terms = self.parse_search(referrer)

        for GET_varname in GET_VARNAMES:
            if request.GET.get(GET_varname):
                terms.extend(request.GET[GET_varname].split())

        if not terms:
            return response

        response.content = highlight(response.content,
                                     remove_duplicates(terms))
        return response

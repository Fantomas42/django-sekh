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
HIGHLIGHT_GET_VARNAME = getattr(settings, 'HIGHLIGHT_GET_VARNAME', 'hl')


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
        ('Google', 'www.google.co.uk', 'django framework'). Note that
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
            return (None, None, None)
        for engine, param in self.SEARCH_PARAMS.iteritems():
            match = re.match(self.NETWORK_RE % engine, network)
            if match and match.group(2):
                term = cgi.parse_qs(query).get(param)
                if term and term[0]:
                    term = ' '.join(term[0].split()).lower()
                    return (engine, network, term)
        return (None, network, None)


class KeywordsHighlightingMiddleware(BaseSearchReferrer):
    """Middleware highlighting keywords on a html page
    by adding a span markup with a class"""

    def process_response(self, request, response):
        """Using BeautifulSoup to modify the HTML
        rendered by the view"""
        referrer = request.META.get('HTTP_REFERER')
        engine, domain, term = self.parse_search(referrer)
        content = response.content

        if HIGHLIGHT_GET_VARNAME in request.GET:
            term = request.GET[HIGHLIGHT_GET_VARNAME]

        if term and '<html' in content:
            update_content = False
            term = term.split()
            index = 1
            soup = BeautifulSoup(smart_str(content))
            for t in term:
                pattern = re.compile(re.escape(t), re.I | re.U)
                if re.search(pattern, HIGHLIGHT_PATTERN):
                    continue
                for text in soup.find('body').findAll(text=pattern):
                    if text.parent.name in ('code', 'script', 'pre'):
                        continue
                    new_text = re.sub(pattern, HIGHLIGHT_PATTERN % (index, t),
                                      text, 0)
                    text.replaceWith(new_text)
                    update_content = True
                index += 1

            if update_content:
                response.content = str(soup)

        return response

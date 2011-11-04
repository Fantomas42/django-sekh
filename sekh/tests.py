"""Unit tests for sekh"""
from django.test import TestCase
from django.http import HttpRequest
from django.http import HttpResponse

from sekh.middleware import HIGHLIGHT_GET_VARNAMES
from sekh.middleware import KeywordsHighlightingMiddleware

HTML_CONTENT = """
<html>
  <body>
    <p>Hello world !</p>
  </body>
</html>
"""


class KeywordsHighlightingMiddlewareTestCase(TestCase):
    """Tests of the Sekh middleware"""

    def _get_request(self, GET={}, referer=None):
        request = HttpRequest()
        request.GET = GET
        if referer:
            request.META['HTTP_REFERER'] = referer
        return request

    def test_with_REFERER(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content, HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(referer='http://toto.com/?q=Hello'),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content, HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(referer='http://www.google.com/?q=world'),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">world</span>' in response.content)

    def test_with_GET(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content, HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'ziltoid'}),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content, HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'Hello world'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'Hello',
                               HIGHLIGHT_GET_VARNAMES[1]: 'World',
                               HIGHLIGHT_GET_VARNAMES[2]: 'Hello'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

    def test_dont_highlight_highlightings(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'Hello high'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span>' in response.content)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'Hello high'}),
            HttpResponse(HTML_CONTENT.replace('world', 'high')))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">high</span>' in response.content)

    def test_multiple_in_one_markup(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'Hello'}),
            HttpResponse('<html><body><p>Hello world hello !' \
                         '</p></body></html>'))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> world ' \
            '<span class="highlight term-1">hello</span>' in response.content)

    def test_with_cases_REFERER(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(referer='http://www.google.com/?q=HELLO World'),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

    def test_with_cases_GET(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAMES[0]: 'HELLO World'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

"""Unit tests for sekh"""
from django.test import TestCase
from django.http import HttpRequest
from django.http import HttpResponse

from sekh.middleware import HIGHLIGHT_GET_VARNAME
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
            self._get_request({HIGHLIGHT_GET_VARNAME: 'ziltoid'}),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content, HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAME: 'Hello world'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

    def test_dont_highlight_highlightings(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAME: 'Hello high'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span>' in response.content)
        # When fixed, add a text with the highlight word and check behavior.

    def test_with_cases_REFERER(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(referer='http://www.google.com/?q=HELLO World'),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

    def test_with_cases_GET(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({HIGHLIGHT_GET_VARNAME: 'HELLO World'}),
            HttpResponse(HTML_CONTENT))
        self.assertTrue(
            '<span class="highlight term-1">Hello</span> ' \
            '<span class="highlight term-2">world</span>' in response.content)

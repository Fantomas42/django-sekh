"""Unit tests for django-sekh"""
from django.test import TestCase
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import Context
from django.template import Template
from django.template import TemplateSyntaxError

from sekh.utils import list_range
from sekh.utils import get_window
from sekh.utils import get_min_index
from sekh.utils import compile_terms
from sekh.utils import remove_duplicates
from sekh.excerpt import excerpt
from sekh.excerpt import shorten_excerpt
from sekh.excerpt import shortest_term_span
from sekh.excerpt import generate_term_positions
from sekh.highlighting import highlight
from sekh.middleware import KeywordsHighlightingMiddleware


HTML_CONTENT = '<html><body><p>Hello world !</p></body></html>'


class TestRemoveDuplicates(TestCase):
    """Tests of remove_duplicates function"""

    def test_remove_duplicates(self):
        self.assertEquals(
            remove_duplicates(['titi', 'toto', 'tata', 'titi']),
            ['titi', 'toto', 'tata'])

    def test_remove_duplicates_with_spaces(self):
        self.assertEquals(
            remove_duplicates(['titi', 'toto', 'tata', ' titi']),
            ['titi', 'toto', 'tata'])

    def test_remove_duplicates_with_void_value(self):
        self.assertEquals(
            remove_duplicates(['titi', ' ', 'toto', '', ' titi']),
            ['titi', 'toto'])


class TestCompileTerms(TestCase):
    """Test of compile_terms function"""

    def test_compile_terms(self):
        terms = compile_terms(['toto', 'titi'])
        self.assertTrue(terms[0].match('TOTO'))


class TestListRange(TestCase):
    """Tests of list_range function"""

    def test_list_range(self):
        self.assertEquals(
            list_range([5, 6, 10]), 5)
        self.assertEquals(
            list_range([1, 7, 9]), 8)


class TestGetWindow(TestCase):
    """Tests of get_window function"""

    def test_get_window(self):
        self.assertEquals(
            get_window([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                       [0, 1, 2]), [1, 5, 9])


class TestGetMinIndex(TestCase):
    """Tests of get_min_index function"""

    def test_get_min_index(self):
        self.assertEquals(
            get_min_index([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          [1, 5, 9]), 0)
        self.assertEquals(
            get_min_index([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          [9, 5, 1]), 2)
        self.assertEquals(
            get_min_index([[1, 2, 3], [4, 5, 6], [7, 8, 0]],
                          [9, 5, 1]), 1)
        self.assertEquals(
            get_min_index([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          [3, 5, 9]), 1)
        self.assertEquals(
            get_min_index([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          [3, 6, 9]), None)


class TestHighlight(TestCase):
    """Tests of highlight function"""

    def test_highlight(self):
        self.assertEquals(
            highlight(HTML_CONTENT, ['Hello', 'world']),
            '<html><body><p><span class="highlight term-1">Hello</span> '
            '<span class="highlight term-2">world</span> !</p></body></html>')

    def test_highlight_case(self):
        self.assertEquals(
            highlight(HTML_CONTENT, ['HELLO', 'World']),
            '<html><body><p><span class="highlight term-1">Hello</span> '
            '<span class="highlight term-2">world</span> !</p></body></html>')

    def test_highlight_none(self):
        self.assertEquals(
            highlight(HTML_CONTENT, []), HTML_CONTENT)

    def test_highlight_multiple_in_one_markup(self):
        self.assertEquals(
            highlight(HTML_CONTENT.replace('!', 'hello'), ['hello']),
            '<html><body><p><span class="highlight term-1">Hello</span> '
            'world <span class="highlight term-1">hello</span></p>'
            '</body></html>')

    def test_dont_highlight_highlightings(self):
        self.assertEquals(
            highlight(HTML_CONTENT.replace('world', 'highlight'),
                      ['hello', 'highlight']),
            '<html><body><p><span class="highlight term-1">Hello</span> '
            '<span class="highlight term-2">highlight</span> !</p>'
            '</body></html>')

    def test_dont_highlight_protected_markups(self):
        self.assertEquals(
            highlight(HTML_CONTENT.replace('world', '<pre>world</pre>'),
                      ['world']),
            '<html><body><p>Hello <pre>world</pre> !</p></body></html>')


class TestGenerateTermPositions(TestCase):
    """Test of generate_term_positions function"""
    content = ('Il etait une fois dans un pays merveilleux, '
               'un petit garcon nomme Darwin').split()

    def test_generate_term_positions(self):
        self.assertEquals(
            generate_term_positions(self.content, ['garcon']),
            [[10]])
        self.assertEquals(
            generate_term_positions(self.content, ['toto']),
            [])

    def test_generate_term_positions_multi(self):
        self.assertEquals(
            generate_term_positions(self.content, ['un', 'garcon']),
            [[10], [2, 5, 8]])
        self.assertEquals(
            generate_term_positions(self.content, ['garcon', 'un']),
            [[10], [2, 5, 8]])
        self.assertEquals(
            generate_term_positions(self.content, ['garcon', 'toto', 'un']),
            [[10], [2, 5, 8]])

    def test_generate_term_positions_case(self):
        self.assertEquals(
            generate_term_positions(self.content, ['UN', 'gARcon']),
            [[2, 5, 8], [10]])


class TestShortestTermSpan(TestCase):
    """Test of shortest_term_span function"""

    def test_shortest_term_span(self):
        self.assertEquals(
            shortest_term_span([[0, 5, 10, 15],
                                [1, 3, 6, 9],
                                [4, 8, 16, 21]]),
            [3, 4, 5])
        self.assertEquals(
            shortest_term_span([[0, 5],
                                [1, 3, 9],
                                [8, 16, 21, 22]]),
            [5, 8, 9])
        self.assertEquals(
            shortest_term_span([[0, 1],
                                [4, 5],
                                [2, 3]]),
            [1, 2, 4])


class TestShortenExcerpt(TestCase):
    """Test of shorten_excerpt function"""

    def test_shorten_excerpt(self):
        self.assertEquals(
            shorten_excerpt(
                'test blah blah blah blah blah blah case',
                'test case'),
            'test blah blah blah blah blah ... case')


class TestExcerpt(TestCase):
    """Test of excerpt function"""
    content = (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
        'In in nunc eros! Suspendisse a feugiat eros, et pharetra nisl ? '
        'Cras pulvinar varius enim et aliquet. Sed sit amet ultricies libero. '
        'Etiam facilisis, lectus ut tristique rutrum, leo libero '
        'elementum eros, sed lobortis urna lacus sit amet velit. '
        'Quisque ut leo eu dolor aliquet eleifend mattis et urna. '
        'Praesent vitae viverra purus.')

    def test_excerpt(self):
        self.assertEquals(
            excerpt(self.content, ['lacus'], 40),
            'et aliquet. Sed sit amet ultricies libero. Etiam facilisis, '
            'lectus ut tristique rutrum, leo libero elementum eros, sed '
            'lobortis urna lacus sit amet velit. Quisque ut leo eu dolor '
            'aliquet eleifend mattis et urna. Praesent vitae viverra purus.')
        self.assertEquals(
            excerpt(self.content, ['lacus'], 10),
            'elementum eros, sed lobortis urna lacus sit amet velit. '
            'Quisque ut')
        self.assertEquals(
            excerpt(self.content, ['aliquet'], 40),
            'consectetur adipiscing elit. In in nunc eros! Suspendisse a '
            'feugiat eros, et pharetra nisl ? Cras pulvinar varius enim '
            'et aliquet. Sed sit amet ultricies libero. Etiam facilisis, '
            'lectus ut tristique rutrum, leo libero elementum eros, sed '
            'lobortis urna lacus sit')
        self.assertEquals(
            excerpt(self.content, ['aliquet'], 10),
            'Cras pulvinar varius enim et aliquet. Sed sit amet '
            'ultricies libero.')

    def test_excerpt_multi_terms(self):
        result = (
            'et aliquet. Sed sit amet ultricies libero. Etiam facilisis, '
            'lectus ut tristique rutrum, leo libero elementum eros, sed '
            'lobortis urna lacus sit amet velit. Quisque ut leo eu dolor '
            'aliquet eleifend mattis et urna. Praesent vitae viverra purus.')
        result_compressed = (
            'ut tristique rutrum, leo libero elementum ... lacus sit amet '
            'velit. Quisque ut ... aliquet eleifend mattis et urna. '
            'Praesent ...')
        self.assertEquals(
            excerpt(self.content, ['aliquet', 'lacus'], 40), result)
        self.assertEquals(
            excerpt(self.content, ['lacus', 'aliquet'], 40), result)
        self.assertEquals(
            excerpt(self.content, ['aliquet', 'lacus'], 20),
            result_compressed)

    def test_excerpt_multi_terms_extra_long(self):
        self.assertEquals(
            excerpt(self.content, ['lorem', 'purus'], 40),
            'Lorem ipsum dolor sit amet, consectetur ... purus.')
        self.assertEquals(
            excerpt(self.content, ['lorem', 'purus'], 10),
            'Lorem ipsum dolor sit amet, consectetur ... purus.')

    def test_excerpt_case(self):
        self.assertEquals(
            excerpt(self.content, ['LACUS'], 40),
            'et aliquet. Sed sit amet ultricies libero. Etiam facilisis, '
            'lectus ut tristique rutrum, leo libero elementum eros, sed '
            'lobortis urna lacus sit amet velit. Quisque ut leo eu dolor '
            'aliquet eleifend mattis et urna. Praesent vitae viverra purus.')

    def test_excerpt_not_present(self):
        self.assertEquals(
            excerpt(self.content, ['toto'], 40),
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
            'In in nunc eros! Suspendisse a feugiat eros, et pharetra '
            'nisl ? Cras pulvinar varius enim et aliquet. Sed sit amet '
            'ultricies libero. Etiam facilisis, lectus ut tristique '
            'rutrum, leo libero elementum')
        self.assertEquals(
            excerpt(self.content, ['toto'], 10),
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
            'In in')

    def test_excerpt_none(self):
        self.assertEquals(
            excerpt(self.content, [], 40),
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
            'In in nunc eros! Suspendisse a feugiat eros, et pharetra '
            'nisl ? Cras pulvinar varius enim et aliquet. Sed sit amet '
            'ultricies libero. Etiam facilisis, lectus ut tristique '
            'rutrum, leo libero elementum')
        self.assertEquals(
            excerpt(self.content, [], 10),
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
            'In in')


class TestKeywordsHighlightingMiddleware(TestCase):
    """Tests of the Sekh middleware"""

    def _get_request(self, GET={}, referer=None):
        request = HttpRequest()
        request.GET = GET
        if referer:
            request.META['HTTP_REFERER'] = referer
        return request

    def test_referer(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(referer='http://toto.com/?q=Hello'),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content.decode('utf-8'), HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(referer='http://www.google.com/?q=world'),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content.decode('utf-8'),
                          '<html><body><p>Hello <span class="highlight '
                          'term-1">world</span> !</p></body></html>')

    def test_get(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request(),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content.decode('utf-8'), HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({'highlight': 'ziltoid'}),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(response.content.decode('utf-8'), HTML_CONTENT)

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({'highlight': 'Hello world'}),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(
            response.content.decode('utf-8'),
            '<html><body><p><span class="highlight term-1">Hello</span> '
            '<span class="highlight term-2">world</span> !</p></body></html>')

        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({'highlight': 'Hello',
                               'hl': 'World',
                               'q': 'Hello'}),
            HttpResponse(HTML_CONTENT))
        self.assertEquals(
            response.content.decode('utf-8'),
            '<html><body><p><span class="highlight term-1">Hello</span> '
            '<span class="highlight term-2">world</span> !</p></body></html>')

    def test_non_html(self):
        response = KeywordsHighlightingMiddleware().process_response(
            self._get_request({'highlight': 'Hello world'}),
            HttpResponse(HTML_CONTENT, content_type='text/xml'))
        self.assertEquals(response.content.decode('utf-8'), HTML_CONTENT)


class TestHighlightFilter(TestCase):
    """Tests of Highlight filter"""
    response = '<p><span class="highlight term-1">Coding</span> is ' \
               '<span class="highlight term-2">fun</span> :).</p>'

    def test_filter(self):
        context = Context({'content': 'Coding is fun :).'})
        t = Template("""
        {% load sekh_tags %}
        <p>{{ content|highlight:"coding,fun" }}</p>
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        <p>{{ content|highlight:"coding, fun" }}</p>
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        <p>{{ content|highlight:"coding fun" }}</p>
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        <p>{{ content|highlight:"coding coding fun" }}</p>
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

    def test_filter_with_variable(self):
        t = Template("""
        {% load sekh_tags %}
        <p>{{ content|highlight:query }}</p>
        """)
        html = t.render(Context({'content': 'Coding is fun :).',
                                 'query': 'coding, fun'}))
        self.assertEquals(html.strip(), self.response)


class TestHighlightTag(TestCase):
    """Test for Highlight tag"""
    response = '<p><span class="highlight term-1">Coding</span> is ' \
               '<span class="highlight term-2">fun</span> :).</p>'

    def test_tag(self):
        t = Template("""
        {% load sekh_tags %}
        {% highlight "coding fun" %}
        <p>{{ content }}</p>
        {% endhighlight %}
        """)
        html = t.render(Context({'content': 'Coding is fun :).'}))
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% highlight "coding,fun" %}
        <p>Coding is fun :).</p>
        {% endhighlight %}
        """)
        html = t.render(Context())
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% highlight "coding, fun" %}
        <p>Coding is fun :).</p>
        {% endhighlight %}
        """)
        html = t.render(Context())
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% highlight "coding fun" %}
        <p>Coding is fun :).</p>
        {% endhighlight %}
        """)
        html = t.render(Context())
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% highlight "coding coding fun" %}
        <p>Coding is fun :).</p>
        {% endhighlight %}
        """)
        html = t.render(Context())
        self.assertEquals(html.strip(), self.response)

    def test_tag_variable_content(self):
        t = Template("""
        {% load sekh_tags %}
        {% highlight query %}
        <p>{{ content }}</p>
        {% endhighlight %}
        """)
        html = t.render(Context({'content': 'Coding is fun :).',
                                 'query': 'coding, fun'}))
        self.assertEquals(html.strip(), self.response)

    def test_tag_error(self):
        with self.assertRaises(TemplateSyntaxError):
            Template("""
            {% load sekh_tags %}
            {% highlight %}
            <p>Coding is fun :).</p>
            {% endhighlight %}
            """)


class ExcerptTestCase(TestCase):
    """Base TestCase for Excerpt"""
    content = (
        "The Zen of Python, by Tim Peters "
        "Beautiful is better than ugly. "
        "Explicit is better than implicit. "
        "Simple is better than complex. "
        "Complex is better than complicated. "
        "Flat is better than nested. "
        "Sparse is better than dense. "
        "Readability counts. "
        "Special cases aren't special enough to break the rules. "
        "Although practicality beats purity. "
        "Errors should never pass silently. "
        "Unless explicitly silenced. "
        "In the face of ambiguity, refuse the temptation to guess. "
        "There should be one- and preferably only one -obvious way to do it."
        "Although that way may not be obvious at first unless you're Dutch. "
        "Now is better than never. "
        "Although never is often better than *right* now. "
        "If the implementation is hard to explain, it's a bad idea. "
        "If the implementation is easy to explain, it may be a good idea. "
        "Namespaces are one honking great idea -- let's do more of those!")
    response = ('The Zen of Python, by Tim ... Beautiful is better than ugly'
                '. Explicit ... temptation to guess. There should be ...')


class TestExcerptFilter(ExcerptTestCase):
    """Tests of Excerpt filter"""

    def test_filter(self):
        context = Context({'content': self.content})
        t = Template("""
        {% load sekh_tags %}
        {{ content|excerpt:"beautiful,temptation" }}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {{ content|excerpt:"beautiful, temptation" }}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {{ content|excerpt:"beautiful temptation" }}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {{ content|excerpt:"beautiful beautiful temptation" }}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

    def test_filter_with_variable(self):
        t = Template("""
        {% load sekh_tags %}
        {{ content|excerpt:query }}
        """)
        html = t.render(Context({'content': self.content,
                                 'query': 'beautiful, temptation'}))
        self.assertEquals(html.strip(), self.response)


class TestExcerptTag(ExcerptTestCase):
    """Test for Excerpt tag"""

    def test_tag(self):
        context = Context({'content': self.content})
        t = Template("""
        {% load sekh_tags %}
        {% excerpt "beautiful temptation" %}
        {{ content }}
        {% endexcerpt %}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% excerpt "beautiful,temptation" %}
        {{ content }}
        {% endexcerpt %}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% excerpt "beautiful, temptation" %}
        {{ content }}
        {% endexcerpt %}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {%% load sekh_tags %%}
        {%% excerpt "beautiful temptation" %%}
        %s
        {%% endexcerpt %%}
        """ % self.content)
        html = t.render(Context())
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% excerpt "beautiful beautiful temptation" %}
        {{ content }}
        {% endexcerpt %}
        """)
        html = t.render(context)
        self.assertEquals(html.strip(), self.response)

        t = Template("""
        {% load sekh_tags %}
        {% excerpt "beautiful temptation" 10 %}
        {{ content }}
        {% endexcerpt %}
        """)
        html = t.render(context)

        self.assertEquals(
            html.strip(),
            'of Python, by Tim Peters Beautiful is better than ugly. '
            'Explicit ... temptation to guess. There should be')

    def test_tag_variable_content(self):
        t = Template("""
        {% load sekh_tags %}
        {% excerpt query %}
        {{ content }}
        {% endexcerpt %}
        """)
        html = t.render(Context({'content': self.content,
                                 'query': 'beautiful, temptation'}))
        self.assertEquals(html.strip(), self.response)

    def test_tag_error(self):
        with self.assertRaises(TemplateSyntaxError):
            Template("""
            {% load sekh_tags %}
            {% excerpt %}
            <p>Coding is fun :).</p>
            {% endexcerpt %}
            """)

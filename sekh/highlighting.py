"""Highlighting for django-sekh"""
from bs4 import BeautifulSoup

from sekh.utils import compile_terms
from sekh.settings import PROTECTED_MARKUPS
from sekh.settings import HIGHLIGHTING_PATTERN


def highlight(content, terms):
    """
    Highlight the HTML with BeautifulSoup.
    """
    index = 1
    update_content = False
    soup = BeautifulSoup(content)
    terms = compile_terms(terms)

    for term in terms:
        for text in soup.find_all(text=term):
            if text.parent.name in PROTECTED_MARKUPS:
                continue

            def highlight(match):
                match_term = match.group(0)
                return HIGHLIGHTING_PATTERN % {
                    'index': index, 'term': match_term}

            new_text = term.sub(highlight, text)
            text.replace_with(BeautifulSoup(new_text))
            update_content = True
        # Reload the entire soup, because substituion
        # doesn't rebuild the document tree
        soup = BeautifulSoup(str(soup))
        index += 1
    if update_content:
        return str(soup)
    return content

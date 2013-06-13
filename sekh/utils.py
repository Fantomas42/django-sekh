"""Utils for django-sekh"""
import re

from bs4 import BeautifulSoup

from sekh.settings import PROTECTED_MARKUPS
from sekh.settings import HIGHLIGHTING_PATTERN


def remove_duplicates(items):
    """Remove duplicates elements in a list preserving the order."""
    seen = {}
    result = []
    for item in items:
        if item in seen:
            continue
        seen[item] = True
        result.append(item)
    return result


def highlight(content, terms):
    """
    Highlight the HTML with BeautifulSoup
    """
    index = 1
    update_content = False
    soup = BeautifulSoup(content)
    for term in terms:
        pattern = re.compile(re.escape(term), re.I | re.U)

        for text in soup.body.find_all(text=pattern):
            if text.parent.name in PROTECTED_MARKUPS:
                continue

            def highlight(match):
                match_term = match.group(0)
                return HIGHLIGHTING_PATTERN % {
                    'index': index, 'term': match_term}

            new_text = pattern.sub(highlight, text)
            text.replace_with(BeautifulSoup(new_text))
            update_content = True
        # Reload the entire soup, because substituion
        # doesn't rebuild the document tree
        soup = BeautifulSoup(str(soup))
        index += 1
    if update_content:
        return str(soup)
    return content

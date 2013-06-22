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
        item = item.strip()
        if not item or item in seen:
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

        for text in soup.find_all(text=pattern):
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


def excerpt(content, terms, context=10):
    """
    Make a excerpt centered on the terms
    """
    from itertools import ifilter

    terms = map(re.escape, terms)
    exprs = [re.compile(r"^%s$" % t, re.I | re.U) for t in terms]
    whitespace = re.compile(r'\s+')

    re_template = r'(%s)'
    pieces = re.compile(re_template % "|".join(terms), re.I | re.U).split(content)
    matches = {}
    word_lists = []
    index = {}
    for i, piece in enumerate(pieces):
        word_lists.append(whitespace.split(piece))
        if i % 2:
            index[i] = expr = ifilter(lambda e: e.match(piece), exprs).next()
            matches.setdefault(expr, []).append(i)

    def merge(lists):
        merged = []
        for words in lists:
            if merged:
                merged[-1] += words[0]
                del words[0]
            merged.extend(words)
        return merged

    i = 0
    merged = []
    for j in map(min, matches.itervalues()):
        merged.append(merge(word_lists[i:j]))
        merged.append(word_lists[j])
        i = j + 1
    merged.append(merge(word_lists[i:]))

    output = []
    for i, words in enumerate(merged):
        omit = None
        if i == len(merged) - 1:
            omit = slice(max(1, 2 - i) * context + 1, None)
        elif i == 0:
            omit = slice(-context - 1)
        elif not i % 2:
            omit = slice(context + 1, -context - 1)
        if omit and words[omit]:
            words[omit] = ["..."]
        output.append(" ".join(words))

    return ''.join(output)

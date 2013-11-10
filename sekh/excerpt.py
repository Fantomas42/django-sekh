"""Excerpt for django-sekh"""
from sekh.utils import list_range
from sekh.utils import get_window
from sekh.utils import get_min_index
from sekh.utils import compile_terms
from sekh.settings import EXCERPT_MAX_LENGTH
from sekh.settings import EXCERPT_MATCH_WINDOW_SIZE


def generate_term_positions(splitted_content, terms):
    """
    Iterates over the words in the corpus and stores the locations of
    each matched query term. This data is structured as a list of lists,
    where each sub-list contains all of the positions for a matched query
    term.
    """
    positions = [[] for i in range(len(terms))]
    terms = compile_terms(sorted(terms))

    for i, word in enumerate(splitted_content):
        for term in terms:
            if term.match(word):
                positions[terms.index(term)].append(i)
                break

    return [x for x in positions if x]


def shortest_term_span(positions):
    """
    Given a list of positions in a corpus, returns
    the shortest span of words that contain all query terms.
    """
    # Initialize our list of lists where each list corresponds
    # to the locations within the document for a term
    indices = [0] * len(positions)
    min_window = window = get_window(positions, indices)

    # Iteratively moving the minimum index forward finds us our
    # minimum span
    while True:
        min_index = get_min_index(positions, window)

        if min_index is None:
            break

        indices[min_index] += 1

        window = get_window(positions, indices)

        if list_range(min_window) > list_range(window):
            min_window = window

        if list_range(min_window) == len(positions):
            break

    return sorted(min_window)


def shorten_excerpt(content, terms):
    """
    Iterates over the words in the excerpt and attempts to
    "close the gap" between matched terms in an overly long excerpt.
    Naive implementation.
    """
    flattened_excerpt_words = []
    last_term_appearence = 0
    skipping_words = False
    terms = compile_terms(terms)

    for i, word in enumerate(content.split()):

        # Spotted a matched term, set our state flag to false and update
        # the "time" of our last term appearance
        for term in terms:
            if term.match(word):
                last_term_appearence = i
                skipping_words = False

        # If it's been too long since our last match, start dropping words
        if i - last_term_appearence > EXCERPT_MATCH_WINDOW_SIZE:

            # Only want to add '...' once between terms,
            # so check our state flag first
            if not skipping_words:
                flattened_excerpt_words.append('...')
                skipping_words = True

            continue

        flattened_excerpt_words.append(word)

    return ' '.join(flattened_excerpt_words)


def excerpt(content, terms, max_length=EXCERPT_MAX_LENGTH):
    """
    Make a excerpt centered on the terms.
    """
    splitted_content = content.split()
    positions = generate_term_positions(splitted_content, terms)

    if not positions:
        return ' '.join(splitted_content[:max_length]).strip()

    span = shortest_term_span(positions)

    half_max_length = int(max_length / 2)
    start = max(0, span[0] - half_max_length)
    end = min(len(splitted_content), span[-1] + half_max_length)

    excerpt = ' '.join(splitted_content[start:end + 1])

    if (end - start > max_length):
        excerpt = shorten_excerpt(excerpt, terms)

    return excerpt

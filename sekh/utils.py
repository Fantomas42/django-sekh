"""Utils for django-sekh"""


def remove_duplicates(items):
    """
    Remove duplicates elements in a list preserving the order.
    """
    seen = {}
    result = []
    for item in items:
        item = item.strip()
        if not item or item in seen:
            continue
        seen[item] = True
        result.append(item)
    return result


def list_range(x):
    """
    Returns the range of a list.
    """
    return max(x) - min(x)


def get_min_index(positions, window):
    """
    Given a list of lists representing term positions in a corpus,
    this returns the index of the min term, or nothing if None left.
    """
    for min_index in [window.index(i) for i in sorted(window)]:
        if window[min_index] < positions[min_index][-1]:
            return min_index
    return None

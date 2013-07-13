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

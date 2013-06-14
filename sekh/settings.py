"""Settings for django-sekh"""
from django.conf import settings

GET_VARNAMES = getattr(
    settings, 'HIGHLIGHT_GET_VARNAMES',
    ('highlight', 'hl', 'q', 'query', 'pattern'))

PROTECTED_MARKUPS = getattr(
    settings, 'HIGHLIGHT_PROTECTED_MARKUPS',
    ('code', 'script', 'pre'))

HIGHLIGHTING_PATTERN = getattr(
    settings, 'HIGHLIGHT_HIGHLIGHTING_PATTERN',
    '<span class="highlight term-%(index)s">%(term)s</span>')
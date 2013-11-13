"""Settings for the sekh demo"""
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_URL = '/static/'

SECRET_KEY = 'secret-key'

ROOT_URLCONF = 'sekh.demo.urls'

MIDDLEWARE_CLASSES = (
    'sekh.middleware.KeywordsHighlightingMiddleware',
    )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    PROJECT_ROOT,
)

INSTALLED_APPS = (
    'sekh',
)

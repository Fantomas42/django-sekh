"""Settings for testing django-sekh"""

DATABASES = {
    'default': {'NAME': ':memory:',
                'ENGINE': 'django.db.backends.sqlite3'}}

INSTALLED_APPS = ['sekh']

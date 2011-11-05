===========
Django-SEKH
===========

Django Search Engine Keywords **Highlighter**,

is a middleware for Django providing the capacities to highlight the user's
search keywords if he is coming from a search engine like Google, Yahoo or
a custom search form plugged in your Website.

It retrieves the keywords of the search and decorate them with a ``span``
markup containing the classes ``highlight term-X`` for CSS makuping.

.. contents::

Installation
============

First of all you need to install `BeautifulSoup`_ >= 3.2.0.

Then install the package in your ``PYTHON_PATH`` by getting the
sources and run ``setup.py`` or use ``pip``. ::

  $ pip install -e git://github.com/Fantomas42/django-sekh.git#egg=django-sekh

Usage
=====

In your settings file, simply add this middleware at the end of the list. ::

  MIDDLEWARE_CLASSES = (
    ...
    'sekh.middleware.KeywordsHighlightingMiddleware',
    )

This is it !

Search Engines
==============

Currenty django-sekh support these following search engines :

* AltaVista
* Ask
* Google
* Live
* Lycos
* MSN
* Yahoo

Testin
=======

If you want to test the highlighter, you can pass keywords in the ``hl``
parameter in GET.

  http://localhost:8000/admin?hl=django%20admin

Caution
=======

If your HTML is not well formated, the middleware can fail and the page
will not be displayed.

.. _`BeautifulSoup`: http://www.crummy.com/software/BeautifulSoup/

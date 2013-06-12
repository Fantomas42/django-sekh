===========
Django-SEKH
===========

|latest-version| |downloads|

|travis-master| |coverage-master|

Django Search Engine Keywords **Highlighter**,

is a middleware for Django providing the capacities to highlight the user's
search keywords if he is coming from a search engine like Google, Yahoo or
a custom search form plugged in your Website.

It retrieves the keywords of the search and decorate them with a ``span``
markup containing the classes ``highlight term-X`` for CSS makuping.

.. contents::

Installation
============

First of all you need to install `BeautifulSoup`_ == 3.2.0.

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

Currenty django-sekh supports these search engines :

* Ask
* Baidu
* Bing
* Google
* Hotbot
* Lycos
* Yahoo

And even if you have a custom search engine plugged on your website,
``sekh`` can highlight the searched keywords. Currently ``sekh`` will
highlight all the terms contained in this list of GET variables :
::

    ['highlight', 'hl', 'q', 'query', 'pattern']

You can change the supported values by defining a variable named
``HIGHLIGHT_GET_VARNAMES`` representing a list of supported variable names
in your project's settings.

Testing
=======

If you want to test the highlighter, you can pass keywords in the ``hl``
parameter in GET.

  http://localhost:8000/admin?hl=django%20admin


.. |travis-master| image:: https://travis-ci.org/Fantomas42/django-sekh.png?branch=master
   :alt: Build Status - master branch
   :target: http://travis-ci.org/Fantomas42/django-sekh
.. |coverage-master| image:: https://coveralls.io/repos/Fantomas42/django-sekh/badge.png?branch=master
   :alt: Coverage of the code
   :target: https://coveralls.io/r/Fantomas42/django-sekh
.. |latest-version| image:: https://pypip.in/v/django-sekh/badge.png
   :alt: Latest version on Pypi
   :target: https://crate.io/packages/django-sekh/
.. |downloads| image:: https://pypip.in/d/django-sekh/badge.png
   :alt: Downloads from Pypi
   :target: https://crate.io/packages/django-sekh/

.. _`BeautifulSoup`: http://www.crummy.com/software/BeautifulSoup/

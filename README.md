django-sekh
===========

Django-**S**earch**E**ngine**K**eywords**H**ighlighter is a django middleware
providing the hability to highlight the user's search keywords if he comming
from a search engine.

It will retrieve the keywords of the search and decorate them 
with a **<span>** markup containing the classes "highlight term_X" for CSS makuping.

Install
-------

First of all, you need to install **BeautifulSoup**?

Then install the django-sekh package in your *PYTHON_PATH* as **sekh**.

Usage
-----

In your settings file, simply add this middleware at the end of the list :

    'sekh.middleware.KeywordsHighlightingMiddleware'

This is all !

Testing
-------

If you want to test the highlighter, you can pass keywords in the **hl** parameters in GET. :

    http://localhost/?hl=django
    http://localhost/?hl=toto titi tata

Caution
-------

If your HTML is not well formated, the middleware will certainly fail and the page
will not be displayed.
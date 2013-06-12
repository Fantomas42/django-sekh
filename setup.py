import os
from setuptools import setup, find_packages

import sekh

setup(
    name='django-sekh',
    version=sekh.__version__,

    description='Highlight the keywords of a page if a visitor ' \
    'is coming form a search engine.',
    long_description=open(os.path.join('README.rst')).read(),
    keywords='django, search engine, keyword, highlight',

    author=sekh.__author__,
    author_email=sekh.__email__,
    url=sekh.__url__,

    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',],

    license=sekh.__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires=['beautifulsoup4']
    )

from distutils.core import setup
import os

version = '0.1'

setup(name='django-sekh',
      version=version,
      
      description='Highlight the keywords of a page if a visitor is coming form a search engine.',
      long_description=open(os.path.join('README.rst')).read(),
      keywords='django, search engine, keyword, highlight',

      author='Fantomas42',
      author_email='fantomas42@gmail.com',
      url='http://github.com/Fantomas42/django-sekh',
      license='BSD License',

      packages=['sekh',],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: BSD License',
          'Topic :: Software Development :: Libraries :: Python Modules',],
      )




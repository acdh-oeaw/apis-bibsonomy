import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='apis-bibsonomy',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='Addon to the APIS system. Allows to manage references via Bibsonomy.',
    long_description=README,
    url='https://www.apis.acdh.oeaw.ac.at/',
    author='Matthias Schlögl, Peter Andorfer',
    author_email='matthias.schloegl@oeaw.ac.at, peter.andorfer@oeaw.ac.at',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=2.0',
        'apis-core>=0.9.22',
        'django-autocomplete-light>=3.2.10',
        'django-filter>=1.1.0',
        'django-reversion>=2.0.13',
        'djangorestframework>=3.7.7',
        'python-dateutil>=2.7.0',
        'requests>=2.18.4',
    ],
)


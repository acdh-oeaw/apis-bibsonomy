APIS Bibsonomy
==============

APIS Bibsonomy is a small addon to the APIS system. It allows to store references in Bibsonomy instances and use these references in APIS.
It is very generic and should work with most Django installations/projects.

Installation
------------

- Install the package:::

  pip install apis-bibsonomy

- Add the package to your installed apps:::

  INSTALLED_APPS = [
  ...
  'apis_bibsonomy'
  ]

- And migrate your DB:::

  python manage.py migrate

Configuration
-------------

APIS Bibsonomy needs an URL of the bibsonomy instance, a username, a API token and an (optional) collection to search in.

You need to add a configuration section to your APIS settings:::

APIS_BIBSONOMY = {
   'url': 'http://url.at',
   'user': 'username',
   'API key': 'api_key',
   'group': 'bibsonomy group'
}

Restart your server and you are good to go.


Usage
-----

- Include the base template somewhere in the header of your template:::

{% include 'apis_bibsonomy/apis_bibsonomy_include.html' %}

- Load the templatetag:::

{% load bibsonomy_templatetags %}

- Include the form somewhere in your template (set hidden=True if you intend to use buttons):::

{% bibsonomy_form content_type='person' hidden=True %}

- And finally add html tags as anker element for the reference forms to your template (dont forget to set "bibsonomy-anker" as class):::

<button class="bibsonomy-anker" data-bibs-contenttype="person" data-bibs-object_pk={{instance.pk}} data-bibs-attribute="Attribute name (optional)">Ref</button>


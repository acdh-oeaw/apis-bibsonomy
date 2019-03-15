APIS Bibsonomy
==============

APIS Bibsonomy is a small addon to the APIS system. It allows to store references in Bibsonomy instances and use these references in APIS.

Installation
------------

- Install the package:::

  pip install apis-bibsonomy

- Add the package to your installed apps:::

  INSTALLED_APPS = [
  ...
  'apis_bibsonomy'
  ]

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

# APIS Bibsonomy

APIS Bibsonomy is a small addon to the APIS system. It allows to store references in Bibsonomy instances and use these references in APIS.
It is very generic and should work with most Django installations/projects.

## Installation

- Install the package:

  `pip install apis-bibsonomy`

- Add the package to your installed apps:

  ```
  INSTALLED_APPS = [
  ...
  'apis_bibsonomy'
  ]
  ```

- And migrate your DB:

  `python manage.py migrate`


Some functionality from APIS Bibsonomy uses `htmx`, so you should [include htmx
into your web application](https://htmx.org/docs/#installing).


## Configuration


APIS Bibsonomy needs an URL of the bibsonomy or zotero instance, a username, a API token and an (optional) collection to search in.

You need to add a configuration section to your APIS settings:

```
APIS_BIBSONOMY = [{
   'type': 'bibsomomy', #or zotero
   'url': 'http://url.at', #url of the bibsonomy instance or zotero.org
   'user': 'username', #for zotero use the user id number found in settings
   'API key': 'api_key',
   'group': 'group'
}]
```

If you want the plugin to add the reference buttons to certain fields you need to add these fields to the config:

```
APIS_BIBSONOMY_FIELDS = ['name', 'first_name', 'profession']
```


Restart your server and you are good to go.


### htmx

APIS Bibsonomy uses htmx. The delete buttons for references trigger deletion
via the API delete route which give an empty response on success. HTMX needs to
be [configured to swap the content even if the response is empty](https://github.com/bigskysoftware/htmx/issues/199):
```
document.body.addEventListener('htmx:beforeSwap', function(event) {
  if (event.detail.xhr.status === 204) {
    // Swap content even when the response is empty.
    event.detail.shouldSwap = true;
  }
});
```


## Usage

*not needed if you are using standard APIS templates*

- Include the base template somewhere in the header of your template:

`{% include 'apis_bibsonomy/apis_bibsonomy_include.html' %}`

- Load the templatetag:

`{% load bibsonomy_templatetags %}`

- Include the form somewhere in your template (set hidden=True if you intend to use buttons):

`{% bibsonomy_form content_type='person' hidden=True %}`

- And finally add html tags as anker element for the reference forms to your template (dont forget to set "bibsonomy-anker" as class):

`<button class="bibsonomy-anker" data-bibs-contenttype="person" data-bibs-object_pk={{instance.pk}} data-bibs-attribute="Attribute name (optional)">Ref</button>`

- If you want to batch add reference forms to attribute fields in a whole form add a hidden anker element. You need to additionally add the names of the form fields you want to have reference forms for to `data-bibs-form-elements=""`

`<button class="bibsonomy-anker-hidden" data-bibs-contenttype="person" data-bibs-object_pk={{instance.pk}} data-bibs-form-elements="first_name|name|gender|start_date_written|lat">Ref</button>`


# Licenses

The *book* icon used for the reference link is the SVG from the [*Import Contacts* icon from the material symbols](https://fonts.google.com/icons?selected=Material+Symbols+Outlined:import_contacts:FILL@0;wght@400;GRAD@0;opsz@24&icon.query=book&icon.size=24&icon.color=%235f6368)

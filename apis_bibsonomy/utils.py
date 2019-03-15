import jmespath
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import json


class BibsonomyEntry:

    def __init__(self, bib_hash=None, bib_entry=None, entry_attrib=None):
        if entry_attrib is None:
            self._entry_attrib = ['authors', 'title', 'year', 'volume', 'test']
        if bib_hash is not None:
            headers = {'accept': 'application/json'}
            base_set = getattr(settings, "APIS_BIBSONOMY", None)
            if base_set is None:
                raise ValueError("You need to specify your APIS_BIBSONOMY settings.")
            self._user = base_set['user']
            self._api_key = base_set['API key']
            auth = HTTPBasicAuth(self._user, self._api_key)
            res = requests.get(bib_hash, auth=auth, headers=headers)
            if res.status_code == 200:
                art = res.json()
            else:
                raise ValueError('The entry could not be parsed.')
        elif bib_entry is not None:
            art = bib_entry
        else:
            raise ValueError('Either bib_hash or bib_entry need to be specified.')
        self.authors = jmespath.search('post.bibtex.author', art)
        self.title = jmespath.search('post.bibtex.title', art)
        self.year = jmespath.search('post.bibtex.year', art)
        self.volume = jmespath.search('post.bibtex.volume', art)
        self.bib_hash = jmespath.search('post.bibtex.href', art)
        self.bibtex = json.dumps(jmespath.search('post.bibtex'))

    def get_html(self):
        rows = ''
        for e in self._entry_attrib:
            if getattr(self, e, False):
                rows += '<tr><th scope="row">{}</th>\n<td>{}</td></tr>\n'.format(e, getattr(self, e))
        if len(rows) > 1:
            table = '<table class="table">\n<tbody>{}</tbody>\n</table>'.format(rows)
        else:
            table = None
        return table

    html = property(_get_html)

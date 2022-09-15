import jmespath
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import json


class BibsonomyEntry:


    def __init__(self, bib_hash=None, bib_entry=None, entry_attrib=None, base_set=None):
        if entry_attrib is None:
            self._entry_attrib = ['authors', 'title', 'year', 'volume']
        if bib_hash is not None:
            headers = {'accept': 'application/json'}
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
        self.bibtex = jmespath.search('post.bibtex', art)

    def get_html(self, include_table=False):
        rows = ''
        for e in self._entry_attrib:
            if getattr(self, e, False):
                rows += '<tr><th scope="row">{}</th>\n<td>{}</td></tr>\n'.format(e, self._get_str(getattr(self, e)))
        if len(rows) > 1 and include_table:
            table = '<table class="table">\n<tbody>{}</tbody>\n</table>'.format(rows)
        elif not include_table:
            table = rows
        else:
            table = None
        return table
    def get_autocomplete(self):
        res_str = "{} ({}): {}".format(self.authors, self.year, self.title)
        return res_str
    html = property(get_html)
    autocomplete = property(get_autocomplete)

import requests
from requests.auth import HTTPBasicAuth
import json

from django import http
from dal import autocomplete
from django.conf import settings
from .utils import BibsonomyEntry


class BibsonomyAutocomplete(autocomplete.Select2ListView):

    def get(self, request, *args, **kwargs):
        choices = []
        offset = (int(self.request.GET.get('page', 1))-1)*self.page_size
        url = '{}api/posts'.format(self.url)
        more = False
        if len(self.q) == 0:
            choices = []
        else:
            params = {'search': self.q, 'resourcetype': 'bibtex', 'start': offset,
                      'end': offset+self.page_size}
            headers = {'accept': 'application/json'}
            if self.group is not None:
                params['group'] = self.group
            auth = HTTPBasicAuth(self.user, self.api_key)
            r = requests.get(url, params=params, auth=auth, headers=headers)
            res = r.json()
            more = res['posts'].get('next', False)
            if 'post' in res['posts'].keys():
                for r in res['posts']['post']:
                    ent = BibsonomyEntry(bib_entry={'post': r})
                    choices.append({'id': ent.bib_hash, 'text': ent.autocomplete})
        if more:
            more = True
        return http.HttpResponse(json.dumps({
            'results': choices + [],
            'pagination': {'more': more}
        }), content_type='application/json')

    def __init__(self, page_size=20, group=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = page_size
        conf = getattr(settings, "APIS_BIBSONOMY", None)
        if 'group' in conf.keys():
            self.group = conf['group']
        else:
            self.group = None
        if 'user' in conf.keys():
            self.user = conf['user']
        else:
            raise ValueError('You need to specify a User.')
        if 'API key' in conf.keys():
            self.api_key = conf['API key']
        else:
            raise ValueError('You need to specify a API key to access the server.')
        if 'url' in conf.keys():
            self.url = conf['url']
        else:
            raise ValueError('You need to specify a BASE url of the Bibsonomy instance.')

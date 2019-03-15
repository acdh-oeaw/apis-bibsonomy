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
        url = '{}/api/posts'.format(self.url)
        params = {'search': self.q, 'resourcetype': 'bibtex', 'start': offset,
                  'end': offset+self.page_size}
        headers = {'accept': 'application/json'}
        auth = HTTPBasicAuth(self.user.split(':')[0], self.api_key)
        res = requests.get(url, params=params, auth=auth, headers=headers).json()
        more = res['posts'].get('next', False)
        for r in res['posts']['post']:
            ent = BibsonomyEntry(bib_entry={'post': r})

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
            self.user = conf['url']
        else:
            raise ValueError('You need to specify a BASE url of the Bibsonomy instance.')

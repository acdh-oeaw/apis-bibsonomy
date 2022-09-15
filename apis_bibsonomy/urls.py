from django.urls import path
from . import api_views
from . import autocompletes

app_name = 'apis_bibsonomy'

urlpatterns = [
    path('save_get/', api_views.SaveBibsonomyEntry.as_view(), name='savegetbibsonomyentry'),
    path('autocomplete/', autocompletes.BibsonomyAutocomplete.as_view(), name='bibsonomyautocomplete')
]


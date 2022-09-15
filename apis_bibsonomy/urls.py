from django.urls import path
from . import api_views
from . import autocompletes

app_name = 'apis_bibsonomy'

urlpatterns = [
    path('save_get/', api_views.SaveCitationEntry.as_view(), name='savegetcitationentry'),
    path('autocomplete/', autocompletes.CitationsAutocomplete.as_view(), name='citationautocomplete')
]


from django.urls import path
from . import api_views

app_name = 'apis_bibsonomy'

urlpatterns = [
    path('save/', api_views.SaveBibsonomyEntry, name='savebibsonomyentry'),
]


from rest_framework.routers import DefaultRouter
from django.urls import path
from . import api_views, views
from . import autocompletes

app_name = 'apis_bibsonomy'

urlpatterns = [
    path('save_get/', api_views.SaveBibsonomyEntry.as_view(), name='savegetbibsonomyentry'),
    path('autocomplete/', autocompletes.BibsonomyAutocomplete.as_view(), name='bibsonomyautocomplete'),
    path('references/', views.ReferenceListView.as_view(), name='referencelist'),
    path('references/<int:pk>', views.ReferenceDetailView.as_view(), name='referencedetail'),
    path('references/<int:pk>/delete', views.ReferenceDeleteView.as_view(), name='referencedelete'),
]

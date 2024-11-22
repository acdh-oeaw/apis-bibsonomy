from rest_framework import routers
from django.urls import include, path
from . import api_views, views
from . import autocompletes

app_name = "apis_bibsonomy"

router = routers.DefaultRouter()
router.register(r"references", api_views.ReferenceViewSet)

urlpatterns = [
    path(
        "autocomplete/",
        autocompletes.BibsonomyAutocomplete.as_view(),
        name="bibsonomyautocomplete",
    ),
    path("references/", views.ReferenceListView.as_view(), name="referencelist"),
    path(
        "references/<int:pk>",
        views.ReferenceDetailView.as_view(),
        name="referencedetail",
    ),
    path(
        "references/<int:pk>/update",
        views.ReferenceUpdateView.as_view(),
        name="referenceupdate",
    ),
    path(
        "references/<int:pk>/delete",
        views.ReferenceDeleteView.as_view(),
        name="referencedelete",
    ),
    path(
        "referenceson/<int:contenttype>/<int:pk>",
        views.ReferenceOnListView.as_view(),
        name="referenceonlist",
    ),
    path(
        "referenceson/<int:contenttype>/<int:pk>/modal",
        views.ReferenceOnListViewModal.as_view(),
        name="referenceonlistmodal",
    ),
    path("api/", include(router.urls)),
]

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from .models import Reference
from .serializers import ReferenceSerializer


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

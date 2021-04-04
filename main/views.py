from django.http import HttpResponse
from .models import Categories, Pictures
from .serialize import CategoriesSerializer, PicturesSerializer
from rest_framework import generics, renderers


# categories
class CategoriesListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filterset_fields = ['id']
    renderer_classes = [renderers.JSONRenderer]


class CategoriesUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class CategoriesDeleteView(generics.DestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


# pictures
class PicturesListCreateView(generics.ListCreateAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer
    filterset_fields = ['name', 'author', 'id']
    renderer_classes = [renderers.JSONRenderer]


class PicturesUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


class PicturesDeleteView(generics.DestroyAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer

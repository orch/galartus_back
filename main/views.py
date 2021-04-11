from django.http import HttpResponse
from .models import Categories, Pictures
from .serialize import CategoriesSerializer, PicturesSerializer
from rest_framework import generics, renderers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


# categories
class CategoriesListView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filterset_fields = ['id', 'name']


class CategoriesCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CategoriesUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class CategoriesDeleteView(generics.DestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


# pictures
class PicturesListView(generics.ListAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer
    filterset_fields = ['name', 'author', 'id', 'categories']


class PicturesCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = PicturesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class PicturesUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer


class PicturesDeleteView(generics.DestroyAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer

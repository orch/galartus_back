from django.http import HttpResponse
from .models import Categories, Pictures
from .serialize import CategoriesSerializer, PicturesSerializer
from rest_framework import generics, renderers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import os


# categories
class CategoriesListView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filterset_fields = ['id', 'name']


class CategoriesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return Categories.objects.get(pk=pk)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        categories = self.get_object(pk)

        os.remove(categories.image.path)

        serializer = CategoriesSerializer(categories, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categories = self.get_object(pk)
        if os.path.isfile(categories.image.path):
            os.remove(categories.image.path)

        categories.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# pictures
class PicturesListView(generics.ListAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer
    filterset_fields = ['name', 'author', 'id', 'categories']


class PicturesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return Pictures.objects.get(pk=pk)

    def post(self, request):
        serializer = PicturesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        pictures = self.get_object(pk)

        os.remove(pictures.image.path)

        serializer = PicturesSerializer(pictures, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pictures = self.get_object(pk)
        if os.path.isfile(pictures.image.path):
            os.remove(pictures.image.path)

        pictures.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

from django.http import HttpResponse
from .models import Categories, Pictures, Exhibitions, Likes
from .serialize import CategoriesSerializer, PicturesSerializer, \
                       ExhibitionsSerializer,  \
                       LikesReadSerializer, LikesWriteSerializer
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django_filters import rest_framework as filters
import os
from .permissions import StaffAndAdmin, UserOnly
import json


# Categories
class CategoriesListView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filterset_fields = ['id', 'name']


class CategoriesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [StaffAndAdmin]

    def get_object(self, pk):
        return Categories.objects.get(pk=pk)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        categories = self.get_object(pk)

        if os.path.isfile(categories.image.path) and request.data.get('image'):
            os.remove(categories.image.path)

        serializer = CategoriesSerializer(categories, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categories = self.get_object(pk)
        if os.path.isfile(categories.image.path):
            os.remove(categories.image.path)

        categories.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Pictures
class PicturesListView(generics.ListAPIView):
    queryset = Pictures.objects.all()
    serializer_class = PicturesSerializer
    filterset_fields = ['name', 'author', 'id', 'categories']


class PicturesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [StaffAndAdmin]

    def get_object(self, pk):
        return Pictures.objects.get(pk=pk)

    def post(self, request):
        serializer = PicturesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        pictures = self.get_object(pk)

        if os.path.isfile(pictures.image.path) and request.data.get('image'):
            os.remove(pictures.image.path)

        serializer = PicturesSerializer(pictures, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pictures = self.get_object(pk)
        if os.path.isfile(pictures.image.path):
            os.remove(pictures.image.path)

        pictures.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Exhibitions
class ExhibitionsFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Exhibitions
        fields = ['name', 'id', 'categories', 'date', 'time', 'min_price', 'max_price', 'weekday']


class ExhibitionsListView(generics.ListAPIView):
    queryset = Exhibitions.objects.all()
    serializer_class = ExhibitionsSerializer
    filterset_class = ExhibitionsFilter


class ExhibitionsView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [StaffAndAdmin]

    def get_object(self, pk):
        return Exhibitions.objects.get(pk=pk)

    def post(self, request):

        serializer = ExhibitionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        exhibition = self.get_object(pk)

        if os.path.isfile(exhibition.image.path) and request.data.get('image'):
            os.remove(exhibition.image.path)

        serializer = ExhibitionsSerializer(exhibition, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        exhibition = self.get_object(pk)
        if os.path.isfile(exhibition.image.path):
            os.remove(exhibition.image.path)

        exhibition.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Likes
# class LikesListView(generics.ListAPIView):
#     queryset = Likes.objects.all()
#     serializer_class = LikesReadSerializer
    # filterset_fields = ['account']


class LikesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [UserOnly]

    def get_object(self, pk):
        return Likes.objects.get(pk=pk)

    def post(self, request):
        user_id = request.user.id
        request.data._mutable = True
        request.data['account'] = user_id
        request.data._mutable = False
        serializer = LikesWriteSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        likes = Likes.objects.filter(account=user)
        serializer = LikesReadSerializer(likes, many=True)

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = request.user
        like_to_delete = Likes.objects.get(account=user, picture=pk)
        like_to_delete.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# class LikesDeleteView(generics.DestroyAPIView):
#     queryset = Likes.objects.all()
#     serializer_class = LikesWriteSerializer
#     permission_classes = [UserOnly]






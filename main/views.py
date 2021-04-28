from django.http import HttpResponse
from .models import Categories, Pictures, Exhibitions, Likes  #, Accounts
from .serialize import CategoriesSerializer, PicturesSerializer, \
                       ExhibitionsSerializer,  \
                       LikesReadSerializer, LikesWriteSerializer
                       #UsersSerializer, AccountsSerializer,
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django_filters import rest_framework as filters
import os


# User
# class UserListView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UsersSerializer


# Categories
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
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        categories = self.get_object(pk)

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


# Accounts
# class AccountsListView(generics.ListAPIView):
#     queryset = Accounts.objects.all()
#     serializer_class = AccountsSerializer
#     filterset_fields = ['nick_name']
#
#
# class AccountsView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#
#     def get_object(self, pk):
#         return Accounts.objects.get(pk=pk)
#
#     def post(self, request):
#
#         serializer = AccountsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         account = self.get_object(pk)
#
#         if os.path.isfile(account.image.path):
#             os.remove(account.image.path)
#
#         serializer = AccountsSerializer(account, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         account = self.get_object(pk)
#
#         if account.image and os.path.isfile(account.image.path):
#             os.remove(account.image.path)
#
#         account.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Likes
class LikesListView(generics.ListAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesReadSerializer
    filterset_fields = ['account']


class LikesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return Likes.objects.get(pk=pk)

    def post(self, request):
        serializer = LikesWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikesDeleteView(generics.DestroyAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesWriteSerializer


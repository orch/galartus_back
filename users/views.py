from django.shortcuts import render
from rest_framework.views import APIView
from .serialize import UsersPutSerializer, UsersPostSerializer
from .models import NewUser
from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import os
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser


class UsersListView(generics.ListAPIView):
    queryset = NewUser.objects.all()
    serializer_class = UsersPostSerializer


class UsersView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer(self, request, account=None):
        if self.request.method == 'PUT':
            serializer_class = UsersPutSerializer(account, data=request.data, partial=True)
        else:
            serializer_class = UsersPostSerializer(data=request.data)
        return serializer_class

    def get_object(self, pk):
        return NewUser.objects.get(pk=pk)

    def post(self, request, format='json'):
        serializer = self.get_serializer(request)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        account = self.get_object(pk)

        if account.image:
            if os.path.isfile(account.image.path):
                os.remove(account.image.path)

        serializer = self.get_serializer(request, account)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = self.get_object(pk)

        if account.image and os.path.isfile(account.image.path):
            os.remove(account.image.path)

        request.data['is_active'] = False
        serializer = UsersPutSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class BlackListView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from users.models import NewUser
from rest_framework.views import APIView
from .serialize import UsersSerializer
from django.http import HttpResponse
from rest_framework import status


class UsersView(APIView):
    def post(self, request, format='json'):
        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

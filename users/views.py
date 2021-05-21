from django.shortcuts import render
from rest_framework.views import APIView
from .serialize import UsersPutSerializer, UsersPostSerializer
from main.serialize import LikesReadSerializer, ExhibitionsSerializer
from .models import NewUser
from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import os
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from main.models import Likes, Exhibitions
from main.permissions import StaffOrAdminOrUser
import json


# class UsersListView(generics.ListAPIView):
#     queryset = NewUser.objects.all()
#     serializer_class = UsersPostSerializer
#     permission_classes = [IsAuthenticated]
#     filterset_fields = ['email']


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

        if os.path.isfile(account.image.path) and request.data.get('image'):
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

        # account.delete()
        # return HttpResponse(status=status.HTTP_204_NO_CONTENT)

        request.data['is_active'] = False
        serializer = UsersPutSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user.email
        account = NewUser.objects.filter(email=user)
        serializer = UsersPostSerializer(account, many=True, context={'request': request})

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


class BlackListView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class RecommendationView(APIView):
    permission_classes = [StaffOrAdminOrUser]

    def get_top_likes(self, dict):
        top_likes = []

        try:
            max_key = max(dict, key=dict.get)
            top_likes.append(max_key)
            del dict[max_key]

            max_key = max(dict, key=dict.get)
            top_likes.append(max_key)
            del dict[max_key]

            max_key = max(dict, key=dict.get)
            top_likes.append(max_key)
            del dict[max_key]
        except:
            pass

        return top_likes

    def get(self, request):
        user = request.user
        like_categories = []
        likes = Likes.objects.filter(account=user.id)

        like_serializer = LikesReadSerializer(likes, many=True)

        for like in like_serializer.data:
            for key, value in like['picture'].items():
                if key == 'categories':
                    like_categories.extend(value)

        auxiliary_list = list(set(like_categories))
        auxiliary_dict = dict.fromkeys(auxiliary_list, 0)

        for categ in like_categories:
            auxiliary_dict[categ] += 1

        top_likes = self.get_top_likes(auxiliary_dict)

        exhibitions = Exhibitions.objects.filter(categories__in=top_likes).distinct()
        exhib_serializer = ExhibitionsSerializer(exhibitions, many=True, context={'request': request})

        return HttpResponse(json.dumps(exhib_serializer.data), status=status.HTTP_200_OK)



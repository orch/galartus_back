from django.shortcuts import render
from rest_framework import generics
from main.models import Exhibitions
from .models import Cart, CartLine
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import status
from main.permissions import UserOnly, StaffOrAdminOrUser, StaffOrAdmin
from .serializer import CartSerializer
import json


class CartView(APIView):
    permission_classes = [StaffOrAdminOrUser]

    def put(self, request, pk, quantity):
        exhibition = Exhibitions.objects.get(id=pk)
        user = request.user
        order_item = CartLine.create(exhibition, quantity,
                                     quantity*exhibition.price)
        order_item.save()
        order, status_tmp = Cart.objects.get_or_create(account=user, is_ordered=False)
        order.items.add(order_item)
        order.amount = Cart.get_cart_amount(order)
        order.save()

        return HttpResponse(request.data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        user = request.user
        order = Cart.objects.get(account=user, is_ordered=False)

        item_to_delete = order.items.get(id=item_id)
        item_to_delete.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        user = request.user
        get_data = request.query_params.get('is_ordered')
        if not get_data:
            is_ordered = 0
        else:
            is_ordered = get_data
        orders = Cart.objects.filter(account=user, is_ordered=is_ordered)
        serializer = CartSerializer(orders, many=True, context={'request': request})

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


class CartPaymentView(APIView):
    permission_classes = [StaffOrAdminOrUser]

    def put(self, request):
        user = request.user
        try:
            order = Cart.objects.get(account=user, is_ordered=False)
        except:
            return HttpResponse(request.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        order.is_ordered = True
        order.save()

        return HttpResponse(request.data, status=status.HTTP_200_OK)


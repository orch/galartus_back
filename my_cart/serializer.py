from rest_framework import serializers
from .models import Cart, CartLine
from main.serialize import ExhibitionsSerializer


class CartLineSerializer(serializers.ModelSerializer):
    exhibition = ExhibitionsSerializer(many=False)

    class Meta:
        model = CartLine
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartLineSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'




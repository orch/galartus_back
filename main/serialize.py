from rest_framework import serializers
from .models import Categories, Pictures, \
                    Exhibitions,  Likes, \
                    CartLine, Cart


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = '__all__'


class ExhibitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibitions
        time = serializers.TimeField(input_formats='%H:%M')
        date = serializers.DateField(input_formats='%Y-%m-%d')
        fields = '__all__'


class LikesReadSerializer(serializers.ModelSerializer):
    picture = PicturesSerializer(many=False, read_only=True)

    class Meta:
        model = Likes
        fields = '__all__'


class LikesWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'


class CartLineSerializer(serializers.ModelSerializer):
    exhibitions = ExhibitionsSerializer(many=False, read_only=True)

    class Meta:
        model = CartLine
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_line = CartLineSerializer(many=False, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

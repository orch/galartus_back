from rest_framework import serializers
from .models import Categories, Pictures, \
                    Exhibitions, Accounts, Likes


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


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        date = serializers.DateField(input_formats='%Y-%m-%d')
        fields = '__all__'


class LikesSerializer(serializers.ModelSerializer):
    picture = PicturesSerializer(many=False, read_only=True)

    class Meta:
        model = Likes
        fields = '__all__'



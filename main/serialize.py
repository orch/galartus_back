from rest_framework import serializers
from .models import Categories, Pictures, Exhibitions


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

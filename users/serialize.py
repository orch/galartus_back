from rest_framework  import serializers
from users.models import NewUser


class UsersPostSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NewUser
        birthday = serializers.DateField(input_formats='%Y-%m-%d')
        read_only_fields = ('is_active', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'email', 'user_name', 'password', 'first_name',
                  'last_name', 'birthday', 'image', 'is_active', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UsersPutSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NewUser
        birthday = serializers.DateField(input_formats='%Y-%m-%d')
        read_only_fields = ('is_active', 'is_staff', 'user_name')
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'email', 'user_name', 'password', 'first_name',
                  'last_name', 'birthday', 'image', 'is_active', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

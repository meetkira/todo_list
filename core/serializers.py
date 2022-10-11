from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password_repeat = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat',)
        read_only_fields = ('id', 'user_status')

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password_repeat']:
            raise serializers.ValidationError({'password error': 'Passwords must match'})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о пользователе"""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)
        read_only_fields = ('id',)


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля пользователя"""
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'new_password', 'old_password',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        user = self.instance
        if not user.check_password(old_password):
            raise serializers.ValidationError({"password error": "Incorrect old password"})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор для авторизации пользователя"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',)
        read_only_fields = ('first_name', 'last_name', 'email',)

    def create(self, validated_data):
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password'],
        )):
            raise AuthenticationFailed
        return user

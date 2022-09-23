from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)
        read_only_fields = ('id',)


class ChangePasswordSerializer(serializers.Serializer):
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"login error": "Incorrect login or password"})
        attrs["user"] = user
        return attrs

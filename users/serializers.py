from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MyUser


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password], write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'address', 'phone_number', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = MyUser.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'user_type']
        extra_kwargs = {
            'user_type': {'read_only': True}
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect Current Password!')
        return value

    def validate(self, value):
        if value["new_password"] != value["confirm_new_password"]:
            raise serializers.ValidationError('New password fields are not matching!')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

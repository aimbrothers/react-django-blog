from django.contrib.auth import authenticate
from django.db import IntegrityError

from rest_framework import serializers

from .models import BackendUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label='Username', write_only=True)
    password = serializers.CharField(label='Password', style={
                                     'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get(
                'request'), username=username, password=password)

            if not user:
                msg = 'Access denied: wrong username or password.'

                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Both "username" and "password" are required.'

            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        label='Username', write_only=True, required=True)
    email = serializers.EmailField(
        label='Email', style={'input_type': 'email'}, write_only=True, required=True)
    password = serializers.CharField(label='Password', style={
                                     'input_type': 'password'}, trim_whitespace=True, write_only=True, required=True)
    password2 = serializers.CharField(label='Password confirmation', style={
        'input_type': 'password'}, trim_whitespace=True, write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if username and email and password and password2:
            if password != password2:
                msg = 'Passwords are not matching.'

                raise serializers.ValidationError(msg, code='authorization')

            user: BackendUser = None

            try:
                # Create user
                user = BackendUser.objects.create(
                    username=username,
                    email=email
                )
            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e.args):
                    msg = 'This username is already taken.'

                    raise serializers.ValidationError(
                        msg, code='authorization')

        else:
            msg = '"username", "email" or passwords are missing.'

            raise serializers.ValidationError(msg, code='authorization')

        user.set_password(password)
        user.save()
        attrs['user'] = user

        return attrs


class BackendUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackendUser
        fields = ('username', 'email')
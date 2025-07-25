from rest_framework import serializers
from .models import UsersInfo
import re
from django.contrib.auth.hashers import make_password

PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'


class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersInfo
        fields = '__all__'
        extra_kwargs = {
            # Don't ever return password back to clients
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        value = value.lower().strip()
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only @gmail.com emails are allowed.")
        return value

    def validate_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one digit, and one special character."
            )
        return value

    def validate_gender(self, value):
        if value not in (None, "", "male", "female"):
            raise serializers.ValidationError("Gender must be either 'male' or 'female'.")
        return value

    # --- Object-level hooks to hash password ---
    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        validated_data['password'] = make_password(raw_password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Only hash if password is being updated
        if 'password' in validated_data:
            raw_password = validated_data.pop('password')
            validated_data['password'] = make_password(raw_password)
        return super().update(instance, validated_data)

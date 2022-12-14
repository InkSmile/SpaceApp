from rest_framework.exceptions import ValidationError

from user.models import User


class ValidateEmailSerializerMixin:

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise ValidationError('User with this email address already exists....')
        return value


class ValidatePathSerializerMixin:

    def validate_path(self, path):
        return path.strip('/')

from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers

from user.models import User
from user.tasks import send_email
from user.tokens import TokenGenerator


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.email = user.email.lower()
        user.set_password(password)
        user.save()
        token = f'{urlsafe_base64_encode(force_bytes(user.email))}.{TokenGenerator.make_token(user)}'
        url = f'{settings.USER_ACTIVATION_URL}?token={token}'
        context = {
            'url': url,
            'email': user.email
        }

        template = 'notifications/activate_user.html'
        send_email.delay(
            subject="Please activate your account",
            template=template,
            recipients=[user.email],
            context=context
        )
        return user

class ActivateUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    custom_fields = serializers.SerializerMethodField()

    def validate(self, attrs):
        token = attrs['token']
        error_text = f"Provided activation token '{token}' is not valid"
        try:
            email, token = token.split('.')
            email = force_str(urlsafe_base64_decode(email))
        except (TypeError, ValueError):
            raise serializers.ValidationError(error_text)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(error_text)

        if not TokenGenerator.check_token(user, token):
            raise serializers.ValidationError(error_text)

        attrs['email'] = email
        return attrs

    def activate_user(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()
        return user
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.serializers import SignUpSerializer, ActivateUserSerializer


class ObtainJSONWebToken(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RefreshJSONWebToken(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class SignUpView(CreateAPIView):
    """
    post:
    Create new user with entered credentials
    Create new user with entered credentials
    """
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )


class ActivateUserView(APIView):
    """
    post:
    Activate user view
    Activate user using token that user get in its email
    """
    serializer_class = ActivateUserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=ActivateUserSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.activate_user()
        token = RefreshToken.for_user(user)
        return Response(data={
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        }, status=status.HTTP_200_OK)


class VerifyJSONWebToken(TokenVerifyView):
    """
    post:
    Verify your token (is it valid?)
    To work with API you need to have valid (verified) token which you get after visiting `/auth/token-verify`
    url, entering your token.[Read JWT docs](https://jwt.io/)
    ### Examples
    If data is successfully processed the server returns status code `200`.
    ```json
    {
        "token": "emskdlgnkngdDFHGergergEGRerRGEgerERE346346vergd456456"
    }
    ```
    ### Errors
    If there were some error in client data, it sends status code `401` with the error message looks like:
    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    serializer_class = TokenVerifySerializer

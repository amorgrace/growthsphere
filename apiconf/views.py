from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializers, FinancesSerializers
from .models import Finances
from rest_framework.response import Response
from dj_rest_auth.views import LoginView as DjRestLoginView
from rest_framework import status
from dj_rest_auth.serializers import JWTSerializer
from dj_rest_auth.utils import jwt_encode
from .serializers import CustomUserDetailsSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializers
    permission_classes = [AllowAny]


class CustomLoginView(DjRestLoginView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)

        self.user = self.serializer.validated_data['user']
        self.access_token, self.refresh_token = jwt_encode(self.user)

        return self.get_response()

    def get_response(self):
        return Response({
            'access': str(self.access_token),
            'refresh': str(self.refresh_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)

class UserFinancesView(ListAPIView):
    serializer_class = FinancesSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Finances.objects.filter(user=self.request.user)
    

class CustomUserDetailsView(RetrieveAPIView):
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
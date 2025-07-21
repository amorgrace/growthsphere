from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializers, FinancesSerializers, KYCSerializer
from .models import Finances, RecentTransaction, KYC
from rest_framework.response import Response
from dj_rest_auth.views import LoginView as DjRestLoginView, APIView
from rest_framework import status
from dj_rest_auth.serializers import JWTSerializer
from drf_yasg.utils import swagger_auto_schema
from dj_rest_auth.utils import jwt_encode
from .serializers import CustomUserDetailsSerializer, RecentTransactionSerializer, ChangePasswordSerializer
from rest_framework.parsers import MultiPartParser, FormParser

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
    
class UserTransactionListView(ListAPIView):
    serializer_class = RecentTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecentTransaction.objects.filter(user=self.request.user).order_by('-date')
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if not user.check_password(current_password):
            return Response({'error': 'Current Password is Incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    

class KYCUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        kyc_instance = KYC.objects.filter(user=request.user).first()
        if not kyc_instance:
            return Response({'detail': 'No KYC submitted yet.', 'status': 'pending'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = KYCSerializer(kyc_instance)
        return Response({
            'kyc_data': serializer.data,
            'status': kyc_instance.status,
            'message': f'KYC status is "{kyc_instance.status}".'
        }, status=status.HTTP_200_OK)

    def post(self, request):
        kyc_instance = KYC.objects.filter(user=request.user).first()

        serializer = KYCSerializer(data=request.data, instance=kyc_instance)
        if serializer.is_valid():
            kyc = serializer.save(user=request.user)

            if kyc.status == "pending":
                kyc.status = "in_review"
                kyc.save()
                message = 'KYC submitted successfully and is now under review.'
            elif kyc.status == "approved":
                message = 'KYC already approved. No further action required.'
            elif kyc.status == "rejected":
                message = 'KYC was rejected. Please contact support before resubmitting.'

            return Response({
                'detail': message,
                'status': kyc.status
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from .models import CustomUser, Finances, RecentTransaction, KYC
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    investment_goal = serializers.CharField(required=False)
    risk_tolerance = serializers.CharField(required=False)
    account_type = serializers.CharField(required=False)
    choose_trades = serializers.CharField(required=False)
    country = serializers.CharField(required=False)  # ✅ Add this


    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.pop('username', None)
        data.update({
            # 'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'investment_goal': self.validated_data.get('investment_goal', ''),
            'risk_tolerance': self.validated_data.get('risk_tolerance', ''),
            'account_type': self.validated_data.get('account_type', ''),
            'choose_trades': self.validated_data.get('choose_trades', ''),
            'country': self.validated_data.get('country', ''),  # ✅ Add this
        })
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.investment_goal = self.cleaned_data.get('investment_goal')
        user.risk_tolerance = self.cleaned_data.get('risk_tolerance')
        user.account_type = self.cleaned_data.get('account_type')
        user.choose_trades = self.cleaned_data.get('choose_trades')
        user.country = self.cleaned_data.get('country')  # ✅ Add this
        user.save()
        return user
    
class FinancesSerializers(serializers.ModelSerializer):
    total_balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Finances
        fields = [
            'total_deposit', 'total_profit', 'total_balance'
        ]

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'pk',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'investment_goal',
            'risk_tolerance',
            'account_type',
            'choose_trades',
            'country',
        ]

class RecentTransactionSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField()

    class Meta:
        model = RecentTransaction
        fields = [
            'id',
            'transaction_id',
            'network',
            'type',
            'currency',
            'status',
            'amount',
            'date',
            'time_since_created',
        ]
        read_only_fields = ['transaction_id', 'date', 'time_since_created']

    def get_time_since_created(self, obj):
        return obj.time_since_created()
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['user', 'id_type', 'id_front_url', 'id_back_url', 'kyc_status']
        read_only_fields = ['user', 'kyc_status']

from rest_framework import serializers
from .models import CustomUser, Finances, RecentTransaction, KYC
from dj_rest_auth.serializers import UserDetailsSerializer


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'investment_goal',
            'risk_tolerance',
            'account_type',
            'choose_trades',
        ]
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
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

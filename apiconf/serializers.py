from rest_framework import serializers
from .models import CustomUser, Finances
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
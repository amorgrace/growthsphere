from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Finances, RecentTransaction

class FinancesInline(admin.TabularInline):
    model = Finances
    extra = 0
    readonly_fields = ('total_balance',)
    can_delete = False

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'account_type', 'kyc_status')
    list_filter = ('account_type', 'risk_tolerance', 'kyc_status')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        ("Login Info", {
            'fields': ('email', 'password')
        }),
        ("Personal Info", {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ("Investment Details", {
            'fields': ('investment_goal', 'risk_tolerance', 'account_type', 'choose_trades')
        }),
        ("KYC Details", {
            'fields': ('kyc_status', 'doc_type', 'kyc_photo')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    inlines = [FinancesInline]

@admin.register(Finances)
class FinancesAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'total_deposit', 'total_profit', 'total_balance_display')
    search_fields = ('user__email',)
    list_filter = ('user__account_type',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def total_balance_display(self, obj):
        return f"{obj.total_balance:.2f}"
    total_balance_display.short_description = 'Total Balance'


@admin.register(RecentTransaction)
class RecentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 'crypto_type', 'transaction_type',
        'transaction_status', 'amount', 'created_at', 'time_since_created'
    )
    search_fields = ('user__email', 'transaction_id')
    list_filter = ('crypto_type', 'transaction_type', 'transaction_status',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def time_since_created(self, obj):
        return obj.time_since_created()
    time_since_created.short_description = 'Time Since'
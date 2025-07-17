from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin, TabularInline
from .models import CustomUser, Finances, RecentTransaction, KYC

class FinancesInline(TabularInline):
    model = Finances
    extra = 0
    readonly_fields = ('total_balance',)
    can_delete = False
    show_change_link = True

class KYCInline(TabularInline):
    model = KYC
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('id_type', 'id_front', 'id_back', 'status')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'account_type')
    list_display_links = ('email', 'first_name', 'last_name')
    list_filter = ('account_type', 'risk_tolerance')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    list_per_page = 25
    list_max_show_all = 100

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
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    inlines = [FinancesInline, KYCInline]

@admin.register(Finances)
class FinancesAdmin(ModelAdmin):
    list_display = ('user_email', 'total_deposit', 'total_profit', 'total_balance_display')
    list_display_links = ('user_email',)
    search_fields = ('user__email',)
    list_filter = ('user__account_type',)
    list_per_page = 25
    list_max_show_all = 100

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def total_balance_display(self, obj):
        return f"{obj.total_balance:.2f}"
    total_balance_display.short_description = 'Total Balance'

@admin.register(RecentTransaction)
class RecentTransactionAdmin(ModelAdmin):
    list_display = (
        'user_email','transaction_id', 'network', 'type', 'currency',
        'status', 'amount', 'date', 'time_since_created'
    )
    list_display_links = ('user_email', 'transaction_id')
    search_fields = ('user__email', 'transaction_id')
    list_filter = ('network', 'type', 'status')
    list_per_page = 25
    list_max_show_all = 100

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def time_since_created(self, obj):
        return obj.time_since_created()
    time_since_created.short_description = 'Time Since'

@admin.register(KYC)
class KYCAdmin(ModelAdmin):
    list_display = ('user', 'id_type', 'status')
    list_filter = ('status', 'id_type')
    search_fields = ('user__email',)
    list_per_page = 25

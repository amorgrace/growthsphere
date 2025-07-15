from django.contrib import admin
from .models import CustomUser, Finances

admin.site.register(CustomUser)
@admin.register(Finances)
class FinancesAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'total_deposit', 'total_profit', 'total_balance_display')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def total_balance_display(self, obj):
        return f"{obj.total_balance:.2f}"
    total_balance_display.short_description = 'Total Balance'
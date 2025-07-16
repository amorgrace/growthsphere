from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        if not password:
            raise ValueError('Password must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] #This means that only email and password required by default because i already set the above

    objects = CustomUserManager()

    INVESTMENT_GOAL_CHOICES = [
        ('select_your_primary_goal', 'Select Your Primary Goal'),
        ('retirement_planning', 'Retirement Planning'),
        ('wealth_building', 'Wealth Building'),
        ('education_funding', 'Education Funding'),
        ('education_funding', 'Education Funding'),
        ('home_purchase', 'Home Purchase'),
        ('general_investing', 'General Investing'),
    ]

    investment_goal = models.CharField(
        max_length=50, 
        choices=INVESTMENT_GOAL_CHOICES, 
        default='select_your_primary_goal'
    )

    RISK_TOLERANCE_CHOICES = [
        ('select_your_risk_tolerance', 'Select Your Risk Tolerance'),
        ('conservative_low_risk', 'Conservative - Low Risk'),
        ('moderate_balanced_risk', 'Moderate - Balance Risk'),
        ('aggressive_high_risk', 'Aggressive - High Risk'),
    ]

    risk_tolerance = models.CharField(
        max_length=50,
        choices=RISK_TOLERANCE_CHOICES,
        default='select_your_risk_tolerance',
    )

    ACCOUNT_TYPE_CHOICES = [
        ('choose_account_type', 'Choose Account Type'),
        ('starter_plan', 'Starter Plan'),
        ('silver_plan', 'Silver Plan'),
        ('gold_plan', 'Gold Plan'),
    ]

    account_type = models.CharField(
        max_length=50,
        choices=ACCOUNT_TYPE_CHOICES,
        default='choose_account_type'
    )

    CHOOSE_TRADES_CHOICES = [
        ('crypto', 'Crypto'),
        ('crude', 'Crude'),
        ('gold', 'Gold'),
        ('stock', 'Stock'),
        ('cfd', 'CFD'),
        ('fx', 'FX'),
    ]

    choose_trades = models.CharField(
        max_length=20,
        choices=CHOOSE_TRADES_CHOICES,
    )

    
    KYC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS_CHOICES,
        default='pending'
    )

    DOCUMENT_TYPE_CHOICES = [
        ('passport', 'Passport'),
        ('drivers_license', "Driver's license"),
        ('national_id', 'National ID'),
    ]

    kyc_photo = models.ImageField(upload_to='kyc_photos/', null=True, blank=True)
    doc_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='passport'
    )

    def __str__(self):
        return self.email


class Finances(models.Model):
    total_deposit = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    total_profit = models.DecimalField(default=0, decimal_places=2, max_digits=15)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='finances')

    @property
    def total_balance(self):
        return self.total_deposit + self.total_profit
    
    def __str__(self):
        return f"{self.user.email} | Balance: {self.total_balance:.2f} | Deposit: {self.total_deposit:.2f} | Profit: {self.total_profit:.2f}"


class RecentTransaction(models.Model):
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('BSC', 'Binance Smart Chain'),
        ('AVAX', 'Avalanche'),
        ('MATIC', 'Polygon'),
    ]


    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    crypto_type = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    transaction_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.crypto_type} - {self.transaction_type}"

    def time_since_created(self):
        from django.utils.timesince import timesince
        return timesince(self.created_at) + " ago"
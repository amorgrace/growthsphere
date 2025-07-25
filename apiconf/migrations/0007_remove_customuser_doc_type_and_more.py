# Generated by Django 5.2.4 on 2025-07-17 23:04

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiconf', '0006_rename_created_at_recenttransaction_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='doc_type',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='kyc_photo',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='kyc_status',
        ),
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_type', models.CharField(choices=[('passport', 'Passport'), ('drivers_license', "Driver's license"), ('national_id', 'National ID')], default='passport', max_length=20)),
                ('id_front', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('id_back', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_review', 'In Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

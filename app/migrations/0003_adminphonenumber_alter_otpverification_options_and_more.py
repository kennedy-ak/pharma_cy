# Generated by Django 5.2 on 2025-06-03 06:39

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_dailysalessummary_monthlysalessummary_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(default='0557782728', max_length=15, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, help_text='Description of who this number belongs to', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Admin Phone Number',
                'verbose_name_plural': 'Admin Phone Numbers',
            },
        ),
        migrations.AlterModelOptions(
            name='otpverification',
            options={'verbose_name': 'OTP Verification', 'verbose_name_plural': 'OTP Verifications'},
        ),
        migrations.RemoveField(
            model_name='otpverification',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='otpverification',
            name='expires_at',
            field=models.DateTimeField(default=app.models.default_expiry),
        ),
        migrations.AddField(
            model_name='otpverification',
            name='admin_phone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.adminphonenumber'),
        ),
    ]

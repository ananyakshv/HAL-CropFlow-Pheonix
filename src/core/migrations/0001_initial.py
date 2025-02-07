# Generated by Django 5.1.3 on 2024-12-31 10:42

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(default='Unknown', max_length=50)),
                ('crop_name', models.CharField(max_length=100)),
                ('quantity_to_sell', models.IntegerField()),
                ('seeds_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fertilizer_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pesticide_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('machinery_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('labor_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('msp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('available_quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(max_length=100)),
                ('quantity_requested', models.PositiveIntegerField()),
                ('total_price', models.FloatField()),
                ('farmer_name', models.CharField(max_length=100)),
                ('farmer_contact', models.CharField(max_length=15)),
                ('farmer_location', models.CharField(max_length=100)),
                ('is_checked_out', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='farmer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

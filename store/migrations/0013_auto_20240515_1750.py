# Generated by Django 3.2.7 on 2024-05-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_customer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

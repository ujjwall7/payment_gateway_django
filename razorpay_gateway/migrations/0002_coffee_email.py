# Generated by Django 4.2.6 on 2023-11-02 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpay_gateway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

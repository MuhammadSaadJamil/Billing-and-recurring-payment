# Generated by Django 4.0.6 on 2022-07-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_usage_unit_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyerprofile',
            name='payment_authorized',
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='stripe_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
# Generated by Django 4.0.6 on 2022-07-28 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_buyerprofile_payment_authorized_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerprofile',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

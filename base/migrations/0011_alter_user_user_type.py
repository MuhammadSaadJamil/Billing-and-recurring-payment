# Generated by Django 3.2.14 on 2022-08-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('A', 'Admin'), ('B', 'buyer')], default=('A', 'Admin'), max_length=255),
        ),
    ]

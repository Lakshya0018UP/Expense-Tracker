# Generated by Django 5.0.6 on 2024-07-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_profile_expense_alter_profile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='expense',
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 4.1 on 2022-11-19 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0004_alter_tariff_distributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='distributor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
# Generated by Django 4.0.3 on 2022-03-27 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="price",
            field=models.DecimalField(
                decimal_places=4, max_digits=10
            ),
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-14 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0003_campaign_deleted_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campaign",
            name="price",
        ),
        migrations.AddField(
            model_name="campaign",
            name="spend",
            field=models.DecimalField(
                decimal_places=4, default=0, max_digits=10
            ),
        ),
    ]

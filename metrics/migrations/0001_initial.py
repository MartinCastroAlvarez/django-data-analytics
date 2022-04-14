# Generated by Django 4.0.3 on 2022-03-26 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("campaigns", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Metric",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "metric_type",
                    models.CharField(
                        choices=[("VI", "View"), ("CL", "Click")],
                        default="VI",
                        max_length=2,
                    ),
                ),
                ("step", models.IntegerField()),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="campaigns.campaign",
                    ),
                ),
            ],
        ),
    ]
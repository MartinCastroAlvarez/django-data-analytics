# Generated by Django 4.0.3 on 2022-03-27 00:09

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
        ("metrics", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="metric",
            name="step",
        ),
        migrations.AddField(
            model_name="metric",
            name="page",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="pages.page",
            ),
            preserve_default=False,
        ),
    ]
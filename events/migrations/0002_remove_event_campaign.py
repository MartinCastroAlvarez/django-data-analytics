# Generated by Django 4.0.3 on 2022-03-27 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="campaign",
        ),
    ]
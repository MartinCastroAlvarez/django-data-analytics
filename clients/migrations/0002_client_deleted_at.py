# Generated by Django 4.0.3 on 2022-03-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="deleted_at",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

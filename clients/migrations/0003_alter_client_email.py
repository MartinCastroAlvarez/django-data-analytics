# Generated by Django 4.0.3 on 2022-03-27 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0002_client_deleted_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="email",
            field=models.CharField(max_length=200),
        ),
    ]
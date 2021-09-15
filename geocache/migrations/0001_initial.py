# Generated by Django 3.2.7 on 2021-09-15 18:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlaceCache",
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
                ("address", models.CharField(max_length=100)),
                ("distance", models.FloatField()),
                (
                    "last_update",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
    ]

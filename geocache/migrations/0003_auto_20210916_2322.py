# Generated by Django 3.2.7 on 2021-09-16 20:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("geocache", "0002_auto_20210915_2256"),
    ]

    operations = [
        migrations.CreateModel(
            name="Place",
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
                (
                    "address",
                    models.CharField(max_length=100, verbose_name="Адрес"),
                ),
                ("lat", models.FloatField(verbose_name="Широта")),
                ("lon", models.FloatField(verbose_name="Долгота")),
                (
                    "last_update",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата последнего обновления",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PlaceCache",
        ),
    ]

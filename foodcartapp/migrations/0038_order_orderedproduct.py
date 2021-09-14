# Generated by Django 3.2.6 on 2021-09-14 12:52

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0037_auto_20210125_1833"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=30)),
                ("lastname", models.CharField(max_length=50)),
                (
                    "phonenumber",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=32, region=None
                    ),
                ),
                ("address", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
            },
        ),
        migrations.CreateModel(
            name="OrderedProduct",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ]
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="foodcartapp.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="order_position",
                        to="foodcartapp.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "позиция",
                "verbose_name_plural": "позиции",
            },
        ),
    ]

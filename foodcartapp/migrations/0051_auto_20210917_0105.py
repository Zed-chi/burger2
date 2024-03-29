# Generated by Django 3.2.7 on 2021-09-16 22:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0050_auto_20210917_0023"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.TextField(
                blank=True, default="", verbose_name="Комментарий к заказу"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="product_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=8,
                validators=[django.core.validators.MinValueValidator(0.1)],
                verbose_name="Цена товара",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=8,
                validators=[django.core.validators.MinValueValidator(0.1)],
                verbose_name="Общая цена",
            ),
        ),
    ]

# Generated by Django 3.0.7 on 2020-06-19 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0006_auto_20200619_0849"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="foodcartapp.Order",
                verbose_name="заказ",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders_items",
                to="foodcartapp.Product",
                verbose_name="товар",
            ),
        ),
    ]

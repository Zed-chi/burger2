# Generated by Django 3.2.7 on 2021-09-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("foodcartapp", "0047_order_restaurant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="is_processed",
            field=models.CharField(
                choices=[
                    ("Handled", "Обработано"),
                    ("Unhandled", "Необработано"),
                ],
                default="Unhandled",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment",
            field=models.CharField(
                choices=[("CASH", "Наличными"), ("CARD", "Электронно")],
                default="CASH",
                max_length=30,
            ),
        ),
    ]

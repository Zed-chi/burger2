# Generated by Django 3.2.7 on 2021-09-15 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0043_auto_20210915_1438"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.TextField(blank=True, default=""),
        ),
    ]

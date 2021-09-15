# Generated by Django 3.2.7 on 2021-09-15 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20210915_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена товара'),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='общая цена'),
        ),
    ]
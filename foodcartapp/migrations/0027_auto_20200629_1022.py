# Generated by Django 3.0.7 on 2020-06-29 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0026_restaurantmenuitem"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="restaurantmenuitem",
            unique_together={("restaurant", "product")},
        ),
    ]

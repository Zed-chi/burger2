# Generated by Django 3.2.6 on 2021-09-14 21:36

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_order_is_processed'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('price', django.db.models.manager.Manager()),
            ],
        ),
    ]
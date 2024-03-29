# Generated by Django 3.0.7 on 2020-06-19 09:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("foodcartapp", "0015_auto_20200619_0935"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="new_admin",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="administrated_restaurants",
                to=settings.AUTH_USER_MODEL,
                verbose_name="администратор",
            ),
        ),
    ]

# Generated by Django 3.2.2 on 2021-05-14 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0009_alter_orders_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='delivery',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]

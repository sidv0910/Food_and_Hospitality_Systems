# Generated by Django 3.2 on 2021-05-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0020_alter_orders_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

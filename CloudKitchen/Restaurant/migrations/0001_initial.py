# Generated by Django 3.2.2 on 2021-05-11 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Home', '0012_auto_20210511_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=1000)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.restaurant')),
            ],
        ),
    ]

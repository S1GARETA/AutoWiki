# Generated by Django 4.2.7 on 2023-11-13 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_brand', models.CharField(max_length=100)),
                ('car_model', models.CharField(max_length=100)),
                ('generation', models.CharField(max_length=100)),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-13 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendAPI_auto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название инструкции')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название раздела инструкции')),
            ],
        ),
        migrations.CreateModel(
            name='SubSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название подраздела')),
                ('content', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='auto',
            name='slug',
            field=models.SlugField(default=1, max_length=255, unique=True, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auto',
            name='car_brand',
            field=models.CharField(max_length=100, verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='car_model',
            field=models.CharField(max_length=100, verbose_name='Модель'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='generation',
            field=models.CharField(max_length=100, verbose_name='Поколение'),
        ),
    ]

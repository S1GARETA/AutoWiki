# Generated by Django 4.2.7 on 2023-11-14 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backendAPI_auto', '0005_alter_auto_instruction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auto',
            name='instruction',
        ),
        migrations.AddField(
            model_name='instruction',
            name='car',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='backendAPI_auto.auto'),
            preserve_default=False,
        ),
    ]

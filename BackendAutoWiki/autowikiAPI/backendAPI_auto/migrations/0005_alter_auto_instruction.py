# Generated by Django 4.2.7 on 2023-11-14 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backendAPI_auto', '0004_rename_instruction_id_auto_instruction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='instruction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backendAPI_auto.instruction'),
        ),
    ]

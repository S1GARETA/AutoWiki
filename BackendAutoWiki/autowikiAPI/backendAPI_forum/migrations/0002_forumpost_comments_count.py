# Generated by Django 4.2.7 on 2024-01-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendAPI_forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='comments_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Ответов'),
        ),
    ]

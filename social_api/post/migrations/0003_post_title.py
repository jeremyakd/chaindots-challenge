# Generated by Django 5.1.2 on 2024-10-27 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
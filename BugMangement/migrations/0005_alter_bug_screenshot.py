# Generated by Django 4.2.3 on 2023-08-28 21:45

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BugMangement', '0004_alter_project_developer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='screenshot',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]

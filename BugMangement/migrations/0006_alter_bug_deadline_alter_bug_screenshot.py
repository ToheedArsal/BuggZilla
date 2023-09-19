# Generated by Django 4.2.3 on 2023-08-30 13:36

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BugMangement', '0005_alter_bug_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bug',
            name='screenshot',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
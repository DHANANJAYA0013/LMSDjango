# Generated by Django 5.1.3 on 2025-01-31 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_remove_book_image_filename_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]

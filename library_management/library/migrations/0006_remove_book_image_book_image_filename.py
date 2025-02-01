# Generated by Django 5.1.3 on 2025-01-31 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_remove_book_image_filename_book_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.AddField(
            model_name='book',
            name='image_filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

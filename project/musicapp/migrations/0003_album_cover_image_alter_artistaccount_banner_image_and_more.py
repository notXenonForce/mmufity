# Generated by Django 5.1.4 on 2025-02-08 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0002_artistaccount_banner_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='album_covers/'),
        ),
        migrations.AlterField(
            model_name='artistaccount',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='banners/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='audio_file',
            field=models.FileField(upload_to='songs/'),
        ),
    ]

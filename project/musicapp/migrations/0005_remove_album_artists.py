# Generated by Django 5.1.4 on 2025-02-09 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0004_playlist_album_artists'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='artists',
        ),
    ]

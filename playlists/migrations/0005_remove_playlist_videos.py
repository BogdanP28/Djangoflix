# Generated by Django 3.2.25 on 2024-08-25 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0004_alter_playlist_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='videos',
        ),
    ]

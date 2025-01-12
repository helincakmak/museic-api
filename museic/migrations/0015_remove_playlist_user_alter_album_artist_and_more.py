# Generated by Django 5.1 on 2024-10-21 19:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museic', '0014_alter_album_artist_alter_album_cover_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='user',
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(help_text='Artist who created the album', on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='museic.artist'),
        ),
        migrations.AlterField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(blank=True, help_text='Cover image of the album', null=True, upload_to='albums/'),
        ),
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateField(blank=True, help_text='Release date of the album', null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(help_text='Title of the album', max_length=100),
        ),
        migrations.AlterField(
            model_name='artist',
            name='genre',
            field=models.CharField(help_text='Music genre of the artist', max_length=100),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(help_text="Artist's name", max_length=100),
        ),
        migrations.AlterField(
            model_name='artist',
            name='photo',
            field=models.ImageField(blank=True, help_text='Photo of the artist', null=True, upload_to='artists/'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date and time when the playlist was created'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the playlist', null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(help_text='Name of the playlist', max_length=100),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(help_text='Songs included in the playlist', related_name='playlists', to='museic.song'),
        ),
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, help_text='Album where the song is included', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='museic.album'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(help_text='Artist who performed the song', on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='museic.artist'),
        ),
        migrations.AlterField(
            model_name='song',
            name='cover_image',
            field=models.ImageField(blank=True, help_text='Cover image of the song', null=True, upload_to='covers/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.DurationField(help_text='Duration of the song in HH:MM:SS format'),
        ),
        migrations.AlterField(
            model_name='song',
            name='file',
            field=models.FileField(blank=True, help_text='Audio file of the song', null=True, upload_to='songs/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='release_date',
            field=models.DateField(blank=True, help_text='Release date of the song', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(help_text='Title of the song', max_length=100),
        ),
    ]

from django.utils.html import format_html
from django.contrib import admin
from .models import Artist, Album, Song, Playlist

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'photo_tag')

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))
        return "-"
    photo_tag.short_description = 'Photo'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'cover_image_tag')  # Fotoğrafı göstermek için yeni alan ekliyoruz

    def cover_image_tag(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.cover_image.url))
        return "-"
    cover_image_tag.short_description = 'Cover Image'

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'duration', 'release_date')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

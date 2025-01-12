from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import CustomUserManager  


class Artist(models.Model):
    name = models.CharField(max_length=100, help_text="Artist's name")
    genre = models.CharField(max_length=100, help_text="Music genre of the artist")
    photo = models.ImageField(upload_to='artists/', null=True, blank=True, help_text="Photo of the artist")

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100, help_text="Title of the album")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums", help_text="Artist who created the album")
    release_date = models.DateField(help_text="Release date of the album", null=True, blank=True)
    cover_image = models.ImageField(upload_to='albums/', null=True, blank=True, help_text="Cover image of the album")

    def __str__(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=100, help_text="Title of the song")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs", help_text="Artist who performed the song")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="album_songs", null=True, blank=True, help_text="Album where the song is included")
    duration = models.DurationField(help_text="Duration of the song in HH:MM:SS format")
    release_date = models.DateField(help_text="Release date of the song", null=True, blank=True)
    file = models.FileField(upload_to='songs/', null=True, blank=True, help_text="Audio file of the song")
    cover_image = models.ImageField(upload_to='songs/covers/', null=True, blank=True, help_text="Cover image of the song")

    def __str__(self):
        return self.title

    def clean(self):
        if self.file and not self.file.name.endswith(('.mp3', '.wav')):
            raise ValidationError("Only .mp3 or .wav files are allowed.")

class Playlist(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the playlist")
    description = models.TextField(help_text="Description of the playlist", blank=True, null=True)
    songs = models.ManyToManyField(Song, related_name="playlists", help_text="Songs included in the playlist")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the playlist was created")

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, default="Female")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Çakışmayı önlemek için 'related_name' ekleyin
        blank=True,
        help_text="The groups this user belongs to."
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Çakışmayı önlemek için 'related_name' ekleyin
        blank=True,
        help_text="Specific permissions for this user."
    )

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.forms import ValidationError
from .managers import CustomUserManager  
from django.conf import settings


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
    name = models.CharField(max_length=255, help_text="Name of the playlist")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the playlist")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Owner of the playlist")
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True, help_text="Songs included in the playlist")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the playlist was created")

    def __str__(self):
        return f"{self.name} by {self.user.username}"



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Kullanıcı oluştururken kullanılacak yardımcı fonksiyon.
        """
        if not email:
            raise ValueError('Email gerekli.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Süper kullanıcı oluştururken kullanılacak fonksiyon.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Kullanıcıya özel alanlar
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, default="Female")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # İstenilen diğer alanlar
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender']

    # Many-to-many ilişkiler
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

    # Kullanıcıyı str olarak göster
    def __str__(self):
        return self.username



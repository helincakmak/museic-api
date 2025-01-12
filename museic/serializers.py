from rest_framework import serializers
from .models import Song, Album, Artist, CustomUser

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()  # İlgili artist'in tüm verilerini döndür

    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()  # İlgili album'in tüm verilerini döndür
    artist = ArtistSerializer()  # İlgili artist'in tüm verilerini döndür
    cover_image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Song
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'gender', 'username']
        extra_kwargs = {
            'password': {'write_only': True},  # Şifreyi yalnızca yazılabilir yapıyoruz
        }

    def create(self, validated_data):
        # Yeni kullanıcıyı oluştururken şifreyi hash'liyoruz
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            gender=validated_data.get('gender'),
            username=validated_data.get('username')
        )
        return user

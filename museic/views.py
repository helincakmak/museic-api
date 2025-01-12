from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song, Album, Artist, CustomUser
from .serializers import SongSerializer, AlbumSerializer, ArtistSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from .models import Playlist
from .serializers import PlaylistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotAuthenticated





class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]  # Herkes kayıt olabilir

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.create_user(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],  # Şifre otomatik hashlenecek
                    gender=serializer.validated_data.get('gender'),
                    username=serializer.validated_data.get('username')
                )
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]  # Herkes giriş yapabilir

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Kullanıcı adı ve şifre gereklidir.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                return Response(
                    {
                        'message': 'Giriş başarılı!',
                        'username': user.username,
                        'email': user.email
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Bu kullanıcı aktif değil.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'error': 'Geçersiz kullanıcı adı veya şifre.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


# Artist API Views
class ArtistListCreate(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]  


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]  

# Album API Views
class AlbumListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.select_related('artist')
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]  


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.select_related('artist')
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]  

# Song API Views
class SongListCreate(generics.ListCreateAPIView):
    queryset = Song.objects.select_related('artist', 'album')
    serializer_class = SongSerializer
    permission_classes = [AllowAny]  


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.select_related('artist', 'album')
    serializer_class = SongSerializer
    permission_classes = [AllowAny]  


# Playlist API
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User must be logged in to create a playlist.")
        serializer.save(user=self.request.user)

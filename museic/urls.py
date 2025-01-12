from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArtistListCreate, ArtistDetail,
    AlbumListCreate, AlbumDetail,
    SongListCreate, SongDetail,
    UserLoginView, UserRegistrationView,
    PlaylistViewSet
)

# Router tanımı
router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    # API endpoint'leri
    path('artists/', ArtistListCreate.as_view(), name='artist-list-create'),
    path('artists/<int:pk>/', ArtistDetail.as_view(), name='artist-detail'),
    path('albums/', AlbumListCreate.as_view(), name='album-list-create'),
    path('albums/<int:pk>/', AlbumDetail.as_view(), name='album-detail'),
    path('songs/', SongListCreate.as_view(), name='song-list-create'),
    path('songs/<int:pk>/', SongDetail.as_view(), name='song-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    # Router'ı dahil et
    path('', include(router.urls)),

]

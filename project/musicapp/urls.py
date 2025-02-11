from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup_user/', views.signup_user, name='signup_user'),
    path('logout/', views.logout, name='logout'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('artist_home/', views.artist_home, name='artist_home'),
    path('album/', views.music_album, name='album'),
    path('tracks/', views.music_tracks, name='tracks'),
    path('player/', views.music_playlist, name='playlist'),
    path('signup_artist/', views.signup_artist, name='signup_artist'),
    path('search/', views.search, name='search'),
    path('user_home/', views.user_home, name='user_home'),
    path('artist/<int:pk>/', views.artist_detail, name='artist_detail'),  # Detail view for artists
    path('album/<int:pk>/', views.album_detail, name='album_detail'),    # Detail view for albums
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),    # Detail view for albums
    path('edit_song/<int:track_id>/', views.edit_song, name='edit_song'),
    path('search_music/', views.search_music_for_playlist, name='search_music_for_playlist'),
    path('playlist/<int:pk>/add_music/', views.add_music_to_playlist, name='add_music_to_playlist'),
    path('toggle_like/', views.toggle_like, name='toggle_like'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
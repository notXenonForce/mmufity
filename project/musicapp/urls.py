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
    path('signup_artist/', views.signup_artist, name='signup_artist'),
    path('search/', views.search, name='search'),
    path('user_home/', views.user_home, name='user_home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup_user', views.signup_user, name='signup_user'),
    path('signup_artist', views.signup_artist, name='signup_artist'),
    path('logout', views.logout, name='logout'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('artist_home', views.artist_home, name='artist_home'),
    path('music', views.music, name='music'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
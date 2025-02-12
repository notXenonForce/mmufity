from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UploadSongForm, AlbumForm, BannerUploadForm, PlaylistForm, EditSongForm, UserBannerUploadForm  # Import forms
from .models import Music, Album, ArtistAccount, Playlist, Like, UserAccount  # Import models
from .validators import validate_audio_file
from django.core.exceptions import ValidationError
from django.db.models import Max, Min
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import traceback  # Import traceback
from django.templatetags.static import static  # Import the static tag


# Helper functions for user type checks
def is_artist(user):
    return user.is_staff and not user.is_superuser  # Artists are is_staff but not is_superuser


def is_admin(user):
    return user.is_staff and user.is_superuser  # Admins are is_staff and is_superuser


def music_tracks(request):
    track_id = request.GET.get('track_id')
    album_id = request.GET.get('album_id')
    selected_track = None
    tracks = []
    album = None
    max_track_id = None
    first_track_id = None
    valid_track_ids = []

    try:
        # Attempt to get the user, if not then we will just provide null variable
        try:
            artist_account = ArtistAccount.objects.get(user=request.user)
        except:
            artist_account = None

        # Filter Music objects by the artist
        if artist_account == None:
            all_tracks = Music.objects.all().order_by('id')
        else:
            all_tracks = Music.objects.filter(artist=artist_account).order_by(
                'id')  # Removed Artist from Filter
        valid_track_ids = list(all_tracks.values_list('id', flat=True))  # Removed Artist from Filter

        # Get the maximum and minimum track IDs upfront.  Use None defaults to avoid errors
        if valid_track_ids:  # Only aggregate if there are tracks
            max_aggregate = all_tracks.aggregate(Max('id'), Min('id'))
            max_track_id = max_aggregate['id__max']
            first_track_id = max_aggregate['id__min']

        if track_id:
            try:
                selected_track = all_tracks.get(pk=track_id)
                album = selected_track.album
                tracks = all_tracks.filter(album=album)

            except Music.DoesNotExist:
                messages.error(request, "Track does not exist. Attempting to play another track.")
                selected_track = None
                tracks = []

        elif album_id:
            album = get_object_or_404(Album, pk=album_id)
            tracks = all_tracks.filter(album=album)
            selected_track = tracks.first() if tracks else None

        else:
            selected_track = all_tracks.first()
            tracks = all_tracks

    except Exception as e:
        messages.error(request, f"Error retrieving music: {e}")
        selected_track = None
        tracks = []

    context = {
        'selected_track': selected_track,
        'album': album,
        'tracks': tracks,
        'max_track_id': max_track_id,
        'first_track_id': first_track_id,
        'valid_track_ids': valid_track_ids,
    }

    return render(request, 'music_tracks.html', context)


def music_album(request):
    track_id = request.GET.get('track_id')  # Get track ID from query parameters
    album_id = request.GET.get('album_id')  # Get album ID from query parameters
    selected_track = None
    tracks = []

    if track_id:
        selected_track = get_object_or_404(Music, pk=track_id)
        album = selected_track.album if selected_track.album else None

    elif album_id:
        album = get_object_or_404(Album, pk=album_id)
        tracks = Music.objects.filter(album=album)
        selected_track = tracks[0] if tracks else None
    else:
        album = None
        selected_track = None

    context = {'selected_track': selected_track, 'album': album, 'tracks': tracks}
    return render(request, 'music_album.html', context)


def user_home(request):
    return render(request, 'profile_user.html')


def search(request):
    return render(request, 'search.html')


def music_playlist(request):
    track_id = request.GET.get('track_id')  # Get track ID from query parameters
    playlist_id = request.GET.get('playlist_id')  # Get playlist ID from query parameters #Changed variable
    selected_track = None
    album = None
    tracks = []
    playlist = None  # Define the playlist as None initially

    try:
        if track_id:
            selected_track = get_object_or_404(Music, pk=track_id)
            playlist = selected_track.playlist if selected_track.playlist else None
            album = selected_track.album if selected_track.album else None
        elif playlist_id:
            playlist = get_object_or_404(Playlist, pk=playlist_id,
                                          user=request.user.useraccount)  # Ensures only get what we are looking for
            tracks = playlist.music_set.all()  # Only look for the playlist and nothing more
            selected_track = tracks[0] if tracks else None
            album = selected_track.album if selected_track.album else None
    except Playlist.DoesNotExist:
        selected_track = None

    except Music.DoesNotExist:
        playlist = None  # If selected code is false, can't run
        selected_track = None  # If selected code is false, can't run
    except Exception as e:
        playlist = None
        selected_track = None

    context = {'selected_track': selected_track, 'playlist': playlist, 'tracks': tracks, 'album': album, }  # Changed code
    return render(request, 'music_playlist.html', context)  # Changed code


# Make sure you have the correct import statement
@login_required(login_url='login')
def user_home(request):
    if request.method == 'POST':
        playlist_form = PlaylistForm(request.POST, request.FILES)
        banner_form = UserBannerUploadForm(request.POST, request.FILES, instance=request.user.useraccount)
        if playlist_form.is_valid():
            playlist = playlist_form.save(commit=False)
            if request.user.is_authenticated:
                playlist.user = request.user.useraccount  # Assuming useraccount is the related name
                playlist.save()
            return redirect('user_home')  # Redirect to the same page
        elif banner_form.is_valid():
            banner_form.save()
            return redirect('user_home')
        else:
            print(playlist_form.errors)  # Print form errors
            print(banner_form.errors)

    else:  # GET request (initial page load)
        playlist_form = PlaylistForm()
        banner_form = UserBannerUploadForm(instance=request.user.useraccount)

    # Get playlists for the user
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user.useraccount)
    else:
        playlists = []

    context = {
        'playlist_form': playlist_form,
        'playlists': playlists,
        'banner_form': banner_form,  # Pass the banner form to the context
        'user': request.user,
    }
    return render(request, 'profile_user.html', context)  # Pass the context to the template


def search(request):
    search_term = request.GET.get('q', '').lower()  # Default to empty string if q is missing

    results = []

    if search_term:
        artist_accounts = ArtistAccount.objects.filter(user__username__icontains=search_term)
        results.extend([{'obj': obj, 'type': 'artist'} for obj in artist_accounts])

        albums = Album.objects.filter(
            Q(name__icontains=search_term) | Q(artists__user__username__icontains=search_term))
        results.extend([{'obj': obj, 'type': 'album'} for obj in albums])

        musics = Music.objects.filter(
            Q(music_name__icontains=search_term) | Q(artist__user__username__icontains=search_term))
        results.extend([{'obj': obj, 'type': 'music'} for obj in musics])

    context = {
        'search_term': search_term,
        'search_results': results,
    }

    return render(request, 'search.html', context)


@login_required(login_url='login')
def index(request):
    if is_admin(request.user):
        return redirect('/admin/')  # Redirect admins to Django admin panel
    elif is_artist(request.user):
        return redirect('artist_home')  # Redirect artists to artist home
    else:
        # Fetch Artists Data
        artists = ArtistAccount.objects.all()  # Get all artists

        # Fetch Albums Data (You might want to limit this)
        albums = Album.objects.all()  # Get all albums for now.  Consider using a slice or filtering.

        context = {
            'artists': artists,  # Pass this to the context
            'albums': albums,  # Pass this to the context
            'user': request.user,  # Useful to pass username to the view
        }

        # Path to your static image
        liked_songs_cover_image = 'banners/liked-songs-banner.webp'  # Replace with your actual path

        # Create the "Liked Songs" playlist if it doesn't exist
        liked_songs_playlist, created = Playlist.objects.get_or_create(
            name="Liked Songs",
            user=request.user.useraccount,
            defaults={'cover_image': liked_songs_cover_image}
        )

        # If the playlist was just created, set the cover image
        if created:
            liked_songs_playlist.cover_image = liked_songs_cover_image
            liked_songs_playlist.save()

        # Update the "Liked Songs" playlist based on current likes
        liked_songs = Music.objects.filter(like__user=request.user)
        liked_songs_playlist.music_set.set(liked_songs)
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials!')
            return render(request, 'login.html', context={'request': request})
    else:
        return render(request, 'login.html', context={'request': request})


def signup_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists!')
                return redirect('signup_user')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!')
                return redirect('signup_user')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, is_staff=False)
                user.save()
                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, 'Password does not match!')
            return render(request, 'signup_user.html', context={'request': request})
    else:
        return render(request, 'signup_user.html', context={'request': request})


def signup_artist(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists!')
                return redirect('signup_artist')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!')
                return redirect('signup_artist')
            else:
                # Create the User
                user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)
                user.save()  # Save the User object. The signal will handle ArtistAccount creation.

                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, 'Password does not match!')
            return render(request, 'signup_artist.html', context={'request': request})
    else:
        return render(request, 'signup_artist.html', context={'request': request})


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    response = redirect('login')  # Or wherever you redirect after logout
    response.delete_cookie('likedTracks')  # Delete the client-side cookie
    return response


# Admin home redirection
@login_required
@user_passes_test(is_admin)
def admin_home(request):
    return redirect('/admin/')  # Redirects admin users to the Django admin panel.


# Artist home: Handles both album creation and song uploads
@login_required
@user_passes_test(is_artist)
def artist_home(request):
    upload_song_form = UploadSongForm()  # instantiating UploadSongForm
    album_form = AlbumForm()
    albums = Album.objects.all()  # added this in as it's used for both uploads

    # **Fetch Tracks for Display:**
    try:
        artist_account = ArtistAccount.objects.get(user=request.user)
        tracks = Music.objects.filter(artist=artist_account)  # Use your Music model here
    except ArtistAccount.DoesNotExist:
        tracks = []  # Handle the case where the artist account doesn't exist.
        messages.error(request, "Artist account not found.")  # Inform Artist to recreate account

    albums = Album.objects.filter(artists=artist_account)

    if request.method == 'POST' and request.FILES.get('banner_image'):
        banner_form = BannerUploadForm(request.POST, request.FILES, instance=request.user.artistaccount)
        if banner_form.is_valid():
            banner_image = request.FILES['banner_image']
            fs = FileSystemStorage(location='media/')  # Configure MEDIA_ROOT and MEDIA_URL in settings.py
            filename = fs.save("banners/" + banner_image.name, banner_image)  # **ADD 'banners/' HERE**
            artist_account = ArtistAccount.objects.get(user=request.user)  # Get the user, not username
            artist_account.banner_image = filename  # Access ArtistAccount through user
            artist_account.save()
            return redirect('artist_home')  # Redirect back to the profile page
        else:  # added validation error rendering
            messages.error(request, "There are problems with your submission")
            return redirect('artist_home')

    else:
        banner_form = BannerUploadForm()  # Instantiating BannerUploadForm

    if request.method == 'POST':
        if request.FILES.get('audio_file'):  # check if the request is an audio file
            upload_song_form = UploadSongForm(request.POST, request.FILES)
            if upload_song_form.is_valid():
                try:
                    # Validate the file using your custom validator
                    validate_audio_file(request.FILES['audio_file'])

                    # If validation passes, save the form
                    new_song = upload_song_form.save(commit=False)  # Don't save to the database yet

                    # Getting the ArtistAccount associated with the logged in user:
                    artist_account = ArtistAccount.objects.get(user=request.user)  # Get the user, not username
                    new_song.artist = artist_account  # Access ArtistAccount through user

                    # **Here's the corrected album assignment:**
                    new_song.album = upload_song_form.cleaned_data['album']

                    new_song.save()  # Save the song to the database
                    messages.success(request, 'Song uploaded successfully!')
                    return redirect('artist_home')  # Redirect to a success page

                except ValidationError as e:
                    # If validation fails, add an error to the form
                    upload_song_form.add_error('audio_file', e)
                    messages.error(request, e)  # Display validator error message.
                except Exception as e:  # Catch other potential exceptions
                    messages.error(request, f"An unexpected error occurred: {e}")
            else:
                messages.error(request, upload_song_form.errors)
                return redirect('artist_home')  # Redirect to a success page


        else:  # Album form handling
            album_form = AlbumForm(request.POST, request.FILES)
            if album_form.is_valid():
                album = album_form.save(commit=False)  # Don't save yet

                # Associate the album with the current artist
                try:
                    artist_account = ArtistAccount.objects.get(user=request.user)
                    album.artists = artist_account  # Set the foreign key
                except ArtistAccount.DoesNotExist:
                    messages.error(request, "Artist account not found. Please create one.")
                    return render(request, 'profile.html',
                                  context)  # Render current html, but inform them of error
                    # Or redirect to a page to create an ArtistAccount
                    # return redirect('create_artist_account') # Replace with your URL

                album.save()  # Now save the album
                messages.success(request, "Album created successfully!")
                return redirect('artist_home')
            else:
                messages.error(request, "Album submission error")
                return redirect('artist_home')

    # Get all albums and genres for dropdowns


    context = {
        'form': upload_song_form,
        'banner_form': banner_form,
        'albums': albums,
        'album_form': album_form,  # Pass album form to the context
        'tracks': tracks,  # Pass the tracks to the template
        'user': request.user,
    }

    return render(request, 'profile.html', context)


@login_required
def artist_detail(request, pk):
    artist = get_object_or_404(ArtistAccount, pk=pk)

    # Order by like_count descending (most likes first), then by music_name
    tracks = artist.music_set.all().order_by('-like_count', 'music_name')

    if request.user.is_authenticated:
        liked_track_ids = Like.objects.filter(user=request.user, music__in=tracks).values_list('music_id',
                                                                                               flat=True)
    else:
        liked_track_ids = []

    # Update is_liked status more efficiently
    for track in tracks:
        track.is_liked = track.id in liked_track_ids

    context = {'artist': artist, 'tracks': tracks}
    return render(request, 'artist_detail.html', context)


@login_required  # Ensure only logged-in users can view
def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    tracks = album.music_set.all().order_by('-like_count', 'music_name')

    if request.user.is_authenticated:
        liked_track_ids = Like.objects.filter(user=request.user, music__in=tracks).values_list('music_id',
                                                                                               flat=True)
    else:
        liked_track_ids = []

    for track in tracks:
        track.is_liked = track.id in liked_track_ids

    context = {'album': album, 'tracks': tracks}  # Pass tracks to template
    return render(request, 'album_detail.html', context)


@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user.useraccount)
    tracks = playlist.music_set.all()

    if request.user.is_authenticated:
        liked_track_ids = Like.objects.filter(user=request.user, music__in=tracks).values_list('music_id', flat=True)
    else:
        liked_track_ids = []

    for track in tracks:
        # Check if the current track is liked by the user
        track.is_liked = track.id in liked_track_ids

    available_music = Music.objects.all()

    context = {
        'playlist': playlist,
        'available_music': available_music,
        'tracks': tracks,
    }

    return render(request, 'playlist_detail.html', context)


@login_required
def search_music_for_playlist(request):
    if request.method == 'GET':
        term = request.GET.get('term')  # Get the search term from the request
        if term:
            results = Music.objects.filter(music_name__icontains=term)[:10]  # Limit to 10 results
            data = [{'id': m.id, 'name': m.music_name, 'artist': m.artist.user.username} for m in results]
        else:
            data = []
        return JsonResponse(data, safe=False)


@login_required
def add_music_to_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)

    if request.method == 'POST':
        music_id = request.POST.get('music_id')
        try:
            music = Music.objects.get(pk=music_id)
            playlist.music_set.add(music)
            messages.success(request, f"Added '{music.music_name}' to '{playlist.name}'")
        except Music.DoesNotExist:
            messages.error(request, "Invalid music selection.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('playlist_detail', pk=pk)  # Redirect back to the playlist detail page


@login_required
@user_passes_test(is_artist)
def edit_song(request, track_id):
    track = get_object_or_404(Music, pk=track_id)
    form = EditSongForm(instance=track)

    if request.method == 'POST':
        form = EditSongForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, 'Song updated successfully!')
            return redirect('artist_home')  # Or wherever you want to redirect after editing
        else:
            messages.error(request, 'There was an error updating the song.')

    return render(request, 'edit_song.html', {'form': form, 'track': track})


def toggle_like(request):
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        try:
            track = get_object_or_404(Music, pk=track_id)
            user = request.user

            like, created = Like.objects.get_or_create(user=user, music=track)

            if not created:
                # Like already exists, so unlike it (delete the like)
                like.delete()
                track.like_count = max(0, track.like_count - 1)
                is_liked = False  # Correct is_liked value!

            else:
                # Like was created, so increment like count
                track.like_count += 1
                is_liked = True  # Correct is_liked value!

            track.save()  # SAVE THE TRACK AFTER MODIFYING like_count

            # Update the "Liked Songs" playlist here
            liked_songs_playlist = Playlist.objects.get(name="Liked Songs", user=user.useraccount)
            liked_songs = Music.objects.filter(like__user=user)
            liked_songs_playlist.music_set.set(liked_songs)  # Update the playlist

            # We need to load this information
            track_info = {
                'status': 'success',
                'like_count': track.like_count,
                'is_liked': is_liked,
            }
            # Return success
            return JsonResponse(track_info)

        except Music.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Track not found'})
        except Exception as e:
            traceback.print_exc()  # Print the full traceback to the console
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user.useraccount) #corrected this

    if request.method == 'POST':
        playlist.delete()
        return redirect('user_home')  # Or redirect to a different page
    else:
        return HttpResponseForbidden("Method not allowed")

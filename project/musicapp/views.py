from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UploadSongForm, AlbumForm, BannerUploadForm  # Import AlbumForm
from .models import Music, Album, ArtistAccount
from .validators import validate_audio_file
from django.core.exceptions import ValidationError
from django.db.models import Max, Min

# Helper functions for user type checks
def is_artist(user):
    return user.is_staff and not user.is_superuser  # Artists are is_staff but not is_superuser

def is_admin(user):
    return user.is_staff and user.is_superuser  # Admins are is_staff and is_superuser

@login_required
def music_tracks(request):
    track_id = request.GET.get('track_id')
    album_id = request.GET.get('album_id')
    selected_track = None
    tracks = []
    album = None

    try:
        # Get the ArtistAccount for the logged-in user
        artist_account = ArtistAccount.objects.get(user=request.user)

        # Filter Music objects by the artist
        all_tracks_for_artist = Music.objects.filter(artist=artist_account)

        if track_id:
            selected_track = get_object_or_404(Music, pk=track_id, artist=artist_account) # ensure only artist's tracks are selected
            album = selected_track.album
        elif album_id:
            album = get_object_or_404(Album, pk=album_id)
            tracks = all_tracks_for_artist.filter(album=album)
            selected_track = tracks.first() if tracks else None
        else:
            tracks = all_tracks_for_artist  # Only get tracks for this artist

        # Get the maximum track ID for the artist's music
        max_track_id = all_tracks_for_artist.aggregate(Max('id'))['id__max'] or 1

        # Get the *minimum* track ID (ID of the first track)
        first_track_id = all_tracks_for_artist.aggregate(Min('id'))['id__min'] or 1

        if max_track_id is None:
            max_track_id = 1
        if first_track_id is None:
            first_track_id = 1

    except ArtistAccount.DoesNotExist:
        messages.error(request, "Artist account not found.  Please create one.")
        max_track_id = 1
        first_track_id = 1
    except Music.DoesNotExist:
         messages.error(request, "Music does not exist. Please upload one.")
         max_track_id = 1
         first_track_id = 1

    except Exception as e:
        messages.error(request, f"Error retrieving music: {e}")
        max_track_id = 1
        first_track_id = 1

    context = {'selected_track': selected_track, 'album': album, 'tracks': tracks, 'max_track_id': max_track_id, 'first_track_id': first_track_id}
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

@login_required(login_url='login')
def index(request):
    if is_admin(request.user):
        return redirect('/admin/')  # Redirect admins to Django admin panel
    elif is_artist(request.user):
        return redirect('artist_home')  # Redirect artists to artist home
    else:
        # Fetch Artists Data
        artists = ArtistAccount.objects.all() # Get all artists

    # Fetch Albums Data (You might want to limit this)
        albums = Album.objects.all()  # Get all albums for now.  Consider using a slice or filtering.

        context = {
            'artists': artists, # Pass this to the context
            'albums': albums,  # Pass this to the context
            'user': request.user, #Useful to pass username to the view
        }

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
    return redirect('login')

# Admin home redirection
@login_required
@user_passes_test(is_admin)
def admin_home(request):
    return redirect('/admin/')  # Redirects admin users to the Django admin panel.

# Artist home: Handles both album creation and song uploads
@login_required
@user_passes_test(is_artist)
def artist_home(request):
    upload_song_form = UploadSongForm() #instantiating UploadSongForm
    album_form = AlbumForm()
    albums = Album.objects.all() # added this in as it's used for both uploads

    # **Fetch Tracks for Display:**
    try:
        artist_account = ArtistAccount.objects.get(user=request.user)
        tracks = Music.objects.filter(artist=artist_account)  # Use your Music model here
    except ArtistAccount.DoesNotExist:
        tracks = []  # Handle the case where the artist account doesn't exist.
        messages.error(request, "Artist account not found.") #Inform Artist to recreate account

    albums = Album.objects.filter(artists=artist_account)

    if request.method == 'POST' and request.FILES.get('banner_image'):
        banner_form = BannerUploadForm(request.POST, request.FILES, instance=request.user.artistaccount)
        if banner_form.is_valid():
            banner_image = request.FILES['banner_image']
            # Save the image to a storage location (e.g., using Django's FileSystemStorage or a cloud storage service like AWS S3).
            # Update the user's profile with the URL of the new banner image.

            # Example (using FileSystemStorage - adapt this to your storage setup!):
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage(location='media/')  # Configure MEDIA_ROOT and MEDIA_URL in settings.py
            filename = fs.save(banner_image.name, banner_image)

            # Assuming you have a UserProfile model or a way to associate the banner with the user:
            artist_account = ArtistAccount.objects.get(user=request.user) #Get the user, not username
            artist_account.banner_image = filename  # Access ArtistAccount through user
            artist_account.save()

            return redirect('artist_home')  # Redirect back to the profile page
        else: #added validation error rendering
            messages.error(request, "There are problems with your submission")
            return redirect('artist_home')

    else:
        banner_form = BannerUploadForm()  # Instantiating BannerUploadForm

    if request.method == 'POST':
        if request.FILES.get('audio_file'): #check if the request is an audio file
            upload_song_form = UploadSongForm(request.POST, request.FILES)
            if upload_song_form.is_valid():
                try:
                    # Validate the file using your custom validator
                    validate_audio_file(request.FILES['audio_file'])

                    # If validation passes, save the form
                    new_song = upload_song_form.save(commit=False)  # Don't save to the database yet

                    #Getting the ArtistAccount associated with the logged in user:
                    artist_account = ArtistAccount.objects.get(user=request.user) #Get the user, not username
                    new_song.artist = artist_account   # Access ArtistAccount through user

                    # **Here's the corrected album assignment:**
                    new_song.album = upload_song_form.cleaned_data['album']

                    new_song.save()  # Save the song to the database
                    messages.success(request, 'Song uploaded successfully!')
                    return redirect('artist_home')  # Redirect to a success page

                except ValidationError as e:
                    # If validation fails, add an error to the form
                    upload_song_form.add_error('audio_file', e)
                    messages.error(request, e)  # Display validator error message.
                except Exception as e: # Catch other potential exceptions
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
                    return render(request, 'profile.html', context) #Render current html, but inform them of error
                    # Or redirect to a page to create an ArtistAccount
                    #return redirect('create_artist_account') # Replace with your URL

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
        'album_form': album_form, #Pass album form to the context
        'tracks': tracks,  # Pass the tracks to the template
        'user': request.user,
    }

    return render(request, 'profile.html', context)
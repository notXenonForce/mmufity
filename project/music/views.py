from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test


# Helper functions for user type checks
def is_artist(user):
    return user.is_staff and not user.is_superuser  # Artists are is_staff but not is_superuser

def is_admin(user):
  return user.is_staff and user.is_superuser # Admins are is_staff and is_superuser


@login_required(login_url='login')
def index(request):
  if is_admin(request.user):
    return redirect('/admin/')  # Redirect admins to Django admin panel
  elif is_artist(request.user):
    return redirect('artist_home') # Redirect artists to artist home
  else:
    return render(request, 'index.html')  # Regular users go to a generic home page

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
            return render(request, 'login.html', context={'request': request}) #Correct code.
    else:
        return render(request, 'login.html', context={'request': request}) #Correct code.



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
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_staff = False; #regular users must not have staff flag enabled
                user.save()
                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, 'Password does not match!')
            return render(request, 'signup_user.html', context={'request': request}) #Correct code.
    else:
        return render(request, 'signup_user.html', context={'request': request}) #Correct code.


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
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_staff = True; # artists must have staff flag enabled.
                user.save()
                auth.login(request, user)
                return redirect('/')
        else:
            messages.info(request, 'Password does not match!')
            return render(request, 'signup_artist.html', context={'request': request}) #Correct code.
    else:
        return render(request, 'signup_artist.html', context={'request': request}) #Correct code.

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

# Sample View for admin home (replace with your actual admin home view)
@login_required
@user_passes_test(is_admin)
def admin_home(request):
    return redirect('/admin/') # Redirects admin users to the django admin panel.

# Sample View for artist home (replace with your actual artist home view)
@login_required
@user_passes_test(is_artist)
def artist_home(request):
    return render(request, 'profile.html')
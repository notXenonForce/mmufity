import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicproject.settings')
django.setup()

from django.contrib.auth.models import User
from musicapp.models import ArtistAccount

def transfer_staff_accounts():
    staff_users = User.objects.filter(is_staff=True) #Filter the user model
    for user in staff_users:
        # Check if an ArtistAccount already exists for this user
        if not ArtistAccount.objects.filter(username=user.username).exists():
            # Create a new ArtistAccount
            artist_account = ArtistAccount.objects.create(
                username=user.username,
                email=user.email,
                password=user.password  # Consider hashing if not already
            )
            print(f"Transferred User '{user.username}' to ArtistAccount")
        else:
            print(f"ArtistAccount already exists for User '{user.username}'")

if __name__ == "__main__":
    transfer_staff_accounts()
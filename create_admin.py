import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Define superuser credentials
# YOU CAN CHANGE THESE VALUES
USERNAME = 'admin'
EMAIL = 'admin@example.com'
PASSWORD = 'adminpassword'

def create_superuser():
    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"\n[SUCCESS] Superuser created!")
        print(f"Username: {USERNAME}")
        print(f"Password: {PASSWORD}")
        print(f"Email:    {EMAIL}")
        print("\nNow run your 'push_repo.bat' to upload the updated database to Vercel.")
    else:
        print(f"\n[INFO] Superuser '{USERNAME}' already exists.")

if __name__ == "__main__":
    create_superuser()

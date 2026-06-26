import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rbdu_base_readers.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

u = os.environ.get("DJANGO_SUPERUSER_USERNAME")
p = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
e = os.environ.get("DJANGO_SUPERUSER_EMAIL")

if u and p:
    if not User.objects.filter(username=u).exists():
        User.objects.create_superuser(u, e, p)
        print("superuser created")
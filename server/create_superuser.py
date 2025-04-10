#!/usr/bin/env python
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# Imposta la configurazione di Django
django.setup()

User = get_user_model()

# Leggi le variabili d'ambiente (con valori di default)
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser creato")
else:
    print("Superuser già esistente")

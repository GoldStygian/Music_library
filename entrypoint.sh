#!/bin/sh
set -e

# Esegue le migrazioni
# echo "Eseguo le migrazioni"
# python manage.py migrate

# Crea il superuser se non esiste
echo "Verifica e creazione del superuser"
python /app/server/create_superuser.py

# Avvia il server
echo "Avvio il server"
python manage.py runserver 0.0.0.0:8000

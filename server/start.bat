@echo off
echo [+] attivo l'ambiente virtuale
cd ..\venv\Scripts
call activate
cd ..\..\server
echo [+] avvio il server
call python manage.py runserver 127.0.0.1:8000
pause
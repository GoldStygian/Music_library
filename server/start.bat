@echo off
echo [+] attivo l'ambiente virtuale
cd ..\venv\Scripts
call activate
cd ..\..\server
echo [+] avvio il server
call python manage.py runserver 192.168.1.2:8000
pause
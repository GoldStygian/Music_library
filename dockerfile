# Usa un'immagine base Python
FROM python:3.11-slim 
#-slim server per scaricare una versione più leggera

# Copia i file requirements
COPY server/requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt
#--no-cache-dir viene usato per non salvare nella cache i pacchetti scaricati durante l'installazione.

# Copia il codice sorgente
COPY . ./app

RUN chmod +x /app/entrypoint.sh

# Espone la porta (8000 è quella usata dal server dev di Django)
EXPOSE 8000

# Comando di default da eseguire quando il container si avvia
# CMD ["sh", "-c", "cd /app/server && python manage.py runserver 0.0.0.0:8000"] 
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["/app/entrypoint.sh"]

# Imposta la directory di lavoro
WORKDIR /app/server

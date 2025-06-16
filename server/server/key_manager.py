import json

class keyManager:

    SECRET_KEY = 'SECRET_KEY'
    LAST_FM_API_KEY = 'LAST_FM_API_KEY'
    MUSIC_BRAINZ_API_EMAIL = 'MUSIC_BRAINZ_API_EMAIL'
    ACOUSTID_API_KEY = 'ACOUSTID_API_KEY'

    def __init__(self, json_file_path):
        self.data = {} # struttura che contiene i dati letti da file

        self.json_file_path = json_file_path
        self.load_data()

    def load_data(self):

        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("File non trovato!")
        except json.JSONDecodeError:
            print("Errore nel parsing del JSON!")

    def get(self, key, default=None):
        """Restituisce il valore associato alla chiave, se esiste."""
        return self.data.get(key, default)

    def all_keys(self):
        """Restituisce tutte le chiavi disponibili nel file JSON caricato."""
        return list(self.data.keys())

    def has_key(self, key):
        """Controlla se una chiave è presente nei dati."""
        return key in self.data
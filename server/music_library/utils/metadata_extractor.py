import os
import json
import subprocess
from typing import Dict, List, Optional
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
import logging

logger = logging.getLogger(__name__)

class MutagenExtractor:
    """Estrae metadati da file audio usando Mutagen"""
    
    def extract(self, file_path: str) -> Dict:
        """
        Estrae metadati da un file audio
        
        Returns:
            Dict con metadati estratti
        """
        try:
            # Determina il tipo di file e carica con Mutagen
            audio = self._load_audio_file(file_path)
            
            if not audio:
                raise ValueError("Impossibile caricare il file audio")
            
            # Estrai metadati base
            metadata = {
                'track_id': self._get_musicbrainz_track_id(audio),
                'album_id': self._get_musicbrainz_album_id(audio),
                'title': self._get_title(audio),
                'artist': self._get_artist(audio),
                'duration': self._get_duration(audio),
                'artists': self._parse_artists(self._get_artist(audio)),
                'raw_metadata': self._get_all_metadata(audio)
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Errore nell'estrazione metadati: {str(e)}")
            raise

    def _load_audio_file(self, file_path: str):
        """Carica il file audio con Mutagen"""
        try:
            if file_path.lower().endswith('.mp3'):
                return MP3(file_path, ID3=EasyID3)
            elif file_path.lower().endswith('.flac'):
                return FLAC(file_path)
            elif file_path.lower().endswith(('.m4a', '.mp4')):
                return MP4(file_path)
            else:
                # Prova il riconoscimento automatico
                return File(file_path)
        except Exception as e:
            logger.error(f"Errore nel caricamento file {file_path}: {str(e)}")
            return None

    def _get_musicbrainz_track_id(self, audio) -> Optional[str]:
        """Estrae MusicBrainz Track ID"""
        try:
            if hasattr(audio, 'get'):
                return audio.get('musicbrainz_trackid', [None])[0]
            return audio.get('musicbrainz_trackid', [None])[0] if 'musicbrainz_trackid' in audio else None
        except (IndexError, KeyError, AttributeError):
            return None

    def _get_musicbrainz_album_id(self, audio) -> Optional[str]:
        """Estrae MusicBrainz Album ID"""
        try:
            if hasattr(audio, 'get'):
                return audio.get('musicbrainz_albumid', [None])[0]
            return audio.get('musicbrainz_albumid', [None])[0] if 'musicbrainz_albumid' in audio else None
        except (IndexError, KeyError, AttributeError):
            return None

    def _get_title(self, audio) -> Optional[str]:
        """Estrae il titolo della traccia"""
        try:
            if hasattr(audio, 'get'):
                return audio.get('title', [None])[0]
            return audio.get('title', [None])[0] if 'title' in audio else None
        except (IndexError, KeyError, AttributeError):
            return None

    def _get_artist(self, audio) -> Optional[str]:
        """Estrae l'artista della traccia"""
        try:
            if hasattr(audio, 'get'):
                return audio.get('artist', [None])[0]
            return audio.get('artist', [None])[0] if 'artist' in audio else None
        except (IndexError, KeyError, AttributeError):
            return None

    def _get_duration(self, audio) -> Optional[str]:
        """Estrae e formatta la durata della traccia"""
        try:
            if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                length_seconds = int(audio.info.length)
                minutes = length_seconds // 60
                seconds = length_seconds % 60
                return f"{minutes}:{seconds:02d}"
            return None
        except (AttributeError, ValueError):
            return None

    def _get_all_metadata(self, audio) -> Dict:
        """Estrae tutti i metadati disponibili"""
        try:
            metadata = {}
            for key, value in audio.items():
                metadata[key] = value
            return metadata
        except Exception:
            return {}

    def _parse_artists(self, artists_string: str) -> List[Dict]:
        """
        Parsifica la stringa degli artisti
        
        Args:
            artists_string: Stringa con artisti separati da delimitatori
            
        Returns:
            Lista di dizionari con informazioni artisti
        """
        if not artists_string:
            return []
        
        # Parole da ignorare nella separazione
        ignore_words = {"feat.", "feat", "featuring", "&", "and"}
        
        # Sostituisci le parole ignorate con virgole
        processed_string = artists_string
        for word in ignore_words:
            processed_string = processed_string.replace(word, ",")
        
        # Dividi per virgola e pulisci
        artists = [artist.strip() for artist in processed_string.split(',') if artist.strip()]
        
        # Converti in formato dict (assumendo che non abbiamo ID MusicBrainz qui)
        return [{'name': artist, 'id': None} for artist in artists]


# utils/ffmpeg_extractor.py
class FFmpegExtractor:
    """Estrae metadati usando FFmpeg/FFprobe"""
    
    def extract(self, file_path: str) -> Dict:
        """
        Estrae metadati usando FFprobe
        
        Returns:
            Dict con metadati estratti da FFmpeg
        """
        try:
            result = subprocess.run(
                [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json',
                    '-show_format', '-show_streams', file_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, 'ffprobe')
            
            metadata = json.loads(result.stdout)
            return self._parse_ffmpeg_metadata(metadata)
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout nell'estrazione metadati con FFmpeg")
            raise
        except json.JSONDecodeError:
            logger.error("Errore nel parsing JSON da FFmpeg")
            raise
        except Exception as e:
            logger.error(f"Errore nell'estrazione metadati FFmpeg: {str(e)}")
            raise

    def _parse_ffmpeg_metadata(self, metadata: Dict) -> Dict:
        """Parsifica i metadati estratti da FFmpeg"""
        format_info = metadata.get('format', {})
        tags = format_info.get('tags', {})
        
        # Normalizza i nomi dei tag (FFmpeg può usare maiuscole/minuscole diverse)
        normalized_tags = {}
        for key, value in tags.items():
            normalized_tags[key.lower()] = value
        
        return {
            'title': normalized_tags.get('title'),
            'artist': normalized_tags.get('artist'),
            'album': normalized_tags.get('album'),
            'duration': format_info.get('duration'),
            'track_id': normalized_tags.get('musicbrainz_trackid'),
            'album_id': normalized_tags.get('musicbrainz_albumid'),
        }
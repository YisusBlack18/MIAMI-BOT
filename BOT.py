import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import requests
import pywhatkit
import os
import sys
import urllib.parse

# Configurar codificación UTF-8 para la salida
if sys.platform == "win32":
    os.system("chcp 65001")  # Configura la consola de Windows a UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Configuración de la API de Spotify
SPOTIFY_CLIENT_ID = "794271bee563455eb34b98468cf46e59"
SPOTIFY_CLIENT_SECRET = "17156d4003fd488aba76cc48b4261874"

# Autenticación con Spotify
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))
except Exception as e:
    print(f"Error en la autenticación con Spotify: {e}")
    sys.exit(1)

# ID de la playlist
PLAYLIST_ID = "20piU9DqsVyW1vE8N2Y1qQ"

# ID del grupo de WhatsApp
GROUP_ID = "GGYqR6FUcYaBnkO6NuEgV3"

def get_random_song_from_playlist(playlist_id, market="MX"):
    try:
        playlist = sp.playlist(playlist_id)
        print(f"Playlist encontrada: {playlist['name']}, Canciones totales: {playlist['tracks']['total']}")
        
        results = sp.playlist_tracks(playlist_id, market=market)
        tracks = results["items"]
        
        if not tracks:
            print(f"No se encontraron canciones en la playlist {playlist_id}")
            return None, None, None, None
        
        random_track = random.choice(tracks)
        track = random_track["track"]
        
        if not track or "name" not in track or "artists" not in track or not track["artists"]:
            print("Error: Datos de la canción incompletos")
            print(f"Track: {track}")
            return None, None, None, None
        
        song_name = track["name"]
        artist_name = track["artists"][0]["name"]
        album_cover_url = track["album"]["images"][0]["url"] if track["album"]["images"] else None
        
        added_by = random_track.get("added_by", {})
        user_id = added_by.get("id", "Desconocido") if added_by else "Desconocido"
        
        user_name = user_id
        try:
            if user_id != "Desconocido":
                user_info = sp.user(user_id)
                user_name = user_info.get("display_name", user_id) or user_id
        except Exception as e:
            print(f"Error al obtener información del usuario {user_id}: {e}")
        
        print(f"Canción seleccionada: {song_name} - {artist_name}, Cortesía de: {user_name}")
        return song_name, artist_name, album_cover_url, user_name
    except Exception as e:
        print(f"Error al obtener la canción de la playlist {playlist_id}: {e}")
        return None, None, None, None

def download_image(url, filename):
    if not url:
        print("No se proporcionó una URL de imagen")
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            print(f"Error al descargar la imagen: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

def main():
    song_name, artist_name, album_cover_url, user_name = get_random_song_from_playlist(PLAYLIST_ID)
    
    if not song_name or not artist_name:
        print("No se pudo obtener la canción o el artista. Terminando.")
        return
    
    message = f" *Cancion del dia* \n{song_name} - {artist_name}\nCortesía de: {user_name}"
    encoded_message = urllib.parse.quote(message)
    print(f"Mensaje preparado: {message}")
    print(f"Mensaje codificado: {encoded_message}")
    
    cover_filename = "album_cover.jpg"
    downloaded_image = download_image(album_cover_url, cover_filename)
    
    if not downloaded_image:
        print("No se pudo descargar la portada. Enviando solo el mensaje.")
        try:
            pywhatkit.sendwhatmsg_to_group_instantly(
                GROUP_ID, 
                message, 
                wait_time=20, 
                tab_close=True
            )
            print("Mensaje enviado exitosamente.")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")
        return
    
    try:
        pywhatkit.sendwhats_image(
            GROUP_ID, 
            downloaded_image, 
            caption=message, 
            wait_time=20, 
            tab_close=True
        )
        print("Imagen y mensaje enviados exitosamente.")
    except Exception as e:
        print(f"Error al enviar la imagen: {e}")
    finally:
        if os.path.exists(cover_filename):
            os.remove(cover_filename)
            print("Imagen temporal eliminada.")

if __name__ == "__main__":
    main()

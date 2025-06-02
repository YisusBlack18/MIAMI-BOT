import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from datetime import datetime
import requests
import json
import os
import sys
import urllib.parse
import pywhatkit
import pyperclip
import pyautogui
import time
from dotenv import load_dotenv
import atexit
import webbrowser
from urllib.parse import quote
from PIL import Image
import io
import win32clipboard
from io import BytesIO
import logging

# Configurar logging
log_filename = "daily_song.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configurar codificación UTF-8 para la salida
if sys.platform == "win32":
    os.system("chcp 65001")  # Configura la consola de Windows a UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Spotify credentials
SPOTIFY_CLIENT_ID = "794271bee563455eb34b98468cf46e59"
SPOTIFY_CLIENT_SECRET = "17156d4003fd488aba76cc48b4261874"
PLAYLIST_ID = "20piU9DqsVyW1vE8N2Y1qQ"

# WhatsApp group ID
GROUP_ID = "GGYqR6FUcYaBnkO6NuEgV3"

# Global Spotify client
sp = None

def init_spotify():
    """Initialize Spotify client with proper cleanup"""
    global sp
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        logging.info("Spotify client initialized successfully")
        return True
    except Exception as e:
        logging.error(f"Error en la autenticación con Spotify: {e}")
        print(f"Error en la autenticación con Spotify: {e}")
        return False

def cleanup_spotify():
    """Cleanup function for Spotify client"""
    global sp
    if sp is not None:
        try:
            sp = None
        except:
            pass

# Register cleanup function
atexit.register(cleanup_spotify)

def get_random_song():
    """Get a random song from the specified playlist"""
    try:
        # Get playlist info first
        playlist = sp.playlist(PLAYLIST_ID)
        print(f"Playlist encontrada: {playlist['name']}, Canciones totales: {playlist['tracks']['total']}")
        
        # Get playlist tracks
        results = sp.playlist_tracks(PLAYLIST_ID, market="MX")
        tracks = results["items"]
        
        if not tracks:
            print(f"No se encontraron canciones en la playlist {PLAYLIST_ID}")
            return None
        
        # Select random track
        random_track_item = random.choice(tracks)
        track_data = random_track_item["track"]
        
        if not track_data or "name" not in track_data or "artists" not in track_data or not track_data["artists"]:
            print("Error: Datos de la canción incompletos")
            print(f"Track: {track_data}")
            return None
        
        # Get user information
        added_by = random_track_item.get("added_by", {})
        user_id = added_by.get("id", "Desconocido") if added_by else "Desconocido"
        
        user_name = user_id
        try:
            if user_id != "Desconocido":
                user_info = sp.user(user_id)
                user_name = user_info.get("display_name", user_id) or user_id
        except Exception as e:
            print(f"Error al obtener información del usuario {user_id}: {e}")
        
        # Get album image
        album_image = track_data["album"]["images"][0]["url"] if track_data["album"]["images"] else None
        
        # Extract song information
        song_info = {
            'name': track_data["name"],
            'artist': track_data["artists"][0]["name"],
            'album': track_data["album"]["name"],
            'url': track_data["external_urls"]["spotify"],
            'added_by': user_name,
            'album_image': album_image
        }
        
        print(f"Canción seleccionada: {song_info['name']} - {song_info['artist']}, Cortesía de: {song_info['added_by']}")
        return song_info
            
    except Exception as e:
        print(f"Error al obtener la canción de la playlist {PLAYLIST_ID}: {e}")
        print("\nFull error details:")
        import traceback
        traceback.print_exc()
        return None

def download_image(url, filename):
    """Download image from URL"""
    if not url:
        print("No image URL provided")
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            print(f"Error downloading image: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def is_whatsapp_web_open():
    """Check if WhatsApp Web is already open in the browser"""
    try:
        # Intentar activar la ventana de WhatsApp Web
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        
        # Verificar si estamos en WhatsApp Web por la URL
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        current_url = pyperclip.paste()
        
        # Si no estamos en WhatsApp Web, volver a la ventana anterior
        if 'web.whatsapp.com' not in current_url:
            pyautogui.hotkey('alt', 'tab')
            return False
            
        return True
    except:
        return False

def is_in_correct_group():
    """Check if we're already in the correct WhatsApp group"""
    try:
        # Verificar si estamos en WhatsApp Web
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        current_url = pyperclip.paste()
        
        if 'web.whatsapp.com' not in current_url:
            return False
            
        # Verificar si estamos en el grupo correcto
        return GROUP_ID in current_url
    except:
        return False

def copy_image_to_clipboard(image_path):
    """Copy image to clipboard using win32clipboard"""
    try:
        # Abrir la imagen
        image = Image.open(image_path)
        
        # Convertir a formato BMP
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # Remover el header BMP
        output.close()
        
        # Copiar al portapapeles usando win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        return True
    except Exception as e:
        print(f"Error al copiar la imagen al portapapeles: {e}")
        return False

def send_whatsapp_message(song_info):
    """Send the daily song message to WhatsApp group using pywhatkit with clipboard"""
    if not song_info:
        return False
    
    # Prepare the message
    message = (
        f"🎵 *Canción del Día* 🎵\n\n"
        f"*{song_info['name']}*\n"
        f"Artista: {song_info['artist']}\n"
        f"Álbum: {song_info['album']}\n"
        f"Agregada por: {song_info['added_by']}\n\n"
        f"Escucha aquí: {song_info['url']}"
    )
    
    print(f"Preparando mensaje: {message}")
    
    # Download album cover if available
    cover_filename = "album_cover.jpg"
    downloaded_image = None
    
    if song_info['album_image']:
        downloaded_image = download_image(song_info['album_image'], cover_filename)
    
    try:
        whatsapp_already_open = is_whatsapp_web_open()
        in_correct_group = is_in_correct_group() if whatsapp_already_open else False
        
        if not whatsapp_already_open:
            # Abrir WhatsApp Web usando pywhatkit si no está abierto
            # Siempre usamos sendwhatmsg_to_group_instantly para abrir el grupo
            pywhatkit.sendwhatmsg_to_group_instantly(
                GROUP_ID,
                "",  # Enviaremos el mensaje después
                wait_time=20,  # Aumentado el tiempo de espera inicial
                tab_close=False  # No cerrar la pestaña para poder enviar el mensaje
            )
            time.sleep(3)  # Aumentado el tiempo de espera después de abrir
        elif not in_correct_group:
            # Si WhatsApp está abierto pero no estamos en el grupo correcto
            group_url = f"https://web.whatsapp.com/accept?code={GROUP_ID}"
            pyautogui.hotkey('ctrl', 'l')  # Seleccionar la barra de direcciones
            pyperclip.copy(group_url)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(5)  # Aumentado el tiempo de espera para cargar el grupo
        
        # En este punto, ya estamos en el grupo correcto
        if downloaded_image:
            # Intentar copiar la imagen al portapapeles
            if copy_image_to_clipboard(cover_filename):
                # Pegar la imagen en el chat (esto abrirá el editor de imagen)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(4)  # Aumentado el tiempo de espera para que se procese la imagen
                
                # Copiar y pegar el mensaje como caption
                pyperclip.copy(message)
                time.sleep(2)  # Aumentado el tiempo de espera antes de pegar el mensaje
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(2)  # Aumentado el tiempo de espera después de pegar el mensaje
                
                # Enviar la imagen con el mensaje
                pyautogui.press('enter')
                time.sleep(3)  # Aumentado el tiempo de espera después de enviar
            else:
                print("No se pudo enviar la imagen, enviando solo el mensaje")
                # Enviar solo el mensaje si falló la imagen
                pyperclip.copy(message)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(2)  # Aumentado el tiempo de espera
                pyautogui.press('enter')
                time.sleep(2)  # Aumentado el tiempo de espera
        else:
            # Si no hay imagen, enviar solo el mensaje
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)  # Aumentado el tiempo de espera
            pyautogui.press('enter')
            time.sleep(2)  # Aumentado el tiempo de espera
        
        print("Mensaje enviado exitosamente")
        return True
    
    except Exception as e:
        print(f"Error al enviar el mensaje: {str(e)}")
        return False
    
    finally:
        # Clean up downloaded image
        if downloaded_image and os.path.exists(cover_filename):
            os.remove(cover_filename)
            print("Imagen temporal eliminada")
        
        # No cerramos la pestaña si WhatsApp ya estaba abierto
        if not whatsapp_already_open:
            time.sleep(3)  # Aumentado el tiempo de espera antes de cerrar
            pyautogui.hotkey('ctrl', 'w')  # Cerrar la pestaña solo si la abrimos nosotros

def main():
    """Main function to run the daily song selection and sending"""
    try:
        current_time = datetime.now()
        logging.info(f"Starting daily song selection at {current_time}")
        print(f"Starting daily song selection at {current_time}")
        
        # Initialize Spotify
        if not init_spotify():
            logging.error("Failed to initialize Spotify client")
            print("Failed to initialize Spotify client")
            return
        
        # Get random song
        song_info = get_random_song()
        if not song_info:
            logging.error("Failed to get song information")
            print("Failed to get song information")
            return
        
        # Send message to WhatsApp
        if send_whatsapp_message(song_info):
            logging.info("Daily song message sent successfully")
            print("Daily song message sent successfully")
        else:
            logging.error("Failed to send daily song message")
            print("Failed to send daily song message")
    
    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}", exc_info=True)
        print(f"Unexpected error: {str(e)}")
    
    finally:
        # Cleanup
        cleanup_spotify()
        logging.info("Script execution completed")

if __name__ == "__main__":
    main()

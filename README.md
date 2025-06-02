# Bot de Canción del Día para WhatsApp

Este bot selecciona aleatoriamente una canción de una playlist de Spotify y la envía diariamente a un grupo de WhatsApp, incluyendo la portada del álbum y detalles de la canción.

## Características

- Selección aleatoria de canciones desde una playlist de Spotify
- Envío automático diario a un grupo de WhatsApp
- Incluye:
  - Nombre de la canción
  - Artista
  - Álbum
  - Portada del álbum
  - Enlace a Spotify
  - Usuario que agregó la canción
- Ejecución programada diaria
- Sistema de logging para seguimiento de ejecuciones
- Manejo robusto de errores

## Requisitos

- Python 3.13 o superior
- Cuenta de Spotify Developer
- WhatsApp Web instalado y configurado
- Navegador Microsoft Edge
- Windows 10 o superior

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/TU_USUARIO/MIAMI-BOT.git
cd MIAMI-BOT
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las credenciales:
   - Obtén tus credenciales de Spotify Developer:
     1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
     2. Crea una nueva aplicación
     3. Obtén el Client ID y Client Secret
   - Actualiza las credenciales en `DailySong.py`:
     ```python
     SPOTIFY_CLIENT_ID = "tu_client_id"
     SPOTIFY_CLIENT_SECRET = "tu_client_secret"
     PLAYLIST_ID = "id_de_tu_playlist"
     GROUP_ID = "id_de_tu_grupo_whatsapp"
     ```

## Configuración de la Ejecución Diaria

1. Ejecuta `setup_scheduler.bat` como administrador:

   - Click derecho en `setup_scheduler.bat`
   - Selecciona "Ejecutar como administrador"
   - Esto configurará la tarea programada para ejecutarse diariamente a las 12:00 PM

2. Para modificar la hora de ejecución:

```batch
schtasks /change /tn "CancionDelDia" /st HH:MM
```

Por ejemplo, para ejecutar a las 3:00 PM:

```batch
schtasks /change /tn "CancionDelDia" /st 15:00
```

3. Para eliminar la tarea programada:

```batch
schtasks /delete /tn "CancionDelDia" /f
```

## Uso Manual

Si deseas ejecutar el bot manualmente:

1. Asegúrate de que WhatsApp Web esté instalado y configurado
2. Ejecuta el script:

```bash
python DailySong.py
```

## Estructura del Proyecto

- `DailySong.py`: Script principal
- `run_daily_song.bat`: Script batch para ejecución programada
- `setup_scheduler.bat`: Script para configurar la tarea programada
- `requirements.txt`: Dependencias del proyecto
- `daily_song.log`: Archivo de registro de ejecuciones

## Logs

El bot mantiene un registro detallado de todas las ejecuciones en `daily_song.log`, incluyendo:

- Fecha y hora de ejecución
- Estado de la selección de la canción
- Estado del envío del mensaje
- Errores y excepciones

## Solución de Problemas

1. Si el bot no envía mensajes:

   - Verifica que WhatsApp Web esté instalado y configurado
   - Asegúrate de que las credenciales de Spotify sean correctas
   - Revisa el archivo `daily_song.log` para ver errores específicos

2. Si la tarea programada no se ejecuta:

   - Verifica que el script batch tenga permisos de ejecución
   - Asegúrate de que la tarea esté configurada correctamente en el Programador de tareas
   - Revisa los logs del Programador de tareas de Windows

3. Si hay problemas con las imágenes:
   - Verifica que Microsoft Edge esté instalado
   - Asegúrate de que la imagen de la portada sea accesible
   - Revisa los permisos de escritura en el directorio temporal

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

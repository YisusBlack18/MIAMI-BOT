@echo off
echo Configurando tarea programada para la Canción del Día...

:: Crear la tarea programada
schtasks /create /tn "CancionDelDia" /tr "%~dp0run_daily_song.bat" /sc daily /st 12:00 /ru "%USERNAME%" /f

echo.
echo Tarea programada creada exitosamente!
echo La canción del día se enviará todos los días a las 12:00 PM
echo.
echo Para modificar la hora, ejecuta:
echo schtasks /change /tn "CancionDelDia" /st HH:MM
echo.
echo Para eliminar la tarea, ejecuta:
echo schtasks /delete /tn "CancionDelDia" /f
echo.
pause 
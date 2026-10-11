@echo off
rem ---------------------------------------------------------------
rem  Doppio clic: ti chiede video/audio, file dei tempi e dove salvare.
rem  Oppure trascina un video su questo file: cerca
rem  nomevideo.karaoke.json (o .lrc) accanto al video o in Download.
rem ---------------------------------------------------------------
setlocal
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if not defined PY goto nopython

%PY% "%~dp0render.py" %*
echo.
pause
exit /b

:nopython
echo Python non trovato.
echo Esegui prima "installa_requisiti.bat" in questa cartella.
echo.
pause

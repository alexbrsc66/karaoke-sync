@echo off
rem ---------------------------------------------------------------
rem  Controlla e, se mancano, installa Python e ffmpeg (via winget).
rem  Non servono diritti di amministratore.
rem ---------------------------------------------------------------
setlocal
echo.
echo === Controllo requisiti per il render karaoke ===
echo.

where winget >nul 2>&1
if errorlevel 1 goto nowinget

rem ---------- Python ----------
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if defined PY goto pyok

echo [..] Python non trovato: lo installo...
winget install -e --id Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements
if errorlevel 1 goto pyfail
set "NEEDRESTART=1"
goto ffcheck

:pyok
echo [OK] Python trovato:
%PY% --version
%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 (
  echo [!!] Manca tkinter, che serve per le finestre di scelta file.
  echo      Reinstalla Python da python.org spuntando "tcl/tk and IDLE".
) else (
  echo [OK] tkinter disponibile
)

rem ---------- ffmpeg ----------
:ffcheck
set "FF="
where ffmpeg >nul 2>&1 && set "FF=1"
if exist "%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe" set "FF=1"
if defined FF goto ffok

echo [..] ffmpeg non trovato: lo installo...
winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
if errorlevel 1 goto fffail
set "NEEDRESTART=1"
goto end

:ffok
echo [OK] ffmpeg trovato

:end
echo.
if defined NEEDRESTART (
  echo Installazione completata.
  echo IMPORTANTE: chiudi questa finestra e apri di nuovo render.bat
  echo per far riconoscere i programmi appena installati.
) else (
  echo Tutto a posto: puoi usare render.bat.
)
echo.
pause
exit /b 0

:nowinget
echo [!!] winget non e' disponibile su questo computer.
echo Installa a mano:
echo   Python: https://www.python.org/downloads/  spunta "Add python.exe to PATH"
echo   ffmpeg: https://www.gyan.dev/ffmpeg/builds/  scarica ffmpeg-release-essentials.zip,
echo           estrai e aggiungi la cartella bin al PATH di Windows.
echo.
pause
exit /b 1

:pyfail
echo [!!] Installazione di Python non riuscita. Scaricalo da https://www.python.org/downloads/
pause
exit /b 1

:fffail
echo [!!] Installazione di ffmpeg non riuscita. Vedi le istruzioni nel LEGGIMI.md
pause
exit /b 1

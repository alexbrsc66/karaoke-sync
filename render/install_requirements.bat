@echo off
rem ---------------------------------------------------------------
rem  Checks for Python and ffmpeg and installs them (via winget)
rem  if they are missing. No administrator rights needed.
rem ---------------------------------------------------------------
setlocal
echo.
echo === Checking requirements for the karaoke render ===
echo.

where winget >nul 2>&1
if errorlevel 1 goto nowinget

rem ---------- Python ----------
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if defined PY goto pyok

echo [..] Python not found: installing it...
winget install -e --id Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements
if errorlevel 1 goto pyfail
set "NEEDRESTART=1"
goto ffcheck

:pyok
echo [OK] Python found:
%PY% --version
%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 (
  echo [!!] tkinter is missing, it is needed for the file dialogs.
  echo      Reinstall Python from python.org keeping "tcl/tk and IDLE" ticked.
) else (
  echo [OK] tkinter available
)

rem ---------- ffmpeg ----------
:ffcheck
set "FF="
where ffmpeg >nul 2>&1 && set "FF=1"
if exist "%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe" set "FF=1"
if defined FF goto ffok

echo [..] ffmpeg not found: installing it...
winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
if errorlevel 1 goto fffail
set "NEEDRESTART=1"
goto end

:ffok
echo [OK] ffmpeg found

:end
echo.
if defined NEEDRESTART (
  echo Installation complete.
  echo IMPORTANT: close this window and open render.bat again
  echo so that the newly installed programs are recognised.
) else (
  echo All good: you can use render.bat.
)
echo.
echo Press any key to close...
pause >nul
exit /b 0

:nowinget
echo [!!] winget is not available on this computer.
echo Install by hand:
echo   Python: https://www.python.org/downloads/  tick "Add python.exe to PATH"
echo   ffmpeg: https://www.gyan.dev/ffmpeg/builds/  download ffmpeg-release-essentials.zip,
echo           extract it and add its bin folder to the Windows PATH.
echo.
echo Press any key to close...
pause >nul
exit /b 1

:pyfail
echo [!!] Python installation failed. Download it from https://www.python.org/downloads/
echo Press any key to close...
pause >nul
exit /b 1

:fffail
echo [!!] ffmpeg installation failed. See the instructions in README.md
echo Press any key to close...
pause >nul
exit /b 1

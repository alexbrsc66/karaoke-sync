@echo off
rem ---------------------------------------------------------------
rem  Double-click: asks for the video/audio, the timing file and
rem  where to save. Or drag a video onto this file: it looks for
rem  videoname.karaoke.json (or .lrc) next to the video or in Downloads.
rem ---------------------------------------------------------------
setlocal
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if not defined PY goto nopython

%PY% "%~dp0render.py" %*
echo.
echo Press any key to close...
pause >nul
exit /b

:nopython
echo Python not found.
echo Run "install_requirements.bat" in this folder first.
echo.
echo Press any key to close...
pause >nul

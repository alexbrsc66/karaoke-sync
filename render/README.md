# Karaoke video render

[🇮🇹 Italiano](README.it.md) · 🇬🇧 English

This folder turns the work done in `karaoke.html` (the `.karaoke.json` file) into a **video with the lyrics burned in**. It is only needed for the last step: syncing is done in the web page, with nothing to install.

## Contents

| File | Purpose |
|---|---|
| `install_requirements.bat` | checks for Python and ffmpeg and installs them if missing |
| `render.bat` | starts the render (double-click, or drag a video onto it) |
| `render.py` | the actual program, used by `render.bat` |

## Installation (once)

1. Double-click **`install_requirements.bat`**.
2. If Python or ffmpeg are missing, they are installed with `winget` (included in Windows 10/11, no administrator rights needed).
3. If it installed anything, **close the window** and open `render.bat` in a new one, so Windows picks up the newly installed programs.

### Installing by hand

**Python 3** (3.9 or later)
- Download it from <https://www.python.org/downloads/>.
- In the installer tick **"Add python.exe to PATH"** and keep **"tcl/tk and IDLE"** enabled (needed for the file dialogs).
- Check from a terminal: `python --version`.

**ffmpeg**
- With winget: `winget install Gyan.FFmpeg`
- Or download `ffmpeg-release-essentials.zip` from <https://www.gyan.dev/ffmpeg/builds/>, extract it (for example to `C:\ffmpeg`) and add its `bin` subfolder to the Windows **PATH** (Settings → search "environment variables").
- Check from a terminal: `ffmpeg -version`.

No extra Python libraries are needed: the script only uses the built-in ones.

## Usage

**Easy way — double-click `render.bat`.** Three dialogs appear:
1. choose the **video or audio** to use;
2. choose the **timing file** (`videoname.karaoke.json`, or an `.lrc`); if one with the same name as the video exists, it is preselected;
3. choose **where to save** the finished video.

Rendering then starts with a progress percentage; when done, the folder with the result opens.

**Dragging a video onto `render.bat`** asks no questions: it looks for `videoname.karaoke.json` (or `.lrc`) in the video's folder or in *Downloads* and saves `videoname.karaoke.mp4` next to the video. If it cannot find the timing file, it asks you for it.

**From a terminal:**

```bash
python render.py video.mp4 project.karaoke.json output.mp4
```

## Linux and macOS

Not tested by the author, but `render.py` only needs Python 3 and ffmpeg, so it should work:

1. Install Python 3 (with tkinter, only needed for the file dialogs) and ffmpeg with your package manager, for example `sudo apt install python3 python3-tk ffmpeg` on Debian/Ubuntu or `brew install python-tk ffmpeg` on macOS.
2. Make sure your ffmpeg has the `libx264` encoder and the `ass` filter (`ffmpeg -encoders | grep libx264`, `ffmpeg -filters | grep ' ass '`). Some distributions ship a reduced build, for example Fedora's default `ffmpeg-free` has no H.264 encoder.
3. Run it from a terminal:

   ```bash
   python3 render.py video.mp4 project.karaoke.json output.mp4
   ```

   Without arguments it opens the file dialogs (needs tkinter).

The lyrics use the Arial font, falling back to whatever font the system picks if it is missing. If you write a `.sh` launcher or an installer for your system, a pull request is welcome.

## Notes

- If the source is an **audio-only** file (`.wav`, `.mp3`…), the video gets a black background.
- The colors chosen in the page are stored inside the `.karaoke.json` and used by the render. An `.lrc` file does not contain them: default colors apply (white, orange, black outline).
- To sync it is easier to listen to the vocals-only track; for the final video you can then choose the instrumental as the source, as long as the timing file is the right one.
- The colour runs through each line word by word, in proportion to the length of the words, from the start of the line to the end of its singing (the blue marker in the page). Lines that wrap onto two rows therefore fill the first row and then the second. Without an end marker it spans the gap to the next line, at most 6 s.
- The result is an H.264 + AAC mp4. Rendering takes roughly the time of a short video encode, depending on length and on the computer.

## Common problems

| Message | What to do |
|---|---|
| "Python not found" | run `install_requirements.bat`, then reopen `render.bat` |
| "ffmpeg not found" | run `install_requirements.bat`; if you just installed it, close and reopen the window |
| "Timing file not found" | start `render.bat` by double-click and pick the file by hand |
| "No line with a time in the file" | the file has no synced line: go back to `karaoke.html` |
| the final video has unreadable lyrics | change the colors in `karaoke.html`, save the project again and re-render |

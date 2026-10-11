"""Karaoke render: video/audio + timings (.karaoke.json or .lrc) -> mp4 with burned-in lyrics.

Ways to use it:
  - double-click render.bat          -> dialogs to pick the video, the timing file and where to save
  - drag a video onto render.bat     -> looks for <video>.karaoke.json / .lrc next to the video or in Downloads
  - command line:  python render.py video.mp4 [project.karaoke.json|file.lrc] [output.mp4]
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path


def find_tool(name):
    p = shutil.which(name)
    if p:
        return p
    links = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft/WinGet/Links' / (name + '.exe')
    if links.exists():
        return str(links)
    sys.exit(f'{name} not found. Install it with: winget install Gyan.FFmpeg')


def load_lines(path):
    txt = Path(path).read_text(encoding='utf-8-sig')
    if txt.lstrip().startswith(('{', '[{', '[\n', '[ ')):
        try:
            j = json.loads(txt)
            arr = j['lines'] if isinstance(j, dict) else j
            orig = isinstance(j, dict) and j.get('mode') == 'orig'   # page set to "Showing: Original"
            return [((l.get('orig') or l['text']) if orig else l['text'], l['t']) for l in arr if l.get('t') is not None]
        except (ValueError, KeyError):
            pass
    out = []
    for raw in txt.splitlines():
        m = re.match(r'\s*\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)', raw)
        if m:
            out.append((m.group(3), int(m.group(1)) * 60 + float(m.group(2))))
    return out


def ts(t):
    cs = round(t * 100)
    return f'{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}'


def esc(s):
    return s.replace('\\', '\\\\').replace('{', '(').replace('}', ')')


def ass_color(hexs, default):
    m = re.fullmatch(r'#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', hexs or '')
    r, g, b = m.groups() if m else re.fullmatch(r'#?(..)(..)(..)', default).groups()
    return f'&H00{b}{g}{r}'.upper().replace('&H', '&H')


def load_style(path):
    try:
        j = json.loads(Path(path).read_text(encoding='utf-8-sig'))
        return j.get('style', {}) if isinstance(j, dict) else {}
    except ValueError:
        return {}


def build_ass(lines, w, h, dur, style=None):
    style = style or {}
    c_text = ass_color(style.get('text'), '#ffffff')
    c_hi = ass_color(style.get('hi'), '#ffb020')
    c_out = ass_color(style.get('outline'), '#000000')
    c_next = ass_color(style.get('next'), '#ffd27a')
    lines = sorted(lines, key=lambda x: x[1])
    big, small = round(h * 0.075), round(h * 0.045)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cur,Arial,{big},{c_hi},{c_text},{c_out},&H80000000,-1,0,0,0,100,100,0,0,1,{max(3, big // 12)},1,2,{round(w * .04)},{round(w * .04)},{round(h * .13)},1
Style: Next,Arial,{small},{c_next},{c_next},{c_out},&H80000000,-1,0,0,0,100,100,0,0,1,{max(2, small // 14)},1,2,{round(w * .04)},{round(w * .04)},{round(h * .04)},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    if lines and lines[0][1] > 0.5:  # preview of the first line before it starts
        ev.append(f'Dialogue: 0,{ts(0)},{ts(lines[0][1])},Next,,0,0,0,,{esc(lines[0][0])}')
    for i, (text, t) in enumerate(lines):
        nxt = lines[i + 1][1] if i + 1 < len(lines) else None
        end = nxt if nxt is not None else min(t + 6, dur)
        sweep = min(end, t + 6) - t
        ev.append(f'Dialogue: 0,{ts(t)},{ts(end)},Cur,,0,0,0,,{{\\kf{max(1, round(sweep * 100))}}}{esc(text)}')
        if nxt is not None:
            ev.append(f'Dialogue: 0,{ts(t)},{ts(end)},Next,,0,0,0,,{esc(lines[i + 1][0])}')
    return head + '\n'.join(ev) + '\n'


VIDEO_TYPES = [('Video and audio', '*.mp4 *.mkv *.mov *.avi *.webm *.m4v *.wav *.mp3 *.flac *.m4a *.aac *.ogg'), ('All files', '*.*')]
PROJ_TYPES = [('Karaoke project', '*.json *.lrc'), ('All files', '*.*')]


def guess_project(video):
    for d in (video.parent, Path.home() / 'Downloads'):
        for suf in ('.karaoke.json', '.lrc'):
            c = d / (video.stem + suf)
            if c.exists():
                return c
    return None


def open_folder(path):
    try:
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', str(path)])
        else:
            subprocess.Popen(['xdg-open', str(path)])
    except (OSError, AttributeError):
        pass


def main():
    args = sys.argv[1:]
    interactive = not args
    tk = fd = mb = None
    if len(args) < 3:                      # a dialog may be needed
        try:
            import tkinter as tk
            from tkinter import filedialog as fd, messagebox as mb
        except ImportError:
            tk = None
    root = None
    if tk:
        root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True)

    # 1) video or audio
    if args:
        video = Path(args[0]).resolve()
    else:
        if not root:
            sys.exit(__doc__)
        f = fd.askopenfilename(title='1/3 - Choose the VIDEO (or audio) to use', filetypes=VIDEO_TYPES)
        if not f:
            sys.exit('Cancelled.')
        video = Path(f)

    # 2) timing file
    proj = Path(args[1]) if len(args) > 1 else guess_project(video)
    if root and (interactive or proj is None):
        f = fd.askopenfilename(title='2/3 - Choose the timing file (.karaoke.json or .lrc)', filetypes=PROJ_TYPES,
                               initialdir=str((proj.parent if proj else video.parent)),
                               initialfile=(proj.name if proj else ''))
        if not f:
            sys.exit('Cancelled.')
        proj = Path(f)
    if proj is None:
        sys.exit('Timing file not found. Save it from the page with "Save project", then double-click render.bat to pick it.')

    # 3) where to save
    if len(args) > 2:
        out = Path(args[2])
    else:
        out = video.with_name(video.stem + '.karaoke.mp4')
        if root and interactive:           # dragging a video: save next to it without asking
            f = fd.asksaveasfilename(title='3/3 - Where should the finished video be saved?', defaultextension='.mp4',
                                     filetypes=[('MP4 video', '*.mp4')], initialdir=str(out.parent), initialfile=out.name)
            if not f:
                sys.exit('Cancelled.')
            out = Path(f)

    ffmpeg, ffprobe = find_tool('ffmpeg'), find_tool('ffprobe')
    info = json.loads(subprocess.check_output([ffprobe, '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height:format=duration', '-of', 'json', str(video)]))
    audio_only = not info.get('streams')
    w, h = (1280, 720) if audio_only else (info['streams'][0]['width'], info['streams'][0]['height'])
    dur = float(info['format']['duration'])

    lines = load_lines(proj)
    if not lines:
        sys.exit('No line with a time in the file.')
    print(f'Source   : {video.name} ({"audio only, black background" if audio_only else "video"} {w}x{h}, {dur:.0f}s)')
    print(f'Timings  : {proj.name} ({len(lines)} synced lines)')
    print(f'Output   : {out}')

    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / 'sub.ass').write_text(build_ass(lines, w, h, dur, load_style(proj)), encoding='utf-8')
        if audio_only:
            src = ['-f', 'lavfi', '-i', f'color=c=black:s={w}x{h}:r=25', '-i', str(video), '-shortest']
        else:
            src = ['-i', str(video)]
        cmd = [ffmpeg, '-y', '-loglevel', 'error', '-nostats', '-progress', 'pipe:1', *src, '-vf', 'ass=sub.ass',
               '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-b:a', '192k', str(out)]
        pr = subprocess.Popen(cmd, cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
        noise = re.compile(r'^(frame|fps|stream_\d+_\d+_q|bitrate|total_size|out_time_us|out_time_ms|out_time|dup_frames|drop_frames|speed|progress)=')
        errors = []
        for line in pr.stdout:
            line = line.strip()
            if line.startswith('out_time_us='):
                try:
                    pct = min(100, int(line.split('=')[1]) / 1e6 / dur * 100)
                    print(f'\rRendering... {pct:5.1f}%', end='', flush=True)
                except ValueError:
                    pass
            elif line and not noise.match(line):
                errors.append(line)
        pr.wait()
        print()
        if pr.returncode != 0:
            msg = 'ffmpeg reported an error:\n' + '\n'.join(errors[-8:])
            if root:
                mb.showerror('Render failed', msg)
            sys.exit(msg)
    print('Done:', out)
    if root and interactive:
        mb.showinfo('Karaoke ready', f'Video saved to:\n{out}')
        open_folder(out.parent)


if __name__ == '__main__':
    main()

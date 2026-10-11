# Render del video karaoke

🇮🇹 Italiano · [🇬🇧 English](README.md)

> I messaggi dei programmi sono in inglese; nella tabella in fondo c'è il significato.

Questa cartella trasforma il lavoro fatto in `karaoke.html` (il file `.karaoke.json`) in un **video con le scritte incise**. Serve solo per l'ultimo passaggio: la sincronizzazione si fa nella pagina web, senza installare nulla.

## Contenuto

| File | A cosa serve |
|---|---|
| `install_requirements.bat` | controlla Python e ffmpeg e li installa se mancano |
| `render.bat` | avvia il render (doppio clic, oppure trascina un video sopra) |
| `render.py` | il programma vero e proprio, usato da `render.bat` |

## Installazione (una volta sola)

1. Doppio clic su **`install_requirements.bat`**.
2. Se Python o ffmpeg mancano, vengono installati con `winget` (incluso in Windows 10/11, non servono i diritti di amministratore).
3. Se ha installato qualcosa, **chiudi la finestra** e apri `render.bat` in una finestra nuova, così Windows riconosce i programmi appena installati.

### Se preferisci installare a mano

**Python 3** (versione 3.9 o successiva)
- Scaricalo da <https://www.python.org/downloads/>.
- Nel programma di installazione spunta **"Add python.exe to PATH"** e lascia attiva l'opzione **"tcl/tk and IDLE"** (serve per le finestre di scelta file).
- Verifica da un terminale: `python --version`.

**ffmpeg**
- Con winget: `winget install Gyan.FFmpeg`
- Oppure da <https://www.gyan.dev/ffmpeg/builds/> scarica `ffmpeg-release-essentials.zip`, estrailo (per esempio in `C:\ffmpeg`) e aggiungi la sottocartella `bin` al **PATH** di Windows (Impostazioni → cerca "variabili d'ambiente").
- Verifica da un terminale: `ffmpeg -version`.

Non servono librerie Python aggiuntive: lo script usa solo quelle incluse.

## Uso

**Modo semplice — doppio clic su `render.bat`.** Compaiono tre finestre:
1. scegli il **video o l'audio** da usare;
2. scegli il **file dei tempi** (`nomevideo.karaoke.json`, oppure un `.lrc`); se ne trova uno con lo stesso nome del video, lo propone già selezionato;
3. scegli **dove salvare** il video finito.

Poi parte il rendering con la percentuale di avanzamento; alla fine si apre la cartella del risultato.

**Trascinando un video su `render.bat`** non vengono fatte domande: cerca `nomevideo.karaoke.json` (o `.lrc`) nella cartella del video o in *Download* e salva `nomevideo.karaoke.mp4` accanto al video. Se non trova il file dei tempi, te lo chiede.

**Da terminale:**

```bash
python render.py video.mp4 lavoro.karaoke.json uscita.mp4
```

## Linux e macOS

Non provato dall'autore, ma `render.py` richiede solo Python 3 e ffmpeg, quindi dovrebbe funzionare:

1. Installa Python 3 (con tkinter, serve solo per le finestre di scelta file) e ffmpeg con il gestore pacchetti, per esempio `sudo apt install python3 python3-tk ffmpeg` su Debian/Ubuntu oppure `brew install python-tk ffmpeg` su macOS.
2. Controlla che il tuo ffmpeg abbia l'encoder `libx264` e il filtro `ass` (`ffmpeg -encoders | grep libx264`, `ffmpeg -filters | grep ' ass '`). Alcune distribuzioni includono una versione ridotta: per esempio `ffmpeg-free` di Fedora non ha l'encoder H.264.
3. Lancialo da terminale:

   ```bash
   python3 render.py video.mp4 progetto.karaoke.json uscita.mp4
   ```

   Senza argomenti apre le finestre di scelta file (serve tkinter).

Per le scritte viene usato il font Arial, o quello che il sistema sceglie se manca. Se scrivi uno script `.sh` o un installatore per il tuo sistema, una pull request è benvenuta.

## Note

- Se come sorgente scegli un file **solo audio** (`.wav`, `.mp3`…), il video avrà lo sfondo nero.
- I colori scelti nella pagina sono salvati dentro il `.karaoke.json` e vengono usati dal render. Un file `.lrc` non li contiene: si usano i colori predefiniti (bianco, arancione, contorno nero).
- Per sincronizzare conviene ascoltare la traccia con la sola voce; per il video finale si può poi scegliere la base strumentale come sorgente, purché il file dei tempi sia quello giusto.
- Il colore scorre su ogni riga parola per parola, in proporzione alla lunghezza delle parole, dall'inizio della riga alla fine del canto (il segnale blu nella pagina). Le righe che vanno a capo su due righe riempiono quindi prima la prima riga e poi la seconda. Senza un segnale di fine copre l'intervallo fino alla riga successiva, al massimo 6 s.
- Il risultato è un mp4 H.264 + AAC. Il rendering richiede più o meno il tempo di una breve codifica video: dipende dalla durata e dal computer.

## Problemi comuni

| Messaggio | Cosa fare |
|---|---|
| "Python not found" (Python non trovato) | esegui `install_requirements.bat`, poi riapri `render.bat` |
| "ffmpeg not found" (ffmpeg non trovato) | esegui `install_requirements.bat`; se l'hai appena installato, chiudi e riapri la finestra |
| "Timing file not found" (file dei tempi non trovato) | avvia `render.bat` con doppio clic e scegli il file a mano |
| "No line with a time in the file" (nessuna riga con tempo) | nel file non c'è nessuna riga sincronizzata: torna a `karaoke.html` |
| il video finale ha le scritte illeggibili | cambia i colori in `karaoke.html`, salva di nuovo il lavoro e rifai il render |

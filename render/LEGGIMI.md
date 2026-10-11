# Render del video karaoke

Questa cartella trasforma il lavoro fatto in `karaoke.html` (il file `.karaoke.json`) in un **video con le scritte incise**. Serve solo per l'ultimo passaggio: la sincronizzazione si fa nella pagina web, senza installare nulla.

## Contenuto

| File | A cosa serve |
|---|---|
| `installa_requisiti.bat` | controlla Python e ffmpeg e li installa se mancano |
| `render.bat` | avvia il render (doppio clic, oppure trascina un video sopra) |
| `render.py` | il programma vero e proprio, usato da `render.bat` |

## Installazione (una volta sola)

1. Doppio clic su **`installa_requisiti.bat`**.
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

## Note

- Se come sorgente scegli un file **solo audio** (`.wav`, `.mp3`…), il video avrà lo sfondo nero.
- I colori scelti nella pagina sono salvati dentro il `.karaoke.json` e vengono usati dal render. Un file `.lrc` non li contiene: si usano i colori predefiniti (bianco, arancione, contorno nero).
- Per sincronizzare conviene ascoltare la traccia con la sola voce; per il video finale si può poi scegliere la base strumentale come sorgente, purché il file dei tempi sia quello giusto.
- Il risultato è un mp4 H.264 + AAC. Il rendering richiede più o meno il tempo di una breve codifica video: dipende dalla durata e dal computer.

## Problemi comuni

| Messaggio | Cosa fare |
|---|---|
| "Python non trovato" | esegui `installa_requisiti.bat`, poi riapri `render.bat` |
| "ffmpeg non trovato" | esegui `installa_requisiti.bat`; se l'hai appena installato, chiudi e riapri la finestra |
| "Non trovo il file dei tempi" | avvia `render.bat` con doppio clic e scegli il file a mano |
| "Nessuna riga con tempo" | nel file non c'è nessuna riga sincronizzata: torna a `karaoke.html` |
| il video finale ha le scritte illeggibili | cambia i colori in `karaoke.html`, salva di nuovo il lavoro e rifai il render |

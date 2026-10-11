# Karaoke Sync

🇮🇹 Italiano · [🇬🇧 English](README.md)

> L'interfaccia del programma e i messaggi degli script sono in inglese: qui i pulsanti e i comandi sono indicati con i loro nomi originali.

Uno strumento semplice per **sincronizzare i testi su un video o un brano audio** e produrre un video karaoke con le parole che si colorano a tempo.

Si usa premendo un tasto mentre il video gira: ogni pressione segna l'inizio della riga successiva. Poi si rifinisce guardando la forma d'onda. Niente account, niente installazioni per la parte di sincronizzazione: è una singola pagina HTML che gira nel browser.

![Karaoke Sync: la pagina con il video, la forma d'onda con i segnali delle righe e la lista delle righe sincronizzate](docs/screenshot.png)

## Cosa fa

- **Sincronizzazione a tap**: `Spazio` (o un clic sul video) assegna il tempo attuale alla riga corrente e passa alla successiva.
- **Forma d'onda** sopra la barra di avanzamento, con zoom (rotella), spostamento (trascina) e i punti di inizio riga disegnati sopra. I punti si **trascinano** per correggerli con precisione.
- **Modifica del testo** riga per riga (doppio clic), aggiunta ed eliminazione di righe, righe vuote per le pause. I tempi non si perdono. `Ctrl+Z` annulla.
- **Testo originale / cover**: ogni riga può contenere due testi. Il pulsante **🔤 Showing: Cover / Original** sceglie quale mostrare, modificare, vedere in anteprima e usare nel render; l'altro resta visibile in piccolo e in grigio sotto ogni riga, comodo per scrivere una cover sopra il testo originale.
- **Barra di colore che segue il canto**: ogni riga può avere un segnale di fine (blu, tratteggiato) che indica dove finisce il canto. **⇥ Auto ends** li trova dalla forma d'onda e si possono trascinare. Il render riempie la riga esattamente dall'inizio a quella fine, invece di distribuirla sull'intervallo fino alla riga successiva.
- **Velocità ridotta** (0.5x, 0.75x) e **anticipo tap** regolabile per compensare i tempi di reazione.
- **Colori configurabili** (testo, evidenziazione, contorno, riga successiva) per video chiari o scuri.
- **Salvataggio automatico** nel browser, **Save project / Load project** su file `.karaoke.json`, esportazione `.lrc`.
- **Render finale** con ffmpeg: video con le scritte incise, sincronizzate al fotogramma. Funziona anche con un file solo audio (sfondo nero).

## Requisiti

| Cosa | Per cosa | Note |
|---|---|---|
| Browser Chrome o Edge | pagina di sincronizzazione | Firefox funziona ma salva i file sempre in Download |
| Python 3 | render finale | usa solo la libreria standard (serve anche tkinter, incluso di default) |
| ffmpeg | render finale | Windows: `winget install Gyan.FFmpeg` |

La pagina di sincronizzazione non richiede nulla. Python e ffmpeg servono solo per il render, che sta nella cartella [`render/`](render/): lì `install_requirements.bat` controlla e installa ciò che manca (istruzioni complete in [`render/README.it.md`](render/README.it.md)).

Provato **solo su Windows 11**. Su altri sistemi la pagina dovrebbe funzionare uguale; `render.bat` è specifico di Windows, ma `render.py` si può lanciare ovunque.

## Come si usa

### 1. Sincronizzare

1. Apri `karaoke.html` (doppio clic).
2. **🎬 Video** → scegli il video o l'audio. **📄 Lyrics / LRC** → scegli il testo, una riga per verso (oppure incollalo con **✏️ Edit text**).
3. Fai partire con `Invio` e premi `Spazio` quando parte ogni riga. Se sbagli: `⌫` annulla l'ultimo tap.
4. Rifinisci: trascina i segnali arancioni sulla forma d'onda, oppure usa `[` e `]` (∓0,1 s) e i pulsanti di ogni riga.
5. **💾 Save project** → salva `nomevideo.karaoke.json` accanto al video.

> Per brani con voce e base separate, conviene sincronizzare ascoltando la traccia **solo voce** (l'attacco delle parole è molto più chiaro) e renderizzare poi con la base.

### 2. Creare il video

La prima volta esegui `render/install_requirements.bat` (installa Python e ffmpeg se mancano).

- **Doppio clic su `render/render.bat`**: compaiono tre finestre — video/audio, file dei tempi, dove salvare. Poi parte il rendering con la percentuale di avanzamento.
- **Oppure** trascina il video su `render/render.bat`: cerca da solo `nomevideo.karaoke.json` (o `.lrc`) accanto al video o in Download.
- **Oppure** da terminale:

  ```bash
  python render/render.py video.mp4 lavoro.karaoke.json uscita.mp4
  ```

Il risultato è un mp4 (H.264 + AAC). I colori scelti nella pagina sono salvati nel `.karaoke.json` e vengono usati dal render.

## Scorciatoie

| Tasto | Azione |
|---|---|
| `Spazio` / clic sul video | segna la riga corrente |
| `Invio` | play / pausa |
| `⌫` | annulla l'ultimo tap (e torna indietro di 2 s) |
| `Canc` | cancella il tempo della riga selezionata |
| `←` `→` | ∓3 secondi |
| `↑` `↓` | riga precedente / successiva |
| `[` `]` | sposta la riga corrente di ∓0,1 s |
| doppio clic su una riga | modifica il testo (`Invio` conferma, `Ctrl+Invio` aggiunge una riga sotto) |
| `Ctrl+Z` | annulla le modifiche alle righe |

Sulla forma d'onda: rotella = zoom, trascina = sposta, clic = vai lì, trascina un segnale arancione = sposta l'inizio di quella riga, trascina un segnale blu = sposta la fine del canto, doppio clic = vista intera.

## Suggerimenti

### Separare voce e base con Ultimate Vocal Remover

Il trucco che rende la sincronizzazione **molto più veloce**: separa la canzone in voce e base con [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui) (programma gratuito che usa modelli di intelligenza artificiale), poi:

1. carica nella pagina la traccia con **la sola voce**: nella forma d'onda ogni parola è ben staccata dal resto, e si vede e si sente esattamente dove attacca ogni riga;
2. segna i tempi con `Spazio` e correggi i segnali sulla forma d'onda;
3. per il video finale, nel render scegli invece la **base strumentale** come sorgente audio, con lo stesso file dei tempi.

Così non c'è la voce originale sopra la base e i tempi restano precisi, perché le due tracce hanno la stessa durata. Se i file sono stati separati con lo stesso programma, il file `nomevoce.karaoke.json` si può usare anche per la base scegliendolo a mano nella seconda finestra del render.

### Scrivere una cover

Incolla prima il testo originale, passa a **Original** e scrivilo, poi torna a **Cover** e scrivi le tue parole riga per riga: l'originale resta in grigio sotto ogni riga, così puoi contare le sillabe. I tempi sono comuni ai due testi. Prima di salvare il lavoro usa lo stesso pulsante per scegliere con quale versione fare il video.

### Far seguire la voce alla barra di colore

Dopo aver sincronizzato gli inizi premi **⇥ Auto ends** (meglio con la traccia di sola voce): legge la forma d'onda e mette un segnale blu di fine dove ogni riga smette di essere cantata. Controllali con lo zoom e trascina quelli sbagliati. Un secondo clic riempie solo quelli mancanti, quindi le correzioni a mano restano; con **Maiusc+clic** li ricalcola tutti. Le righe senza segnale di fine mantengono il comportamento di prima.

Per correggere una fine a mano, ingrandisci con la rotella e trascina il suo segnale blu (`⟧` con il numero della riga): il video salta 1 s prima della nuova fine, così puoi ascoltarla con `Invio`. `Ctrl+Z` annulla un trascinamento. Salva poi il progetto: il render legge le fini dal `.karaoke.json`, non da un `.lrc`.

### Altri consigli

- Se segni i tempi in ritardo o in anticipo in modo costante, regola **Tap lead**: il valore viene sottratto a ogni tap.
- Per le parti difficili, rallenta a **0.5x** e usa lo zoom sulla forma d'onda.
- Una **riga vuota** (pulsante ＋) cancella il testo dallo schermo: usala per le pause strumentali.
- Salva il lavoro ogni tanto con **💾 Save project**: il salvataggio automatico del browser è comodo ma resta sul tuo computer.

## Formati

- **`.karaoke.json`**: `{ "version": 3, "video": "nome", "mode": "cover", "style": { "text", "hi", "outline", "next" }, "lines": [ { "text": "cover", "orig": "originale", "t": 12.34, "e": 15.2 } ] }`, con `t` in secondi (`null` se la riga non è ancora sincronizzata). `e` è la fine del canto di quella riga, facoltativa (senza, la barra copre l'intervallo fino alla riga successiva, al massimo 6 s). `mode` è `cover` oppure `orig` e decide quale testo viene inciso nel render (se una riga non ha il testo originale si usa quello della cover).
- **`.lrc`**: formato standard `[mm:ss.xx]testo`. Contiene i tempi ma non i colori.

## Limiti noti

- La forma d'onda decodifica il file nel browser: per file sopra circa 600 MB viene saltata (il resto funziona).
- I video che il browser non sa riprodurre (alcuni `.mkv`, H.265) non si possono sincronizzare nella pagina; vanno convertiti in mp4 H.264 oppure si usa il solo audio.
- Il render usa il font Arial e uno stile fisso (posizione in basso, dimensione proporzionale al video). Si cambia in `build_ass()` dentro `render/render.py`.
- Il browser salva il lavoro automaticamente solo sul proprio computer: per spostarlo o tenerne una copia usa **Save project**.

## Come è stato realizzato

Questo progetto è stato scritto da un'**intelligenza artificiale (Claude, tramite Claude Code)** seguendo le richieste e i feedback di una persona: è stata la persona a decidere cosa serviva e come doveva comportarsi lo strumento, a provarlo su canzoni vere e a segnalare ogni problema, e l'IA ha scritto il codice e lo ha corretto di conseguenza. Il codice non è stato revisionato riga per riga da uno sviluppatore: è stato collaudato nell'uso, quindi è normale trovare spigoli. Segnalazioni e correzioni sono benvenute.

## Licenza

[PolyForm Noncommercial 1.0.0](LICENSE): puoi usare, copiare e modificare il programma liberamente per scopi **non commerciali** (uso personale, hobby, studio, associazioni senza scopo di lucro). L'uso commerciale non è consentito. Il software è fornito **così com'è, senza alcuna garanzia e senza responsabilità** dell'autore.

Nota: non è una licenza open source in senso stretto, proprio perché vieta l'uso commerciale.

# FastFocus ⚡

**FastFocus** è un software di lettura veloce basato sulla tecnica **RSVP** (Rapid Serial Visual Presentation), scritto interamente in Python puro utilizzando la libreria grafica Tkinter.

Il programma permette di leggere testi (incollati o caricati da file) mostrando una parola alla volta a velocità elevata, ottimizzando il movimento oculare attraverso il posizionamento del punto focale.

## 🚀 Caratteristiche principali

* **Algoritmo ORP (Optimal Recognition Point)**: Ogni parola viene centrata sulla lettera che permette al cervello di riconoscerla più velocemente. La lettera focale è evidenziata in rosso.
* **Gestione Intelligente della Punteggiatura**: Inserisce automaticamente dei micro-ritardi quando incontra punti, virgole o punti interrogativi per simulare una lettura naturale.
* **Controllo Dinamico della Velocità**: Regola i WPM (Words Per Minute) tramite slider o inserimento manuale da tastiera.
* **Supporto File .TXT**: Carica file di testo direttamente dal tuo computer.
* **Interfaccia Minimalista**: Progettata per ridurre le distrazioni e massimizzare la concentrazione.

## 🛠️ Requisiti

* **Python 3.x**: Il programma non richiede librerie esterne (usa solo la Standard Library).
* **Tkinter**: Solitamente incluso nelle installazioni standard di Python.

## 📦 Installazione e Utilizzo

1. **Clona la repository**:
   ```bash
   git clone [https://github.com/tuo-username/FastFocus.git](https://github.com/tuo-username/FastFocus.git)
   cd FastFocus
2. **Avvia l'applicazione:**
   ```bash
   python main.py
   
## ⌨️ Comandi Rapidi

| Comando | Descrizione |
| :--- | :--- |
| **START READING** | Inizia la sessione di lettura caricando il testo presente nell'area di input. |
| **ESC** | Interrompe la lettura in qualsiasi momento e torna al menu principale. |
| **INVIO** | Premuto all'interno della casella WPM, conferma e applica la velocità inserita manualmente. |
| **SPAZIO** | Mette in pausa o riprende la lettura senza uscire dal lettore. |
## 📂 Struttura del Progetto

Il progetto è strutturato in modo modulare per separare la logica dalla presentazione:

* **`main.py`**: Gestisce l'interfaccia grafica (GUI) con Tkinter, il passaggio tra i frame e il coordinamento del ciclo di lettura.
* **`logic.py`**: Contiene il motore di elaborazione: calcolo dell'ORP (Optimal Recognition Point) e gestione dei ritardi basati sulla punteggiatura.
* **`config.py`**: Centralizza tutte le impostazioni: colori del tema (Dark Mode), font monospaziati, tempi di delay e il testo predefinito.
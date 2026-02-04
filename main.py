import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from logic import FastFocusEngine
import config


class FastFocusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastFocus - RSVP Speed Reader")
        self.root.geometry("800x500")
        self.root.configure(bg=config.BG_COLOR)

        self.words = []
        self.current_idx = 0
        self.is_running = False
        self.is_paused = False  # Aggiungi questa riga
        self.wpm = config.DEFAULT_WPM

        # 1. Container Principali
        self.menu_frame = tk.Frame(self.root, bg=config.BG_COLOR)
        self.reader_frame = tk.Frame(self.root, bg=config.BG_COLOR)

        # Inizializziamo entrambi
        self.setup_menu_ui()
        self.setup_reader_ui()

        # Mostriamo solo il menu all'inizio
        self.menu_frame.pack(expand=True, fill=tk.BOTH)

    def setup_menu_ui(self):
        # Area Testo
        self.input_area = scrolledtext.ScrolledText(self.menu_frame, height=10, bg="#2d2d2d", fg="white",
                                                    font=("Arial", 12))
        self.input_area.pack(pady=20, padx=20, fill=tk.X)
        self.input_area.insert(tk.INSERT, config.DEFAULT_TEXT)

        # Controlli WPM
        wpm_control_frame = tk.Frame(self.menu_frame, bg=config.BG_COLOR)
        wpm_control_frame.pack(pady=10)

        tk.Label(wpm_control_frame, text="WPM:", bg=config.BG_COLOR, fg="white").pack(side=tk.LEFT)
        self.wpm_var = tk.StringVar(value=str(config.DEFAULT_WPM))
        self.wpm_entry = tk.Entry(wpm_control_frame, textvariable=self.wpm_var, width=6, justify='center', bg="#2d2d2d",
                                  fg="white", insertbackground="white")
        self.wpm_entry.pack(side=tk.LEFT, padx=5)
        self.wpm_entry.bind("<Return>", self.on_entry_wpm)

        self.wpm_slider = tk.Scale(self.menu_frame, from_=100, to_=1000, orient=tk.HORIZONTAL, showvalue=False,
                                   bg=config.BG_COLOR, fg="white", highlightthickness=0, command=self.update_wpm)
        self.wpm_slider.set(config.DEFAULT_WPM)
        self.wpm_slider.pack(pady=5, padx=100, fill=tk.X)

        # Bottoni
        btn_container = tk.Frame(self.menu_frame, bg=config.BG_COLOR)
        btn_container.pack(pady=20)

        self.load_btn = tk.Label(btn_container, text="📂 APRI .TXT", bg="#555555", fg="white",
                                 font=("Arial", 11, "bold"), pady=10, padx=20, cursor="hand2")
        self.load_btn.pack(side=tk.LEFT, padx=10)
        self.load_btn.bind("<Button-1>", lambda e: self.load_file())

        self.start_btn = tk.Label(btn_container, text="START READING", bg="#4CAF50", fg="white",
                                  font=("Arial", 12, "bold"), pady=10, padx=20, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.start_btn.bind("<Button-1>", lambda e: self.toggle_reader())

    def setup_reader_ui(self):
        # Canvas del lettore
        self.focus_canvas = tk.Canvas(self.reader_frame, width=800, height=200, bg=config.BG_COLOR,
                                      highlightthickness=0)
        self.focus_canvas.pack(expand=True)

        cx = 400
        self.focus_canvas.create_line(cx, 40, cx, 60, fill=config.HIGHLIGHT_COLOR, width=3)
        self.focus_canvas.create_line(cx, 140, cx, 160, fill=config.HIGHLIGHT_COLOR, width=3)

        # Barra di progresso
        self.progress_canvas = tk.Canvas(self.reader_frame, width=600, height=5, bg=config.PROGRESS_BG,
                                         highlightthickness=0)
        self.progress_canvas.pack(pady=20)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 5, fill=config.PROGRESS_COLOR, width=0)

        # Istruzione per uscire
        tk.Label(self.reader_frame, text="Premi ESC per fermarti", bg=config.BG_COLOR, fg="#777777",
                 font=("Arial", 10)).pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=(("Testo", "*.txt"), ("Tutti", "*.*")))
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.input_area.delete("1.0", tk.END)
                self.input_area.insert(tk.INSERT, f.read())

    def update_wpm(self, val):
        self.wpm = int(val)
        self.wpm_var.set(val)

    def on_entry_wpm(self, event):
        try:
            val = int(self.wpm_var.get())
            self.wpm_slider.set(val)
            self.wpm = val
        except:
            pass

    def toggle_reader(self):
        text = self.input_area.get("1.0", tk.END).strip()
        if not text: return

        self.words = FastFocusEngine.process_text(text)
        self.current_idx = 0
        self.is_running = True

        # Scambio Frame
        self.menu_frame.pack_forget()
        self.reader_frame.pack(expand=True, fill=tk.BOTH)

        self.root.bind('<Escape>', lambda e: self.stop_reading())
        self.root.bind('<space>', lambda e: self.toggle_pause())  # Aggiungi questa riga
        self.is_paused = False  # Assicurati che parta non in pausa
        self.run_reader()

    def stop_reading(self):
        self.is_running = False
        self.reader_frame.pack_forget()
        self.menu_frame.pack(expand=True, fill=tk.BOTH)
        self.root.unbind('<Escape>')

    def run_reader(self):
        # Se non sta girando o è in pausa, interrompi l'esecuzione del ciclo attuale
        if not self.is_running or self.is_paused:
            return

        if self.current_idx >= len(self.words):
            self.stop_reading()
            return

        word = self.words[self.current_idx]
        orp_idx = FastFocusEngine.get_orp_index(word)
        self.render_word(word, orp_idx)

        # Aggiorna Barra
        prog = (self.current_idx / len(self.words)) * 600
        self.progress_canvas.coords(self.progress_bar, 0, 0, prog, 5)

        # Delay
        delay = int(60000 / self.wpm)
        total_delay = FastFocusEngine.get_delay(word, delay, config.PUNCTUATION_DELAY_MULTIPLIER,
                                                config.PUNCTUATION_CHARS)

        self.current_idx += 1
        self.root.after(total_delay, self.run_reader)

    def render_word(self, word, orp_idx):
        self.focus_canvas.delete("word_parts")
        cx, cy = 400, 100
        offset = 11

        pre, orp, post = word[:orp_idx], word[orp_idx], word[orp_idx + 1:]

        self.focus_canvas.create_text(cx, cy, text=orp, fill=config.HIGHLIGHT_COLOR,
                                      font=(config.FONT_FAMILY, config.FONT_SIZE, "bold"), tags="word_parts",
                                      anchor="center")
        if pre:
            self.focus_canvas.create_text(cx - offset, cy, text=pre, fill=config.TEXT_COLOR,
                                          font=(config.FONT_FAMILY, config.FONT_SIZE), tags="word_parts", anchor="e")
        if post:
            self.focus_canvas.create_text(cx + offset, cy, text=post, fill=config.TEXT_COLOR,
                                          font=(config.FONT_FAMILY, config.FONT_SIZE), tags="word_parts", anchor="w")

    def toggle_pause(self):
        """Alterna lo stato di pausa."""
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                # Feedback visivo opzionale sulla canvas
                self.focus_canvas.create_text(400, 180, text="PAUSA", fill="#ff9800",
                                              font=("Arial", 10, "bold"), tags="pause_msg")
            else:
                self.focus_canvas.delete("pause_msg")
                self.run_reader()  # Riprende il ciclo

if __name__ == "__main__":
    root = tk.Tk()
    app = FastFocusApp(root)
    root.mainloop()
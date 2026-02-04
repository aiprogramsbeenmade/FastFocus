import math

class FastFocusEngine:
    @staticmethod
    def get_orp_index(word):
        """Calcola l'indice del punto di riconoscimento ottimale."""
        length = len(word)
        if length <= 1:
            return 0
        elif length <= 5:
            return 1
        elif length <= 9:
            return 2
        elif length <= 13:
            return 3
        else:
            return 4

    @staticmethod
    def process_text(text):
        """Pulisce il testo e restituisce una lista di parole."""
        return text.split()

    @staticmethod
    def get_delay(word, base_delay, multiplier, chars):
        """Calcola se aggiungere un ritardo per la punteggiatura."""
        if word.endswith(chars):
            return int(base_delay * multiplier)
        return base_delay
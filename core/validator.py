import re
from difflib import SequenceMatcher

class CADDataValidator:
    def __init__(self, threshold=0.05):
        self.threshold = threshold
        # Campi che non ammettono errori (scale, quote, coordinate)
        self.critical_keywords = ["scala", "scale", "format", "quota", "coord"]

    def _normalize(self, val):
        """Sostituisce la virgola con il punto per i disegni europei."""
        return str(val).strip().replace(',', '.')

    def evaluate(self, key, val_ocr, val_dwg):
        v_ocr = self._normalize(val_ocr)
        v_dwg = self._normalize(val_dwg)

        # LOGICA RIGIDA: Se contiene numeri o è una parola chiave critica
        if any(char.isdigit() for char in v_ocr) or key.lower() in self.critical_keywords:
            return "MATCH" if v_ocr == v_dwg else "CRITICAL_CONFLICT"

        # LOGICA FUZZY: Per nomi, luoghi e testi puri
        similarity = SequenceMatcher(None, v_ocr, v_dwg).ratio()
        diff = 1.0 - similarity
        
        if diff <= self.threshold:
            return "AUTO_CORRECT" # Differenza minima (<5%), risolve l'IA
        return "TEXT_CONFLICT" # Differenza oltre soglia, chiede all'utente
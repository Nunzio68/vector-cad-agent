class SmartOCREngine:
    def __init__(self, min_confidence=0.85):
        self.min_confidence = min_confidence

    def get_text(self, image_path):
        # Simulazione processo OCR
        # 1. Prima scansione a 300 DPI
        confidenza_rilevata = 0.70 # Esempio di scansione sporca
        
        if confidenza_rilevata < self.min_confidence:
            print(f"[INFO] Confidenza bassa ({confidenza_rilevata}). Attivazione Double-Scan a 600 DPI...")
            # Qui il codice raddoppierebbe la risoluzione prima di riprovare
            return "Risultato Ottimizzato", True
            
        return "Risultato Standard", False
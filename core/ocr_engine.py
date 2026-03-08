import os
from dotenv import load_dotenv

load_dotenv()

class OCREngine:
    def __init__(self):
        self.model_vision = os.getenv("MODEL_VISION")
        self.confidence_threshold = float(os.getenv("OCR_CONFIDENCE_TRIGGER", 0.85))

    def process_image(self, image_path):
        """Simula l'analisi dell'immagine con Llama 3.2-Vision."""
        if not os.path.exists(image_path):
            return None, "File non trovato."
        
        print(f"[OCR] Analisi in corso con {self.model_vision} su {image_path}...")
        
        # Simulazione dati estratti dall'impianto
        extracted_data = {
            "potenza_termica": "24.5 kW",
            "pressione_esercizio": "1.5 bar",
            "località": "Lanciano"
        }
        confidence = 0.82 # Esempio sotto soglia per attivare Dual-Scan
        
        if confidence < self.confidence_threshold:
            print(f"[!] Confidenza {confidence*100}% < {self.confidence_threshold*100}%: ATTIVAZIONE SCAN 600 DPI.")
            # Qui avverrebbe la seconda passata ad alta risoluzione
            confidence = 0.95 
            
        return extracted_data, confidence
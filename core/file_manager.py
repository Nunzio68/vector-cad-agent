import os
import ezdxf
from dotenv import load_dotenv

load_dotenv()

class FileManager:
    def __init__(self):
        self.user_agent = os.getenv("USER_AGENT")
        self.safe_save = os.getenv("ENABLE_SAFE_SAVE") == "True"

    def save_incremental(self, doc, base_filename):
        """Salva il file con suffisso progressivo _v1, _v2 se necessario."""
        name, ext = os.path.splitext(base_filename)
        counter = 1
        new_filename = f"{name}_v{counter}{ext}"
        
        while os.path.exists(new_filename):
            counter += 1
            new_filename = f"{name}_v{counter}{ext}"
            
        try:
            doc.saveas(new_filename)
            return new_filename
        except Exception as e:
            return f"Errore nel salvataggio: {str(e)}"

    def get_headers(self):
        """Ritorna gli header corretti per chiamate esterne."""
        return {"User-Agent": self.user_agent}
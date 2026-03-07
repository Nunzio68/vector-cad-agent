import os
from dotenv import load_dotenv
from core.file_manager import CADFileManager
from core.validator import CADDataValidator
from core.orchestrator import CADOrchestrator

# Carica i parametri dal file .env (Soglia 5%, Disclaimer, ecc.)
load_dotenv()

def main():
    # Inizializzazione con i parametri del .env
    threshold = float(os.getenv("TEXT_THRESHOLD", 0.05))
    
    manager = CADFileManager()
    validator = CADDataValidator(threshold)
    orchestrator = CADOrchestrator()
    
    print(f"--- Vector CAD Agent v1.0 Avviato ---")
    print(f"Soglia tolleranza testo impostata: {threshold*100}%")
    
    # Esempio di flusso su un file (da sostituire con il tuo loop di file)
    file_target = "progetto_test.dwg"
    
    # Qui il sistema inizierà a processare...
    # Se il file è in sola lettura, manager.get_safe_path garantirà il salvataggio _v1
    save_path = manager.get_safe_path(file_target)
    
    print(f"Pronto per il salvataggio sicuro su: {save_path}")

if __name__ == "__main__":
    main()
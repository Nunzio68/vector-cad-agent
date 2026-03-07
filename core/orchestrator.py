class CADOrchestrator:
    def resolve_conflict_ui(self, key, ocr_val, dwg_val, conflict_type):
        print(f"\n--- ATTENZIONE: CONFLITTO RILEVATO [{key}] ---")
        print(f"Lettura OCR: '{ocr_val}'")
        print(f"Dati Originali DWG: '{dwg_val}'")
        print("-" * 45)
        print("Scegli come procedere:")
        print("1) MEDIAZIONE: DeepSeek-R1 analizza e pulisce il refuso (es. Sca1a -> Scala).")
        print("2) PREVALE OCR: Conferma la lettura della scansione.")
        print("3) PREVALE DWG: Mantieni il dato originale del file vettoriale.")
        
        return input("\nInserisci 1, 2 o 3: ").strip()
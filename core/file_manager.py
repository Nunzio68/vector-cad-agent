import os

class CADFileManager:
    """Gestisce il versioning automatico per evitare sovrascritture e blocchi."""
    
    @staticmethod
    def get_safe_path(original_path: str) -> str:
        if not os.path.exists(original_path):
            return original_path
            
        name, ext = os.path.splitext(original_path)
        counter = 1
        # Genera nomi tipo: progetto_v1.dwg, progetto_v2.dwg...
        new_path = f"{name}_v{counter}{ext}"
        
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{name}_v{counter}{ext}"
            
        return new_path
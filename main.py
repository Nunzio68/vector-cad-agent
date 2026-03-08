import os
import ezdxf
import math
import traceback
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

app = Flask(__name__)
CORS(app)

OUTPUT_FOLDER = r"C:\vector-cad-agent\output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Dimensioni ISO Reali
FORMATI_ISO = {
    "A0": (1189, 841), 
    "A1": (841, 594), 
    "A2": (594, 420), 
    "A3": (420, 297), 
    "A4": (210, 297)
}

def get_squadratura_coords(formato):
    """
    Calcola le coordinate della squadratura applicando un margine di rispetto 
    tecnico per i formati >= A3.
    """
    L_F, H_F = FORMATI_ISO.get(formato, (841, 594))
    
    # Margine di rispetto (M): 10mm per A0-A2, 5mm per A3, 0mm per A4
    if formato in ["A0", "A1", "A2"]:
        M = 10.0
    elif formato == "A3":
        M = 5.0
    else:
        M = 3.0 # Minimo sindacale per A4
        
    # Per il tuo caso specifico A1 (841x594) -> 835x590 significa circa 3mm di margine
    if formato == "A1":
        L_SQ, H_SQ = 835.0, 590.0
        off_x = (L_F - L_SQ) / 2
        off_y = (H_F - H_SQ) / 2
        return off_x, off_y, L_SQ, H_SQ
    
    return M, M, L_F - (2*M), H_F - (2*M)

@app.route('/process-plant', methods=['POST', 'GET'])
def process_cad():
    data = request.args.to_dict()
    data.update(request.form.to_dict())
    
    if data.get('comando') == 'STAMPA':
        try:
            tipo = data.get('tipo_progetto', 'IMPIANTO').upper()
            formato = data.get('formato', 'A1').upper()
            L_F, H_F = FORMATI_ISO.get(formato, (841, 594))
            
            # 1. Ottenimento coordinate squadratura parametrica
            ox, oy, l_sq, h_sq = get_squadratura_coords(formato)
            
            doc = ezdxf.new('R2010')
            doc.styles.new('CAD_STYLE', dxfattribs={'font': 'arial.ttf'})
            doc.layers.new('SQUADRATURA', dxfattribs={'color': 7, 'lineweight': 35})
            doc.layers.new('TUBAZIONE', dxfattribs={'color': 1, 'lineweight': 60})
            doc.layers.new('QUOTE', dxfattribs={'color': 3, 'lineweight': 25})
            
            msp = doc.modelspace()
            
            # Disegno Squadratura
            msp.add_lwpolyline([(ox, oy), (ox+l_sq, oy), (ox+l_sq, oy+h_sq), (ox, oy+h_sq), (ox, oy)], 
                               dxfattribs={'layer': 'SQUADRATURA'})
            
            # 2. Logica Vettore Perpendicolare per i Testi (Offset 12mm)
            punti_raw = data.get('punti', "150,150; 600,150; 600,450; 150,450")
            punti = [tuple(map(float, p.split(','))) for p in punti_raw.split(';')]
            
            for i in range(len(punti) - 1):
                p1, p2 = punti[i], punti[i+1]
                msp.add_line(p1, p2, dxfattribs={'layer': 'TUBAZIONE'})
                
                dx, dy = p2[0]-p1[0], p2[1]-p1[1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist == 0: continue
                
                mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
                ang = math.degrees(math.atan2(dy, dx))
                
                # Vettore normale (perpendicolare)
                ux, uy = -dy/dist, dx/dist
                dist_offset = 12.0 # Offset richiesto
                
                if 90 < ang <= 270 or -270 <= ang < -90:
                    ang = (ang - 180) if ang > 0 else (ang + 180)
                    dist_offset = -dist_offset # Inverte per restare sul lato corretto

                txt = msp.add_text(f"L={dist:.1f}", dxfattribs={'layer': 'QUOTE', 'height': 7, 'rotation': ang, 'style': 'CAD_STYLE'})
                txt.set_placement((mx + ux*dist_offset, my + uy*dist_offset))

            # Rendering PDF con sfondo bianco forzato
            fig = plt.figure(figsize=(L_F/25.4, H_F/25.4), facecolor='white')
            ax = fig.add_axes([0, 0, 1, 1], facecolor='white')
            ax.set_xlim(0, L_F); ax.set_ylim(0, H_F); ax.axis('off')
            
            ctx = RenderContext(doc)
            Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp, finalize=True)
            
            path_pdf = os.path.join(OUTPUT_FOLDER, "BACKUP_SICUREZZA.pdf")
            fig.savefig(path_pdf, format='pdf', dpi=300)
            plt.close(fig)
            
            return jsonify({"status": "Backup Completato", "formato": formato, "squadra": f"{l_sq}x{h_sq}"})
        except Exception:
            return jsonify({"status": "error", "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
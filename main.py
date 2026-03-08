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

# Configurazione A1
L_A1, H_A1 = 841.0, 594.0

@app.route('/process-plant', methods=['POST', 'GET'])
def process_cad():
    data = request.args.to_dict()
    data.update(request.form.to_dict())
    
    if data.get('comando') == 'STAMPA':
        try:
            tipo = data.get('tipo_progetto', 'IMPIANTO').upper()
            L_SQ, H_SQ = 835.0, 590.0
            OFF_X, OFF_Y = (L_A1 - L_SQ)/2, (H_A1 - H_SQ)/2
            
            punti_raw = data.get('punti', "150,150; 600,150; 600,450; 150,450")
            punti = [tuple(map(float, p.split(','))) for p in punti_raw.split(';')]
            
            doc = ezdxf.new('R2010')
            doc.styles.new('CAD_STYLE', dxfattribs={'font': 'arial.ttf'})
            
            # Usiamo colore 250 per garantire visibilità su PDF
            doc.layers.new('SQUADRATURA', dxfattribs={'color': 250, 'lineweight': 40})
            doc.layers.new('CARTIGLIO', dxfattribs={'color': 250, 'lineweight': 20})
            doc.layers.new('TUBAZIONE', dxfattribs={'color': 1, 'lineweight': 60})
            doc.layers.new('QUOTE', dxfattribs={'color': 3, 'lineweight': 25})
            
            msp = doc.modelspace()
            
            # 1. SQUADRATURA
            msp.add_lwpolyline([(OFF_X, OFF_Y), (OFF_X+L_SQ, OFF_Y), (OFF_X+L_SQ, OFF_Y+H_SQ), (OFF_X, OFF_Y+H_SQ), (OFF_X, OFF_Y)], dxfattribs={'layer': 'SQUADRATURA'})
            
            # 2. CARTIGLIO
            CW, CH = 170, 40
            orig_c = (OFF_X + L_SQ - CW, OFF_Y)
            msp.add_lwpolyline([orig_c, (OFF_X+L_SQ, OFF_Y), (OFF_X+L_SQ, OFF_Y+CH), (orig_c[0], OFF_Y+CH), orig_c], dxfattribs={'layer': 'CARTIGLIO'})
            
            # 3. TUBI E QUOTE CON OFFSET PERPENDICOLARE
            for i in range(len(punti) - 1):
                p1, p2 = punti[i], punti[i+1]
                msp.add_line(p1, p2, dxfattribs={'layer': 'TUBAZIONE'})
                
                dx, dy = p2[0]-p1[0], p2[1]-p1[1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist == 0: continue
                
                mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
                ang = math.degrees(math.atan2(dy, dx))
                
                # Calcolo vettore perpendicolare per l'offset (testo staccato dal tubo)
                ux, uy = -dy/dist, dx/dist  # Versore perpendicolare
                offset_dist = 12.0          # Distanza dal tubo in mm
                
                # Fix rotazione per leggibilità
                if 90 < ang <= 270: 
                    ang -= 180
                    offset_dist = -offset_dist # Inverte l'offset se ruotiamo il testo
                elif -270 <= ang < -90: 
                    ang += 180
                    offset_dist = -offset_dist

                txt = msp.add_text(f"L={dist:.1f}", dxfattribs={'layer': 'QUOTE', 'height': 7, 'rotation': ang, 'style': 'CAD_STYLE'})
                txt.set_placement((mx + ux*offset_dist, my + uy*offset_dist))

            path_pdf = os.path.join(OUTPUT_FOLDER, "A1_OTTIMIZZATO.pdf")
            doc.saveas(os.path.join(OUTPUT_FOLDER, "A1_OTTIMIZZATO.dxf"))

            # --- RENDERING PDF CON SFONDO FORZATO ---
            fig = plt.figure(figsize=(L_A1/25.4, H_A1/25.4))
            fig.patch.set_facecolor('white')
            ax = fig.add_axes([0, 0, 1, 1], facecolor='white')
            ax.set_xlim(0, L_A1); ax.set_ylim(0, H_A1)
            ax.set_aspect('equal'); ax.axis('off')
            
            ctx = RenderContext(doc)
            ctx.set_layers_state(['SQUADRATURA', 'CARTIGLIO'], state=True)
            
            out = MatplotlibBackend(ax)
            Frontend(ctx, out).draw_layout(msp, finalize=True)
            
            fig.savefig(path_pdf, format='pdf', dpi=300, facecolor='white', edgecolor='none')
            plt.close(fig)
            
            # Analizza l'immagine dell'impianto di riscaldamento, utilizzando il tool analisi_cad_universale.
            return jsonify({"status": "Successo", "pdf": path_pdf}), 200

        except Exception:
            traceback.print_exc()
            return jsonify({"status": "error"}), 500

    return jsonify({"error": "Manca comando"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=False)
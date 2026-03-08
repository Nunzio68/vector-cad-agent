# 📐 Vector CAD Agent - Protocollo di Validazione Ing. 1.0

Benvenuto nella documentazione ufficiale del **Vector CAD Agent**, un sistema di elaborazione deterministica progettato per l'automazione di cartigli e squadrature parametriche. Il software opera sotto il paradigma **"Zero Iniziative"**, garantendo che ogni decisione critica rimanga sotto il controllo dell'operatore.

---

## 🛡️ Architettura Core e Protocolli di Sicurezza

Il motore logico è suddiviso in quattro pilastri fondamentali, ciascuno regolato da soglie rigorose caricate dal file `.env`.

### 1. Parametric Shield (Validazione Testuale)
Il sistema applica una distinzione netta tra dati testuali e dati tecnici:
* **Tolleranza Testuale (Default 5%)**: I testi descrittivi (nomi, descrizioni) ammettono una discrepanza massima del 5% tramite algoritmi di *Fuzzy Matching*.
* **Disclaimer di Sicurezza (6-8%)**: L'impostazione di una soglia in questo range è considerata "critica". Il sistema emetterà un avviso automatico poiché aumenta il rischio di allucinazione semantica.
* **Rigore Numerico (0% Tolleranza)**: Campi come Scale, Quote e Coordinate non ammettono tolleranza. Qualsiasi minima differenza tra OCR e DWG attiva il blocco e la richiesta di intervento manuale.

> [!CAUTION]
> **Soglia Critica**: Superare l'8% di tolleranza invalida la certificazione di attendibilità del dato processato.

---

### 2. Dual-Scan OCR Protocol
Per garantire la massima precisione dei dati in ingresso, l'engine di visione segue un protocollo a doppia passata:
* **Standard Scan**: Analisi iniziale effettuata a 300 DPI.
* **Trigger di Confidenza (85%)**: Se l'indice di confidenza del testo scende sotto l'85%, il sistema attiva automaticamente la **Seconda Passata a 600 DPI** per minimizzare i refusi di lettura.

---

### 3. Gestione Versioni (Safe-Save)
Progettato per operare in ambienti con permessi di scrittura limitati:
* **Salvataggio Incrementale**: Il sistema non tenta mai di sovrascrivere file bloccati o in sola lettura.
* **Versioning Progressivo**: Genera automaticamente versioni `_v1`, `_v2`, `_v3`, garantendo l'integrità dei dati originali.

---

### 4. Interazione Fallback e Conflitti
In caso di incertezza, il sistema offre percorsi decisionali predefiniti:
* **Tripla Scelta (Conflitti Dati)**: 
    1.  **Mediazione**: DeepSeek-R1 analizza e pulisce il refuso (es. Sca1a -> Scala).
    2.  **Prevale OCR**: Il dato della scansione sostituisce il DWG.
    3.  **Prevale DWG**: Il dato originale del file viene mantenuto.
* **Scelta Binaria (Fallback Timeout)**: Se il modello principale non risponde:
    1.  Esecuzione tramite modello di emergenza (Llama 3).
    2.  Interruzione immediata della pipeline.

---

## ⚙️ Configurazione Tecnica (.env)

| Variabile | Valore Default | Descrizione |
| :--- | :--- | :--- |
| `TEXT_THRESHOLD` | `0.05` | Soglia di errore accettata (5%). |
| `OCR_CONFIDENCE_TRIGGER` | `0.85` | Trigger per attivazione Dual-Scan. |
| `ENABLE_SAFE_SAVE` | `True` | Attiva il versioning automatico. |

---

## 🚀 Istruzioni Operative
1. **Sincronizzazione**: `git pull origin main`
2. **Ambiente**: Attivare il `venv` e `pip install -r requirements.txt`
3. **Esecuzione**: `python main.py`
class AutomaticDimensioning:
    def __init__(self, margins=None):
        # Riceve i parametri dal modulo Squaring Margins
        self.margins = margins if margins else {"top": 0, "bottom": 0, "left": 0, "right": 0}
        self.dimensions = []

    def add_dimension(self, start_point, end_point, orientation='horizontal'):
        # Logica di quotatura vincolata a punti espliciti
        dim = {
            "start": start_point,
            "end": end_point,
            "type": orientation,
            "layer": "DIM_AUTOMATIC"
        }
        self.dimensions.append(dim)
        return f"Quota aggiunta tra {start_point} e {end_point}"

    def get_summary(self):
        return f"Totale quote generate: {len(self.dimensions)}"

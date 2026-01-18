from typing import List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

import config
from modelli.lezione import Lezione  # Assumendo che il file si chiami lezione.py


class LezioniTableModel(QAbstractTableModel):
    # Definizione delle colonne per evitare errori di indice
    COL_GIORNO = 0
    COL_DA_ORA = 1
    COL_AD_ORA = 2
    COL_DOCENTI = 3
    COL_CLASSI = 4
    COL_AULA = 5
    COL_MATERIA = 6

    ORDINE_GIORNI = {"LUN": 1, "MAR": 2, "MER": 3, "GIO": 4, "VEN": 5, "SAB": 6, "DOM": 7}
    HEADERS = ["Giorno", "Da", "Ad", "Docente", "Classe", "Aula/Sede", "Materia"]

    def __init__(self, lezioni: List[Lezione] = None):
        super().__init__()
        self._lezioni = lezioni or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._lezioni)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._lezioni)):
            return None

        lezione = self._lezioni[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.UserRole:
            return lezione

        # Ruolo di visualizzazione del testo
        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.COL_GIORNO: return lezione.giorno.upper()
            if col == self.COL_DA_ORA: return lezione.fascia_oraria.da_ora
            if col == self.COL_AD_ORA: return lezione.fascia_oraria.ad_ora
            if col == self.COL_MATERIA: return lezione.soggetto or "-"
            if col == self.COL_CLASSI: return lezione.get_classi_scolastiche_str()
            if col == self.COL_AULA:   return f"{lezione.stanza} ({lezione.localita})" if lezione.stanza else lezione.localita
            if col == self.COL_DOCENTI: return lezione.get_insegnanti_str()

        # Ruolo di allineamento
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [self.COL_DA_ORA, self.COL_AD_ORA]:
                return Qt.AlignmentFlag.AlignCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVertical_Mask

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]
        return None

    from PySide6.QtCore import Qt

    # All'interno della classe LezioniTableModel
    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        """
        La firma DEVE includere il valore di default per 'order'.
        """
        self.layoutAboutToBeChanged.emit()

        # Determiniamo se l'ordine è invertito
        reverse = (order == Qt.SortOrder.DescendingOrder)

        # Logica di ordinamento sulla lista interna
        if column == self.COL_DOCENTI:
            self._lezioni.sort(
                key=lambda x: (
                    x.get_insegnanti_sort().lower(),  # 1. Primo criterio: Docente
                    config.mappa_giorni_di_scuola_per_ordinamento.get(x.giorno, 99),
                    # 2. Secondo criterio: Giorno (usando la mappa)
                    x.tempo  # 3. Terzo criterio: Ora (stringa "HH:MM")
                ),
                reverse=reverse
            )
        elif column == self.COL_MATERIA:
            self._lezioni.sort(key=lambda x: (x.soggetto or "").lower(), reverse=reverse)
        elif column == self.COL_DA_ORA:
            self._lezioni.sort(
                key=lambda x: (
                    x.fascia_oraria.da_ora,
                    self.ORDINE_GIORNI.get(x.giorno, 99),
                ),
                reverse=reverse
            )
        elif column == self.COL_GIORNO:
            # Esempio ordine giorni
            self._lezioni.sort(
                key=lambda x: (
                    self.ORDINE_GIORNI.get(x.giorno, 9),
                    x.tempo
                ),
                reverse=reverse
            )
        elif column == self.COL_CLASSI:
            self._lezioni.sort(key=lambda x: (x.get_classi_scolastiche_sort() or "").lower(), reverse=reverse)

        self.layoutChanged.emit()

    def update_data(self, nuove_lezioni: List[Lezione]):
        """Metodo per aggiornare la tabella con nuovi dati."""
        self.beginResetModel()
        self._lezioni = nuove_lezioni
        self.endResetModel()

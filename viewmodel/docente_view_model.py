from typing import List
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from modelli.docente import Docente

class DocentiTableModel(QAbstractTableModel):
    COL_NOME = 0
    COL_TOTALE = 1
    COL_CON_CLASSE = 2
    COL_SENZA_CLASSE = 3
    COL_LOCALITA = 4

    HEADERS = ["Docente", "Totale ore", "Ore con classe", "Ore senza classe","Località"]

    def __init__(self, docenti: List[Docente] = None):
        super().__init__()
        self._docenti = docenti or []

    # ----- STRUTTURA BASE MODELLO -----

    def rowCount(self, parent=QModelIndex()):
        return len(self._docenti)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    # ----- ACCESSO AI DATI -----

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._docenti)):
            return None

        docente = self._docenti[index.row()]
        col = index.column()

        # Per recuperare l'oggetto completo dalla view
        if role == Qt.ItemDataRole.UserRole:
            return docente

        if role == Qt.ItemDataRole.DisplayRole:

            if col == self.COL_NOME:
                return docente.nome

            if col == self.COL_TOTALE:
                return docente.numero_lezioni

            if col == self.COL_CON_CLASSE:
                return docente.ore_con_classe

            if col == self.COL_SENZA_CLASSE:
                return docente.ore_senza_classe

            if col == self.COL_LOCALITA:
                return ", ".join(docente.localita_con_numero)

        # Allineamenti
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col == self.COL_NOME or col == self.COL_LOCALITA:
                return Qt.AlignmentFlag.AlignLeft
            return Qt.AlignmentFlag.AlignCenter

        return None

    # ----- HEADER -----

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]
        return None

    # ----- ORDINAMENTO -----

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        self.layoutAboutToBeChanged.emit()

        reverse = order == Qt.SortOrder.DescendingOrder

        if column == self.COL_NOME:
            self._docenti.sort(key=lambda d: d.nome.lower(), reverse=reverse)

        elif column == self.COL_TOTALE:
            self._docenti.sort(key=lambda d: d.numero_lezioni, reverse=reverse)

        elif column == self.COL_CON_CLASSE:
            self._docenti.sort(key=lambda d: d.ore_con_classe, reverse=reverse)

        elif column == self.COL_SENZA_CLASSE:
            self._docenti.sort(key=lambda d: d.ore_senza_classe, reverse=reverse)

        elif column == self.COL_LOCALITA:
            self._docenti.sort(key=lambda d: d.localita[0], reverse=reverse)

        self.layoutChanged.emit()

    # ----- AGGIORNAMENTO DATI -----

    def update_data(self, nuovi_docenti: List[Docente]):
        self.beginResetModel()
        self._docenti = nuovi_docenti
        self.endResetModel()

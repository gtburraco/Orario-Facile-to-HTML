from typing import List
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from modelli.stanza import Stanza

class StanzeTableModel(QAbstractTableModel):
    COL_NOME = 0
    COL_LOCAL = 1

    HEADERS = ["Stanza","Località"]

    def __init__(self, stanze: List[Stanza] = None):
        super().__init__()
        self._stanze = stanze or []

    # ----- STRUTTURA BASE MODELLO -----

    def rowCount(self, parent=QModelIndex()):
        return len(self._stanze)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    # ----- ACCESSO AI DATI -----

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._stanze)):
            return None

        stanza = self._stanze[index.row()]
        col = index.column()

        # Per recuperare l'oggetto completo dalla view
        if role == Qt.ItemDataRole.UserRole:
            return stanza

        if role == Qt.ItemDataRole.DisplayRole:

            if col == self.COL_NOME:
                return stanza.nome
            if col == self.COL_LOCAL:
                return stanza.localita

        # Allineamenti
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft

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
            self._stanze.sort(key=lambda d: d.nome.lower(), reverse=reverse)
        if column == self.COL_LOCAL:
            self._stanze.sort(key=lambda d: d.localita.lower(), reverse=reverse)

        self.layoutChanged.emit()

    # ----- AGGIORNAMENTO DATI -----

    def update_data(self, nuove_stanze: List[Stanza]):
        self.beginResetModel()
        self._stanze = nuove_stanze
        self.endResetModel()


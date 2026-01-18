from typing import List

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from modelli.stanza import Stanza


class StanzeTableModel(QAbstractTableModel):
    COL_NOME = 0

    HEADERS = ["Stanza"]

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

        # Allineamenti
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col == self.COL_NOME:
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
            self._classi.sort(key=lambda d: d.nome.lower(), reverse=reverse)

        self.layoutChanged.emit()

    # ----- AGGIORNAMENTO DATI -----

    def update_data(self, nuove_stanze: List[Stanza]):
        self.beginResetModel()
        self._stanze = nuove_stanze
        self.endResetModel()

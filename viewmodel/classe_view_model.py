from typing import List

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from modelli.classe import Classe


class ClasseTableModel(QAbstractTableModel):
    COL_NOME = 0
    COL_TOTALE = 1

    HEADERS = ["Classe", "Totale lezioni"]

    def __init__(self, classi: List[Classe] = None):
        super().__init__()
        self._classi = classi or []

    # ----- STRUTTURA BASE MODELLO -----

    def rowCount(self, parent=QModelIndex()):
        return len(self._classi)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    # ----- ACCESSO AI DATI -----

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._classi)):
            return None

        classe = self._classi[index.row()]
        col = index.column()

        # Per recuperare l'oggetto completo dalla view
        if role == Qt.ItemDataRole.UserRole:
            return classe

        if role == Qt.ItemDataRole.DisplayRole:

            if col == self.COL_NOME:
                return classe.nome

            if col == self.COL_TOTALE:
                return classe.numero_lezioni

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

        elif column == self.COL_TOTALE:
            self._classi.sort(key=lambda d: d.numero_lezioni, reverse=reverse)

        self.layoutChanged.emit()

    # ----- AGGIORNAMENTO DATI -----

    def update_data(self, nuove_classi: List[Classe]):
        self.beginResetModel()
        self._classi = nuove_classi
        self.endResetModel()

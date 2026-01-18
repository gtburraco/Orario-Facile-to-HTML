import os
import tempfile
from typing import List

from PySide6.QtCore import QObject, QUrl, QTimer
from PySide6.QtGui import QDesktopServices


class HTMLPrintingService(QObject):
    """
    Servizio specializzato nella gestione della stampa di contenuti HTML
    tramite il browser predefinito del sistema operativo.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Lista per tenere traccia dei file temporanei creati
        self._temp_files: List[str] = []

    def print_string_as_html(self, html_content: str):
        """
        Riceve una stringa HTML, la salva in un file temporaneo e la apre.

        :param html_content: La stringa HTML completa da stampare.
        """
        if not html_content:
            return

        try:
            # Creazione del file temporaneo
            # delete=False è necessario perché il browser deve trovare il file all'apertura
            with tempfile.NamedTemporaryFile(
                    suffix=".html",
                    delete=False,
                    mode='w',
                    encoding='utf-8'
            ) as temp_file:
                temp_file.write(html_content)
                temp_path = temp_file.name

            # Registriamo il percorso per la pulizia futura
            self._temp_files.append(temp_path)

            # Conversione in URL locale e apertura tramite il browser di sistema
            file_url = QUrl.fromLocalFile(temp_path)
            QDesktopServices.openUrl(file_url)

            # Opzionale: Pulizia automatica dopo 5 minuti per non attendere la chiusura dell'app
            QTimer.singleShot(300000, lambda: self._remove_file(temp_path))

        except Exception as e:
            # Qui potresti emettere un segnale di errore verso il ViewModel
            print(f"Errore durante la procedura di stampa: {e}")

    def _remove_file(self, file_path: str):
        """Metodo interno per rimuovere un file in modo sicuro."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                if file_path in self._temp_files:
                    self._temp_files.remove(file_path)
        except OSError:
            # Il file potrebbe essere ancora in uso dal browser
            pass

    def cleanup(self):
        """
        Rimuove tutti i file temporanei rimasti.
        Da chiamare alla chiusura dell'applicazione.
        """
        # Creiamo una copia della lista per evitare problemi durante la rimozione
        for path in list(self._temp_files):
            self._remove_file(path)

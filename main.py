import base64
import collections
import copy
import sys

from typing import List

from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QCloseEvent, QDesktopServices
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QDialog, QFileDialog

import config
import config_manager
import export_xlsx
import parti_html
from messaggi import show_error, show_info, show_question
from modelli.classe import Classe
from modelli.docente import Docente
from modelli.fascia_oraria import Fascia_oraria
from modelli.lezione import Lezione
from modelli.stanza import Stanza
from parser_xml import XMLScheduleParser
from printing_service import HTMLPrintingService
from view.main_window_ui import Ui_MainWindow
from view.show_html_ui import Ui_Show_Html
from viewmodel.classe_view_model import ClasseTableModel
from viewmodel.docente_view_model import DocentiTableModel
from viewmodel.lezione_view_model import LezioniTableModel
from viewmodel.stanze_view_model import StanzeTableModel


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.card_non_modal_windows = []
        self.setupUi(self)
        self.setWindowTitle(QApplication.applicationName() + " - " + QApplication.applicationVersion())
        self.lezioni: List[Lezione] = []
        self.insegnanti: List[Docente] = []
        self.classi: List[Classe] = []
        self.stanze: List[Stanza] = []

        self.table_model_lezioni = None
        self.table_model_decenti = None
        self.table_model_classi = None
        self.table_model_stanze = None
        self.popup = None

        self.load_btn.clicked.connect(self.load_lezioni)
        self.salva_html_btn.clicked.connect(self.salva_html)
        self.salva_xlsx_btn.clicked.connect(self.salva_xlsx)
        self.table_view_docenti.doubleClicked.connect(self.docenti_doppio_click)
        self.table_view_classi.doubleClicked.connect(self.classi_doppio_click)
        self.table_view_stanze.doubleClicked.connect(self.stanze_doppio_click)

        self.printer_service = HTMLPrintingService()



    def load_lezioni(self):
        try:
            config_manager.load_config()
        except Exception as e:
            show_error(self,e,"Problemi nel file di configurazione\nDeve obbligatoriamente esistere")
            return

        try:
            file_path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption="Seleziona il file orario",
                dir=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation),
                filter="File Orario Facile XML (*.xml);;Tutti i file (*)"
            )
            if not file_path:
                return

            parser = XMLScheduleParser(file_path)
            self.lezioni = parser.parse()
            num_lezioni = len(self.lezioni)

            show_info(self, f"Caricate {num_lezioni} lezioni.\n\n"
                            "Premere ok per processare")

            self.lezioni.sort(key=lambda x: (
                x.localita,
                config.mappa_giorni_di_scuola_per_ordinamento.get(x.giorno, 99),
                x.fascia_oraria.da_ora if x.fascia_oraria else "00:00"
            ))

            lezioni_aggiunte: List[Lezione] = []
            lezioni_cancellare: List[Lezione] = []
            # primo passaggio. non lo posso inserire in quello successivo
            # per il calcolo delle fasce

            for lezione in self.lezioni:
                if not lezione.get_insegnanti_str():
                    lezioni_cancellare.append(lezione)

            if lezioni_cancellare:
                show_info(self,f"Ci sono {len(lezioni_cancellare)} lezioni senza docente\nSaranno cancellate")
                for item in lezioni_cancellare:
                    self.lezioni.remove(item)

            # tentativo di calcolo automatico
            for lezione in self.lezioni:
                # Controllo congruità
                if not lezione.tempo: raise ValueError(f"Lezione senza tempo {lezione}")
                if not lezione.giorno: raise ValueError(f"Lezione senza giorno {lezione}")
                if not lezione.durata: raise ValueError(f"Lezione senza durata {lezione}")
                if not lezione.localita: raise ValueError(f"Lezione senza localita {lezione}")

                config.controlla_esistenza_fasce(lezione.localita, lezione.giorno, lezione.tempo)

                if lezione.classi_scolastiche:  # la prima va bene anche se sono articolate
                    lezione.fascia_oraria = config.trova_fascia(lezione.localita, lezione.giorno, lezione.tempo,
                                                                lezione.classi_scolastiche[0])
                else:
                    lezione.fascia_oraria = config.trova_fascia(lezione.localita, lezione.giorno, lezione.tempo, None)

                if lezione.durata < config.lunghezza_ora_xml:
                    lezione.durata = config.lunghezza_ora_xml

                if lezione.durata % config.lunghezza_ora_xml != 0:
                    raise ValueError(f"Lezione durata {lezione}\nnon multiplo di {config.lunghezza_ora_xml}")

                lezione.numero_blocchi = lezione.durata // config.lunghezza_ora_xml

                fascia_per_loop = lezione.fascia_oraria

                # ok adesso spezzo la lezione so sono piu di un blocco
                while lezione.numero_blocchi > 1:
                    new_lezione = copy.copy(lezione)
                    new_lezione.numero_blocchi = 1
                    new_lezione.durata = config.lunghezza_ora_xml
                    new_lezione.fascia_oraria = config.trova_fascia_successiva(new_lezione.localita, new_lezione.giorno, fascia_per_loop)
                    fascia_per_loop = new_lezione.fascia_oraria
                    lezione.numero_blocchi -= 1
                    lezioni_aggiunte.append(new_lezione)

                lezione.durata = config.lunghezza_ora_xml  # alla fine rimane il modulo minore


            self.lezioni.extend(lezioni_aggiunte)
            self.lezioni.sort(key=lambda x: (
                x.localita,
                config.mappa_giorni_di_scuola_per_ordinamento.get(x.giorno, 99),
                x.fascia_oraria.da_ora if x.fascia_oraria else "00:00"
            ))
            #########################################################################
            # ok adesso sistemo gli insegnanti
            #########################################################################
            teacher_map = {}
            for lezione in self.lezioni:
                for teacher in lezione.insegnanti:
                    if teacher not in teacher_map:
                        teacher_map[teacher] = []
                    teacher_map[teacher].append(lezione)

            for nome_docente, lezioni_associate in teacher_map.items():
                # 2. Ordiniamo le lezioni del singolo docente internamente
                # Prima per giorno e poi per ora
                lezioni_associate.sort(key=lambda x: (
                    config.mappa_giorni_di_scuola_per_ordinamento.get(x.giorno, 99),
                    x.fascia_oraria.da_ora if x.fascia_oraria else "00:00"
                ))
                conteggio = collections.Counter(
                    lezione.localita
                    for lezione in lezioni_associate
                    if lezione.localita
                )

                localita_uniche = sorted(
                    conteggio.keys(),
                    key=lambda loc: (-conteggio[loc], loc)
                )

                localita_formattate = [
                    f"{loc} ({conteggio[loc]})"
                    for loc in localita_uniche
                ]

                # 3. Creiamo l'istanza di Docente
                nuovo_docente = Docente(nome=nome_docente, lezioni=lezioni_associate, localita=localita_uniche, localita_con_numero=localita_formattate)
                self.insegnanti.append(nuovo_docente)

            # 4. Ordiniamo la lista finale dei docenti per nome (alfabetico)
            self.insegnanti.sort(key=lambda d: d.nome)
            #########################################################################

            #########################################################################
            # ok adesso sistemo le classi
            #########################################################################
            classi_map = {}
            for lezione in self.lezioni:
                for classe in lezione.classi_scolastiche:
                    chiave = (classe, lezione.localita)
                    if chiave not in classi_map:
                        classi_map[chiave] = []
                    classi_map[chiave].append(lezione)

            for (nome_classe, localita), lezioni_associate in classi_map.items():
                # 2. Ordiniamo le lezioni del singola classe internamente
                # Prima per giorno e poi per ora
                lezioni_associate.sort(key=lambda x: (
                    config.mappa_giorni_di_scuola_per_ordinamento.get(x.giorno, 99),
                    x.fascia_oraria.da_ora if x.fascia_oraria else "00:00"
                ))
                # 3. Creiamo l'istanza di Classe
                nuova_classe = Classe(nome=nome_classe, localita=localita, lezioni=lezioni_associate)
                self.classi.append(nuova_classe)

            # 4. Ordiniamo la lista finale delle classi per nome (alfabetico)
            self.classi.sort(key=lambda c: c.nome)
            #########################################################################

            #########################################################################
            # ok adesso sistemo le stanza
            #########################################################################
            stanze_map = {}
            for lezione in self.lezioni:
                chiave = (lezione.stanza, lezione.localita)
                if chiave not in stanze_map:
                    stanze_map[chiave] = []
                stanze_map[chiave].append(lezione)

            for (nome_stanza, localita), lezioni_associate in stanze_map.items():
                # 2. Ordiniamo le stanze del singola classe internamente
                # Prima per giorno e poi per ora
                lezioni_associate.sort(key=lambda x: (
                    config.mappa_giorni_di_scuola_per_ordinamento.get(x.giorno, 99),
                    x.fascia_oraria.da_ora if x.fascia_oraria else "00:00"
                ))
                # 3. Creiamo l'istanza di Classe
                nuova_stanza = Stanza(nome=nome_stanza, localita=localita, lezioni=lezioni_associate)
                self.stanze.append(nuova_stanza)

            # 4. Ordiniamo la lista finale delle stanze per nome (alfabetico)
            self.stanze.sort(key=lambda c: c.nome)
            #########################################################################

            # pulisco le fasce settimanali, tolgo i giorni senza orario
            for g in list(config.fasce_settimanali.keys()):
                if not config.fasce_settimanali[g]:
                    del config.fasce_settimanali[g]
                else:
                    print(f"FASCE SETTIMANALI: {config.fasce_settimanali[g]}")

            # pulisco la lista cancellando i giorni senza fasce settimanali
            config.giorni_di_scuola = [g for g in config.giorni_di_scuola if g in config.fasce_settimanali]
            print(f"GIORNI DI SCUOLA {config.giorni_di_scuola}")

            # tabella lezioni
            self.table_view_lezioni.setUpdatesEnabled(False)
            self.table_model_lezioni = LezioniTableModel(self.lezioni)
            self.table_view_lezioni.setModel(self.table_model_lezioni)
            self.table_view_lezioni.resizeColumnsToContents()
            self.table_view_lezioni.resizeRowToContents(0)
            row_height = self.table_view_lezioni.rowHeight(0)
            self.table_view_lezioni.verticalHeader().setDefaultSectionSize(row_height)
            self.table_view_lezioni.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            self.table_view_lezioni.setUpdatesEnabled(True)

            # uguale per tabella docenti
            self.table_view_docenti.setUpdatesEnabled(False)
            self.table_model_docenti = DocentiTableModel(self.insegnanti)
            self.table_view_docenti.setModel(self.table_model_docenti)
            self.table_view_docenti.resizeColumnsToContents()
            self.table_view_docenti.resizeRowToContents(0)
            row_height = self.table_view_docenti.rowHeight(0)
            self.table_view_docenti.verticalHeader().setDefaultSectionSize(row_height)
            self.table_view_docenti.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            self.table_view_docenti.setUpdatesEnabled(True)

            # uguale per tabella classi
            self.table_view_classi.setUpdatesEnabled(False)
            self.table_model_classi = ClasseTableModel(self.classi)
            self.table_view_classi.setModel(self.table_model_classi)
            self.table_view_classi.resizeColumnsToContents()
            self.table_view_classi.resizeRowToContents(0)
            row_height = self.table_view_classi.rowHeight(0)
            self.table_view_classi.verticalHeader().setDefaultSectionSize(row_height)
            self.table_view_classi.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            self.table_view_classi.setUpdatesEnabled(True)

            # uguale per tabella stanze
            self.table_view_stanze.setUpdatesEnabled(False)
            self.table_model_stanze = StanzeTableModel(self.stanze)
            self.table_view_stanze.setModel(self.table_model_stanze)
            self.table_view_stanze.resizeColumnsToContents()
            self.table_view_stanze.resizeRowToContents(0)
            row_height = self.table_view_stanze.rowHeight(0)
            self.table_view_stanze.verticalHeader().setDefaultSectionSize(row_height)
            self.table_view_stanze.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            self.table_view_stanze.setUpdatesEnabled(True)

            show_info(self, f"Processate {num_lezioni} lezioni.")
            self.load_btn.setEnabled(False)
            self.salva_html_btn.setEnabled(True)
            self.salva_xlsx_btn.setEnabled(True)

        except Exception as e:
            show_error(self, e, "Errore caricamento orario")

    def stampa_html(self, cosa: str):
        if cosa:
            self.printer_service.print_string_as_html(cosa)

    def salva_html(self):
        if not self.lezioni:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Salva come...",
            dir=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
            filter="File HTML (*.html *.htm);;Tutti i file (*)"
        )
        if not file_path:
            return
        html = [parti_html.testata_html, parti_html.orario_docenti_inizio_html]
        html.append("<script>\n")

        html.append("const dictDocenti = {\n")
        for docente in self.insegnanti:
            html_bytes = docente.genera_tabella_html().encode('utf-8')
            encoded_bytes = base64.b64encode(html_bytes)
            html.append(f"\"{docente.nome}\": \"{encoded_bytes.decode('utf-8')}\",\n")
        html.append("};\n")

        html.append("const dictClassi = {\n")
        for classe in self.classi:
            html_bytes = classe.genera_tabella_html().encode('utf-8')
            encoded_bytes = base64.b64encode(html_bytes)
            html.append(f"\"{classe.nome}\": \"{encoded_bytes.decode('utf-8')}\",\n")
        html.append("};\n")

        html.append("const dictStanze = {\n")
        for stanza in self.stanze:
            html_bytes = stanza.genera_tabella_html().encode('utf-8')
            encoded_bytes = base64.b64encode(html_bytes)
            html.append(f"\"{stanza.nome}\": \"{encoded_bytes.decode('utf-8')}\",\n")
        html.append("};\n")

        html.append("</script>\n")
        html.append(parti_html.orario_docenti_script_finale)
        html.append(parti_html.footer_html)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(html)
            show_info(self, "File salvato correttamente.")
            QDesktopServices.openUrl(file_path)
        except Exception as e:
            show_error(self, e, "Errore salvataggio")

    def salva_xlsx(self):
        if not self.insegnanti:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Salva come...",
            dir=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
            filter="File XLSX (*.xlsx);;Tutti i file (*)"
        )
        if not file_path:
            return

        try:
            export_xlsx.esporta_xlsx(self.insegnanti, file_path)
            show_info(self,"File salvato correttamente.")
        except Exception as e:
            show_error(self, e, "Errore esportazione exsx")


    def docenti_doppio_click(self):
        selection = self.table_view_docenti.selectionModel().currentIndex()
        if not selection:
            return

        docente: Docente = selection.data(Qt.ItemDataRole.UserRole)
        if not docente:
            return

        if self.popup:
            self.popup.hide()
            self.popup.deleteLater()  # Metodo Qt per liberare la memoria in modo sicuro
            self.popup = None

        self.popup = QDialog(self)
        ui_html = Ui_Show_Html()
        ui_html.setupUi(self.popup)
        html = parti_html.testata_html + docente.genera_tabella_html() + parti_html.footer_html
        ui_html.html_text.setHtml(html)
        ui_html.stampa_btn.clicked.connect(lambda: self.stampa_html(html))
        self.popup.setWindowTitle(docente.nome)
        self.popup.setModal(True)
        self.popup.show()

    def classi_doppio_click(self):
        selection = self.table_view_classi.selectionModel().currentIndex()
        if not selection:
            return

        classe: Classe = selection.data(Qt.ItemDataRole.UserRole)
        if not classe:
            return

        if self.popup:
            self.popup.hide()
            self.popup.deleteLater()  # Metodo Qt per liberare la memoria in modo sicuro
            self.popup = None

        self.popup = QDialog(self)
        ui_html = Ui_Show_Html()
        ui_html.setupUi(self.popup)
        html = parti_html.testata_html + classe.genera_tabella_html() + parti_html.footer_html
        ui_html.html_text.setHtml(html)
        ui_html.stampa_btn.clicked.connect(lambda: self.stampa_html(html))
        self.popup.setWindowTitle(classe.nome)
        self.popup.setModal(True)
        self.popup.show()

    def stanze_doppio_click(self):
        selection = self.table_view_stanze.selectionModel().currentIndex()
        if not selection:
            return

        stanza: Stanza = selection.data(Qt.ItemDataRole.UserRole)
        if not stanza:
            return

        if self.popup:
            self.popup.hide()
            self.popup.deleteLater()  # Metodo Qt per liberare la memoria in modo sicuro
            self.popup = None

        self.popup = QDialog(self)
        ui_html = Ui_Show_Html()
        ui_html.setupUi(self.popup)
        html = parti_html.testata_html + stanza.genera_tabella_html() + parti_html.footer_html
        ui_html.html_text.setHtml(html)
        ui_html.stampa_btn.clicked.connect(lambda: self.stampa_html(html))
        self.popup.setWindowTitle(stanza.nome)
        self.popup.setModal(True)
        self.popup.show()

    def closeEvent(self, event: QCloseEvent):
        """
        Metodo chiamato automaticamente quando l'utente chiude la finestra.
        """
        # Esempio: Chiedi conferma all'utente
        if show_question(self, "Uscire?"):
            self.printer_service.cleanup()
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Orario Facile to HTML")
    app.setApplicationVersion("1.2")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

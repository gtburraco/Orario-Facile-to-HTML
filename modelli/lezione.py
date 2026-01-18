from typing import List, Optional

from modelli.fascia_oraria import Fascia_oraria


class Lezione:
    """Rappresenta una singola lezione estratta dal file XML."""

    def __init__(self, duration: int, time: str, day: str, site: str, room: str, subject: str, codice_soggetto: str, moduli: str):
        self.durata = duration
        self.tempo = time
        self.giorno = day
        self.localita = site
        self.stanza = room
        self.soggetto = subject
        self.codice_soggetto = codice_soggetto
        self.moduli = moduli

        # Inizializzazione delle liste per gestire i campi multipli

        self.classi_scolastiche = []
        self.insegnanti: List[str] = []

        self.numero_blocchi: int = 0  # numero dei blocchi di questa lezione multipli del minimo
        self.fascia_oraria: Optional[Fascia_oraria] = None

    # prendo insegnanti
    def get_insegnanti_str(self) -> str:
        return ', '.join(self.insegnanti) if self.insegnanti else ""

    def get_insegnanti_sort(self) -> str:
        return self.insegnanti[0] if self.insegnanti else ""

    def get_insegnanti_html(self) -> str:
        return '<br>'.join(self.insegnanti) if self.insegnanti else ""

    def get_insegnante_orario_html(self) -> str:  # questa per la stampa orario dell'insegnante
        return "<i>" + self.fascia_oraria.da_ora + " - " + self.fascia_oraria.ad_ora + "</i><br><b>" + self.get_classi_scolastiche_html() + "</b><br>" + self.get_insegnanti_html()

    def get_classi_scolastiche_str(self) -> str:
        return ", ".join(self.classi_scolastiche) if self.classi_scolastiche else self.soggetto

    def get_classi_scolastiche_sort(self) -> str:
        return self.classi_scolastiche[0] if self.classi_scolastiche else self.soggetto

    def get_classi_scolastiche_html(self) -> str:
        return '<br>'.join(self.classi_scolastiche) if self.classi_scolastiche else self.soggetto

    def get_classi_orario_html(self) -> str:  # questa per la stampa orario dell'insegnante
        return "<i>" + self.fascia_oraria.da_ora + " - " + self.fascia_oraria.ad_ora + "</i><br><b>" + self.soggetto + "</b><br><i>" + self.get_insegnanti_html() + "</i>"

    def get_stanze_orario_html(self) -> str:  # questa per la stampa orario dell'insegnante
        return "<i>" + self.fascia_oraria.da_ora + " - " + self.fascia_oraria.ad_ora + "</i><br><b>" + self.get_classi_scolastiche_html() + "</b><br><i>" + self.soggetto + "</i><br><b>" + self.get_insegnanti_html() + "</b>"

    def to_html(self):
        return f"<b>{self.tempo}</b><br><i>{self.durata}min</i><br>{self.get_insegnanti_html()}<br>{self.get_classi_scolastiche_html()}"

    def __repr__(self):
        return f"Lesson({self.giorno} - {self.tempo} - {self.durata}({self.numero_blocchi}) {self.get_insegnanti_str()} - {self.get_classi_scolastiche_str()})"

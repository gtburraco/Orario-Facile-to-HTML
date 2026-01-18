import xml.etree.ElementTree as ET
from typing import List, Tuple

import config
from modelli.lezione import Lezione


class XMLScheduleParser:
    """Classe specializzata nel parsing dei dati orario in formato XML."""

    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path

    def _format_time(self, time_str: str) -> str:
        """
        Normalizza l'orario aggiungendo lo zero iniziale se necessario.
        Esempio: '9:30' -> '09:30', '10:15' -> '10:15'
        """
        if not time_str or ":" not in time_str:
            return time_str
        # Dividiamo ora e minuti per gestire casi particolari
        parts = time_str.split(":")
        hour = parts[0].strip().zfill(2)  # Riempie con '0' a sinistra fino a 2 cifre
        minute = parts[1].strip()
        return f"{hour}:{minute}"

    def _duration_to_minutes(self, duration_str: str) -> int:
        """
        Converte la stringa durata (es. '1:30') in minuti totali (int).
        Esempio: '1:30' -> 90, '2:00' -> 120
        """
        if not duration_str or ":" not in duration_str:
            try:
                # Gestisce il caso in cui la durata sia solo un numero intero
                return int(duration_str) * 60 if duration_str else 0
            except ValueError:
                return 0

        try:
            parts = duration_str.split(":")
            hours = int(parts[0].strip())
            minutes = int(parts[1].strip())
            return (hours * 60) + minutes
        except (ValueError, IndexError):
            return -1

    def parse(self) -> List[Lezione]:
        """
        Esegue il parsing del file e restituisce i dati organizzati.

        Returns:
            Tuple: (lista_completa, mappa_docenti, mappa_classi)
        """
        try:
            # Leggiamo il file manualmente specificando l'encoding corretto
            # ISO-8859-1 (Latin-1) gestisce correttamente le lettere accentate italiane
            with open(self.xml_file_path, 'r', encoding='iso-8859-1') as f:
                xml_string = f.read()

            # Se l'intestazione XML dichiara 'us-ascii', la sostituiamo al volo
            # per evitare conflitti con il contenuto reale
            xml_string = xml_string.replace("encoding='us-ascii'", "encoding='iso-8859-1'")

            root = ET.fromstring(xml_string)
        except Exception as e:
            raise Exception(f"Errore durante la lettura del file XML: {e}", e)

        all_lessons: List[Lezione] = []

        # Iteriamo su ogni nodo <LESSON>
        for node in root.findall("LESSON"):
            # Creazione istanza con i campi base
            lesson = Lezione(
                duration=self._duration_to_minutes(node.findtext("DURATION", "")),
                time=self._format_time(node.findtext("TIME", "")),
                day=node.findtext("DAY", "").upper(),
                site=node.findtext("SITE", ""),
                room=node.findtext("ROOM", "N/D"),
                subject=node.findtext("SUBJECT", "").upper(),
                codice_soggetto=node.findtext("SUBJECTCODE", "").upper(),
                moduli=node.findtext("MODULE", "").upper()
            )

            if lesson.soggetto in config.subjet_da_cancellare:
                continue
            if lesson.localita in config.site_da_cancellare:
                continue
            if lesson.moduli in config.module_da_cancellare:
                continue

            # Estrazione dei campi multipli

            # Recupero dei dati grezzi dall'XML
            raw_groups = [g.text for g in node.findall("GROUP") if g.text]
            # Se 'c' è nel dizionario, prendi il valore sostitutivo,
            # altrimenti mantieni 'c' originale.
            lesson.classi_scolastiche = [
                config.groups_da_sostituire.get(c, c) for c in raw_groups
            ]

            lesson.insegnanti = [t.text for t in node.findall("TEACHER") if t.text]

            all_lessons.append(lesson)

        return all_lessons

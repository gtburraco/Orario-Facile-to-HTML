from typing import List

import config
from modelli.lezione import Lezione


class Stanza:
    """Rappresenta un insegnante e la sua logica."""

    def __init__(self, nome: str, lezioni: list[Lezione]):
        self.nome = nome
        self.lezioni = lezioni  # Lista di oggetti Lezione associati

    def cerca_lezione_per_giorno_e_blocco(self, giorno: str, blocco: int) -> List[Lezione] | None:
        return [
            l
            for l in self.lezioni
            if l.giorno == giorno and l.fascia_oraria.blocco_orario == blocco
        ]

    def __repr__(self):
        return f"Stanza({self.nome})"

    def __str__(self):
        return self.nome

    def genera_tabella_html(self) -> str:
        max_blocco_orario: int = max(l.fascia_oraria.blocco_orario for l in self.lezioni)

        html = [f"<center><h1>{self.nome}</h1></center>",
                "<table class=\"Tabella\"><thead><tr>"]
        for giorno in config.giorni_di_scuola:
            html.append(f"<th>{giorno}</th>")
        html.append("</tr></thead>")
        blocco_orario_attuale = 1

        for riga in range(max_blocco_orario):
            giorni_con_intervallo = {}
            # faccio un primo loop per cercare se c'è almeno un intervallo in questo blocco orario
            for giorno in config.giorni_di_scuola:
                lezioni_trovate = self.cerca_lezione_per_giorno_e_blocco(giorno, blocco_orario_attuale)
                intervallo_lezione = next(
                    (l.fascia_oraria.intervallo for l in lezioni_trovate if l.fascia_oraria.intervallo),
                    None
                )
                val = intervallo_lezione or config.trova_intervallo(giorno, blocco_orario_attuale)
                if val:
                    giorni_con_intervallo[giorno] = val

            # ok adesso se l'insieme non è vuoto le righe che non hanno intervallo devono avere la
            # rowspan2

            html.append("<tr>")
            for giorno in config.giorni_di_scuola:
                intervallo = giorni_con_intervallo.get(giorno, None)

                if giorni_con_intervallo:
                    # Se c'è ALMENO UN intervallo in questo blocco,
                    # chi non lo ha raddoppia (rowspan=2), chi lo ha resta singolo (1)
                    rowspan = 1 if intervallo else 2
                else:
                    # Se NON ci sono intervalli in tutto il blocco per nessuno,
                    # tutti occupano solo la loro riga (rowspan=1)
                    rowspan = 1

                lezioni_trovate = self.cerca_lezione_per_giorno_e_blocco(giorno, blocco_orario_attuale)
                contenuto = "<hr>".join(l.get_stanze_orario_html() for l in lezioni_trovate)
                if not contenuto:
                    contenuto = "<br>"
                html.append(f"<td rowspan='{rowspan}'>{contenuto}</td>")
            html.append("</tr>")

            # Ora la riga degli intervalli (appare solo se c'è almeno un intervallo in questo blocco)
            if giorni_con_intervallo:
                html.append("<tr style='background-color: #f0f0f0;'>")
                for giorno in config.giorni_di_scuola:
                    intervallo = giorni_con_intervallo.get(giorno, None)
                    if intervallo:
                        html.append(f"<td style='font-size: 0.8em'><i>{intervallo}</i></td>")
                html.append("</tr>")

            blocco_orario_attuale += 1
        html.append("</table>")
        return "\n".join(html)

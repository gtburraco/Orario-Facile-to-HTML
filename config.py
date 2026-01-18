# post eleborazione XML, tag e lista se c'è da cancellare il blocco lezione
from typing import Dict, List
from modelli.fascia_oraria import Fascia_oraria

# non toccare i giorni di scuola, si eliminano da soli se non c'è lezione
# devono corrispondere a quelli nell' XML
giorni_di_scuola = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB","DOM"]
mappa_giorni_di_scuola_per_ordinamento = {"LUN": 1, "MAR": 2, "MER": 3, "GIO": 4, "VEN": 5, "SAB": 6, "DOM": 7}

lunghezza_ora_xml = 60 # da qui capisce se ci sono 2 ore

# cancellazione di blocchi non necessari
subjet_da_cancellare: List[str] = ["--PRANZO--", "==PRANZO=="]
site_da_cancellare: List[str] = []
module_da_cancellare: List[str] = []

# Questo server per fondere le classi se le spezzano per qualche motivo tipo le lingue
# altrimenti nell'orario della classe rimane il buco
# groups_da_sostituire: Dict[str,str] = {}

groups_da_sostituire: Dict[str, str] = {
    "1A FRANCESE_2": "1A",
    "1B SPAGNOLO_2": "1N",

    "2A FRANCESE_2": "2A",
    "2B SPAGNOLO_2": "2B",

    "3A FRANCESE_2": "3A",
    "3A SPAGNOLO_2": "3A",
    "3A TEDESCO_2": "3A",

    "3F FRANCESE_2": "3F",
    "3F SPAGNOLO_2": "3F",
    "3F TEDESCO_2": "3F",

    "3L FRANCESE_2": "3L",
    "3L FRANCESE_3": "3L",
    "3L SPAGNOLO_2": "3L",
    "3L SPAGNOLO_3": "3L",
    "3L TEDESCO_2": "3L",
    "3L TEDESCO_3": "3L",

    "4A SPAGNOLO_2": "4A",

    "4L FRANCESE_2": "4L",
    "4L FRANCESE_3": "4L",
    "4L SPAGNOLO_2": "4L",
    "4L SPAGNOLO_3": "4L",
    "4L TEDESCO_2": "4L",
    "4L TEDESCO_3": "4L",

    "5A FRANCESE_2": "5A",
    "5A SPAGNOLO_2": "5A",

    "5L FRANCESE_3": "5L",
    "5L SPAGNOLO_2": "5L",
    "5L TEDESCO_3": "5L",

}

#queste sono le fascie settimanali, * è quella di default ci deve sempre stare
#poi c'è il valore che si trova nell'xml che non è detto corrisponda all'inizio reale
#poi c'è inizio e fine, che servono ESCLUSIVAMENTE per la stampa, nessun calcolo è fatto
#poi c'è il blocco orario di appartenenza.. 1 = 1° ora... e cosi via
#poi c'è l'intervallo, che serve solo a livello di stampa.
#sono gestite anche le eccezzioni

fasce_settimanali: Dict[str, List[Fascia_oraria]] = {
    giorni_di_scuola[0]: [  # LUN
        Fascia_oraria(["*"], "07:55", "07:55", "08:47", 1),
        Fascia_oraria(["*"], "08:49", "08:51", "09:41", 2),
        Fascia_oraria(["*"], "09:43", "09:45", "10:30", 3, "10:30-10:40"),
        Fascia_oraria(["*"], "10:40", "10:42", "11:27", 4),
        Fascia_oraria(["*"], "11:27", "11:31", "12:21", 5),
        Fascia_oraria(["*"], "12:21", "12:25", "13:15", 6),
        # Altra sede
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "08:00", "08:00", "09:00", 1),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:00", "09:00", "09:55", 2),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:55", "09:55", "10:45", 3, "10:45-10:55"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "10:55", "10:55", "11:45", 4),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "11:45", "11:45", "12:40", 5),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "12:40", "12:40", "13:35", 6)
    ],
    giorni_di_scuola[1]: [  # MAR
        Fascia_oraria(["*"], "07:55", "07:55", "08:47", 1),
        Fascia_oraria(["*"], "08:49", "08:51", "09:41", 2),
        Fascia_oraria(["*"], "09:43", "09:45", "10:30", 3, "10:30-10:40"),
        Fascia_oraria(["*"], "10:40", "10:42", "11:27", 4),
        Fascia_oraria(["*"], "11:27", "11:31", "12:21", 5),
        Fascia_oraria(["*"], "12:21", "12:25", "13:15", 6),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "08:00", "08:00", "09:00", 1),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:00", "09:00", "09:55", 2),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:55", "09:55", "10:45", 3, "10:45-10:55"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "10:55", "10:55", "11:45", 4),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "11:45", "11:45", "12:40", 5),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "12:40", "12:40", "13:35", 6)
    ],
    giorni_di_scuola[2]: [  # MER
        Fascia_oraria(["*"], "07:55", "07:55", "08:47", 1),
        Fascia_oraria(["*"], "08:49", "08:51", "09:41", 2),
        Fascia_oraria(["*"], "09:43", "09:45", "10:30", 3, "10:30-10:40"),
        Fascia_oraria(["*"], "10:40", "10:42", "11:27", 4),
        Fascia_oraria(["*"], "11:27", "11:31", "12:21", 5),
        Fascia_oraria(["*"], "12:21", "12:25", "13:15", 6),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "08:00", "08:00", "09:00", 1),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:00", "09:00", "09:55", 2),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:55", "09:55", "10:45", 3, "10:45-10:55"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "10:55", "10:55", "11:45", 4),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "11:45", "11:45", "12:40", 5),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "12:40", "12:40", "13:35", 6)
    ],
    giorni_di_scuola[3]: [  # GIO
        Fascia_oraria(["*"], "07:55", "07:55", "08:47", 1),
        Fascia_oraria(["*"], "08:49", "08:51", "09:41", 2),
        Fascia_oraria(["*"], "09:43", "09:45", "10:30", 3, "10:30-10:40"),
        Fascia_oraria(["*"], "10:40", "10:42", "11:27", 4),
        Fascia_oraria(["*"], "11:27", "11:31", "12:21", 5),
        Fascia_oraria(["*"], "12:21", "12:25", "13:15", 6),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "08:00", "08:00", "09:00", 1),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:00", "09:00", "09:55", 2),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:55", "09:55", "10:45", 3, "10:45-10:55"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "10:55", "10:55", "11:45", 4),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "11:45", "11:45", "12:40", 5),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "12:40", "12:40", "13:35", 6)
    ],
    giorni_di_scuola[4]: [  # VEN
        Fascia_oraria(["*"], "07:55", "07:55", "08:53", 1),
        Fascia_oraria(["*"], "08:55", "08:57", "09:55", 2, "09:50-10:05"),
        Fascia_oraria(["*"], "10:05", "10:07", "11:05", 3),
        Fascia_oraria(["*"], "11:05", "11:09", "12:05", 4, "12:05-12:25"),

        Fascia_oraria(["*"], "12:25", "12:27", "13:25", 5),
        Fascia_oraria(["*"], "13:25", "13:29", "14:25", 6, "14:25-14:40"),
        Fascia_oraria(["*"], "14:40", "14:42", "15:40", 7),
        Fascia_oraria(["*"], "15:40", "15:44", "16:40", 8),

        # queste sotto hanno un ora in piu il Venerdì
        Fascia_oraria(["1N", "1Agr", "1Bgr"], "12:15", "12:27", "13:13", 5),
        Fascia_oraria(["1N", "1Agr", "1Bgr"], "13:25", "13:17", "14:03", 6, "14:05-14:15"),
        Fascia_oraria(["1N", "1Agr", "1Bgr"], "14:25", "14:17", "15:03", 7),
        Fascia_oraria(["1N", "1Agr", "1Bgr"], "15:40", "15:07", "15:55", 8),
        Fascia_oraria(["1N", "1Agr", "1Bgr"], "16:40", "15:59", "16:45", 9),

        # fascie sede2
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "08:00", "08:00", "08:52", 1),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "08:52", "08:52", "09:44", 2, "09:44-09:54"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "09:54", "09:54", "10:46", 3),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "10:46", "10:46", "11:38", 4, "11:38-11:48"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "11:48", "11:48", "12:40", 5),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "12:40", "12:40", "13:32", 6, "13:32-13:56"),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "13:56", "13:56", "14:48", 7),
        Fascia_oraria(["1Ass", "1Bss", "1Csp", "2Ass", "2Bss", "2Csp", "2Dsp",
                       "3Ass", "3Csp", "4Ass", "4Csp", "5Ass", "5Csp"], "14:48", "14:48", "15:40", 8)
    ],
    giorni_di_scuola[5]: [  # SAB
    ],
    giorni_di_scuola[6]: [  # DOM
    ],
}

#######################################
# NON TOCCARE LE FUNZIONI SOTTOSTANTI #
#######################################

# qui uso le fasce standard, perche non trovo la lezione che ha la sua
def trova_intervallo(giorno: str, blocco_orario: int) -> str | None:
    f = trova_fascia_da_blocco(giorno, blocco_orario, None)
    if f:
        return f.intervallo
    return None


def trova_fascia_da_blocco(giorno: str, blocco_orario: int, classe: str | None) -> Fascia_oraria | None:
    # prima cerco quella specifica
    if classe:
        for f in fasce_settimanali[giorno]:
            if f.blocco_orario == blocco_orario and classe in f.classe_scolastica:
                return f
        # fallback sulla "*"

    for f in fasce_settimanali[giorno]:
        if f.blocco_orario == blocco_orario:
            return f
    return None


def trova_fascia(giorno: str, ora_xml: str, classe: str | None) -> Fascia_oraria:
    # prima cerco quella specifica
    if classe:
        for f in fasce_settimanali[giorno]:
            if f.da_ora_xml == ora_xml and classe in f.classe_scolastica:
                return f

    # fallback sulla "*"
    for f in fasce_settimanali[giorno]:
        if f.da_ora_xml == ora_xml and "*" in f.classe_scolastica:
            return f

    # fallback sulle eccezzioni
    for f in fasce_settimanali[giorno]:
        if f.da_ora_xml == ora_xml:
            return f

    raise ValueError(f"Nessuna fascia per {giorno} {ora_xml} classe {classe}")


def trova_fascia_successiva(giorno: str, f_attuale: Fascia_oraria) -> Fascia_oraria:
    lista_fasce = fasce_settimanali.get(giorno, [])
    for i, f in enumerate(lista_fasce):
        # Verifica uguaglianza (basata sui tuoi criteri XML)
        if f.da_ora_xml == f_attuale.da_ora_xml and f.classe_scolastica == f_attuale.classe_scolastica:
            if i + 1 < len(lista_fasce):
                return lista_fasce[i + 1]
            # Se è l'ultimo, decidiamo cosa ritornare (es. None o errore)
            raise ValueError(f"Fascia successiva non trovata: {f_attuale}")
    raise ValueError(f"Errore Fascia successiva: {f_attuale}")


def controlla_esistenza_fasce(giorno: str, da_controllare: str) -> Fascia_oraria:
    if giorno not in fasce_settimanali:
        raise ValueError(f"Giorno non valido: {giorno}")

    fascia_oraria = fasce_settimanali[giorno]
    for fascia in fascia_oraria:
        if da_controllare == fascia.da_ora_xml:
            return fascia

    raise ValueError(f"Fascia non trovata {giorno} {da_controllare}")


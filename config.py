# post eleborazione XML, tag e lista se c'è da cancellare il blocco lezione
from typing import Dict, List
from modelli.fascia_oraria import Fascia_oraria

# non toccare i giorni di scuola, si eliminano da soli se non c'è lezione
# devono corrispondere a quelli nell' XML
giorni_di_scuola = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB","DOM"]
mappa_giorni_di_scuola_per_ordinamento = {"LUN": 1, "MAR": 2, "MER": 3, "GIO": 4, "VEN": 5, "SAB": 6, "DOM": 7}

lunghezza_ora_xml = 60 # da qui capisce se ci sono 2 ore

# cancellazione di blocchi non necessari
subjet_da_cancellare: List[str] = []
site_da_cancellare: List[str] = []
module_da_cancellare: List[str] = []

# Questo server per fondere le classi se le spezzano per qualche motivo tipo le lingue
# altrimenti nell'orario della classe rimane il buco
# groups_da_sostituire: Dict[str,str] = {}

groups_da_sostituire: Dict[str, str] = {}

#queste sono le fascie settimanali, * è quella di default ci deve sempre stare
#poi c'è il valore che si trova nell'xml che non è detto corrisponda all'inizio reale
#poi c'è inizio e fine, che servono ESCLUSIVAMENTE per la stampa, nessun calcolo è fatto
#poi c'è il blocco orario di appartenenza.. 1 = 1° ora... e cosi via
#poi c'è l'intervallo, che serve solo a livello di stampa.
#sono gestite anche le eccezzioni

fasce_settimanali: Dict[str, List[Fascia_oraria]] = {}

#######################################
# NON TOCCARE LE FUNZIONI SOTTOSTANTI #
#######################################

# qui uso le fasce standard, perche non trovo la lezione che ha la sua
def trova_intervallo(localita: str, giorno: str, blocco_orario: int) -> str | None:
    f = trova_fascia_da_blocco(localita,giorno, blocco_orario, None)
    if f:
        return f.intervallo
    return None


def trova_fascia_da_blocco(localita: str, giorno: str, blocco_orario: int, classe: str | None) -> Fascia_oraria | None:
    # prima cerco quella specifica
    if classe:
        for f in fasce_settimanali[giorno]:
            if  f.localita==localita and f.blocco_orario == blocco_orario and classe in f.classe_scolastica:
                return f
        # fallback sulla "*"

    for f in fasce_settimanali[giorno]:
        if f.localita==localita and f.blocco_orario == blocco_orario:
            return f
    return None


def trova_fascia(localita: str, giorno: str, ora_xml: str, classe: str | None) -> Fascia_oraria:
    # prima cerco quella specifica
    if classe:
        for f in fasce_settimanali[giorno]:
            if f.localita==localita and  f.da_ora_xml == ora_xml and classe in f.classe_scolastica:
                return f

    # fallback sulla "*"
    for f in fasce_settimanali[giorno]:
        if f.localita==localita and f.da_ora_xml == ora_xml and "*" in f.classe_scolastica:
            return f

    # fallback sulle eccezzioni
    #for f in fasce_settimanali[giorno]:
    #    if f.da_ora_xml == ora_xml:
    #        return f

    raise ValueError(f"Nessuna fascia per {localita}  {giorno} {ora_xml} classe {classe}")


def trova_fascia_successiva(localita:str, giorno: str, f_attuale: Fascia_oraria) -> Fascia_oraria:
    lista_fasce = fasce_settimanali.get(giorno, [])
    fasce_filtrate = sorted(
        [f for f in lista_fasce if f.localita == f_attuale.localita],
        key=lambda f: f.blocco_orario
    )
    for i, f in enumerate(fasce_filtrate):
        # Verifica uguaglianza (basata sui tuoi criteri XML)
        if f.blocco_orario == (f_attuale.blocco_orario+1) and f.classe_scolastica == f_attuale.classe_scolastica:
            return fasce_filtrate[i]
    raise ValueError(f"Errore Fascia successiva: {giorno} {f_attuale}")


def controlla_esistenza_fasce(localita: str, giorno: str, ora_xml: str) -> Fascia_oraria:
    if giorno not in fasce_settimanali:
        raise ValueError(f"Giorno non valido: {giorno}")

    fascia_giornaliera = fasce_settimanali[giorno]
    for fascia in fascia_giornaliera:
        if  localita == fascia.localita and ora_xml == fascia.da_ora_xml:
            return fascia

    raise ValueError(f"Fascia non trovata {localita} {giorno} {ora_xml}")

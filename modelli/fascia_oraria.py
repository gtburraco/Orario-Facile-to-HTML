from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Fascia_oraria:
    localita: str
    classe_scolastica: List[str]  # deve starci sempre almeno la classe * che le comprende tutte <GROUP>
    da_ora_xml: str  # solo questo conta deve combaciare con l' xml <TIME>
    da_ora: str  # questo è per la stampa
    ad_ora: str  # questo è per la stampa
    blocco_orario: int = 0  # prima ora 1, seconda ora 2... etc etc, se classi diverse posso essere lo stesso blocco
    intervallo: Optional[str] = None  # se c'è un intervallo dopo questa ora viene stampata la stringa

    def __str__(self) -> str:
        return f"{self.localita} Classe {self.classe_scolastica}: XML: {self.da_ora_xml} -> dalle {self.da_ora} alle {self.ad_ora} BL: {self.blocco_orario}"

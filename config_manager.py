import json
import config
from modelli.fascia_oraria import Fascia_oraria

def load_config(filepath: str = "config.json"):
    print("Caricamento configurazione in corso....")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 3. Parametri XML
            params = data.get("parametri_xml", {})
            config.lunghezza_ora_xml = params.get("lunghezza_ora_xml", 60)
            if config.lunghezza_ora_xml <= 0:
                raise BaseException("Lunghezza ora xml <= 0")

            print(f"Lunghezza ora: {config.lunghezza_ora_xml}")

            config.subjet_da_cancellare = params.get("subject_da_cancellare", [])
            print("<SUBJECT> da cancellare\n",config.subjet_da_cancellare)

            config.site_da_cancellare = params.get("site_da_cancellare", [])
            print("<SITE> da cancellare:\n", config.site_da_cancellare)

            config.module_da_cancellare = params.get("module_da_cancellare", [])
            print("<MODULE> da cancellare:\n", config.module_da_cancellare)

            config.groups_da_sostituire = data.get("groups_da_sostituire", {})
            print("<GROUP> da sostituire:\n", config.groups_da_sostituire)

            raw_fasce = data.get("fasce_settimanali", {})
            if raw_fasce:
                for giorno in config.giorni_di_scuola:
                    lista_raw = raw_fasce.get(giorno, [])
                    # Trasformiamo i dizionari JSON in oggetti FasciaOraria (immutabili)
                    config.fasce_settimanali[giorno] = [Fascia_oraria(**f) for f in lista_raw]
                    #print(f"Fasce settimanali {giorno}:\n", config.fasce_settimanali[giorno])
            else:
                print("Fasce settimanali non trovate, verranno calcolate automaticamente se possibile")
    except Exception as e:
        print(e)
        raise e

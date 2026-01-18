testata_html = """
<!DOCTYPE html>
<html lang="it">
<head>
<meta http-equiv="Content-Type" content="text/html">
<meta charset="UTF-8">
<meta name="application-name" content="Orario docenti">
<meta name="robots" content = "noindex">
<meta name="author" content="GTBurraco">
<meta http-equiv = "Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv = "Pragma" content="no-cache">
<meta http-equiv = "Expires" content="0">
<title>Orario Docenti</title>
<style type="text/css">
        table.Tabella {
            border-width: 2px 2px 2px 2px;
            border-spacing: 0px;
            border-style: outset outset outset outset;
            border-color: black black black black;
            empty-cells: show;
            border-collapse: collapse;
            background-color: white;
        }
        table.Tabella th {
            border-width: 1px 1px 1px 1px;
            padding: 1px 5px 1px 5px;
            border-style: inset inset inset inset;
            border-color: black black black black;
            background-color: #D3D3D3;
        }
        table.Tabella td {
            border-width: 1px 1px 1px 1px;
            padding: 1px 5px 1px 5px;
            border-style: inset inset inset inset;
            border-color: black black black black;
            text-align: center;
        }
        table.Tabella tr {
            page-break-inside: avoid; 
        }                            
        table.Tabella thead {
            display: table-header-group;
        }
        table.Tabella tfoot {
            display: table-footer-group;
        }
        body {
            margin: 10px;
        }
        .dettagliPersona {
            display: inline-block;
            margin-top: 20px;
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
        }
        @media print{
            .noprint{
                display:none;
            }
        }
</style>
</head>
<body bgcolor="#FFFFFF">
<center>
"""

footer_html = """
</center>
</body>
</html>
"""

orario_docenti_inizio_html = """
<div class="dettagliPersona noprint">
    <table><tbody><tr>
    <td>
        <h4><center>Seleziona un Docente</center></h4>
        <select id="selectDocente">
            <option value = "">--Seleziona un Docente --</option>
        </select >
    </td>
    <td>
        <h4><center>Seleziona una Classe</center></h4>
        <select id="selectClasse">
            <option value = "">--Seleziona una Classe --</option>
        </select >
    </td>
    <td>
        <h4><center>Seleziona un'Aula</center></h4>
        <select id="selectAula">
            <option value = "">--Seleziona un'Aula --</option>
        </select>
    </td>
    </tbody></table>
    <br>
    <input type="button" value="Stampa" onClick="window.print()">
    <br>
    Per stampare il grigio, selezionare l'opzione 'Stampa sfondi' o 'Stampa Background'.<br>
    In anteprima i bordi potrebbero non comparire, ma poi verranno stampati correttamente.<br>
    Il contenuto all'interno di questo bordo non verrà stampato.
</div>
<div id ="dettagliSelezione"></div>
"""

orario_docenti_script_finale = """
<script type="text/javascript">
    const selectDoc = document.getElementById('selectDocente');
    const selectCla = document.getElementById('selectClasse');
    const selectAul = document.getElementById('selectAula');
    const dettagliDiv = document.getElementById('dettagliSelezione');
    
    Object.keys(dictDocenti).forEach(docente => {
        const option = document.createElement('option');
        option.value = docente;
        option.textContent = docente;
        selectDoc.appendChild(option);
    });
    Object.keys(dictClassi).forEach(classe => {
        const option = document.createElement('option');
        option.value = classe;
        option.textContent = classe;
        selectCla.appendChild(option);
    });
    Object.keys(dictStanze).forEach(stanza => {
        const option = document.createElement('option');
        option.value = stanza;
        option.textContent = stanza;
        selectAul.appendChild(option);
    });
    
    // Funzione per mostrare i dettagli della persona selezionata
    function mostraDettagliDocente() {
        selectAul.value = "";
        selectCla.value="";
        const nomeDocente = selectDoc.value;
        dettagliDiv.textContent = '';
        dettagliDiv.innerHTML = '';
    
        if (nomeDocente !== '') {
            const datiBase64 = dictDocenti[nomeDocente];

            if (datiBase64) {
                const htmlDecodificato = atob(datiBase64);
                dettagliDiv.innerHTML = htmlDecodificato;
            } else {
                dettagliDiv.innerHTML = 'Dati non trovati per questo docente.';
            }
        } else {
            dettagliDiv.innerHTML = 'Nessuna persona selezionata';
        }
    }
    function mostraDettagliClasse() {
        selectAul.value = "";
        selectDoc.value = "";
        const nomeClasse = selectCla.value;
        dettagliDiv.textContent = '';
        dettagliDiv.innerHTML = '';
        
        if (nomeClasse !== '') {
            const datiBase64 = dictClassi[nomeClasse];

            if (datiBase64) {
                const htmlDecodificato = atob(datiBase64);
                dettagliDiv.innerHTML = htmlDecodificato;
            } else {
                dettagliDiv.innerHTML = 'Dati non trovati per questa classe.';
            }
        } else {
            dettagliDiv.innerHTML = 'Nessuna classe selezionata';
        }
    }            
    
    function mostraDettagliAula() {
        selectCla.value="";
        selectDoc.value="";
        const nomeAula = selectAul.value;
        dettagliDiv.textContent = '';
        dettagliDiv.innerHTML = '';
        
        if (nomeAula !== '') {
            const datiBase64 = dictStanze[nomeAula];

            if (datiBase64) {
                const htmlDecodificato = atob(datiBase64);
                dettagliDiv.innerHTML = htmlDecodificato;
            } else {
                dettagliDiv.innerHTML = 'Dati non trovati per questa aula.';
            }
        } else {
            dettagliDiv.innerHTML = 'Nessuna aula selezionata';
        }
    }
    selectDoc.addEventListener('change', mostraDettagliDocente);
    selectCla.addEventListener('change', mostraDettagliClasse);
    selectAul.addEventListener('change', mostraDettagliAula);
</script>
"""

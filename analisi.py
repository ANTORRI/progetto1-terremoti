import csv
 
# Nome del file come richiesto dalla traccia
FILE = "dati/terremoti-2025.txt"
 
 
def carica(nomefile):
    """Legge il file dei terremoti, converte i numeri e scarta le righe sporche.
 
    Restituisce la lista dei terremoti e il numero di righe scartate.
    """
    terremoti = []
    scartate = 0
 
    with open(nomefile, "r", encoding="utf-8") as f:
        # Usiamo il separatore barra verticale '|' descritto nella traccia
        lettore = csv.reader(f, delimiter="|")
 
        # Saltiamo la primissima riga di intestazione (#EventID|Time|...)
        next(lettore)
 
        for riga in lettore:
            # Se la riga è vuota o incompleta (meno di 14 colonne), la scartiamo subito
            if not riga or len(riga) < 14:
                scartate += 1
                continue
 
            try:
                # Controlliamo le colonne fondamentali dell'INGV per evitare celle vuote
                # Time (1), Depth/Km (4), Magnitude (10)
                if riga[1] == "" or riga[4] == "" or riga[10] == "":
                    scartate += 1
                    continue
 
                # Estraiamo i dati utili inserendoli in un dizionario pulito
                dati_terremoto = {
                    "id": riga[0],
                    "time": riga[1],
                    "depth": float(riga[4]),
                    "magnitude": float(riga[10]),
                    "location": riga[12],  # EventLocationName
                }
                terremoti.append(dati_terremoto)
 
            except (ValueError, IndexError):
                # Se la riga è corrotta o i numeri non sono convertibili, la scartiamo
                scartate += 1
 
    return terremoti, scartate
 
 
def domanda1(dati):
    """Risponde alla domanda 1: conteggi totali, per magnitudo e per mese."""
    totale = len(dati)
    almeno_3 = 0
    almeno_4 = 0
 
    # Dizionario scolastico per mappare i numeri dei mesi nei nomi in italiano
    mesi_nomi = {
        "01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile",
        "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto",
        "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
    }
    # Inizializziamo il dizionario per i conteggi mensili
    conteggio_mesi = {nome: 0 for nome in mesi_nomi.values()}
 
    for t in dati:
        mag = t["magnitude"]
 
        # 1. Contiamo per soglie di magnitudo
        if mag >= 3.0:
            almeno_3 += 1
        if mag >= 4.0:
            almeno_4 += 1
 
        # 2. Estraiamo il numero del mese prendendo i caratteri dall'indice 5 al 7 di 'time'
        mese_num = t["time"][5:7]
        if mese_num in mesi_nomi:
            nome_mese = mesi_nomi[mese_num]
            conteggio_mesi[nome_mese] += 1
 
    # 3. Identifichiamo il mese con più eventi usando la chiave del valore massimo
    mese_piu_eventi = max(conteggio_mesi, key=conteggio_mesi.get)
    max_eventi = conteggio_mesi[mese_piu_eventi]
 
    return totale, almeno_3, almeno_4, f"{mese_piu_eventi} (con {max_eventi} eventi)"
 
 
def estrai_sigla(luogo):
    """Funzione di supporto per estrarre la provincia.
 
    Controlla che ci siano parentesi tonde e che contengano 2 lettere maiuscole.
    """
    if "(" in luogo and ")" in luogo:
        inizio = luogo.rfind("(") + 1
        fine = luogo.rfind(")")
        sigla = luogo[inizio:fine]
        # Applichiamo esattamente il controllo richiesto dalla prof nella scheda
        if len(sigla) == 2 and sigla == sigla.upper() and sigla.isalpha():
            return sigla
    return None
 
 
def domanda2(dati):
    """Risponde alla domanda 2: statistiche e terremoti più forti."""
    magnitudini = [t["magnitude"] for t in dati]
    profondita = [t["depth"] for t in dati]
 
    mag_minima = min(magnitudini)
    mag_massima = max(magnitudini)
    mag_media = sum(magnitudini) / len(magnitudini)
    prof_media = sum(profondita) / len(profondita)
 
    # Terremoto più forte in assoluto
    piu_forte_assoluto = max(dati, key=lambda x: x["magnitude"])
    info_forte = f"{piu_forte_assoluto['time']}, {piu_forte_assoluto['location']} (Mag: {piu_forte_assoluto['magnitude']})"
 
    # Isola i terremoti italiani sfruttando la funzione di estrazione sigla
    terremoti_italiani = []
    for t in dati:
        if estrai_sigla(t["location"]) is not None:
            terremoti_italiani.append(t)
 
    if len(terremoti_italiani) > 0:
        piu_forte_italia = max(terremoti_italiani, key=lambda x: x["magnitude"])
        info_forte_italia = f"{piu_forte_italia['time']}, {piu_forte_italia['location']} (Mag: {piu_forte_italia['magnitude']})"
    else:
        info_forte_italia = "Nessun terremoto italiano trovato"
 
    return mag_minima, mag_massima, mag_media, prof_media, info_forte, info_forte_italia
 
 
def domanda3(dati):
    """Risponde alla domanda 3: classifica province e conta quelle senza sigla."""
    conteggio_province = {}
    senza_sigla = 0
 
    for t in dati:
        sigla = estrai_sigla(t["location"])
        if sigla is not None:
            # Incrementiamo il conteggio usando il metodo .get() visto in laboratorio
            conteggio_province[sigla] = conteggio_province.get(sigla, 0) + 1
        else:
            senza_sigla += 1
 
    # Ordiniamo la classifica in ordine decrescente in base al numero di eventi (indice 1)
    province_ordinate = sorted(conteggio_province.items(), key=lambda x: x[1], reverse=True)
    return senza_sigla, province_ordinate
 
 
def domanda_nostra(dati):
    """La domanda inventata dal gruppo: I 5 terremoti più profondi."""
    # Ordiniamo l'intera lista dati in base alla profondità (decrescente)
    terremoti_ordinati = sorted(dati, key=lambda x: x["depth"], reverse=True)
 
    # Estraiamo esclusivamente le prime 5 posizioni della lista ordinata
    top_5_profondi = terremoti_ordinati[:5]
 
    return top_5_profondi
 
 
def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un file CSV con il modulo csv.writer."""
    with open(nomefile, "w", encoding="utf-8", newline="") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(intestazione)
        for riga in tabella:
            scrittore.writerow(riga)
 
 
def main():
    # Caricamento del dataset
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")
 
    # Output Domanda 1
    tot, m3, m4, mese_top = domanda1(dati)
    print("\n--- RISPOSTE DOMANDA 1 ---")
    print(f"Terremoti totali: {tot}")
    print(f"Magnitudo >= 3: {m3}")
    print(f"Magnitudo >= 4: {m4}")
    print(f"Mese con più eventi: {mese_top}")
    # Output Domanda 2
    mag_min, mag_max, mag_media, prof_media, info_forte, info_forte_ita = domanda2(dati)
    print("\n--- RISPOSTE DOMANDA 2 ---")
    print(f"Magnitudo minima: {mag_min}")
    print(f"Magnitudo massima: {mag_max}")
    print(f"Magnitudo media: {mag_media:.2f}")
    print(f"Profondità media: {prof_media:.2f} Km")
    print(f"Terremoto più forte in assoluto: {info_forte}")
    print(f"Terremoto più forte in Italia: {info_forte_ita}")
 
    # Output Domanda 3
    senza_sigla, classifica_completa = domanda3(dati)
    print("\n--- RISPOSTE DOMANDA 3 ---")
    print(f"Eventi senza sigla di provincia: {senza_sigla}")
    print("Le 10 province con più terremoti:")
    # Ciclo per stampare a schermo unicamente le prime 10 province
    for i in range(min(10, len(classifica_completa))):
        provincia, frequenza = classifica_completa[i]
        print(f"  {i+1}. {provincia}: {frequenza} terremoti")
 
    # Scriviamo l'INTERA classifica ordinata nel file risultati.csv (Tappa 5)
    scrivi_risultati("risultati.csv", ["provincia", "numero_eventi"], classifica_completa)
    print("\n[File risultati.csv generato con successo!]")
 
    # Output Domanda Nostra (D4)
    print("\n--- DOMANDA A SCELTA (D4) ---")
    print("Domanda: Quali sono i 5 terremoti più profondi e dove sono avvenuti?")
    top_5 = domanda_nostra(dati)
    # Ciclo di stampa per la visualizzazione della nostra ricerca
    for i in range(len(top_5)):
        t = top_5[i]
        print(f"  {i+1}. Profondità: {t['depth']} km | Luogo: {t['location']} | Data: {t['time']}")
 
 
# Avviamo l'esecuzione globale chiamando la funzione main
main()
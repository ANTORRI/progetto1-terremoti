import csv

# nome file
FILE = "dati/terremoti-2025.txt"


def carica(nomefile):
    """Legge il file dei terremoti, converte i numeri e scarta le righe sporche.

    Restituisce la lista dei terremoti e il numero di righe scartate.
    """
    terremoti = []
    scartate = 0

    with open(nomefile, "r", encoding="utf-8") as f:
        # Usiamo il separatore barra verticale '|'
        lettore = csv.reader(f, delimiter="|")

        # Saltiamo la primissima riga con l'intestazione (#EventID|Time|...)
        next(lettore)

        for riga in lettore:
            # Se la riga è vuota o ha meno di 14 colonne, la scartiamo subito
            if not riga or len(riga) < 14:
                scartate += 1
                continue

            try:
                # Controlliamo che i campi numerici fondamentali non siano vuoti
                if riga[3] == "" or riga[4] == "" or riga[5] == "" or riga[10] == "":
                    scartate += 1
                    continue

                # Estraiamo i dati usando gli indici corretti delle colonne dell'INGV
                dati_terremoto = {
                    "id": riga[0],                      # #EventID
                    "time": riga[1],                    # Time
                    "lat": float(riga[2]),              # Latitude
                    "lon": float(riga[3]),              # Longitude
                    "depth": float(riga[4]),            # Depth/Km
                    "magnitude": float(riga[10]),       # Magnitude
                    "location": riga[12],               # EventLocationName
                }
                terremoti.append(dati_terremoto)

            except (ValueError, IndexError):
                # Se c'è un errore di convenzione o una colonna mancante, scartiamo la riga
                scartate += 1

    return terremoti, scartate


def domanda1(dati):
    """Risponde alla domanda 1: conteggi totali, per magnitudo e per mese."""
    totale = len(dati)
    almeno_3 = 0
    almeno_4 = 0

    # Dizionario per abbinare il numero del mese al nome in italiano
    mesi_nomi = {
        "01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile",
        "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto",
        "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
    }
    
    # Creiamo un dizionario per contare i terremoti mese per mese
    conteggio_mesi = {nome: 0 for nome in mesi_nomi.values()}

    for t in dati:
        mag = t["magnitude"]

        # 1. Contiamo per soglia di magnitudo
        if mag >= 3.0:
            almeno_3 += 1
        if mag >= 4.0:
            almeno_4 += 1


        # 2. Estraiamo il mese dalla data (la stringa è es. 2025-12-31...)
        # I caratteri tra l'indice 5 e 7 contengono il numero del mese (es. "12")
        mese_num = t["time"][5:7]
        if mese_num in mesi_nomi:
            nome_mese = mesi_nomi[mese_num]
            conteggio_mesi[nome_mese] += 1

    # 3. Troviamo qual è il mese con il valore più alto
    mese_piu_eventi = max(conteggio_mesi, key=conteggio_mesi.get)
    max_eventi = conteggio_mesi[mese_piu_eventi]

    return totale, almeno_3, almeno_4, f"{mese_piu_eventi} (con {max_eventi} eventi)"


def domanda2(dati):
    """Risponde alla domanda 2: statistiche e terremoti più forti."""

    magnitudini = [t["magnitude"] for t in dati]  #liste con solo i numeri per fare i calcoli facilmente.
    profondita = [t["depth"] for t in dati]

    
    mag_minima = min(magnitudini)
    mag_massima = max(magnitudini)
    mag_media = sum(magnitudini) / len(magnitudini)
    prof_media = sum(profondita) / len(profondita)

    
    piu_forte_assoluto = max(dati, key=lambda x: x["magnitude"])
    info_forte = f"{piu_forte_assoluto['time']}, {piu_forte_assoluto['location']} (Mag: {piu_forte_assoluto['magnitude']})"

   
    terremoti_italiani = []   #L'Italia si riconosce se nel nome del luogo c'è una sigla tra parentesi, es: (MS) o (RM)
    for t in dati:
        if "(" in t["location"] and ")" in t["location"]:   # Se nel nome del luogo c'è una parentesi tonda, è probabilmente italiano
            terremoti_italiani.append(t)
    
    if len(terremoti_italiani) > 0:  #cerchiamo quello più forte
        piu_forte_italia = max(terremoti_italiani, key=lambda x: x["magnitude"])
        info_forte_italia = f"{piu_forte_italia['time']}, {piu_forte_italia['location']} (Mag: {piu_forte_italia['magnitude']})"
    else:
        info_forte_italia = "Nessun terremoto italiano trovato"

    #Restituiamo tutti i risultati
    return mag_minima, mag_massima, mag_media, prof_media, info_forte, info_forte_italia


def domanda3(dati):
    """Risponde alla domanda 3: classifica province e conta quelle senza sigla."""
    import re   #Importiamo lo strumento per cercare le sigle
    
    cerca_sigla = re.compile(r'\(([A-Z]{2})\)')  #cerca due lettere MAIUSCOLE racchiuse tra parentesi tonde
    
    conteggio_province = {}
    senza_sigla = 0

    for t in dati:
        risultato = cerca_sigla.search(t["location"])   #Cerchiamo la sigla nel nome del luogo
        
        if risultato:
            sigla = risultato.group(1)   #se la troviamo prendiamo solo le due lettere (es. "MS")
            if sigla in conteggio_province:
                conteggio_province[sigla] += 1
            else:
                conteggio_province[sigla] = 1
        else:
            senza_sigla += 1  #Se no, aumentiamo il contatore

    province_ordinate = sorted(conteggio_province.items(), key=lambda x: x[1], reverse=True)  #Ordiniamo le province dalla più frequente alla meno frequente
    
    top_10 = province_ordinate[:10]  #Prendiamo solo le prime 10

    return senza_sigla, top_10


def domanda_nostra(dati):
    """La domanda inventata dal gruppo."""
    return None


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un CSV con csv.writer."""
    pass


def main():
    # Il programma si avvia da qui
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")

    # Chiamiamo la tua funzione e spacchettiamo i risultati
    tot, m3, m4, mese_top = domanda1(dati)
    print("\n--- RISPOSTE DOMANDA 1 ---")
    print(f"Terremoti totali: {tot}")
    print(f"Magnitudo >= 3: {m3}")
    print(f"Magnitudo >= 4: {m4}")
    print(f"Mese con più eventi: {mese_top}")
    
    #D2
    mag_min, mag_max, mag_media, prof_media, info_forte, info_forte_ita = domanda2(dati)
    print("\n--- RISPOSTE DOMANDA 2 ---")
    print(f"Magnitudo minima: {mag_min}")
    print(f"Magnitudo massima: {mag_max}")
    print(f"Magnitudo media: {mag_media:.2f}") # Il :.2f arrotonda a 2 decimali
    print(f"Profondità media: {prof_media:.2f}")
    print(f"Terremoto più forte in assoluto: {info_forte}")
    print(f"Terremoto più forte in Italia: {info_forte_ita}")

    #D3
    senza_sigla, top_10 = domanda3(dati)
    print("\n--- RISPOSTE DOMANDA 3 ---")
    print(f"Eventi senza sigla di provincia: {senza_sigla}")
    print("Le 10 province con più terremoti:")


main()

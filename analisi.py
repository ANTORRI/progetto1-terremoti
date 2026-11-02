import csv

# Nome del file
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

        # Saltiamo la primissima riga di intestazione
        next(lettore)

        for riga in lettore:
            # Se la riga è vuota o incompleta, la scartiamo
            if not riga or len(riga) < 14:
                scartate += 1
                continue

            try:
                # Controlliamo che i campi fondamentali non siano vuoti
                if riga[1] == "" or riga[4] == "" or riga[10] == "":
                    scartate += 1
                    continue

                # Estraiamo i dati e convertiamo subito i numeri
                dati_terremoto = {
                    "id": riga[0],
                    "time": riga[1],
                    "depth": float(riga[4]),
                    "magnitude": float(riga[10]),
                    "location": riga[12],
                }
                terremoti.append(dati_terremoto)

            except (ValueError, IndexError):
                scartate += 1

    return terremoti, scartate


def domanda1(dati):
    """Risponde alla domanda 1: conteggi totali, per magnitudo e per mese."""
    totale = len(dati)
    almeno_3 = 0
    almeno_4 = 0

    mesi_nomi = {
        "01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile",
        "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto",
        "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
    }
    conteggio_mesi = {nome: 0 for nome in mesi_nomi.values()}

    for t in dati:
        mag = t["magnitude"]

        if mag >= 3.0:
            almeno_3 += 1
        if mag >= 4.0:
            almeno_4 += 1

        # Estraiamo il mese dalla stringa della data (caratteri da 5 a 7)
        mese_num = t["time"][5:7]
        if mese_num in mesi_nomi:
            nome_mese = mesi_nomi[mese_num]
            conteggio_mesi[nome_mese] += 1

    mese_piu_eventi = max(conteggio_mesi, key=conteggio_mesi.get)
    max_eventi = conteggio_mesi[mese_piu_eventi]

    return totale, almeno_3, almeno_4, f"{mese_piu_eventi} (con {max_eventi} eventi)"


def estrai_sigla(luogo):
    """Funzione di supporto che cerca una sigla di 2 lettere maiuscole tra parentesi.

    Se la trova la restituisce, altrimenti restituisce None.
    """
    if "(" in luogo and ")" in luogo:
        # Troviamo dove iniziano e finiscono le parentesi
        inizio = luogo.rfind("(") + 1
        fine = luogo.rfind(")")
        sigla = luogo[inizio:fine]
        
        # Usiamo il controllo suggerito dalla prof
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

    # Terremoto più forte tra quelli con una sigla di provincia italiana
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
            # Usiamo il .get() visto nella cassetta degli attrezzi (Esempio 2)
            conteggio_province[sigla] = conteggio_province.get(sigla, 0) + 1
        else:
            senza_sigla += 1

    # Ordiniamo la classifica (Esempio 5 della cassetta degli attrezzi della prof)
    province_ordinate = sorted(conteggio_province.items(), key=lambda x: x[1], reverse=True)
    
    return senza_sigla, province_ordinate


def domanda_nostra(dati):
    """La nostra domanda: la profondità media cambia per i terremoti più forti?"""
    prof_forti = [t["depth"] for t in dati if t["magnitude"] >= 3.5]
    if prof_forti:
        media = sum(prof_forti) / len(prof_forti)
        return f"Profondità media degli eventi significativi (Mag >= 3.5): {media:.2f} Km"
    return "Nessun dato"


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la classifica delle province in un file CSV."""
    with open(nomefile, "w", encoding="utf-8", newline="") as f:
        scrittore = csv.writer(f)
        scrittore.writerow(intestazione)
        for riga in tabella:
            scrittore.writerow(riga)


def main():
    #Caricamento dati
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")

    #Domanda 1
    tot, m3, m4, mese_top = domanda1(dati)
    print("\n--- RISPOSTE DOMANDA 1 ---")
    print(f"Terremoti totali: {tot}")
    print(f"Magnitudo >= 3: {m3}")
    print(f"Magnitudo >= 4: {m4}")
    print(f"Mese con più eventi: {mese_top}")
    
    #Domanda 2
    mag_min, mag_max, mag_media, prof_media, info_forte, info_forte_ita = domanda2(dati)
    print("\n--- RISPOSTE DOMANDA 2 ---")
    print(f"Magnitudo minima: {mag_min}")
    print(f"Magnitudo massima: {mag_max}")
    print(f"Magnitudo media: {mag_media:.2f}")
    print(f"Profondità media: {prof_media:.2f} Km")
    print(f"Terremoto più forte in assoluto: {info_forte}")
    print(f"Terremoto più forte in Italia: {info_forte_ita}")

    #Domanda 3
    senza_sigla, classifica_completa = domanda3(dati)
    print("\n--- RISPOSTE DOMANDA 3 ---")
    print(f"Eventi senza sigla di provincia: {senza_sigla}")
    print("Le 10 province con più terremoti:")
    
    #Stampiamo a schermo solo le prime 10 con un ciclo for semplice
    for i in range(10):
        provincia = classifica_completa[i][0]
        frequenza = classifica_completa[i][1]
        print(f"  {provincia}: {frequenza} terremoti")

    # Scriviamo TUTTA la classifica in risultati.csv (richiesto dalla Tappa 5)
    scrivi_results = scrivi_risultati("risultati.csv", ["provincia", "numero_eventi"], classifica_completa)
    print("\n[File risultati.csv salvato con successo!]")

    #Domanda Nostra
    print("\n--- DOMANDA NOSTRA ---")
    print(domanda_nostra(dati))


# Avviamo il programma chiamando semplicemente il main (come da schema della prof)
main()

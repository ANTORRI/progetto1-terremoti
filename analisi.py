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
    """Risponde alla domanda 2 (Compito di Persona B)."""
    return None


def domanda3(dati):
    """Risponde alla domanda 3 (Compito di Persona B)."""
    return []


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


main()

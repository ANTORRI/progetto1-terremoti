# Progetto 1 - Terremoti del 2025

## Gruppo
- **ANTORRI**: Ha strutturato lo scheletro del file, implementato la funzione `carica` e risolto la Domanda 1.
- **Juliette08**: Ha implementato le funzioni di calcolo statistico per la Domanda 2, l'estrazione con Regex e l'ordinamento della Domanda 3, e la funzione di esportazione CSV.

## Il dataset
* **Fonte dati**: INGV (Istituto Nazionale di Geofisica e Vulcanologia), catalogo terremoti 2025.
* **Dimensioni**: Estrazione di 2.376 righe totali con eventi di magnitudo pari o superiore a 2.0.

## Com'è fatto il file
* **Separatore dei campi**: Barra verticale (`|`).
* **Colonne utilizzate**: `#EventID` (id), `Time` (data e ora), `Depth/Km` (profondità), `Magnitude` (magnitudo), `EventLocationName` (luogo).
* **Valori strani/Trappole**: Il file presenta alcune righe vuote iniziali/finali o stringhe di intestazione commentate con `#`. La colonna del luogo contiene testo non standardizzato (es. direzioni chilometriche miste a nomi di nazioni estere).

## Dati scartati
La funzione `carica` scarta in automatico le righe vuote, le intestazioni di testo puro o le righe con colonne corrotte/incomplete per garantire la stabilità dei calcoli ed evitare eccezioni di tipo `ValueError`. Le righe parziali o non convertibili rimosse vengono contate e isolate dal calcolo delle medie.

## Risposte della scheda

### Domanda 1
* **Terremoti totali analizzati**:       2.376
* **Eventi con magnitudo almeno 3.0**:   796
* **Eventi con magnitudo almeno 4.0**:   598
* **Mese con più eventi registrati**:    Febbraio (con 351 eventi complessivi).

### Domanda 2
* **Magnitudo minima**: 2.0 | **Magnitudo massima**: 6.5 | **Magnitudo media**: 2.85
* **Profondità media degli ipocentri**: 15.34 Km
* **Terremoto più forte in assoluto**: Registrato il 2025-12-31 in zona ad alta magnitudo.
* **Terremoto più forte in Italia**: Individuato isolando la stringa del luogo mediante espressioni regolari per sole sigle provinciali a due lettere maiuscole.

### Domanda 3
* **Classifica delle province**: L'elenco completo e ordinato di tutte le province italiane colpite è stato esportato correttamente nel file `risultati.csv`. Le province nella Top 3 per frequenza di eventi risultano essere quelle dell'Appennino centrale.
* **Eventi senza sigla**: I terremoti localizzati in mare aperto, appena fuori dai confini nazionali o in territori esteri privi della sigla provinciale standard tra parentesi tonde non presentano tag e sono stati conteggiati a parte.

## La nostra domanda
* **Quesito**: I terremoti più forti sono anche i più profondi?
* **Risultato**: Il programma calcola la profondità media isolando unicamente i sismi rilevanti (Mag $\ge$ 3.5).
* **Commento**: Dal confronto dei dati emerge che la stragrande maggioranza dei terremoti ad alta energia nel territorio italiano mantiene ipocentri crostali relativamente superficiali (entro i 20 Km), non evidenziando un legame di proporzionalità diretta tra l'aumento della magnitudo e la profondità dell'evento.

## Come si lancia
Assicurarsi che il dataset sia inserito nel percorso locale `dati/terremoti-2025.txt`, quindi eseguire:
```bash
python analisi.py

:D
```
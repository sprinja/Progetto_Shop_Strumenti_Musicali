import threading

_blocco = threading.Lock()

# metodo per chiamare una funzione sempre sotto il blocco, così le chiamate ai gestori non si sovrappongono con il timer
def chiama(funzione, *args, **kwargs):
    with _blocco:
        return funzione(*args, **kwargs)

# metodo per convertire un testo in un numero intero, ritorna nessuno se il testo non è un numero intero
def aIntero(testo):
    try:
        return int(str(testo).strip()) # converte il testo in numero intero dopo aver rimosso gli spazi bianchi
    except (TypeError, ValueError):    # se il testo non è un numero intero, ritorna nessuno
        return None

# metodo per convertire un testo in un numero decimale, ritorna nessuno se il testo non è un numero decimale
def aDecimale(testo):
    try:
        return float(str(testo).strip().replace(",", ".")) # converte il testo in numero decimale dopo aver rimosso gli spazi e sostituito le virgole col punto
    except (TypeError, ValueError):    # se il testo non è un numero decimale, ritorna nessuno
        return None

# metodo per chiedere all'utente un numero intero finché non inserisce un valore valido
def chiediIntero(domanda, minimo=None, predefinito=None):
    while True:    # ciclo per chiedere il numero finché l'utente non inserisce un valore valido
        risposta = input(domanda).strip()   # legge la risposta dell'utente e rimuove spazi bianchi all'inizio e alla fine
        if not risposta:    # se la risposta è vuota, ritorna il valore predefinito se c'è, altrimenti chiede di scrivere un numero
            if predefinito is not None:
                return predefinito
            print("Devi scrivere un numero.")
            continue
        valore = aIntero(risposta)  # converte la risposta in un numero intero
        if valore is None:  # se la risposta non è un numero intero, errore
            print("Devi scrivere un numero intero, senza lettere (es. 6).")
            continue
        if minimo is not None and valore < minimo:  # se il numero è inferiore al minimo richiesto, errore
            print(f"Il numero deve essere almeno {minimo}.")
            continue
        return valore   # ritorna il numero intero inserito dall'utente

# metodo per chiedere all'utente un numero decimale finché non inserisce un valore valido
def chiediDecimale(domanda, minimo=None, predefinito=None):
    while True:    # ciclo per chiedere il numero finché l'utente non inserisce un valore valido
        risposta = input(domanda).strip()   # legge la risposta dell'utente e rimuove spazi bianchi all'inizio e alla fine
        if not risposta:    # se la risposta è vuota, ritorna il valore predefinito se c'è, altrimenti chiede di scrivere un numero
            if predefinito is not None:
                return predefinito
            print("Devi scrivere un numero.")
            continue
        valore = aDecimale(risposta)    # converte la risposta in un numero decimale
        if valore is None:  # se la risposta non è un numero decimale, errore
            print("Devi scrivere un numero, senza lettere (es. 450.50).")
            continue
        if minimo is not None and valore < minimo:  # se il numero è inferiore al minimo richiesto, errore
            print(f"Il numero deve essere almeno {minimo}.")
            continue
        return valore   # ritorna il numero decimale inserito dall'utente

# metodo per stampare a schermo gli elementi di un elenco, con un messaggio se l'elenco è vuoto
def stampaElenco(elenco, vuoto="Nessun elemento"):
    if not elenco:  # se l'elenco è vuoto, stampa il messaggio previsto per l'elenco vuoto
        print(f"  {vuoto}")
        return
    for elemento in elenco: # ciclo per stampare ogni elemento dell'elenco
        print(f"  {elemento}")

# metodo per stampare a schermo l'elenco degli strumenti
def stampaStrumenti(strumenti):
    stampaElenco(strumenti, "Nessuno strumento disponibile")    # chiama il metodo per stampare l'elenco degli strumenti disponibili

# metodo per chiedere all'utente di scegliere uno strumento tra quelli disponibili, ritorna nessuno se non ne sceglie nessuno
def scegliStrumento(strumenti):
    if not strumenti:   # se non ci sono strumenti tra cui scegliere, ritorna nessuno
        print("Non ci sono strumenti tra cui scegliere")
        return None
    codice = input("Id dello strumento (vuoto per annullare)> ").strip()   # legge l'id dello strumento inserito dall'utente e rimuove spazi bianchi
    if not codice:  # se l'id non è stato inserito, ritorna nessuno
        return None
    for i in strumenti: # ciclo per confrontare l'id di ogni strumento disponibile con l'id inserito
        if i.getId().lower() == codice.lower():    # se l'id dello strumento corrisponde a quello inserito, ritorna quello strumento
            return i
    print("Non e' stato trovato nessuno strumento con queste caratteristiche")  # se nessun id corrisponde, stampa un messaggio di errore
    return None

from PyQt5.QtWidgets import QMessageBox

# metodo per verificare se il testo inserito in un campo è un numero intero
def _interoValido(testo: str) -> bool:
    return testo.isdecimal()    # verifica che il testo sia un numero intero

# metodo per verificare se il testo inserito in un campo è un numero decimale
def _decimaleValido(testo: str) -> bool:
    for indice, carattere in enumerate(testo):  # itera sui caratteri del testo
        if carattere in ".,":   # se il carattere è un punto o una virgola, verifica le parti intera e decimale
            parte_intera = testo[:indice]   # la parte intera è quella prima del punto o della virgola
            parte_decimale = testo[indice + 1:] # la parte decimale è quella dopo il punto o la virgola
            return parte_intera.isdecimal() and (not parte_decimale or parte_decimale.isdecimal())  # verifica che la parte intera sia un numero intero e che la parte decimale sia o vuota o un numero intero
    return testo.isdecimal()    # se non ci sono punti o virgole verifica che il testo sia un numero intero

# metodo per verificare se il testo inserito in un campo è un numero valido (sia decimale che intero)
def numeroValido(testo, intero: bool = False) -> bool:
    testo = (testo or "").strip()   # rimuove gli spazi all'inizio e alla fine
    if not testo:   # se il testo è vuoto restituisce false
        return False
    if intero:  # se è stato richiesto di accettare solo numeri interi
        return _interoValido(testo) # verifica se il testo è un numero intero
    return _decimaleValido(testo)   # altrimenti verifica se il testo è un numero decimale

# metodo per validare il contenuto del campo e mostrare un messaggio di errore se il contenuto non è valido
def controllaNumero(campo, intero: bool = False, nome_campo: str = "valore") -> bool:
    testo = campo.text().strip()    # rimuove gli spazi all'inizio e alla fine del testo del campo
    if numeroValido(testo, intero): # se il testo è un numero valido restituisce true
        return True
    esempio = "6" if intero else "450.50"   # esempio di numero valido da mostrare
    if testo:   # se il testo non è vuoto mostra un messaggio di errore preciso, altrimenti mostra un messaggio generico
        messaggio = (f"Nel campo '{nome_campo}' hai scritto '{testo}': sono ammessi solo numeri (es. {esempio}), senza lettere")
    else:
        messaggio = f"Nel campo '{nome_campo}' devi scrivere un numero (es. {esempio})"
    QMessageBox.warning(campo.window(), "Attenzione", messaggio)    # mostra il messaggio di errore
    campo.setFocus()
    campo.selectAll() 
    return False

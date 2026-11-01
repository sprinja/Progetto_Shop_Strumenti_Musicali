from Services import GestoreUtenti, GestoreAmministratore
from Boundary.utilita import chiama

TIPI_ACCESSO = [("compratore", "Compratore"), ("venditore", "Venditore"), ("amministratore", "Amministratore")]

class BoundaryAccesso:
    # costruttore
    def __init__(self, gestore_utenti: GestoreUtenti, gestore_amministratore: GestoreAmministratore):
        self._gestore_utenti = gestore_utenti
        self._gestore_amministratore = gestore_amministratore

    # metodo per l'accesso al sistema
    def form_accesso(self):
        while True:
            print("\n=======================================================")
            print(" ACCESSO AL SISTEMA RICHIESTO ")
            print("=======================================================")
            print("Comandi: \n'login' (accedi alla tua pagina)\n'registra' (crea account)\n'esci'")
            print("=======================================================\n")
            scelta = input("Scegli un'opzione> ").strip().lower()
            if scelta == "esci":    # se l'utente sceglie di uscire, ritorna None
                return None
            elif scelta == "registra":  # se l'utente sceglie di registrarsi, chiama il metodo form_registrazione
                self.form_registrazione()
            elif scelta == "login": # se l'utente sceglie di accedere, chiama il metodo form_login e ritorna l'esito
                esito = self.form_login()
                if esito is not None:
                    return esito
            else:   # se l'utente inserisce un'opzione non valida, stampa un messaggio di errore
                print(f"Opzione '{scelta}' non valida.")

    # metodo per il login
    def form_login(self):
        tipo = self.form_scegli_tipo()
        if tipo is None:    # se l'utente non sceglie un tipo valido, ritorna None
            return None
        username = input("Nome utente> ").strip()
        password = input("Password> ").strip()
        if not username or not password:    # se l'utente non inserisce username o password, ritorna None
            print("Inserisci nome utente e password")
            return None
        if tipo == "Amministratore":    # se l'utente sceglie di accedere come amministratore, chiama il metodo verificaAccesso del gestore amministratore
            esito, utente = chiama(self._gestore_amministratore.verificaAccesso, username, password)
        else:   # se l'utente sceglie di accedere come compratore o venditore, chiama il metodo verificaLogin del gestore utenti
            esito, utente = chiama(self._gestore_utenti.verificaLogin, tipo, username, password)
        print(esito)
        if utente is None:  # se l'utente non esiste o le credenziali sono errate, ritorna None
            return None
        return tipo, utente

    # metodo per la registrazione
    def form_registrazione(self):
        tipo = self.form_scegli_tipo()
        if tipo is None:    # se l'utente non sceglie un tipo valido, ritorna None
            return None
        if tipo == "Amministratore":    # se l'utente sceglie di registrarsi come amministratore, stampa un messaggio di errore, altrimenti chiama il metodo verificaRegistrazione del gestore utenti
            print("Attenzione! Non e' possibile registrarsi come amministratore:\nle credenziali devono essere note a priori")
            return None 
        username = input("Nome utente> ").strip()   # legge l'input dell'utente e lo converte in minuscolo
        password = input("Password> ").strip()  # legge la password dell'utente
        esito = chiama(self._gestore_utenti.verificaRegistrazione,tipo, username, password) # chiama il metodo verificaRegistrazione del gestore utenti per verificare se l'utente può essere registrato
        print(esito)

    # metodo per scegliere il tipo di accesso
    def form_scegli_tipo(self):
        print("Tipi disponibili: " + ", ".join(f"'{chiave}'" for chiave, _ in TIPI_ACCESSO))
        while True: # ciclo per chiedere all'utente di scegliere un tipo di accesso finché non inserisce un'opzione valida
            scelta = input("Scegli l'accesso> ").strip().lower()    # legge l'input dell'utente e lo converte in minuscolo
            for chiave, nome in TIPI_ACCESSO:
                if scelta == chiave:    # se l'utente sceglie un tipo valido, ritorna il nome del tipo
                    return nome
            print(f"Opzione '{scelta}' non valida.")

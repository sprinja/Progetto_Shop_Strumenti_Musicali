from Services import GestoreAmministratore
from Boundary.utilita import chiama, stampaElenco

class BoundaryAmministratore:
    # costruttore
    def __init__(self, gestore_amministratore: GestoreAmministratore):
        self._gestore = gestore_amministratore

    # metodo per il menu di gestione degli utenti
    def menu_utenti(self):
        while True:    # ciclo per mostrare il menu degli utenti finché l'utente non sceglie di tornare indietro
            print("\n=======================================================")
            print(" Pagina Amministratore - gestione utenti")
            print("=======================================================")
            print("Compratori registrati:")
            stampaElenco(chiama(self._gestore.elencaCompratori), "Nessun compratore registrato")    # chiama il metodo del gestore per elencare i compratori registrati e stampa l'elenco
            print("Venditori registrati:")
            stampaElenco(chiama(self._gestore.elencaVenditori), "Nessun venditore registrato")    # chiama il metodo del gestore per elencare i venditori registrati e stampa l'elenco
            print("\nComandi disponibili: \n'compratore' (rimuovi) \n'venditore' (rimuovi) \n'indietro'")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()    # legge il comando inserito dall'utente e lo converte in minuscolo
            if comando == "indietro":    # se l'utente sceglie di tornare indietro, esce dal menu
                return
            elif comando == "compratore":    # se l'utente sceglie di rimuovere un compratore, chiama il metodo form_rimuovi_compratore
                self.form_rimuovi_compratore()
            elif comando == "venditore":    # se l'utente sceglie di rimuovere un venditore, chiama il metodo form_rimuovi_venditore
                self.form_rimuovi_venditore()
            else:   # se l'utente inserisce un comando non valido, stampa un messaggio di errore
                print(f"Comando '{comando}' non riconosciuto.")

    # metodo per la rimozione di un compratore
    def form_rimuovi_compratore(self):
        username = input("Username del compratore da rimuovere> ").strip()    # legge l'username del compratore da rimuovere
        print(chiama(self._gestore.rimuoviUtente, "Compratore", username))    # chiama il metodo del gestore per rimuovere il compratore e stampa l'esito

    # metodo per la rimozione di un venditore
    def form_rimuovi_venditore(self):
        username = input("Username del venditore da rimuovere> ").strip()    # legge l'username del venditore da rimuovere
        print(chiama(self._gestore.rimuoviUtente, "Venditore", username))    # chiama il metodo del gestore per rimuovere il venditore e stampa l'esito

    # metodo per il menu di gestione degli strumenti
    def menu_catalogo(self):
        while True:    # ciclo per mostrare il menu degli strumenti finché l'utente non sceglie di tornare indietro
            print("\n=======================================================")
            print(" Pagina Amministratore - gestione strumenti")
            print("=======================================================")
            print("Strumenti nello shop:")
            stampaElenco(chiama(self._gestore.elencaStrumenti), "Nessuno strumento nello shop")    # chiama il metodo del gestore per elencare gli strumenti nello shop e stampa l'elenco
            print("\nComandi disponibili: \n'rimuovi' \n'indietro'")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()    # legge il comando inserito dall'utente e lo converte in minuscolo
            if comando == "indietro":    # se l'utente sceglie di tornare indietro, esce dal menu
                return
            elif comando == "rimuovi":    # se l'utente sceglie di rimuovere uno strumento, chiama il metodo form_rimuovi_strumento
                self.form_rimuovi_strumento()
            else:   # se l'utente inserisce un comando non valido, stampa un messaggio di errore
                print(f"Comando '{comando}' non riconosciuto.")

    # metodo per la rimozione di uno strumento
    def form_rimuovi_strumento(self):
        codice = input("Id dello strumento da rimuovere> ").strip()    # legge l'id dello strumento da rimuovere
        print(chiama(self._gestore.rimuoviStrumento, codice))    # chiama il metodo del gestore per rimuovere lo strumento e stampa l'esito

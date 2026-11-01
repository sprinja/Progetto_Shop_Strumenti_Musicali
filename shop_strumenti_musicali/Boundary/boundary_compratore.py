from Services import GestoreCatalogo, GestoreAcquisti, GestoreNoleggi
from Boundary.utilita import (chiama, aDecimale, chiediIntero, stampaElenco, stampaStrumenti, scegliStrumento)

class BoundaryCompratore:
    # costruttore
    def __init__(self, gestore_catalogo: GestoreCatalogo, gestore_acquisti: GestoreAcquisti, gestore_noleggi: GestoreNoleggi, compratore):
        self._gestore_catalogo = gestore_catalogo
        self._gestore_acquisti = gestore_acquisti
        self._gestore_noleggi = gestore_noleggi
        self._compratore = compratore
        self._criterio = ""
        self._valore = ""

    # metodo per il menu principale del compratore
    def menu_compratore(self):
        while True:    # ciclo per mostrare il menu finché l'utente non sceglie di tornare indietro
            print("\n=======================================================")
            print(f" Pagina Compratore - {self._compratore.getUsername()}")
            print("=======================================================")
            if self._valore:    # se c'è una ricerca in corso, mostra e cerca i risultati della ricerca
                print(f"Risultati della ricerca ({self._criterio}: {self._valore})")
                strumenti = chiama(self._gestore_catalogo.cercaStrumenti, self._criterio, self._valore)    # chiama il metodo del gestore catalogo per cercare gli strumenti con la ricerca in corso
            else:   # altrimenti, elenca tutti gli strumenti disponibili nello shop
                print("Ecco tutti gli strumenti disponibili nello shop:")
                strumenti = chiama(self._gestore_catalogo.elencaStrumenti)    # chiama il metodo del gestore catalogo per elencare tutti gli strumenti
            stampaStrumenti(strumenti)  # stampa l'elenco degli strumenti trovati
            print("\nComandi disponibili: \n'cerca' (cerca strumenti) \n'azzera' (azzera ricerca) \n'acquista' \n'noleggia' \n'termina' (termina noleggio) \n'indietro'")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()    # legge il comando inserito dall'utente e lo converte in minuscolo
            if comando == "indietro":    # se l'utente sceglie di tornare indietro, esce dal menu
                return
            elif comando == "cerca":    # se l'utente sceglie di cercare, chiama il metodo form_cerca
                self.form_cerca()
            elif comando == "azzera":   # se l'utente sceglie di azzerare la ricerca, azzera criterio e valore
                self._criterio = ""
                self._valore = ""
            elif comando == "acquista":    # se l'utente sceglie di acquistare, chiama il metodo form_acquisto
                self.form_acquisto(strumenti)
            elif comando == "noleggia":    # se l'utente sceglie di noleggiare, chiama il metodo form_noleggio
                self.form_noleggio(strumenti)
            elif comando == "termina":    # se l'utente sceglie di terminare un noleggio, chiama il metodo form_termina_noleggio
                self.form_termina_noleggio()
            else:   # se l'utente inserisce un comando non valido, stampa un messaggio di errore
                print(f"Comando '{comando}' non riconosciuto.")

    # metodo per la ricerca degli strumenti
    def form_cerca(self):
        print("Criteri di ricerca disponibili: " + ", ".join(f"'{i}'" for i in GestoreCatalogo.CRITERI_RICERCA))    # stampa i criteri di ricerca disponibili
        while True:    # ciclo per chiedere all'utente il criterio di ricerca finché non inserisce un criterio valido
            criterio = input("Cerca per> ").strip().lower()    # legge il criterio di ricerca inserito dall'utente e lo converte in minuscolo
            if criterio in GestoreCatalogo.CRITERI_RICERCA:    # se il criterio è valido, esce dal ciclo
                break
            print(f"Criterio '{criterio}' non valido.")    # se il criterio non è valido, stampa un messaggio di errore
        valore = input("Valore da cercare> ").strip()    # legge il valore da cercare inserito dall'utente
        if valore and criterio == "prezzo" and aDecimale(valore) is None:    # se il criterio è il prezzo e il valore non è un numero, stampa un messaggio di errore e azzera il valore
            print("Nel campo 'prezzo massimo' devi scrivere un numero (es. 450.50), senza lettere")
            valore = ""
        if valore and not chiama(self._gestore_catalogo.cercaStrumenti, criterio, valore):    # se il valore è stato inserito ma non è stato trovato nessuno strumento, entra nel blocco
            print("Non e' stato trovato nessuno strumento con queste caratteristiche")    # stampa un messaggio di errore
        self._criterio = criterio    # salva il criterio della ricerca
        self._valore = valore    # salva il valore della ricerca

    # metodo per l'acquisto di uno strumento
    def form_acquisto(self, strumenti):
        s = scegliStrumento(strumenti)  # chiede all'utente di scegliere uno strumento tra quelli disponibili
        if s is None:   # se l'utente non sceglie nessuno strumento, esce dal metodo
            return
        quantita = chiediIntero("Quantita'> ", minimo=1)    # chiede all'utente la quantità di strumenti da acquistare
        print(chiama(self._gestore_acquisti.effettuaAcquisto, self._compratore.getUsername(), s.getId(), quantita))    # chiama il metodo del gestore acquisti per effettuare l'acquisto e stampa l'esito

    # metodo per il noleggio di uno strumento
    def form_noleggio(self, strumenti):
        scelta = scegliStrumento(strumenti)  # chiede all'utente di scegliere uno strumento tra quelli disponibili
        if scelta is None:   # se l'utente non sceglie nessuno strumento, esce dal metodo
            return
        quantita = chiediIntero("Quantita'> ", minimo=1)    # chiede all'utente la quantità di strumenti da noleggiare
        durata = chiediIntero("Durata (giorni)> ", minimo=1)    # chiede all'utente la durata del noleggio in giorni
        costo_massimo = round(scelta.getPrezzoNoleggioGiornaliero() * durata, 2)    # calcola il costo massimo del noleggio: prezzo di noleggio giornaliero per la durata
        print("Strumento selezionato (il prezzo di noleggio giornaliero e' l'ultimo valore indicato nella riga):")
        print(f"  {scelta}")
        print(f"Confermi il noleggio di {quantita} pezzi di '{scelta.getNome()}' ({scelta.getId()}) per {durata} giorni (costo massimo {costo_massimo:.2f} €)?")
        if input("Risposta (s/n)> ").strip().lower() == "s":    # se l'utente conferma il noleggio, lo registra
            print(chiama(self._gestore_noleggi.effettuaNoleggio, self._compratore.getUsername(), scelta.getId(), quantita, durata))    # chiama il metodo del gestore noleggi per effettuare il noleggio e stampa l'esito

    # metodo per la terminazione di un noleggio attivo
    def form_termina_noleggio(self):
        attivi = chiama(self._gestore_noleggi.noleggiAttivi, self._compratore.getUsername())    # chiama il metodo del gestore noleggi per elencare i noleggi attivi del compratore
        if not attivi:  # se il compratore non ha noleggi attivi, stampa un messaggio e torna al menu
            print("Non hai noleggi attivi a tuo carico")
            return
        print("Noleggi attivi a tuo carico:")
        for i in attivi:    # ciclo per stampare ogni noleggio attivo con il suo id
            print(f"  [{i.getId()}] {i}")
        codice = input("Id del noleggio da terminare (vuoto per annullare)> ").strip()    # legge l'id del noleggio da terminare inserito dall'utente
        if not codice:  # se l'id non è stato inserito, torna al menu
            return
        noleggio = next((i for i in attivi if i.getId().lower() == codice.lower()), None)    # cerca tra i noleggi attivi quello con l'id inserito
        if noleggio is None:    # se il noleggio non è stato trovato, stampa un messaggio di errore
            print("Non hai questo noleggio a tuo carico")
            return
        print(chiama(self._gestore_noleggi.terminaNoleggio, self._compratore.getUsername(), noleggio.getStrumento().get("id")))    # chiama il metodo del gestore noleggi per terminare il noleggio e stampa l'esito

    # metodo per il menu della cronologia acquisti e noleggi
    def menu_cronologia(self):
        while True:    # ciclo per mostrare il menu finché l'utente non sceglie di tornare indietro
            print("\n=======================================================")
            print(f" Cronologia - {self._compratore.getUsername()}")
            print("=======================================================")
            print("Comandi disponibili: \n'acquisti' \n'noleggi' \n'indietro'")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()    # legge il comando inserito dall'utente e lo converte in minuscolo
            if comando == "indietro":    # se l'utente sceglie di tornare indietro, esce dal menu
                return
            elif comando == "acquisti":  # se l'utente sceglie di vedere gli acquisti, stampa la cronologia degli acquisti
                print("Cronologia acquisti:")
                stampaElenco(chiama(self._gestore_acquisti.cronologiaAcquisti, self._compratore.getUsername()), "Cronologia vuota")    # chiama il metodo del gestore acquisti per la cronologia e stampa l'elenco
            elif comando == "noleggi":   # se l'utente sceglie di vedere i noleggi, stampa la cronologia dei noleggi
                print("Cronologia noleggi:")
                stampaElenco(chiama(self._gestore_noleggi.cronologiaNoleggi, self._compratore.getUsername()), "Cronologia vuota")    # chiama il metodo del gestore noleggi per la cronologia e stampa l'elenco
            else:   # se l'utente inserisce un comando non valido, stampa un messaggio di errore
                print(f"Comando '{comando}' non riconosciuto.")

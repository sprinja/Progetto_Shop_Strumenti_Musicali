from Models import Noleggio, Strumento, noleggio
from Repos import (StrumentoRepository, CategoriaRepository, CompratoreRepository, NoleggioRepository)

class GestoreNoleggi:
    # costruttore
    def __init__(self, strumento_repo: StrumentoRepository, categoria_repo: CategoriaRepository, compratore_repo: CompratoreRepository, noleggio_repo: NoleggioRepository):
        self._strumento_repo = strumento_repo
        self._categoria_repo = categoria_repo
        self._compratore_repo = compratore_repo
        self._noleggio_repo = noleggio_repo

    # effettua un noleggio
    def effettuaNoleggio(self, id_compratore: str, id_strumento: str, quantita: int, durata_giorni: int) -> str:
        compratore = self._compratore_repo.trovaPerUsername(id_compratore)  # trova il compratore corrispondente all'id fornito
        if compratore is None:  # se non esiste un compratore con l'id fornito, errore
            return "Errore: compratore non trovato"
        strumento = self._strumento_repo.trovaPerId(id_strumento)   # trova lo strumento corrispondente all'id fornito
        if strumento is None:   # se non esiste uno strumento con l'id fornito, errore
            return "Errore: strumento non trovato"
        try:
            q = int(quantita)   
            durata = int(durata_giorni)
        except (TypeError, ValueError): # se la quantita o la durata non sono numeri interi, errore
            return "Errore: quantita' o durata non valide"
        if q <= 0:  # se la quantita è minore o uguale a zero, errore
            return "Errore: la quantita' deve essere maggiore di zero"
        if durata < 1:  # se la durata è minore di 1 giorno, errore
            return "Errore: la durata del noleggio deve essere di almeno 1 giorno"
        if durata > 3650:   # se la durata supera il massimo consentito di 3650 giorni (10 anni), errore
            return "Errore: la durata massima del noleggio e' di 3650 giorni"
        if strumento.getQuantita() < q: # se la quantita richiesta è maggiore della quantita disponibile dello strumento, errore
            return (f"Errore: quantita' non disponibile (disponibili {strumento.getQuantita()})")
        temp = strumento.toDict()   # crea un dizionario con le informazioni dello strumento al momento del noleggio
        strumento.aggiornaQuantita(-q)  # aggiorna la quantita dello strumento sottraendo la quantita noleggiata
        self._strumento_repo.salva()
        noleggio = Noleggio(self._noleggio_repo.nuovoId(), compratore, temp, q, durata) # crea un oggetto Noleggio con le informazioni del noleggio
        self._noleggio_repo.aggiungi(noleggio)  # aggiunge il noleggio alla repository
        return (f"Noleggio registrato fino al {noleggio.getDataFine()} (costo massimo {noleggio.calcolaCostoMassimo():.2f} €): {noleggio}")

    # termina un noleggio 
    def terminaNoleggio(self, id_compratore: str, id_noleggio: str) -> str:
        for noleggio in self._noleggio_repo.perCompratore(id_compratore):   # itera sui noleggi del compratore corrispondente all'id fornito
            if noleggio.isAttivo() and noleggio.getId() == id_noleggio:   # se il noleggio è attivo e corrisponde all'id fornito, termina quel noleggio
                return self._termina(noleggio)
        return "Errore: non hai questo noleggio a tuo carico"

    # termina un noleggio e restituisce lo strumento al venditore
    def _termina(self, noleggio) -> str:
        try:
            rimborso = noleggio.restituisciStrumento()  # calcola il rimborso per il compratore
            self._rimettiInVendita(noleggio)    # rimette in vendita lo strumento noleggiato
            self._noleggio_repo.salva()
        except (TypeError, ValueError, OverflowError) as e: # se la chiusura del noleggio fallisce, ritorna un messaggio di errore invece di far bloccare l'applicazione
            return f"Errore: impossibile terminare il noleggio ({e})"
        esito = f"Noleggio terminato correttamente (rimborso {rimborso:.2f} €)"
        if rimborso > 0:    # se il rimborso è maggiore di zero, ossia se i noleggio è terminato anticipatamente il compratore viene rimborsato della somma extra pagata
            esito += " - il compratore viene rimborsato della somma extra pagata"
        return esito

    # verifica se ci sono noleggi scaduti e li termina automaticamente
    def verificaScadenze(self) -> list:
        esiti = []  # lista di esiti dei noleggi scaduti
        for noleggio in self._noleggio_repo.tuttiAttivi():  # itera su tutti i noleggi attivi
            if noleggio.isScaduto():    # se il noleggio è scaduto
                try:
                    noleggio.restituisciStrumento() #restituisce lo strumento al venditore
                    self._rimettiInVendita(noleggio)    # rimette in vendita lo strumento noleggiato
                    self._noleggio_repo.salva()
                    esiti.append(f"Noleggio scaduto e terminato: {noleggio}")   # aggiunge l'esito alla lista degli esiti
                except (TypeError, ValueError, OverflowError) as e: # se la chiusura di questo noleggio fallisce, lo segnala e passa al successivo senza bloccare il timer
                    esiti.append(f"Errore nella chiusura del noleggio {noleggio.getId()}: {e}")
        return esiti

    # rimette in vendita uno strumento noleggiato
    def _rimettiInVendita(self, noleggio) -> None:
        temp = noleggio.getStrumento()  # recupera i dati dello strumento salvati nel noleggio        
        quantita = noleggio.getQuantita()   # recupera la quantita noleggiata
        esistente = self._strumento_repo.trovaPerId(temp.get("id")) # verifica se lo strumento esiste già nella repository
        if (esistente is not None and esistente.getNome() == temp.get("nome") and esistente.getVenditore() == temp.get("venditore")):   # se lo strumento esiste già nella repository e ha lo stesso nome e venditore, aggiorna la quantita dello strumento
            esistente.aggiornaQuantita(quantita)
            self._strumento_repo.salva()
            return
        categoria = self._categoria_repo.trovaPerNome(temp.get("tipo")) # verifica se la categoria dello strumento esiste nella repository
        if categoria is None:   # se la categoria non esiste, stampa un messaggio di avviso e non rimette in vendita lo strumento
            print(f"[Attenzione] impossibile rimettere in vendita '{temp.get('nome')}': tipo '{temp.get('tipo')}' inesistente")
            return
        id_strumento = temp.get("id")   
        if self._strumento_repo.trovaPerId(id_strumento) is not None:   # se lo strumento esiste già nella repository, genera un nuovo id per lo strumento
            id_strumento = self._strumento_repo.nuovoId()
        self._strumento_repo.aggiungi(Strumento( id_strumento, temp.get("nome"), categoria, temp.get("azienda"), temp.get("venditore"), quantita, temp.get("prezzo"), temp.get("nome_venditore"), temp.get("prezzo_noleggio_giornaliero")))  # aggiunge lo strumento alla repository con la nuova quantita e il prezzo di noleggio salvato nel noleggio

    # elenca tutti i noleggi
    def cronologiaNoleggi(self, id_compratore: str) -> list:
        return self._noleggio_repo.perCompratore(id_compratore)

    # elenca tutti i noleggi attivi di un compratore
    def noleggiAttivi(self, id_compratore: str) -> list:
        return self._noleggio_repo.attiviPerCompratore(id_compratore)

    # elenca tutti i noleggi attivi di un venditore
    def noleggiDelVenditore(self, id_venditore: str) -> list:
        return self._noleggio_repo.perVenditore(id_venditore)

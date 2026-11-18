from Models import Amministratore
from Repos import (AmministratoreRepository, CompratoreRepository, VenditoreRepository, StrumentoRepository, AcquistoRepository, NoleggioRepository)
from Services.gestore_noleggi import GestoreNoleggi

class GestoreAmministratore:
    # costruttore
    def __init__(self, amministratore_repo: AmministratoreRepository, compratore_repo: CompratoreRepository, venditore_repo: VenditoreRepository, strumento_repo: StrumentoRepository, acquisto_repo: AcquistoRepository, noleggio_repo: NoleggioRepository, gestore_noleggi: GestoreNoleggi):
        self._amministratore_repo = amministratore_repo
        self._compratore_repo = compratore_repo
        self._venditore_repo = venditore_repo
        self._strumento_repo = strumento_repo
        self._acquisto_repo = acquisto_repo
        self._noleggio_repo = noleggio_repo
        self._gestore_noleggi = gestore_noleggi

    # verifica l'accesso di un amministratore
    def verificaAccesso(self, username: str, password: str):
        username = (username or "").strip() # rimuove spazi bianchi all'inizio e alla fine del nome utente
        if not username:    # se il nome utente è vuoto, errore
            return ("Errore: inserisci il nome utente", None)
        if not password:    # se la password è vuota, errore
            return ("Errore: inserisci la password", None)
        if not self._amministratore_repo.verificaCredenziali(username, password):   # se il nome utente non esiste nella repository o la password non corrisponde, errore
            return ("Errore: dati non validi", None)
        admin = self._amministratore_repo.trovaPerUsername(username)    # se l'accesso è corretto, restituisce l'amministratore corrispondente
        return (f"Accesso effettuato come {admin}", admin)

    # elenca tutti i compratori
    def elencaCompratori(self) -> list:
        return self._compratore_repo.tutti()

    # elenca tutti i venditori
    def elencaVenditori(self) -> list:
        return self._venditore_repo.tutti()

    # elenca tutti gli strumenti
    def elencaStrumenti(self) -> list:
        return self._strumento_repo.tutti()

    # rimuove uno strumento dal catalogo
    def rimuoviStrumento(self, id_strumento: str) -> str:
        strumento = self._strumento_repo.trovaPerId(id_strumento)   # trova lo strumento corrispondente all'id fornito
        if strumento is None:   # se non esiste uno strumento con l'id fornito, errore
            return "Errore: non e' stato trovato uno strumento"
        self._strumento_repo.rimuovi(strumento.getId()) # rimuove lo strumento dalla repository
        return f"Lo strumento e' stato rimosso: {strumento}"

    # rimuove un utente (compratore o venditore) dal sistema
    def rimuoviUtente(self, tipo: str, username: str) -> str:
        username = (username or "").strip() # rimuove spazi bianchi all'inizio e alla fine del nome utente
        if not username:    # se il nome utente è vuoto, errore
            return "Errore: inserisci il nome utente" 
        if tipo == "Compratore":    # se il tipo è compratore, rimuove il compratore corrispondente
            return self._rimuoviCompratore(username)
        if tipo == "Venditore": # se il tipo è venditore, rimuove il venditore corrispondente
            return self._rimuoviVenditore(username)
        return "Errore: scegli se rimuovere un compratore o un venditore"

    # rimuove un compratore dal sistema
    def _rimuoviCompratore(self, username: str) -> str:
        compratore = self._compratore_repo.trovaPerUsername(username)   # trova il compratore corrispondente all'username fornito
        if compratore is None:  # se non esiste un compratore con l'username fornito, errore
            return "Errore: non esiste un compratore con questo nome utente"
        for noleggio in list(self._noleggio_repo.attiviPerCompratore(username)):    # per ogni noleggio attivo del compratore, termina il noleggio e restituisce lo strumento
            self._gestore_noleggi.terminaNoleggio(username, noleggio.getId())
        acquisti = self._acquisto_repo.rimuoviPerUtente(username)   # rimuove tutti gli acquisti del compratore
        noleggi = self._noleggio_repo.rimuoviPerUtente(username)    # rimuove tutti i noleggi del compratore
        self._compratore_repo.rimuovi(username) # rimuove il compratore dalla repository
        return (f"Il compratore e' stato rimosso  ({acquisti} acquisti e {noleggi} noleggi eliminati, strumenti noleggiati rimessi in vendita)")

    # rimuove un venditore dal sistema
    def _rimuoviVenditore(self, username: str) -> str:
        venditore = self._venditore_repo.trovaPerUsername(username) # trova il venditore corrispondente all'username fornito
        if venditore is None:   # se non esiste un venditore con l'username fornito, errore
            return "Errore: non esiste un venditore con questo nome utente"
        for noleggio in list(self._noleggio_repo.attiviPerVenditore(username)): # per ogni noleggio attivo del venditore, termina il noleggio
            noleggio.restituisciStrumento()
        self._noleggio_repo.salva()
        rimossi = 0 # conta il numero di strumenti rimossi dallo shop
        for strumento in list(self._strumento_repo.tutti()):    # per ogni strumento, se il venditore corrisponde all'username fornito, rimuove lo strumento dalla repository e incrementa il contatore
            if strumento.getVenditore() == username:    # se il venditore dello strumento corrisponde all'username fornito, rimuove lo strumento dalla repository
                self._strumento_repo.rimuovi(strumento.getId()) 
                rimossi += 1
        self._venditore_repo.rimuovi(username)  # rimuove il venditore dalla repository
        return (f"Il venditore e' stato rimosso ({rimossi} strumenti rimossi dallo shop)")

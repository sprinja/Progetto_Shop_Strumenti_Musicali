from Models import Compratore, Venditore
from Repos import CompratoreRepository, VenditoreRepository

class GestoreUtenti:
    # regole per la password
    LUNGHEZZA_PASSWORD = 5
    REGOLE_PASSWORD = ("almeno 5 caratteri, almeno un numero, almeno una lettera maiuscola e una minuscola")

    # costruttore
    def __init__(self, compratore_repo: CompratoreRepository, venditore_repo: VenditoreRepository):
        self._compratore_repo = compratore_repo
        self._venditore_repo = venditore_repo

    # verifica se la password rispetta le regole
    @staticmethod
    def passwordValida(password: str) -> bool:
        return (isinstance(password, str) and len(password) >= GestoreUtenti.LUNGHEZZA_PASSWORD and any(i.isdigit() for i in password) and any(i.isupper() for i in password) and any(i.islower() for i in password))

    # restituisce il repository corretto in base al tipo di utente
    def _repo(self, tipo: str):
        if tipo == "Compratore":
            return self._compratore_repo
        if tipo == "Venditore":
            return self._venditore_repo
        return None

    # verifica la registrazione di un nuovo utente
    def verificaRegistrazione(self, tipo: str, username: str, password: str) -> str:
        repo = self._repo(tipo) # prende la repository corretta in base al tipo di utente
        if repo is None:    # se il tipo non è valido, errore
            return "Errore: tipo di accesso non valido"
        username = (username or "").strip() # rimuove spazi bianchi all'inizio e alla fine del nome utente
        if not username:    # se il nome utente è vuoto, errore
            return "Errore: inserisci il nome utente"
        if not self.passwordValida(password):   # se la password non rispetta le regole, errore
            return f"Errore: la password deve avere {self.REGOLE_PASSWORD}"
        if repo.esiste(username):   # se il nome utente esiste già nella repository, errore
            return f"Errore: il nome utente '{username}' e' gia' utilizzato"
        if tipo == "Compratore":    # se il tipo è compratore, aggiunge un nuovo compratore alla repository
            repo.aggiungi(Compratore(username, password))
        elif tipo == "Venditore":   # se il tipo è venditore, aggiunge un nuovo venditore alla repository
            repo.aggiungi(Venditore(username, password))
        return f"Registrazione completata: {tipo} '{username}' creato"

    # verifica il login di un utente
    def verificaLogin(self, tipo: str, username: str, password: str):
        repo = self._repo(tipo) # prende la repository corretta in base al tipo di utente
        if repo is None:    # se il tipo non è valido, errore
            return ("Errore: tipo di accesso non valido", None)
        username = (username or "").strip() # rimuove spazi bianchi all'inizio e alla fine del nome utente
        if not username:    # se il nome utente è vuoto, errore
            return ("Errore: inserisci il nome utente", None)
        if not password:    # se la password è vuota, errore
            return ("Errore: inserisci la password", None)
        if not repo.esiste(username) or not repo.verificaCredenziali(username, password):   # se il nome utente non esiste nella repository o la password non corrisponde, errore
            return ("Errore: nome utente o password non validi", None)
        utente = repo.trovaPerUsername(username)    # se il login è corretto, restituisce l'utente corrispondente
        return (f"Accesso effettuato come {utente}", utente)

    # elenca tutti i compratori
    def elencaCompratori(self) -> list:
        return self._compratore_repo.tutti()

    # elenca tutti i venditori
    def elencaVenditori(self) -> list:
        return self._venditore_repo.tutti()

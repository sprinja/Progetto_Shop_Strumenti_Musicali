import json
from Models import Compratore

class CompratoreRepository:
    # costruttore
    def __init__(self, path: str = "compratori.json"):
        self._path = path
        self._compratori: dict = {}
        self.carica()

    # metodo che carica i dati dei compratori dal file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apre il file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._compratori = {i["username"]: Compratore.fromDict(i) for i in dati}   # crea un dizionario di oggetti Compratore a partire dai dati caricati
        except FileNotFoundError:   # se il file non esiste, inizializza un dizionario vuoto
            self._compratori = {}

    # metodo che salva i dati dei compratori nel file JSON
    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:  # apre il file in modalità scrittura
            json.dump([i.toDict() for i in self._compratori.values()], f, ensure_ascii=False, indent=2) # salva i dati dei compratori nel file JSON, convertendo gli oggetti Compratore in dizionari

    # metodo che trova un compratore per username
    def trovaPerUsername(self, username: str):
        return self._compratori.get(username)

    # metodo che verifica se un compratore esiste
    def esiste(self, username: str) -> bool:
        return username in self._compratori

    # metodo che verifica le credenziali di un compratore
    def verificaCredenziali(self, username: str, password: str) -> bool:
        compratore = self._compratori.get(username)
        return compratore is not None and compratore.credenzialiCorrette(username, password)    # verifica se le credenziali del compratore sono corrette

    # metodo che aggiunge un nuovo compratore
    def aggiungi(self, compratore: Compratore) -> None:
        self._compratori[compratore.getUsername()] = compratore
        self.salva()

    # metodo che rimuove un compratore per username
    def rimuovi(self, username: str) -> bool:
        if username not in self._compratori:    # se il compratore non esiste, restituisce False
            return False
        del self._compratori[username]
        self.salva()
        return True

    # metodo che restituisce una lista di tutti i compratori
    def tutti(self) -> list:
        return list(self._compratori.values())

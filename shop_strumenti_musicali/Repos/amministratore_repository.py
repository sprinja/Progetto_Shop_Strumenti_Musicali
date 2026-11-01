import json
from Models import Amministratore

class AmministratoreRepository:
    # costruttore
    def __init__(self, path: str = "amministratori.json"):
        self._path = path
        self._amministratori: dict = {}
        self.carica()

    # metodo che carica i dati degli amministratori dal file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apre il file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._amministratori = {i["username"]: Amministratore.fromDict(i) for i in dati}  # crea un dizionario di oggetti Amministratore a partire dai dati caricati
        except FileNotFoundError:   # se il file non esiste, inizializza un dizionario vuoto
            self._amministratori = {}

    # metodo che trova un amministratore per username
    def trovaPerUsername(self, username: str):
        return self._amministratori.get(username)

    # metodo che verifica le credenziali di un amministratore
    def verificaCredenziali(self, username: str, password: str) -> bool:
        admin = self._amministratori.get(username)
        return admin is not None and admin.credenzialiCorrette(username, password)  # verifica se le credenziali dell'amministratore sono corrette

    # metodo che restituisce una lista di tutti gli amministratori
    def tutti(self) -> list:
        return list(self._amministratori.values())

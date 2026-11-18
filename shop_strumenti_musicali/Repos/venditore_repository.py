import json
from Models import Venditore

class VenditoreRepository:
    # costruttore
    def __init__(self, path: str = "venditori.json"):
        self._path = path
        self._venditori: dict = {}
        self.carica()

    # metodo che carica i dati dei venditori dal file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apre il file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._venditori = {i["username"]: Venditore.fromDict(i) for i in dati}  # crea un dizionario di oggetti Venditore a partire dai dati caricati
        except FileNotFoundError:   # se il file non esiste, inizializza un dizionario vuoto
            self._venditori = {}
        except (json.JSONDecodeError, KeyError, TypeError, ValueError, UnicodeDecodeError) as e:   # se il file è corrotto o contiene dati non validi, interrompe l'avvio con un messaggio chiaro senza sovrascriverlo
            raise SystemExit(f"File dati non leggibile: {self._path} ({e}) - ripristina il file o eliminalo per ripartire con dati vuoti")

    # metodo che salva i dati dei venditori nel file JSON
    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:  # apre il file in modalità scrittura
            json.dump([i.toDict() for i in self._venditori.values()], f, ensure_ascii=False, indent=2)  # salva i dati dei venditori nel file JSON, convertendo gli oggetti Venditore in dizionari

    # metodo che trova un venditore per username
    def trovaPerUsername(self, username: str):
        return self._venditori.get(username)

    # metodo che verifica se un venditore esiste
    def esiste(self, username: str) -> bool:
        return username in self._venditori

    # metodo che verifica le credenziali di un venditore
    def verificaCredenziali(self, username: str, password: str) -> bool:
        venditore = self._venditori.get(username)
        return venditore is not None and venditore.credenzialiCorrette(username, password)  # verifica se le credenziali del venditore sono corrette

    # metodo che aggiunge un nuovo venditore
    def aggiungi(self, venditore: Venditore) -> None:
        self._venditori[venditore.getUsername()] = venditore
        self.salva()

    # metodo che rimuove un venditore per username
    def rimuovi(self, username: str) -> bool:
        if username not in self._venditori: # se il venditore non esiste, restituisce False
            return False
        del self._venditori[username]
        self.salva()
        return True

    # metodo che restituisce una lista di tutti i venditori
    def tutti(self) -> list:
        return list(self._venditori.values())

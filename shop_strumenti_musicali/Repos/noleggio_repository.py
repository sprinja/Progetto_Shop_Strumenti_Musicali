import json
from Repos import CompratoreRepository
from Models import Noleggio

class NoleggioRepository:
    # costruttore
    def __init__(self, path: str, compratore_repo: CompratoreRepository):
        self._path = path
        self._compratore_repo = compratore_repo
        self._noleggi: dict = {}
        self.carica()

    # metodo che carica i dati dei noleggi dal file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apre il file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._noleggi = {}  # crea un dizionario di oggetti Noleggio a partire dai dati caricati
            for i in dati:  # itera sui dati caricati dal file JSON
                compratore = self._compratore_repo.trovaPerUsername(i["compratore"])  # trova il compratore corrispondente all'username del compratore del noleggio
                if compratore:  # se il compratore esiste, crea un oggetto Noleggio a partire dai dati caricati e dal compratore trovato
                    self._noleggi[i["id"]] = Noleggio.fromDict(i, compratore)
        except FileNotFoundError:
            self._noleggi = {}  # se il file non esiste, inizializza un dizionario vuoto

    # metodo che salva i dati dei noleggi nel file JSON
    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:  # apre il file in modalità scrittura
            json.dump([i.toDict() for i in self._noleggi.values()], f, ensure_ascii=False, indent=2) # salva i dati dei noleggi nel file JSON, convertendo gli oggetti Noleggio in dizionari

    # metodo che trova un noleggio per id
    def trovaPerId(self, id_noleggio: str):
        return self._noleggi.get(id_noleggio)

    # metodo che aggiunge un nuovo noleggio
    def aggiungi(self, noleggio: Noleggio) -> None:
        self._noleggi[noleggio.getId()] = noleggio
        self.salva()

    # metodo che rimuove un noleggio per id
    def rimuovi(self, id_noleggio: str) -> bool:
        if id_noleggio not in self._noleggi: # se il noleggio non esiste, restituisce False
            return False
        del self._noleggi[id_noleggio]   # rimuove il noleggio dal dizionario
        self.salva()
        return True

    # metodo che restituisce una lista di tutti i noleggi
    def tutti(self) -> list:
        return list(self._noleggi.values())

    # metodo che genera un nuovo id per un noleggio
    def nuovoId(self) -> str:
        IDmax = 0   # inizializza il massimo id trovato a 0
        for i in self._noleggi:   # itera sugli id dei noleggi presenti nel dizionario
            if i.startswith("N") and i[1:].isdigit():   # se l'id inizia con "N" e il resto è un numero, aggiorna IDmax
                IDmax = max(IDmax, int(i[1:]))  # aggiorna il massimo id trovato
        return f"N{IDmax + 1}"  # restituisce il nuovo id generato, incrementando il massimo id trovato di 1 e aggiungendo il prefisso "N"

    # metodo che restituisce una lista di noleggi per un compratore
    def perCompratore(self, username: str) -> list:
        return [i for i in self._noleggi.values() if i.getCompratore().getUsername() == username]

    # metodo che restituisce una lista di noleggi attivi per un compratore
    def attiviPerCompratore(self, username: str) -> list:
        return [i for i in self.perCompratore(username) if i.isAttivo()]

    # metodo che restituisce una lista di noleggi per un venditore
    def perVenditore(self, username: str) -> list:
        return [i for i in self._noleggi.values() if i.getStrumento().get("venditore") == username]

    # metodo che restituisce una lista di noleggi attivi per un venditore
    def attiviPerVenditore(self, username: str) -> list:
        return [i for i in self.perVenditore(username) if i.isAttivo()]

    # metodo che restituisce una lista di tutti i noleggi attivi
    def tuttiAttivi(self) -> list:
        return [i for i in self._noleggi.values() if i.isAttivo()]

    # metodo che rimuove tutti i noleggi di un compratore e restituisce il numero di noleggi rimossi
    def rimuoviPerUtente(self, username: str) -> int:
        temp = len(self._noleggi)   # salvataggio stato iniziale del numero di noleggi
        self._noleggi = {k: v for k, v in self._noleggi.items() if v.getCompratore().getUsername() != username}   # rimuove tutti i noleggi del compratore specificato
        rimossi = temp - len(self._noleggi) # calcola il numero di noleggi rimossi
        if rimossi: # se sono stati rimossi dei noleggi, salva lo stato aggiornato nel file JSON
            self.salva()
        return rimossi

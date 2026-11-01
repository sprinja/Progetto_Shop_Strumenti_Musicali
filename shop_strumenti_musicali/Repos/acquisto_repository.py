import json
from Repos import CompratoreRepository
from Models import Acquisto

class AcquistoRepository:
    # costruttore
    def __init__(self, path: str, compratore_repo: CompratoreRepository):
        self._path = path
        self._compratore_repo = compratore_repo
        self._acquisti: dict = {}
        self.carica()

    # metodo che carica i dati degli acquisti dal file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apre il file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._acquisti = {} # crea un dizionario di oggetti Acquisto a partire dai dati caricati
            for i in dati:  # itera sui dati caricati dal file JSON
                compratore = self._compratore_repo.trovaPerUsername(i["compratore"])  # trova il compratore corrispondente all'id del compratore dell'acquisto
                if compratore:  # se il compratore esiste, crea un oggetto Acquisto a partire dai dati caricati e dal compratore trovato
                    self._acquisti[i["id"]] = Acquisto.fromDict(i, compratore)
        except FileNotFoundError:
            self._acquisti = {} # se il file non esiste, inizializza un dizionario vuoto

    # metodo che salva i dati degli acquisti nel file JSON
    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:  # apre il file in modalità scrittura
            json.dump([i.toDict() for i in self._acquisti.values()], f, ensure_ascii=False, indent=2)   # salva i dati degli acquisti nel file JSON, convertendo gli oggetti Acquisto in dizionari

    # metodo che trova un acquisto per id
    def trovaPerId(self, id_acquisto: str):
        return self._acquisti.get(id_acquisto)

    # metodo che aggiunge un nuivo acquisto
    def aggiungi(self, acquisto: Acquisto) -> None:
        self._acquisti[acquisto.getId()] = acquisto
        self.salva()

    # metodo che rimuove un acquisto per id
    def rimuovi(self, id_acquisto: str) -> bool:
        if id_acquisto not in self._acquisti:   # se l'acquisto non esiste, restituisce False
            return False
        del self._acquisti[id_acquisto] # rimuove l'acquisto dal dizionario
        self.salva()
        return True

    # metodo che restituisce una lista di tutti gli acquisti
    def tutti(self) -> list:
        return list(self._acquisti.values())

    # metodo che genera un nuovo id per un acquisto
    def nuovoId(self) -> str:
        IDmax = 0
        for i in self._acquisti:
            if i.startswith("A") and i[1:].isdigit():
                IDmax = max(IDmax, int(i[1:]))
        return f"A{IDmax + 1}"

    # metodo che restituisce una lista di acquisti per un compratore
    def perCompratore(self, username: str) -> list:
        return [i for i in self._acquisti.values() if i.getCompratore().getUsername() == username]

    # metodo che restituisce una lista di acquisti per un venditore
    def perVenditore(self, username: str) -> list:
        return [i for i in self._acquisti.values() if i.getStrumento().get("venditore") == username]

    # metodo che rimuove tutti gli acquisti di un compratore e restituisce il numero di acquisti rimossi
    def rimuoviPerUtente(self, username: str) -> int:
        temp = len(self._acquisti)  # salvataggio stato iniziale del numero di acquisti
        self._acquisti = {k: v for k, v in self._acquisti.items() if v.getCompratore().getUsername() != username} # rimuove tutti gli acquisti del compratore specificato
        rimossi = temp - len(self._acquisti)    # calcola il numero di acquisti rimossi
        if rimossi: # se sono stati rimossi degli acquisti, salva lo stato aggiornato nel file JSON
            self.salva()
        return rimossi

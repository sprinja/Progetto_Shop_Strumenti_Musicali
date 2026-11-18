import json
from Repos import CategoriaRepository
from Models import Strumento

class StrumentoRepository:
    # costruttore
    def __init__(self, path: str, categoria_repo: CategoriaRepository):
        self._path = path
        self._categoria_repo = categoria_repo
        self._strumenti: dict = {}
        self.carica()

    # metodo che carica i dati degli strumenti dal file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apre il file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._strumenti = {}    # crea un dizionario di oggetti Strumento a partire dai dati caricati
            for i in dati:  # itera sui dati caricati dal file JSON
                categoria = self._categoria_repo.trovaPerNome(i["tipo"])    # trova la categoria corrispondente al tipo dello strumento
                if categoria is None:   # se la categoria non esiste, stampa un messaggio di avviso e scarta lo strumento
                    print(f"[Attenzione] tipo '{i.get('tipo')}' inesistente, strumento '{i.get('nome')}' scartato")
                    continue
                self._strumenti[i["id"]] = Strumento.fromDict(i, categoria) # crea un oggetto Strumento a partire dai dati caricati e dalla categoria trovata
        except FileNotFoundError:
            self._strumenti = {}    # se il file non esiste, inizializza un dizionario vuoto

    # metodo che salva i dati degli strumenti nel file JSON
    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:  # apre il file in modalità scrittura
            json.dump([i.toDict() for i in self._strumenti.values()], f, ensure_ascii=False, indent=2)  # salva i dati degli strumenti nel file JSON, convertendo gli oggetti Strumento in dizionari

    # metodo che trova uno strumento per id
    def trovaPerId(self, id_strumento: str):
        return self._strumenti.get(id_strumento)

    # metodo che verifica se uno strumento esiste
    def esiste(self, id_strumento: str) -> bool:
        return id_strumento in self._strumenti

    # metodo che aggiunge un nuovo strumento
    def aggiungi(self, strumento: Strumento) -> None:
        self._strumenti[strumento.getId()] = strumento
        self.salva()

    # metodo che rimuove uno strumento per id
    def rimuovi(self, id_strumento: str) -> bool:
        if id_strumento not in self._strumenti: # se lo strumento non esiste, restituisce False
            return False
        del self._strumenti[id_strumento]   # rimuove lo strumento dal dizionario
        self.salva()
        return True

    # metodo che restituisce una lista di tutti gli strumenti
    def tutti(self) -> list:
        return list(self._strumenti.values())

    # metodo che genera un nuovo id per uno strumento
    def nuovoId(self) -> str:
        IDmax = 0   # inizializza il massimo id trovato a 0
        for i in self._strumenti:   # itera sugli id degli strumenti presenti nel dizionario
            if i.startswith("S") and i[1:].isdigit():   # se l'id inizia con "S" e il resto è un numero, aggiorna IDmax
                IDmax = max(IDmax, int(i[1:]))  # aggiorna il massimo id trovato
        return f"S{IDmax + 1}"  # restituisce il nuovo id generato, incrementando il massimo id trovato di 1 e aggiungendo il prefisso "S"

    # metodo che cerca strumenti in base a un criterio e un valore
    def cerca(self, criterio: str, valore) -> list:
        testo = str(valore).strip().lower() # converte il valore in stringa, rimuove gli spazi bianchi iniziali e finali e lo converte in minuscolo
        if not testo:   # se il valore è vuoto, restituisce tutti gli strumenti
            return self.tutti()
        criterio = (criterio or "").strip().lower() # converte il criterio in stringa, rimuove gli spazi bianchi iniziali e finali e lo converte in minuscolo
        if criterio == "prezzo massimo":    # se il criterio è "prezzo massimo", cerca gli strumenti con prezzo minore o uguale al valore specificato
            try:
                prezzo = float(testo.replace(",", ".")) # converte il valore in float, sostituendo eventuali virgole con punti
            except ValueError:
                return []
            return [i for i in self._strumenti.values() if i.getPrezzo() <= prezzo] # restituisce gli strumenti con prezzo minore o uguale al valore specificato
        if criterio == "tipo":  # se il criterio è "tipo", cerca gli strumenti con tipo che contiene il valore specificato
            return [i for i in self._strumenti.values() if testo in i.getTipo()]
        if criterio in ("azienda", "produttore", "marca"):  # se il criterio è "azienda", "produttore" o "marca", cerca gli strumenti con azienda che contiene il valore specificato
            return [i for i in self._strumenti.values() if testo in i.getAzienda().lower()]
        if criterio == "nome":  # se il criterio è "nome", cerca gli strumenti con nome che contiene il valore specificato
            return [i for i in self._strumenti.values() if testo in i.getNome().lower()]
        if criterio == "venditore": # se il criterio è "venditore", cerca gli strumenti con nome del venditore che contiene il valore specificato
            return [i for i in self._strumenti.values() if testo in i.getNomeVenditore().lower()]
        return self.tutti() # se il criterio non è valido, restituisce tutti gli strumenti

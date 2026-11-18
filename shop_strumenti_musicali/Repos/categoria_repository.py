import json
from Models import CategoriaStrumento

class CategoriaRepository:
    # costruttore
    def __init__(self, path: str = "categorie.json"):
        self._path = path
        self._categorie: dict = {}
        self.carica()

    # metodo per caricare le categorie da un file JSON
    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:  # apertura del file in modalità lettura
                dati = json.load(f) # carica i dati dal file JSON
            self._categorie = {d["nome_tipo"]: CategoriaStrumento.fromDict(d) for d in dati}    # crea un dizionario di oggetti CategoriaStrumento a partire dai dati caricati
        except FileNotFoundError:   # se il file non esiste, inizializza un dizionario vuoto
            self._categorie = {}
        except (json.JSONDecodeError, KeyError, TypeError, ValueError, UnicodeDecodeError) as e:   # se il file è corrotto o contiene dati non validi, interrompe l'avvio con un messaggio chiaro senza sovrascriverlo
            raise SystemExit(f"File dati non leggibile: {self._path} ({e}) - ripristina il file o eliminalo per ripartire con dati vuoti")

    # metodo per salvare le categorie in un file JSON
    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:  # apre il file in modalità scrittura
            json.dump([c.toDict() for c in self._categorie.values()], f, ensure_ascii=False, indent=2)  # salva i dati delle categorie nel file JSON, convertendo gli oggetti CategoriaStrumento in dizionari

    # metodo per trovare una categoria per nome_tipo
    def trovaPerNome(self, nome_tipo: str):
        if not nome_tipo:   # se il nome_tipo è vuoto o None, restituisce None
            return None
        return self._categorie.get(str(nome_tipo).strip().lower())  # restituisce la categoria corrispondente al nome_tipo, ignorando spazi e maiuscole/minuscole

    # metodo per verificare se una categoria esiste
    def esiste(self, nome_tipo: str) -> bool:
        return self.trovaPerNome(nome_tipo) is not None

    # metodo per aggiungere una nuova categoria
    def aggiungi(self, categoria: CategoriaStrumento) -> None:
        self._categorie[categoria.getNomeTipo()] = categoria
        self.salva()

    # metodo che restituisce una lista di tutte le categorie
    def tutti(self) -> list:
        return list(self._categorie.values())

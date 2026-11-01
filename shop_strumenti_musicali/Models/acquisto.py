from datetime import date
from Models import Compratore

class Acquisto:
    # costruttore
    def __init__(self, id: str, compratore: Compratore, strumento: dict, quantita: int, data_acquisto: str = None):
        if not isinstance(compratore, Compratore):  # se compratore non è un oggetto Compratore, errore
            raise TypeError("compratore deve essere un Compratore")
        if int(quantita) <= 0:  # se quantita è negativa o zero, errore
            raise ValueError("la quantita' acquistata deve essere positiva")
        self._id = id
        self._compratore = compratore
        self._strumento = dict(strumento)
        self._quantita = int(quantita)
        self._data = data_acquisto or str(date.today())

    # metodi getter
    def getId(self) -> str:
        return self._id

    def getCompratore(self) -> Compratore:
        return self._compratore

    def getStrumento(self) -> dict:
        return self._strumento

    def getQuantita(self) -> int:
        return self._quantita

    def getData(self) -> str:
        return self._data

    def getPrezzoUnitario(self) -> float:
        return float(self._strumento.get("prezzo", 0.0))

    def getTotale(self) -> float:
        return round(self.getPrezzoUnitario() * self._quantita, 2)

    # metodo che restituisce un dizionario con le informazioni dell'acquisto
    def toDict(self) -> dict:
        return {
            "id": self._id,
            "compratore": self._compratore.getUsername(),
            "strumento": self._strumento,
            "quantita": self._quantita,
            "data_acquisto": self._data
        }

    # metodo che crea un oggetto Acquisto a partire da un dizionario
    @classmethod
    def fromDict(cls, d: dict, compratore: Compratore) -> "Acquisto":
        return cls(d["id"], compratore, d["strumento"], d["quantita"], d["data_acquisto"])

    # metodo che restituisce una stringa con le informazioni dell'acquisto
    def __str__(self) -> str:
        return (f"{self._data} | {self._strumento.get('nome')} x{self._quantita} | {self.getTotale():.2f} €")

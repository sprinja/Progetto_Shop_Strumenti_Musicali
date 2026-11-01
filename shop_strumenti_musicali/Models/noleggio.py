from datetime import date, timedelta
from Models import Compratore

class Noleggio:
    # costruttore
    def __init__(self, id: str, compratore: Compratore, strumento: dict, quantita: int, durata_giorni: int, data_inizio: str = None, data_restituzione: str = None):
        if not isinstance(compratore, Compratore):  # se compratore non è un oggetto Compratore, errore
            raise TypeError("compratore deve essere un Compratore")
        if int(quantita) <= 0:  # se quantita è negativa o zero, errore
            raise ValueError("la quantita' noleggiata deve essere positiva")
        if int(durata_giorni) < 1:  # se durata_giorni è minore di 1, errore
            raise ValueError("la durata del noleggio deve essere di almeno 1 giorno")
        self._id = id
        self._compratore = compratore
        self._strumento = dict(strumento)
        self._quantita = int(quantita)
        self._durata_giorni = int(durata_giorni)
        self._data_inizio = data_inizio or str(date.today())
        self._data_restituzione = data_restituzione

    # metodi getter
    def getId(self) -> str:
        return self._id

    def getCompratore(self) -> Compratore:
        return self._compratore

    def getStrumento(self) -> dict:
        return self._strumento

    def getQuantita(self) -> int:
        return self._quantita

    def getDurata(self) -> int:
        return self._durata_giorni

    def getDataInizio(self) -> str:
        return self._data_inizio

    def getDataRestituzione(self) -> str:
        return self._data_restituzione

    def getDataFine(self) -> str:
        return str(date.fromisoformat(self._data_inizio) + timedelta(days=self._durata_giorni))

    def getTempoRimanente(self) -> int:
        return (date.fromisoformat(self.getDataFine()) - date.today()).days

    # metodi che verificano lo stato del noleggio
    def isAttivo(self) -> bool:
        return self._data_restituzione is None

    def isScaduto(self) -> bool:
        return self.isAttivo() and self.getTempoRimanente() <= 0

    # metodo che calcola il prezzo di noleggio giornaliero dello strumento
    def _prezzoGiornaliero(self) -> float:
        return float(self._strumento.get("prezzo_noleggio_giornaliero", 0.0))

    # metodo che calcola il numero di giorni effettivi del noleggio, considerando la data di restituzione
    def getGiorniEffettivi(self) -> int:
        if self._data_restituzione is None: # se il noleggio non è stato restituito, ritorna 0
            return 0
        giorni = (date.fromisoformat(self._data_restituzione) - date.fromisoformat(self._data_inizio)).days
        return max(1, min(giorni, self._durata_giorni)) # ritorna almeno 1 giorno e al massimo la durata del noleggio

    # metodo che calcola il costo massimo del noleggio, basato sul prezzo giornaliero e sulla durata inserita del noleggio
    def calcolaCostoMassimo(self) -> float:
        return round(self._prezzoGiornaliero() * self._durata_giorni, 2)

    # metodo che calcola il costo effettivo del noleggio, basato sul prezzo giornaliero e sui giorni effettivi del noleggio
    def calcolaCostoEffettivo(self) -> float:
        giorni = self.getGiorniEffettivi() or self._durata_giorni
        return round(self._prezzoGiornaliero() * giorni, 2)

    # metodo che calcola il rimborso dovuto al compratore, basato sulla differenza tra il costo massimo e il costo effettivo del noleggio
    def getRimborso(self) -> float:
        return round(self.calcolaCostoMassimo() - self.calcolaCostoEffettivo(), 2)

    # metodo che restituisce lo strumento noleggiato al venditore, impostando la data di restituzione e calcolando il rimborso dovuto al compratore
    def restituisciStrumento(self, data_restituzione: str = None) -> float:
        if not self.isAttivo(): # se il noleggio non è attivo, ritorna 0.0
            return 0.0
        self._data_restituzione = data_restituzione or str(date.today())    # se non viene fornita una data di restituzione, usa la data odierna
        return self.getRimborso()

    # metodo che restituisce un dizionario con le informazioni del noleggio
    def toDict(self) -> dict:
        return {
            "id": self._id,
            "compratore": self._compratore.getUsername(),
            "strumento": self._strumento,
            "quantita": self._quantita,
            "durata_giorni": self._durata_giorni,
            "data_inizio": self._data_inizio,
            "data_restituzione": self._data_restituzione
        }

    # metodo che crea un oggetto Noleggio a partire da un dizionario e un compratore
    @classmethod
    def fromDict(cls, d: dict, compratore: Compratore) -> "Noleggio":
        return cls(d["id"], compratore, d["strumento"], d["quantita"], d["durata_giorni"], d["data_inizio"], d.get("data_restituzione"))

    # metodo che restituisce una stringa con le informazioni del noleggio
    def __str__(self) -> str:
        if self.isAttivo(): # se il noleggio è attivo, mostra i giorni rimanenti
            stato = f"attivo, mancano {self.getTempoRimanente()} giorni"
        else:   # se il noleggio è terminato, mostra la data di restituzione
            stato = f"terminato il {self._data_restituzione}"
        return (f"{self._data_inizio} -> {self.getDataFine()} | {self._strumento.get('nome')} x{self._quantita} | {stato} | {self.calcolaCostoMassimo():.2f} €")
    
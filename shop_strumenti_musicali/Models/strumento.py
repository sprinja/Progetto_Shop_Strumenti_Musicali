from Models import CategoriaStrumento

class Strumento:
    #costruttore
    def __init__(self, id: str, nome: str, categoria: CategoriaStrumento, azienda: str, venditore: str, quantita: int, prezzo: float, nome_venditore: str = None, prezzo_noleggio_giornaliero=None):
        if not isinstance(categoria, CategoriaStrumento):   # se categoria non è un oggetto CategoriaStrumento, errore
            raise TypeError("categoria deve essere una CategoriaStrumento")
        if not isinstance(nome, str) or not nome.strip():   # se nome non è una stringa o è vuoto, errore
            raise ValueError("nome dello strumento obbligatorio")
        if int(quantita) < 0:   # se quantita è negativa, errore
            raise ValueError("la quantita' non puo' essere negativa")
        if float(prezzo) < 0:   # se prezzo è negativo, errore
            raise ValueError("il prezzo non puo' essere negativo")

        self._id = id
        self._nome = nome.strip()
        self._categoria = categoria
        self._azienda = azienda.strip()
        self._venditore = venditore
        self._nome_venditore = nome_venditore.strip() if nome_venditore else venditore
        self._quantita = int(quantita)
        self._prezzo = float(prezzo)

        if prezzo_noleggio_giornaliero is None: # se non viene fornito il prezzo di noleggio giornaliero, calcolalo automaticamente
            self._prezzo_noleggio_giornaliero = self._calcolaNoleggioGiornaliero()
        else:   # se viene fornito il prezzo di noleggio giornaliero, impostalo
            nol = float(str(prezzo_noleggio_giornaliero).replace(",", "."))
            if nol <= 0:    # se il prezzo di noleggio giornaliero è negativo o zero, errore
                raise ValueError("il prezzo di noleggio giornaliero deve essere positivo")
            self._prezzo_noleggio_giornaliero = round(nol, 2)

    # metodo che calcola il prezzo di noleggio giornaliero in base alla categoria dello strumento e al prezzo di vendita
    def _calcolaNoleggioGiornaliero(self) -> float:
        return self._categoria.stimaNoleggioGiornaliero(self._prezzo)

    # metodi getter
    def getId(self) -> str:
        return self._id

    def getNome(self) -> str:
        return self._nome

    def getCategoria(self) -> CategoriaStrumento:
        return self._categoria

    def getTipo(self) -> str:
        return self._categoria.getNomeTipo()

    def getAzienda(self) -> str:
        return self._azienda

    def getVenditore(self) -> str:
        return self._venditore

    def getNomeVenditore(self) -> str:
        return self._nome_venditore

    def getQuantita(self) -> int:
        return self._quantita

    def getPrezzo(self) -> float:
        return self._prezzo

    def getPrezzoNoleggioGiornaliero(self) -> float:
        return self._prezzo_noleggio_giornaliero

    # metodo che restituisce True se la quantità dello strumento è maggiore di 0, altrimenti False
    def isDisponibile(self) -> bool:
        return self._quantita > 0

    # metodi setter
    def setNome(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip(): # se nome non è una stringa o è vuoto, errore
            raise ValueError("nome dello strumento obbligatorio")
        self._nome = v.strip()

    def setCategoria(self, v: CategoriaStrumento) -> None:
        if not isinstance(v, CategoriaStrumento): # se categoria non è un oggetto CategoriaStrumento, errore
            raise TypeError("categoria deve essere una CategoriaStrumento")
        self._categoria = v

    def setAzienda(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip(): # se azienda non è una stringa o è vuoto, errore
            raise ValueError("azienda produttrice obbligatoria")
        self._azienda = v.strip()

    def setNomeVenditore(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip(): # se nome venditore non è una stringa o è vuoto, errore
            raise ValueError("nome del venditore obbligatorio")
        self._nome_venditore = v.strip()

    def setPrezzo(self, v) -> None:
        p = float(str(v).replace(",", ".")) # rende il prezzo un float, sostituendo eventuali virgole con punti
        if p < 0:   # se il prezzo è negativo, errore
            raise ValueError("il prezzo non puo' essere negativo")
        self._prezzo = p

    def setPrezzoNoleggioGiornaliero(self, v) -> None:
        try:
            nol = float(str(v).replace(",", "."))   # rende il prezzo di noleggio giornaliero un float, sostituendo eventuali virgole con punti
        except (TypeError, ValueError): # se il prezzo di noleggio giornaliero non è un numero, errore
            raise ValueError("il prezzo di noleggio giornaliero deve essere un numero")
        if nol <= 0:    # se il prezzo di noleggio giornaliero è negativo o zero, errore
            raise ValueError("il prezzo di noleggio giornaliero deve essere positivo")
        self._prezzo_noleggio_giornaliero = round(nol, 2)

    def setQuantita(self, v: int) -> None:
        q = int(v)  # rende la quantità un intero
        if q < 0:    # se la quantità è negativa, errore
            raise ValueError("la quantita' non puo' essere negativa")
        self._quantita = q

    # metodo che aggiorna la quantità dello strumento, aggiungendo o sottraendo un valore delta
    def aggiornaQuantita(self, delta: int) -> None:
        if self._quantita + int(delta) < 0: # se la quantità aggiornata è negativa, errore
            raise ValueError("quantita' insufficiente")
        self._quantita += int(delta)

    # metodo che restituisce un dizionario con le informazioni dello strumento
    def toDict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "tipo": self._categoria.getNomeTipo(),
            "azienda": self._azienda,
            "venditore": self._venditore,
            "nome_venditore": self._nome_venditore,
            "quantita": self._quantita,
            "prezzo": self._prezzo,
            "prezzo_noleggio_giornaliero": self._prezzo_noleggio_giornaliero
        }

    # metodo che crea un oggetto Strumento a partire da un dizionario e una categoria
    @classmethod
    def fromDict(cls, d: dict, categoria: CategoriaStrumento) -> "Strumento":
        return cls(d["id"], d["nome"], categoria, d["azienda"],
                   d["venditore"], d["quantita"], d["prezzo"],
                   d.get("nome_venditore"),
                   d.get("prezzo_noleggio_giornaliero"))

    # metodo che restituisce una stringa con le informazioni dello strumento
    def __str__(self) -> str:
        return (f"{self._id} | {self._nome} | tipo: {self._categoria.getNomeTipo()} | azienda: {self._azienda} | venditore: {self._nome_venditore} | q: {self._quantita} | {self._prezzo:.2f} € | noleggio {self._prezzo_noleggio_giornaliero:.2f} €/giorno")
    
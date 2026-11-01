class CategoriaStrumento:
    QUOTA_NOLEGGIO_DEFAULT = 0.1    # quota di noleggio giornaliero di default (10% del prezzo dello strumento)

    # costruttore
    def __init__(self, nome_tipo: str, quota_noleggio: float = QUOTA_NOLEGGIO_DEFAULT):
        if not isinstance(nome_tipo, str) or not nome_tipo.strip(): # se nome_tipo non è una stringa o è vuoto, errore
            raise ValueError("il tipo di strumento non puo' essere vuoto")
        if not isinstance(quota_noleggio, (int, float)) or quota_noleggio <= 0: # se quota_noleggio non è un numero positivo, errore
            raise TypeError("quota_noleggio deve essere un numero positivo")
        self._nome_tipo = nome_tipo.strip().lower() # rende il nome del tipo di strumento minuscolo e senza spazi iniziali o finali
        self._quota_noleggio = float(quota_noleggio)

    # metodi getter
    def getNomeTipo(self) -> str:
        return self._nome_tipo

    def getQuotaNoleggio(self) -> float:
        return self._quota_noleggio

    # metodi setter
    def setQuotaNoleggio(self, v: float) -> None:
        if not isinstance(v, (int, float)) or v <= 0:   # se v non è un numero positivo, errore
            raise TypeError("quota_noleggio deve essere un numero positivo")
        self._quota_noleggio = float(v)

    # metodo che stima il prezzo di noleggio giornaliero in base al prezzo dello strumento e alla quota di noleggio
    def stimaNoleggioGiornaliero(self, prezzo) -> float:
        return round(float(prezzo) * self._quota_noleggio, 2)   # arrotonda il prezzo di noleggio giornaliero a 2 decimali

    # metodo che restituisce un dizionario con le informazioni della categoria dello strumento
    def toDict(self) -> dict:
        return {
            "nome_tipo": self._nome_tipo,
            "quota_noleggio": self._quota_noleggio
        }

    # metodo che crea un oggetto CategoriaStrumento a partire da un dizionario
    @classmethod
    def fromDict(cls, d: dict) -> "CategoriaStrumento":
        return cls(d["nome_tipo"], d.get("quota_noleggio", cls.QUOTA_NOLEGGIO_DEFAULT))

    # metodo che restituisce una stringa con le informazioni della categoria dello strumento
    def __str__(self) -> str:
        return f"{self._nome_tipo} (noleggio {self._quota_noleggio * 100:.2f}%/giorno)"
from Models import Utente

# classe Venditore figlia della classe Utente
class Venditore(Utente):
    TIPO_UTENTE = "Venditore"

    # costruttore
    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    # metodo che crea un oggetto Venditore a partire da un dizionario
    @classmethod
    def fromDict(cls, d: dict) -> "Venditore":
        return cls(d["username"], d["password"])

    # metodo che restituisce una rappresentazione in stringa dell'oggetto
    def __str__(self) -> str:
        return f"Venditore {self.getUsername()}"

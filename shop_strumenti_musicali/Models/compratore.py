from Models import Utente

# classe Compratore figlia della classe Utente
class Compratore(Utente):
    TIPO_UTENTE = "Compratore"

    # costruttore
    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    # metodo che crea un oggetto Compratore a partire da un dizionario
    @classmethod
    def fromDict(cls, d: dict) -> "Compratore":
        return cls(d["username"], d["password"])

    # metodo che restituisce una rappresentazione in stringa dell'oggetto
    def __str__(self) -> str:
        return f"Compratore {self.getUsername()}"

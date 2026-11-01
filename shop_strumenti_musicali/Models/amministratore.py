from Models import Utente

# classe amministratore figlia della classe utente
class Amministratore(Utente):
    TIPO_UTENTE = "Amministratore"

    # costruttore
    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    # metodo che crea un oggetto Amministratore a partire da un dizionario
    @classmethod
    def fromDict(cls, d: dict) -> "Amministratore":
        return cls(d["username"], d["password"])

    # metodo che restituisce una rappresentazione in stringa dell'oggetto
    def __str__(self) -> str:
        return f"Amministratore {self.getUsername()}"

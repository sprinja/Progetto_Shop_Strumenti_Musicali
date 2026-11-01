class Utente:
    TIPO_UTENTE = "Utente"

    # costruttore
    def __init__(self, username: str, password: str):
        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("username e password devono essere stringhe")
        self._username = username.strip()
        self._password = password
        self._tipoUtente = self.TIPO_UTENTE

    # metodi getter
    def getUsername(self) -> str:
        return self._username

    def getTipoUtente(self) -> str:
        return self._tipoUtente

    def getPassword(self) -> str:
        return self._password

    # metodi setter
    def setUsername(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("username non valido")
        self._username = v.strip()

    def setPassword(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("password non valida")
        self._password = v

    # metodo per verificare se le credenziali sono corrette
    def credenzialiCorrette(self, username: str, password: str) -> bool:
        return self._username == username.strip() and self._password == password

    # metodo per convertire l'oggetto in un dizionario
    def toDict(self) -> dict:
        return {
            "username": self._username,
            "password": self._password
        }

    # metodo per creare un oggetto Utente a partire da un dizionario
    @classmethod
    def fromDict(cls, d: dict) -> "Utente":
        return cls(d["username"], d["password"])

    # metodo che restituisce una rappresentazione in stringa dell'oggetto
    def __str__(self) -> str:
        return f"{self._username}"

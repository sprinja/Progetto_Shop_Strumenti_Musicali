from Views.vista_accesso import VistaAccesso
from Views.vista_finestra_compratore import VistaFinestraCompratore
from Views.vista_finestra_venditore import VistaFinestraVenditore
from Views.vista_finestra_amministratore import VistaFinestraAmministratore

class Applicazione:
    # costruttore
    def __init__(self, app, gestori: dict, intervallo_timer: int = 10_000):
        self._app = app
        self._gestori = gestori
        self._intervallo_timer = intervallo_timer
        self._vista = None

    # metodo per aprire una nuova vista
    def apri(self, tipo: str, utente=None):
        if tipo == "accesso":   # se il tipo è accesso, crea una nuova vista accesso
            nuova = VistaAccesso(self._gestori["utenti"], self._gestori["amministratore"], self.apri)
        elif tipo == "compratore":  # se il tipo è compratore, crea una nuova vista finestra compratore
            nuova = VistaFinestraCompratore(utente, self._gestori["catalogo"], self._gestori["acquisti"], self._gestori["noleggi"], self.apri, intervallo_timer=self._intervallo_timer)
        elif tipo == "venditore":   # se il tipo è venditore, crea una nuova vista finestra venditore
            nuova = VistaFinestraVenditore(utente, self._gestori["catalogo"], self._gestori["acquisti"], self._gestori["noleggi"], self.apri, intervallo_timer=self._intervallo_timer)
        elif tipo == "amministratore":  # se il tipo è amministratore, crea una nuova vista finestra amministratore
            nuova = VistaFinestraAmministratore(utente, self._gestori["amministratore"], self.apri, self._gestori["noleggi"], self._intervallo_timer)
        else:   # se non è un tipo valido, errore
            raise ValueError(f"tipo di pagina sconosciuto: {tipo}")
        for w in self._app.topLevelWidgets():   # chiude la finestra aperta in precedenza e anche ogni finestra secondaria rimasta aperta, per non lasciarne attive con la vecchia sessione
            if w is not nuova:
                w.close()
        self._vista = nuova
        self._vista.show()  # mostra la nuova vista

    # metodo per eseguire l'applicazione
    def esegui(self) -> int:
        self.apri("accesso")
        return self._app.exec_()

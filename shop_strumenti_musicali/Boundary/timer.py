import threading
import time

class Timer:
    # costruttore
    def __init__(self, azione_da_eseguire, intervallo_secondi=60):
        self._azione = azione_da_eseguire
        self._intervallo = intervallo_secondi
        self._attivo = False
        self._thread = None

    # metodo per avviare il timer in un thread separato
    def avvia(self):
        if not self._attivo:    # se il timer non è già attivo, lo avvia in un thread separato
            self._attivo = True
            self._thread = threading.Thread(target=self._loop, daemon=True)   # crea il thread che esegue il loop del timer
            self._thread.start()

    # metodo per fermare il timer
    def ferma(self):
        self._attivo = False    # disattiva il timer, così il loop si ferma al prossimo ciclo

    # metodo per il loop del timer, chiama l'azione da eseguire ogni intervallo di secondi
    def _loop(self):
        while self._attivo: # ciclo per eseguire l'azione finché il timer è attivo
            time.sleep(self._intervallo)    # aspetta l'intervallo di secondi tra un'esecuzione e la successiva
            if self._attivo:    # se il timer è ancora attivo dopo l'attesa, esegue l'azione
                try:
                    self._azione()  # chiama l'azione da eseguire (la verifica delle scadenze dei noleggi)
                except Exception as e:  # se l'azione genera un errore, lo stampa senza far fermare il timer
                    print(f"[Timer] Errore: {e}")

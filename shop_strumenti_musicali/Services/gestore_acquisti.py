from Models import Acquisto
from Repos import StrumentoRepository, CompratoreRepository, AcquistoRepository

class GestoreAcquisti:
    # costruttore
    def __init__(self, strumento_repo: StrumentoRepository, compratore_repo: CompratoreRepository, acquisto_repo: AcquistoRepository):
        self._strumento_repo = strumento_repo
        self._compratore_repo = compratore_repo
        self._acquisto_repo = acquisto_repo

    # effettua un acquisto
    def effettuaAcquisto(self, id_compratore: str, id_strumento: str, quantita) -> str:
        compratore = self._compratore_repo.trovaPerUsername(id_compratore)    # trova il compratore corrispondente all'id fornito
        if compratore is None:  # se non esiste un compratore con l'id fornito, errore
            return "Errore: compratore non trovato"
        strumento = self._strumento_repo.trovaPerId(id_strumento)   # trova lo strumento corrispondente all'id fornito
        if strumento is None:   # se non esiste uno strumento con l'id fornito, errore
            return "Errore: strumento non trovato"
        try:
            q = int(quantita)   # converte la quantita in un numero intero
        except (TypeError, ValueError): # se la quantita non è un numero intero, errore
            return "Errore: quantita' non valida"
        if q <= 0:  # se la quantita è minore o uguale a zero, errore
            return "Errore: la quantita' deve essere maggiore di zero"
        if strumento.getQuantita() < q: # se la quantita richiesta è maggiore della quantita disponibile dello strumento, errore
            return (f"Errore: quantita' non disponibile (disponibili {strumento.getQuantita()})")
        temp = strumento.toDict()   # crea un dizionario con le informazioni dello strumento al momento dell'acquisto
        strumento.aggiornaQuantita(-q)  # aggiorna la quantita dello strumento sottraendo la quantita acquistata
        if strumento.getQuantita() == 0:    # se la quantita dello strumento è zero, rimuove lo strumento dalla repository
            self._strumento_repo.rimuovi(strumento.getId())
        else:   # se la quantita dello strumento è maggiore di zero, salva le modifiche alla repository
            self._strumento_repo.salva()
        acquisto = Acquisto(self._acquisto_repo.nuovoId(), compratore, temp, q) # crea un oggetto Acquisto con le informazioni dell'acquisto
        self._acquisto_repo.aggiungi(acquisto)  # aggiunge l'acquisto alla repository
        return f"Acquisto completato: {acquisto}"

    # elenca tutti gli acquisti di un compratore
    def cronologiaAcquisti(self, id_compratore: str) -> list:
        return self._acquisto_repo.perCompratore(id_compratore)

    # elenca tutti gli acquisti di un venditore
    def venditeDelVenditore(self, id_venditore: str) -> list:
        return self._acquisto_repo.perVenditore(id_venditore)

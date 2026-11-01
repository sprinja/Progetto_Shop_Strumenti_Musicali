import sys
from PyQt5.QtWidgets import QApplication
from Repos import (CompratoreRepository, VenditoreRepository, AmministratoreRepository, CategoriaRepository, StrumentoRepository, AcquistoRepository, NoleggioRepository)
from Services import (GestoreUtenti, GestoreCatalogo, GestoreAcquisti, GestoreNoleggi, GestoreAmministratore)
from Views import Applicazione

def main():
    # costruisce il sistema
    compratori = CompratoreRepository("data/compratori.json")
    venditori = VenditoreRepository("data/venditori.json")
    amministratori = AmministratoreRepository("data/amministratori.json")
    categorie = CategoriaRepository("data/categorie.json")
    strumenti = StrumentoRepository("data/strumenti.json", categorie)
    acquisti = AcquistoRepository("data/acquisti.json", compratori)
    noleggi = NoleggioRepository("data/noleggi.json", compratori)
    gestore_utenti = GestoreUtenti(compratori, venditori)
    gestore_catalogo = GestoreCatalogo(strumenti, categorie)
    gestore_acquisti = GestoreAcquisti(strumenti, compratori, acquisti)
    gestore_noleggi = GestoreNoleggi(strumenti, categorie, compratori, noleggi)
    gestore_amministratore = GestoreAmministratore(amministratori, compratori, venditori, strumenti, acquisti, noleggi, gestore_noleggi)
    gestori = {
        "utenti": gestore_utenti,
        "catalogo": gestore_catalogo,
        "acquisti": gestore_acquisti,
        "noleggi": gestore_noleggi,
        "amministratore": gestore_amministratore
    }
    app = QApplication(sys.argv)
    applicazione = Applicazione(app, gestori, intervallo_timer=60_000)
    sys.exit(applicazione.esegui())

if __name__ == "__main__":
    main()
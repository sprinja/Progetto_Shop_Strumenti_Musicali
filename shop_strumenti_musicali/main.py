import os
import sys
from PyQt5.QtWidgets import QApplication
from Repos import (CompratoreRepository, VenditoreRepository, AmministratoreRepository, CategoriaRepository, StrumentoRepository, AcquistoRepository, NoleggioRepository)
from Services import (GestoreUtenti, GestoreCatalogo, GestoreAcquisti, GestoreNoleggi, GestoreAmministratore)
from Views import Applicazione

def main():
    # costruisce il sistema
    cartella = os.path.dirname(os.path.abspath(__file__))
    compratori = CompratoreRepository(os.path.join(cartella, "data", "compratori.json"))
    venditori = VenditoreRepository(os.path.join(cartella, "data", "venditori.json"))
    amministratori = AmministratoreRepository(os.path.join(cartella, "data", "amministratori.json"))
    categorie = CategoriaRepository(os.path.join(cartella, "data", "categorie.json"))
    strumenti = StrumentoRepository(os.path.join(cartella, "data", "strumenti.json"), categorie)
    acquisti = AcquistoRepository(os.path.join(cartella, "data", "acquisti.json"), compratori)
    noleggi = NoleggioRepository(os.path.join(cartella, "data", "noleggi.json"), compratori)
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
import os
from Repos import (CompratoreRepository, VenditoreRepository, AmministratoreRepository, CategoriaRepository, StrumentoRepository, AcquistoRepository, NoleggioRepository)
from Services import (GestoreUtenti, GestoreCatalogo, GestoreAcquisti, GestoreNoleggi, GestoreAmministratore)
from Boundary import (BoundaryAccesso, BoundaryCompratore, BoundaryVenditore, BoundaryAmministratore, Timer)
from Boundary.utilita import chiama

INTERVALLO_TIMER = 60

def main():
    print("Avvio")

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
    boundary_accesso = BoundaryAccesso(gestore_utenti, gestore_amministratore)

    def verifica_scadenze_noleggi():
        for esito in chiama(gestore_noleggi.verificaScadenze):
            print(f"\n[Timer] {esito}")

    # Avvio timer
    timer_noleggi = Timer(azione_da_eseguire=verifica_scadenze_noleggi, intervallo_secondi=INTERVALLO_TIMER)
    timer_noleggi.avvia()
    print(f"[Timer] attore Tempo avviato: le scadenze dei noleggi vengono verificate ogni {INTERVALLO_TIMER} secondi")

    try:
        while True:
            # Registrazione o autenticazione utente
            utente_autenticato = None
            while utente_autenticato is None:
                esito = boundary_accesso.form_accesso()
                if esito is None:
                    print("Chiusura in corso...")
                    return
                tipo, utente_autenticato = esito
                if tipo == "Compratore":
                    pagina = BoundaryCompratore(gestore_catalogo, gestore_acquisti, gestore_noleggi, utente_autenticato)
                elif tipo == "Venditore":
                    pagina = BoundaryVenditore(gestore_catalogo, gestore_acquisti, gestore_noleggi, utente_autenticato)
                else:
                    pagina = BoundaryAmministratore(gestore_amministratore)

            while True:
                print("\n=======================================================")
                print("Schermata principale. Inserisci un comando:")
                if tipo == "Compratore":
                    print("Comandi disponibili: \n'shop' (gestione strumenti)\n'cronologia' (acquisti e noleggi)\n'cambia account' \n'esci'")
                elif tipo == "Venditore":
                    print("Comandi disponibili: \n'catalogo' (i tuoi strumenti) \n'attivita' (vendite e noleggi)\n'cambia account' \n'esci'")
                else:
                    print("Comandi disponibili: \n'utenti' (gestione utenti)\n'catalogo' (gestione strumenti)\n'cambia account' \n'esci'")
                print("=======================================================\n")
                comando = input("Inserisci comando> ").strip().lower()
                if comando == "esci":
                    print("Chiusura in corso...")
                    return
                elif comando == "cambia account":
                    break
                elif tipo == "Compratore" and comando == "shop":
                    pagina.menu_compratore()
                elif tipo == "Compratore" and comando == "cronologia":
                    pagina.menu_cronologia()
                elif tipo == "Venditore" and comando == "catalogo":
                    pagina.menu_catalogo()
                elif tipo == "Venditore" and comando == "attivita":
                    pagina.menu_attivita()
                elif tipo == "Amministratore" and comando == "utenti":
                    pagina.menu_utenti()
                elif tipo == "Amministratore" and comando == "catalogo":
                    pagina.menu_catalogo()
                else:
                    print(f"Comando '{comando}' non riconosciuto.")
    except (EOFError, KeyboardInterrupt):
        print("\nChiusura in corso...")
    finally:
        timer_noleggi.ferma()

if __name__ == "__main__":
    main()

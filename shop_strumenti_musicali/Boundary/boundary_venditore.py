from Services import GestoreCatalogo, GestoreAcquisti, GestoreNoleggi
from Boundary.utilita import (chiama, aDecimale, chiediIntero, chiediDecimale, stampaElenco, stampaStrumenti, scegliStrumento)

class BoundaryVenditore:
    # costruttore
    def __init__(self, gestore_catalogo: GestoreCatalogo, gestore_acquisti: GestoreAcquisti, gestore_noleggi: GestoreNoleggi, venditore):
        self._gestore_catalogo = gestore_catalogo
        self._gestore_acquisti = gestore_acquisti
        self._gestore_noleggi = gestore_noleggi
        self._venditore = venditore
        self._criterio = ""
        self._valore = ""

    # metodo per il menu del catalogo del venditore
    def menu_catalogo(self):
        while True:    # ciclo per mostrare il menu finché l'utente non sceglie di tornare indietro
            print("\n=======================================================")
            print(f" Pagina Venditore - {self._venditore.getUsername()}")
            print("=======================================================")
            if self._valore:    # se c'è una ricerca in corso, mostra e cerca i risultati della ricerca
                print(f"Risultati della ricerca ({self._criterio}: {self._valore})")
                strumenti = chiama(self._gestore_catalogo.cercaStrumenti, self._criterio, self._valore, self._venditore.getUsername())    # chiama il metodo del gestore catalogo per cercare i tuoi strumenti con la ricerca in corso
            else:   # altrimenti, elenca tutti i tuoi strumenti in vendita
                print("Questi sono i tuoi strumenti in vendita:")
                strumenti = chiama(self._gestore_catalogo.elencaStrumenti, id_venditore=self._venditore.getUsername())    # chiama il metodo del gestore catalogo per elencare i tuoi strumenti
            stampaStrumenti(strumenti)  # stampa l'elenco degli strumenti trovati
            print("\nComandi disponibili: \n'cerca' \n'azzera' \n'tipo' (inserisci nuovo tipo) \n'aggiungi' (nuovo strumento) \n'modifica' \n'rimuovi' \n'indietro'")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()    # legge il comando inserito dall'utente e lo converte in minuscolo
            if comando == "indietro":    # se l'utente sceglie di tornare indietro, esce dal menu
                return
            elif comando == "cerca":    # se l'utente sceglie di cercare, chiama il metodo form_cerca
                self.form_cerca()
            elif comando == "azzera":   # se l'utente sceglie di azzerare la ricerca, azzera criterio e valore
                self._criterio = ""
                self._valore = ""
            elif comando == "tipo":    # se l'utente sceglie di inserire un nuovo tipo, chiama il metodo form_inserisci_tipo
                self.form_inserisci_tipo()
            elif comando == "aggiungi":    # se l'utente sceglie di aggiungere uno strumento, chiama il metodo form_aggiungi_strumento
                self.form_aggiungi_strumento()
            elif comando == "modifica":    # se l'utente sceglie di modificare uno strumento, chiama il metodo form_modifica_strumento
                self.form_modifica_strumento(strumenti)
            elif comando == "rimuovi":    # se l'utente sceglie di rimuovere uno strumento, chiama il metodo form_rimuovi_strumento
                self.form_rimuovi_strumento(strumenti)
            else:   # se l'utente inserisce un comando non valido, stampa un messaggio di errore
                print(f"Comando '{comando}' non riconosciuto.")

    # metodo per la ricerca dei tuoi strumenti
    def form_cerca(self):
        print("Criteri di ricerca disponibili: " + ", ".join(f"'{i}'" for i in GestoreCatalogo.CRITERI_RICERCA))    # stampa i criteri di ricerca disponibili
        while True:    # ciclo per chiedere all'utente il criterio di ricerca finché non inserisce un criterio valido
            criterio = input("Cerca per> ").strip().lower()    # legge il criterio di ricerca inserito dall'utente e lo converte in minuscolo
            if criterio in GestoreCatalogo.CRITERI_RICERCA:    # se il criterio è valido, esce dal ciclo
                break
            print(f"Criterio '{criterio}' non valido.")    # se il criterio non è valido, stampa un messaggio di errore
        valore = input("Valore da cercare> ").strip()    # legge il valore da cercare inserito dall'utente
        if valore and criterio == "prezzo" and aDecimale(valore) is None:    # se il criterio è il prezzo e il valore non è un numero, stampa un messaggio di errore e azzera il valore
            print("Nel campo 'prezzo massimo' devi scrivere un numero (es. 450.50), senza lettere")
            valore = ""
        if valore and not chiama(self._gestore_catalogo.cercaStrumenti, criterio, valore, self._venditore.getUsername()):    # se il valore è stato inserito ma non è stato trovato nessuno strumento, entra nel blocco
            print("Non e' stato trovato nessuno strumento con queste caratteristiche")    # stampa un messaggio di errore
        self._criterio = criterio    # salva il criterio della ricerca
        self._valore = valore    # salva il valore della ricerca

    # metodo per l'inserimento di un nuovo tipo di strumento
    def form_inserisci_tipo(self):
        print("Tipi gia' presenti nello shop:")
        stampaElenco(chiama(self._gestore_catalogo.elencaTipi), "Nessun tipo presente")    # chiama il metodo del gestore catalogo per elencare i tipi presenti e stampa l'elenco
        nome = input("Nuovo tipo di strumento (vuoto per annullare)> ").strip()    # legge il nome del nuovo tipo inserito dall'utente
        if not nome:    # se il nome non è stato inserito, esce dal metodo
            return
        quota = chiediDecimale("Quota di noleggio (% del prezzo al giorno) [10]> ", minimo=0.01, predefinito=10.0)    # chiede all'utente la quota di noleggio in percentuale sul prezzo al giorno
        print(chiama(self._gestore_catalogo.inserisciTipo, nome, quota / 100))    # chiama il metodo del gestore catalogo per inserire il nuovo tipo e stampa l'esito

    # metodo per l'aggiunta di un nuovo strumento al catalogo
    def form_aggiungi_strumento(self):
        print("Tipi gia' presenti nello shop (quota di noleggio):")
        stampaElenco(chiama(self._gestore_catalogo.elencaTipi), "Nessun tipo presente")    # chiama il metodo del gestore catalogo per elencare i tipi presenti e stampa l'elenco
        tipo = input("Tipo dello strumento (vuoto per annullare)> ").strip()    # legge il tipo dello strumento inserito dall'utente
        if not tipo:    # se il tipo non è stato inserito, esce dal metodo
            return
        categoria = chiama(self._gestore_catalogo.trovaTipo, tipo)    # chiama il metodo del gestore catalogo per trovare la categoria del tipo inserito
        if categoria is None:   # se il tipo inserito non esiste, stampa un messaggio di errore ed esce dal metodo
            print(f"Errore: non esiste il tipo inserito ('{tipo}'). Crealo prima con 'tipo'.")
            return
        nome = input("Nome dello strumento> ").strip()    # legge il nome dello strumento inserito dall'utente
        azienda = input("Azienda produttrice> ").strip()  # legge l'azienda produttrice inserita dall'utente
        quantita = chiediIntero("Quantita'> ", minimo=1)    # chiede all'utente la quantità di strumenti da mettere in vendita
        prezzo = chiediDecimale("Prezzo (es. 450.50)> ", minimo=0.01)    # chiede all'utente il prezzo dello strumento
        stima = categoria.stimaNoleggioGiornaliero(prezzo)    # calcola la stima del prezzo di noleggio giornaliero con la quota della categoria
        print(f"Stima noleggio giornaliero ({categoria.getQuotaNoleggio() * 100:g}% del prezzo): {stima:.2f} €/giorno")    # stampa la stima del prezzo di noleggio giornaliero
        prezzo_noleggio = input(f"Prezzo di noleggio giornaliero [predefinito {stima:.2f}]> ").strip()    # legge il prezzo di noleggio giornaliero inserito dall'utente
        if not prezzo_noleggio:    # se l'utente non inserisce nessun prezzo, usa la stima calcolata
            prezzo_noleggio = stima
        print(chiama(self._gestore_catalogo.aggiungiStrumento, nome, tipo, azienda, quantita, prezzo, self._venditore.getUsername(), None, prezzo_noleggio))    # chiama il metodo del gestore catalogo per aggiungere lo strumento e stampa l'esito

    # metodo per la modifica di una caratteristica dello strumento selezionato
    def form_modifica_strumento(self, strumenti):
        scelta = scegliStrumento(strumenti)  # chiede all'utente di scegliere uno strumento tra quelli disponibili
        if scelta is None:   # se l'utente non sceglie nessuno strumento, esce dal metodo
            return
        print(f"Strumento selezionato:\n  {scelta}")
        caratteristiche = ("nome", "azienda", "tipo", "prezzo", "prezzo_noleggio", "quantita")
        print("Caratteristiche modificabili: " + ", ".join(f"'{i}'" for i in caratteristiche))    # stampa le caratteristiche modificabili
        while True:    # ciclo per chiedere all'utente la caratteristica da modificare finché non ne sceglie una valida
            car = input("Caratteristica da modificare> ").strip().lower()    # legge la caratteristica da modificare inserita dall'utente e la converte in minuscolo
            if car in caratteristiche:    # se la caratteristica è valida, esce dal ciclo
                break
            print(f"Caratteristica '{car}' non modificabile.")    # se la caratteristica non è valida, stampa un messaggio di errore
        if car in ("prezzo", "prezzo_noleggio"):    # se la caratteristica è il prezzo o il prezzo di noleggio, chiede un numero decimale
            valore = chiediDecimale("Nuovo valore> ", minimo=0.01)
        elif car == "quantita":    # se la caratteristica è la quantità, chiede un numero intero
            valore = chiediIntero("Nuovo valore> ", minimo=0)
        elif car == "tipo":    # se la caratteristica è il tipo, mostra i tipi presenti e chiede il nuovo tipo
            print("Tipi gia' presenti nello shop:")
            stampaElenco(chiama(self._gestore_catalogo.elencaTipi), "Nessun tipo presente")    # chiama il metodo del gestore catalogo per elencare i tipi presenti e stampa l'elenco
            valore = input("Nuovo tipo> ").strip()
        else:   # altrimenti, chiede il nuovo valore come testo
            valore = input("Nuovo valore> ").strip()
        print(chiama(self._gestore_catalogo.modificaStrumento, scelta.getId(), car, valore))    # chiama il metodo del gestore catalogo per modificare la caratteristica e stampa l'esito

    # metodo per la rimozione di uno strumento dal catalogo
    def form_rimuovi_strumento(self, strumenti):
        scelta = scegliStrumento(strumenti)  # chiede all'utente di scegliere uno strumento tra quelli disponibili
        if scelta is None:   # se l'utente non sceglie nessuno strumento, esce dal metodo
            return
        print(chiama(self._gestore_catalogo.rimuoviStrumento, scelta.getId(), self._venditore.getUsername()))    # chiama il metodo del gestore catalogo per rimuovere lo strumento e stampa l'esito

    # metodo per il menu delle attività dei tuoi strumenti
    def menu_attivita(self):
        while True:    # ciclo per mostrare il menu finché l'utente non sceglie di tornare indietro
            print("\n=======================================================")
            print(f" Attivita' dei tuoi strumenti - {self._venditore.getUsername()}")
            print("=======================================================")
            print("Comandi disponibili: \n'vendite' \n'noleggi' \n'indietro'")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()    # legge il comando inserito dall'utente e lo converte in minuscolo
            if comando == "indietro":    # se l'utente sceglie di tornare indietro, esce dal menu
                return
            elif comando == "vendite":  # se l'utente sceglie di vedere le vendite, stampa la cronologia delle vendite
                print("Vendite dei tuoi strumenti:")
                vendite = chiama(self._gestore_acquisti.venditeDelVenditore, self._venditore.getUsername())    # chiama il metodo del gestore acquisti per elencare le vendite dei tuoi strumenti
                if not vendite: # se non ci sono vendite, stampa il messaggio per la cronologia vuota
                    print("  Cronologia vuota")
                for i in vendite:    # ciclo per stampare ogni vendita con strumento, quantità, data, compratore e totale
                    print(f"  {i.getStrumento().get('nome')} x{i.getQuantita()} - {i.getData()} - compratore: {i.getCompratore().getUsername()} - {i.getTotale():.2f} €")
            elif comando == "noleggi":   # se l'utente sceglie di vedere i noleggi, stampa la cronologia dei noleggi
                print("Noleggi dei tuoi strumenti:")
                noleggi = chiama(self._gestore_noleggi.noleggiDelVenditore, self._venditore.getUsername())    # chiama il metodo del gestore noleggi per elencare i noleggi dei tuoi strumenti
                if not noleggi: # se non ci sono noleggi, stampa il messaggio per la cronologia vuota
                    print("  Cronologia vuota")
                for i in noleggi:    # ciclo per stampare ogni noleggio con strumento, quantità e periodo
                    print(f"  {i.getStrumento().get('nome')} x{i.getQuantita()} - dal {i.getDataInizio()} al {i.getDataFine()} - compratore: {i.getCompratore().getUsername()}")
            else:   # se l'utente inserisce un comando non valido, stampa un messaggio di errore
                print(f"Comando '{comando}' non riconosciuto.")

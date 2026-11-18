from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QMessageBox)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QTimer
from Services import GestoreCatalogo, GestoreAcquisti, GestoreNoleggi
from Models import Venditore
from Views.validazione_campi import controllaNumero, numeroValido
from Views.vista_aggiungi_strumento import VistaAggiungiStrumento
from Views.vista_modifica_strumento import VistaModificaStrumento
from Views.vista_inserisci_tipo import VistaInserisciTipoStrumento

class VistaFinestraVenditore(QWidget):
    # costruttore
    def __init__(self, venditore: Venditore, gestore_catalogo: GestoreCatalogo, gestore_acquisti: GestoreAcquisti, gestore_noleggi: GestoreNoleggi, apri_finestra, intervallo_timer: int = 60_000):
        super().__init__()
        self._venditore = venditore
        self._catalogo = gestore_catalogo
        self._acquisti = gestore_acquisti
        self._noleggi = gestore_noleggi
        self._apri = apri_finestra
        self._intervallo_timer = intervallo_timer
        self._strumenti = []
        self._vista_corrente = None
        self.setWindowTitle(f"Pagina Venditore - {venditore.getUsername()}")
        self.resize(1150, 850)
        self._buildUI()
        self._connectSegnali()
        self._avviaTimer()
        self.update_ui()

    # metodo per costruire l'interfaccia grafica della finestra del venditore
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Benvenuto {self._venditore.getUsername()}. Questi sono i tuoi strumenti in vendita:"))   # etichetta per visualizzare il messaggio di benvenuto
        rigaRicerca = QHBoxLayout() # layout per la riga contenente il menù a tendina per la ricerca e il campo di testo
        rigaRicerca.addWidget(QLabel("Cerca per:"))
        self.combo_caratteristica_ricerca = QComboBox()   # menù a tendina per scegliere la caratteristica per cui cercare
        self.combo_caratteristica_ricerca.addItems(["tipo", "prezzo massimo", "azienda", "nome"])
        rigaRicerca.addWidget(self.combo_caratteristica_ricerca)
        self.txt_ricerca = QLineEdit()   # campo di testo per inserire il valore da cercare
        self.txt_ricerca.setPlaceholderText("es. chitarra")  # esempio di valore di ricerca valido
        rigaRicerca.addWidget(self.txt_ricerca)
        self.btn_cerca = QPushButton("Cerca")
        self.btn_azzera = QPushButton("Azzera")
        rigaRicerca.addWidget(self.btn_cerca)
        rigaRicerca.addWidget(self.btn_azzera)
        layout.addLayout(rigaRicerca)    # aggiunge la riga di ricerca al layout principale
        layout.addWidget(QLabel("I miei strumenti:"))
        self.list_miei_strumenti = QListWidget()    # lista per visualizzare i tuoi strumenti in vendita
        layout.addWidget(self.list_miei_strumenti)  # aggiunge la lista dei tuoi strumenti al layout principale
        pulsanti = QHBoxLayout()   # layout per i pulsanti per le azioni possibili sullo shop
        self.button_aggiungi_strumento = QPushButton("Aggiungi strumento")
        self.button_modifica_strumento = QPushButton("Modifica strumento")
        self.button_rimuovi_strumento = QPushButton("Rimuovi strumento")
        self.button_inserisci_tipo = QPushButton("Inserisci nuovo tipo")
        self.button_cambia_account = QPushButton("Cambia account")
        for i in (self.button_aggiungi_strumento, self.button_modifica_strumento, self.button_rimuovi_strumento, self.button_inserisci_tipo, self.button_cambia_account):    # ciclo per aggiungere ogni pulsante al layout della riga dei pulsanti
            pulsanti.addWidget(i)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        layout.addWidget(QLabel("Cronologia:"))
        cronologia = QHBoxLayout()  # layout per la cronologia contenente le colonne delle vendite e dei noleggi
        colonnaVendite = QVBoxLayout()  # layout per la colonna della cronologia delle vendite
        colonnaVendite.addWidget(QLabel("Le tue vendite:"))
        self.list_vendite = QListWidget()   # lista per visualizzare la cronologia delle vendite
        colonnaVendite.addWidget(self.list_vendite)
        cronologia.addLayout(colonnaVendite)
        colonnaNoleggi = QVBoxLayout()  # layout per la colonna della cronologia dei noleggi
        colonnaNoleggi.addWidget(QLabel("I tuoi noleggi:"))
        self.list_noleggi = QListWidget()   # lista per visualizzare la cronologia dei noleggi
        colonnaNoleggi.addWidget(self.list_noleggi)
        cronologia.addLayout(colonnaNoleggi)
        layout.addLayout(cronologia)    # aggiunge la cronologia al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare gli esiti delle operazioni e le scadenze dei noleggi
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare gli esiti al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra del venditore

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_cerca.clicked.connect(self.cerca_strumenti)
        self.btn_azzera.clicked.connect(self.azzera_ricerca)
        self.txt_ricerca.returnPressed.connect(self.cerca_strumenti)
        self.combo_caratteristica_ricerca.currentTextChanged.connect(self.aggiornaPlaceholderRicerca)
        self.button_aggiungi_strumento.clicked.connect(self.aggiungi_strumento)
        self.button_modifica_strumento.clicked.connect(self.modifica_strumento)
        self.button_rimuovi_strumento.clicked.connect(self.rimuovi_strumento)
        self.button_inserisci_tipo.clicked.connect(self.inserisci_tipo_strumento)
        self.button_cambia_account.clicked.connect(self.cambia_account)
        self.aggiornaPlaceholderRicerca()

    # metodo per avviare il timer che verifica le scadenze dei noleggi
    def _avviaTimer(self):
        self._timer = QTimer()
        self._timer.setInterval(self._intervallo_timer)
        self._timer.timeout.connect(self.onTimerScattato)
        self._timer.start()

    # metodo chiamato quando il timer scatta, verifica le scadenze dei noleggi e aggiorna l'interfaccia
    def onTimerScattato(self):
        esiti = self._noleggi.verificaScadenze()
        if esiti:   # se ci sono esiti da visualizzare, li stampa e aggiorna l'interfaccia
            for esito in esiti: # ciclo per stampare ogni esito della verifica delle scadenze
                print(f"[Timer] {esito}")
            self.label_esito.setText(esiti[-1])
            self.update_ui()

    # metodo chiamato quando la finestra viene chiusa, ferma il timer e chiama il metodo che gestisce la chiusura della finestra madre
    def closeEvent(self, event):
        self._timer.stop()
        super().closeEvent(event)

    # metodo per cercare i tuoi strumenti con il criterio e il valore inseriti nella barra di ricerca
    def cerca_strumenti(self):
        criterio = self.combo_caratteristica_ricerca.currentText()  # ottiene il criterio di ricerca selezionato nel menù a tendina
        valore = self.txt_ricerca.text().strip()   # ottiene il valore da cercare e rimuove spazi bianchi all'inizio e alla fine
        if (criterio == "prezzo massimo" and valore and not controllaNumero(self.txt_ricerca, False, "prezzo massimo")):  # se il criterio è il prezzo massimo e il valore non è un numero valido, errore
            return
        self._aggiornaStrumenti()   # aggiorna la lista dei tuoi strumenti
        if valore and not self._strumenti:  # se il valore è stato inserito ma non è stato trovato nessuno strumento, scrive che non è stato trovato nessuno strumento
            self.label_esito.setText("Non e' stato trovato nessuno strumento con queste caratteristiche")  # scrive che non è stato trovato nessuno strumento
        else:   # altrimenti, se è stato trovato almeno uno strumento, svuota l'etichetta dell'esito
            self.label_esito.setText("")

    # metodo per azzerare la ricerca e mostrare di nuovo tutti i tuoi strumenti
    def azzera_ricerca(self):
        self.txt_ricerca.clear()    # svuota il campo di testo della ricerca
        self.label_esito.setText("")    # svuota l'etichetta dell'esito
        self._aggiornaStrumenti()   # mostra di nuovo tutti i tuoi strumenti

    # metodo per aggiornare il suggerimento nel campo di ricerca in base al criterio selezionato
    def aggiornaPlaceholderRicerca(self):
        suggerimenti = {"tipo": "es. chitarra", "prezzo massimo": "prezzo massimo in euro: es. 450", "azienda": "es. Yamaha", "nome": "es. Stratocaster"}  # dizionario con i suggerimenti per ogni criterio di ricerca
        criterio = self.combo_caratteristica_ricerca.currentText()  # ottiene il criterio di ricerca selezionato nel menù a tendina
        self.txt_ricerca.setPlaceholderText(suggerimenti.get(criterio, ""))   # imposta il suggerimento nel campo di testo in base al criterio selezionato
        if criterio == "prezzo massimo":    # se il criterio è il prezzo massimo, imposta un validatore per il campo di testo
            self.txt_ricerca.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))  # imposta un validatore per il campo di testo che consente solo numeri decimali compresi tra 0 e 999999
        else:   # altrimenti, se il criterio non è il prezzo massimo, non imposta nessun validatore
            self.txt_ricerca.setValidator(None)

    # metodo per aprire la finestra per aggiungere uno strumento
    def aggiungi_strumento(self):
        self._vista_corrente = VistaAggiungiStrumento(self._catalogo, self._venditore, self.update_ui) # crea la finestra per aggiungere uno strumento
        self._vista_corrente.show() # mostra la finestra per aggiungere uno strumento

    # metodo per aprire la finestra per modificare lo strumento selezionato
    def modifica_strumento(self):
        if not self._strumenti:    # se il venditore non ha nessuno strumento, segnalalo
            QMessageBox.warning(self, "Attenzione", "Non hai nessuno strumento da modificare") # scrive che non c'è nessuno strumento da modificare
            return
        self._vista_corrente = VistaModificaStrumento(self._catalogo, self._venditore, self._strumenti, self.update_ui)   # crea la finestra per modificare uno strumento
        self._vista_corrente.show() # mostra la finestra per modificare uno strumento

    # metodo per rimuovere lo strumento selezionato dallo shop
    def rimuovi_strumento(self):
        strumento = self._strumentoSelezionato()    # ottiene lo strumento selezionato nella lista
        if strumento is None:   # se non è stato selezionato nessuno strumento, errore
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare dallo shop lo strumento '{strumento}'?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la rimozione dello strumento selezionato
        if risposta != QMessageBox.Yes: # se la risposta non è positiva, annulla la rimozione
            return
        esito = self._catalogo.rimuoviStrumento(strumento.getId(), self._venditore.getUsername())    # chiama il metodo del gestore catalogo per rimuovere lo strumento selezionato e ottenere l'esito
        self.label_esito.setText(esito) # visualizza l'esito della rimozione nella finestra
        self.update_ui()    # aggiorna la lista dei tuoi strumenti

    # metodo per ottenere lo strumento selezionato nella lista, mostra un messaggio se non c'è selezione o se non è più disponibile
    def _strumentoSelezionato(self):
        item = self.list_miei_strumenti.currentItem()   # ottiene l'elemento selezionato nella lista dei tuoi strumenti
        if item is None:    # se non è stato selezionato nessuno strumento, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona uno strumento dalla lista")
            return None
        id_strumento = item.text().split(" | ")[0]  # ottiene l'id dello strumento selezionato dalla descrizione dell'elemento
        strumento = self._catalogo.trovaStrumento(id_strumento)   # cerca lo strumento nel catalogo tramite il suo id
        if strumento is None:   # se lo strumento non esiste più nel catalogo, errore
            QMessageBox.warning(self, "Attenzione", "Lo strumento selezionato non e' piu' disponibile") # segnala che lo strumento selezionato non è più disponibile
            self.update_ui()    # aggiorna la lista dei tuoi strumenti
            return None
        return strumento    # restituisce lo strumento selezionato

    # metodo per aprire la finestra per inserire un nuovo tipo di strumento
    def inserisci_tipo_strumento(self):
        self._vista_corrente = VistaInserisciTipoStrumento(self._catalogo, self.update_ui)  # crea la finestra per inserire un nuovo tipo di strumento
        self._vista_corrente.show() # mostra la finestra per inserire un nuovo tipo di strumento

    # metodo per cambiare account
    def cambia_account(self):
        self._apri("accesso")  # apre la finestra di accesso per cambiare account

    # metodo per aggiornare la lista dei tuoi strumenti in base alla ricerca
    def _aggiornaStrumenti(self):
        criterio = self.combo_caratteristica_ricerca.currentText()  # ottiene il criterio di ricerca selezionato nel menù a tendina
        valore = self.txt_ricerca.text().strip()   # ottiene il valore da cercare e rimuove spazi bianchi all'inizio e alla fine
        if valore and criterio == "prezzo massimo" and not numeroValido(valore):  # se il criterio è il prezzo massimo e il valore non è un numero valido, azzera il valore
            valore = ""
        if valore:  # se il valore non è vuoto, cerca i tuoi strumenti nel catalogo con il criterio e il valore inseriti
            self._strumenti = self._catalogo.cercaStrumenti(criterio, valore, self._venditore.getUsername())
        else:   # altrimenti, se il valore è vuoto, elenca tutti i tuoi strumenti, anche quelli esauriti
            self._strumenti = self._catalogo.elencaStrumenti(True, self._venditore.getUsername())
        self.list_miei_strumenti.clear()    # svuota la lista dei tuoi strumenti
        for i in self._strumenti:  # ciclo per aggiungere ogni tuo strumento alla lista
            self.list_miei_strumenti.addItem(str(i))

    # metodo per aggiornare le liste della cronologia vendite e noleggi
    def _aggiornaCronologie(self):
        self.list_vendite.clear()   # svuota la lista della cronologia delle vendite
        vendite = self._acquisti.venditeDelVenditore(self._venditore.getUsername())    # ottiene la cronologia delle vendite del venditore
        for i in vendite:   # ciclo per aggiungere ogni vendita alla cronologia
            self.list_vendite.addItem(f"{i.getStrumento().get('nome')} x{i.getQuantita()} - {i.getData()} - compratore: {i.getCompratore().getUsername()} - {i.getTotale():.2f} €")  # descrizione della vendita con strumento, quantita', data, compratore e totale
        if not vendite: # se la cronologia delle vendite è vuota, segnalalo nella lista
            self.list_vendite.addItem("Cronologia vuota")
        self.list_noleggi.clear()   # svuota la lista della cronologia dei noleggi
        noleggi = self._noleggi.noleggiDelVenditore(self._venditore.getUsername()) # ottiene la cronologia dei noleggi del venditore
        for i in noleggi:   # ciclo per aggiungere ogni noleggio alla cronologia
            self.list_noleggi.addItem(f"{i.getStrumento().get('nome')} x{i.getQuantita()} - dal {i.getDataInizio()} al {i.getDataFine()} - compratore: {i.getCompratore().getUsername()}")    # descrizione del noleggio con strumento, quantita', date e compratore
        if not noleggi: # se la cronologia dei noleggi è vuota, segnalalo nella lista
            self.list_noleggi.addItem("Cronologia vuota")

    # metodo per aggiornare l'interfaccia grafica della finestra
    def update_ui(self):
        self._aggiornaStrumenti()   # aggiorna la lista dei tuoi strumenti
        self._aggiornaCronologie()  # aggiorna le liste della cronologia vendite e noleggi

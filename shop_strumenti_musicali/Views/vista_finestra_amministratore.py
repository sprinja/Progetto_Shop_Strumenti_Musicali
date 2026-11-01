from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox)
from PyQt5.QtCore import QTimer
from Services import GestoreAmministratore, GestoreNoleggi
from Models import Amministratore
from Views.vista_rimuovi_compratore import VistaRimuoviCompratore
from Views.vista_rimuovi_venditore import VistaRimuoviVenditore
from Views.vista_rimuovi_strumento import VistaRimuoviStrumento

class VistaFinestraAmministratore(QWidget):
    # costruttore
    def __init__(self, amministratore: Amministratore, gestore: GestoreAmministratore, apri_finestra, gestore_noleggi: GestoreNoleggi, intervallo_timer: int = 60_000):
        super().__init__()
        self._amministratore = amministratore
        self._gestore = gestore
        self._noleggi = gestore_noleggi
        self._apri = apri_finestra
        self._intervallo_timer = intervallo_timer
        self._vista_corrente = None
        self._compratori = []
        self._venditori = []
        self._strumenti = []
        self.setWindowTitle(f"Pagina Amministratore - {amministratore.getUsername()}")
        self.resize(1050, 750)
        self._buildUI()
        self._connectSegnali()
        self._avviaTimer()
        self.update_ui()

    # metodo per costruire l'interfaccia grafica della finestra di aggiunta strumento
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Benvenuto {self._amministratore.getUsername()}. Seleziona una riga e premi il pulsante per eliminarla."))
        colonne = QHBoxLayout() # layout orizzontale per disporre le colonne delle liste
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Compratori registrati:"))
        self.list_compratori = QListWidget() # lista per visualizzare i compratori registrati
        col1.addWidget(self.list_compratori)
        colonne.addLayout(col1)
        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Venditori registrati:"))
        self.list_venditori = QListWidget() # lista per visualizzare i venditori registrati
        col2.addWidget(self.list_venditori)
        colonne.addLayout(col2)
        col3 = QVBoxLayout()
        col3.addWidget(QLabel("Strumenti nello shop:"))
        self.list_strumenti = QListWidget() # lista per visualizzare gli strumenti presenti nello shop
        col3.addWidget(self.list_strumenti)
        colonne.addLayout(col3)
        layout.addLayout(colonne) # aggiunge il layout delle colonne al layout principale
        pulsanti = QHBoxLayout() # layout per i pulsanti di gestione
        self.button_rimuovi_compratore = QPushButton("Rimuovi compratore")
        self.button_rimuovi_venditore = QPushButton("Rimuovi venditore")
        self.button_rimuovi_strumento = QPushButton("Rimuovi strumento")
        self.button_cambia_account = QPushButton("Cambia account")
        for i in (self.button_rimuovi_compratore, self.button_rimuovi_venditore,self.button_rimuovi_strumento, self.button_cambia_account): # ciclo per aggiungere i pulsanti al layout
            pulsanti.addWidget(i)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("") # etichetta per visualizzare l'esito delle operazioni
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)
        self.setLayout(layout) # imposta il layout principale della finestra

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.button_rimuovi_compratore.clicked.connect(self.rimuovi_compratore)
        self.button_rimuovi_venditore.clicked.connect(self.rimuovi_venditore)
        self.button_rimuovi_strumento.clicked.connect(self.rimuovi_strumento)
        self.button_cambia_account.clicked.connect(self.cambia_account)

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
            self.update_ui(esiti[-1])

    # metodo chiamato quando la finestra viene chiusa, ferma il timer e chiama il metodo che gestisce la chiusura della finestra madre
    def closeEvent(self, event):
        self._timer.stop()
        super().closeEvent(event)

    # metodo per ottenere l'elemento selezionato in una lista, restituisce None se non c'è selezione
    def _elementoSelezionato(self, lista, elenco):
        riga = lista.currentRow()   # ottiene l'indice della riga selezionata nella lista
        if 0 <= riga < len(elenco): # se l'indice è valido, restituisce l'elemento corrispondente nell'elenco
            return elenco[riga]
        return None

    # metodo per gestire il caso in cui non ci sia selezione nella lista, mostra un messaggio e apre la finestra corrispondente
    def _nessunaSelezione(self, messaggio, elenco, finestra):
        if not elenco:  # se l'elenco è vuoto, mostra un messaggio e non apre la finestra
            QMessageBox.information(self, "Rimuovi", messaggio)
            return
        self._vista_corrente = finestra(self._gestore, self.update_ui)  # crea una nuova finestra per la rimozione dell'elemento selezionato
        self._vista_corrente.show()

    # metodo per rimuovere un compratore selezionato nella lista, mostra un messaggio di conferma e aggiorna l'interfaccia
    def rimuovi_compratore(self):
        elemento = self._elementoSelezionato(self.list_compratori, self._compratori)    # ottiene l'elemento selezionato nella lista dei compratori
        if elemento is None:    # se l'elemento selezionato è None, significa che non ci sono compratori registrati corrispondenti, quindi mostra un messaggio
            self._nessunaSelezione("Non ci sono compratori registrati", self._compratori, VistaRimuoviCompratore)
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare definitivamente il compratore {elemento.getUsername()}?\n\nVerranno eliminati anche i suoi acquisti e i suoi noleggi; gli strumenti noleggiati verranno rimessi in vendita.", QMessageBox.Yes | QMessageBox.No)  # messaggio di conferma per la rimozione del compratore
        if risposta != QMessageBox.Yes: # se l'amministratore non conferma, esce
            return
        esito = self._gestore.rimuoviUtente("Compratore", elemento.getUsername())   # chiama il metodo del gestore per rimuovere il compratore e ottenere l'esito
        self.label_esito.setText(esito)
        self.update_ui()

    # metodo per rimuovere un venditore selezionato nella lista, mostra un messaggio di conferma e aggiorna l'interfaccia
    def rimuovi_venditore(self):
        elemento = self._elementoSelezionato(self.list_venditori, self._venditori)  # ottiene l'elemento selezionato nella lista dei venditori
        if elemento is None:    # se l'elemento selezionato è None, significa che non ci sono venditori registrati corrispondenti, quindi mostra un messaggio
            self._nessunaSelezione("Non ci sono venditori registrati", self._venditori, VistaRimuoviVenditore) 
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare definitivamente il venditore {elemento.getUsername()}?\n\n", QMessageBox.Yes | QMessageBox.No)  # messaggio di conferma per la rimozione del venditore
        if risposta != QMessageBox.Yes: # se l'amministratore non conferma, esce
            return
        esito = self._gestore.rimuoviUtente("Venditore", elemento.getUsername())    # chiama il metodo del gestore per rimuovere il venditore e ottenere l'esito
        self.label_esito.setText(esito)
        self.update_ui()

    # metodo per rimuovere uno strumento selezionato nella lista, mostra un messaggio di conferma e aggiorna l'interfaccia
    def rimuovi_strumento(self):
        elemento = self._elementoSelezionato(self.list_strumenti, self._strumenti)  # ottiene l'elemento selezionato nella lista degli strumenti
        if elemento is None:    # se l'elemento selezionato è None, significa che non ci sono strumenti nello shop corrispondenti, quindi mostra un messaggio
            self._nessunaSelezione("Non ci sono strumenti nello shop", self._strumenti, VistaRimuoviStrumento)
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare dallo shop lo strumento '{elemento}'?", QMessageBox.Yes | QMessageBox.No) # messaggio di conferma per la rimozione dello strumento
        if risposta != QMessageBox.Yes: # se l'amministratore non conferma, esce    
            return
        esito = self._gestore.rimuoviStrumento(elemento.getId())    # chiama il metodo del gestore per rimuovere lo strumento e ottenere l'esito
        self.label_esito.setText(esito)
        self.update_ui()

    # metodo per cambiare account
    def cambia_account(self):
        self._apri("accesso")

    # metodo per riempire una lista con gli elementi di un elenco
    def _riempi(self, lista, elenco, vuoto):
        lista.clear()   # pulisci la lista
        for elemento in elenco:   # itera per aggiungere tutti gli elementi alla lista
            lista.addItem(str(elemento))
        if not elenco:  # se l'elenco è vuoto segnalalo
            lista.addItem(vuoto)

    # metodo per aggiornare l'interfaccia grafica della finestra
    def update_ui(self, esito: str = None):
        if esito:   # se è stato passato un esito lo si visualizza
            self.label_esito.setText(esito)
        self._compratori = self._gestore.elencaCompratori() # ottiene l'elenco dei compratori registrati
        self._venditori = self._gestore.elencaVenditori()   # ottiene l'elenco dei venditori registrati
        self._strumenti = self._gestore.elencaStrumenti()   # ottiene l'elenco degli strumenti
        self._riempi(self.list_compratori, self._compratori, "Nessun compratore registrato")    # riempie la lista dei compratori con l'elenco
        self._riempi(self.list_venditori, self._venditori, "Nessun venditore registrato")   # riempie la lista dei venditori con l'elenco
        self._riempi(self.list_strumenti, self._strumenti, "Nessuno strumento nello shop")  # riempie la lista degli strumenti con l'elenco

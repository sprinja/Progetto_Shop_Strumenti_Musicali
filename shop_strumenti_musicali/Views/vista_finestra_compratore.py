from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QMessageBox)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QTimer
from Services import GestoreCatalogo, GestoreAcquisti, GestoreNoleggi
from Models import Compratore
from Views.validazione_campi import controllaNumero, numeroValido
from Views.vista_acquisto import VistaAcquisto
from Views.vista_noleggio import VistaNoleggio
from Views.vista_termina_noleggio import VistaTerminaNoleggio

class VistaFinestraCompratore(QWidget):
    # costruttore
    def __init__(self, compratore: Compratore, gestore_catalogo: GestoreCatalogo, gestore_acquisti: GestoreAcquisti, gestore_noleggi: GestoreNoleggi, apri_finestra, intervallo_timer: int = 60_000):
        super().__init__()
        self._compratore = compratore
        self._catalogo = gestore_catalogo
        self._acquisti = gestore_acquisti
        self._noleggi = gestore_noleggi
        self._apri = apri_finestra
        self._intervallo_timer = intervallo_timer
        self._strumenti = []
        self._vista_corrente = None
        self.setWindowTitle(f"Pagina Compratore - {compratore.getUsername()}")
        self.resize(1150, 850)
        self._buildUI()
        self._connectSegnali()
        self._avviaTimer()
        self.update_ui()

    # metodo per costruire l'interfaccia grafica della finestra
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Benvenuto {self._compratore.getUsername()}. Ecco tutti gli strumenti disponibili nello shop:"))    # etichetta per visualizzare il messaggio di benvenuto
        rigaRicerca = QHBoxLayout() # layout per la riga contenente il menù a tendina per la ricerca e il campo di testo
        rigaRicerca.addWidget(QLabel("Cerca per:"))
        self.combo_caratteristica_ricerca = QComboBox()   # menù a tendina per scegliere la caratteristica per cui cercare
        self.combo_caratteristica_ricerca.addItems(["tipo", "prezzo", "azienda", "nome"])
        rigaRicerca.addWidget(self.combo_caratteristica_ricerca)
        self.txt_ricerca = QLineEdit()   # campo di testo per inserire il valore da cercare
        self.txt_ricerca.setPlaceholderText("es. chitarra")  # esempio di valore di ricerca valido
        rigaRicerca.addWidget(self.txt_ricerca)
        self.btn_cerca = QPushButton("Cerca")
        self.btn_azzera = QPushButton("Azzera")
        rigaRicerca.addWidget(self.btn_cerca)
        rigaRicerca.addWidget(self.btn_azzera)
        layout.addLayout(rigaRicerca)    # aggiunge la riga di ricerca al layout principale
        self.list_strumenti_shop = QListWidget()    # lista per visualizzare gli strumenti trovati nella ricerca
        layout.addWidget(self.list_strumenti_shop)  # aggiunge la lista degli strumenti al layout principale
        pulsanti = QHBoxLayout()   # layout per i pulsanti per le azioni possibili sullo strumento selezionato
        self.button_acquista = QPushButton("Acquista")
        self.button_noleggia = QPushButton("Noleggia")
        self.button_termina_noleggio = QPushButton("Termina noleggio")
        self.button_cambia_account = QPushButton("Cambia account")
        for i in (self.button_acquista, self.button_noleggia, self.button_termina_noleggio, self.button_cambia_account):  # ciclo per aggiungere ogni pulsante al layout della riga dei pulsanti
            pulsanti.addWidget(i)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        layout.addWidget(QLabel("Cronologia:"))
        cronologia = QHBoxLayout()  # layout per la cronologia contenente le colonne degli acquisti e dei noleggi
        colonnaAcquisti = QVBoxLayout() # layout per la colonna della cronologia degli acquisti
        colonnaAcquisti.addWidget(QLabel("I tuoi acquisti:"))
        self.list_acquisti = QListWidget()  # lista per visualizzare la cronologia degli acquisti
        colonnaAcquisti.addWidget(self.list_acquisti)
        cronologia.addLayout(colonnaAcquisti)
        colonnaNoleggi = QVBoxLayout()  # layout per la colonna della cronologia dei noleggi
        colonnaNoleggi.addWidget(QLabel("I tuoi noleggi (con tempo rimanente):"))
        self.list_noleggi = QListWidget()   # lista per visualizzare la cronologia dei noleggi con il tempo rimanente
        colonnaNoleggi.addWidget(self.list_noleggi)
        cronologia.addLayout(colonnaNoleggi)
        layout.addLayout(cronologia)    # aggiunge la cronologia al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare gli esiti delle operazioni e le scadenze dei noleggi
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare gli esiti al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra del compratore

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_cerca.clicked.connect(self.cerca_strumenti)
        self.btn_azzera.clicked.connect(self.azzera_ricerca)
        self.txt_ricerca.returnPressed.connect(self.cerca_strumenti)
        self.combo_caratteristica_ricerca.currentTextChanged.connect(self.aggiornaPlaceholderRicerca)
        self.button_acquista.clicked.connect(self.acquista_strumento)
        self.button_noleggia.clicked.connect(self.noleggia_strumento)
        self.button_termina_noleggio.clicked.connect(self.termina_noleggio)
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

    # metodo per cercare gli strumenti con il criterio e il valore inseriti nella barra di ricerca
    def cerca_strumenti(self):
        criterio = self.combo_caratteristica_ricerca.currentText()  # ottiene il criterio di ricerca selezionato nel menù a tendina
        valore = self.txt_ricerca.text().strip()   # ottiene il valore da cercare e rimuove spazi bianchi all'inizio e alla fine
        if (criterio == "prezzo" and valore and not controllaNumero(self.txt_ricerca, False, "prezzo massimo")):  # se il criterio è il prezzo e il valore non è un numero valido, errore
            return
        self._aggiornaStrumenti()   # aggiorna la lista degli strumenti
        if valore and not self._strumenti:  # se il valore è stato inserito ma non è stato trovato nessuno strumento, scrive che non è stato trovato nessuno strumento
            self.label_esito.setText("Non e' stato trovato nessuno strumento con queste caratteristiche")  # scrive che non è stato trovato nessuno strumento
        else:   # altrimenti, se è stato trovato almeno uno strumento, svuota l'etichetta dell'esito
            self.label_esito.setText("")

    # metodo per azzerare la ricerca e mostrare di nuovo tutti gli strumenti
    def azzera_ricerca(self):
        self.txt_ricerca.clear()    # svuota il campo di testo della ricerca
        self.label_esito.setText("")    # svuota l'etichetta dell'esito
        self._aggiornaStrumenti()   # mostra di nuovo tutti gli strumenti

    # metodo per aggiornare il suggerimento nel campo di ricerca in base al criterio selezionato
    def aggiornaPlaceholderRicerca(self):
        suggerimenti = {"tipo": "es. chitarra", "prezzo": "prezzo massimo in euro: es. 450", "azienda": "es. Yamaha", "nome": "es. Stratocaster"}  # dizionario con i suggerimenti per ogni criterio di ricerca
        criterio = self.combo_caratteristica_ricerca.currentText()  # ottiene il criterio di ricerca selezionato nel menù a tendina
        self.txt_ricerca.setPlaceholderText(suggerimenti.get(criterio, ""))   # imposta il suggerimento nel campo di testo in base al criterio selezionato
        if criterio == "prezzo":    # se il criterio è il prezzo, imposta un validatore per il campo di testo
            self.txt_ricerca.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))  # imposta un validatore per il campo di testo che consente solo numeri decimali compresi tra 0 e 999999
        else:   # altrimenti, se il criterio non è il prezzo, non imposta nessun validatore
            self.txt_ricerca.setValidator(None)

    # metodo per aprire la finestra di acquisto dello strumento selezionato
    def acquista_strumento(self):
        strumento = self._strumentoSelezionato()    # ottiene lo strumento selezionato nella lista
        if strumento is None:   # se non è stato selezionato nessuno strumento, errore
            return
        self._vista_corrente = VistaAcquisto(self._acquisti, self._compratore, strumento, self.update_ui)  # crea la finestra di acquisto dello strumento selezionato
        self._vista_corrente.show() # mostra la finestra di acquisto

    # metodo per aprire la finestra di noleggio dello strumento selezionato
    def noleggia_strumento(self):
        strumento = self._strumentoSelezionato()    # ottiene lo strumento selezionato nella lista
        if strumento is None:   # se non è stato selezionato nessuno strumento, errore
            return
        self._vista_corrente = VistaNoleggio(self._noleggi, self._compratore, strumento, self.update_ui)    # crea la finestra di noleggio dello strumento selezionato
        self._vista_corrente.show() # mostra la finestra di noleggio

    # metodo per aprire la finestra per terminare un noleggio attivo
    def termina_noleggio(self):
        attivi = self._noleggi.noleggiAttivi(self._compratore.getUsername())   # ottiene i noleggi attivi del compratore
        if not attivi:  # se il compratore non ha noleggi attivi, segnalalo
            QMessageBox.information(self, "Termina noleggio", "Non hai noleggi attivi a tuo carico")   # scrive che non ci sono noleggi attivi
            return
        self._vista_corrente = VistaTerminaNoleggio(self._noleggi, self._compratore, attivi, self.update_ui)  # crea la finestra per terminare un noleggio attivo
        self._vista_corrente.show() # mostra la finestra per terminare un noleggio attivo

    # metodo per cambiare account
    def cambia_account(self):
        self._apri("accesso")  # apre la finestra di accesso per cambiare account

    # metodo per ottenere lo strumento selezionato nella lista, mostra un messaggio se non c'è selezione o se non è più disponibile
    def _strumentoSelezionato(self):
        item = self.list_strumenti_shop.currentItem()   # ottiene l'elemento selezionato nella lista degli strumenti
        if item is None:    # se non è stato selezionato nessuno strumento, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona uno strumento dalla lista")
            return None
        id_strumento = item.text().split(" | ")[0]  # ottiene l'id dello strumento selezionato dalla descrizione dell'elemento
        strumento = self._catalogo.trovaStrumento(id_strumento)   # cerca lo strumento nel catalogo tramite il suo id
        if strumento is None:   # se lo strumento non esiste più nel catalogo, errore
            QMessageBox.warning(self, "Attenzione", "Lo strumento selezionato non e' piu' disponibile") # segnala che lo strumento selezionato non è più disponibile
            self.update_ui()    # aggiorna la lista degli strumenti
            return None
        return strumento    # restituisce lo strumento selezionato

    # metodo per aggiornare la lista degli strumenti in base alla ricerca
    def _aggiornaStrumenti(self):
        criterio = self.combo_caratteristica_ricerca.currentText()  # ottiene il criterio di ricerca selezionato nel menù a tendina
        valore = self.txt_ricerca.text().strip()   # ottiene il valore da cercare e rimuove spazi bianchi all'inizio e alla fine
        if valore and criterio == "prezzo" and not numeroValido(valore):  # se il criterio è il prezzo e il valore non è un numero valido, azzera il valore
            valore = ""
        if valore:  # se il valore non è vuoto, cerca gli strumenti nel catalogo con il criterio e il valore inseriti
            self._strumenti = self._catalogo.cercaStrumenti(criterio, valore)
        else:   # altrimenti, se il valore è vuoto, elenca tutti gli strumenti
            self._strumenti = self._catalogo.elencaStrumenti()
        self.list_strumenti_shop.clear()    # svuota la lista degli strumenti
        for i in self._strumenti:  # ciclo per aggiungere ogni strumento alla lista
            self.list_strumenti_shop.addItem(str(i))

    # metodo per aggiornare le liste della cronologia acquisti e noleggi
    def _aggiornaCronologie(self):
        self.list_acquisti.clear()  # svuota la lista della cronologia degli acquisti
        acquisti = self._acquisti.cronologiaAcquisti(self._compratore.getUsername())   # ottiene la cronologia degli acquisti del compratore
        for i in acquisti:  # ciclo per aggiungere ogni acquisto alla cronologia
            self.list_acquisti.addItem(str(i))
        if not acquisti:    # se la cronologia degli acquisti è vuota, segnalalo nella lista
            self.list_acquisti.addItem("Cronologia vuota")
        self.list_noleggi.clear()   # svuota la lista della cronologia dei noleggi
        noleggi = self._noleggi.cronologiaNoleggi(self._compratore.getUsername())  # ottiene la cronologia dei noleggi del compratore
        for i in noleggi:   # ciclo per aggiungere ogni noleggio alla cronologia
            self.list_noleggi.addItem(str(i))
        if not noleggi: # se la cronologia dei noleggi è vuota, segnalalo nella lista
            self.list_noleggi.addItem("Cronologia vuota")

    # metodo per aggiornare l'interfaccia grafica della finestra
    def update_ui(self):
        self._aggiornaStrumenti()   # aggiorna la lista degli strumenti
        self._aggiornaCronologie()  # aggiorna le liste della cronologia acquisti e noleggi

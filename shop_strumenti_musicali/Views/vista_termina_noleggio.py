from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QListWidget, QMessageBox)
from Models import Compratore

class VistaTerminaNoleggio(QWidget):
    # costruttore
    def __init__(self, gestore_noleggi, compratore: Compratore, noleggi_attivi: list, termina_callback):
        super().__init__()
        self._gestore = gestore_noleggi
        self._compratore = compratore
        self._noleggi = noleggi_attivi
        self._callback = termina_callback
        self.setWindowTitle("Termina noleggio")
        self.resize(820, 420)
        self._buildUI()
        self._connectSegnali()

    # metodo per costruire l'interfaccia grafica della finestra di terminazione noleggio
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("I tuoi noleggi attivi:"))
        self.list_noleggi = QListWidget()  # lista per visualizzare i noleggi attivi del compratore
        for i in self._noleggi:    # ciclo per aggiungere ogni noleggio attivo alla lista
            self.list_noleggi.addItem(str(i))
        layout.addWidget(self.list_noleggi)   # aggiunge la lista dei noleggi attivi al layout principale
        riga = QHBoxLayout()   # layout per la riga contenente l'etichetta e il menù a tendina per scegliere il noleggio da terminare
        riga.addWidget(QLabel("Noleggio da terminare:"))
        self.combo_noleggio_da_terminare = QComboBox()   # menù a tendina per selezionare il noleggio da terminare
        for i in self._noleggi:    # ciclo per aggiungere al menù a tendina l'id dello strumento di ogni noleggio attivo
            self.combo_noleggio_da_terminare.addItem(i.getStrumento().get("id"), i.getStrumento().get("id")) # sia il testo mostrato sia il dato associato all'elemento del menù a tendina è l'id dello strumento noleggiato
        riga.addWidget(self.combo_noleggio_da_terminare)    # aggiunge il menù a tendina alla riga
        layout.addLayout(riga) # aggiunge la riga contenente il menù a tendina al layout principale
        layout.addWidget(QLabel("Terminando il noleggio prima della scadenza verrai rimborsato della somma extra pagata."))    # etichetta per avvisare che terminando il noleggio prima della scadenza si viene rimborsati della somma extra pagata
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare la terminazione del noleggio o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma terminazione")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito della terminazione del noleggio (successo o errore)
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito della terminazione del noleggio al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di terminazione noleggio

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_termina_noleggio)
        self.btn_chiudi.clicked.connect(self.close)
        self.list_noleggi.itemClicked.connect(self.onNoleggioSelezionato)

    # metodo per selezionare nel menù a tendina il noleggio cliccato nella lista dei noleggi attivi
    def onNoleggioSelezionato(self, item):
        id_strumento = item.text().split(" | ")[0]    # ottiene l'id dello strumento dalla riga cliccata nella lista, separando il testo della riga per il carattere "|"
        indice = self.combo_noleggio_da_terminare.findData(id_strumento)   # cerca il noleggio con lo stesso id nel menù a tendina
        if indice >= 0:    # se il noleggio è stato trovato nel menù a tendina, lo seleziona
            self.combo_noleggio_da_terminare.setCurrentIndex(indice)

    # metodo per confermare la terminazione del noleggio selezionato nel menù a tendina
    def conferma_termina_noleggio(self):
        id_strumento = self.combo_noleggio_da_terminare.currentData()  # ottiene l'id dello strumento del noleggio selezionato nel menù a tendina
        if not id_strumento:    # se non è stato selezionato nessun noleggio, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona un noleggio")
            return
        risposta = QMessageBox.question(self, f"Confermi di terminare il noleggio dello strumento {id_strumento}?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la terminazione del noleggio selezionato
        if risposta == QMessageBox.Yes: # se la risposta è positiva, termina il noleggio
            self.registra_termina_noleggio()

    # metodo per registrare la terminazione del noleggio selezionato
    def registra_termina_noleggio(self):
        id_strumento = self.combo_noleggio_da_terminare.currentData()
        esito = self._gestore.terminaNoleggio(self._compratore.getUsername(), id_strumento) # chiama il metodo del gestore noleggi per terminare il noleggio selezionato
        self.label_esito.setText(esito) # visualizza l'esito della terminazione nella finestra di terminazione noleggio
        self._callback()    # aggiorna la lista dei noleggi attivi nella finestra principale
        if not esito.startswith("Errore"):  # se il noleggio è stato terminato correttamente, chiude la finestra di terminazione noleggio
            self.close()

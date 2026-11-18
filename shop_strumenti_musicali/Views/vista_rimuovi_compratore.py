from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox)

class VistaRimuoviCompratore(QWidget):
    # costruttore
    def __init__(self, gestore_amministratore, rimuovi_callback, elemento=None):
        super().__init__()
        self._gestore = gestore_amministratore
        self._callback = rimuovi_callback
        self._elemento = elemento
        self.setWindowTitle("Rimuovi compratore")
        self.resize(620, 480)
        self._buildUI()
        self._connectSegnali()
        self._aggiornaSelezione()

    # metodo per costruire l'interfaccia grafica della finestra di rimozione compratore
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Compratori registrati (clicca quello da eliminare):"))
        self.list_compratori = QListWidget()    # lista per visualizzare i compratori registrati
        elenco = self._gestore.elencaCompratori()   # ottiene l'elenco dei compratori registrati
        self._elenco = elenco    # salva l'elenco mostrato in lista, così la selezione usa sempre le righe visibili
        for i in elenco:    # ciclo per aggiungere ogni compratore registrato alla lista
            self.list_compratori.addItem(str(i))
        if not elenco:  # se non ci sono compratori registrati, segnalalo nella lista
            self.list_compratori.addItem("Nessun compratore registrato")
        layout.addWidget(self.list_compratori)  # aggiunge la lista dei compratori al layout principale
        layout.addWidget(QLabel("Compratore selezionato:"))
        self.label_selezionato = QLabel("") # etichetta per visualizzare il compratore selezionato nella lista
        self.label_selezionato.setWordWrap(True)
        self.label_selezionato.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_selezionato)    # aggiunge l'etichetta con il compratore selezionato al layout principale
        layout.addWidget(QLabel("Attenzione: verranno eliminati anche i suoi acquisti e i suoi noleggi; gli strumenti noleggiati verranno rimessi in vendita."))
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare la rimozione del compratore o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma rimozione")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito della rimozione del compratore
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito della rimozione al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di rimozione compratore

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_rimozione)
        self.btn_chiudi.clicked.connect(self.close)
        self.list_compratori.currentRowChanged.connect(self._selezionaRiga)

    # metodo chiamato quando si clicca una riga della lista, aggiorna il compratore selezionato
    def _selezionaRiga(self, riga: int):
        elenco = self._elenco   # usa l'elenco mostrato in lista, così la riga cliccata corrisponde sempre all'elemento visibile
        self._elemento = elenco[riga] if 0 <= riga < len(elenco) else None    # prende il compratore della riga cliccata, oppure nessuno se la riga non è valida
        self._aggiornaSelezione()

    # metodo per aggiornare l'etichetta con il compratore selezionato nella lista
    def _aggiornaSelezione(self):
        if self._elemento is None:
            self.label_selezionato.setText("Nessuno selezionato: clicca un compratore nella lista")   # se non c'è nessun compratore selezionato, scrive che non è stato selezionato nessuno
        else:
            self.label_selezionato.setText(str(self._elemento))   # visualizza il compratore selezionato nell'etichetta
            if self.list_compratori.currentRow() < 0: # se il compratore non è selezionato nella lista, seleziona la riga corrispondente
                for i in range(self.list_compratori.count()): # ciclo per confrontare ogni riga della lista con il compratore selezionato
                    if self.list_compratori.item(i).text() == str(self._elemento):   # se il testo della riga corrisponde al compratore selezionato, seleziona quella riga
                        self.list_compratori.setCurrentRow(i)
                        break

    # metodo per confermare la rimozione del compratore selezionato
    def conferma_rimozione(self):
        if self._elemento is None:  # se non è stato selezionato nessun compratore, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona un compratore dalla lista")
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare definitivamente il compratore '{self._elemento.getUsername()}'?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la rimozione del compratore selezionato
        if risposta == QMessageBox.Yes: # se la risposta è positiva, rimuove il compratore
            self.registra_rimozione()

    # metodo per registrare la rimozione del compratore selezionato
    def registra_rimozione(self):
        esito = self._gestore.rimuoviUtente("Compratore", self._elemento.getUsername())   # chiama il metodo del gestore per rimuovere il compratore selezionato e ottenere l'esito
        self.label_esito.setText(esito) # visualizza l'esito della rimozione nella finestra di rimozione compratore
        self._callback(esito)   # aggiorna la lista dei compratori nella finestra principale
        if not esito.startswith("Errore"):  # se il compratore è stato rimosso correttamente, chiude la finestra
            self.close()

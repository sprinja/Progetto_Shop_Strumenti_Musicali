from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox)

class VistaRimuoviVenditore(QWidget):
    # costruttore
    def __init__(self, gestore_amministratore, rimuovi_callback, elemento=None):
        super().__init__()
        self._gestore = gestore_amministratore
        self._callback = rimuovi_callback
        self._elemento = elemento
        self.setWindowTitle("Rimuovi venditore")
        self.resize(620, 480)
        self._buildUI()
        self._connectSegnali()
        self._aggiornaSelezione()

    # metodo per costruire l'interfaccia grafica della finestra di rimozione venditore
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Venditori registrati (clicca quello da eliminare):"))
        self.list_venditori = QListWidget()   # lista per visualizzare i venditori registrati
        elenco = self._gestore.elencaVenditori()  # ottiene l'elenco dei venditori registrati
        self._elenco = elenco    # salva l'elenco mostrato in lista, così la selezione usa sempre le righe visibili
        for i in elenco:    # ciclo per aggiungere ogni venditore registrato alla lista
            self.list_venditori.addItem(str(i))
        if not elenco:  # se non ci sono venditori registrati, segnalalo nella lista
            self.list_venditori.addItem("Nessun venditore registrato")
        layout.addWidget(self.list_venditori)    # aggiunge la lista dei venditori al layout principale
        layout.addWidget(QLabel("Venditore selezionato:"))
        self.label_selezionato = QLabel("")   # etichetta per visualizzare il venditore selezionato nella lista
        self.label_selezionato.setWordWrap(True)
        self.label_selezionato.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_selezionato)  # aggiunge l'etichetta con il venditore selezionato al layout principale
        layout.addWidget(QLabel("Attenzione: verranno eliminati dallo shop tutti gli strumenti da lui inseriti."))
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare la rimozione del venditore o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma rimozione")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito della rimozione del venditore
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito della rimozione al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di rimozione venditore

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_rimozione)
        self.btn_chiudi.clicked.connect(self.close)
        self.list_venditori.currentRowChanged.connect(self._selezionaRiga)

    # metodo chiamato quando si clicca una riga della lista, aggiorna il venditore selezionato
    def _selezionaRiga(self, riga: int):
        elenco = self._elenco   # usa l'elenco mostrato in lista, così la riga cliccata corrisponde sempre all'elemento visibile
        self._elemento = elenco[riga] if 0 <= riga < len(elenco) else None    # prende il venditore della riga cliccata, oppure nessuno se la riga non è valida
        self._aggiornaSelezione()

    # metodo per aggiornare l'etichetta con il venditore selezionato nella lista
    def _aggiornaSelezione(self):
        if self._elemento is None:
            self.label_selezionato.setText("Nessuno selezionato: clicca un venditore nella lista")   # se non c'è nessun venditore selezionato, scrive che non è stato selezionato nessuno
        else:
            self.label_selezionato.setText(str(self._elemento))   # visualizza il venditore selezionato nell'etichetta
            if self.list_venditori.currentRow() < 0: # se il venditore non è selezionato nella lista, seleziona la riga corrispondente
                for i in range(self.list_venditori.count()): # ciclo per confrontare ogni riga della lista con il venditore selezionato
                    if self.list_venditori.item(i).text() == str(self._elemento):   # se il testo della riga corrisponde al venditore selezionato, seleziona quella riga
                        self.list_venditori.setCurrentRow(i)
                        break

    # metodo per confermare la rimozione del venditore selezionato
    def conferma_rimozione(self):
        if self._elemento is None:  # se non è stato selezionato nessun venditore, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona un venditore dalla lista")
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare definitivamente il venditore '{self._elemento.getUsername()}' e tutti i suoi strumenti?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la rimozione del venditore selezionato
        if risposta == QMessageBox.Yes: # se la risposta è positiva, rimuove il venditore
            self.registra_rimozione()

    # metodo per registrare la rimozione del venditore selezionato
    def registra_rimozione(self):
        esito = self._gestore.rimuoviUtente("Venditore", self._elemento.getUsername())   # chiama il metodo del gestore per rimuovere il venditore selezionato e ottenere l'esito
        self.label_esito.setText(esito) # visualizza l'esito della rimozione nella finestra di rimozione venditore
        self._callback(esito)   # aggiorna la lista dei venditori nella finestra principale
        if not esito.startswith("Errore"):  # se il venditore è stato rimosso correttamente, chiude la finestra
            self.close()

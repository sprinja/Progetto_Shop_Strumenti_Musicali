from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox)

class VistaRimuoviStrumento(QWidget):
    # costruttore
    def __init__(self, gestore_amministratore, rimuovi_callback, elemento=None):
        super().__init__()
        self._gestore = gestore_amministratore
        self._callback = rimuovi_callback
        self._elemento = elemento
        self.setWindowTitle("Rimuovi strumento")
        self.resize(860, 500)
        self._buildUI()
        self._connectSegnali()
        self._aggiornaSelezione()

    # metodo per costruire l'interfaccia grafica della finestra di rimozione strumento
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Strumenti presenti nello shop (clicca quello da eliminare):"))
        self.list_strumenti = QListWidget()   # lista per visualizzare gli strumenti presenti nello shop
        elenco = self._gestore.elencaStrumenti()  # ottiene l'elenco degli strumenti presenti nello shop
        for i in elenco:    # ciclo per aggiungere ogni strumento alla lista
            self.list_strumenti.addItem(str(i))
        if not elenco:  # se non ci sono strumenti nello shop, segnalalo nella lista
            self.list_strumenti.addItem("Nessuno strumento nello shop")
        layout.addWidget(self.list_strumenti)    # aggiunge la lista degli strumenti al layout principale
        layout.addWidget(QLabel("Strumento selezionato:"))
        self.label_selezionato = QLabel("")   # etichetta per visualizzare lo strumento selezionato nella lista
        self.label_selezionato.setWordWrap(True)
        self.label_selezionato.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_selezionato)  # aggiunge l'etichetta con lo strumento selezionato al layout principale
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare la rimozione dello strumento o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma rimozione")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito della rimozione dello strumento
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito della rimozione al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di rimozione strumento

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_rimozione)
        self.btn_chiudi.clicked.connect(self.close)
        self.list_strumenti.currentRowChanged.connect(self._selezionaRiga)

    # metodo chiamato quando si clicca una riga della lista, aggiorna lo strumento selezionato
    def _selezionaRiga(self, riga: int):
        elenco = self._gestore.elencaStrumenti()  # ottiene l'elenco degli strumenti presenti nello shop
        self._elemento = elenco[riga] if 0 <= riga < len(elenco) else None    # prende lo strumento della riga cliccata, oppure nessuno se la riga non è valida
        self._aggiornaSelezione()

    # metodo per aggiornare l'etichetta con lo strumento selezionato nella lista
    def _aggiornaSelezione(self):
        if self._elemento is None:
            self.label_selezionato.setText("Nessuno selezionato: clicca uno strumento nella lista")   # se non c'è nessuno strumento selezionato, scrive che non è stato selezionato nessuno
        else:
            self.label_selezionato.setText(str(self._elemento))   # visualizza lo strumento selezionato nell'etichetta
            if self.list_strumenti.currentRow() < 0: # se lo strumento non è selezionato nella lista, seleziona la riga corrispondente
                for i in range(self.list_strumenti.count()): # ciclo per confrontare ogni riga della lista con lo strumento selezionato
                    if self.list_strumenti.item(i).text() == str(self._elemento):   # se il testo della riga corrisponde allo strumento selezionato, seleziona quella riga
                        self.list_strumenti.setCurrentRow(i)
                        break

    # metodo per confermare la rimozione dello strumento selezionato
    def conferma_rimozione(self):
        if self._elemento is None:  # se non è stato selezionato nessuno strumento, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona uno strumento dalla lista")
            return
        risposta = QMessageBox.question(self, "Conferma", f"Eliminare dallo shop lo strumento '{self._elemento}'?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la rimozione dello strumento selezionato
        if risposta == QMessageBox.Yes: # se la risposta è positiva, rimuove lo strumento
            self.registra_rimozione()

    # metodo per registrare la rimozione dello strumento selezionato
    def registra_rimozione(self):
        esito = self._gestore.rimuoviStrumento(self._elemento.getId())   # chiama il metodo del gestore per rimuovere lo strumento selezionato e ottenere l'esito
        self.label_esito.setText(esito) # visualizza l'esito della rimozione nella finestra di rimozione strumento
        self._callback(esito)   # aggiorna la lista degli strumenti nella finestra principale
        if not esito.startswith("Errore"):  # se lo strumento è stato rimosso correttamente, chiude la finestra
            self.close()

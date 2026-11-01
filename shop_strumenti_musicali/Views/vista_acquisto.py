from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QIntValidator
from Models import Compratore, Strumento
from Views.validazione_campi import controllaNumero

class VistaAcquisto(QWidget):
    # costruttore
    def __init__(self, gestore_acquisti, compratore: Compratore, strumento: Strumento, acquisto_callback):
        super().__init__()
        self._gestore = gestore_acquisti
        self._compratore = compratore
        self._strumento = strumento
        self._id_strumento = strumento.getId()
        self._callback = acquisto_callback
        self.setWindowTitle("Acquisto strumento")
        self.resize(720, 340)
        self._buildUI()
        self._connectSegnali()

    # metodo per costruire l'interfaccia grafica della finestra di acquisto
    def _buildUI(self):
        layout = QVBoxLayout() 
        layout.addWidget(QLabel("Strumento selezionato:"))
        self.label_strumento = QLabel(str(self._strumento)) # etichetta per visualizzare le informazioni dello strumento selezionato
        self.label_strumento.setWordWrap(True)
        self.label_strumento.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_strumento)  # aggiunge l'etichetta con le informazioni dello strumento al layout principale
        riga = QHBoxLayout()    # layout per la riga contenente l'etichetta e il campo di testo per inserire la quantità da acquistare
        riga.addWidget(QLabel("Quantita':"))
        self.txt_quantita = QLineEdit() # campo di testo per inserire la quantità da acquistare
        self.txt_quantita.setPlaceholderText("es. 1")   # esempio di quantità valida
        self.txt_quantita.setValidator(QIntValidator(1, 999999, self))  # imposta un validatore per il campo di testo che consente solo numeri interi compresi tra 1 e 999999
        riga.addWidget(self.txt_quantita)   
        layout.addLayout(riga)  # aggiunge la riga contenente la quantità al layour principale
        pulsanti = QHBoxLayout()    # layout per i pulsanti per confermare l'acquisto o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma acquisto")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)   
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti)  # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito dell'acquisto
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito dell'acquisto al layout principale
        self.setLayout(layout)  # imposta il layout principale alla finestra di acquisto

    # metodo per connettere i segnali dei pulsanti alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_acquisto)
        self.btn_chiudi.clicked.connect(self.close)

    # metodo per confermare l'acquisto dello strumento selezionato
    def conferma_acquisto(self):
        quantita = self.txt_quantita.text().strip() # ottiene la quantità inserita e rimuove spazi bianchi all'inizio e alla fine
        if not quantita:    # se la quantità è vuota, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci la quantita'")
            return
        if not controllaNumero(self.txt_quantita, True, "quantita'"):   # se la quantità non è un numero valido, errore
            return
        risposta = QMessageBox.question(self, "Conferma", f"Confermi l'acquisto di {quantita} pezzi di '{self._strumento.getNome()}' ({self._id_strumento})?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per l'acquisto dello strumento selezionato
        if risposta == QMessageBox.Yes: # se la risposta è positiva, registra l'acquisto
            self.registra_acquisto()

    # metodo per registrare l'acquisto dello strumento selezionato
    def registra_acquisto(self):
        esito = self._gestore.effettuaAcquisto(self._compratore.getUsername(), self._id_strumento, self.txt_quantita.text().strip())    # chiama il metodo del gestore acquisti per registrare l'acquisto dello strumento selezionato
        self.label_esito.setText(esito) # visualizza l'esito dell'acquisto nella finestra di acquisto
        self._callback()    # aggiorna la lista degli acquisti nella finestra principale
        if not esito.startswith("Errore"):  # se l'acquisto è stato registrato correttamente, svuota il campo di testo per la quantità
            self.txt_quantita.clear()

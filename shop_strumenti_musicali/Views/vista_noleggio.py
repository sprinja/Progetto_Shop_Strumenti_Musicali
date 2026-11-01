from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QIntValidator
from Models import Compratore, Strumento
from Views.validazione_campi import controllaNumero

class VistaNoleggio(QWidget):
    # costruttore
    def __init__(self, gestore_noleggi, compratore: Compratore, strumento: Strumento, noleggio_callback):
        super().__init__()
        self._gestore = gestore_noleggi
        self._compratore = compratore
        self._strumento = strumento
        self._id_strumento = strumento.getId()
        self._callback = noleggio_callback
        self.setWindowTitle("Noleggio strumento")
        self.resize(760, 380)
        self._buildUI()
        self._connectSegnali()

    # metodo per costruire l'interfaccia grafica della finestra di noleggio
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Strumento selezionato (il prezzo di noleggio giornaliero e' l'ultimo valore indicato nella riga):"))
        self.label_strumento = QLabel(str(self._strumento)) # etichetta per visualizzare le informazioni dello strumento selezionato
        self.label_strumento.setWordWrap(True)
        self.label_strumento.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.label_strumento)  # aggiunge l'etichetta con le informazioni dello strumento al layout principale
        riga = QHBoxLayout()    # layout per la riga contenente l'etichetta e il campo di testo per inserire la quantità da noleggiare
        riga.addWidget(QLabel("Quantita':"))
        self.txt_quantita = QLineEdit() # campo di testo per inserire la quantità da noleggiare
        self.txt_quantita.setPlaceholderText("es. 1")   # esempio di quantità valida
        self.txt_quantita.setValidator(QIntValidator(1, 999999, self))  # imposta un validatore per il campo di testo che consente solo numeri interi compresi tra 1 e 999999
        riga.addWidget(self.txt_quantita)
        riga.addWidget(QLabel("Durata (giorni):"))
        self.txt_durata = QLineEdit()   # campo di testo per inserire la durata del noleggio in giorni
        self.txt_durata.setPlaceholderText("es. 7")  # esempio di durata valida
        self.txt_durata.setValidator(QIntValidator(1, 3650, self)) # imposta un validatore per il campo di testo che consente solo numeri interi compresi tra 1 e 3650
        riga.addWidget(self.txt_durata)
        layout.addLayout(riga)  # aggiunge la riga contenente quantità e durata al layout principale
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare il noleggio o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma noleggio")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito del noleggio (successo o errore)
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito del noleggio al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di noleggio

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_noleggio)
        self.btn_chiudi.clicked.connect(self.close)

    # metodo per confermare il noleggio dello strumento selezionato
    def conferma_noleggio(self):
        quantita = self.txt_quantita.text().strip() # ottiene la quantità inserita e rimuove spazi bianchi all'inizio e alla fine
        durata = self.txt_durata.text().strip() # ottiene la durata inserita e rimuove spazi bianchi all'inizio e alla fine
        if not quantita or not durata:  # se la quantità o la durata sono vuote, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci quantita' e durata")
            return
        if not controllaNumero(self.txt_quantita, True, "quantita'"):   # se la quantità non è un numero valido, errore
            return
        if not controllaNumero(self.txt_durata, True, "durata"):    # se la durata non è un numero valido, errore
            return
        risposta = QMessageBox.question(self, "Conferma", f"Confermi il noleggio di {quantita} pezzi di '{self._strumento.getNome()}' ({self._id_strumento}) per {durata} giorni?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per il noleggio dello strumento selezionato
        if risposta == QMessageBox.Yes: # se la risposta è positiva, registra il noleggio
            self.registra_noleggio()

    # metodo per registrare il noleggio dello strumento selezionato
    def registra_noleggio(self):
        esito = self._gestore.effettuaNoleggio(self._compratore.getUsername(), self._id_strumento, self.txt_quantita.text().strip(), self.txt_durata.text().strip())    # chiama il metodo del gestore noleggi per registrare il noleggio dello strumento selezionato
        self.label_esito.setText(esito) # visualizza l'esito del noleggio nella finestra di noleggio
        self._callback()    # aggiorna la lista degli strumenti nella finestra principale
        if not esito.startswith("Errore"):  # se il noleggio è stato registrato correttamente, svuota i campi di testo
            self.txt_quantita.clear()
            self.txt_durata.clear()

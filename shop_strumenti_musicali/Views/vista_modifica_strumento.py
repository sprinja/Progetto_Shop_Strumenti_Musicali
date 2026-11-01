from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from Models import Venditore
from Views.validazione_campi import controllaNumero

class VistaModificaStrumento(QWidget):
    # elenco delle caratteristiche che si possono modificare
    CARATTERISTICHE = ["nome", "tipo", "azienda", "quantita", "prezzo", "prezzo_noleggio", "nome_venditore"]
    # caratteristiche numeriche con i loro valori minimo e massimo ammessi
    CARATTERISTICHE_NUMERICHE = {"quantita": (0, 999999), "prezzo": (0.0, 999999.0), "prezzo_noleggio": (0.0, 99999.0)}

    # costruttore
    def __init__(self, gestore_catalogo, venditore: Venditore, strumenti: list, modifica_callback):
        super().__init__()
        self._gestore = gestore_catalogo
        self._venditore = venditore
        self._strumenti = strumenti
        self._callback = modifica_callback
        self.setWindowTitle("Modifica strumento")
        self.resize(660, 460)
        self._buildUI()
        self._connectSegnali()
        self.aggiornaValidatore()

    # metodo per costruire l'interfaccia grafica della finestra di modifica strumento
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Strumento da modificare:"))
        self.combo_strumento_da_modificare = QComboBox()   # menù a tendina per scegliere lo strumento da modificare
        for i in self._strumenti:  # ciclo per aggiungere ogni strumento al menù a tendina, con il testo mostrato e l'id come dato associato
            self.combo_strumento_da_modificare.addItem(str(i), i.getId())
        layout.addWidget(self.combo_strumento_da_modificare)  # aggiunge il menù a tendina con gli strumenti al layout principale
        riga = QHBoxLayout()   # layout per la riga contenente la caratteristica da modificare e il nuovo valore
        riga.addWidget(QLabel("Caratteristica:"))
        self.combo_caratteristica_da_modificare = QComboBox()    # menù a tendina per scegliere la caratteristica da modificare
        self.combo_caratteristica_da_modificare.addItems(self.CARATTERISTICHE)
        riga.addWidget(self.combo_caratteristica_da_modificare)
        riga.addWidget(QLabel("Nuovo valore:"))
        self.txt_nuovo_valore = QLineEdit()  # campo di testo per inserire il nuovo valore della caratteristica
        self.txt_nuovo_valore.setPlaceholderText("es. 120")  # esempio di nuovo valore valido
        riga.addWidget(self.txt_nuovo_valore)
        self.combo_nuovo_tipo = QComboBox()    # menù a tendina con i tipi già esistenti, al posto del campo di testo quando la caratteristica selezionata è il tipo
        for i in self._gestore.elencaTipi():    # ciclo per aggiungere ogni tipo esistente al menù a tendina
            self.combo_nuovo_tipo.addItem(i.getNomeTipo())
        riga.addWidget(self.combo_nuovo_tipo)   # aggiunge il menù a tendina dei tipi alla riga del nuovo valore
        layout.addLayout(riga)  # aggiunge la riga contenente caratteristica e nuovo valore al layout principale
        layout.addWidget(QLabel("Nota: se il tipo non esiste o se dopo la modifica lo strumento risulta identico ad un altro, verra' segnalato."))
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare la modifica dello strumento o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma modifica")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito della modifica dello strumento
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito della modifica al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di modifica strumento

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_modifica)
        self.btn_chiudi.clicked.connect(self.close)
        self.combo_caratteristica_da_modificare.currentTextChanged.connect(self.aggiornaValidatore)

    # metodo per aggiornare il campo del nuovo valore in base alla caratteristica selezionata: validatore numerico o menù a tendina dei tipi
    def aggiornaValidatore(self):
        car = self.combo_caratteristica_da_modificare.currentText()   # ottiene la caratteristica selezionata nel menù a tendina
        if car == "tipo":   # se la caratteristica selezionata è il tipo, nasconde il campo di testo e mostra il menù a tendina con i tipi già esistenti
            self.txt_nuovo_valore.hide()
            self.combo_nuovo_tipo.show()
            return
        self.combo_nuovo_tipo.hide()    # altrimenti, nasconde il menù a tendina dei tipi e mostra il campo di testo per il nuovo valore
        self.txt_nuovo_valore.show()
        if car in self.CARATTERISTICHE_NUMERICHE:   # se la caratteristica selezionata è numerica, imposta il validatore numerico con minimo e massimo
            minimo, massimo = self.CARATTERISTICHE_NUMERICHE[car]   # ottiene il valore minimo e massimo ammessi per la caratteristica
            if isinstance(minimo, int): # se i valori ammessi sono interi, imposta il validatore per i numeri interi
                self.txt_nuovo_valore.setValidator(QIntValidator(minimo, massimo, self))
                self.txt_nuovo_valore.setPlaceholderText(f"es. 6 ({minimo}-{massimo})")    # esempio di nuovo valore valido con il suo intervallo
            else:   # altrimenti, se i valori ammessi sono decimali, imposta il validatore per i numeri decimali
                self.txt_nuovo_valore.setValidator(QDoubleValidator(minimo, massimo, 2, self))
                self.txt_nuovo_valore.setPlaceholderText("es. 450,50")  # esempio di nuovo valore valido
        else:   # se la caratteristica non è numerica (come nome o azienda), il valore non ha un intervallo
            self.txt_nuovo_valore.setValidator(None)    # non imposta nessun validatore per il campo di testo
            self.txt_nuovo_valore.setPlaceholderText("es. Yamaha")  # esempio di nuovo valore valido
        self.txt_nuovo_valore.clear()   # svuota il campo del nuovo valore

    # metodo per ottenere il nuovo valore: il tipo si sceglie nel menù a tendina, le altre caratteristiche si scrivono nel campo di testo
    def _nuovoValore(self):
        if self.combo_caratteristica_da_modificare.currentText() == "tipo":   # se la caratteristica selezionata è il tipo, ritorna il tipo scelto nel menù a tendina
            return self.combo_nuovo_tipo.currentText()
        return self.txt_nuovo_valore.text().strip()   # altrimenti, ritorna il nuovo valore scritto nel campo di testo

    # metodo per confermare la modifica della caratteristica dello strumento selezionato
    def conferma_modifica(self):
        id_strumento = self.combo_strumento_da_modificare.currentData()    # ottiene l'id dello strumento selezionato nel menù a tendina
        caratteristica = self.combo_caratteristica_da_modificare.currentText()  # ottiene la caratteristica selezionata nel menù a tendina
        nuovo_valore = self._nuovoValore()  # ottiene il nuovo valore dal menù a tendina o dal campo di testo a seconda della caratteristica selezionata
        if not id_strumento:    # se non è stato selezionato nessuno strumento, errore
            QMessageBox.warning(self, "Attenzione", "Seleziona uno strumento")
            return
        if caratteristica == "tipo" and not nuovo_valore:   # se la caratteristica è il tipo ma nel menù a tendina non c'è nessun tipo, errore
            QMessageBox.warning(self, "Attenzione", "Non esiste nessun tipo: creane uno nuovo prima")
            return
        if not nuovo_valore:    # se non è stato inserito nessun nuovo valore, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci il nuovo valore")
            return
        if caratteristica in self.CARATTERISTICHE_NUMERICHE:   # se la caratteristica è numerica, controlla che il nuovo valore sia un numero valido
            intero = isinstance(self.CARATTERISTICHE_NUMERICHE[caratteristica][0], int)  # controlla se la caratteristica richiede un numero intero
            if not controllaNumero(self.txt_nuovo_valore, intero, caratteristica):   # se il nuovo valore non è un numero valido per la caratteristica, errore
                return
        risposta = QMessageBox.question(self, "Conferma", f"Cambiare '{caratteristica}' in '{nuovo_valore}'?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la modifica della caratteristica
        if risposta == QMessageBox.Yes: # se la risposta è positiva, registra la modifica
            self.registra_modifica()

    # metodo per registrare la modifica della caratteristica dello strumento selezionato
    def registra_modifica(self):
        esito = self._gestore.modificaStrumento(self.combo_strumento_da_modificare.currentData(), self.combo_caratteristica_da_modificare.currentText(), self._nuovoValore())   # chiama il metodo del gestore catalogo per modificare la caratteristica dello strumento con il nuovo valore selezionato
        self.label_esito.setText(esito) # visualizza l'esito della modifica nella finestra di modifica strumento
        self._callback()    # aggiorna la lista degli strumenti nella finestra principale
        if not esito.startswith("Errore"):  # se la modifica è stata registrata correttamente, chiude la finestra
            self.close()

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from Models import Venditore
from Views.validazione_campi import controllaNumero

class VistaAggiungiStrumento(QWidget):
    # costruttore
    def __init__(self, gestore_catalogo, venditore: Venditore, aggiungi_callback):
        super().__init__()
        self._gestore = gestore_catalogo
        self._venditore = venditore
        self._callback = aggiungi_callback
        self._ultimo_default_noleggio = ""
        self.setWindowTitle("Aggiungi strumento (vendita)")
        self.resize(600, 560)
        self._buildUI()
        self._connectSegnali()

    # metodo per costruire l'interfaccia grafica della finestra di aggiunta strumento
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tipo di strumento (deve gia' esistere):"))
        self.combo_tipo_strumento = QComboBox() # menu a tendina per selezionare il tipo di strumento da aggiungere
        for categoria in self._gestore.elencaTipi():    # aggiunge al menù a tendina tutti i tipi di strumento esistenti nel catalogo
            self.combo_tipo_strumento.addItem(categoria.getNomeTipo())
        layout.addWidget(self.combo_tipo_strumento) # aggiunge il menù a tendina al layout principale
        self.txt_nome_strumento = QLineEdit()   # campo di testo per inserire il nome dello strumento da aggiungere
        self.txt_nome_strumento.setPlaceholderText("es. Flauto dolce in legno di ciliegio in chiave di sol")
        riga1 = QHBoxLayout()   # layout per la riga contenente l'etichetta e il campo di testo per inserire il nome dello strumento
        riga1.addWidget(QLabel("Nome:"))
        riga1.addWidget(self.txt_nome_strumento)
        layout.addLayout(riga1) # aggiunge la riga contenente il nome dello strumento al layout principale
        self.txt_azienda_strumento = QLineEdit()    # campo di testo per inserire il nome dell'azienda produttrice dello strumento da aggiungere
        self.txt_azienda_strumento.setPlaceholderText("es. Yamaha")
        riga2 = QHBoxLayout()   # layout per la riga contenente l'etichetta e il campo di testo per inserire il nome dell'azienda produttrice dello strumento
        riga2.addWidget(QLabel("Azienda produttrice:"))
        riga2.addWidget(self.txt_azienda_strumento)
        layout.addLayout(riga2) # aggiunge la riga contenente il nome dell'azienda produttrice dello strumento al layout principale
        self.txt_nome_venditore = QLineEdit()   # campo di testo per inserire il nome del venditore che aggiunge lo strumento
        self.txt_nome_venditore.setPlaceholderText(f"nome mostrato nello shop (default: {self._venditore.getUsername()})")
        riga3 = QHBoxLayout()   # layout per la riga contenente l'etichetta e il campo di testo per inserire il nome del venditore
        riga3.addWidget(QLabel("Nome del venditore:"))
        riga3.addWidget(self.txt_nome_venditore)
        layout.addLayout(riga3) # aggiunge la riga contenente il nome del venditore al layout principale
        self.txt_quantita = QLineEdit() # campo di testo per inserire la quantità disponibile dello strumento da aggiungere
        self.txt_quantita.setPlaceholderText("es. 6")
        self.txt_quantita.setValidator(QIntValidator(1, 999999, self))  # imposta un validatore per il campo di testo che consente solo numeri interi compresi tra 1 e 999999
        riga4 = QHBoxLayout()   # layout per la riga contenente l'etichetta e il campo di testo per inserire la quantità disponibile dello strumento
        riga4.addWidget(QLabel("Quantita' disponibile:"))
        riga4.addWidget(self.txt_quantita)
        layout.addLayout(riga4) # aggiunge la riga contenente la quantità disponibile dello strumento al layout principale
        self.txt_prezzo_strumento = QLineEdit() # campo di testo per inserire il prezzo di acquisto dello strumento da aggiungere
        self.txt_prezzo_strumento.setPlaceholderText("es. 450 (o 450,50)")
        self.txt_prezzo_strumento.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))    # imposta un validatore per il campo di testo che consente solo numeri decimali compresi tra 0.0 e 999999.0 con massimo 2 cifre decimali
        riga5 = QHBoxLayout()   # layout per la riga contenente l'etichetta e il campo di testo per inserire il prezzo di acquisto dello strumento
        riga5.addWidget(QLabel("Prezzo di acquisto:"))
        riga5.addWidget(self.txt_prezzo_strumento)
        layout.addLayout(riga5) # aggiunge la riga contenente il prezzo di acquisto dello strumento al layout principale
        self.txt_prezzo_noleggio = QLineEdit()  # campo di testo per inserire il prezzo di noleggio giornaliero dello strumento da aggiungere
        self.txt_prezzo_noleggio.setPlaceholderText("es. 0,90 (default: quota del tipo x prezzo di acquisto)")
        self.txt_prezzo_noleggio.setValidator(QDoubleValidator(0.0, 99999.0, 2, self))  # imposta un validatore per il campo di testo che consente solo numeri decimali compresi tra 0.0 e 99999.0 con massimo 2 cifre decimali
        riga6 = QHBoxLayout()   # layout per la riga contenente l'etichetta e il campo di testo per inserire il prezzo di noleggio giornaliero dello strumento
        riga6.addWidget(QLabel("Prezzo di noleggio giornaliero:"))
        riga6.addWidget(self.txt_prezzo_noleggio)
        layout.addLayout(riga6) # aggiunge la riga contenente il prezzo di noleggio giornaliero dello strumento al layout principale
        self.label_stima_noleggio = QLabel("")  # etichetta per visualizzare la stima del prezzo di noleggio giornaliero dello strumento da aggiungere
        self.label_stima_noleggio.setWordWrap(True)
        layout.addWidget(self.label_stima_noleggio)
        layout.addWidget(QLabel("(in euro al giorno: è il valore che pagherà chi noleggia, per ogni giorno di noleggio: lo puoi cambiare a piacimento)"))
        pulsanti = QHBoxLayout()    # layout per i pulsanti per confermare l'aggiunta dello strumento o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma aggiunta")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti)  # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito dell'aggiunta dello strumento (successo o errore)
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito dell'aggiunta dello strumento al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di aggiunta strumento

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_aggiunta)
        self.btn_chiudi.clicked.connect(self.close)
        self.combo_tipo_strumento.currentTextChanged.connect(self.aggiornaDefaultNoleggio)
        self.txt_prezzo_strumento.textChanged.connect(self.aggiornaDefaultNoleggio)

    # metodo per aggiornare il prezzo di noleggio giornaliero di default in base al tipo di strumento selezionate e al prezzo di acquisto inserito
    def aggiornaDefaultNoleggio(self):
        categoria = self._gestore.trovaTipo(self.combo_tipo_strumento.currentText())    # trova la categoria corrispondente al tipo di strumento selezionato nel menù a tendina
        testo_prezzo = self.txt_prezzo_strumento.text().strip() # ottiene il prezzo di acquisto inserito e rimuove spazi bianchi all'inizio e alla fine
        prezzo = None   # inizializza la variabile prezzo a None, che verrà utilizzata per calcolare la stima del prezzo di noleggio giornaliero
        if testo_prezzo:    # se il prezzo di acquisto è stato inserito lo converte in un numero decimale
            try:
                prezzo = float(testo_prezzo.replace(",", "."))  # converte il prezzo di acquisto in un numero decimale, sostituendo eventuali virgole con punti
            except ValueError:  # se il prezzo di acquisto non è un numero valido, lo imposta a None
                prezzo = None
        if categoria is None or prezzo is None: # se il tipo di strumento selezionato non esiste o il prezzo di acquisto non è valido, errore
            self.label_stima_noleggio.setText("Errore: seleziona un tipo valido e inserisci un prezzo di acquisto valido")
            return
        stima = categoria.stimaNoleggioGiornaliero(prezzo)  # calcola la stima del prezzo di noleggio giornaliero in base al tipo di strumento selezionato e al prezzo di acquisto inserito
        self.label_stima_noleggio.setText(f"Stima noleggio giornaliero (quota del tipo '{categoria.getNomeTipo()}' {categoria.getQuotaNoleggio() * 100:g}%/giorno): {prezzo:.2f} € x {categoria.getQuotaNoleggio():g} = {stima:.2f} € al giorno. Il prezzo qui sopra lo puoi cambiare a piacimento.")
        default = str(stima)    # converte la stima del prezzo di noleggio giornaliero in una stringa
        attuale = self.txt_prezzo_noleggio.text().strip()   # ottiene il prezzo di noleggio giornaliero inserito e rimuove spazi all'inizio e alla fine
        if attuale == "" or attuale == self._ultimo_default_noleggio:   # se il prezzo di noleggio giornaliero inserito è vuoto o uguale all'ultimo prezzo di noleggio giornaliero di default, lo aggiorna con la nuova stima
            self.txt_prezzo_noleggio.setText(default)
        self._ultimo_default_noleggio = default # aggiorna l'ultimo prezzo di noleggio giornaliero di default con la nuova stima

    # metodo per confermare l'aggiunta dello strumento selezionato
    def conferma_aggiunta(self):
        if not self.txt_nome_strumento.text().strip():  # se il nome dello strumento da aggiungere è vuoto, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci il nome dello strumento")
            return
        if not self.combo_tipo_strumento.currentText(): # se il tipo di strumento da aggiungere non è selezionato, errore
            QMessageBox.warning(self, "Attenzione", "Non esiste nessun tipo: creane uno nuovo prima")
            return
        if not self.txt_quantita.text().strip():    # se la quantità disponibile dello strumento da aggiungere è vuota, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci la quantita'")
            return
        if not controllaNumero(self.txt_quantita, True, "quantita' disponibile"):   # se la quantità disponibile dello strumento da aggiungere non è un numero valido, errore
            return
        if not self.txt_prezzo_strumento.text().strip():    # se il prezzo di acquisto dello strumento da aggiungere è vuoto, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci il prezzo di acquisto")
            return
        if not controllaNumero(self.txt_prezzo_strumento, False, "prezzo di acquisto"): # se il prezzo di acquisto dello strumento da aggiungere non è un numero valido, errore
            return
        if not self.txt_prezzo_noleggio.text().strip(): # se il prezzo di noleggio dello strumento da aggiungere è vuoto, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci il prezzo di noleggio giornaliero")
            return
        if not controllaNumero(self.txt_prezzo_noleggio, False, "prezzo di noleggio giornaliero"):  # se il prezzo di noleggio dello strumento da aggiungere non è un numero valido, errore
            return
        risposta = QMessageBox.question(self, "Conferma", f"Aggiungere lo strumento '{self.txt_nome_strumento.text().strip()}' nello shop?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per l'aggiunta dello strumento
        if risposta == QMessageBox.Yes: # se la risposta è positiva, registra l'aggiunta
            self.registra_aggiunta()

    # metodo per registrare l'aggiunta di uno strumento al catalogo
    def registra_aggiunta(self):
        esito = self._gestore.aggiungiStrumento(self.txt_nome_strumento.text().strip(), self.combo_tipo_strumento.currentText(), self.txt_azienda_strumento.text().strip(), self.txt_quantita.text().strip(), self.txt_prezzo_strumento.text().strip(), self._venditore.getUsername(), self.txt_nome_venditore.text().strip() or None, self.txt_prezzo_noleggio.text().strip())  # chiama il metodo del gestore catalogo per registrare l'aggiunta dello strumento
        self.label_esito.setText(esito) # visualizza l'esito dell'acquisto nella finestra di acquisto
        self.label_esito.setText(esito) # visualizza l'esito dell'aggiunta dello strumento
        self._callback()    # aggiorna il catalogo degli strumenti
        if not esito.startswith("Errore"):  # se lo strumento è stato aggiunto al catalogo correttamente svuota i campi
            self.txt_nome_strumento.clear()
            self.txt_azienda_strumento.clear()
            self.txt_quantita.clear()
            self.txt_prezzo_strumento.clear()
            self.txt_prezzo_noleggio.clear()
            self.aggiornaDefaultNoleggio()

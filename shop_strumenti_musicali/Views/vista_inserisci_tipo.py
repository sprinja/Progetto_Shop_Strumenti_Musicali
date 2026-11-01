from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox)
from PyQt5.QtGui import QDoubleValidator
from Models import CategoriaStrumento
from Views.validazione_campi import controllaNumero

class VistaInserisciTipoStrumento(QWidget):
    # costruttore
    def __init__(self, gestore_catalogo, inserisci_callback):
        super().__init__()
        self._gestore = gestore_catalogo
        self._callback = inserisci_callback
        self.setWindowTitle("Inserisci nuovo tipo di strumento")
        self.resize(560, 480)
        self._buildUI()
        self._connectSegnali()
        self.aggiornaListaTipi()
        self.aggiornaStimaQuota()
        self.controllaTipo()

    # metodo per costruire l'interfaccia grafica della finestra di inserimento tipo di strumento
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tipi di strumenti gia' esistenti:"))
        self.list_tipi_esistenti = QListWidget()    # lista per visualizzare i tipi di strumenti gia' esistenti
        layout.addWidget(self.list_tipi_esistenti)  # aggiunge la lista dei tipi esistenti al layout principale
        layout.addWidget(QLabel("Nuovo tipo (es. violino):"))
        self.txt_nome_nuovo_tipo = QLineEdit()  # campo di testo per inserire il nome del nuovo tipo di strumento
        self.txt_nome_nuovo_tipo.setPlaceholderText("es. violino")    # esempio di nome valido
        layout.addWidget(self.txt_nome_nuovo_tipo)   # aggiunge il campo di testo del nuovo tipo al layout principale
        rigaQuota = QHBoxLayout()  # layout per la riga contenente l'etichetta e il campo di testo per inserire la quota di noleggio
        rigaQuota.addWidget(QLabel("Quota di noleggio (% del prezzo al giorno):"))
        self.txt_quota_noleggio = QLineEdit()    # campo di testo per inserire la quota di noleggio giornaliera in percentuale
        self.txt_quota_noleggio.setPlaceholderText("es. 0.2")    # esempio di quota valida
        self.txt_quota_noleggio.setValidator(QDoubleValidator(0.0, 100.0, 4, self))
        self.txt_quota_noleggio.setText(f"{round(CategoriaStrumento.QUOTA_NOLEGGIO_DEFAULT * 100, 4):g}") # imposta la quota predefinita di noleggio convertita in percentuale
        rigaQuota.addWidget(self.txt_quota_noleggio)
        layout.addLayout(rigaQuota) # aggiunge la riga contenente la quota di noleggio al layout principale
        self.label_stima_quota = QLabel("")    # etichetta per visualizzare la stima del prezzo di noleggio giornaliero
        self.label_stima_quota.setWordWrap(True)
        layout.addWidget(self.label_stima_quota)   # aggiunge l'etichetta con la stima al layout principale
        layout.addWidget(QLabel("Il tipo va creato PRIMA di poter inserire uno strumento di quel tipo. Non e' possibile creare due volte lo stesso tipo. La quota viene creata insieme al tipo e serve a stimare il prezzo di noleggio giornaliero."))
        pulsanti = QHBoxLayout()   # layout per i pulsanti per confermare l'inserimento del nuovo tipo o chiudere la finestra
        self.btn_conferma = QPushButton("Conferma inserimento")
        self.btn_chiudi = QPushButton("Chiudi")
        pulsanti.addWidget(self.btn_conferma)
        pulsanti.addWidget(self.btn_chiudi)
        layout.addLayout(pulsanti) # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito dell'inserimento del nuovo tipo
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)  # aggiunge l'etichetta per visualizzare l'esito dell'inserimento al layout principale
        self.setLayout(layout)  # imposta il layout principale della finestra di inserimento tipo di strumento

    # metodo per connettere i segnali dei widget alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_conferma.clicked.connect(self.conferma_inserimento)
        self.btn_chiudi.clicked.connect(self.close)
        self.txt_nome_nuovo_tipo.textChanged.connect(self.controllaTipo)
        self.txt_quota_noleggio.textChanged.connect(self.aggiornaStimaQuota)

    # metodo per aggiornare l'etichetta con la stima del prezzo di noleggio giornaliero in base alla quota inserita
    def aggiornaStimaQuota(self):
        percentuale = self.txt_quota_noleggio.text().strip().replace(",", ".")  # ottiene la quota inserita, sostituisce la virgola col punto e rimuove spazi bianchi
        try:
            p = float(percentuale)  # converte la quota in numero decimale
        except ValueError:  # se la quota non e' un numero, errore
            self.label_stima_quota.setText("La quota va scritta come numero (es. 0.2 = 0,2% del prezzo al giorno)")  # scrive che la quota va scritta come numero
            return
        esempio = 500.0    # prezzo dello strumento usato per la stima
        stima = round(esempio * p / 100, 2)    # calcola il prezzo di noleggio giornaliero: prezzo dello strumento per la quota diviso 100
        self.label_stima_quota.setText(f"Stima: con quota {p:g}%/giorno uno strumento da {esempio:.2f} € costerebbe {stima:.2f} € al giorno")  # visualizza la stima del prezzo di noleggio giornaliero

    # metodo per ottenere la quota di noleggio scelta, restituisce nessuna se la quota non e' valida
    def _quotaScelta(self):
        if not controllaNumero(self.txt_quota_noleggio, False, "quota di noleggio"):    # se la quota non e' un numero valido, errore
            return None
        percentuale = float(self.txt_quota_noleggio.text().strip().replace(",", "."))   # ottiene la quota inserita, sostituisce la virgola col punto e la converte in numero decimale
        if percentuale <= 0:    # se la quota non e' maggiore di zero, errore
            QMessageBox.warning(self, "Attenzione", "La quota di noleggio deve essere maggiore di zero")
            return None
        return percentuale / 100    # restituisce la quota convertita da percentuale a frazione

    # metodo per controllare se il tipo inserito esiste gia', disattiva il pulsante di conferma se esiste gia'
    def controllaTipo(self):
        tipo = self.txt_nome_nuovo_tipo.text().strip().lower()   # ottiene il nome del tipo inserito, minuscolo e senza spazi bianchi all'inizio e alla fine
        if tipo and self._gestore.trovaTipo(tipo) is not None:   # se il tipo esiste gia', disattiva il pulsante di conferma e segnalalo
            self.btn_conferma.setEnabled(False)
            self.label_esito.setText(f"Esiste gia' questo tipo di strumenti ('{tipo}'): non verra' ricreato.")    # scrive che il tipo esiste gia' e non verra' ricreato
            return False
        self.btn_conferma.setEnabled(True)   # altrimenti, se il tipo non esiste, attiva il pulsante di conferma
        if not self.label_esito.text().startswith("Creazione"):  # se il messaggio di esito non indica una creazione riuscita, svuota l'etichetta dell'esito
            self.label_esito.setText("")
        return True

    # metodo per aggiornare la lista con i tipi di strumenti gia' esistenti
    def aggiornaListaTipi(self):
        self.list_tipi_esistenti.clear()  # svuota la lista dei tipi esistenti
        tipi = self._gestore.elencaTipi() # ottiene l'elenco dei tipi di strumenti esistenti
        for categoria in tipi:  # ciclo per aggiungere ogni tipo esistente alla lista
            self.list_tipi_esistenti.addItem(str(categoria))
        if not tipi:    # se non ci sono tipi presenti, segnalalo nella lista
            self.list_tipi_esistenti.addItem("Nessun tipo presente")

    # metodo per confermare l'inserimento del nuovo tipo di strumento
    def conferma_inserimento(self):
        tipo = self.txt_nome_nuovo_tipo.text().strip()   # ottiene il nome del tipo inserito e rimuove spazi bianchi all'inizio e alla fine
        if not tipo:    # se il nome del tipo non e' stato inserito, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci il nome del nuovo tipo")
            return
        quota = self._quotaScelta() # ottiene la quota di noleggio scelta
        if quota is None:   # se la quota non e' valida, errore
            return
        if not self.controllaTipo():    # se il tipo esiste gia', errore
            QMessageBox.information(self, "Tipo gia' esistente", self.label_esito.text())   # mostra un messaggio di informazione che il tipo esiste gia'
            return
        risposta = QMessageBox.question(self, "Conferma", f"Creare il tipo '{tipo}' con quota {quota * 100:g}%/giorno?", QMessageBox.Yes | QMessageBox.No)   # mostra un messaggio di conferma per la creazione del nuovo tipo di strumento
        if risposta == QMessageBox.Yes: # se la risposta è positiva, registra il nuovo tipo
            self.registra_inserimento()

    # metodo per registrare il nuovo tipo di strumento
    def registra_inserimento(self):
        quota = self._quotaScelta() # ottiene la quota di noleggio scelta
        if quota is None:   # se la quota non e' valida, errore
            return
        esito = self._gestore.inserisciTipo(self.txt_nome_nuovo_tipo.text(), quota)    # chiama il metodo del gestore catalogo per inserire il nuovo tipo di strumento con la sua quota
        self.label_esito.setText(esito) # visualizza l'esito dell'inserimento nella finestra di inserimento tipo di strumento
        if not esito.startswith("Errore") and "gia' esistente" not in esito:   # se il tipo e' stato creato correttamente, svuota il campo del nome del tipo
            self.txt_nome_nuovo_tipo.clear()
        self.aggiornaListaTipi()    # aggiorna la lista dei tipi esistenti
        self.controllaTipo()    # ricontrolla se il tipo inserito esiste gia'
        self._callback()    # aggiorna la lista dei tipi nella finestra principale

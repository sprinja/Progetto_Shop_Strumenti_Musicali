from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)
from Services import GestoreUtenti, GestoreAmministratore

class VistaAccesso(QWidget):
    # costruttore della finestra di accesso
    def __init__(self, gestore_utenti: GestoreUtenti, gestore_amministratore: GestoreAmministratore, apri_finestra):
        super().__init__()
        self._gestore_utenti = gestore_utenti
        self._gestore_amministratore = gestore_amministratore
        self._apri = apri_finestra
        self.setWindowTitle("Shop Strumenti Musicali - Scegli l'accesso")
        self.resize(430, 330)
        self._buildUI()
        self._connectSegnali()

    # metodo per costruire l'interfaccia grafica della finestra di accesso
    def _buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Scegli l'accesso:")) 
        self.combo_tipo_utente = QComboBox() # combox per selezionare il tipo di utente
        self.combo_tipo_utente.addItems(["Compratore", "Venditore", "Amministratore"])
        layout.addWidget(self.combo_tipo_utente)    # aggiunge la combox al layout principale
        rigaUsername = QHBoxLayout()
        rigaUsername.addWidget(QLabel("Nome utente:"))
        self.txt_username = QLineEdit() # campo di testo per inserire il nome utente
        self.txt_username.setPlaceholderText("es. mario.rossi") # esempio di testo visualizzato
        rigaUsername.addWidget(self.txt_username)
        layout.addLayout(rigaUsername)  # aggiunge la riga del nome utente al layout principale
        rigaPassword = QHBoxLayout()
        rigaPassword.addWidget(QLabel("Password:"))
        self.txt_password = QLineEdit() # campo di testo per inserire la password
        self.txt_password.setPlaceholderText("almeno 5 caratteri, un numero, una maiuscola e una minuscola")    # regole da seguire per la password
        self.txt_password.setEchoMode(QLineEdit.Password)
        rigaPassword.addWidget(self.txt_password)
        layout.addLayout(rigaPassword)  # aggiunge la riga della password al layout principale
        pulsanti = QHBoxLayout()    # layout per i pulsanti per il login e per la registrazione
        self.btn_login = QPushButton("Login")
        self.btn_registrati = QPushButton("Registrati")
        pulsanti.addWidget(self.btn_login)
        pulsanti.addWidget(self.btn_registrati)
        layout.addLayout(pulsanti)  # aggiunge i pulsanti al layout principale
        self.label_esito = QLabel("")   # etichetta per visualizzare l'esito del login o della registrazione
        self.label_esito.setWordWrap(True)
        layout.addWidget(self.label_esito)
        self.setLayout(layout)  # imposta il layout principale della finestra di accesso

    # metodo per connettere i segnali dei pulsanti e del campo password alle rispettive funzioni
    def _connectSegnali(self):
        self.btn_login.clicked.connect(self.esegui_login)  
        self.btn_registrati.clicked.connect(self.registra_utente)
        self.txt_password.returnPressed.connect(self.esegui_login)

    # metodo per eseguire il login dell'utente in base al tipo selezionato nella combobox
    def esegui_login(self):
        tipo = self.combo_tipo_utente.currentText() # ottiene il tipo di utente selezionato nella combobox
        username = self.txt_username.text().strip() # ottiene il nome utente inserito e rimuove spazi bianchi all'inizio e alla fine del nome utente inserito
        password = self.txt_password.text().strip() # ottiene la password inserita e rimuove spazi bianchi all'inizio e alla fine
        if not username or not password:    # se il nome utente o la password sono vuoti, errore
            QMessageBox.warning(self, "Attenzione", "Inserisci nome utente e password")
            return
        if tipo == "Amministratore":    # se il tipo di utente è Amministratore, verifica l'accesso da amministratore
            esito, admin = self._gestore_amministratore.verificaAccesso(username, password)
            utente = admin  # se l'accesso è riuscito l'utente sarà ora l'amministratore
        else:   # altrimenti verifica l'accesso da compratore o da venditore
            esito, utente = self._gestore_utenti.verificaLogin(tipo, username, password)
        self.label_esito.setText(esito) # visualizza l'esito del login
        if utente is None:  # se l'utente non è stato trovato, errore
            QMessageBox.warning(self, "Accesso non riuscito", esito)
            return
        self._apri(tipo.lower(), utente)    # apre la finestra dell'applicazione corrispondente all'utente loggato

    # metodo per registrare un nuovo utente in base al tipo selezionato nella combobox
    def registra_utente(self):
        tipo = self.combo_tipo_utente.currentText() # ottiene il tipo di utente selezionato nella combobox
        if tipo == "Amministratore":    # se il tipo di utente è amministratore, errore perchè non ci si può registrare come amministratore
            QMessageBox.warning(self, "Attenzione", "Non e' possibile registrarsi come amministratore:\n le credenziali devono essere note a priori")
            return
        username = self.txt_username.text().strip() # ottiene il nome utente inserito e rimuove spazi bianchi all'inizio e alla fine del nome utente inserito
        password = self.txt_password.text().strip() # ottiene la password inserita e rimuove spazi bianchi all'inizio e alla fine
        esito = self._gestore_utenti.verificaRegistrazione(tipo, username, password)    # verifica la validità dei dati inseriti per la registrazione
        self.label_esito.setText(esito) # visualizza l'esito della registrazione
        if esito.startswith("Errore"):  # se l'esito della registrazione inizia con Errore, visualizza un messaggio di errore
            QMessageBox.warning(self, "Registrazione non riuscita", esito)
        else:   # altrimenti visualizza un messagggio di conferma della registrazione
            QMessageBox.information(self, "Registrazione", esito)
            self.update_ui()    # aggiorna l'interfaccia grafica della finestra di accesso

    # metodo per aggiornare l'interfaccia grafica della finestra di accesso con valori di default
    def update_ui(self):
        self.txt_username.clear()
        self.txt_password.clear()
        self.label_esito.setText("")
        self.txt_username.setFocus()

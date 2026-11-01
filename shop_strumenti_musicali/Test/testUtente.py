import unittest
from Models import Utente

class TestUtente(unittest.TestCase):
    # Fase di Arrange: si crea un utente valido riutilizzabile nei test
    def setUp(self):
        self.utente = Utente("mario.rossi", "Mario123")

    # Verifica che il costruttore assegni correttamente i parametri e i valori di default
    def test_stato_iniziale(self):
        self.assertEqual(self.utente.getUsername(), "mario.rossi")
        self.assertEqual(self.utente.getPassword(), "Mario123")
        self.assertEqual(self.utente.getTipoUtente(), "Utente")
    
    # Verifica che l'username venga modificato correttamente (compresi gli spazi rimossi)
    def test_set_username_valido(self):
        self.utente.setUsername("  luigi.verdi  ")
        self.assertEqual(self.utente.getUsername(), "luigi.verdi")
        
    # Verifica la password venga modificata correttamente
    def test_set_password_valida(self):
        self.utente.setPassword("Luigi123")
        self.assertEqual(self.utente.getPassword(), "Luigi123")

    # Verifica che il costruttore sollevi TypeError se i tipi non sono stringhe
    def test_tipo_errato_raises(self):
        with self.assertRaises(TypeError):
            Utente(123, "Mario123")  # username non stringa
        with self.assertRaises(TypeError):
            Utente("mario.rossi", 123)  # password non stringa

    # Verifica che i setter sollevino ValueError con stringhe vuote o non valide
    def test_valori_setter_errati_raises(self):
        with self.assertRaises(ValueError):
            self.utente.setUsername("")
        with self.assertRaises(ValueError):
            self.utente.setUsername("   ")  # solo spazi
        with self.assertRaises(ValueError):
            self.utente.setPassword("")

    # Verifica il metodo di controllo delle credenziali
    def test_credenziali_corrette(self):
        # Credenziali giuste
        self.assertTrue(self.utente.credenzialiCorrette("mario.rossi", "Mario123"))
        # Password errata
        self.assertFalse(self.utente.credenzialiCorrette("mario.rossi", "sbagliata"))
        # Username errato
        self.assertFalse(self.utente.credenzialiCorrette("altro_utente", "Mario123"))

    # Verifica la serializzazione dell'oggetto in dizionario
    def test_to_dict(self):
        i = self.utente.toDict()
        self.assertEqual(i["username"], "mario.rossi")
        self.assertEqual(i["password"], "Mario123")

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        i = {"username": "anna.neri", "password": "securepass"}
        utente_creato = Utente.fromDict(i)
        
        self.assertIsInstance(utente_creato, Utente)
        self.assertEqual(utente_creato.getUsername(), "anna.neri")
        self.assertEqual(utente_creato.getPassword(), "securepass")

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.utente), "mario.rossi")

if __name__ == "__main__":
    unittest.main()
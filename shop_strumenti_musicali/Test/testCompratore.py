import unittest
from Models import Utente, Compratore

class TestCompratore(unittest.TestCase):
    # Fase di Arrange: si crea un compratore valido riutilizzabile nei test
    def setUp(self):
        self.compratore = Compratore("anna.neri", "Anna123")

    # Verifica che il compratore sia una classe figlia di Utente con il proprio tipo di utente
    def test_stato_iniziale(self):
        self.assertIsInstance(self.compratore, Utente)
        self.assertEqual(self.compratore.getUsername(), "anna.neri")
        self.assertEqual(self.compratore.getPassword(), "Anna123")
        self.assertEqual(self.compratore.getTipoUtente(), "Compratore")

    # Verifica che l'username venga modificato correttamente dai metodi ereditati (compresi gli spazi rimossi)
    def test_set_username_valido(self):
        self.compratore.setUsername("  luigi_verdi  ")
        self.assertEqual(self.compratore.getUsername(), "luigi_verdi")

    # Verifica che la password venga modificata correttamente dai metodi ereditati
    def test_set_password_valida(self):
        self.compratore.setPassword("Luigi123")
        self.assertEqual(self.compratore.getPassword(), "Luigi123")

    # Verifica che il costruttore ereditato sollevi TypeError se i tipi non sono stringhe
    def test_tipo_errato_raises(self):
        with self.assertRaises(TypeError):
            Compratore(123, "Anna123")  # username non stringa
        with self.assertRaises(TypeError):
            Compratore("anna.neri", 123)  # password non stringa

    # Verifica che i setter ereditati sollevino ValueError con stringhe vuote o non valide
    def test_valori_setter_errati_raises(self):
        with self.assertRaises(ValueError):
            self.compratore.setUsername("")
        with self.assertRaises(ValueError):
            self.compratore.setUsername("   ")  # solo spazi
        with self.assertRaises(ValueError):
            self.compratore.setPassword("")

    # Verifica il metodo ereditato di controllo delle credenziali
    def test_credenziali_corrette(self):
        # Credenziali giuste
        self.assertTrue(self.compratore.credenzialiCorrette("anna.neri", "Anna123"))
        # Password errata
        self.assertFalse(self.compratore.credenzialiCorrette("anna.neri", "sbagliata"))
        # Username errato
        self.assertFalse(self.compratore.credenzialiCorrette("altro_utente", "Anna123"))

    # Verifica la serializzazione dell'oggetto in dizionario con il metodo ereditato
    def test_to_dict(self):
        i = self.compratore.toDict()
        self.assertEqual(i["username"], "anna.neri")
        self.assertEqual(i["password"], "Anna123")

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        i = {"username": "mario.rossi", "password": "securepass"}
        compratore_creato = Compratore.fromDict(i)
        self.assertIsInstance(compratore_creato, Compratore)
        self.assertEqual(compratore_creato.getUsername(), "mario.rossi")
        self.assertEqual(compratore_creato.getTipoUtente(), "Compratore")

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.compratore), "Compratore anna.neri")

if __name__ == "__main__":
    unittest.main()

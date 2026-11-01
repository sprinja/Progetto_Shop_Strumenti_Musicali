import unittest
from Models import Utente, Venditore

class TestVenditore(unittest.TestCase):
    # Fase di Arrange: si crea un venditore valido riutilizzabile nei test
    def setUp(self):
        self.venditore = Venditore("mario.rossi", "Mario123")

    # Verifica che il venditore sia una classe figlia di Utente con il proprio tipo di utente
    def test_stato_iniziale(self):
        self.assertIsInstance(self.venditore, Utente)
        self.assertEqual(self.venditore.getUsername(), "mario.rossi")
        self.assertEqual(self.venditore.getPassword(), "Mario123")
        self.assertEqual(self.venditore.getTipoUtente(), "Venditore")

    # Verifica che l'username venga modificato correttamente dai metodi ereditati (compresi gli spazi rimossi)
    def test_set_username_valido(self):
        self.venditore.setUsername("  luigi_verdi  ")
        self.assertEqual(self.venditore.getUsername(), "luigi_verdi")

    # Verifica che la password venga modificata correttamente dai metodi ereditati
    def test_set_password_valida(self):
        self.venditore.setPassword("Luigi123")
        self.assertEqual(self.venditore.getPassword(), "Luigi123")

    # Verifica che il costruttore ereditato sollevi TypeError se i tipi non sono stringhe
    def test_tipo_errato_raises(self):
        with self.assertRaises(TypeError):
            Venditore(123, "Mario123")  # username non stringa
        with self.assertRaises(TypeError):
            Venditore("mario.rossi", 123)  # password non stringa

    # Verifica che i setter ereditati sollevino ValueError con stringhe vuote o non valide
    def test_valori_setter_errati_raises(self):
        with self.assertRaises(ValueError):
            self.venditore.setUsername("")
        with self.assertRaises(ValueError):
            self.venditore.setUsername("   ")  # solo spazi
        with self.assertRaises(ValueError):
            self.venditore.setPassword("")

    # Verifica il metodo ereditato di controllo delle credenziali
    def test_credenziali_corrette(self):
        # Credenziali giuste
        self.assertTrue(self.venditore.credenzialiCorrette("mario.rossi", "Mario123"))
        # Password errata
        self.assertFalse(self.venditore.credenzialiCorrette("mario.rossi", "sbagliata"))
        # Username errato
        self.assertFalse(self.venditore.credenzialiCorrette("altro_utente", "Mario123"))

    # Verifica la serializzazione dell'oggetto in dizionario con il metodo ereditato
    def test_to_dict(self):
        i = self.venditore.toDict()
        self.assertEqual(i["username"], "mario.rossi")
        self.assertEqual(i["password"], "Mario123")

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        i = {"username": "anna.neri", "password": "securepass"}
        venditore_creato = Venditore.fromDict(i)
        self.assertIsInstance(venditore_creato, Venditore)
        self.assertEqual(venditore_creato.getUsername(), "anna.neri")
        self.assertEqual(venditore_creato.getTipoUtente(), "Venditore")

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.venditore), "Venditore mario.rossi")

if __name__ == "__main__":
    unittest.main()

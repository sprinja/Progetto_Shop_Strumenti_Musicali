import unittest
from Models import Utente, Amministratore

class TestAmministratore(unittest.TestCase):
    # Fase di Arrange: si crea un amministratore valido riutilizzabile nei test
    def setUp(self):
        self.amministratore = Amministratore("admin", "Admin123")

    # Verifica che l'amministratore sia una classe figlia di Utente con il proprio tipo di utente
    def test_stato_iniziale(self):
        self.assertIsInstance(self.amministratore, Utente)
        self.assertEqual(self.amministratore.getUsername(), "admin")
        self.assertEqual(self.amministratore.getPassword(), "Admin123")
        self.assertEqual(self.amministratore.getTipoUtente(), "Amministratore")

    # Verifica che l'username venga modificato correttamente dai metodi ereditati (compresi gli spazi rimossi)
    def test_set_username_valido(self):
        self.amministratore.setUsername("  luigi_verdi  ")
        self.assertEqual(self.amministratore.getUsername(), "luigi_verdi")

    # Verifica che la password venga modificata correttamente dai metodi ereditati
    def test_set_password_valida(self):
        self.amministratore.setPassword("Luigi123")
        self.assertEqual(self.amministratore.getPassword(), "Luigi123")

    # Verifica che il costruttore ereditato sollevi TypeError se i tipi non sono stringhe
    def test_tipo_errato_raises(self):
        with self.assertRaises(TypeError):
            Amministratore(123, "Admin123")  # username non stringa
        with self.assertRaises(TypeError):
            Amministratore("admin", 123)  # password non stringa

    # Verifica che i setter ereditati sollevino ValueError con stringhe vuote o non valide
    def test_valori_setter_errati_raises(self):
        with self.assertRaises(ValueError):
            self.amministratore.setUsername("")
        with self.assertRaises(ValueError):
            self.amministratore.setUsername("   ")  # solo spazi
        with self.assertRaises(ValueError):
            self.amministratore.setPassword("")

    # Verifica il metodo ereditato di controllo delle credenziali
    def test_credenziali_corrette(self):
        # Credenziali giuste
        self.assertTrue(self.amministratore.credenzialiCorrette("admin", "Admin123"))
        # Password errata
        self.assertFalse(self.amministratore.credenzialiCorrette("admin", "sbagliata"))
        # Username errato
        self.assertFalse(self.amministratore.credenzialiCorrette("altro_utente", "Admin123"))

    # Verifica la serializzazione dell'oggetto in dizionario con il metodo ereditato
    def test_to_dict(self):
        i = self.amministratore.toDict()
        self.assertEqual(i["username"], "admin")
        self.assertEqual(i["password"], "Admin123")

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        i = {"username": "mario.rossi", "password": "securepass"}
        amministratore_creato = Amministratore.fromDict(i)
        self.assertIsInstance(amministratore_creato, Amministratore)
        self.assertEqual(amministratore_creato.getUsername(), "mario.rossi")
        self.assertEqual(amministratore_creato.getTipoUtente(), "Amministratore")

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.amministratore), "Amministratore admin")

if __name__ == "__main__":
    unittest.main()

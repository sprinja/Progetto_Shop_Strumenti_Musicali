import unittest
from Models import CategoriaStrumento

class TestCategoriaStrumento(unittest.TestCase):
    # Fase di Arrange: si crea una categoria valida riutilizzabile nei test
    def setUp(self):
        self.categoria = CategoriaStrumento("  Chitarra ", 0.15)

    # Verifica che il costruttore tolga gli spazi e renda minuscolo il nome del tipo
    def test_stato_iniziale(self):
        self.assertEqual(self.categoria.getNomeTipo(), "chitarra")
        self.assertEqual(self.categoria.getQuotaNoleggio(), 0.15)

    # Verifica che senza quota venga usata quella di default del 10%
    def test_quota_default(self):
        categoria = CategoriaStrumento("batteria")
        self.assertEqual(categoria.getQuotaNoleggio(), CategoriaStrumento.QUOTA_NOLEGGIO_DEFAULT)
        self.assertEqual(categoria.getQuotaNoleggio(), 0.1)

    # Verifica che il costruttore sollevi ValueError se il nome del tipo è vuoto o non è una stringa
    def test_nome_errato_raises(self):
        with self.assertRaises(ValueError):
            CategoriaStrumento("")  # nome vuoto
        with self.assertRaises(ValueError):
            CategoriaStrumento("   ")  # solo spazi
        with self.assertRaises(ValueError):
            CategoriaStrumento(123)  # nome non stringa

    # Verifica che il costruttore sollevi TypeError se la quota non è un numero positivo
    def test_quota_errata_raises(self):
        with self.assertRaises(TypeError):
            CategoriaStrumento("chitarra", 0)  # quota uguale a zero
        with self.assertRaises(TypeError):
            CategoriaStrumento("chitarra", -0.5)  # quota negativa
        with self.assertRaises(TypeError):
            CategoriaStrumento("chitarra", "dieci")  # quota non numero

    # Verifica il setter della quota di noleggio
    def test_set_quota_noleggio(self):
        self.categoria.setQuotaNoleggio(0.25)
        self.assertEqual(self.categoria.getQuotaNoleggio(), 0.25)
        with self.assertRaises(TypeError):
            self.categoria.setQuotaNoleggio(0)  # quota uguale a zero
        with self.assertRaises(TypeError):
            self.categoria.setQuotaNoleggio("abc")  # quota non numero

    # Verifica il calcolo del prezzo di noleggio giornaliero dal prezzo dello strumento
    def test_stima_noleggio_giornaliero(self):
        self.assertEqual(self.categoria.stimaNoleggioGiornaliero(450), 67.5)

    # Verifica la serializzazione dell'oggetto in dizionario
    def test_to_dict(self):
        i = self.categoria.toDict()
        self.assertEqual(i["nome_tipo"], "chitarra")
        self.assertEqual(i["quota_noleggio"], 0.15)

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        i = {"nome_tipo": "Violino", "quota_noleggio": 0.2}
        categoria_creato = CategoriaStrumento.fromDict(i)
        self.assertIsInstance(categoria_creato, CategoriaStrumento)
        self.assertEqual(categoria_creato.getNomeTipo(), "violino")
        self.assertEqual(categoria_creato.getQuotaNoleggio(), 0.2)

    # Verifica che dal dizionario senza quota venga usata quella di default
    def test_from_dict_quota_default(self):
        i = {"nome_tipo": "flauto"}
        categoria_creato = CategoriaStrumento.fromDict(i)
        self.assertEqual(categoria_creato.getQuotaNoleggio(), 0.1)

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.categoria), "chitarra (noleggio 15.00%/giorno)")

if __name__ == "__main__":
    unittest.main()

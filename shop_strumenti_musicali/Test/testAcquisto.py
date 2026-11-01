import unittest
from datetime import date
from Models import Acquisto, Compratore, Utente

class TestAcquisto(unittest.TestCase):
    # Fase di Arrange: si crea un acquisto valido riutilizzabile nei test
    def setUp(self):
        self.compratore = Compratore("anna.neri", "Anna123")
        self.dati_strumento = {"id": "S1", "nome": "Chitarra", "prezzo": 450.0}
        self.acquisto = Acquisto("A1", self.compratore, self.dati_strumento, 2, "2026-10-01")

    # Verifica che il costruttore assegni i parametri forniti
    def test_stato_iniziale(self):
        self.assertEqual(self.acquisto.getId(), "A1")
        self.assertIs(self.acquisto.getCompratore(), self.compratore)
        self.assertEqual(self.acquisto.getQuantita(), 2)
        self.assertEqual(self.acquisto.getData(), "2026-10-01")
        self.assertEqual(self.acquisto.getStrumento(), {"id": "S1", "nome": "Chitarra", "prezzo": 450.0})

    # Verifica che senza data venga usata quella odierna
    def test_data_default(self):
        acquisto = Acquisto("A2", self.compratore, self.dati_strumento, 1)
        self.assertEqual(acquisto.getData(), str(date.today()))

    # Verifica che i dati dello strumento vengano salvati come copia al momento dell'acquisto
    def test_snapshot_strumento(self):
        self.dati_strumento["prezzo"] = 999.0
        self.assertEqual(self.acquisto.getPrezzoUnitario(), 450.0)

    # Verifica che il compratore debba essere un oggetto Compratore
    def test_compratore_errato_raises(self):
        with self.assertRaises(TypeError):
            Acquisto("A1", Utente("anna.neri", "Anna123"), self.dati_strumento, 1)  # utente di tipo base
        with self.assertRaises(TypeError):
            Acquisto("A1", "anna.neri", self.dati_strumento, 1)  # compratore non è un oggetto

    # Verifica che la quantità acquistata debba essere positiva
    def test_quantita_errata_raises(self):
        with self.assertRaises(ValueError):
            Acquisto("A1", self.compratore, self.dati_strumento, 0)  # quantità uguale a zero
        with self.assertRaises(ValueError):
            Acquisto("A1", self.compratore, self.dati_strumento, -3)  # quantità negativa
        with self.assertRaises(ValueError):
            Acquisto("A1", self.compratore, self.dati_strumento, "abc")  # quantità non numero

    # Verifica che una quantità scritta come testo venga convertita in numero intero
    def test_quantita_da_testo(self):
        acquisto = Acquisto("A2", self.compratore, self.dati_strumento, "3")
        self.assertEqual(acquisto.getQuantita(), 3)
        self.assertIsInstance(acquisto.getQuantita(), int)

    # Verifica il prezzo unitario e il totale dell'acquisto
    def test_prezzo_e_totale(self):
        self.assertEqual(self.acquisto.getPrezzoUnitario(), 450.0)
        self.assertEqual(self.acquisto.getTotale(), 900.0)
        acquisto_senza_prezzo = Acquisto("A3", self.compratore, {"nome": "Plettro"}, 4)
        self.assertEqual(acquisto_senza_prezzo.getPrezzoUnitario(), 0.0)
        self.assertEqual(acquisto_senza_prezzo.getTotale(), 0.0)

    # Verifica la serializzazione dell'oggetto in dizionario
    def test_to_dict(self):
        i = self.acquisto.toDict()
        self.assertEqual(i["id"], "A1")
        self.assertEqual(i["compratore"], "anna.neri")
        self.assertEqual(i["quantita"], 2)
        self.assertEqual(i["data_acquisto"], "2026-10-01")
        self.assertEqual(i["strumento"]["nome"], "Chitarra")

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        acquisto_creato = Acquisto.fromDict(self.acquisto.toDict(), self.compratore)
        self.assertIsInstance(acquisto_creato, Acquisto)
        self.assertEqual(acquisto_creato.getId(), "A1")
        self.assertEqual(acquisto_creato.getQuantita(), 2)
        self.assertEqual(acquisto_creato.getData(), "2026-10-01")

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.acquisto), "2026-10-01 | Chitarra x2 | 900.00 €")

if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import date, timedelta
from Models import Compratore, Noleggio

class TestNoleggio(unittest.TestCase):
    # Fase di Arrange: si crea un noleggio valido riutilizzabile nei test
    def setUp(self):
        self.compratore = Compratore("anna.neri", "Anna123")
        self.dati_strumento = {"id": "S1", "nome": "Batteria", "venditore": "mario.rossi", "prezzo_noleggio_giornaliero": 20.0}
        self.noleggio = Noleggio("N1", self.compratore, self.dati_strumento, 1, 3, str(date.today()))

    # Verifica che il costruttore assegni i parametri forniti e il noleggio risulti attivo
    def test_stato_iniziale(self):
        self.assertEqual(self.noleggio.getId(), "N1")
        self.assertIs(self.noleggio.getCompratore(), self.compratore)
        self.assertEqual(self.noleggio.getQuantita(), 1)
        self.assertEqual(self.noleggio.getDurata(), 3)
        self.assertEqual(self.noleggio.getDataInizio(), str(date.today()))
        self.assertIsNone(self.noleggio.getDataRestituzione())
        self.assertTrue(self.noleggio.isAttivo())

    # Verifica che senza data di inizio venga usata quella odierna
    def test_data_default(self):
        noleggio = Noleggio("N2", self.compratore, self.dati_strumento, 1, 2)
        self.assertEqual(noleggio.getDataInizio(), str(date.today()))

    # Verifica che il costruttore rifiuti compratore errato, quantità e durata non valide
    def test_valori_errati_raises(self):
        with self.assertRaises(TypeError):
            Noleggio("N1", "anna.neri", self.dati_strumento, 1, 3)  # compratore non è un oggetto
        with self.assertRaises(ValueError):
            Noleggio("N1", self.compratore, self.dati_strumento, 0, 3)  # quantità uguale a zero
        with self.assertRaises(ValueError):
            Noleggio("N1", self.compratore, self.dati_strumento, -1, 3)  # quantità negativa
        with self.assertRaises(ValueError):
            Noleggio("N1", self.compratore, self.dati_strumento, 1, 0)  # durata uguale a zero
        with self.assertRaises(ValueError):
            Noleggio("N1", self.compratore, self.dati_strumento, 1, -5)  # durata negativa

    # Verifica il calcolo della data di fine noleggio dalla data di inizio e dalla durata
    def test_data_fine(self):
        noleggio = Noleggio("N3", self.compratore, self.dati_strumento, 1, 4, "2026-10-01")
        self.assertEqual(noleggio.getDataFine(), "2026-10-05")

    # Verifica il tempo rimanente di un noleggio appena iniziato
    def test_tempo_rimanente(self):
        noleggio = Noleggio("N4", self.compratore, self.dati_strumento, 1, 5)
        self.assertEqual(noleggio.getTempoRimanente(), 5)
        self.assertFalse(noleggio.isScaduto())

    # Verifica che un noleggio scaduto e non restituito risulti scaduto
    def test_scaduto(self):
        noleggio = Noleggio("N5", self.compratore, self.dati_strumento, 1, 3, str(date.today() - timedelta(days=10)))
        self.assertTrue(noleggio.isAttivo())
        self.assertTrue(noleggio.isScaduto())
        self.assertEqual(noleggio.getTempoRimanente(), -7)

    # Verifica i costi di un noleggio attivo non ancora restituito
    def test_costi_attivo(self):
        self.assertEqual(self.noleggio.getGiorniEffettivi(), 0)
        self.assertEqual(self.noleggio.calcolaCostoMassimo(), 60.0)
        self.assertEqual(self.noleggio.calcolaCostoEffettivo(), 60.0)
        self.assertEqual(self.noleggio.getRimborso(), 0.0)

    # Verifica costi e rimborso con una restituzione anticipata
    def test_restituzione_anticipata(self):
        noleggio = Noleggio("N6", self.compratore, self.dati_strumento, 1, 3, "2026-10-01", "2026-10-02")
        self.assertFalse(noleggio.isAttivo())
        self.assertEqual(noleggio.getGiorniEffettivi(), 1)
        self.assertEqual(noleggio.calcolaCostoEffettivo(), 20.0)
        self.assertEqual(noleggio.getRimborso(), 40.0)

    # Verifica che una restituzione oltre la durata non aumenti il costo massimo
    def test_restituzione_oltre_durata(self):
        noleggio = Noleggio("N7", self.compratore, self.dati_strumento, 1, 3, "2026-10-01", "2026-10-10")
        self.assertEqual(noleggio.getGiorniEffettivi(), 3)
        self.assertEqual(noleggio.calcolaCostoEffettivo(), 60.0)
        self.assertEqual(noleggio.getRimborso(), 0.0)

    # Verifica la restituzione dello strumento e il rimborso, anche ripetuta
    def test_restituisci_strumento(self):
        rimborso = self.noleggio.restituisciStrumento()
        self.assertEqual(rimborso, 40.0)
        self.assertFalse(self.noleggio.isAttivo())
        self.assertEqual(self.noleggio.getDataRestituzione(), str(date.today()))
        self.assertEqual(self.noleggio.restituisciStrumento(), 0.0)

    # Verifica la serializzazione dell'oggetto in dizionario
    def test_to_dict(self):
        i = self.noleggio.toDict()
        self.assertEqual(i["id"], "N1")
        self.assertEqual(i["compratore"], "anna.neri")
        self.assertEqual(i["quantita"], 1)
        self.assertEqual(i["durata_giorni"], 3)
        self.assertIsNone(i["data_restituzione"])

    # Verifica la creazione dell'oggetto tramite il costruttore alternativo
    def test_from_dict(self):
        noleggio_creato = Noleggio.fromDict(self.noleggio.toDict(), self.compratore)
        self.assertIsInstance(noleggio_creato, Noleggio)
        self.assertEqual(noleggio_creato.getId(), "N1")
        self.assertEqual(noleggio_creato.getDataFine(), str(date.today() + timedelta(days=3)))

    # Verifica la rappresentazione in stringa di un noleggio attivo
    def test_str_representation(self):
        atteso = f"{str(date.today())} -> {str(date.today() + timedelta(days=3))} | Batteria x1 | attivo, mancano 3 giorni | 60.00 €"
        self.assertEqual(str(self.noleggio), atteso)

    # Verifica la rappresentazione in stringa di un noleggio terminato
    def test_str_terminato(self):
        noleggio = Noleggio("N8", self.compratore, self.dati_strumento, 1, 3, "2026-10-01", "2026-10-04")
        self.assertEqual(str(noleggio), "2026-10-01 -> 2026-10-04 | Batteria x1 | terminato il 2026-10-04 | 60.00 €")

if __name__ == "__main__":
    unittest.main()

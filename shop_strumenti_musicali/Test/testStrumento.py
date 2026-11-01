import unittest
from Models import CategoriaStrumento, Strumento

class TestStrumento(unittest.TestCase):
    # Fase di Arrange: si crea uno strumento valido riutilizzabile nei test
    def setUp(self):
        self.categoria = CategoriaStrumento("chitarra", 0.1)
        self.strumento = Strumento("S1", "  Chitarra elettrica ", self.categoria, "  Yamaha ", "mario.rossi", 5, 450)

    # Verifica che il costruttore assegni i dati e calcoli il prezzo di noleggio dalla categoria
    def test_stato_iniziale(self):
        self.assertEqual(self.strumento.getId(), "S1")
        self.assertEqual(self.strumento.getNome(), "Chitarra elettrica")
        self.assertIs(self.strumento.getCategoria(), self.categoria)
        self.assertEqual(self.strumento.getTipo(), "chitarra")
        self.assertEqual(self.strumento.getAzienda(), "Yamaha")
        self.assertEqual(self.strumento.getVenditore(), "mario.rossi")
        self.assertEqual(self.strumento.getNomeVenditore(), "mario.rossi")
        self.assertEqual(self.strumento.getQuantita(), 5)
        self.assertEqual(self.strumento.getPrezzo(), 450.0)
        self.assertEqual(self.strumento.getPrezzoNoleggioGiornaliero(), 45.0)

    # Verifica che il prezzo di noleggio scritto a mano accetti anche la virgola decimale
    def test_prezzo_noleggio_scritto(self):
        strumento = Strumento("S2", "Batteria", self.categoria, "Yamaha", "mario.rossi", 3, 600, None, "35,5")
        self.assertEqual(strumento.getPrezzoNoleggioGiornaliero(), 35.5)

    # Verifica che un prezzo di noleggio non positivo causi ValueError
    def test_prezzo_noleggio_errato_raises(self):
        with self.assertRaises(ValueError):
            Strumento("S2", "Batteria", self.categoria, "Yamaha", "mario.rossi", 3, 600, None, 0)  # noleggio uguale a zero
        with self.assertRaises(ValueError):
            Strumento("S2", "Batteria", self.categoria, "Yamaha", "mario.rossi", 3, 600, None, -5)  # noleggio negativo

    # Verifica che il costruttore rifiuti categoria errata, nome vuoto, quantità e prezzo negativi
    def test_valori_errati_raises(self):
        with self.assertRaises(TypeError):
            Strumento("S1", "Chitarra", "chitarra", "Yamaha", "mario.rossi", 5, 450)  # categoria non è una CategoriaStrumento
        with self.assertRaises(ValueError):
            Strumento("S1", "", self.categoria, "Yamaha", "mario.rossi", 5, 450)  # nome vuoto
        with self.assertRaises(ValueError):
            Strumento("S1", "Chitarra", self.categoria, "Yamaha", "mario.rossi", -1, 450)  # quantità negativa
        with self.assertRaises(ValueError):
            Strumento("S1", "Chitarra", self.categoria, "Yamaha", "mario.rossi", 5, -450)  # prezzo negativo

    # Verifica che i setter accettino i valori validi
    def test_setter_validi(self):
        self.strumento.setNome("  Les Paul ")
        self.assertEqual(self.strumento.getNome(), "Les Paul")
        self.strumento.setAzienda("  Gibson ")
        self.assertEqual(self.strumento.getAzienda(), "Gibson")
        self.strumento.setNomeVenditore("  luigi_verdi ")
        self.assertEqual(self.strumento.getNomeVenditore(), "luigi_verdi")
        self.strumento.setPrezzo("455,5")
        self.assertEqual(self.strumento.getPrezzo(), 455.5)
        self.strumento.setQuantita("7")
        self.assertEqual(self.strumento.getQuantita(), 7)
        self.strumento.setCategoria(CategoriaStrumento("batteria"))
        self.assertEqual(self.strumento.getTipo(), "batteria")

    # Verifica che i setter rifiutino i valori non validi
    def test_setter_errati_raises(self):
        with self.assertRaises(ValueError):
            self.strumento.setNome(" ")  # nome vuoto
        with self.assertRaises(ValueError):
            self.strumento.setAzienda("")  # azienda vuota
        with self.assertRaises(ValueError):
            self.strumento.setNomeVenditore("")  # nome del venditore vuoto
        with self.assertRaises(ValueError):
            self.strumento.setPrezzo(-1)  # prezzo negativo
        with self.assertRaises(ValueError):
            self.strumento.setPrezzoNoleggioGiornaliero(0)  # noleggio uguale a zero
        with self.assertRaises(ValueError):
            self.strumento.setPrezzoNoleggioGiornaliero("abc")  # noleggio non numero
        with self.assertRaises(ValueError):
            self.strumento.setQuantita(-2)  # quantità negativa
        with self.assertRaises(TypeError):
            self.strumento.setCategoria("chitarra")  # categoria non è una CategoriaStrumento

    # Verifica l'aggiornamento della quantità con delta positivo e negativo
    def test_aggiorna_quantita(self):
        self.strumento.aggiornaQuantita(3)
        self.assertEqual(self.strumento.getQuantita(), 8)
        self.strumento.aggiornaQuantita(-8)
        self.assertEqual(self.strumento.getQuantita(), 0)
        with self.assertRaises(ValueError):
            self.strumento.aggiornaQuantita(-1)  # quantità insufficiente

    # Verifica il controllo di disponibilità dello strumento
    def test_is_disponibile(self):
        self.assertTrue(self.strumento.isDisponibile())
        self.strumento.setQuantita(0)
        self.assertFalse(self.strumento.isDisponibile())

    # Verifica la serializzazione dell'oggetto in dizionario
    def test_to_dict(self):
        i = self.strumento.toDict()
        self.assertEqual(i["id"], "S1")
        self.assertEqual(i["nome"], "Chitarra elettrica")
        self.assertEqual(i["tipo"], "chitarra")
        self.assertEqual(i["azienda"], "Yamaha")
        self.assertEqual(i["venditore"], "mario.rossi")
        self.assertEqual(i["nome_venditore"], "mario.rossi")
        self.assertEqual(i["quantita"], 5)
        self.assertEqual(i["prezzo"], 450.0)
        self.assertEqual(i["prezzo_noleggio_giornaliero"], 45.0)

    # Verifica la creazione dell'oggetto da dizionario, con e senza nome del venditore
    def test_from_dict(self):
        i = {"id": "S9", "nome": "Violino", "tipo": "chitarra", "azienda": "Yamaha", "venditore": "mario.rossi", "quantita": 2, "prezzo": 300, "prezzo_noleggio_giornaliero": 12.5}
        strumento_creato = Strumento.fromDict(i, self.categoria)
        self.assertIsInstance(strumento_creato, Strumento)
        self.assertEqual(strumento_creato.getNome(), "Violino")
        self.assertEqual(strumento_creato.getNomeVenditore(), "mario.rossi")
        self.assertEqual(strumento_creato.getPrezzoNoleggioGiornaliero(), 12.5)
        i["nome_venditore"] = "luigi.verdi"
        strumento_con_venditore = Strumento.fromDict(i, self.categoria)
        self.assertEqual(strumento_con_venditore.getNomeVenditore(), "luigi.verdi")

    # Verifica la rappresentazione in stringa (__str__)
    def test_str_representation(self):
        self.assertEqual(str(self.strumento), "S1 | Chitarra elettrica | tipo: chitarra | azienda: Yamaha | venditore: mario.rossi | q: 5 | 450.00 € | noleggio 45.00 €/giorno")

if __name__ == "__main__":
    unittest.main()

import os
import unittest
from Models import CategoriaStrumento, Strumento
from Repos import CategoriaRepository, StrumentoRepository
from Services import GestoreCatalogo

class TestGestoreCatalogo(unittest.TestCase):
    # Fase di Arrange: si creano repository con file finti e il gestore con dati di esempio, eseguito prima di ogni singolo test
    def setUp(self):
        self.file_categorie = "test_categorie.json"
        self.file_strumenti = "test_strumenti.json"
        self.categoria_repo = CategoriaRepository(self.file_categorie)
        self.strumento_repo = StrumentoRepository(self.file_strumenti, self.categoria_repo)
        self.gestore = GestoreCatalogo(self.strumento_repo, self.categoria_repo)
        self.gestore.inserisciTipo("chitarra", 0.1)
        self.gestore.inserisciTipo("batteria", 0.15)
        self.gestore.aggiungiStrumento("Chitarra elettrica", "chitarra", "Yamaha", 5, "450", "mario.rossi")

    # Fase di cleanup: si eliminano i file finti prodotti dal test, eseguito dopo ogni singolo test
    def tearDown(self):
        file_da_eliminare = [self.file_categorie, self.file_strumenti]
        for file in file_da_eliminare:
            if os.path.exists(file):
                os.remove(file)

    # Verifica che i due tipi inseriti in Arrange siano elencati come oggetti CategoriaStrumento
    def test_elenca_tipi(self):
        tipi = self.gestore.elencaTipi()
        self.assertEqual(len(tipi), 2)
        self.assertIsInstance(tipi[0], CategoriaStrumento)

    # Verifica che la ricerca del tipo ignori maiuscole e spazi e restituisca None se ignoto
    def test_trova_tipo(self):
        self.assertIsNotNone(self.gestore.trovaTipo(" CHITARRA "))
        self.assertEqual(self.gestore.trovaTipo("CHITARRA").getNomeTipo(), "chitarra")
        self.assertIsNone(self.gestore.trovaTipo("sax"))

    # Verifica il recupero di uno strumento per id e il None se l'id non esiste
    def test_trova_strumento(self):
        self.assertIsInstance(self.gestore.trovaStrumento("S1"), Strumento)
        self.assertIsNone(self.gestore.trovaStrumento("999"))

    # Verifica la creazione di un nuovo tipo con la sua persistenza su file
    def test_inserisci_tipo_successo(self):
        # Fase 2 - Act
        esito = self.gestore.inserisciTipo("Violino", "0,2")
        # Fase 3 - Assert
        self.assertIn("Creazione del tipo 'violino' andata a buon fine", esito)
        self.assertEqual(self.gestore.trovaTipo("violino").getQuotaNoleggio(), 0.2)
        categorie_ricaricate = CategoriaRepository(self.file_categorie)
        self.assertTrue(categorie_ricaricate.esiste("violino"))

    # Verifica che il tipo creato senza quota usi la quota di default del 10%
    def test_inserisci_tipo_successo_quota_default(self):
        esito = self.gestore.inserisciTipo("Oboe")
        self.assertIn("(quota noleggio 10.00%/giorno)", esito)
        self.assertEqual(self.gestore.trovaTipo("oboe").getQuotaNoleggio(), 0.1)

    # Verifica che un tipo vuoto non venga inserito
    def test_inserisci_tipo_vuoto(self):
        esito = self.gestore.inserisciTipo(" ")
        self.assertEqual(esito, "Errore: inserisci il nuovo tipo di strumento")

    # Verifica che un tipo duplicato non venga inserito due volte
    def test_inserisci_tipo_duplicato(self):
        esito = self.gestore.inserisciTipo("Chitarra")
        self.assertEqual(esito, "Il tipo 'chitarra' era gia' esistente: nessuna aggiunta")

    # Verifica che una quota di noleggio non numerica venga rifiutata
    def test_inserisci_tipo_quota_non_valida(self):
        esito = self.gestore.inserisciTipo("Sassofono", "abc")
        self.assertEqual(esito, "Errore: la quota di noleggio non e' un numero valido")

    # Verifica che una quota di noleggio negativa venga rifiutata
    def test_inserisci_tipo_quota_non_positiva(self):
        esito = self.gestore.inserisciTipo("Sassofono", "-0,5")
        self.assertEqual(esito, "Errore: la quota di noleggio deve essere maggiore di zero")

    # Verifica l'aggiunta di un nuovo strumento con gli effetti sulle repository e su file
    def test_aggiungi_strumento_successo(self):
        # Fase 2 - Act
        esito = self.gestore.aggiungiStrumento("Batteria acustica", "batteria", "Pearl", 3, "600", "mario.rossi", "Mario Rossi")
        # Fase 3 - Assert
        self.assertIn("Strumento aggiunto correttamente", esito)
        self.assertEqual(len(self.strumento_repo.tutti()), 2)
        self.assertEqual(self.gestore.trovaStrumento("S2").getNomeVenditore(), "Mario Rossi")
        self.assertEqual(self.gestore.trovaStrumento("S2").getPrezzoNoleggioGiornaliero(), 90.0)
        strumenti_ricaricati = StrumentoRepository(self.file_strumenti, self.categoria_repo)
        self.assertEqual(len(strumenti_ricaricati.tutti()), 2)

    # Verifica che un prodotto uguale aggiorni la quantità invece di crearne uno nuovo
    def test_aggiungi_strumento_duplicato(self):
        esito = self.gestore.aggiungiStrumento("Chitarra elettrica", "chitarra", "Yamaha", 5, "450", "mario.rossi")
        self.assertIn("Prodotto gia' esistente: quantita' aggiornata (ora 10)", esito)
        self.assertEqual(len(self.strumento_repo.tutti()), 1)
        self.assertEqual(self.gestore.trovaStrumento("S1").getQuantita(), 10)

    # Verifica che senza nome o azienda l'aggiunta venga bloccata
    def test_aggiungi_strumento_nome_vuoto(self):
        esito = self.gestore.aggiungiStrumento("", "chitarra", "Yamaha", 1, "100", "mario.rossi")
        self.assertEqual(esito, "Errore: inserisci nome dello strumento e azienda produttrice")

    # Verifica che un tipo inesistente blocchi l'aggiunta dello strumento
    def test_aggiungi_strumento_tipo_mancante(self):
        esito = self.gestore.aggiungiStrumento("Sassofono alto", "sax", "Yamaha", 1, "300", "mario.rossi")
        self.assertEqual(esito, "Errore: non esiste il tipo inserito ('sax'). Crealo prima con 'Inserisci tipo'.")

    # Verifica che una quantità non numerica venga rifiutata
    def test_aggiungi_strumento_quantita_non_valida(self):
        esito = self.gestore.aggiungiStrumento("Batteria acustica", "batteria", "Pearl", "abc", "600", "mario.rossi")
        self.assertEqual(esito, "Errore: quantità o prezzo non validi")

    # Verifica che una quantità zero venga rifiutata
    def test_aggiungi_strumento_quantita_non_positiva(self):
        esito = self.gestore.aggiungiStrumento("Batteria acustica", "batteria", "Pearl", 0, "600", "mario.rossi")
        self.assertEqual(esito, "Errore: la quantità deve essere maggiore di zero")

    # Verifica che un prezzo negativo venga rifiutato
    def test_aggiungi_strumento_prezzo_negativo(self):
        esito = self.gestore.aggiungiStrumento("Batteria acustica", "batteria", "Pearl", 3, "-5", "mario.rossi")
        self.assertEqual(esito, "Errore: il prezzo non può essere negativo")

    # Verifica che un prezzo di noleggio non numerico venga rifiutato
    def test_aggiungi_strumento_prezzo_noleggio_non_valido(self):
        esito = self.gestore.aggiungiStrumento("Batteria acustica", "batteria", "Pearl", 3, "600", "mario.rossi", None, "abc")
        self.assertEqual(esito, "Errore: il prezzo di noleggio giornaliero non e' valido")

    # Verifica la modifica del prezzo con persistenza su file
    def test_modifica_strumento_successo(self):
        # Fase 2 - Act
        esito = self.gestore.modificaStrumento("S1", "prezzo", "500")
        # Fase 3 - Assert
        self.assertIn("Modifica andata a buon fine", esito)
        self.assertEqual(self.gestore.trovaStrumento("S1").getPrezzo(), 500.0)
        strumenti_ricaricati = StrumentoRepository(self.file_strumenti, self.categoria_repo)
        self.assertEqual(strumenti_ricaricati.trovaPerId("S1").getPrezzo(), 500.0)

    # Verifica la modifica del tipo di uno strumento
    def test_modifica_strumento_tipo(self):
        esito = self.gestore.modificaStrumento("S1", "tipo", "batteria")
        self.assertIn("Modifica andata a buon fine", esito)
        self.assertEqual(self.gestore.trovaStrumento("S1").getTipo(), "batteria")

    # Verifica che la modifica di uno strumento inesistente venga bloccata
    def test_modifica_strumento_non_esistente(self):
        esito = self.gestore.modificaStrumento("999", "prezzo", "500")
        self.assertEqual(esito, "Errore: non esiste questo strumento")

    # Verifica che una caratteristica non modificabile venga rifiutata
    def test_modifica_caratteristica_non_valida(self):
        esito = self.gestore.modificaStrumento("S1", "peso", "3")
        self.assertEqual(esito, "Errore: caratteristica 'peso' non modificabile")

    # Verifica che un valore non numerico su una caratteristica numerica venga rifiutato
    def test_modifica_valore_non_valido(self):
        esito = self.gestore.modificaStrumento("S1", "quantita", "abc")
        self.assertIn("Errore: valore non valido", esito)

    # Verifica che il tipo scelto per la modifica debba esistere
    def test_modifica_strumento_tipo_inesistente(self):
        esito = self.gestore.modificaStrumento("S1", "tipo", "sax")
        self.assertEqual(esito, "Errore: non esiste il tipo selezionato ('sax')")

    # Verifica che la modifica che crea un duplicato unisca le due schede in una sola
    def test_modifica_strumento_unisce_duplicati(self):
        self.gestore.aggiungiStrumento("Chitarra elettrica", "chitarra", "Yamaha", 3, "500", "mario.rossi")
        esito = self.gestore.modificaStrumento("S2", "prezzo", "450")
        self.assertIn("sono stati uniti", esito)
        self.assertEqual(len(self.strumento_repo.tutti()), 1)
        self.assertEqual(self.gestore.trovaStrumento("S1").getQuantita(), 8)
        self.assertIsNone(self.gestore.trovaStrumento("S2"))

    # Verifica la rimozione di uno strumento con gli effetti su repository e file
    def test_rimuovi_strumento_successo(self):
        esito = self.gestore.rimuoviStrumento("S1")
        self.assertIn("Lo strumento e' stato rimosso", esito)
        self.assertEqual(len(self.strumento_repo.tutti()), 0)
        self.assertIsNone(self.gestore.trovaStrumento("S1"))
        strumenti_ricaricati = StrumentoRepository(self.file_strumenti, self.categoria_repo)
        self.assertEqual(len(strumenti_ricaricati.tutti()), 0)

    # Verifica che la rimozione di uno strumento inesistente venga bloccata
    def test_rimuovi_strumento_non_trovato(self):
        esito = self.gestore.rimuoviStrumento("999")
        self.assertEqual(esito, "Errore: non e' stato trovato uno strumento")

    # Verifica che un venditore non possa rimuovere lo strumento di un altro
    def test_rimuovi_strumento_altro_venditore(self):
        esito = self.gestore.rimuoviStrumento("S1", "luigi.verdi")
        self.assertEqual(esito, "Errore: puoi rimuovere solo i tuoi strumenti")
        self.assertIsNotNone(self.gestore.trovaStrumento("S1"))

    # Verifica i filtri dell'elenco per disponibilità e per venditore
    def test_elenca_strumenti(self):
        self.gestore.aggiungiStrumento("Batteria acustica", "batteria", "Pearl", 2, "600", "luigi.verdi")
        self.assertEqual(len(self.gestore.elencaStrumenti()), 2)
        self.assertEqual(len(self.gestore.elencaStrumenti(False, "mario.rossi")), 1)
        self.assertEqual(len(self.gestore.elencaStrumenti(False, "luigi.verdi")), 1)
        self.assertEqual(len(self.gestore.elencaStrumenti(False, "paolo.bianchi")), 0)

    # Verifica che gli strumenti senza quantità non compaiano nell'elenco di default
    def test_elenca_strumenti_esclude_non_disponibili(self):
        self.gestore.trovaStrumento("S1").setQuantita(0)
        self.assertEqual(len(self.gestore.elencaStrumenti()), 0)
        self.assertEqual(len(self.gestore.elencaStrumenti(True)), 1)
        self.assertEqual(len(self.gestore.elencaStrumenti(False, "mario.rossi")), 0)

    # Verifica la ricerca multi-criterio con esclusione degli strumenti non disponibili
    def test_cerca_strumenti(self):
        self.assertEqual(len(self.gestore.cercaStrumenti("nome", "elettrica")), 1)
        self.assertEqual(len(self.gestore.cercaStrumenti("prezzo massimo", "500")), 1)
        self.assertEqual(len(self.gestore.cercaStrumenti("tipo", "chit")), 1)
        self.assertEqual(len(self.gestore.cercaStrumenti("venditore", "mario")), 1)
        self.assertEqual(len(self.gestore.cercaStrumenti("nome", "violino")), 0)
        self.gestore.trovaStrumento("S1").setQuantita(0)
        self.assertEqual(len(self.gestore.cercaStrumenti("nome", "elettrica")), 0)

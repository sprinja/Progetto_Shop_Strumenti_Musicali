from Models import CategoriaStrumento, Strumento
from Repos import StrumentoRepository, CategoriaRepository

class GestoreCatalogo:
    CRITERI_RICERCA = ("tipo", "prezzo massimo", "azienda", "nome", "venditore")

    # costruttore
    def __init__(self, strumento_repo: StrumentoRepository, categoria_repo: CategoriaRepository):
        self._strumento_repo = strumento_repo
        self._categoria_repo = categoria_repo

    # elenca gli strumenti, se id_venditore è fornito, filtra gli strumenti per venditore, in modo che i venditori possano vedere solo i propri strumenti
    def elencaStrumenti(self, inc_nondisp: bool = False, id_venditore: str = None) -> list:
        if inc_nondisp: # se inc_nondisp è True, restituisce tutti gli strumenti, altrimenti solo quelli disponibili
            return self._strumento_repo.tutti()
        strumenti = [i for i in self._strumento_repo.tutti() if i.isDisponibile()]  # filtra gli strumenti disponibili
        if id_venditore:    # se id_venditore è fornito, filtra gli strumenti per venditore, in modo che i venditori possano vedere solo i propri strumenti
            strumenti = [i for i in strumenti if i.getVenditore() == id_venditore]
        return strumenti

    # trova uno strumento per id
    def trovaStrumento(self, id_strumento: str):
        return self._strumento_repo.trovaPerId(id_strumento)

    # rimuove uno strumento dal catalogo, se id_venditore è fornito, verifica che lo strumento appartenga al venditore
    def rimuoviStrumento(self, id_strumento: str, id_venditore: str = None) -> str:
        strumento = self._strumento_repo.trovaPerId(id_strumento)   # trova lo strumento corrispondente all'id fornito
        if strumento is None:   # se non esiste uno strumento con l'id fornito, errore
            return "Errore: non e' stato trovato uno strumento"
        if id_venditore and strumento.getVenditore() != id_venditore:   # se id_venditore è fornito, verifica che lo strumento appartenga al venditore, altrimenti errore
            return "Errore: puoi rimuovere solo i tuoi strumenti"
        self._strumento_repo.rimuovi(strumento.getId()) # rimuove lo strumento dalla repository
        return f"Lo strumento e' stato rimosso: {strumento}"

    # cerca strumenti in base ad un criterio
    def cercaStrumenti(self, criterio: str, valore, id_venditore: str = None) -> list:
        risultati = self._strumento_repo.cerca(criterio, valore)    # cerca gli strumenti in base al criterio e al valore del criterio forniti
        if id_venditore:    # se id_venditore è fornito, filtra gli strumenti per venditore, in modo che i venditori possano vedere solo i propri strumenti
            risultati = [i for i in risultati if i.getVenditore() == id_venditore]
        return [i for i in risultati if i.isDisponibile()]

    # elenca tutti i tipi di strumenti
    def elencaTipi(self) -> list:
        return self._categoria_repo.tutti()

    # trova un tipo di strumento per nome
    def trovaTipo(self, nome_tipo: str):
        return self._categoria_repo.trovaPerNome(nome_tipo)

    # inserisce un nuovo tipo di strumento
    def inserisciTipo(self, nome_tipo: str, quota_noleggio=None) -> str:
        nome = (nome_tipo or "").strip().lower()    # rimuove spazi bianchi all'inizio e alla fine del nome del tipo di strumento e lo converte in minuscolo
        if not nome:    # se il nome del tipo di strumento è vuoto, errore
            return "Errore: inserisci il nuovo tipo di strumento"
        if self._categoria_repo.esiste(nome):   # se il tipo di strumento esiste già nella repository, errore
            return f"Il tipo '{nome}' era gia' esistente: nessuna aggiunta"
        quota = CategoriaStrumento.QUOTA_NOLEGGIO_DEFAULT   # prende la quota di noleggio di default
        if quota_noleggio is not None:  # se la quota di noleggio è fornita, verifica che sia un numero valido e maggiore di zero
            try:
                quota = float(str(quota_noleggio).replace(",", "."))    # converte la quota di noleggio in float, sostituendo eventuali virgole con punti
            except (TypeError, ValueError): # se la quota di noleggio non è un numero valido, errore
                return "Errore: la quota di noleggio non e' un numero valido"
            if quota <= 0:  # se la quota di noleggio è minore o uguale a zero, errore
                return "Errore: la quota di noleggio deve essere maggiore di zero"
        self._categoria_repo.aggiungi(CategoriaStrumento(nome, quota))  # aggiunge il nuovo tipo di strumento alla repository
        return (f"Creazione del tipo '{nome}' andata a buon fine (quota noleggio {quota * 100:.2f}%/giorno)")

    # aggiunge un nuovo strumento al catalogo, se esiste già uno strumento uguale, aggiorna la quantità
    def aggiungiStrumento(self, nome: str, tipo: str, azienda: str, quantita, prezzo, id_venditore: str, nome_venditore: str = None, prezzo_noleggio=None) -> str:
        nome = (nome or "").strip() # rimuove spazi bianchi all'inizio e alla fine del nome dello strumento
        azienda = (azienda or "").strip()   # rimuove spazi bianchi all'inizio e alla fine del nome dell'azienda produttrice dello strumento
        if not nome or not azienda: # se il nome dello strumento o il nome dell'azienda produttrice dello strumento è vuoto, errore
            return "Errore: inserisci nome dello strumento e azienda produttrice"
        categoria = self._categoria_repo.trovaPerNome(tipo) # trova il nome_tipo corrispondente al nome del tipo fornito
        if categoria is None:   # se non esiste un tipo di strumento con il nome fornito, errore
            return (f"Errore: non esiste il tipo inserito ('{tipo}'). Crealo prima con 'Inserisci tipo'.")
        try:
            q = int(quantita)   # converte la quantità in intero
            p = float(str(prezzo).replace(",", "."))    # converte il prezzo in float, sostituendo eventuali virgole con punti
        except (TypeError, ValueError): # se la quantità o il prezzo non sono numeri validi, errore
            return "Errore: quantità o prezzo non validi"
        if q <= 0:  # se la quantità è minore o uguale a zero, errore
            return "Errore: la quantità deve essere maggiore di zero"
        if p <= 0:   # se il prezzo è minore o uguale a zero, errore
            return "Errore: il prezzo non può essere negativo"
        p_noleggio = None   
        if prezzo_noleggio is not None and str(prezzo_noleggio).strip() != "":  # se il prezzo di noleggio è fornito e non è vuoto, verifica che sia un numero valido e maggiore di zero
            try:
                p_noleggio = round(float(str(prezzo_noleggio).replace(",", ".")), 2)    # converte il prezzo di noleggio in float, sostituendo eventuali virgole con punti e arrotondando a due decimali
            except (TypeError, ValueError): # se il prezzo di noleggio non è un numero valido, errore
                return "Errore: il prezzo di noleggio giornaliero non e' valido"
            if p_noleggio <= 0: # se il prezzo di noleggio è minore o uguale a zero, errore
                return "Errore: il prezzo di noleggio giornaliero deve essere maggiore di zero"
        esistente = self._trovaUguale(nome, categoria, azienda, id_venditore, p)    
        if esistente is not None:   # se esiste già uno strumento uguale, aggiorna la quantità e il prezzo di noleggio se fornito
            esistente.aggiornaQuantita(q)
            if p_noleggio is not None and esistente.getPrezzoNoleggioGiornaliero() != p_noleggio: # se il prezzo di noleggio è fornito e diverso da quello esistente, aggiorna il prezzo di noleggio
                esistente.setPrezzoNoleggioGiornaliero(p_noleggio)
            self._strumento_repo.salva()
            return (f"Prodotto gia' esistente: quantita' aggiornata (ora {esistente.getQuantita()}) - {esistente}")
        strumento = Strumento(self._strumento_repo.nuovoId(), nome, categoria, azienda, id_venditore, q, p, nome_venditore or id_venditore, p_noleggio) # crea un nuovo oggetto Strumento con i dati forniti
        self._strumento_repo.aggiungi(strumento)    # aggiunge il nuovo strumento alla repository
        return f"Strumento aggiunto correttamente: {strumento}"

    # trova uno strumento uguale a quello fornito
    def _trovaUguale(self, nome, categoria, azienda, venditore, prezzo):
        for i in self._strumento_repo.tutti():  # itera su tutti gli strumenti del catalogo
            if (i.getNome().lower() == nome.lower() and i.getTipo() == categoria.getNomeTipo() and i.getAzienda().lower() == azienda.lower() and i.getVenditore() == venditore and i.getPrezzo() == prezzo):    # se il nome, il tipo, l'azienda, il prezzo e il venditore sono uguali, restituisce lo strumento
                return i
        return None

    # modifica le caratteristiche di uno strumento, se esiste già uno strumento uguale, aggiorna la quantità
    def modificaStrumento(self, id_strumento: str, caratteristica: str, nuovo_valore) -> str:
        strumento = self._strumento_repo.trovaPerId(id_strumento)   # trova lo strumento corrispondente all'id fornito
        if strumento is None:   # se non esiste uno strumento con l'id fornito, errore
            return "Errore: non esiste questo strumento"
        car = (caratteristica or "").strip().lower()    # rimuove spazi bianchi all'inizio e alla fine della caratteristica fornita e la converte in minuscolo
        valore = (nuovo_valore or "").strip() if isinstance(nuovo_valore, str) else nuovo_valore    # rimuove spazi bianchi all'inizio e alla fine del nuovo valore fornito se è una stringa
        try:    
            if car == "nome":   # se la caratteristica è "nome", modifica il nome dello strumento
                strumento.setNome(valore)
            elif car == "azienda":  # se la caratteristica è "azienda", modifica l'azienda produttrice dello strumento
                strumento.setAzienda(valore)
            elif car == "nome_venditore":   # se la caratteristica è "nome_venditore", modifica il nome del venditore dello strumento
                strumento.setNomeVenditore(valore)
            elif car == "tipo": # se la caratteristica è "tipo", modifica il tipo dello strumento, verificando che esista il tipo fornito
                categoria = self._categoria_repo.trovaPerNome(valore)
                if categoria is None:   # se non esiste un tipo di strumento con il nome fornito, errore
                    return f"Errore: non esiste il tipo selezionato ('{valore}')"
                strumento.setCategoria(categoria)
            elif car == "prezzo":   # se la caratteristica è "prezzo", modifica il prezzo dello strumento
                strumento.setPrezzo(str(valore).replace(",", "."))
            elif car == "prezzo_noleggio":  # se la caratteristica è "prezzo_noleggio", modifica il prezzo di noleggio dello strumento
                strumento.setPrezzoNoleggioGiornaliero(valore)
            elif car == "quantita": # se la caratteristica è "quantità", modifica la quantità dello strumento
                strumento.setQuantita(int(valore))
            else:
                return f"Errore: caratteristica '{caratteristica}' non modificabile"
        except (TypeError, ValueError) as e:
            return f"Errore: valore non valido ({e})"
        self._strumento_repo.salva()    # salva le modifiche nella repository
        duplicato = self._trovaDuplicato(strumento) # verifica se esiste uno strumento duplicato dopo la modifica
        if duplicato is not None:   # se esiste un duplicato
            quantita = strumento.getQuantita()  # prende la quantità dello strumento modificato
            duplicato.aggiornaQuantita(quantita)    # somma le quantità
            self._strumento_repo.rimuovi(strumento.getId()) # rimuove lo strumento modificato
            self._strumento_repo.salva()    # salva la repository dopo l'unione
            return (f"Modifica andata a buon fine: esisteva uno strumento uguale, sono stati uniti - {duplicato}")
        return f"Modifica andata a buon fine: {strumento}"  # nessun duplicato: modifica completata normalmente
       
    # trova strumenti duplicati
    def _trovaDuplicato(self, strumento):
        for i in self._strumento_repo.tutti():  # itera su tutti gli strumenti del catalogo
            if i.getId() == strumento.getId():
                continue    # salta lo strumento che ha lo stesso ID (se stesso)
            if (i.getNome().lower() == strumento.getNome().lower() and i.getTipo() == strumento.getTipo() and i.getAzienda().lower() == strumento.getAzienda().lower() and i.getVenditore() == strumento.getVenditore()):
                return i    # se trova uno strumento uguale lo ritorna
        return None

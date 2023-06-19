#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Esame di Laboratorio di Programmazione 
# Data: 20 / 06 / 2023
# Nome: De Angelis Mario
# N° matricola: SM3201231
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExamException(Exception):
    """
    Classe di eccezione personalizzata da sollevare in caso di problemi con gli input 
    o l'elaborazione dei file nell'analisi dei dati delle serie temporali.
    """

    pass

def compute_avg_monthly_difference(time_series, first_year, last_year):
    """
    Calcola la differenza media mensile dei valori in una serie temporale 
    per l'intervallo di anni specificato.

    Parameters
    ----------
    time_series : list
        Un elenco di tuple o liste in cui ogni elemento rappresenta un record della serie temporale. 
        Ogni record deve avere il formato ('AAAA-MM', valore) dove 'AAAA-MM' è l'anno e il mese e il 
        valore è il dato numerico per quel periodo di tempo. 
        
    first_year : int
        L'anno iniziale per il quale deve essere calcolata la differenza media mensile.
        
    last_year : int
        L'anno finale per il quale deve essere calcolata la differenza media mensile.
    
    Returns
    -------
    list
        Un elenco di 12 differenze medie mensili tra gli anni consecutivi. 
        Ogni elemento dell'elenco rappresenta la differenza media per un mese specifico.
    
    Raises
    ------
    ExamException
        Se i parametri di input non soddisfano i formati previsti o se ci sono incongruenze nei dati. 
    """
    if not time_series or not isinstance(time_series, list):
        raise ExamException("Fornito un time_series non valido")
    
    # Verifica che first_year sia valido
    if not isinstance(first_year, str):
        raise ExamException("Fornito un first_year non valido")
    
    # Verifica che last_year sia valido
    if not isinstance(last_year, str):
        raise ExamException("Fornito un last_year non valido")

    # Creazione di un dizionario vuoto per contenere i dati trasformati
    time_series_dict = {}

    # Iterazione su ogni elemento della lista di liste originale
    for item in time_series:
        # Controlla se l'elemento ha un formato valido
        if not isinstance(item, list) or len(item) != 2:
            raise ExamException("Formato time_series non valido")

        # Estrazione di anno, mese e valore da ogni elemento
        year_month, value = item

        if not isinstance(year_month, str) or '-' not in year_month:
            raise ExamException("Formato data non valido in time_series")

        year = year_month.split('-')[0]
        
        # Aggiunta del valore alla chiave corrispondente all'anno
        if year not in time_series_dict:
            # Se l'anno non è nel dizionario, crea una nuova lista
            time_series_dict[year] = []
        
        # Controlla se il valore è vuoto o None, e gestiscilo di conseguenza
        if value is None or value == '':
            time_series_dict[year].append(None)  # aggiungi None per i valori mancanti
        else:
            try:
                time_series_dict[year].append(int(value))  # tenta di convertire il valore in un intero
            except ValueError:
                raise ExamException("Valore non valido in time_series")
    
    first_year = int(first_year)
    last_year = int(last_year)

    # Il numero di mesi
    months = 12

    # Il numero di anni nell'intervallo
    number_of_years = last_year - first_year + 1

    # Inizializza i conteggi per ogni mese
    month_counts = [0] * months

    # Inizializza la somma delle differenze per ogni mese a 0
    sum_diffs = [0] * months

    # Itera attraverso ogni anno nella serie storica
    for year in range(first_year, last_year):
        # Ottieni i dati per l'anno corrente e l'anno successivo
        current_year_data = time_series_dict.get(str(year))
        next_year_data = time_series_dict.get(str(year + 1))

        # Se i dati per entrambi gli anni sono disponibili
        if current_year_data is not None and next_year_data is not None:
            # Itera attraverso ogni mese
            for month in range(months):
                # Se i dati per il mese sono disponibili in entrambi gli anni
                if month < len(current_year_data) and month < len(next_year_data):
                    # Se il valore è None, aggiungi 0
                    if current_year_data[month] is not None or next_year_data[month] is not None:
                        # Calcola la differenza per ogni mese
                        # e aggiungilo a sum_diffs
                        sum_diffs[month] += next_year_data[month] - current_year_data[month]

                    # Incrementa conteggi_mesi
                    month_counts[month] += 1
    
    if number_of_years == 2:  # Caso specifico per intervallo di due anni
        avg_diffs = []
        for i in range(months):
            # Se non abbiamo misurazioni per il mese, aggiungi 0
            if month_counts[i] > 0:
                avg_diffs.append(round(sum_diffs[i] / month_counts[i], 2))
            else:
                avg_diffs.append(0)
    else:  # Caso per intervallo di più di due anni
        avg_diffs = []
        for i in range(months):
            # Se abbiamo meno di due misurazioni
            if month_counts[i] < 2:
                avg_diffs.append(0)
            else:
                avg_diffs.append(round(sum_diffs[i] / month_counts[i], 2))

    return avg_diffs


class CSVTimeSeriesFile:
    """
    Classe responsabile della gestione di file CSV contenenti dati di serie temporali.
    """

    def __init__(self, name):
        """
        Inizializza l'oggetto CSVTimeSeriesFile con il nome del file da leggere.
        
        Parameters
        ----------
        name : str
            Il nome del file o il percorso da leggere.
            
        Raises
        ------
        ExamException
            Se il nome del file non è una stringa o se il file non può essere aperto.
        """

        # Verifica che il nome del file sia una stringa
        if not isinstance(name, str):
            raise ExamException("Il nome del file dovrebbe essere una stringa")
        
        self.name = name
        self.can_read = True

        # Tenta di aprire il file
        try:
            with open(self.name, 'r') as my_file:
                my_file.readline()

        except Exception as e:
            self.can_read = False
            raise ExamException(f'Errore nell\'apertura del file: "{e}"')

    def get_data(self):
        """
        Leggere e restituire i dati dal file CSV.
        
        Returns
        -------
        list
            Un elenco di liste che rappresentano le righe di dati nel file.
            
        Raises
        ------
        ExamException
            Se non è possibile leggere il file.
        """

        # Se non è possibile leggere il file, solleva un'eccezione
        if not self.can_read:
            raise ExamException('Errore, impossibile leggere il file')

        # Tenta di leggere i dati dal file
        try:
            with open(self.name, 'r') as my_file:
                # Salta l'intestazione
                next(my_file)
                # Processa ogni riga e aggiungila alla lista dei dati
                data = [line.strip().split(',') for line in my_file]
        except Exception as e:
            raise ExamException(f'Errore nella lettura del file: "{e}"')

        return data

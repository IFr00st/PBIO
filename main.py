import random  # Import biblioteki random do generowania losowych sekwencji
import os  # Import biblioteki os do sprawdzania istnienia plików

def generate_dna_sequence(length):  # Definicja funkcji generującej sekwencję DNA
    return ''.join(random.choices('ACGT', k=length))  # Zwraca ciąg losowych liter A, C, G, T o zadanej długości

def insert_name_into_sequence(sequence, name):  # Funkcja wstawiająca imię w losowe miejsce sekwencji
    insert_pos = random.randint(0, len(sequence))  # Losowo wybiera indeks, gdzie wstawić imię
    return sequence[:insert_pos] + name + sequence[insert_pos:]  # Wstawia imię do sekwencji i zwraca nową sekwencję

def calculate_statistics(sequence):  # Funkcja licząca statystyki dla sekwencji DNA
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}  # Zlicza wystąpienia każdego nukleotydu
    total = sum(counts.values())  # Oblicza łączną długość sekwencji
    percentages = {nuc: (counts[nuc] / total * 100) for nuc in 'ACGT'}  # Oblicza procentowy udział każdego nukleotydu
    cg = counts['C'] + counts['G']  # Liczy łączną ilość C i G
    at = counts['A'] + counts['T']  # Liczy łączną ilość A i T
    cg_at_ratio = (cg / at * 100) if at > 0 else 0  # Oblicza stosunek C+G do A+T (w %), unika dzielenia przez 0
    return percentages, cg_at_ratio  # Zwraca procenty i stosunek CG/AT

def save_to_fasta(filename, seq_id, description, sequence_with_name):  # Funkcja zapisująca dane do pliku FASTA
    # MODIFIED (dodano sprawdzenie czy plik istnieje i tryb zapisu 'a' zamiast 'w' jeśli ma być wspólny plik):
    if os.path.exists(filename):  # Sprawdza, czy plik już istnieje
        mode = 'a'  # Jeśli istnieje, otwieramy w trybie dopisywania
    else:
        mode = 'w'  # Jeśli nie, tworzymy nowy plik

    # ORIGINAL:
    # with open(filename, 'w') as f:
    #     f.write(f">{seq_id} {description}\n")
    #     f.write(sequence_with_name + "\n")

    with open(filename, mode) as f:  # Otwiera plik w odpowiednim trybie ('a' lub 'w')
        f.write(f">{seq_id} {description}\n")  # Zapisuje nagłówek FASTA
        f.write(sequence_with_name + "\n")  # Zapisuje sekwencję z wstawionym imieniem

def main():  # Główna funkcja programu
    print("Generator sekwencji FASTA z dodatkowymi opcjami (zakończ program wpisując 'nie')\n")  # Powitanie i instrukcja

    while True:  # MODIFIED (dodanie pętli, by program działał wielokrotnie)
        try:
            length = int(input("Podaj długość sekwencji: "))  # Prośba o długość sekwencji i konwersja na int
        except ValueError:  # Obsługa błędu jeśli użytkownik poda coś innego niż liczba
            print("Nieprawidłowa wartość. Podaj liczbę całkowitą.")  # Komunikat o błędzie
            continue  # Powrót do początku pętli

        seq_id = input("Podaj ID sekwencji: ")  # Pobranie ID sekwencji od użytkownika
        description = input("Podaj opis sekwencji: ")  # Pobranie opisu sekwencji
        name = input("Podaj imię: ")  # Pobranie imienia do wstawienia w sekwencję
        file_mode = input("Czy chcesz zapisać do wspólnego pliku? (tak/nie): ").strip().lower()  # Pytanie o tryb zapisu

        if file_mode == 'tak':  # MODIFIED (użytkownik może wybrać wspólny plik)
            filename = "wspolny_output.fasta"  # Nazwa wspólnego pliku
        else:
            filename = f"{seq_id}.fasta"  # Nazwa indywidualnego pliku na podstawie ID

        dna_sequence = generate_dna_sequence(length)  # Generowanie losowej sekwencji DNA

        stats, cg_at_ratio = calculate_statistics(dna_sequence)  # Obliczenie statystyk sekwencji

        sequence_with_name = insert_name_into_sequence(dna_sequence, name)  # Wstawienie imienia do sekwencji

        save_to_fasta(filename, seq_id, description, sequence_with_name)  # Zapis sekwencji do pliku

        print(f"\nSekwencja została zapisana do pliku {filename}")  # Informacja o zapisaniu pliku
        print("Statystyki sekwencji:")  # Nagłówek statystyk
        for nuc in 'ACGT':  # Iteracja po nukleotydach
            print(f"{nuc}: {stats[nuc]:.1f}%")  # Wyświetlenie procentowej zawartości danego nukleotydu
        print(f"%CG: {stats['C'] + stats['G']:.1f}")  # Wyświetlenie sumy C+G w procentach
        print(f"Stosunek C+G / A+T: {cg_at_ratio:.1f}%\n")  # Wyświetlenie stosunku C+G do A+T

        continue_choice = input("Czy chcesz wygenerować kolejną sekwencję? (tak/nie): ").strip().lower()  # Pytanie o kontynuację
        if continue_choice != 'tak':  # Jeśli użytkownik nie chce kontynuować
            print("Zakończono działanie programu.")  # Informacja o zakończeniu
            break  # Przerwanie pętli

if __name__ == "__main__":  # Sprawdzenie, czy plik jest uruchamiany bezpośrednio
    main()  # Wywołanie funkcji głównej

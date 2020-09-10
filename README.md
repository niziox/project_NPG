# Dziennik ciśnieniowca
>Aplikacja służąca do zapisu pomiaru ciśnień.

## Spis treści
* [Informacje ogólne](#informacje-ogólne)
* [Technologie](#technologie)
* [Uruchamianie](#uruchamianie)
* [Funkcje](#funkcje)
* [Status](#status)
* [Kontakt](#Kontakt)

## Informacje ogólne
Aplikacja służy do zapisu pomiarów ciśnienia krwi. Umożliwia również przeglądanie wcześniej dodanych pomiarów i usuwanie ich. Została stworzona jako praca zaliczeniowa na przedmiot Narzędzia Pracy Grupowej.

## Technologie
* Python 3.8
* SQLite 3.32
* Tkinter

## Uruchamianie
W celu uruchomienia należy posiadać zainstalowane biblioteki:
* tkinter
* sqlite3
* datetime
* matplotlib

Domyślnie plik z ścieżką pod którą zapisujemy bazę danych z pomiarami, oraz sama baza danych znajduje się w folderze paths.

Aby uruchomić program należy znajdując się w katalogu z projektem wpisać komendę:

```
$ python v1.1.py
```

## Funkcje
Aplikacja zawiera funkjonalności:
* Dodanie nowej pozycji poziomu ciśnienia.
* Wyszukanie pomiaru po dacie lub wartości.
* Zapis i wczytywanie pomiarów zamknięciu/otwarciu programu.
* Zapis pomorów do pliku pod zadaną ścieżkę.
* Wykres pomiarów.
* Ostrzeżenie o nieprawidłowym ciśnieniu krwi.

## Status
Projekt zakończony.

## Kontakt
Stworozne przez:
* Arkadiusz Kontek	arekkontek@student.agh.edu.pl
* Dawid Bogon		bogondawid@student.agh.edu.pl
* Konrad Kropornicki	kropornicki@student.agh.edu.pl
* Michał Święciło	swiecilo@student.agh.edu.pl
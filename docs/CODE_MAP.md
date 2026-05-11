# Code Map - Manager

## Zakres mapy

Ta mapa opisuje obecny stan repozytorium na podstawie istniejacych plikow. Nie jest to jeszcze pelna dokumentacja techniczna calego kodu.

Gdy cos nie jest pewne, oznaczono to jako niejasne.

## Struktura repozytorium

```text
.
|-- .git/
|-- .gitignore
|-- AGENTS.md
|-- README.md
|-- build_exe.bat
|-- main.py
`-- docs/
    |-- BACKLOG.md
    |-- CODE_MAP.md
    |-- DECISIONS.md
    |-- PROJECT_PLAN.md
    |-- TECH_SPEC.md
    `-- VISION.md
```

## Pliki glowne

### `main.py`

Kategoria: UI, dane, logika aplikacji, konfiguracja.

Co prawdopodobnie robi:

- uruchamia aplikacje Tkinter,
- definiuje tytul aplikacji, nazwy plikow danych i ustawien,
- definiuje obecne statusy i priorytety,
- definiuje motywy jasny i ciemny,
- zarzadza ustawieniami lokalnymi przez JSON,
- tworzy i migruje tabele SQLite `orders`,
- dodaje, aktualizuje, usuwa, pobiera i eksportuje rekordy,
- buduje glowne okno aplikacji,
- buduje zakladki aktywnych rekordow i archiwum,
- obsluguje formularz, tabele, wyszukiwanie, filtrowanie, sortowanie, archiwum, backup i eksport CSV.

Znane elementy:

- `get_app_data_dir()` wybiera lokalny katalog danych uzytkownika.
- `resource_path()` buduje sciezki do plikow danych.
- `SettingsManager` obsluguje plik ustawien JSON.
- `Database` obsluguje SQLite i aktualny model tabeli `orders`.
- `WorkshopApp` laczy UI Tkinter z logika aplikacji.

Ryzyka i niejasne obszary:

- Plik laczy wiele odpowiedzialnosci, co utrudnia bezpieczne zmiany.
- Nazwy i model danych sa nadal zwiazane ze starsza aplikacja warsztatowa.
- Schemat `orders` nie jest jeszcze generycznym modelem rekordow.
- Migracje bazy sa wykonywane w kodzie aplikacji; wymagaja ostroznosci.
- Niejasne, czy istnieja zewnetrzne dane uzytkownika, ktore musza byc migrowane.
- Niejasne, jakie reczne scenariusze testowe sa obecnie najwazniejsze.

### `build_exe.bat`

Kategoria: build, narzedzia.

Co prawdopodobnie robi:

- przechodzi do katalogu projektu,
- aktualizuje `pip`,
- instaluje `pyinstaller`,
- buduje jednoplikowy EXE z `main.py`,
- zostawia wynik w katalogu `dist`.

Ryzyka i niejasne obszary:

- Skrypt instaluje zaleznosci globalnie lub w aktywnym srodowisku Python.
- Niejasne, czy projekt ma docelowo uzywac wirtualnego srodowiska.
- Nie powinien byc zmieniany przy zadaniach dotyczacych samej dokumentacji.

### `README.md`

Kategoria: dokumentacja.

Co prawdopodobnie robi:

- opisuje obecna wersje aplikacji,
- opisuje uruchamianie przez Python,
- opisuje budowanie EXE,
- wskazuje lokalizacje danych w katalogu uzytkownika.

Ryzyka i niejasne obszary:

- README nadal opisuje starszy, branzowy stan aplikacji.
- W przyszlosci powinien zostac zneutralizowany zgodnie z wizja Managera.

### `AGENTS.md`

Kategoria: dokumentacja, zasady pracy.

Co robi:

- opisuje zasady dla przyszlych agentow AI/kodu,
- podkresla male zmiany, zachowanie dzialania aplikacji i generyczny kierunek Managera.

Ryzyka i niejasne obszary:

- Zasady trzeba aktualizowac, gdy zmieniaja sie decyzje architektoniczne.

### `.gitignore`

Kategoria: konfiguracja repozytorium.

Co prawdopodobnie robi:

- okresla pliki, ktore nie powinny trafiac do repozytorium.

Ryzyka i niejasne obszary:

- Niejasne, czy ignoruje wszystkie lokalne bazy danych, backupy, katalogi builda i pliki tymczasowe.
- W przyszlosci warto sprawdzic go osobnym zadaniem.

## Foldery

### `.git/`

Kategoria: konfiguracja Git.

Co robi:

- przechowuje lokalna historie i metadane repozytorium Git.

Ryzyka i niejasne obszary:

- Nie modyfikowac recznie.

### `docs/`

Kategoria: dokumentacja.

Co robi:

- przechowuje dokumentacje projektu, wizje, backlog, decyzje i mape kodu.

Pliki:

- `PROJECT_PLAN.md` opisuje plan projektu i przejscie do uniwersalnego Managera.
- `VISION.md` opisuje wizje produktu.
- `TECH_SPEC.md` opisuje stack i obecna strukture techniczna.
- `BACKLOG.md` opisuje plan MVP.
- `DECISIONS.md` zapisuje decyzje architektoniczne.
- `CODE_MAP.md` opisuje obecna baze kodu.

Ryzyka i niejasne obszary:

- Dokumentacja musi byc utrzymywana razem ze zmianami architektury.
- Czesc dokumentacji opisuje stan docelowy, a czesc stan obecny; trzeba to rozrozniac.

## Obecne granice odpowiedzialnosci

Na ten moment granice odpowiedzialnosci sa slabe, bo duza czesc aplikacji znajduje sie w `main.py`.

Przy przyszlym rozwoju warto stopniowo wydzielac:

- warstwe danych,
- warstwe konfiguracji,
- warstwe UI,
- logike importu i eksportu,
- logike wyszukiwania i filtrowania,
- migracje danych.

Nie nalezy robic tego jednym duzym refaktorem.

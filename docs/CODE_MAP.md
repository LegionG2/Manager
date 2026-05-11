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

## MVP-002 - Dokladniejsza mapa `main.py`

### Punkt wejscia aplikacji

Punkt wejscia znajduje sie na koncu `main.py`:

- tworzona jest instancja `WorkshopApp`,
- uruchamiany jest `app.mainloop()`.

Oznacza to, ze `main.py` jest jednoczesnie plikiem startowym i glownym miejscem implementacji aplikacji.

### Stale i zalozenia globalne

Na gorze `main.py` znajduja sie stale:

- `APP_TITLE`,
- `DB_NAME`,
- `SETTINGS_NAME`,
- `STATUSES`,
- `PRIORITIES`,
- `THEMES`,
- `PRIORITY_TAGS`.

Obecne ryzyka:

- `APP_TITLE`, `DB_NAME` i katalog danych zawieraja nazwy zwiazane ze stara aplikacja warsztatowa.
- `STATUSES` i `PRIORITIES` sa hardcodowane w kodzie.
- Statusy, priorytety, nazwy plikow i czesc etykiet UI nie sa jeszcze konfigurowalne.
- Zmiana tych wartosci moze wplynac jednoczesnie na UI, sortowanie, filtry, dane i eksport.

### Kod zwiazany z baza danych

Kod bazy danych znajduje sie glownie w klasie `Database`.

Znane metody:

- `create_tables()` tworzy tabele `orders`.
- `migrate_tables()` dodaje brakujace kolumny do `orders`.
- `generate_next_order_no()` generuje numer rekordu w obecnym formacie.
- `add_order()` dodaje rekord.
- `update_order()` aktualizuje rekord.
- `delete_order()` usuwa rekord.
- `fetch_orders()` pobiera liste rekordow z wyszukiwaniem, filtrem statusu i archiwum.
- `fetch_order()` pobiera jeden rekord.
- `stats()` liczy podsumowania dla panelu statystyk.
- `export_csv()` eksportuje dane do CSV.

Ryzyka:

- Model tabeli `orders` jest branzowy i nie jest jeszcze generycznym modelem rekordow.
- Zapytania SQL, wyszukiwanie, sortowanie i statystyki znaja konkretne kolumny.
- `migrate_tables()` wykonuje migracje przy starcie aplikacji.
- `Database` jest uzywana bezposrednio przez `WorkshopApp`, wiec UI i dane sa mocno polaczone.
- `export_csv()` jest w warstwie bazy, ale dotyka formatu eksportu, czyli przyszlej osobnej odpowiedzialnosci.

Obszary niejasne:

- Nie wiadomo, jakie rzeczywiste dane uzytkownika istnieja w lokalnych bazach.
- Nie wiadomo, czy wszystkie kolumny sa nadal aktywnie uzywane w UI.
- Nie ma osobnych testow migracji ani eksportu.

### Kod zwiazany z UI

Kod UI znajduje sie glownie w klasie `WorkshopApp`, ktora dziedziczy po `tk.Tk`.

Znane grupy metod:

- start i inicjalizacja: `__init__()`,
- style i motywy: `configure_style()`, `apply_theme()`, `toggle_theme()`, `repaint_widgets()`,
- budowanie widoku: `build_ui()`, `build_orders_tab()`, `build_form_area()`, `build_form()`, `build_archive_tab()`,
- pomocnicze kontrolki: `create_text_block()`, `add_form_row()`, `add_combo_row()`,
- obsluga formularza i tabel: `refresh_table()`, `refresh_archive_table()`, `load_order_to_form()`, `clear_form()`,
- akcje uzytkownika: `save_order()`, `delete_order()`, `duplicate_order()`, `quick_status()`, `archive_order()`, `restore_archived_order()`,
- eksport i backup: `export_csv()`, `backup_database()`.

Ryzyka:

- UI wywoluje metody bazy danych bez warstwy posredniej.
- UI zna nazwy kolumn bazy i obecny model danych.
- Formularz jest oparty o hardcodowane pola w `form_vars`.
- Etykiety i akcje nadal zawieraja zalozenia starej aplikacji.
- Sortowanie, filtrowanie i walidacja formularza sa wymieszane z kodem widoku.

Obszary niejasne:

- Nie wiadomo, ktore elementy UI sa krytyczne dla obecnych uzytkownikow.
- Nie ma automatycznych testow zachowania UI.
- Przed wydzielaniem UI potrzebne sa scenariusze testow recznych.

### Konfiguracja i stan aplikacji

Konfiguracja jest rozproszona:

- `SettingsManager` zapisuje ustawienia w JSON.
- `get_app_data_dir()` wybiera katalog danych.
- `resource_path()` buduje sciezki do plikow danych.
- `WorkshopApp.__init__()` tworzy zmienne Tkinter, m.in. filtry, tryb wyszukiwania, motyw, sortowanie i `form_vars`.

Ryzyka:

- Czesc ustawien jest w JSON, a czesc w stalych globalnych.
- Nie ma osobnego modelu konfiguracji aplikacji.
- Katalog danych i nazwy plikow sa nadal powiazane ze stara nazwa aplikacji.
- Przyszla konfiguracja typow rekordow i pol wymaga osobnego projektu, a nie szybkiego dopisywania kolejnych stalych.

### Hardcodowane zalozenia branzowe

Obecne przyklady zalozen, ktore trzeba traktowac jako stan przejsciowy:

- nazwa `WorkshopApp`,
- tytul `Warsztat Manager Premium`,
- baza `warsztat_manager.db`,
- katalog `WarsztatManagerPremium`,
- tabela `orders`,
- numeracja `WM/YYYY/NNNN`,
- pola klienta, pojazdu, VIN, miejsca parkingowego, mechanika, czesci i kosztow,
- statusy typu `Oczekuje na czesci`, `Gotowe do odbioru`, `Odebrane`,
- nazwy eksportow i backupow zaczynajace sie od `warsztat_`.

Nie nalezy usuwac ani zmieniac tych elementow bez osobnego etapu migracji, bo moga byc powiazane z istniejacymi danymi i obecnym dzialaniem UI.

### Bezpieczna kolejnosc przyszlego refaktoru

1. Najpierw opisac scenariusze testow recznych dla obecnego zachowania.
2. Wydzielic pomocnicze funkcje dostepu do danych bez zmiany schematu.
3. Wydzielic konfiguracje stalych i ustawien bez zmiany wartosci.
4. Wydzielic fragmenty UI do mniejszych funkcji lub modulow bez zmiany wygladu.
5. Dopiero pozniej projektowac generyczny model typow rekordow i pol.

# Tech Spec - Manager

## Obecny stack

- Python
- Tkinter
- SQLite
- Lokalny plik ustawien JSON
- Podejscie local-first

## Docelowy stack na ten moment

- Python jako glowny jezyk aplikacji.
- Tkinter jako framework UI.
- SQLite jako lokalna baza danych.
- Brak chmury na start.
- Brak systemu logowania na start.
- Brak zewnetrznego backendu na ten moment.
- Brak nowych zaleznosci bez osobnej decyzji.

## Obecna znana struktura techniczna

Repozytorium jest male i skupione wokol jednego pliku aplikacji:

- `main.py` zawiera aplikacje Tkinter, obsluge SQLite, ustawienia, logike rekordow, archiwum, eksport CSV i backup.
- `build_exe.bat` zawiera prosty proces budowy pliku EXE przez PyInstaller.
- `README.md` opisuje obecna aplikacje i sposob uruchamiania.
- `docs/` zawiera dokumentacje projektu.
- `AGENTS.md` zawiera zasady pracy dla przyszlych agentow AI/kodu.

## Dane lokalne

Na podstawie obecnego kodu aplikacja zapisuje dane poza repozytorium, w katalogu uzytkownika Windows:

- baza SQLite: `warsztat_manager.db`,
- ustawienia: `settings.json`,
- katalog aplikacji: `AppData/Local/WarsztatManagerPremium`.

Nazwy te sa obecnie zwiazane ze stara wersja aplikacji. Nalezy traktowac je jako stan przejsciowy, a nie docelowa wizje produktu.

## Obecny model danych

Obecny kod tworzy tabele `orders` w SQLite. Model zawiera pola zwiazane z poprzednim zastosowaniem aplikacji, m.in. klient, pojazd, status, priorytet, terminy, koszty, notatki i archiwum.

To nie jest jeszcze docelowy generyczny model rekordow. Przed zmianami schematu nalezy zaplanowac migracje i zabezpieczenie istniejacych danych.

## Current architecture observations

### UI logic

UI logic currently lives in `main.py`, mainly inside `WorkshopApp`.

`WorkshopApp` is responsible for:

- creating the Tkinter window,
- configuring styles and themes,
- building tabs, tables, forms and buttons,
- holding Tkinter state variables,
- handling user actions,
- calling database methods directly,
- refreshing active and archived record views.

This means the UI layer is tightly coupled to the current data model.

### Database logic

Database logic currently lives in `main.py`, mainly inside `Database`.

`Database` is responsible for:

- opening the SQLite connection,
- creating the `orders` table,
- applying simple migrations,
- inserting, updating, deleting and fetching rows,
- calculating dashboard statistics,
- exporting rows to CSV.

This is a useful starting point, but it is not yet a separated data access layer. The class still exposes the current business-specific table shape directly to the UI.

### Configuration and state

Configuration and state currently live in several places:

- global constants in `main.py`,
- `SettingsManager` for JSON settings,
- Tkinter variables inside `WorkshopApp`,
- SQLite rows in the `orders` table.

Future configurable record types, fields and statuses should not be added as more unrelated globals. They need a clear configuration model.

### Coupling level

The code is tightly coupled rather than modular:

- UI methods know database column names.
- Database queries know current status names and workflow assumptions.
- Sorting and filtering know current business fields.
- Export and backup are triggered by UI methods and implemented near current database assumptions.
- The current model is still based on `orders`, not generic records.

This is expected for the current stage, but it should be treated as refactor risk.

### What should be separated in future MVPs

Future MVPs should separate responsibilities gradually:

- data/database access helpers,
- UI layout and reusable UI components,
- domain/business model,
- configuration and settings,
- import/export helpers,
- search/filter helpers,
- archive behavior.

Each separation should preserve current behavior first. Generic record types and configurable fields should come after the current responsibilities are clearer.

## Zasady techniczne

- Nie zmieniac schematu bazy danych bez wyraznego zadania.
- Nie dodawac zaleznosci bez decyzji architektonicznej.
- Nie przenosic plikow bez potrzeby.
- Wydzielanie modulow robic stopniowo.
- Zachowywac kompatybilnosc z obecnym dzialaniem aplikacji.
- Dokumentowac istotne decyzje w `docs/DECISIONS.md`.

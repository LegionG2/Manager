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

- `main.py` zawiera prosty punkt wejscia aplikacji.
- `ui/app.py` zawiera aplikacje Tkinter, ustawienia, logike UI, archiwum i backup.
- `ui/__init__.py` oznacza `ui` jako pakiet warstwy UI.
- `services/order_service.py` zawiera przejsciowy serwis logiki rekordow/zlecen.
- `services/__init__.py` oznacza `services` jako pakiet serwisow aplikacyjnych.
- `data/database.py` zawiera obsluge SQLite, obecny model tabeli `orders`, operacje CRUD, statystyki i eksport CSV.
- `data/__init__.py` oznacza `data` jako pakiet warstwy danych.
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

UI logic currently lives in `ui/app.py`, mainly inside `WorkshopApp`.

`WorkshopApp` is responsible for:

- creating the Tkinter window,
- configuring styles and themes,
- building tabs, tables, forms and buttons,
- holding Tkinter state variables,
- handling user actions,
- coordinating `OrderService` and selected database calls,
- refreshing active and archived record views.

This means the UI layer is tightly coupled to the current data model.

### Application service logic

Record/order application logic currently starts in `services/order_service.py`, inside `OrderService`.

`OrderService` is responsible for:

- parsing money values,
- calculating totals and balances,
- calculating due-date display state,
- matching rows against the current search mode,
- sorting current order rows,
- building validated order data from form values,
- preparing default form values and duplicated order data,
- performing simple record actions through `Database`.

The name is intentionally transitional. The current database table is still `orders`, so the service keeps the current vocabulary until a separate generic record model is designed.

### Database logic

Database logic currently lives in `data/database.py`, inside `Database`.

`Database` is responsible for:

- opening the SQLite connection,
- creating the `orders` table,
- applying simple migrations,
- inserting, updating, deleting and fetching rows,
- calculating dashboard statistics,
- exporting rows to CSV.

This is the first separated data access module. The class still exposes the current business-specific table shape directly to the UI.

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
- `OrderService` knows database column names and current order fields.
- Database queries know current status names and workflow assumptions.
- Sorting, filtering and validation still know current business fields, though part of that logic moved out of UI.
- Export and backup are triggered by UI methods and implemented near current database assumptions.
- The current model is still based on `orders`, not generic records.
- Backup in `ui/app.py` still reaches into `self.db.conn`.

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

## MVP-003 data layer extraction

MVP-003 added a small `data` package:

- `data/database.py`,
- `data/__init__.py`.

Moved from `main.py` to `data/database.py`:

- SQLite connection setup,
- `orders` table creation,
- existing column migration logic,
- add/update/delete/fetch operations,
- current stats queries,
- CSV export.

After MVP-003 these parts were still in `main.py`; after MVP-004 they live in `ui/app.py` except for startup:

- Tkinter application and UI layout,
- Tkinter state variables,
- form validation and data mapping,
- search and sort behavior,
- archive button behavior,
- backup file dialog and copy operation,
- app data path helpers,
- JSON settings manager.

No schema changes were made. The `orders` table, column names, status values and public `Database` method names remain compatible with the previous code.

## MVP-004 UI layer extraction

MVP-004 added a small `ui` package:

- `ui/app.py`,
- `ui/__init__.py`.

Moved from `main.py` to `ui/app.py`:

- UI imports and constants,
- app data path helpers,
- `SettingsManager`,
- `WorkshopApp`,
- Tkinter layout, styles, state variables and user action handlers.

Still in `main.py`:

- import of `WorkshopApp`,
- `main()` function,
- application startup and `mainloop()`.

No UI labels, layouts, status values, database schema, dependencies or data access method names were changed.

Known remaining coupling:

- `WorkshopApp` still creates and calls `Database` directly.
- UI code still knows the current `orders` columns and current form fields.
- Search, sorting, form validation, archive behavior, export triggering and backup triggering still live inside the UI class.
- Backup still reaches into `self.db.conn`.

Next safe step:

- move configuration/path helpers or backup behavior out of `ui/app.py` in a separate small change, preserving current values and behavior.

## MVP-005 application service extraction

MVP-005 added a small `services` package:

- `services/order_service.py`,
- `services/__init__.py`.

Moved from `ui/app.py` to `services/order_service.py`:

- money parsing,
- total and balance calculations,
- due-date state calculation,
- current search matching,
- current order sorting,
- form data validation and payload building,
- default form values,
- duplicated order payload building,
- simple record operations: save, delete, status update, archive and restore.

Still in `ui/app.py`:

- Tkinter layout, widgets, styles and state variables,
- message boxes and file dialogs,
- reading values from Tkinter widgets,
- filling tables and forms,
- export CSV trigger,
- backup trigger and file copy.

No UI labels, layouts, status values, database schema, dependencies or visible behavior were changed.

Known remaining coupling:

- `OrderService` still wraps the current `orders` model rather than a generic record model.
- `WorkshopApp` still knows current table columns while rendering tables and loading forms.
- `OrderService` still calls `Database` directly.
- Backup still reaches into `self.db.conn` from UI.

Next safe step:

- extract backup or configuration/path helpers in a separate small change, or add focused tests around `OrderService` before designing generic records.

## Zasady techniczne

- Nie zmieniac schematu bazy danych bez wyraznego zadania.
- Nie dodawac zaleznosci bez decyzji architektonicznej.
- Nie przenosic plikow bez potrzeby.
- Wydzielanie modulow robic stopniowo.
- Zachowywac kompatybilnosc z obecnym dzialaniem aplikacji.
- Dokumentowac istotne decyzje w `docs/DECISIONS.md`.

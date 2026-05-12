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
- `config/default_record_fields.json` zawiera neutralna domyslna konfiguracje przyszlych pol rekordow.
- `config/default_record_type.json` zawiera neutralna domyslna konfiguracje przyszlego typu rekordu.
- `ui/app.py` zawiera aplikacje Tkinter, ustawienia, logike UI, archiwum i backup.
- `ui/__init__.py` oznacza `ui` jako pakiet warstwy UI.
- `domain/record.py` zawiera fundament generycznego modelu domenowego rekordow.
- `domain/field_definition.py` zawiera fundament definicji konfigurowalnych pol.
- `domain/record_type.py` zawiera fundament definicji konfigurowalnych typow rekordow.
- `domain/__init__.py` oznacza `domain` jako pakiet domenowy.
- `services/field_config_service.py` zawiera loader konfiguracji pol z JSON.
- `services/record_type_config_service.py` zawiera loader konfiguracji typu rekordu z JSON.
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

## Fundament modelu domenowego

`domain/record.py` wprowadza neutralne pojecia przyszlego Managera:

- `RecordField` dla definicji pola,
- `RecordStatus` dla statusu rekordu,
- `RecordType` dla typu rekordu,
- `Record` dla pojedynczej instancji rekordu.

Ten model nie jest jeszcze podlaczony do UI ani bazy danych. Obecna aplikacja nadal dziala na tabeli `orders` i przejsciowym `OrderService`.

## Fundament konfigurowalnych pol

`domain/field_definition.py` wprowadza neutralne pojecia definicji pol:

- `FieldType` dla typow `text`, `number`, `date`, `boolean` i `select`,
- `FieldOption` dla opcji pola wyboru,
- `FieldDefinition` dla pojedynczej definicji pola.

Domyslna konfiguracja znajduje sie w `config/default_record_fields.json`. Jest neutralna i zawiera pola `title`, `description`, `status` oraz `created_date`.

`services/field_config_service.py` zawiera `FieldConfigService`, ktory wczytuje liste pol z JSON i mapuje ja na obiekty domenowe. Loader nie jest jeszcze podlaczony do UI, bazy ani obecnego statycznego formularza.

## Fundament konfigurowalnych typow rekordow

`domain/record_type.py` wprowadza neutralne pojecie `RecordTypeDefinition`.

Definicja typu rekordu zawiera:

- `id`,
- `name`,
- opcjonalny `description`,
- liste identyfikatorow pol.

Domyslna konfiguracja znajduje sie w `config/default_record_type.json`. Jest neutralna i opisuje typ `default` o nazwie `Default record`, uzywajacy pol `title`, `description`, `status` i `created_date`.

`services/record_type_config_service.py` zawiera `RecordTypeConfigService`, ktory wczytuje konfiguracje typu rekordu z JSON i mapuje ja na obiekt domenowy. Loader nie jest jeszcze podlaczony do UI, bazy ani obecnego statycznego formularza.

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

### Domain model

Generic domain model definitions live in `domain/record.py`, `domain/field_definition.py` and `domain/record_type.py`.

The modules currently contain simple structures only:

- `RecordField`,
- `RecordStatus`,
- `RecordType`,
- `Record`,
- `FieldType`,
- `FieldOption`,
- `FieldDefinition`,
- `RecordTypeDefinition`.

They are intentionally not wired into the running application yet. This keeps MVP-006, MVP-007 and MVP-008 as safe foundations without changing database schema, UI behavior or data persistence.

### Field configuration loader

Field configuration loading starts in `services/field_config_service.py`.

`FieldConfigService` is responsible for:

- reading a JSON file with field definitions,
- checking that the root value is a list,
- converting raw dictionaries into `FieldDefinition`,
- converting select options into `FieldOption`.

It does not save configuration, load user-specific configuration or build UI controls yet.

### Record type configuration loader

Record type configuration loading starts in `services/record_type_config_service.py`.

`RecordTypeConfigService` is responsible for:

- reading a JSON file with one record type definition,
- checking that the root value is an object,
- checking that `fields` is a list,
- converting the raw dictionary into `RecordTypeDefinition`.

It does not save configuration, load user-specific configuration, validate field references against `FieldDefinition` or build UI controls yet.

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
- The new `domain/record.py` model is not yet mapped to `orders`.
- The field configuration model is not yet mapped to the current static form.
- The record type configuration model is not yet mapped to the current static form or database.
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

## MVP-006 generic record model foundation

MVP-006 added a small `domain` package:

- `domain/record.py`,
- `domain/__init__.py`.

Added generic concepts:

- `RecordField`,
- `RecordStatus`,
- `RecordType`,
- `Record`.

The current workshop-oriented model remains active as a transitional state:

- the SQLite schema still uses `orders`,
- existing UI fields and labels remain unchanged,
- `OrderService` still works with the current order-shaped data,
- no migration, new tables or new user-facing features were added.

Future MVPs should gradually connect the running application to the generic model. The main migration risks are preserving existing local data, mapping current `orders` columns to configurable fields, keeping status behavior compatible and avoiding a large combined schema/UI rewrite.

## MVP-007 configurable fields foundation

MVP-007 added:

- `domain/field_definition.py`,
- `config/default_record_fields.json`,
- `services/field_config_service.py`.

Added generic concepts:

- `FieldType`,
- `FieldOption`,
- `FieldDefinition`.

The supported field types are:

- `text`,
- `number`,
- `date`,
- `boolean`,
- `select`.

The current workshop-oriented model remains active as a transitional state. The default field configuration and loader are not connected to UI, SQLite or `OrderService`. No migration, new tables, dynamic form, dynamic list or user-facing feature was added.

Next safe steps are to validate field definitions more strictly, map the default fields into a future `RecordType`, or add a read-only adapter. Those steps should still avoid changing the current UI and database schema.

## MVP-008 configurable record types foundation

MVP-008 added:

- `domain/record_type.py`,
- `config/default_record_type.json`,
- `services/record_type_config_service.py`.

Added generic concept:

- `RecordTypeDefinition`.

The default record type configuration is neutral:

- `id`: `default`,
- `name`: `Default record`,
- `fields`: `title`, `description`, `status`, `created_date`.

The current workshop-oriented model remains active as a transitional state. The default record type configuration and loader are not connected to UI, SQLite or `OrderService`. No migration, new tables, dynamic form, dynamic list or user-facing feature was added.

Next safe steps are to validate that record type field references exist in loaded field definitions, build a read-only adapter that combines `RecordTypeDefinition` and `FieldDefinition`, or prepare documentation for user-owned type configuration. Those steps should still avoid changing the current UI and database schema.

## Zasady techniczne

- Nie zmieniac schematu bazy danych bez wyraznego zadania.
- Nie dodawac zaleznosci bez decyzji architektonicznej.
- Nie przenosic plikow bez potrzeby.
- Wydzielanie modulow robic stopniowo.
- Zachowywac kompatybilnosc z obecnym dzialaniem aplikacji.
- Dokumentowac istotne decyzje w `docs/DECISIONS.md`.

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
- `config/app_config.json` zawiera neutralna domyslna konfiguracje aplikacji.
- `config/default_record_fields.json` zawiera neutralna domyslna konfiguracje przyszlych pol rekordow.
- `config/default_record_type.json` zawiera neutralna domyslna konfiguracje przyszlego typu rekordu.
- `config/default_sections.json` zawiera neutralna domyslna konfiguracje przyszlych sekcji/kart.
- `ui/app.py` zawiera aplikacje Tkinter, ustawienia, logike UI, archiwum i backup.
- `ui/__init__.py` oznacza `ui` jako pakiet warstwy UI.
- `domain/record.py` zawiera fundament generycznego modelu domenowego rekordow.
- `domain/app_config.py` zawiera fundament modelu konfiguracji aplikacji.
- `domain/app_section.py` zawiera fundament modelu sekcji/kart aplikacji.
- `domain/field_definition.py` zawiera fundament definicji konfigurowalnych pol.
- `domain/record_type.py` zawiera fundament definicji konfigurowalnych typow rekordow.
- `domain/__init__.py` oznacza `domain` jako pakiet domenowy.
- `services/app_config_service.py` zawiera loader konfiguracji aplikacji z JSON.
- `services/config_service.py` zawiera centralny serwis konfiguracji agregujacy szczegolowe loadery.
- `services/config_validation_service.py` zawiera podstawowa walidacje konfiguracji.
- `services/field_config_service.py` zawiera loader konfiguracji pol z JSON.
- `services/record_type_config_service.py` zawiera loader konfiguracji typu rekordu z JSON.
- `services/section_config_service.py` zawiera loader konfiguracji sekcji/kart z JSON.
- `services/order_service.py` zawiera przejsciowy serwis logiki rekordow/zlecen.
- `services/__init__.py` oznacza `services` jako pakiet serwisow aplikacyjnych.
- `tools/check_config.py` zawiera developerska diagnostyke ladowania i walidacji konfiguracji.
- `tools/__init__.py` oznacza `tools` jako pakiet narzedzi developerskich.
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

## Fundament konfiguracji aplikacji

`domain/app_config.py` wprowadza neutralne pojecia konfiguracji aplikacji:

- `AppSection` dla sekcji aplikacji,
- `AppConfig` dla konfiguracji z nazwa aplikacji, aktywnym typem rekordu i lista sekcji.

Domyslna konfiguracja znajduje sie w `config/app_config.json`. Jest neutralna i zawiera:

- `app_name`: `Manager`,
- `active_record_type_id`: `default`,
- sekcje `Dashboard`, `Records`, `Archive`.

`services/app_config_service.py` zawiera `AppConfigService`, ktory wczytuje konfiguracje aplikacji z JSON i mapuje ja na obiekty domenowe. `app_name` z tej konfiguracji jest uzywany jako tytul okna aplikacji przez `ui/app.py`. Pozostale elementy konfiguracji aplikacji nie sa jeszcze podlaczone do obecnych kart ani bazy danych. Przyszly ekran ustawien i ikona zebatki sa osobnym MVP.

## Szkielet ustawien

`ui/app.py` zawiera pierwszy, subtelny szkielet ustawien. W gornym pasku UI znajduje sie przycisk z zebatka, ktory otwiera proste okno ustawien.

Okno pozwala edytowac:

- nazwe aplikacji,

oraz pokazuje informacyjnie:

- aktywny typ rekordu,
- liczbe sekcji/kart,
- liste sekcji/kart z `config/default_sections.json`,
- informacje, ze edycja kart, typow rekordow i pol zostanie dodana pozniej.

Zapis nazwy aplikacji korzysta z `ConfigService.save_app_config()` i trafia do `config/app_config.json`. Przed zapisem wykonywana jest walidacja konfiguracji. Podglad sekcji korzysta z `ConfigService` i pokazuje nazwe, id, typ, widocznosc oraz kolejnosc. Jesli konfiguracja nie zaladuje sie poprawnie, UI pokazuje fallback zamiast przerywac dzialanie aplikacji. Ten szkielet nie dodaje edytora kart, typow rekordow ani pol, nie przebudowuje dynamicznie UI i nie zmienia schematu bazy danych.

## Fundament sekcji/kart aplikacji

`domain/app_section.py` wprowadza neutralne pojecie `AppSectionDefinition`.

Definicja sekcji/karty zawiera:

- `id`,
- `name`,
- `type`,
- opcjonalne `record_type_id`,
- `visible`,
- `order`.

Domyslna konfiguracja znajduje sie w `config/default_sections.json`. Jest neutralna i zawiera sekcje `dashboard`, `records`, `archive` oraz `settings`.

`services/section_config_service.py` zawiera `SectionConfigService`, ktory wczytuje liste sekcji z JSON i mapuje ja na obiekty domenowe. Loader nie jest jeszcze podlaczony do UI, obecnych zakladek, menu ani bazy danych. Przyszla ikona zebatki, ekran ustawien, edytor kart i dynamiczne menu sa osobnymi MVP.

## Centralny serwis konfiguracji

`services/config_service.py` wprowadza `ConfigService` i `ManagerConfig`.

`ConfigService` agreguje istniejace loadery:

- `AppConfigService`,
- `FieldConfigService`,
- `RecordTypeConfigService`,
- `SectionConfigService`.

Udostepnia metody:

- `load_app_config()`,
- `load_field_definitions()`,
- `load_record_type()`,
- `load_sections()`,
- `load_all()`.

Centralny serwis nie duplikuje logiki szczegolowych loaderow. Jest przygotowaniem pod przyszla ikone zebatki, ekran ustawien, konfigurator pol i konfigurator kart. Nie jest jeszcze podlaczony do UI i nie zapisuje konfiguracji.

## Fundament walidacji konfiguracji

`services/config_validation_service.py` wprowadza `ConfigValidationService` i `ConfigValidationResult`.

Walidator sprawdza podstawowe wymagania dla:

- konfiguracji aplikacji,
- definicji pol,
- typu rekordu,
- sekcji.

Sprawdzane sa tylko proste reguly:

- wymagane pola tekstowe nie sa puste,
- listy maja poprawny typ,
- typy logiczne i liczbowe maja poprawny typ,
- typ pola nalezy do `text`, `number`, `date`, `boolean`, `select`,
- identyfikatory pol i sekcji nie sa powielone w swoich listach.

Walidacja nie jest jeszcze pelnym systemem ustawien, nie jest podlaczona do UI i nie przerywa startu aplikacji.

## Diagnostyka konfiguracji

`tools/check_config.py` jest prostym narzedziem developerskim do sprawdzenia konfiguracji z konsoli:

```text
python tools/check_config.py
```

Skrypt laduje konfiguracje przez `ConfigService`, a nastepnie uruchamia `ConfigService.validate_all()`, ktory korzysta z `ConfigValidationService`. Poprawna konfiguracja wypisuje `Configuration check: OK`. Problemy z ladowaniem albo walidacja wypisuja krotka, czytelna liste bledow.

To nie jest element UI, ekran ustawien ani ikona zebatki. Skrypt nie zmienia konfiguracji, nie zmienia schematu bazy danych i nie wplywa na start aplikacji przez `python main.py`. Przyszly ekran ustawien powinien korzystac z tych samych uslug konfiguracji i walidacji.

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

Generic domain model definitions live in `domain/record.py`, `domain/field_definition.py`, `domain/record_type.py`, `domain/app_config.py` and `domain/app_section.py`.

The modules currently contain simple structures only:

- `RecordField`,
- `RecordStatus`,
- `RecordType`,
- `Record`,
- `FieldType`,
- `FieldOption`,
- `FieldDefinition`,
- `RecordTypeDefinition`,
- `AppSection`,
- `AppConfig`,
- `AppSectionDefinition`.

They are intentionally not wired into the running application yet. This keeps MVP-006 through MVP-010 as safe foundations without changing database schema, UI behavior or data persistence.

### Application configuration loader

Application configuration loading starts in `services/app_config_service.py`.

`AppConfigService` is responsible for:

- reading a JSON file with application configuration,
- checking that the root value is an object,
- checking that `sections` is a list,
- converting section dictionaries into `AppSection`,
- converting the raw dictionary into `AppConfig`.

It does not save configuration, load user-specific configuration, build a settings screen or add a settings icon yet. The current window title is the only UI value already using `app_name`.

### Central configuration service

Central configuration access starts in `services/config_service.py`.

`ConfigService` is responsible for:

- holding default paths to config files,
- delegating application config loading to `AppConfigService`,
- delegating field definition loading to `FieldConfigService`,
- delegating record type loading to `RecordTypeConfigService`,
- delegating section loading to `SectionConfigService`,
- returning a combined `ManagerConfig` through `load_all()`,
- validating the combined configuration through `validate_all()`,
- writing application config, field definitions, record type config and section config back to JSON.

It does not replace the detailed loaders, build settings UI, add a gear icon or change runtime behavior yet. Config writing is available as a technical foundation and is not connected to UI.

### Configuration validation service

Configuration validation starts in `services/config_validation_service.py`.

`ConfigValidationService` is responsible for:

- validating `AppConfig`,
- validating field definitions,
- validating `RecordTypeDefinition`,
- validating section definitions,
- returning `ConfigValidationResult` with a list of errors.

It intentionally performs shallow validation only. It does not yet validate every cross-file relationship and it does not stop the current application from starting.

### Section configuration loader

Section configuration loading starts in `services/section_config_service.py`.

`SectionConfigService` is responsible for:

- reading a JSON file with section definitions,
- checking that the root value is a list,
- converting section dictionaries into `AppSectionDefinition`.

It does not save configuration, load user-specific configuration, build dynamic tabs, build dynamic menus, switch views or add a settings icon yet.

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
- The application configuration model is mapped only to the current window title. It is not yet mapped to tabs, sections or other UI behavior.
- The section configuration model is not yet mapped to the current Tkinter notebook or navigation.
- The central configuration service is not yet used by UI.
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

## MVP-009 application configuration foundation

MVP-009 added:

- `domain/app_config.py`,
- `config/app_config.json`,
- `services/app_config_service.py`.

Added generic concepts:

- `AppSection`,
- `AppConfig`.

The default application configuration is neutral:

- `app_name`: `Manager`,
- `active_record_type_id`: `default`,
- `sections`: `Dashboard`, `Records`, `Archive`.

The current workshop-oriented UI remains active as a transitional state. After MVP-015, `app_name` from the application configuration is used as the window title. The rest of the application configuration is not connected to SQLite, tabs or runtime UI behavior. No settings screen, gear icon, migration, new table or broader user-facing feature was added.

Next safe steps are to validate application configuration more strictly or plan a separate MVP for a subtle settings screen under a gear icon. Those steps should still avoid changing the current database schema.

## MVP-010 application sections foundation

MVP-010 added:

- `domain/app_section.py`,
- `config/default_sections.json`,
- `services/section_config_service.py`.

Added generic concept:

- `AppSectionDefinition`.

The default section configuration is neutral:

- `dashboard`,
- `records`,
- `archive`,
- `settings`.

The current workshop-oriented UI remains active as a transitional state. The section configuration and loader are not connected to UI, SQLite, menu, notebook tabs or view switching. No settings screen, gear icon, dynamic menu, migration, new table or user-facing feature was added.

Next safe steps are to validate section configuration more strictly or plan a separate MVP for a subtle settings screen under a gear icon. Those steps should still avoid changing the current database schema.

## MVP-011 central configuration service

MVP-011 added:

- `services/config_service.py`.

Added concepts:

- `ConfigService`,
- `ManagerConfig`.

`ConfigService` aggregates:

- application configuration,
- field definitions,
- record type configuration,
- section configuration.

The detailed loaders remain in place and still own JSON parsing for their specific configuration files. The central service is only a thin access layer for future settings work. It is not connected to UI and does not add any user-facing feature.

## MVP-012 configuration writing foundation

MVP-012 extended:

- `services/config_service.py`.

Added write methods:

- `save_app_config()`,
- `save_field_definitions()`,
- `save_record_type()`,
- `save_sections()`,
- `save_all()`.

The writable config files are:

- `config/app_config.json`,
- `config/default_record_fields.json`,
- `config/default_record_type.json`,
- `config/default_sections.json`.

JSON writing uses the Python standard library with `ensure_ascii=False` and `indent=2`. The writer serializes the existing domain objects into the current JSON structures. It is not connected to UI and does not change application behavior.

Known risks:

- There is no automatic backup before writing configuration files yet.
- There is no user-specific configuration location yet.
- Future settings UI must validate changes before saving and handle write errors clearly.

## MVP-013 configuration validation foundation

MVP-013 added:

- `services/config_validation_service.py`.

MVP-013 extended:

- `services/config_service.py` with `validate_all()`.

Added concepts:

- `ConfigValidationService`,
- `ConfigValidationResult`.

The validator checks application config, field definitions, record type and sections. It returns a list of readable error messages and does not raise a full custom exception system.

The validator is not connected to UI and does not block application startup. Future settings UI should call validation before saving configuration changes.

## MVP-014 configuration diagnostics

MVP-014 added:

- `tools/__init__.py`,
- `tools/check_config.py`.

The diagnostic script gives developers a console check for configuration loading and validation:

```text
python tools/check_config.py
```

It uses the existing `ConfigService` and `ConfigValidationService` path. It does not add a user-facing feature, does not connect anything to Tkinter, does not change database schema and does not add dependencies. Future settings UI should reuse these same configuration and validation services instead of creating a separate validation path.

## MVP-015 window title from configuration

MVP-015 connected one small part of application configuration to the current UI:

- `ui/app.py` loads `app_name` from `config/app_config.json` through `ConfigService`,
- `WorkshopApp` uses that value as the Tkinter window title,
- the fallback title is `Manager` when configuration loading fails or the name is empty.

This is the first small integration between configuration and UI. It does not add a settings screen, gear icon, name editor, dynamic UI, database migration or new dependency. The rest of the application still uses the old transitional UI and data model.

## MVP-016 settings preview skeleton

MVP-016 added a small read-only settings preview:

- `ui/app.py` shows a subtle `Ustawienia` button in the top bar,
- clicking it opens a simple modal with configuration details,
- the modal shows application name, active record type and section/tab count,
- the modal uses `ConfigService` and shows a fallback if configuration loading fails.

This is only a skeleton. It does not allow editing, does not save configuration from UI, does not add a full settings screen, does not add card or field editors, does not dynamically rebuild the UI and does not change the database schema. The current application still runs on the old transitional UI.

## MVP-017 application name editing

MVP-017 made application name the first editable settings value:

- the settings modal contains a text field for `app_name`,
- `Zapisz` validates the configuration and writes the updated value to `config/app_config.json` through `ConfigService.save_app_config()`,
- an empty name is rejected and not saved,
- after a successful save, the current window title is updated.

This does not add card editing, field editing, record type editing, dynamic UI rebuilding, database migration, new tables or new dependencies. Those remain separate MVPs.

## MVP-018 sections preview in settings

MVP-018 added a read-only sections/tabs preview to the existing settings modal:

- sections are loaded through `ConfigService` from `config/default_sections.json`,
- the preview shows section name, id, type, visibility and order,
- configuration loading errors show a safe fallback instead of crashing the UI,
- application name editing from MVP-017 remains unchanged.

This does not add section editing, adding, deleting or dynamic rebuilding of the main UI. Section editor, field editor and record type editor remain separate future MVPs.

## Zasady techniczne

- Nie zmieniac schematu bazy danych bez wyraznego zadania.
- Nie dodawac zaleznosci bez decyzji architektonicznej.
- Nie przenosic plikow bez potrzeby.
- Wydzielanie modulow robic stopniowo.
- Zachowywac kompatybilnosc z obecnym dzialaniem aplikacji.
- Dokumentowac istotne decyzje w `docs/DECISIONS.md`.

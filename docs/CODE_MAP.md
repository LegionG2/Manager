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
|-- config/
|   |-- app_config.json
|   |-- default_record_fields.json
|   |-- default_record_type.json
|   `-- default_sections.json
|-- data/
|   |-- __init__.py
|   `-- database.py
|-- domain/
|   |-- __init__.py
|   |-- app_config.py
|   |-- app_section.py
|   |-- field_definition.py
|   |-- record_type.py
|   `-- record.py
|-- services/
|   |-- __init__.py
|   |-- app_config_service.py
|   |-- config_service.py
|   |-- config_validation_service.py
|   |-- field_config_service.py
|   |-- order_service.py
|   |-- record_type_config_service.py
|   `-- section_config_service.py
|-- tools/
|   |-- __init__.py
|   `-- check_config.py
|-- ui/
|   |-- __init__.py
|   `-- app.py
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

### `config/app_config.json`

Kategoria: konfiguracja aplikacji.

Co robi:

- zawiera neutralna domyslna konfiguracje aplikacji,
- definiuje `app_name` jako `Manager`,
- wskazuje `active_record_type_id` jako `default`,
- opisuje sekcje `Dashboard`, `Records` i `Archive`.

Ryzyka i niejasne obszary:

- `app_name` jest juz uzywany jako tytul okna aplikacji.
- Pozostale elementy pliku nie sa jeszcze podlaczone do UI ani bazy danych.
- Nie istnieje jeszcze ekran ustawien ani ikona zebatki.
- Przyszle zmiany musza rozstrzygnac, gdzie bedzie zapisywana konfiguracja uzytkownika.

### `config/default_record_fields.json`

Kategoria: konfiguracja, fundament pol rekordow.

Co robi:

- zawiera neutralna domyslna konfiguracje pol przyszlego rekordu,
- opisuje pola `title`, `description`, `status` i `created_date`,
- uzywa typow `text`, `date` i `select`.

Ryzyka i niejasne obszary:

- Plik nie jest jeszcze podlaczony do UI ani bazy danych.
- To przyklad techniczny, a nie preset branzowy ani docelowy konfigurator.
- Przyszle zmiany musza rozstrzygnac, gdzie bedzie zapisywana konfiguracja uzytkownika.

### `config/default_record_type.json`

Kategoria: konfiguracja, fundament typow rekordow.

Co robi:

- zawiera neutralna domyslna konfiguracje typu rekordu,
- definiuje typ `default` o nazwie `Default record`,
- wskazuje liste identyfikatorow pol: `title`, `description`, `status`, `created_date`.

Ryzyka i niejasne obszary:

- Plik nie jest jeszcze podlaczony do UI ani bazy danych.
- To techniczny przyklad konfiguracji typu rekordu, a nie preset branzowy.
- Nie istnieje jeszcze edytor typow rekordow ani zapis konfiguracji uzytkownika.

### `config/default_sections.json`

Kategoria: konfiguracja, fundament sekcji/kart aplikacji.

Co robi:

- zawiera neutralna domyslna konfiguracje przyszlych sekcji aplikacji,
- definiuje sekcje `dashboard`, `records`, `archive` i `settings`,
- opisuje kolejnosc, widocznosc, typ sekcji i opcjonalne powiazanie z typem rekordu.

Ryzyka i niejasne obszary:

- Plik jest uzywany przez ustawienia i przez szkielet glownych zakladek Tkinter.
- Sekcja `settings` moze byc pokazana jako placeholder, ale nie oznacza jeszcze pelnego ekranu ustawien.
- Nie istnieje jeszcze pelny edytor kart ani dynamiczne menu.

### `main.py`

Kategoria: punkt wejscia.

Co robi:

- importuje `WorkshopApp` z `ui.app`,
- tworzy instancje aplikacji,
- uruchamia `mainloop()`.

Ryzyka i niejasne obszary:

- Punkt startowy nadal uruchamia obecna aplikacje warsztatowa, bo nie zmieniano zachowania ani nazewnictwa UI.

### `data/__init__.py`

Kategoria: dane.

Co robi:

- oznacza `data` jako pakiet Pythona dla warstwy danych.

Ryzyka i niejasne obszary:

- Na ten moment nie zawiera logiki.

### `data/database.py`

Kategoria: dane, SQLite, eksport CSV.

Co robi:

- zawiera klase `Database` przeniesiona z `main.py`,
- otwiera polaczenie SQLite,
- ustawia `sqlite3.Row`,
- tworzy tabele `orders`,
- wykonuje dotychczasowe migracje kolumn,
- dodaje, aktualizuje, usuwa i pobiera rekordy,
- liczy statystyki dla obecnego UI,
- eksportuje dane z `orders` do CSV.

Ryzyka i niejasne obszary:

- Schemat `orders` nie jest jeszcze generycznym modelem rekordow.
- Zapytania nadal zawieraja obecne statusy i zalozenia starego modelu.
- Eksport CSV nadal jest czescia klasy `Database`; w przyszlosci moze zostac wydzielony.
- `Database.conn` nadal jest uzywane w `ui/app.py` przy backupie.
- Nie zmieniono schematu bazy ani zachowania migracji.

### `domain/__init__.py`

Kategoria: domena.

Co robi:

- oznacza `domain` jako pakiet Pythona dla przyszlych generycznych modeli domenowych.

Ryzyka i niejasne obszary:

- Na ten moment nie zawiera logiki.

### `domain/app_config.py`

Kategoria: domena, konfiguracja aplikacji.

Co robi:

- definiuje `AppSection` jako neutralny opis sekcji aplikacji,
- definiuje `AppConfig` jako konfiguracje z `app_name`, `active_record_type_id` i lista sekcji.

Ryzyka i niejasne obszary:

- Model konfiguracji aplikacji nie jest jeszcze podlaczony do UI.
- `app_name` z konfiguracji jest uzywany jako tytul okna aplikacji.
- Nie zmienia obecnych kart ani sekcji.
- Nie istnieje jeszcze zapis konfiguracji uzytkownika.

### `domain/app_section.py`

Kategoria: domena, konfiguracja sekcji/kart aplikacji.

Co robi:

- definiuje `AppSectionDefinition`,
- opisuje generyczna sekcje lub karte aplikacji przez `id`, `name`, `type`, `visible`, `order` i opcjonalne `record_type_id`.

Ryzyka i niejasne obszary:

- Model sekcji jest uzywany przez ustawienia i przez szkielet zakladek Tkinter.
- Pelny system dynamicznych widokow jeszcze nie istnieje.
- Edytor sekcji jest ograniczony do prostego zapisu JSON i nie jest jeszcze konfiguracja per uzytkownik.

### `domain/record.py`

Kategoria: domena, generyczny model rekordow.

Co robi:

- definiuje `RecordField` jako opis pojedynczego pola rekordu,
- definiuje `RecordStatus` jako neutralny status rekordu,
- definiuje `RecordType` jako opis typu rekordu z polami i statusami,
- definiuje `Record` jako neutralny rekord z typem, wartosciami, statusem i opcjonalnym identyfikatorem.

Ryzyka i niejasne obszary:

- Model domenowy nie jest jeszcze podlaczony do UI, `OrderService` ani SQLite.
- Nie istnieje jeszcze migracja z tabeli `orders` do generycznego modelu.
- Przyszle podpiecie musi uwzglednic istniejace dane uzytkownika i zgodnosc z obecnym zachowaniem.
- Obecny model warsztatowy nadal dziala jako stan przejsciowy.

### `domain/field_definition.py`

Kategoria: domena, konfiguracja pol rekordow.

Co robi:

- definiuje `FieldType` z typami `text`, `number`, `date`, `boolean` i `select`,
- definiuje `FieldOption` jako opcje dla pol wyboru,
- definiuje `FieldDefinition` jako generyczny opis pola rekordu.

Ryzyka i niejasne obszary:

- Model definicji pol nie jest jeszcze podlaczony do dynamicznego formularza.
- Nie istnieje jeszcze walidacja runtime dla wszystkich typow pol.
- Nie ma jeszcze zapisu konfiguracji uzytkownika ani migracji danych.

### `domain/record_type.py`

Kategoria: domena, konfiguracja typow rekordow.

Co robi:

- definiuje `RecordTypeDefinition`,
- opisuje generyczny typ rekordu przez `id`, `name`, opcjonalny `description` i liste identyfikatorow pol.

Ryzyka i niejasne obszary:

- Model typu rekordu nie jest jeszcze podlaczony do UI, bazy ani dynamicznych formularzy.
- Lista pol wskazuje identyfikatory, ale nie jest jeszcze walidowana wzgledem `FieldDefinition`.
- Obecny model `orders` nadal dziala jako stan przejsciowy.

### `services/__init__.py`

Kategoria: logika aplikacyjna.

Co robi:

- oznacza `services` jako pakiet Pythona dla serwisow aplikacyjnych.

Ryzyka i niejasne obszary:

- Na ten moment nie zawiera logiki.

### `services/app_config_service.py`

Kategoria: konfiguracja, logika aplikacyjna.

Co robi:

- zawiera `AppConfigService`,
- wczytuje konfiguracje aplikacji z pliku JSON,
- mapuje JSON na `AppConfig` i `AppSection`,
- sprawdza, czy konfiguracja jest obiektem i czy `sections` jest lista.

Ryzyka i niejasne obszary:

- Loader nie jest jeszcze uzywany przez UI.
- Loader nie zapisuje konfiguracji i nie obsluguje konfiguracji per uzytkownik.
- Nie dodaje ekranu ustawien ani ikony zebatki.
- Nie zmienia schematu SQLite ani obecnego modelu `orders`.

### `services/config_service.py`

Kategoria: konfiguracja, logika aplikacyjna.

Co robi:

- zawiera `ConfigService`,
- zawiera `ManagerConfig` jako zebrany wynik wczytania konfiguracji,
- agreguje `AppConfigService`, `FieldConfigService`, `RecordTypeConfigService` i `SectionConfigService`,
- korzysta z `ConfigValidationService` dla jawnej walidacji konfiguracji,
- udostepnia metody `load_app_config()`, `load_field_definitions()`, `load_record_type()`, `load_sections()` i `load_all()`,
- udostepnia metody zapisu `save_app_config()`, `save_field_definitions()`, `save_record_type()`, `save_sections()` i `save_all()`,
- udostepnia `validate_all()`,
- korzysta z plikow JSON w katalogu `config`.

Ryzyka i niejasne obszary:

- Centralny serwis jest uzywany przez szkielet ustawien i ladowanie sekcji w UI.
- Nie zastępuje szczegolowych loaderow i nie usuwa ich odpowiedzialnosci.
- Zapis konfiguracji jest uzywany dla nazwy aplikacji i sekcji.
- Nie obsluguje konfiguracji per uzytkownik.
- Nie jest jeszcze pelnym systemem edycji ustawien.

### `services/config_validation_service.py`

Kategoria: konfiguracja, walidacja.

Co robi:

- zawiera `ConfigValidationService`,
- zawiera `ConfigValidationResult`,
- waliduje podstawowe wymagania konfiguracji aplikacji, definicji pol, typu rekordu i sekcji,
- zwraca liste czytelnych komunikatow bledow,
- sprawdza m.in. puste identyfikatory, wymagane nazwy, listy oraz dozwolone typy pol.

Ryzyka i niejasne obszary:

- Walidator nie jest jeszcze podlaczony do UI.
- Walidator nie przerywa startu aplikacji.
- To nie jest pelny system ustawien ani pelna walidacja relacji miedzy wszystkimi plikami.
- Przyszly ekran ustawien powinien uzywac walidacji przed zapisem.

### `services/order_service.py`

Kategoria: logika aplikacyjna, rekordy/zlecenia.

Co robi:

- zawiera klase `OrderService`,
- deleguje generowanie numeru zlecenia do `Database`,
- przygotowuje dane formularza do zapisu w obecnym modelu `orders`,
- waliduje pola wymagane i kwoty przed zapisem,
- liczy koszt laczny i saldo,
- wylicza stan terminu dla tabeli,
- obsluguje logike wyszukiwania i sortowania rekordow,
- przygotowuje dane duplikowanego zlecenia,
- wykonuje proste operacje na rekordach: zapis, usuniecie, zmiana statusu, archiwizacja i przywrocenie.

Ryzyka i niejasne obszary:

- Nazwa `OrderService` jest przejsciowa, bo obecny schemat nadal uzywa tabeli `orders` i warsztatowych pol.
- Serwis nadal zna konkretne kolumny `orders`, statusy i pola formularza.
- Serwis korzysta bezposrednio z `Database`; nie ma jeszcze osobnego generycznego modelu domenowego.
- To nie jest jeszcze docelowy serwis generycznych rekordow.

### `services/field_config_service.py`

Kategoria: konfiguracja, logika aplikacyjna.

Co robi:

- zawiera `FieldConfigService`,
- wczytuje liste definicji pol z pliku JSON,
- mapuje JSON na `FieldDefinition`, `FieldType` i `FieldOption`,
- sprawdza, czy konfiguracja ma postac listy obiektow.

Ryzyka i niejasne obszary:

- Loader nie jest jeszcze uzywany przez UI.
- Loader nie zapisuje konfiguracji i nie obsluguje konfiguracji per uzytkownik.
- Nie zmienia schematu SQLite ani obecnego modelu `orders`.

### `services/record_type_config_service.py`

Kategoria: konfiguracja, logika aplikacyjna.

Co robi:

- zawiera `RecordTypeConfigService`,
- wczytuje konfiguracje typu rekordu z pliku JSON,
- mapuje JSON na `RecordTypeDefinition`,
- sprawdza, czy konfiguracja typu jest obiektem i czy `fields` jest lista.

Ryzyka i niejasne obszary:

- Loader nie jest jeszcze uzywany przez UI.
- Loader nie laczy jeszcze typu rekordu z definicjami pol.
- Loader nie zapisuje konfiguracji i nie obsluguje konfiguracji per uzytkownik.
- Nie zmienia schematu SQLite ani obecnego modelu `orders`.

### `services/section_config_service.py`

Kategoria: konfiguracja, logika aplikacyjna.

Co robi:

- zawiera `SectionConfigService`,
- wczytuje liste sekcji z pliku JSON,
- mapuje JSON na `AppSectionDefinition`,
- sprawdza, czy konfiguracja sekcji ma postac listy obiektow.

Ryzyka i niejasne obszary:

- Loader jest uzywany przez `ConfigService`, ustawienia i szkielet glownych zakladek.
- Loader nie buduje samodzielnie dynamicznych zakladek ani menu.
- Loader nie zapisuje konfiguracji i nie obsluguje konfiguracji per uzytkownik.
- Nie zmienia schematu SQLite ani obecnego modelu `orders`.

### `tools/__init__.py`

Kategoria: narzedzia developerskie.

Co robi:

- oznacza `tools` jako pakiet Pythona dla pomocniczych narzedzi developerskich.

Ryzyka i niejasne obszary:

- Na ten moment nie zawiera logiki.

### `tools/check_config.py`

Kategoria: narzedzia developerskie, diagnostyka konfiguracji.

Co robi:

- pozwala uruchomic diagnostyke konfiguracji z konsoli przez `python tools/check_config.py`,
- laduje konfiguracje przez `ConfigService`,
- uruchamia walidacje przez `ConfigValidationService` za posrednictwem `ConfigService.validate_all()`,
- wypisuje `Configuration check: OK`, gdy konfiguracja jest poprawna,
- wypisuje czytelna liste bledow, gdy konfiguracja nie laduje sie albo nie przechodzi walidacji.

Ryzyka i niejasne obszary:

- To narzedzie developerskie, nie element UI.
- Nie jest ekranem ustawien ani ikona zebatki.
- Nie zmienia obecnego startu aplikacji, schematu SQLite ani plikow konfiguracji.
- Przyszly ekran ustawien powinien korzystac z tych samych uslug konfiguracji i walidacji.

### `ui/__init__.py`

Kategoria: UI.

Co robi:

- oznacza `ui` jako pakiet Pythona dla warstwy interfejsu.

Ryzyka i niejasne obszary:

- Na ten moment nie zawiera logiki.

### `ui/app.py`

Kategoria: UI, konfiguracja.

Co robi:

- definiuje tytul aplikacji, nazwy plikow danych i ustawien,
- laduje `app_name` z konfiguracji przez `ConfigService` i uzywa go jako tytulu okna,
- uzywa `app_name` z konfiguracji jako glownego naglowka aplikacji,
- pokazuje subtelny przycisk ustawien z edycja nazwy aplikacji, edycja istniejacych sekcji/kart, dodawaniem sekcji, usuwaniem niestandardowych sekcji oraz podgladem typu rekordu i pol,
- porzadkuje okno ustawien w sekcje `Ogolne`, `Sekcje aplikacji`, `Typ rekordu` i `Pola`,
- buduje i odswieza glowne zakladki z widocznych sekcji konfiguracji jako bezpieczny szkielet,
- definiuje obecne statusy i priorytety,
- definiuje motywy jasny i ciemny,
- zarzadza ustawieniami lokalnymi przez JSON,
- importuje `Database` z `data.database`,
- tworzy `OrderService` z `services.order_service`,
- buduje glowne okno aplikacji,
- buduje zakladki aktywnych rekordow i archiwum,
- obsluguje formularz, tabele, filtrowanie, archiwum, backup i eksport CSV.

Znane elementy:

- `get_app_data_dir()` wybiera lokalny katalog danych uzytkownika.
- `resource_path()` buduje sciezki do plikow danych.
- `SettingsManager` obsluguje plik ustawien JSON.
- `WorkshopApp` laczy UI Tkinter z logika aplikacji.
- Czystsza czesc logiki rekordow zostala wydzielona do `OrderService`.

Ryzyka i niejasne obszary:

- Modul UI nadal laczy wiele odpowiedzialnosci, co utrudnia bezpieczne zmiany.
- Nazwy i model danych sa nadal zwiazane ze starsza aplikacja warsztatowa.
- Glowny naglowek jest juz neutralny, ale czesc starszych pol i tekstow nadal jest przejsciowo warsztatowa.
- UI nadal zna konkretne kolumny aktualnego modelu danych przy budowaniu tabel i wypelnianiu formularza.
- Szkielet ustawien zapisuje nazwe aplikacji oraz wybrane pola istniejacych sekcji/kart; pozwala dodawac sekcje, usuwac sekcje niestandardowe, chroni sekcje bazowe, a typ rekordu i pola sa pokazywane read-only.
- Glowne zakladki korzystaja z konfiguracji sekcji i sa odswiezane po zmianach sekcji; typy `dashboard`, `settings` i `custom` maja proste widoki, ale pelny system dynamicznych widokow nie istnieje jeszcze.
- Backup nadal korzysta bezposrednio z `self.db.conn`.
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

Na ten moment granice odpowiedzialnosci sa lepsze niz na starcie. Punkt wejscia znajduje sie w `main.py`, dostep do danych w `data/database.py`, fundament generycznej domeny w `domain/record.py`, czesc logiki rekordow w `services/order_service.py`, a obecna aplikacja Tkinter w `ui/app.py`.

Przy przyszlym rozwoju warto stopniowo wydzielac:

- warstwe danych,
- warstwe konfiguracji,
- warstwe UI,
- logike rekordow,
- modele domenowe,
- logike importu i eksportu,
- logike wyszukiwania i filtrowania,
- migracje danych.

Nie nalezy robic tego jednym duzym refaktorem.

## MVP-002 - Dokladniejsza mapa `main.py`

### Punkt wejscia aplikacji

Stan opisany w MVP-002 dotyczyl kodu przed wydzieleniem UI. Po MVP-004 punkt wejscia znajduje sie w `main.py`, a implementacja UI w `ui/app.py`.

Punkt wejscia:

- tworzona jest instancja `WorkshopApp`,
- uruchamiany jest `app.mainloop()`.

Oznacza to, ze `main.py` jest juz tylko plikiem startowym aplikacji.

### Stale i zalozenia globalne

Stale przeniesiono do `ui/app.py`:

- `APP_TITLE`,
- `DB_NAME`,
- `SETTINGS_NAME`,
- `STATUSES`,
- `PRIORITIES`,
- `THEMES`,
- `PRIORITY_TAGS`.

Obecne ryzyka:

- `APP_TITLE` nadal jest uzywany przez czesc komunikatow UI jako przejsciowy tytul dialogow.
- `DB_NAME` i katalog danych zawieraja nazwy zwiazane ze stara aplikacja warsztatowa.
- `STATUSES` i `PRIORITIES` sa hardcodowane w kodzie.
- Statusy, priorytety, nazwy plikow i czesc etykiet UI nie sa jeszcze konfigurowalne.
- Zmiana tych wartosci moze wplynac jednoczesnie na UI, sortowanie, filtry, dane i eksport.

### Kod zwiazany z baza danych

Kod bazy danych znajduje sie w `data/database.py`, w klasie `Database`.

Znane metody:

- `create_tables()` tworzy tabele `orders`.
- `migrate_tables()` dodaje brakujace kolumny do `orders`.
- `generate_next_order_no()` generuje numer rekordu w obecnym formacie.
- `add_order()` dodaje rekord.
- `update_order()` aktualizuje rekord.
- `delete_order()` usuwa rekord.
- `fetch_orders()` pobiera liste rekordow z wyszukiwaniem, filtrem statusu i archiwum.
- `fetch_order()` pobiera jeden rekord.
- `stats()` nadal liczy podsumowania, ale globalny pasek statystyk w UI jest ukryty.
- `export_csv()` eksportuje dane do CSV.

Ryzyka:

- Model tabeli `orders` jest branzowy i nie jest jeszcze generycznym modelem rekordow.
- Zapytania SQL, wyszukiwanie, sortowanie i statystyki znaja konkretne kolumny.
- `migrate_tables()` wykonuje migracje przy starcie aplikacji.
- `Database` jest importowana i uzywana bezposrednio przez `WorkshopApp`, wiec UI i dane nadal sa mocno polaczone.
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
2. Wydzielic dalsze pomocnicze funkcje dostepu do danych bez zmiany schematu.
3. Wydzielic konfiguracje stalych i ustawien bez zmiany wartosci.
4. Wydzielic fragmenty UI do mniejszych funkcji lub modulow bez zmiany wygladu.
5. Dopiero pozniej projektowac generyczny model typow rekordow i pol.

## MVP-003 - Wydzielenie warstwy danych

Dodano pakiet `data` i modul `data/database.py`.

Przeniesiono z `main.py`:

- importy `csv`, `sqlite3` i `datetime` potrzebne klasie bazy,
- klase `Database`,
- tworzenie tabeli `orders`,
- migracje obecnych kolumn,
- operacje `add_order`, `update_order`, `delete_order`, `fetch_orders`, `fetch_order`,
- statystyki,
- eksport CSV.

Po MVP-003 zostalo w `main.py`; po MVP-004 te elementy przeniesiono dalej do `ui/app.py` poza samym punktem wejscia:

- punkt wejscia aplikacji,
- stale aplikacji,
- sciezki do lokalnych danych,
- `SettingsManager`,
- cala warstwa UI `WorkshopApp`,
- stan formularza i filtrow,
- akcje uzytkownika,
- backup pliku bazy danych.

Kolejne bezpieczne kroki po MVP-003:

- usunac bezposrednie uzycie `self.db.conn` z UI przez metode backupu w warstwie danych,
- wydzielic `SettingsManager` i sciezki danych do osobnego modulu konfiguracji,
- dopiero potem zaczac rozbijac UI,
- nie zmieniac schematu `orders` przed osobna decyzja migracyjna.

## MVP-004 - Wydzielenie warstwy UI

Dodano pakiet `ui` i modul `ui/app.py`.

Przeniesiono z `main.py`:

- importy i stale uzywane przez UI,
- funkcje sciezek `get_app_data_dir()` i `resource_path()`,
- `SettingsManager`,
- klase `WorkshopApp`,
- budowanie okna, zakladek, formularzy, tabel i stylow,
- obsluge akcji UI: zapis, edycje, usuwanie, wyszukiwanie, archiwum, eksport CSV i backup.

Zostalo w `main.py`:

- import `WorkshopApp`,
- funkcja `main()`,
- utworzenie aplikacji i `mainloop()`.

Sprzezenia, ktore nadal istnieja:

- `WorkshopApp` nadal bezposrednio tworzy `Database`.
- UI nadal zna kolumny tabeli `orders`, statusy, priorytety i obecne pola formularza.
- Walidacja, mapowanie formularza, sortowanie i filtrowanie nadal sa metodami UI.
- Backup nadal uzywa `self.db.conn` oraz sciezki pliku bazy.

Nastepny bezpieczny krok:

- wydzielic konfiguracje i sciezki danych z `ui/app.py` do malego modulu konfiguracyjnego albo przeniesc backup do `data/database.py`, bez zmiany wartosci, schematu ani zachowania UI.

## MVP-005 - Wydzielenie logiki aplikacyjnej rekordow

Dodano pakiet `services` i modul `services/order_service.py`.

Wydzielono z `ui/app.py`:

- parsowanie kwot,
- liczenie kosztu lacznego i salda,
- wyliczanie stanu terminu,
- logike dopasowania wyszukiwania,
- sortowanie obecnych rekordow,
- przygotowanie danych formularza do zapisu,
- domyslne wartosci formularza,
- przygotowanie danych duplikowanego zlecenia,
- proste operacje na rekordzie: zapis, usuniecie, zmiana statusu, archiwizacja i przywrocenie.

Zostalo w `ui/app.py`:

- budowanie okna, zakladek, tabel, formularza i stylow,
- zmienne Tkinter i odczyt/zapis wartosci widgetow,
- obsluga zdarzen, zaznaczen, messageboxow i filedialogow,
- wypelnianie tabel i formularza,
- eksport CSV wywolywany z UI,
- backup pliku bazy danych.

Sprzezenia, ktore nadal istnieja:

- `OrderService` nadal korzysta bezposrednio z `Database`.
- `OrderService` nadal zna tabele `orders`, pola zlecen i obecne statusy.
- `WorkshopApp` nadal zna kolumny bazy przy budowaniu tabel i uzupelnianiu formularza.
- Backup nadal uzywa `self.db.conn` w UI.

Nazwa `order_service.py` jest przejsciowa. Uzyto jej, bo obecny kod i baza nadal operuja na zleceniach (`orders`). Docelowo serwis powinien zostac zastapiony lub przemianowany przy wprowadzaniu generycznego modelu rekordow.

Nastepny bezpieczny krok:

- wydzielic backup z UI do warstwy danych albo wydzielic konfiguracje/sciezki danych, bez zmiany schematu i bez zmiany zachowania aplikacji.

## MVP-006 - Fundament generycznego modelu rekordu

Dodano pakiet `domain` i modul `domain/record.py`.

Wprowadzono generyczne pojecia:

- `RecordField` - opis pola rekordu,
- `RecordStatus` - neutralny status rekordu,
- `RecordType` - typ rekordu z lista pol i statusow,
- `Record` - instancja rekordu z typem, wartosciami, statusem i opcjonalnym ID.

Nie podlaczono jeszcze nowego modelu do:

- UI,
- `OrderService`,
- `Database`,
- schematu SQLite.

Obecny model warsztatowy nadal dziala jako stan przejsciowy:

- tabela `orders` pozostaje bez zmian,
- pola warsztatowe pozostaja w UI i serwisie,
- nie wykonano migracji danych,
- nie zmieniono widocznego zachowania aplikacji.

Ryzyka przyszlej migracji:

- trzeba zachowac istniejace lokalne dane uzytkownika,
- trzeba zaplanowac mapowanie kolumn `orders` na generyczne pola,
- trzeba oddzielic konfiguracje typow rekordow od danych rekordow,
- trzeba uniknac zmiany UI i zapisu danych w jednym duzym kroku.

Nastepny bezpieczny krok:

- opisac konfiguracje typow i pol rekordow albo przygotowac adapter mapujacy obecne `orders` na `Record` tylko do odczytu, bez zmiany schematu bazy.

## MVP-007 - Fundament konfigurowalnych pol

Dodano:

- `domain/field_definition.py`,
- `config/default_record_fields.json`,
- `services/field_config_service.py`.

Wprowadzono generyczne pojecia:

- `FieldType` - wspierane typy pol: `text`, `number`, `date`, `boolean`, `select`,
- `FieldOption` - opcja dla pola wyboru,
- `FieldDefinition` - definicja pola rekordu.

Domyslna konfiguracja pol znajduje sie w `config/default_record_fields.json` i zawiera neutralne pola:

- `title`,
- `description`,
- `status`,
- `created_date`.

`FieldConfigService` umie wczytac JSON z lista pol i zamienic go na obiekty domenowe. Loader nie jest jeszcze podlaczony do UI, bazy ani obecnego formularza.

Obecny model warsztatowy nadal dziala jako stan przejsciowy:

- tabela `orders` pozostaje bez zmian,
- formularze i tabele UI pozostaja statyczne,
- `OrderService` nadal obsluguje obecny model zlecen,
- nie dodano migracji ani nowych tabel.

Nastepny bezpieczny krok:

- dodac walidacje definicji pol albo przygotowac adapter tylko do odczytu, ktory mapuje domyslna konfiguracje na przyszly `RecordType`, bez zmiany UI i schematu bazy.

## MVP-008 - Fundament konfigurowalnych typow rekordow

Dodano:

- `domain/record_type.py`,
- `config/default_record_type.json`,
- `services/record_type_config_service.py`.

Wprowadzono generyczne pojecie:

- `RecordTypeDefinition` - definicja typu rekordu z `id`, `name`, opcjonalnym opisem i lista identyfikatorow pol.

Domyslna konfiguracja typu rekordu znajduje sie w `config/default_record_type.json` i zawiera neutralny typ:

- `id`: `default`,
- `name`: `Default record`,
- `fields`: `title`, `description`, `status`, `created_date`.

`RecordTypeConfigService` umie wczytac JSON typu rekordu i zamienic go na obiekt domenowy. Loader nie jest jeszcze podlaczony do UI, bazy, obecnego formularza ani `OrderService`.

Obecny model warsztatowy nadal dziala jako stan przejsciowy:

- tabela `orders` pozostaje bez zmian,
- formularze i tabele UI pozostaja statyczne,
- `OrderService` nadal obsluguje obecny model zlecen,
- nie dodano migracji ani nowych tabel.

Nastepny bezpieczny krok:

- dodac walidacje zgodnosci typu rekordu z definicjami pol albo przygotowac adapter tylko do odczytu laczacy `RecordTypeDefinition` z `FieldDefinition`, bez zmiany UI i schematu bazy.

## MVP-009 - Fundament konfiguracji aplikacji

Dodano:

- `domain/app_config.py`,
- `config/app_config.json`,
- `services/app_config_service.py`.

Wprowadzono generyczne pojecia:

- `AppSection` - neutralny opis sekcji aplikacji,
- `AppConfig` - konfiguracja aplikacji z `app_name`, `active_record_type_id` i lista sekcji.

Domyslna konfiguracja aplikacji znajduje sie w `config/app_config.json` i zawiera:

- `app_name`: `Manager`,
- `active_record_type_id`: `default`,
- sekcje `Dashboard`, `Records`, `Archive`.

`AppConfigService` umie wczytac JSON konfiguracji aplikacji i zamienic go na obiekty domenowe. `app_name` z tej konfiguracji jest juz uzywany jako tytul okna aplikacji. Pozostale elementy loadera nie sa jeszcze podlaczone do obecnych kart, bazy ani `OrderService`.

Obecna aplikacja nadal uzywa przejsciowego starego UI:

- tytul okna i teksty pozostaja bez zmian,
- zakladki UI pozostaja statyczne,
- nie dodano ekranu ustawien ani ikony zebatki,
- nie dodano migracji ani nowych tabel.

Nastepny bezpieczny krok:

- dodac walidacje konfiguracji aplikacji albo przygotowac osobny MVP dla subtelnego ekranu ustawien pod ikona zebatki, nadal bez zmiany schematu bazy.

## MVP-010 - Fundament sekcji/kart aplikacji

Dodano:

- `domain/app_section.py`,
- `config/default_sections.json`,
- `services/section_config_service.py`.

Wprowadzono generyczne pojecie:

- `AppSectionDefinition` - definicja sekcji/karty aplikacji z `id`, `name`, `type`, `visible`, `order` i opcjonalnym `record_type_id`.

Domyslna konfiguracja sekcji znajduje sie w `config/default_sections.json` i zawiera neutralne sekcje:

- `dashboard`,
- `records`,
- `archive`,
- `settings`.

`SectionConfigService` umie wczytac JSON z lista sekcji i zamienic go na obiekty domenowe. Loader jest uzywany posrednio przez `ConfigService` w ustawieniach i przy budowie szkieletu glownych zakladek. Nadal nie zmienia bazy ani `OrderService`.

Obecna aplikacja nadal uzywa przejsciowego starego UI:

- obecne zakladki Tkinter pozostaja statyczne,
- nie dodano dynamicznego menu ani przelaczania widokow,
- nie dodano ekranu ustawien ani ikony zebatki,
- nie dodano migracji ani nowych tabel.

Nastepny bezpieczny krok:

- dodac walidacje sekcji albo przygotowac osobny MVP dla ustawien/ikony zebatki, ktory zacznie uzywac konfiguracji sekcji bez zmiany schematu bazy.

## MVP-011 - Centralny serwis konfiguracji

Dodano:

- `services/config_service.py`.

Centralny serwis agreguje:

- konfiguracje aplikacji z `config/app_config.json`,
- definicje pol z `config/default_record_fields.json`,
- typ rekordu z `config/default_record_type.json`,
- sekcje z `config/default_sections.json`.

Istniejace szczegolowe serwisy pozostaja:

- `AppConfigService`,
- `FieldConfigService`,
- `RecordTypeConfigService`,
- `SectionConfigService`.

`ConfigService` jest cienka warstwa porzadkujaca dostep do konfiguracji. Jest uzywany przez szkielet ustawien oraz zapis nazwy aplikacji i sekcji, ale nie jest jeszcze pelnym systemem ustawien ani zapisem konfiguracji per uzytkownik.

Nastepny bezpieczny krok:

- dodac walidacje spojnosc konfiguracji albo w osobnym MVP zaczac uzywac `ConfigService` w przyszlym ekranie ustawien, bez zmiany obecnego UI i schematu bazy.

## MVP-012 - Fundament zapisu konfiguracji

Rozbudowano:

- `services/config_service.py`.

Dodano zapis JSON dla:

- `config/app_config.json`,
- `config/default_record_fields.json`,
- `config/default_record_type.json`,
- `config/default_sections.json`.

Dodane metody:

- `save_app_config()`,
- `save_field_definitions()`,
- `save_record_type()`,
- `save_sections()`,
- `save_all()`.

Zapis uzywa standardowej biblioteki Pythona, `ensure_ascii=False` i `indent=2`. Serwis serializuje obiekty domenowe do obecnych struktur JSON i jest uzywany przez obecny szkielet ustawien dla nazwy aplikacji oraz sekcji.

Ryzyka:

- Brak automatycznego backupu plikow konfiguracji przed zapisem.
- Brak zapisu konfiguracji per uzytkownik.
- Przyszly ekran ustawien musi uwzglednic walidacje i obsluge bledow zapisu.

Nastepny bezpieczny krok:

- dodac prosty backup konfiguracji przed zapisem albo walidacje spojnosc konfiguracji przed zapisaniem zmian z przyszlego UI ustawien.

## MVP-013 - Fundament walidacji konfiguracji

Dodano:

- `services/config_validation_service.py`.

Rozbudowano:

- `services/config_service.py` o jawna metode `validate_all()`.

Walidator sprawdza:

- `app_config`,
- definicje pol,
- typ rekordu,
- sekcje.

Zakres walidacji jest podstawowy:

- wymagane pola tekstowe nie sa puste,
- listy maja poprawny typ,
- wartosci logiczne i liczbowe maja poprawny typ,
- typ pola nalezy do `text`, `number`, `date`, `boolean`, `select`,
- identyfikatory sekcji i pol nie sa powielone w swoich listach.

Walidacja nie jest jeszcze podlaczona do UI, nie blokuje startu aplikacji i nie jest pelnym systemem ustawien.

Nastepny bezpieczny krok:

- uzyc walidatora w przyszlym ekranie ustawien przed zapisem albo rozszerzyc walidacje o spojnosc referencji miedzy typem rekordu, polami i sekcjami.

## MVP-014 - Diagnostyka konfiguracji z konsoli

Dodano:

- `tools/__init__.py`,
- `tools/check_config.py`.

Skrypt `tools/check_config.py` jest prostym narzedziem developerskim do sprawdzania konfiguracji bez uruchamiania nowego UI ustawien. Uruchamia sie go poleceniem:

```text
python tools/check_config.py
```

Skrypt laduje konfiguracje przez `ConfigService`, a nastepnie wywoluje `ConfigService.validate_all()`, ktory korzysta z `ConfigValidationService`. Gdy konfiguracja jest poprawna, wypisuje `Configuration check: OK`. Gdy wystapia problemy z ladowaniem albo walidacja zwroci bledy, wypisuje krotka liste komunikatow.

Nie zmieniono:

- UI Tkinter,
- sposobu startu aplikacji przez `python main.py`,
- schematu bazy danych,
- plikow JSON konfiguracji,
- zaleznosci projektu.

Przyszla ikona zebatki albo ekran ustawien powinny korzystac z tych samych uslug konfiguracji i walidacji, ale pozostaja osobnym MVP.

## MVP-015 - Tytul okna z konfiguracji aplikacji

Rozbudowano:

- `ui/app.py`.

Obecny `WorkshopApp` laduje `app_name` z `config/app_config.json` przez `ConfigService` i uzywa tej wartosci jako tytulu okna Tkinter. Jesli konfiguracja nie zaladuje sie poprawnie albo nazwa jest pusta, tytul okna wraca do bezpiecznego fallbacku `Manager`.

To pierwszy maly krok integracji konfiguracji z obecnym UI.

Nie zmieniono:

- ukladu UI,
- formularzy, tabel, zapisu, edycji, usuwania ani wyszukiwania,
- schematu bazy danych,
- plikow JSON konfiguracji,
- zaleznosci projektu.

Nie dodano ekranu ustawien, ikony zebatki, edytora nazwy aplikacji, edytora kart, edytora pol ani dynamicznego UI. Reszta aplikacji nadal dziala na starym przejsciowym UI.

## MVP-016 - Szkielet ustawien read-only

Rozbudowano:

- `ui/app.py`.

Dodano subtelny przycisk `Ustawienia` w gornym pasku obecnego UI. Klikniecie otwiera proste okno podgladu ustawien. Okno korzysta z `ConfigService` i pokazuje:

- nazwe aplikacji,
- aktywny typ rekordu,
- liczbe sekcji/kart,
- informacje, ze edycja ustawien zostanie dodana pozniej.

Jesli konfiguracja nie zaladuje sie poprawnie, okno pokazuje fallback zamiast crasha.

Nie zmieniono:

- zapisu ustawien z UI, bo go jeszcze nie ma,
- edycji nazwy aplikacji,
- edytora kart,
- edytora pol,
- dynamicznego przebudowywania UI,
- schematu bazy danych,
- obecnych funkcji formularzy, tabel, wyszukiwania i archiwum.

Obecna aplikacja nadal dziala na starym przejsciowym UI. Pelny edytor ustawien pozostaje osobnym MVP.

## MVP-017 - Edycja nazwy aplikacji w ustawieniach

Rozbudowano:

- `ui/app.py`.

Okno ustawien zawiera teraz pole tekstowe dla nazwy aplikacji. Pole pokazuje aktualne `app_name` z `config/app_config.json`. Przycisk `Zapisz`:

- odrzuca pusta nazwe,
- laduje pelna konfiguracje przez `ConfigService`,
- aktualizuje `app_name`,
- waliduje konfiguracje,
- zapisuje `config/app_config.json` przez `ConfigService.save_app_config()`,
- aktualizuje tytul obecnego okna po poprawnym zapisie.

To pierwszy edytowalny element ustawien.

Nie zmieniono:

- edycji kart,
- edycji pol,
- edycji typow rekordow,
- dynamicznego przebudowywania UI,
- schematu bazy danych,
- obecnych funkcji zapisu rekordow, edycji, usuwania, wyszukiwania i archiwum.

Edycja kart, pol i typow rekordow pozostaje osobnymi MVP.

## MVP-018 - Podglad sekcji/kart w ustawieniach

Rozbudowano:

- `ui/app.py`.

Okno ustawien pokazuje teraz read-only liste sekcji/kart ladowanych przez `ConfigService` z `config/default_sections.json`. Lista pokazuje:

- nazwe,
- id,
- typ,
- widocznosc,
- kolejnosc.

Jesli konfiguracja nie zaladuje sie poprawnie, okno pokazuje bezpieczny fallback zamiast crasha.

Nie zmieniono:

- edycji sekcji,
- dodawania sekcji,
- usuwania sekcji,
- dynamicznego przebudowywania glownego UI,
- edytora pol,
- edytora typow rekordow,
- schematu bazy danych.

Edycja nazwy aplikacji z MVP-017 zostala zachowana. Edytor sekcji pozostaje osobnym przyszlym MVP.

## MVP-019 - Podglad typu rekordu i pol w ustawieniach

Rozbudowano:

- `ui/app.py`.

Okno ustawien pokazuje teraz read-only podglad typu rekordu ladowanego przez `ConfigService` z `config/default_record_type.json`. Podglad pokazuje:

- id typu rekordu,
- nazwe typu rekordu,
- liste przypisanych pol.

Okno ustawien pokazuje tez read-only liste pol ladowanych przez `ConfigService` z `config/default_record_fields.json`. Lista pokazuje:

- id pola,
- etykiete,
- typ pola,
- czy pole jest wymagane,
- opcje dla pol wyboru.

Nie zmieniono:

- edycji typu rekordu,
- edycji pol,
- dodawania pol,
- usuwania pol,
- dynamicznego formularza,
- dynamicznej listy rekordow,
- schematu bazy danych,
- glownego UI.

Edycja nazwy aplikacji i podglad sekcji/kart zostaly zachowane. Edytor typu rekordu i pol pozostaje osobnymi przyszlymi MVP.

## MVP-020 - Uporzadkowanie okna ustawien

Rozbudowano:

- `ui/app.py`.

Istniejace okno ustawien zostalo uporzadkowane w czytelne sekcje:

- `Ogolne`,
- `Sekcje aplikacji`,
- `Typ rekordu`,
- `Pola`.

Zachowano:

- edycje nazwy aplikacji,
- podglad sekcji/kart,
- podglad typu rekordu,
- podglad pol.

Nie dodano:

- edycji sekcji,
- dodawania/usuwania sekcji,
- edycji pol,
- edycji typu rekordu,
- dynamicznego przebudowywania glownego UI,
- migracji bazy danych,
- nowych tabel.

Zmiana dotyczy tylko czytelnosci okna ustawien.

## MVP-021 - Edycja istniejacych sekcji/kart

Rozbudowano:

- `ui/app.py`.

W oknie ustawien mozna teraz edytowac istniejace sekcje/karty w ograniczonym zakresie:

- `name`,
- `visible`,
- `order`.

Pola `id` i `type` pozostaja tylko do odczytu. Przycisk `Zapisz sekcje`:

- odrzuca pusta nazwe sekcji,
- wymaga liczby calkowitej w polu kolejnosci,
- laduje pelna konfiguracje przez `ConfigService`,
- waliduje konfiguracje po zmianach,
- zapisuje `config/default_sections.json` przez `ConfigService.save_sections()`.

Nie dodano:

- dodawania sekcji,
- usuwania sekcji,
- edycji `id`,
- edycji `type`,
- dynamicznego przebudowywania glownego UI,
- edycji pol,
- edycji typow rekordow,
- migracji bazy danych,
- nowych tabel.

Glowny UI nadal dziala jak wczesniej i nie jest jeszcze budowany dynamicznie na podstawie konfiguracji sekcji.

## MVP-023 - Usuwanie niestandardowych sekcji/kart

Rozbudowano:

- `ui/app.py`.

W oknie ustawien mozna teraz usuwac sekcje niestandardowe. Sekcje bazowe sa chronione:

- `dashboard`,
- `records`,
- `archive`,
- `settings`.

Usuwanie wymaga potwierdzenia. Po potwierdzeniu aplikacja:

- laduje pelna konfiguracje przez `ConfigService`,
- usuwa wybrana sekcje z listy sekcji,
- waliduje konfiguracje,
- zapisuje `config/default_sections.json` przez `ConfigService.save_sections()`,
- odswieza okno ustawien.

Nie dodano:

- usuwania sekcji systemowych,
- dynamicznego przebudowywania glownego UI,
- edycji pol,
- edycji typow rekordow,
- migracji bazy danych,
- nowych tabel,
- presetow branzowych.

Pelny system zarzadzania kartami bedzie rozwijany dalej.

## MVP-024 - Sekcje z konfiguracji w glownym UI

Rozbudowano:

- `ui/app.py`.

Glowne zakladki aplikacji sa teraz tworzone na podstawie widocznych sekcji z konfiguracji. Zasady:

- sekcje sa ladowane przez `ConfigService`,
- pokazywane sa tylko sekcje z `visible = true`,
- kolejnosc pochodzi z pola `order`,
- sekcje typu `records` i `archive` korzystaja z obecnych widokow,
- pozostale sekcje pokazuja placeholder `Sekcja w przygotowaniu`,
- przy bledzie ladowania konfiguracji uzywany jest fallback z obecnymi widokami.

Nie dodano:

- pelnego systemu dynamicznych widokow,
- dynamicznych formularzy,
- dynamicznej listy rekordow,
- edycji pol,
- edycji typow rekordow,
- migracji bazy danych,
- nowych tabel,
- importu/eksportu,
- presetow branzowych.

Ustawienia nadal sa dostepne przez zebatke. Glowny UI zachowuje obecne funkcje rekordow i archiwum.

## MVP-025 - Neutralny branding naglowka

Rozbudowano:

- `ui/app.py`.

Usunieto warsztatowy branding z glownego naglowka aplikacji. Naglowek pokazuje teraz `app_name` z `config/app_config.json`, czyli ta sama nazwe, ktora jest uzywana jako tytul okna. Po zapisaniu nazwy aplikacji w ustawieniach aktualizowany jest tytul okna oraz tekst naglowka.

Opis pod naglowkiem jest neutralny:

```text
Lokalna aplikacja do zarzadzania rekordami
```

Opis jest jeszcze tymczasowo staly w kodzie. Nie dodano `app_description` do konfiguracji w tym MVP.

Nie zmieniono:

- pelnego rebrandingu wszystkich warsztatowych pol,
- migracji bazy danych,
- dynamicznych formularzy,
- edycji pol,
- edycji typow rekordow,
- nowych tabel,
- presetow branzowych,
- duzego redesignu UI.

Stare warsztatowe pola danych nadal istnieja jako etap przejsciowy.

Po MVP-027 opis pod naglowkiem zostal usuniety. Naglowek pokazuje tylko nazwe aplikacji z konfiguracji.

## MVP-026 - Zarzadzanie sekcjami i odswiezanie UI po zapisie ustawien

Rozbudowano:

- `ui/app.py`.

Okno ustawien pozwala teraz dodac nowa sekcje/karte przez prosty wiersz w sekcji `Sekcje aplikacji`. Nowa sekcja zapisuje `id`, `name`, `type`, `visible` i `order` do `config/default_sections.json` przez `ConfigService.save_sections()`.

Po zmianach sekcji aplikacja:

- waliduje konfiguracje przez `ConfigService.validate_all()`,
- zapisuje aktualna liste sekcji,
- odswieza okno ustawien przez ponowne wczytanie konfiguracji,
- przebudowuje glowne zakladki `Notebook` bez restartu aplikacji.

Sekcje bazowe nadal sa chronione przed usunieciem:

- `dashboard`,
- `records`,
- `archive`,
- `settings`.

Nie zmieniono:

- schematu bazy danych,
- tabel SQLite,
- edycji pol,
- edycji typow rekordow,
- dynamicznych formularzy,
- pelnego systemu widokow.

Sekcje bez pelnego widoku nadal pokazuja placeholder `Sekcja w przygotowaniu`. To nadal jest bezpieczny szkielet zarzadzania sekcjami, nie pelny konfigurator UI.

## MVP-027 - Czystszy naglowek i podstawowe typy sekcji

Rozbudowano:

- `ui/app.py`.

Glowny naglowek pokazuje teraz tylko nazwe aplikacji z `config/app_config.json`. Usunieto szary opis pod naglowkiem, a zapis nazwy aplikacji w ustawieniach nadal od razu aktualizuje tytul okna i tekst naglowka.

Podstawowe typy sekcji sa obslugiwane w glownym `Notebook`:

- `records` uzywa obecnego widoku rekordow,
- `archive` uzywa obecnego widoku archiwum,
- globalny pasek statystyk jest ukryty,
- `dashboard` pokazuje neutralny placeholder bez statystyk,
- `settings` pokazuje prosty widok z przyciskiem otwierajacym okno ustawien,
- `custom` pokazuje placeholder `Sekcja wlasna w przygotowaniu`.

Nie zmieniono:

- schematu SQLite,
- zapisu, edycji ani usuwania rekordow,
- edytora pol,
- edytora typow rekordow,
- nowych tabel,
- duzego redesignu UI.

To nadal jest szkielet sekcji. Pelne dynamiczne widoki i konfigurator widokow pozostaja osobnymi przyszlymi MVP.

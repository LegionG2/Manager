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
|   `-- default_record_type.json
|-- data/
|   |-- __init__.py
|   `-- database.py
|-- domain/
|   |-- __init__.py
|   |-- app_config.py
|   |-- field_definition.py
|   |-- record_type.py
|   `-- record.py
|-- services/
|   |-- __init__.py
|   |-- app_config_service.py
|   |-- field_config_service.py
|   |-- order_service.py
|   `-- record_type_config_service.py
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

- Plik nie jest jeszcze podlaczony do UI ani bazy danych.
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
- Nie zmienia obecnego tytulu okna, kart ani sekcji.
- Nie istnieje jeszcze zapis konfiguracji uzytkownika.

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
- UI nadal zna konkretne kolumny aktualnego modelu danych przy budowaniu tabel i wypelnianiu formularza.
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

- `APP_TITLE`, `DB_NAME` i katalog danych zawieraja nazwy zwiazane ze stara aplikacja warsztatowa.
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
- `stats()` liczy podsumowania dla panelu statystyk.
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

`AppConfigService` umie wczytac JSON konfiguracji aplikacji i zamienic go na obiekty domenowe. Loader nie jest jeszcze podlaczony do UI, obecnych kart, tytulu okna, bazy ani `OrderService`.

Obecna aplikacja nadal uzywa przejsciowego starego UI:

- tytul okna i teksty pozostaja bez zmian,
- zakladki UI pozostaja statyczne,
- nie dodano ekranu ustawien ani ikony zebatki,
- nie dodano migracji ani nowych tabel.

Nastepny bezpieczny krok:

- dodac walidacje konfiguracji aplikacji albo przygotowac osobny MVP dla subtelnego ekranu ustawien pod ikona zebatki, nadal bez zmiany schematu bazy.

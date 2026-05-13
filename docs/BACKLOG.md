# Backlog - Manager

## MVP

### MVP-001 - Dokumentacja i mapa kodu

Status: wykonane

Cel:

- dodac podstawowa dokumentacje projektu,
- opisac wizje produktu,
- opisac obecna strukture techniczna,
- przygotowac mape kodu bez zmiany dzialania aplikacji.

### MVP-002 - Przeglad struktury repozytorium i kodu

Status: wykonane

Cel:

- dokladniej przejrzec `main.py`,
- opisac odpowiedzialnosci klas i metod,
- wskazac obszary do przyszlego wydzielenia.

Zakres:

- dokumentacja-only,
- bez zmiany dzialania aplikacji,
- bez zmiany UI,
- bez zmiany schematu bazy danych.

### MVP-003 - Extract database/data access helpers

Status: wykonane

Cel:

- stopniowo wydzielic obsluge SQLite,
- zachowac obecny schemat i zachowanie,
- przygotowac miejsce pod przyszly model generycznych rekordow.

Kandydaci prac:

- przeniesc dostep do SQLite do osobnego modulu lub helperow,
- zachowac nazwy tabel i kolumn bez zmian,
- nie zmieniac migracji ani danych,
- dodac reczne scenariusze testowe dla zapisu, edycji, usuwania, archiwum i eksportu.

Wynik MVP-003:

- dodano `data/database.py`,
- dodano `data/__init__.py`,
- przeniesiono klase `Database` z `main.py`,
- zachowano dotychczasowy schemat `orders`,
- zachowano dotychczasowe metody uzywane przez UI.

Pozostale ryzyka:

- `main.py` nadal zawiera UI, stan formularzy, mapowanie danych i backup,
- `main.py` nadal korzysta z `self.db.conn` przy backupie,
- model danych nadal jest oparty o `orders`.

### MVP-004 - Extract UI layer

Status: wykonane

Cel:

- stopniowo wydzielic budowanie interfejsu Tkinter,
- ograniczyc rozrost `main.py`,
- zachowac obecny wyglad i zachowanie UI.

Wynik MVP-004:

- dodano `ui/app.py`,
- dodano `ui/__init__.py`,
- przeniesiono `WorkshopApp`, `SettingsManager`, stale UI i helpery sciezek z `main.py` do `ui/app.py`,
- zostawiono w `main.py` prosty punkt startowy aplikacji,
- pozostawiono te same etykiety, rozmiary, akcje i zachowanie przyciskow,
- nie zmieniono ukladu, schematu bazy ani zaleznosci.

Pozostale ryzyka:

- `ui/app.py` nadal laczy layout, stan formularza, walidacje, sortowanie, filtrowanie i akcje uzytkownika,
- `WorkshopApp` nadal korzysta bezposrednio z `Database`,
- backup nadal siega do `self.db.conn`,
- obecny UI nadal zna branzowe pola i statusy starego modelu.

Nastepny bezpieczny krok:

- wydzielic konfiguracje/sciezki albo backup do osobnego malego modulu bez zmiany zachowania.

### MVP-005 - Extract application/record service

Status: wykonane

Cel:

- zmniejszyc odpowiedzialnosc `ui/app.py`,
- wydzielic najbezpieczniejsza logike rekordow/zlecen,
- zachowac obecny wyglad, zachowanie i schemat bazy.

Wynik MVP-005:

- dodano `services/order_service.py`,
- dodano `services/__init__.py`,
- przeniesiono parsowanie kwot, liczenie salda, stan terminu, wyszukiwanie, sortowanie i przygotowanie danych formularza do `OrderService`,
- przeniesiono proste operacje na rekordzie: zapis, usuniecie, zmiane statusu, archiwizacje i przywrocenie,
- zostawiono UI, messageboxy, filedialogi, odczyt widgetow i wypelnianie tabel w `ui/app.py`,
- nie zmieniono UI, schematu bazy ani zaleznosci.

Pozostale ryzyka:

- `OrderService` nadal zna warsztatowe pola i tabele `orders`,
- nazwa `order_service.py` jest przejsciowa do czasu generycznego modelu rekordow,
- `WorkshopApp` nadal zna kolumny danych przy budowaniu tabel i formularzy,
- backup nadal jest w UI i uzywa `self.db.conn`.

Nastepny bezpieczny krok:

- wydzielic backup albo konfiguracje/sciezki danych bez zmiany zachowania, ewentualnie dodac testy jednostkowe dla `OrderService`.

### MVP-006 - Introduce generic record type model

Status: wykonane

Cel:

- zaprojektowac neutralny model typow rekordow,
- unikac zalozen branzowych,
- przygotowac fundament pod przyszla migracje z obecnego modelu.

Wynik MVP-006:

- dodano `domain/record.py`,
- dodano `domain/__init__.py`,
- wprowadzono neutralne dataclassy `Record`, `RecordField`, `RecordType` i `RecordStatus`,
- nie podpieto jeszcze modelu do UI, `OrderService` ani bazy danych,
- nie zmieniono schematu SQLite, UI ani zachowania aplikacji.

Pozostale ryzyka:

- obecny model `orders` nadal jest aktywnym modelem zapisu danych,
- przyszla migracja musi zachowac lokalne dane uzytkownika,
- trzeba zaprojektowac mapowanie warsztatowych kolumn na generyczne pola,
- typy rekordow i pola nie sa jeszcze konfigurowalne.

Nastepny bezpieczny krok:

- opisac konfiguracje pol i typow rekordow albo dodac adapter tylko do odczytu mapujacy obecne `orders` na `Record`, bez zmiany schematu.

### MVP-007 - Introduce configurable fields model

Status: wykonane

Cel:

- zaprojektowac konfiguracje pol,
- uwzglednic podstawowe typy danych,
- zachowac mozliwosc wyswietlania i edycji danych lokalnie.

Wynik MVP-007:

- dodano `domain/field_definition.py`,
- dodano `config/default_record_fields.json`,
- dodano `services/field_config_service.py`,
- wprowadzono `FieldDefinition`, `FieldType` i `FieldOption`,
- obslugiwane typy pol to `text`, `number`, `date`, `boolean` i `select`,
- domyslna konfiguracja uzywa neutralnych pol `title`, `description`, `status` i `created_date`,
- loader potrafi wczytac JSON i zmapowac go na obiekty domenowe,
- konfiguracja nie jest jeszcze podlaczona do UI ani bazy.

Pozostale ryzyka:

- obecny statyczny formularz nadal dziala na modelu `orders`,
- nie ma jeszcze edytora pol ani zapisu konfiguracji uzytkownika,
- przyszle podpiecie musi zachowac obecne dane i UI,
- trzeba dopracowac walidacje definicji pol przed uzyciem w runtime.

Nastepny bezpieczny krok:

- dodac walidacje konfiguracji albo adapter tylko do odczytu laczacy definicje pol z `RecordType`, bez zmiany schematu bazy i UI.

### MVP-008 - Introduce configurable record types model

Status: wykonane

Cel:

- zaprojektowac konfiguracje typow rekordow,
- powiazac typ rekordu z lista pol,
- zachowac obecne UI, zachowanie i schemat bazy.

Wynik MVP-008:

- dodano `domain/record_type.py`,
- dodano `config/default_record_type.json`,
- dodano `services/record_type_config_service.py`,
- wprowadzono `RecordTypeDefinition`,
- domyslna konfiguracja typu jest neutralna: `default`, `Default record`, pola `title`, `description`, `status`, `created_date`,
- loader potrafi wczytac JSON i zmapowac go na obiekt domenowy,
- konfiguracja typu rekordu nie jest jeszcze podlaczona do UI ani bazy.

Pozostale ryzyka:

- obecny statyczny formularz nadal dziala na modelu `orders`,
- nie ma jeszcze edytora typow rekordow ani zapisu konfiguracji uzytkownika,
- referencje pol w typie rekordu nie sa jeszcze walidowane wzgledem `FieldDefinition`,
- przyszle podpiecie musi zachowac obecne dane i UI.

Nastepny bezpieczny krok:

- dodac walidacje zgodnosci typu rekordu z definicjami pol albo adapter tylko do odczytu laczacy `RecordTypeDefinition` i `FieldDefinition`, bez zmiany schematu bazy i UI.

### MVP-009 - Application configuration foundation

Status: wykonane

Cel:

- przygotowac neutralna konfiguracje aplikacji,
- opisac przyszle sekcje/karty aplikacji,
- zachowac obecne UI, zachowanie i schemat bazy.

Wynik MVP-009:

- dodano `domain/app_config.py`,
- dodano `config/app_config.json`,
- dodano `services/app_config_service.py`,
- wprowadzono `AppConfig` i `AppSection`,
- domyslna konfiguracja jest neutralna: `Manager`, `default`, sekcje `Dashboard`, `Records`, `Archive`,
- loader potrafi wczytac JSON i zmapowac go na obiekty domenowe,
- konfiguracja aplikacji nie jest jeszcze podlaczona do UI ani bazy.

Pozostale ryzyka:

- obecny UI nadal uzywa statycznych tekstow, kart i starego tytulu,
- nie ma jeszcze ekranu ustawien ani ikony zebatki,
- nie ma jeszcze zapisu konfiguracji uzytkownika,
- przyszle podpiecie musi zachowac obecne dane i UI.

Nastepny bezpieczny krok:

- dodac walidacje konfiguracji aplikacji albo zaplanowac osobny MVP dla subtelnego ekranu ustawien pod ikona zebatki.

### MVP-010 - Application sections/tabs foundation

Status: wykonane

Cel:

- przygotowac neutralny model sekcji/kart aplikacji,
- opisac przyszle dynamiczne sekcje,
- zachowac obecne UI, zachowanie i schemat bazy.

Wynik MVP-010:

- dodano `domain/app_section.py`,
- dodano `config/default_sections.json`,
- dodano `services/section_config_service.py`,
- wprowadzono `AppSectionDefinition`,
- domyslna konfiguracja sekcji jest neutralna: `dashboard`, `records`, `archive`, `settings`,
- loader potrafi wczytac JSON i zmapowac go na obiekty domenowe,
- konfiguracja sekcji nie jest jeszcze podlaczona do UI ani bazy.

Pozostale ryzyka:

- obecne zakladki Tkinter nadal sa statyczne,
- nie ma jeszcze edytora kart, dynamicznego menu, ekranu ustawien ani ikony zebatki,
- nie ma jeszcze zapisu konfiguracji uzytkownika,
- przyszle podpiecie musi zachowac obecne dane i UI.

Nastepny bezpieczny krok:

- dodac walidacje konfiguracji sekcji albo zaplanowac osobny MVP dla ustawien/ikony zebatki.

### MVP-011 - Central configuration service

Status: wykonane

Cel:

- uporzadkowac dostep do konfiguracji,
- dodac jeden centralny serwis agregujacy istniejace loadery,
- zachowac obecne UI, zachowanie i schemat bazy.

Wynik MVP-011:

- dodano `services/config_service.py`,
- wprowadzono `ConfigService`,
- wprowadzono `ManagerConfig`,
- centralny serwis korzysta z `AppConfigService`, `FieldConfigService`, `RecordTypeConfigService` i `SectionConfigService`,
- udostepniono `load_app_config()`, `load_field_definitions()`, `load_record_type()`, `load_sections()` i `load_all()`,
- nie usunieto szczegolowych loaderow,
- centralny serwis nie jest jeszcze podlaczony do UI.

Pozostale ryzyka:

- nie ma jeszcze zapisu konfiguracji uzytkownika,
- nie ma jeszcze ekranu ustawien ani ikony zebatki,
- konfiguracje nie sa jeszcze walidowane jako spojny zestaw,
- przyszle podpiecie musi zachowac obecne dane i UI.

Nastepny bezpieczny krok:

- dodac walidacje spojnosc konfiguracji albo zaplanowac osobny MVP dla ustawien korzystajacych z `ConfigService`.

### MVP-012 - Configuration writing foundation

Status: wykonane

Cel:

- dodac fundament zapisu konfiguracji do JSON,
- zachowac obecne UI, zachowanie i schemat bazy,
- przygotowac przyszly ekran ustawien do zapisywania zmian.

Wynik MVP-012:

- rozbudowano `services/config_service.py`,
- dodano `save_app_config()`,
- dodano `save_field_definitions()`,
- dodano `save_record_type()`,
- dodano `save_sections()`,
- dodano `save_all()`,
- zapis obejmuje `app_config.json`, `default_record_fields.json`, `default_record_type.json` i `default_sections.json`,
- zapis uzywa standardowej biblioteki Pythona oraz `indent=2`,
- zapis nie jest jeszcze podlaczony do UI.

Pozostale ryzyka:

- nie ma jeszcze automatycznego backupu konfiguracji przed zapisem,
- nie ma jeszcze zapisu konfiguracji per uzytkownik,
- nie ma jeszcze ekranu ustawien ani ikony zebatki,
- przyszle UI ustawien musi walidowac dane przed zapisem.

Nastepny bezpieczny krok:

- dodac backup konfiguracji przed zapisem albo walidacje spojnosc konfiguracji przed uzyciem zapisu w UI.

### MVP-013 - Configuration validation foundation

Status: wykonane

Cel:

- dodac podstawowa walidacje konfiguracji,
- przygotowac przyszly ekran ustawien do sprawdzania danych przed zapisem,
- zachowac obecne UI, zachowanie i schemat bazy.

Wynik MVP-013:

- dodano `services/config_validation_service.py`,
- wprowadzono `ConfigValidationService`,
- wprowadzono `ConfigValidationResult`,
- rozbudowano `ConfigService` o `validate_all()`,
- walidator sprawdza konfiguracje aplikacji, definicje pol, typ rekordu i sekcje,
- walidator zwraca liste komunikatow bledow,
- walidacja nie jest jeszcze podlaczona do UI.

Pozostale ryzyka:

- walidacja nie obejmuje jeszcze wszystkich relacji miedzy plikami,
- walidacja nie zatrzymuje startu aplikacji,
- nie ma jeszcze ekranu ustawien ani ikony zebatki,
- przyszle UI ustawien musi wywolywac walidacje przed zapisem.

Nastepny bezpieczny krok:

- rozszerzyc walidacje o spojnosc referencji albo uzyc jej w przyszlym ekranie ustawien przed zapisem konfiguracji.

### MVP-014 - Diagnostyka konfiguracji z konsoli

Status: wykonane

Cel:

- dodac prosty developerski check konfiguracji,
- sprawdzac ladowanie i walidacje konfiguracji z poziomu konsoli,
- zachowac obecne UI, zachowanie aplikacji i schemat bazy.

Wynik MVP-014:

- dodano `tools/check_config.py`,
- dodano `tools/__init__.py`,
- skrypt uruchamia sie przez `python tools/check_config.py`,
- skrypt laduje konfiguracje przez `ConfigService`,
- skrypt uruchamia walidacje przez `ConfigService.validate_all()` i `ConfigValidationService`,
- poprawna konfiguracja wypisuje `Configuration check: OK`,
- bledy ladowania albo walidacji sa wypisywane jako prosta lista komunikatow,
- narzedzie nie jest podlaczone do Tkinter ani obecnego UI.

Pozostale ryzyka:

- walidacja nadal nie obejmuje wszystkich relacji miedzy plikami,
- nie ma jeszcze ekranu ustawien ani ikony zebatki,
- przyszly ekran ustawien powinien korzystac z tych samych uslug konfiguracji i walidacji.

Nastepny bezpieczny krok:

- rozszerzyc walidacje o spojnosc referencji albo uzyc tych samych uslug w osobnym MVP ekranu ustawien.

### MVP-015 - Tytul okna z konfiguracji aplikacji

Status: wykonane

Cel:

- podlaczyc `app_name` z konfiguracji do obecnego UI w minimalny sposob,
- ustawic tytul okna na podstawie `config/app_config.json`,
- zachowac obecne UI, zachowanie aplikacji i schemat bazy.

Wynik MVP-015:

- `WorkshopApp` ustawia tytul okna na podstawie `ConfigService().load_app_config().app_name`,
- dodano bezpieczny fallback `Manager`, gdy konfiguracja nie zaladuje sie poprawnie albo nazwa jest pusta,
- jest to pierwszy maly krok integracji konfiguracji z UI,
- nie dodano ekranu ustawien, ikony zebatki ani edytora nazwy aplikacji,
- reszta aplikacji nadal dziala na starym przejsciowym UI.

Pozostale ryzyka:

- konfiguracja aplikacji nadal nie steruje kartami, formularzami ani widokami,
- pelny ekran ustawien i ikona zebatki pozostaja osobnym MVP,
- obecny model danych i UI nadal zawieraja przejsciowe nazwy oraz zalozenia starej aplikacji.

Nastepny bezpieczny krok:

- przygotowac osobny MVP dla ustawien albo kontynuowac male integracje konfiguracji bez zmiany schematu bazy.

### MVP-016 - Szkielet ustawien read-only

Status: wykonane

Cel:

- dodac pierwszy subtelny widoczny zalazek przyszlych ustawien,
- pokazac podstawowe informacje z konfiguracji bez edycji,
- zachowac obecne UI, funkcje aplikacji i schemat bazy.

Wynik MVP-016:

- dodano subtelny przycisk `Ustawienia` w gornym pasku obecnego UI,
- klikniecie otwiera proste okno podgladu ustawien,
- okno pokazuje nazwe aplikacji, aktywny typ rekordu i liczbe sekcji/kart,
- podglad korzysta z `ConfigService`,
- przy bledzie ladowania konfiguracji pokazywany jest fallback zamiast crasha,
- okno jest tylko read-only i nie zapisuje zmian.

Pozostale ryzyka:

- pelny edytor nazwy aplikacji, kart, typow rekordow i pol pozostaje osobnym MVP,
- obecna aplikacja nadal dziala na starym przejsciowym UI,
- konfiguracja nadal nie przebudowuje dynamicznie glownego interfejsu.

Nastepny bezpieczny krok:

- zaprojektowac osobny MVP dla edycji jednego ustawienia albo rozszerzyc read-only diagnostyke ustawien, nadal bez migracji bazy.

### MVP-017 - Edycja nazwy aplikacji w ustawieniach

Status: wykonane

Cel:

- dodac pierwszy edytowalny element ustawien,
- pozwolic zmienic nazwe aplikacji z okna ustawien,
- zapisywac zmiane przez istniejacy mechanizm konfiguracji.

Wynik MVP-017:

- okno ustawien zawiera pole tekstowe `Nazwa aplikacji`,
- przycisk `Zapisz` zapisuje `app_name` do `config/app_config.json`,
- zapis korzysta z `ConfigService.save_app_config()`,
- przed zapisem wykonywana jest walidacja konfiguracji,
- pusta nazwa pokazuje blad i nie zapisuje sie,
- po poprawnym zapisie tytul obecnego okna jest aktualizowany.

Pozostale ryzyka:

- edycja kart, pol i typow rekordow pozostaje osobnymi MVP,
- UI nadal nie przebudowuje sie dynamicznie na podstawie konfiguracji,
- obecna aplikacja nadal dziala na starym przejsciowym UI.

Nastepny bezpieczny krok:

- dodac osobny, maly MVP dla edycji sekcji albo rozszerzyc walidacje relacji miedzy plikami konfiguracji.

### MVP-018 - Podglad sekcji/kart w ustawieniach

Status: wykonane

Cel:

- pokazac skonfigurowane sekcje/karty w oknie ustawien,
- zachowac sekcje jako read-only,
- nie zmieniac glownego UI ani schematu bazy.

Wynik MVP-018:

- okno ustawien pokazuje sekcje z `config/default_sections.json`,
- podglad korzysta z centralnego `ConfigService`,
- lista pokazuje nazwe, id, typ, widocznosc i kolejnosc,
- przy problemie z ladowaniem konfiguracji pokazywany jest bezpieczny fallback,
- edycja nazwy aplikacji z MVP-017 zostala zachowana.

Pozostale ryzyka:

- sekcji nie da sie jeszcze edytowac, dodawac ani usuwac,
- glowny UI nie jest jeszcze przebudowywany dynamicznie na podstawie sekcji,
- edytor sekcji, pol i typow rekordow pozostaje osobnymi MVP.

Nastepny bezpieczny krok:

- zaprojektowac osobny MVP dla edytora sekcji albo rozszerzyc walidacje konfiguracji sekcji.

### MVP-019 - Podglad typu rekordu i pol w ustawieniach

Status: wykonane

Cel:

- pokazac skonfigurowany typ rekordu w oknie ustawien,
- pokazac skonfigurowane pola rekordu w oknie ustawien,
- zachowac podglad jako read-only.

Wynik MVP-019:

- okno ustawien pokazuje typ rekordu z `config/default_record_type.json`,
- podglad typu pokazuje id, nazwe i przypisane pola,
- okno ustawien pokazuje pola z `config/default_record_fields.json`,
- lista pol pokazuje id, etykiete, typ, wymagalnosc i opcje dla pol wyboru,
- podglad korzysta z centralnego `ConfigService`,
- edycja nazwy aplikacji i podglad sekcji/kart zostaly zachowane.

Pozostale ryzyka:

- typu rekordu ani pol nie da sie jeszcze edytowac,
- nie ma jeszcze dodawania ani usuwania pol,
- glowny formularz i lista rekordow nie sa jeszcze dynamiczne.

Nastepny bezpieczny krok:

- zaprojektowac osobny MVP dla edycji pol albo rozszerzyc walidacje relacji typu rekordu z polami.

### MVP-020 - Uporzadkowanie okna ustawien

Status: wykonane

Cel:

- uporzadkowac istniejace okno ustawien,
- oddzielic obecne informacje w czytelne sekcje,
- nie dodawac nowych funkcji.

Wynik MVP-020:

- okno ustawien ma sekcje `Ogolne`, `Sekcje aplikacji`, `Typ rekordu` i `Pola`,
- zachowano edycje nazwy aplikacji,
- zachowano podglad sekcji/kart,
- zachowano podglad typu rekordu i pol,
- nie dodano edycji sekcji, pol ani typow rekordow.

Pozostale ryzyka:

- okno ustawien nadal jest technicznym szkieletem,
- edytory sekcji, pol i typow rekordow pozostaja osobnymi MVP,
- glowny UI nadal nie jest dynamicznie budowany z konfiguracji.

Nastepny bezpieczny krok:

- przed dodaniem edytorow dopracowac walidacje relacji konfiguracji albo dodac pojedynczy edytowalny element w osobnym MVP.

### MVP-021 - Edycja istniejacych sekcji/kart

Status: wykonane

Cel:

- dodac prosta edycje istniejacych sekcji/kart w ustawieniach,
- pozwolic zmieniac tylko `name`, `visible` i `order`,
- nie dodawac ani nie usuwac sekcji.

Wynik MVP-021:

- sekcja `Sekcje aplikacji` w oknie ustawien pokazuje edytowalne pola nazwy, widocznosci i kolejnosci,
- `id` i `type` pozostaja tylko do odczytu,
- przycisk `Zapisz sekcje` zapisuje zmiany do `config/default_sections.json`,
- zapis korzysta z `ConfigService.save_sections()`,
- przed zapisem uruchamiana jest walidacja konfiguracji,
- dodawanie i usuwanie sekcji nie jest dostepne,
- glowny UI nie jest dynamicznie przebudowywany na podstawie sekcji.

Pozostale ryzyka:

- zmiany sekcji sa widoczne w konfiguracji i ustawieniach, ale nie steruja jeszcze glownym UI,
- edytor dodawania/usuwania sekcji pozostaje osobnym MVP,
- edycja pol i typow rekordow pozostaje osobnymi MVP.

Nastepny bezpieczny krok:

- zaplanowac osobny MVP dla dynamicznego uzycia sekcji albo dla dodawania/usuwania sekcji.

### MVP-022 - Fundament wyszukiwania i filtrowania

Status: planowane

Cel:

- przygotowac wyszukiwanie niezalezne od jednej branzy,
- zaprojektowac filtry dla konfigurowalnych pol i statusow.

### MVP-023 - Fundament archiwum

Status: planowane

Cel:

- utrzymac mozliwosc archiwizacji rekordow,
- oddzielic pojecie archiwum od obecnego modelu zlecen.

### MVP-024 - Fundament importu i eksportu

Status: planowane

Cel:

- zaprojektowac import i eksport dla generycznych rekordow,
- utrzymac prosty eksport lokalny,
- unikac zaleznosci od chmury i zewnetrznego backendu.

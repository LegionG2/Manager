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

### MVP-010 - Fundament wyszukiwania i filtrowania

Status: planowane

Cel:

- przygotowac wyszukiwanie niezalezne od jednej branzy,
- zaprojektowac filtry dla konfigurowalnych pol i statusow.

### MVP-011 - Fundament archiwum

Status: planowane

Cel:

- utrzymac mozliwosc archiwizacji rekordow,
- oddzielic pojecie archiwum od obecnego modelu zlecen.

### MVP-012 - Fundament importu i eksportu

Status: planowane

Cel:

- zaprojektowac import i eksport dla generycznych rekordow,
- utrzymac prosty eksport lokalny,
- unikac zaleznosci od chmury i zewnetrznego backendu.

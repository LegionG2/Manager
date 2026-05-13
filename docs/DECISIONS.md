# Decisions - Manager

## Format

Kazda decyzja powinna zawierac:

- date,
- decyzje,
- kontekst,
- konsekwencje.

## 2026-05-11 - Manager pozostaje generyczny

Decyzja:

Manager musi pozostac aplikacja generyczna, a nie branzowa.

Kontekst:

Obecny kod i nazwy nadal zawieraja slady starszej aplikacji warsztatowej. Dalszy rozwoj ma isc w strone uniwersalnego systemu rekordow.

Konsekwencje:

- Nowe funkcje nie powinny hardcodowac jednej branzy.
- Dokumentacja powinna opisywac rekordy, pola, statusy i widoki w sposob neutralny.
- Stare nazwy nalezy traktowac jako stan przejsciowy.

## 2026-05-11 - Aplikacja pozostaje local-first

Decyzja:

Manager pozostaje aplikacja local-first.

Kontekst:

Projekt ma dzialac lokalnie na komputerze uzytkownika.

Konsekwencje:

- Brak chmury na start.
- Brak zewnetrznego backendu na ten moment.
- Dane powinny pozostac pod kontrola uzytkownika.

## 2026-05-11 - SQLite jest lokalna baza danych

Decyzja:

SQLite pozostaje lokalna baza danych.

Kontekst:

Obecna aplikacja juz zapisuje dane w SQLite i nie ma potrzeby zmiany technologii w pierwszym etapie.

Konsekwencje:

- Nie zmieniamy schematu bez osobnego zadania.
- Migracje musza byc planowane ostroznie.
- Backup danych pozostaje wazna funkcja.

## 2026-05-11 - Tkinter pozostaje frameworkiem UI

Decyzja:

Tkinter pozostaje frameworkiem UI na ten moment.

Kontekst:

Obecna aplikacja jest aplikacja desktopowa Python/Tkinter.

Konsekwencje:

- Nie dodajemy nowego frameworka UI bez osobnej decyzji.
- Prace nad UI powinny zachowac obecne dzialanie aplikacji.

## 2026-05-11 - Zmiany maja byc male i odwracalne

Decyzja:

Zmiany maja byc male, kontrolowane i mozliwie latwe do cofniecia.

Kontekst:

Projekt ma przejsc ze starego modelu na generyczny Manager bez ryzyka utraty dzialajacych funkcji.

Konsekwencje:

- Unikamy duzych zmian naraz.
- Kazdy krok powinien miec jasny zakres.
- Dokumentacja i testy reczne sa czescia pracy.

## 2026-05-11 - Nie robimy duzego refaktoru przed udokumentowaniem kodu

Decyzja:

Nie robimy duzego refaktoru przed udokumentowaniem obecnego kodu.

Kontekst:

`main.py` zawiera wiele odpowiedzialnosci. Przed rozbijaniem pliku trzeba opisac obecna strukture i ryzyka.

Konsekwencje:

- Najpierw dokumentacja i mapa kodu.
- Potem przeglad struktury.
- Dopiero pozniej stopniowe wydzielanie modulow.

## 2026-05-11 - Najpierw stopniowe oddzielenie odpowiedzialnosci

Decyzja:

Przed zmiana funkcjonalnosci projekt najpierw bedzie stopniowo oddzielal odpowiedzialnosci.

Kontekst:

Obecny `main.py` laczy punkt wejscia aplikacji, UI Tkinter, dostep do SQLite, konfiguracje, walidacje formularza, wyszukiwanie, sortowanie, archiwum, backup i eksport. To zwieksza ryzyko przypadkowej zmiany zachowania podczas refaktoru.

Konsekwencje:

- Najpierw wydzielamy warstwe danych/bazy danych bez zmiany schematu.
- Potem wydzielamy warstwe UI bez zmiany wygladu i zachowania.
- Model biznesowy/domenowy oddzielamy od konkretnych nazw warsztatowych stopniowo.
- Warstwe konfiguracji projektujemy osobno, zanim dodamy konfigurowalne typy rekordow i pola.
- Kazdy etap musi byc maly, odwracalny i mozliwy do sprawdzenia recznie.

## 2026-05-11 - Warstwa danych zaczyna sie w `data/database.py`

Decyzja:

Kod SQLite i klasa `Database` zostaly przeniesione z `main.py` do `data/database.py`.

Kontekst:

MVP-003 ma byc malym refaktorem bez zmiany dzialania aplikacji. Celem bylo oddzielenie najbardziej oczywistej warstwy danych bez zmiany schematu bazy, UI ani publicznych metod uzywanych przez `WorkshopApp`.

Konsekwencje:

- `main.py` importuje `Database` z `data.database`.
- Tabela `orders`, migracje i zapytania SQL pozostaja bez zmiany funkcjonalnej.
- UI nadal jest powiazane z obecnym modelem danych, ale kod SQLite ma juz osobny modul.
- Backup nadal wymaga dalszego uporzadkowania, bo `main.py` uzywa `self.db.conn`.
- Nastepne kroki powinny byc rownie male: metoda backupu w warstwie danych, potem konfiguracja/sciezki, potem UI.

## 2026-05-12 - Warstwa UI zaczyna sie w `ui/app.py`

Decyzja:

Kod Tkinter UI zostal przeniesiony z `main.py` do `ui/app.py`, a `main.py` pozostaje prostym punktem startowym.

Kontekst:

MVP-004 mial oddzielic warstwe UI bez zmiany wygladu i zachowania aplikacji. Obecny `WorkshopApp` jest nadal mocno powiazany z aktualnym modelem danych, wiec bezpiecznym krokiem bylo przeniesienie calej glownej klasy UI i powiazanych helperow do osobnego modulu bez rozbijania metod.

Konsekwencje:

- `main.py` importuje `WorkshopApp` i uruchamia `mainloop()`.
- `ui/app.py` zawiera `WorkshopApp`, `SettingsManager`, stale UI i helpery sciezek.
- Nie zmieniono tekstow UI, schematu bazy, zaleznosci ani zachowania formularzy.
- UI nadal wywoluje `Database` bezposrednio i zna obecne kolumny `orders`.
- Backup nadal wymaga dalszego uporzadkowania, bo `WorkshopApp` uzywa `self.db.conn`.
- Nastepny bezpieczny krok to wydzielenie konfiguracji/sciezek albo backupu bez zmiany zachowania.

## 2026-05-12 - Logika rekordow zaczyna sie w `services/order_service.py`

Decyzja:

Najbezpieczniejsza logika aplikacyjna zwiazana z obecnymi rekordami/zleceniami zostala wydzielona z `ui/app.py` do `services/order_service.py`.

Kontekst:

MVP-005 mial zmniejszyc odpowiedzialnosc UI bez zmiany wygladu, zachowania aplikacji i schematu bazy. Obecny model nadal uzywa tabeli `orders` oraz warsztatowych pol, wiec wybrano przejsciowa nazwe `OrderService` zamiast udawac, ze istnieje juz generyczny model rekordow.

Konsekwencje:

- `ui/app.py` tworzy `OrderService` i deleguje do niego logike parsowania kwot, liczenia salda, sortowania, wyszukiwania, walidacji danych formularza i prostych operacji na rekordzie.
- `ui/app.py` nadal odpowiada za Tkinter, widgety, tabele, formularze, messageboxy i filedialogi.
- `services/order_service.py` nadal zna obecne pola zlecen, statusy i tabele `orders`.
- Nie zmieniono UI, tekstow, schematu bazy danych, zaleznosci ani widocznego zachowania aplikacji.
- Nazwy warsztatowe pozostaja etapem przejsciowym do czasu osobnej decyzji o generycznym modelu rekordow.
- Nastepny bezpieczny krok to wydzielenie backupu lub konfiguracji/sciezek danych albo dodanie testow dla `OrderService`.

## 2026-05-12 - Generyczny model rekordu zaczyna sie w `domain/record.py`

Decyzja:

Dodano neutralny modul domenowy `domain/record.py` z podstawowymi strukturami `Record`, `RecordField`, `RecordType` i `RecordStatus`.

Kontekst:

MVP-006 ma przygotowac fundament pod docelowego Managera jako aplikacje do generycznych rekordow, ale bez zmiany dzialania obecnej aplikacji. Obecny model `orders` oraz warsztatowe pola nadal obsluguja realne dane, wiec nowy model domenowy nie zostal jeszcze podlaczony do UI, serwisu ani SQLite.

Konsekwencje:

- Powstal pakiet `domain` dla przyszlych modeli domenowych.
- Nowe struktury sa neutralne i nie uzywaja warsztatowych nazw jako docelowych pojec domenowych.
- Nie zmieniono schematu bazy, UI, zaleznosci ani sposobu zapisu danych.
- `orders`, `OrderService` i obecne pola UI pozostaja stanem przejsciowym.
- Przyszle MVP powinny stopniowo mapowac obecny model na `Record`, projektowac konfigurowalne pola i statusy oraz planowac migracje z ochrona istniejacych danych.
- Glownym ryzykiem pozniejszej migracji jest utrata kompatybilnosci z lokalnymi bazami uzytkownikow albo jednoczesna zmiana schematu, UI i logiki zapisu.

## 2026-05-12 - Definicje pol zaczynaja sie w `domain/field_definition.py`

Decyzja:

Dodano neutralny model definicji pol w `domain/field_definition.py`, domyslna konfiguracje w `config/default_record_fields.json` oraz loader w `services/field_config_service.py`.

Kontekst:

MVP-007 ma przygotowac fundament pod konfigurowalne pola rekordow bez zmiany obecnego UI, zachowania aplikacji i schematu SQLite. Dlatego konfiguracja pol jest wczytywalna, ale nie jest jeszcze uzywana przez statyczny formularz ani obecny model `orders`.

Konsekwencje:

- `FieldType` definiuje typy `text`, `number`, `date`, `boolean` i `select`.
- `FieldOption` opisuje opcje dla pola wyboru.
- `FieldDefinition` opisuje pojedyncze pole rekordu.
- `FieldConfigService` wczytuje liste definicji pol z JSON i mapuje ja na obiekty domenowe.
- Domyslna konfiguracja jest neutralna: `title`, `description`, `status`, `created_date`.
- Nie zmieniono UI, bazy danych, zaleznosci ani sposobu zapisu danych.
- Obecny model warsztatowy i `OrderService` pozostaja stanem przejsciowym.
- Nastepny bezpieczny krok to walidacja konfiguracji albo adapter do `RecordType`, nadal bez dynamicznego UI i migracji bazy.

## 2026-05-12 - Definicje typow rekordow zaczynaja sie w `domain/record_type.py`

Decyzja:

Dodano neutralny model typu rekordu w `domain/record_type.py`, domyslna konfiguracje w `config/default_record_type.json` oraz loader w `services/record_type_config_service.py`.

Kontekst:

MVP-008 ma przygotowac fundament pod konfigurowalne typy rekordow bez zmiany obecnego UI, zachowania aplikacji i schematu SQLite. Typ rekordu ma w przyszlosci laczyc zestaw pol w uzytkownikowo definiowana kategorie danych, ale obecny statyczny formularz i model `orders` pozostaja aktywne.

Konsekwencje:

- `RecordTypeDefinition` opisuje typ rekordu przez `id`, `name`, opcjonalny opis i liste identyfikatorow pol.
- `RecordTypeConfigService` wczytuje konfiguracje typu rekordu z JSON i mapuje ja na obiekt domenowy.
- Domyslna konfiguracja jest neutralna: `default`, `Default record`, pola `title`, `description`, `status`, `created_date`.
- Nie zmieniono UI, bazy danych, zaleznosci ani sposobu zapisu danych.
- Obecny model warsztatowy i `OrderService` pozostaja stanem przejsciowym.
- Nastepny bezpieczny krok to walidacja referencji pol albo adapter laczacy `RecordTypeDefinition` z `FieldDefinition`, nadal bez dynamicznego UI i migracji bazy.

## 2026-05-12 - Konfiguracja aplikacji zaczyna sie w `domain/app_config.py`

Decyzja:

Dodano neutralny model konfiguracji aplikacji w `domain/app_config.py`, domyslna konfiguracje w `config/app_config.json` oraz loader w `services/app_config_service.py`.

Kontekst:

MVP-009 ma przygotowac fundament pod przyszle ustawienia Managera, takie jak nazwa aplikacji i sekcje/karty. Pelny ekran ustawien oraz ikona zebatki maja byc osobnym MVP, dlatego konfiguracja jest wczytywalna, ale nie jest jeszcze uzywana przez obecny UI.

Konsekwencje:

- `AppConfig` opisuje `app_name`, `active_record_type_id` i liste sekcji.
- `AppSection` opisuje pojedyncza sekcje aplikacji.
- `AppConfigService` wczytuje konfiguracje aplikacji z JSON i mapuje ja na obiekty domenowe.
- Domyslna konfiguracja jest neutralna: `Manager`, `default`, sekcje `Dashboard`, `Records`, `Archive`.
- Nie zmieniono UI, tytulu okna, kart, bazy danych, zaleznosci ani sposobu zapisu danych.
- Obecny stary UI pozostaje stanem przejsciowym.
- Nastepny bezpieczny krok to walidacja konfiguracji aplikacji albo osobny MVP dla ustawien pod ikona zebatki.

## 2026-05-12 - Sekcje aplikacji zaczynaja sie w `domain/app_section.py`

Decyzja:

Dodano neutralny model sekcji/kart aplikacji w `domain/app_section.py`, domyslna konfiguracje w `config/default_sections.json` oraz loader w `services/section_config_service.py`.

Kontekst:

MVP-010 ma przygotowac fundament pod przyszle konfigurowalne sekcje i karty Managera. Dynamiczne menu, edytor kart, ikona zebatki oraz ekran ustawien maja byc osobnymi MVP, dlatego konfiguracja sekcji jest wczytywalna, ale nie jest jeszcze uzywana przez obecny UI.

Konsekwencje:

- `AppSectionDefinition` opisuje sekcje przez `id`, `name`, `type`, opcjonalne `record_type_id`, `visible` i `order`.
- `SectionConfigService` wczytuje liste sekcji z JSON i mapuje ja na obiekty domenowe.
- Domyslna konfiguracja jest neutralna: `dashboard`, `records`, `archive`, `settings`.
- Nie zmieniono UI, kart Tkinter, bazy danych, zaleznosci ani sposobu zapisu danych.
- Obecny stary UI pozostaje stanem przejsciowym.
- Nastepny bezpieczny krok to walidacja konfiguracji sekcji albo osobny MVP dla ustawien/ikony zebatki.

## 2026-05-12 - Centralny dostep do konfiguracji zaczyna sie w `services/config_service.py`

Decyzja:

Dodano `ConfigService` i `ManagerConfig` w `services/config_service.py` jako centralny punkt odczytu konfiguracji.

Kontekst:

MVP-011 ma uporzadkowac rozproszone loadery konfiguracji bez zmiany UI i zachowania aplikacji. Projekt ma juz osobne loadery dla konfiguracji aplikacji, pol, typu rekordu i sekcji, wiec centralny serwis powinien byc cienka warstwa agregujaca, a nie nowym miejscem duplikowania parsowania JSON.

Konsekwencje:

- `ConfigService` korzysta z `AppConfigService`, `FieldConfigService`, `RecordTypeConfigService` i `SectionConfigService`.
- Szczegolowe loadery pozostaja w projekcie i nadal odpowiadaja za parsowanie swoich plikow.
- `load_all()` zwraca `ManagerConfig` z konfiguracja aplikacji, definicjami pol, typem rekordu i sekcjami.
- Nie zmieniono UI, bazy danych, zaleznosci ani sposobu zapisu danych.
- Centralny serwis jest przygotowaniem pod przyszla ikone zebatki, ekran ustawien, konfigurator pol i konfigurator kart.
- Nastepny bezpieczny krok to walidacja spojnosc konfiguracji albo osobny MVP dla ustawien korzystajacych z `ConfigService`.

## 2026-05-12 - Zapis konfiguracji zaczyna sie w `services/config_service.py`

Decyzja:

Rozbudowano `ConfigService` o metody zapisu konfiguracji do plikow JSON.

Kontekst:

MVP-012 ma przygotowac fundament pod przyszly ekran ustawien i ikone zebatki bez zmiany obecnego UI. Poniewaz `ConfigService` jest centralnym punktem dostepu do konfiguracji, dodano w nim zapis obiektow domenowych do istniejacych plikow JSON, bez usuwania szczegolowych loaderow.

Konsekwencje:

- `ConfigService` zapisuje `app_config.json`, `default_record_fields.json`, `default_record_type.json` i `default_sections.json`.
- Dodano `save_app_config()`, `save_field_definitions()`, `save_record_type()`, `save_sections()` i `save_all()`.
- Zapis uzywa standardowej biblioteki Pythona, `ensure_ascii=False` i `indent=2`.
- Zapis nie jest jeszcze podlaczony do UI i nie dodaje funkcji uzytkowych.
- Nie zmieniono UI, bazy danych, zaleznosci ani sposobu dzialania aplikacji.
- Backup konfiguracji przed zapisem pozostaje osobnym przyszlym krokiem.

## 2026-05-12 - Walidacja konfiguracji zaczyna sie w `services/config_validation_service.py`

Decyzja:

Dodano `ConfigValidationService` i `ConfigValidationResult` jako podstawowy mechanizm walidacji konfiguracji.

Kontekst:

MVP-013 ma przygotowac przyszly ekran ustawien do sprawdzania konfiguracji przed zapisem, ale bez zmiany obecnego UI i startu aplikacji. Poniewaz konfiguracja nie jest jeszcze uzywana przez runtime UI, walidacja jest dostepna jako jawnie wywolywany serwis i nie blokuje uruchamiania aplikacji.

Konsekwencje:

- Walidator sprawdza konfiguracje aplikacji, definicje pol, typ rekordu i sekcje.
- Wynik walidacji zawiera liste czytelnych komunikatow bledow i flage `is_valid`.
- `ConfigService` udostepnia `validate_all()`.
- Walidacja jest podstawowa i nie jest jeszcze pelnym systemem ustawien.
- Nie zmieniono UI, bazy danych, zaleznosci ani sposobu dzialania aplikacji.
- Przyszly ekran ustawien powinien uzywac walidacji przed zapisem konfiguracji.

## 2026-05-13 - Diagnostyka konfiguracji zaczyna sie w `tools/check_config.py`

Decyzja:

Dodano prosty skrypt developerski `tools/check_config.py` do konsolowego sprawdzania ladowania i walidacji konfiguracji.

Kontekst:

MVP-014 ma dac bezpieczny dev-check przed przyszlym ekranem ustawien, bez zmiany obecnego UI, startu aplikacji i schematu bazy danych. Projekt ma juz `ConfigService` oraz `ConfigValidationService`, wiec diagnostyka powinna korzystac z tych samych uslug zamiast tworzyc osobna sciezke walidacji.

Konsekwencje:

- Konfiguracje mozna sprawdzic poleceniem `python tools/check_config.py`.
- Skrypt laduje konfiguracje przez `ConfigService` i uruchamia walidacje przez `ConfigService.validate_all()`.
- Narzedzie wypisuje `Configuration check: OK` albo czytelna liste bledow.
- Skrypt jest narzedziem developerskim, nie ekranem ustawien, ikona zebatki ani elementem Tkinter.
- Nie zmieniono UI, schematu SQLite, plikow JSON konfiguracji, zaleznosci ani sposobu startu przez `python main.py`.
- Przyszly ekran ustawien powinien korzystac z tych samych uslug konfiguracji i walidacji.

## 2026-05-13 - Tytul okna korzysta z `app_name` w konfiguracji

Decyzja:

Obecny tytul okna Tkinter jest ladowany z `config/app_config.json` przez `ConfigService`.

Kontekst:

MVP-015 ma byc pierwszym malym krokiem integracji konfiguracji aplikacji z UI. Celem jest tylko uzycie `app_name` jako tytulu okna, bez dodawania ekranu ustawien, ikony zebatki, dynamicznych kart, edytora nazwy aplikacji ani migracji bazy danych.

Konsekwencje:

- `WorkshopApp` ustawia tytul okna na wartosc `app_name` z konfiguracji.
- Jesli konfiguracja nie zaladuje sie poprawnie albo nazwa jest pusta, uzywany jest fallback `Manager`.
- Reszta aplikacji nadal dziala na starym przejsciowym UI.
- Nie zmieniono formularzy, tabel, zapisu, edycji, usuwania, wyszukiwania, schematu SQLite ani zaleznosci.
- Pelny ekran ustawien i ikona zebatki pozostaja osobnym MVP.

## 2026-05-13 - Ustawienia zaczynaja sie od read-only podgladu

Decyzja:

Dodano pierwszy widoczny szkielet ustawien jako subtelny przycisk z zebatka i proste okno podgladu read-only.

Kontekst:

Manager ma docelowo pozwalac na konfiguracje nazwy aplikacji, sekcji, typow rekordow i pol. MVP-016 ma byc jednak tylko malym krokiem wizualnym i diagnostycznym, bez edycji, zapisu ustawien z UI, dynamicznego przebudowywania interfejsu i zmian w bazie danych.

Konsekwencje:

- Uzytkownik widzi zalazek przyszlych ustawien w obecnym UI.
- Okno ustawien pokazuje nazwe aplikacji, aktywny typ rekordu i liczbe sekcji/kart.
- Podglad korzysta z `ConfigService` i ma fallback przy bledzie ladowania konfiguracji.
- Niczego nie da sie jeszcze edytowac ani zapisac z UI.
- Nie dodano edytora nazwy aplikacji, kart, pol, migracji bazy, nowych tabel ani presetow branzowych.
- Obecna aplikacja nadal dziala na starym przejsciowym UI.

## 2026-05-13 - Nazwa aplikacji jest pierwszym edytowalnym ustawieniem

Decyzja:

Okno ustawien pozwala edytowac `app_name` i zapisuje zmiane do `config/app_config.json` przez `ConfigService`.

Kontekst:

Manager ma juz konfiguracje, walidacje, zapis konfiguracji, tytul okna pobierany z `app_name` i zalazek ustawien pod zebatka. MVP-017 ma dodac tylko jeden maly edytowalny element, bez wchodzenia w edytory kart, pol i typow rekordow.

Konsekwencje:

- Nazwa aplikacji moze byc zmieniona z okna ustawien.
- Pusta nazwa jest odrzucana i nie zapisuje sie.
- Zapis trafia do `config/app_config.json`.
- Po poprawnym zapisie tytul obecnego okna jest aktualizowany.
- Edycja kart, pol i typow rekordow pozostaje osobnymi MVP.
- Nie zmieniono schematu SQLite, tabel, importu, eksportu ani glownych funkcji aplikacji.

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

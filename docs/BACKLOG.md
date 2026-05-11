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

Status: w toku

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

Status: planowane

Cel:

- stopniowo wydzielic obsluge SQLite,
- zachowac obecny schemat i zachowanie,
- przygotowac miejsce pod przyszly model generycznych rekordow.

Kandydaci prac:

- przeniesc dostep do SQLite do osobnego modulu lub helperow,
- zachowac nazwy tabel i kolumn bez zmian,
- nie zmieniac migracji ani danych,
- dodac reczne scenariusze testowe dla zapisu, edycji, usuwania, archiwum i eksportu.

### MVP-004 - Extract UI layout/components

Status: planowane

Cel:

- stopniowo wydzielic budowanie interfejsu Tkinter,
- ograniczyc rozrost `main.py`,
- zachowac obecny wyglad i zachowanie UI.

Kandydaci prac:

- wydzielic budowanie zakladek i formularza,
- pozostawic te same etykiety, rozmiary i akcje,
- nie zmieniac zachowania przyciskow,
- nie zmieniac ukladu bez osobnego zadania UI.

### MVP-005 - Introduce generic record type model

Status: planowane

Cel:

- zaprojektowac neutralny model typow rekordow,
- unikac zalozen branzowych,
- przygotowac bezpieczna migracje z obecnego modelu.

Kandydaci prac:

- opisac docelowy model typu rekordu,
- zaplanowac migracje z `orders`,
- nie wdrazac nowego schematu bez decyzji i backupu.

### MVP-006 - Introduce configurable fields model

Status: planowane

Cel:

- zaprojektowac konfiguracje pol,
- uwzglednic podstawowe typy danych,
- zachowac mozliwosc wyswietlania i edycji danych lokalnie.

Kandydaci prac:

- opisac typy pol,
- opisac walidacje,
- opisac sposob zapisu konfiguracji,
- unikac hardcodowania nowych pol pod konkretna branze.

### MVP-007 - Fundament wyszukiwania i filtrowania

Status: planowane

Cel:

- przygotowac wyszukiwanie niezalezne od jednej branzy,
- zaprojektowac filtry dla konfigurowalnych pol i statusow.

### MVP-008 - Fundament archiwum

Status: planowane

Cel:

- utrzymac mozliwosc archiwizacji rekordow,
- oddzielic pojecie archiwum od obecnego modelu zlecen.

### MVP-009 - Fundament importu i eksportu

Status: planowane

Cel:

- zaprojektowac import i eksport dla generycznych rekordow,
- utrzymac prosty eksport lokalny,
- unikac zaleznosci od chmury i zewnetrznego backendu.

# Backlog - Manager

## MVP

### MVP-001 - Dokumentacja i mapa kodu

Status: w toku

Cel:

- dodac podstawowa dokumentacje projektu,
- opisac wizje produktu,
- opisac obecna strukture techniczna,
- przygotowac mape kodu bez zmiany dzialania aplikacji.

### MVP-002 - Przeglad struktury repozytorium i kodu

Status: planowane

Cel:

- dokladniej przejrzec `main.py`,
- opisac odpowiedzialnosci klas i metod,
- wskazac obszary do przyszlego wydzielenia.

### MVP-003 - Oddzielenie warstwy danych

Status: planowane

Cel:

- stopniowo wydzielic obsluge SQLite,
- zachowac obecny schemat i zachowanie,
- przygotowac miejsce pod przyszly model generycznych rekordow.

### MVP-004 - Oddzielenie warstwy UI

Status: planowane

Cel:

- stopniowo wydzielic budowanie interfejsu Tkinter,
- ograniczyc rozrost `main.py`,
- zachowac obecny wyglad i zachowanie UI.

### MVP-005 - Fundament konfigurowalnych typow rekordow

Status: planowane

Cel:

- zaprojektowac neutralny model typow rekordow,
- unikac zalozen branzowych,
- przygotowac bezpieczna migracje z obecnego modelu.

### MVP-006 - Fundament konfigurowalnych pol

Status: planowane

Cel:

- zaprojektowac konfiguracje pol,
- uwzglednic podstawowe typy danych,
- zachowac mozliwosc wyswietlania i edycji danych lokalnie.

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

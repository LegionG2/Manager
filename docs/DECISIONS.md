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

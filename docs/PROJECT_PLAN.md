# Project Plan — Leon Warsztat Manager

## Cel projektu

Uporządkować i rozwijać lokalną aplikację desktopową.
Zrobić ją bardziej uniwersalną.

## Aktualny stan

Aplikacja działa jako program Python/Tkinter i zapisuje dane lokalnie w SQLite.

## Aktualne funkcje

- obsługa zleceń warsztatowych
- dane klienta
- dane pojazdu
- status zlecenia
- priorytet
- mechanik
- terminy
- koszty
- notatki
- archiwum
- eksport CSV
- backup danych
- tryb jasny/ciemny

## Zasady rozwoju

- Najpierw import projektu do Git/GitHub.
- Potem małe, kontrolowane zmiany.
- Bez dużego refaktoru na start.
- Każda zmiana musi być testowana ręcznie.
- Nie wrzucać bazy danych ani danych klientów do repozytorium.

## Backlog

- uporządkowanie README
- poprawa UI
- poprawa wyszukiwania
- lepsze filtrowanie zleceń
- eksport danych
- rozbicie dużego main.py na mniejsze moduły w przyszłości
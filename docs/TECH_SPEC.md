# Tech Spec - Manager

## Obecny stack

- Python
- Tkinter
- SQLite
- Lokalny plik ustawien JSON
- Podejscie local-first

## Docelowy stack na ten moment

- Python jako glowny jezyk aplikacji.
- Tkinter jako framework UI.
- SQLite jako lokalna baza danych.
- Brak chmury na start.
- Brak systemu logowania na start.
- Brak zewnetrznego backendu na ten moment.
- Brak nowych zaleznosci bez osobnej decyzji.

## Obecna znana struktura techniczna

Repozytorium jest male i skupione wokol jednego pliku aplikacji:

- `main.py` zawiera aplikacje Tkinter, obsluge SQLite, ustawienia, logike rekordow, archiwum, eksport CSV i backup.
- `build_exe.bat` zawiera prosty proces budowy pliku EXE przez PyInstaller.
- `README.md` opisuje obecna aplikacje i sposob uruchamiania.
- `docs/` zawiera dokumentacje projektu.
- `AGENTS.md` zawiera zasady pracy dla przyszlych agentow AI/kodu.

## Dane lokalne

Na podstawie obecnego kodu aplikacja zapisuje dane poza repozytorium, w katalogu uzytkownika Windows:

- baza SQLite: `warsztat_manager.db`,
- ustawienia: `settings.json`,
- katalog aplikacji: `AppData/Local/WarsztatManagerPremium`.

Nazwy te sa obecnie zwiazane ze stara wersja aplikacji. Nalezy traktowac je jako stan przejsciowy, a nie docelowa wizje produktu.

## Obecny model danych

Obecny kod tworzy tabele `orders` w SQLite. Model zawiera pola zwiazane z poprzednim zastosowaniem aplikacji, m.in. klient, pojazd, status, priorytet, terminy, koszty, notatki i archiwum.

To nie jest jeszcze docelowy generyczny model rekordow. Przed zmianami schematu nalezy zaplanowac migracje i zabezpieczenie istniejacych danych.

## Zasady techniczne

- Nie zmieniac schematu bazy danych bez wyraznego zadania.
- Nie dodawac zaleznosci bez decyzji architektonicznej.
- Nie przenosic plikow bez potrzeby.
- Wydzielanie modulow robic stopniowo.
- Zachowywac kompatybilnosc z obecnym dzialaniem aplikacji.
- Dokumentowac istotne decyzje w `docs/DECISIONS.md`.

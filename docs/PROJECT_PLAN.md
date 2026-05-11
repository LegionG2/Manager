# Project Plan - Manager

## Cel projektu

Rozwijac lokalna aplikacje desktopowa Manager jako czysty, uniwersalny system do zarzadzania dowolnymi rekordami.

Projekt ma pozostac prosty, lokalny i elastyczny. Uzytkownik powinien moc dopasowac aplikacje do wlasnego sposobu pracy bez zmiany kodu aplikacji.

## Wizja projektu

Manager ma byc systemem bazowym, podobnym ideowo do czystej platformy do zarzadzania danymi.

Aplikacja nie powinna narzucac konkretnej branzy, konkretnego procesu ani gotowego modelu danych. Jej glowna wartoscia ma byc elastyczny rdzen, ktory pozwala uzytkownikowi samodzielnie okreslic, czym chce zarzadzac.

Docelowo uzytkownik powinien moc:

- definiowac typy rekordow,
- definiowac pola dla rekordow,
- definiowac statusy,
- wyszukiwac i filtrowac dane,
- zapisywac wszystko lokalnie,
- eksportowac i archiwizowac dane,
- dostosowac aplikacje do roznych zastosowan bez zmian w kodzie.

## Rdzen aplikacji

Rdzen aplikacji powinien byc neutralny i niezalezny od branzy.

Podstawowe zalozenia techniczne:

- aplikacja lokalna desktopowa,
- Python/Tkinter,
- SQLite jako lokalna baza danych,
- brak chmury na start,
- brak logowania na start,
- brak gotowych branzowych presetow na start,
- male, kontrolowane zmiany,
- bez duzego refaktoru w pierwszym kroku.

Podstawowe zalozenia funkcjonalne:

- przechowywanie rekordow,
- edycja rekordow,
- usuwanie lub archiwizacja rekordow,
- statusy rekordow,
- pola tekstowe, liczbowe, daty i notatki,
- wyszukiwanie,
- filtrowanie,
- eksport danych,
- backup danych,
- ustawienia lokalne.

## Konfigurowalne elementy

Aplikacja powinna zmierzac w strone modelu, w ktorym uzytkownik sam konfiguruje elementy systemu.

Elementy do konfiguracji:

- typy rekordow,
- nazwy pol,
- rodzaje pol,
- kolejnosc pol,
- wymagane i opcjonalne pola,
- statusy,
- priorytety lub inne listy wyboru,
- widocznosc kolumn,
- podstawowe filtry,
- nazwy widokow,
- eksport wybranych danych.

Konfiguracja powinna byc zapisywana lokalnie, najlepiej w SQLite lub prostych plikach konfiguracyjnych, jezeli bedzie to uzasadnione.

## Czego projekt nie powinien narzucac

Manager nie powinien byc projektowany jako zestaw gotowych szablonow dla konkretnych branz.

Projekt nie powinien narzucac:

- konkretnej branzy,
- jednego typu rekordu,
- stalego zestawu pol,
- stalego zestawu statusow,
- stalego procesu pracy,
- gotowych presetow branzowych na start,
- koniecznosci logowania,
- zaleznosci od chmury,
- zmiany kodu przy kazdym nowym zastosowaniu.

Nazwy i struktury zwiazane ze stara aplikacja warsztatowa powinny byc traktowane jako stan przejsciowy, a nie jako docelowy kierunek projektu.

## Plan przejscia ze starej aplikacji warsztatowej do uniwersalnego Managera

Przejscie powinno odbywac sie malymi krokami, bez przebudowy calej aplikacji na raz.

1. Uporzadkowac dokumentacje i opisac poprawna wizje projektu.
2. Zachowac dzialajaca aplikacje bez duzego refaktoru na start.
3. Zidentyfikowac miejsca w kodzie, gdzie logika jest zbyt mocno zwiazana z modelem warsztatowym.
4. Stopniowo zmieniac nazewnictwo w UI i dokumentacji na neutralne.
5. Wydzielic liste statusow i pol do konfiguracji.
6. Dodac mozliwosc definiowania typow rekordow.
7. Dodac mozliwosc definiowania pol dla typu rekordu.
8. Zachowac istniejace dane i funkcje podczas migracji.
9. Dopiero po stabilizacji rozwazyc rozbicie duzego `main.py` na mniejsze moduly.

Kazdy etap powinien byc testowany recznie przed przejsciem dalej.

## Aktualny stan

Aplikacja dziala jako lokalny program Python/Tkinter i zapisuje dane w SQLite.

Obecny kod nadal zawiera elementy starej aplikacji warsztatowej. To jest punkt startowy do stopniowego przejscia na uniwersalny Manager.

## Aktualne funkcje

- lokalna aplikacja desktopowa,
- zapis danych w SQLite,
- obsluga rekordow w obecnym modelu aplikacji,
- status rekordu,
- priorytet,
- terminy,
- koszty lub inne dane liczbowe,
- notatki,
- archiwum,
- eksport CSV,
- backup danych,
- tryb jasny/ciemny.

## Zasady rozwoju

- Pracowac malymi zmianami.
- Nie przebudowywac calej aplikacji bez potrzeby.
- Nie zmieniac plikow niezwiazanych z zadaniem.
- Najpierw zachowac dzialajace funkcje aplikacji.
- Nie zmieniac sposobu zapisu danych bez wyraznej potrzeby.
- Kazda zmiana musi byc testowana recznie.
- Nie wrzucac bazy danych ani danych uzytkownika do repozytorium.
- Nie dodawac gotowych branzowych presetow jako glownego kierunku projektu.

## Backlog

- uporzadkowanie README,
- neutralizacja nazw w UI,
- poprawa UI,
- poprawa wyszukiwania,
- lepsze filtrowanie rekordow,
- eksport danych,
- konfiguracja statusow,
- konfiguracja pol,
- konfiguracja typow rekordow,
- rozbicie duzego `main.py` na mniejsze moduly w przyszlosci.

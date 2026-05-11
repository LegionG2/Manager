# AGENTS.md

## Zasady pracy

- Pracuj malymi, kontrolowanymi zmianami.
- Najpierw zrozum aktualna strukture projektu.
- Nie przepisuj `main.py`, chyba ze zadanie wyraznie tego wymaga.
- Nie przebudowuj calej aplikacji bez potrzeby.
- Nie zmieniaj plikow niezwiazanych z zadaniem.
- Zachowuj obecne dzialanie aplikacji, chyba ze zadanie mowi inaczej.
- Nie zmieniaj sposobu zapisu danych bez wyraznej potrzeby.
- Nie modyfikuj schematu bazy danych bez osobnego zadania.
- Preferuj stopniowe wydzielanie modulow zamiast duzego refaktoru.
- Unikaj hardcodowania zalozen pod konkretna branze.
- Utrzymuj Managera jako aplikacje generyczna i konfigurowalna.
- Aktualizuj dokumentacje, gdy zmieniaja sie decyzje architektoniczne.
- Po kazdej zmianie podsumuj zmienione pliki.
- Podaj kroki testowe po zakonczeniu zadania.

## Kierunek architektury

- Manager ma byc lokalna aplikacja desktopowa typu local-first.
- Docelowo uzytkownik powinien definiowac typy rekordow, pola, statusy i widoki.
- Obecne nazwy i struktury zwiazane z warsztatem traktuj jako stan przejsciowy.
- Nowe funkcje projektuj neutralnie: jako rekordy, pola, statusy, widoki, archiwum, import i eksport.
- Nie dodawaj presetow branzowych jako glownego kierunku projektu.

## Walidacja

Przed zakonczeniem zadania sprawdz, jesli zakres zmiany tego wymaga:

- czy aplikacja uruchamia sie przez Python,
- czy glowne okno aplikacji dziala,
- czy dane zapisuja sie poprawnie,
- czy istniejace funkcje nie zostaly zepsute,
- czy `git diff --stat` obejmuje tylko zamierzone pliki.

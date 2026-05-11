# Vision - Manager

## Wizja produktu

Manager to lokalna aplikacja desktopowa do zarzadzania wlasnymi rekordami.

Aplikacja ma byc czystym, generycznym systemem bazowym. Nie powinna byc budowana wokol jednej konkretnej branzy ani jednego narzuconego procesu pracy.

Uzytkownik powinien moc sam okreslic, jakiego typu dane chce obslugiwac i jak chce je organizowac.

## Glowne zalozenia

- Aplikacja dziala lokalnie na komputerze uzytkownika.
- Dane sa przechowywane lokalnie.
- Manager nie wymaga chmury na start.
- Manager nie wymaga logowania na start.
- Manager nie narzuca branzy ani gotowych branzowych presetow.
- Konfiguracja powinna byc mozliwa bez zmiany kodu aplikacji.

## Docelowy kierunek

Manager powinien zmierzac w strone elastycznego systemu, w ktorym uzytkownik moze konfigurowac:

- typy rekordow,
- pola rekordow,
- statusy,
- widoki,
- wyszukiwanie,
- filtrowanie,
- archiwum,
- import danych,
- eksport danych.

## Czego unikamy

- Budowania aplikacji pod jedna branze.
- Dodawania gotowych presetow branzowych jako fundamentu produktu.
- Wiazania nazw, statusow i pol z jednym konkretnym zastosowaniem.
- Duzych refaktorow bez udokumentowania obecnego stanu.

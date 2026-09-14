# Użycie

`python app.py prepare --destination E:/ --tool ../prestige-hash-checker` — plan.
`python app.py prepare --destination E:/ --tool ../prestige-hash-checker --apply`
`python app.py verify --destination E:/PrestigeUSB`

Może działać na dowolnym folderze, nie tylko USB. Nie formatuje, nie kasuje, nie pobiera
programów. Wymaga nowego katalogu PrestigeUSB. Kopiuje tylko wskazane narzędzia z wersją
w metadata.json; pomija .git, logi, raporty, .env i środowiska zależności.
Nie tworzy bootowalnego nośnika. Wersje porównuje z zapisanym manifestem, nie Internetem.
Nowe raporty w przeznaczonych na nie katalogach są danymi użytkownika, poza kontrolą kodu zestawu.

## Rozszerzenia 0.2.0

`python app.py update --destination E:/PrestigeUSB --tool ../prestige-hash-checker` pokazuje plan.
Dodaj `--apply`, aby wykonać aktualizację. Lokalne modyfikacje kodu/config i nieznane pliki kodu
blokują wymianę. Raporty/logi są zachowane. Poprzednie wersje i dziennik trafiają do Backup/Updates.
`python app.py rollback --destination E:/PrestigeUSB/Backup/Updates/ID --apply` cofa aktualizację,
sprawdzając czy zestawu nie zmieniono później. Nowe raporty wersji wycofywanej pozostają przy niej
w katalogu .retired, bez usuwania danych. Nie formatuje nośnika ani nie tworzy bootowalnego USB.
Weryfikacja ignoruje dodatkowe pliki użytkownika w Reports/Backup i logs/reports narzędzi.

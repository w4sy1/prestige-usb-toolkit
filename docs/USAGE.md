# Użycie

`python app.py prepare --destination E:/ --tool ../prestige-hash-checker` — plan.
`python app.py prepare --destination E:/ --tool ../prestige-hash-checker --apply`
`python app.py verify --destination E:/PrestigeUSB`

Może działać na dowolnym folderze, nie tylko USB. Nie formatuje, nie kasuje, nie pobiera
programów. Wymaga nowego katalogu PrestigeUSB. Kopiuje tylko wskazane narzędzia z wersją
w metadata.json; pomija .git, logi, raporty, .env i środowiska zależności.
Nie tworzy bootowalnego nośnika. Wersje porównuje z zapisanym manifestem, nie Internetem.
Nowe raporty zapisane później na USB są widoczne jako nowe pliki przy weryfikacji.

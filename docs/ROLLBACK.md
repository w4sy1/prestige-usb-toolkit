# Weryfikacja poprzedniej wersji

Od 0.3.3 rollback sprawdza również poprzednią wersję w katalogu Backup/Updates.
Brak lub zmiana zarządzanego pliku blokuje odtwarzanie przed pierwszą zmianą.
Niezarządzany kod także blokuje operację; logs/reports pozostają danymi użytkownika.

Brak katalogu zapisanej wersji jest dopuszczalny wyłącznie wtedy, gdy docelowe
narzędzie nadal ma wszystkie pliki poprzedniej wersji z poprawnymi hashami.
Pozwala to ponowić przerwane odtwarzanie, bez udawania powodzenia przy utracie kopii.

Testy obejmują uszkodzoną i brakującą kopię, błąd instalacji po przeniesieniu
poprzedniej wersji oraz odzyskanie z dziennika. Testy wykonano w katalogach próbnych;
nie potwierdzają zachowania konkretnego pendrive przy utracie zasilania.

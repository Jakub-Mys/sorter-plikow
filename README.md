**1.Automatyczne Sprzątanie Plików**
Ten program sam robi porządek w Twoim komputerze. 
Rozkłada pobrane pliki do odpowiednich folderów (np. zdjęcia lądują w folderze "Obrazki", a dokumenty w folderze "Dokumenty"). Jeśli znajdzie dwa identyczne pliki, jeden z nich odkłada do folderu "Kwarantanna", żeby nie zajmował niepotrzebnie miejsca.
Wystarczy kliknąć i działa – nie musisz niczego instalować.

**2.Szybka konfiguracja**

Wszystkie ustawienia skryptu znajdziesz w pliku `main.py`.

**2.1. Zmiana folderów i rodzajów plików**
Na samej górze pliku znajdziesz listę. Możesz tam łatwo dopisać nowe rodzaje plików:

```python
CATEGORIES = {
    "Obrazki": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    "Dokumenty": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    "Instalatory": ['.exe', '.msi'],
    "Archiwa": ['.zip', '.rar', '.7z', '.tar', '.gz'],
    "Wideo": ['.mp4', '.mkv', '.avi', '.mov'],
    "Muzyka": ['.mp3', '.wav', '.flac']
}
```

**2.2. Zmiana miejsca sprzątania**
Na samym dole pliku możesz wskazać, który folder ma być posprzątany (domyślnie jest to folder Pobrane):

```python
if __name__ == "__main__":
    downloads_path = Path.home() / "Downloads" # <- Tutaj możesz wpisać inną ścieżkę
    organize_and_deduplicate(downloads_path)
```

---

3. Jak uruchomić?

-**Windows:** Kliknij dwukrotnie plik `uruchom_sorter.bat`.
-**Terminal Windows:** Wpisz polecenie `python main.py`.

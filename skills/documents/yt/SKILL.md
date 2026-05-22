---
name: yt
description: Pobranie i analiza transkrypcji YouTube. Triggers: youtube, yt, transkrypcja, transcript
allowed-tools: Bash, Read, Write, Grep, Task, Glob
---

# Komenda /yt - YouTube Transcript

Pobiera transkrypcję z YouTube i umożliwia analizę/pytania o film.

## Ścieżka tymczasowa:
`C:\Users\kamil\AppData\Local\Temp\yt-transcripts\`

## Workflow:

### 1. Przygotuj folder (Bash):
```bash
mkdir -p "C:\Users\kamil\AppData\Local\Temp\yt-transcripts"
```

### 2. Pobierz transkrypcję (Bash):
```bash
python -m yt_dlp --write-auto-sub --sub-lang en,pl --skip-download --sub-format vtt -o "C:\Users\kamil\AppData\Local\Temp\yt-transcripts\%(id)s" "$url" 2>&1
```

**Możliwe błędy:**
- `429 Too Many Requests` → Spróbuj tylko `--sub-lang en`
- `No subtitles` → Film nie ma napisów, poinformuj użytkownika

### 3. Znajdź plik VTT:
```bash
dir "C:\Users\kamil\AppData\Local\Temp\yt-transcripts\*.vtt" /b 2>nul
```

### 4. Wyczyść VTT do czystego tekstu (Bash):
Usuń timestampy i duplikaty - stwórz czysty plik .txt:
```bash
python -c "
import re
import sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    content = f.read()
# Usuń nagłówek WEBVTT
content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.DOTALL)
# Usuń timestampy i tagi
content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', content)
content = re.sub(r'<[^>]+>', '', content)
content = re.sub(r'align:start position:\d+%', '', content)
# Usuń puste linie i duplikaty
lines = [l.strip() for l in content.split('\n') if l.strip()]
# Usuń powtarzające się linie (napisy często duplikują)
unique = []
for line in lines:
    if not unique or line != unique[-1]:
        unique.append(line)
print('\n'.join(unique))
" "$vtt_file" > "${vtt_file%.vtt}.txt"
```

### 5. Deleguj agenta do analizy (Task tool):

```
Task(subagent_type="Explore"):
    "KONTEKST: Użytkownik chce przeanalizować film YouTube.

    ZADANIE: Przeczytaj CAŁY plik transkrypcji:
    [ścieżka do .txt]

    Następnie:
    1. Podaj tytuł/temat filmu (pierwsze 30 sekund)
    2. Zrób SZCZEGÓŁOWE podsumowanie (500-800 słów)
    3. Wypisz KLUCZOWE PUNKTY (bullet points)
    4. Wypisz CYTATY WARTE ZAPAMIĘTANIA
    5. Jeśli użytkownik zadał pytanie: '$pytanie' - odpowiedz na nie

    FORMAT: Markdown z sekcjami"
```

### 6. Pokaż wynik użytkownikowi:

```
📺 **YouTube Transcript Ready**

**Film:** [tytuł z transkrypcji]
**Plik:** [ścieżka do .txt]

[Podsumowanie od agenta]

---
Możesz zadawać pytania o ten film.
Plik transkrypcji: [ścieżka]
```

## Późniejsze pytania:

Jeśli użytkownik zadaje pytanie o film (po /yt), użyj:
```
Task(subagent_type="Explore"):
    "KONTEKST: Użytkownik pyta o film YouTube.
    Transkrypcja: [ścieżka]

    PYTANIE: [pytanie użytkownika]

    Przeczytaj transkrypcję i odpowiedz szczegółowo."
```

## Cleanup (opcjonalnie):

Po zakończeniu rozmowy o filmie:
```bash
del "C:\Users\kamil\AppData\Local\Temp\yt-transcripts\*.*"
```

## Obsługa błędów:

| Błąd | Rozwiązanie |
|------|-------------|
| No subtitles | Film nie ma napisów - poinformuj |
| 429 Rate limit | Poczekaj 30s, spróbuj ponownie |
| File too large | Podziel na części (offset/limit) |
| JS runtime warning | Ignoruj - działa bez tego |

## WAŻNE:
- Zawsze deleguj czytanie do agenta (oszczędność kontekstu)
- Czysty .txt jest ~10x mniejszy niż .vtt
- Zachowaj ścieżkę do pliku dla kolejnych pytań

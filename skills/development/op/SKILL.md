---
name: op
description: Integracja KFG do istniejącego projektu bez logs/. Triggers: dodaj KFG, old project, zintegruj
allowed-tools: Glob, Read, Write, Edit, Bash(git:*), Bash(mkdir:*)
---

# Komenda /op - Old Project

Zintegruj KFG (Kmylpenter File Genius) z istniejącym projektem.

## Ścieżki projektów (sprawdź w kolejności):
1. `D:\Projekty StriX\` (preferowana)
2. `C:\Users\kamil\projekty\`
3. Current directory (jeśli user jest już w projekcie)

## Co robić:

### 1. Jeśli podano argument (nazwa projektu):
- Znajdź projekt o tej nazwie
- Przejdź do kroku 3

### 2. Jeśli brak argumentu:
- Użyj `Glob("*/logs")` w ścieżkach projektów
- Wylistuj projekty które NIE mają folderu `logs/`
- Pokaż listę i zapytaj który zainicjalizować

### 3. Analiza projektu (użyj Read/Glob, NIE Bash):
- `Glob("package.json")` → typ node, czytaj dependencies
- `Glob("requirements.txt")` → typ python
- `Glob("Cargo.toml")` → typ rust
- `Glob("go.mod")` → typ go
- `Read("README.md")` → opis (pierwsze 2-3 linie bez #)
- `git log --oneline -5` → ostatnie commity

### 4. Utwórz strukturę (użyj Write):
```
logs/
├── STATE.md       ← wypełnij danymi z analizy
├── CHANGELOG.md   ← dodaj ostatnie commity
├── DEVLOG.md      ← dodaj kontekst projektu
├── CONTINUITY.md  ← pusty szablon
├── adr/README.md
├── archive/
├── handoffs/
└── screenshots/
```

### 5. Dodaj do .gitignore:
```
logs/archive/
logs/screenshots/
```

### 6. Podsumowanie:
```
✅ KFG zainicjalizowany w [nazwa]

Wykryto:
- Typ: [node/python/rust/...]
- Stack: [dependencies]
- Commits: [liczba]

Utworzono: logs/ (STATE, CHANGELOG, DEVLOG, CONTINUITY)

Powiedz "stan" aby zobaczyć status.
```

## WAŻNE:
- Użyj Glob/Read zamiast Bash (szybciej!)
- Jeden Bash call tylko dla git log
- Wypełnij pliki sensowną treścią z analizy

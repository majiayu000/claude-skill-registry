---
name: np
description: Nowy projekt z pełną strukturą KFG (logs, docs). Triggers: nowy projekt KFG, new project, inicjalizuj
allowed-tools: Glob, Read, Write, Edit, Bash(git:*), Bash(mkdir:*), Bash(gh:*)
---

# Komenda /np - New Project

Utwórz nowy projekt z pełną konfiguracją KFG.

## Ścieżki projektów (sprawdź w kolejności):
1. `D:\Projekty StriX\` (preferowana)
2. `C:\Users\kamil\projekty\`
3. Current directory (jeśli user jest w innym folderze)

## Kroki (wykonaj RÓWNOLEGLE gdzie możliwe):

### 1. Git init (jeden Bash call):
```bash
cd "[ścieżka]" && mkdir -p "$1" && cd "$1" && git init && mkdir -p logs/adr logs/archive logs/handoffs logs/screenshots
```

### 2. Utwórz pliki (Write RÓWNOLEGLE - jeden tool message):

**logs/STATE.md:**
```markdown
# Current State

**Last Updated:** [DZIŚ]
**Updated By:** KFG init

---

## Active Work
- Nowy projekt - do zdefiniowania

## Blockers
- Brak

## Recently Completed
- ✅ Projekt zainicjalizowany z KFG ([DZIŚ])

## Next Priorities
1. Zdefiniować cel projektu
2. Pierwszy feature
```

**logs/CHANGELOG.md:**
```markdown
# Changelog

## [Unreleased]

### Added
- Inicjalizacja projektu z KFG
```

**logs/DEVLOG.md:**
```markdown
# Development Log

## Current Context
**Last Updated:** [DZIŚ]

### Project State
- **Project:** $1
- **Version:** v0.1.0-dev
- **Phase:** Inicjalizacja

### Current Objectives
- [ ] Zdefiniować cel projektu
```

**logs/CONTINUITY.md:**
```markdown
# Continuity Ledger

## Aktywna Sesja
**Data:** [DZIŚ]
**Urządzenie:** PC
**Cel:** Nowy projekt
**Status:** IN_PROGRESS
```

**logs/adr/README.md:**
```markdown
# ADRs
| ID | Title | Status | Date |
|----|-------|--------|------|
| - | No ADRs yet | - | - |
```

**CLAUDE.md:**
```markdown
# $1

## KFG Commands
- "stan" → STATE + CONTINUITY
- "eos" → Zakończ sesję
```

**.gitignore:**
```
logs/archive/
logs/screenshots/
```

### 3. Opcjonalnie GitHub (zapytaj):
```bash
gh repo create "$1" --private --source=. --push
```

### 4. Podsumowanie:
```
✅ Projekt "$1" utworzony

Ścieżka: [pełna ścieżka]
Struktura: logs/ (STATE, CHANGELOG, DEVLOG, CONTINUITY, adr/)

Powiedz "stan" aby zobaczyć status.
```

## WAŻNE:
- Użyj Write dla WSZYSTKICH plików w JEDNYM RÓWNOLEGŁYM WYWOŁANIU
- Tylko 1-2 wywołania Bash (git init + opcjonalnie gh)
- Data: użyj aktualnej daty

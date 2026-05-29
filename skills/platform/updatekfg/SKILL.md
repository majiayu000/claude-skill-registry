---
name: updatekfg
description: Synchronizacja KFG między urządzeniami (Windows/Android). Triggers: sync KFG, updatekfg, zaktualizuj
---

# /updatekfg - Aktualizacja środowiska KFG

Skill do synchronizacji zmian KFG na wszystkie urządzenia.

## Architektura KFG (PRZECZYTAJ!)

```
KFG/.claude/           →  ~/.claude/ (instalatory kopiują)
├── CLAUDE.md          →  CLAUDE.md (globalne instrukcje)
├── settings.json      →  settings.json (permissions + hooks + statusLine)
├── rules/*.md         →  rules/*.md (reguły automatyczne)
├── hooks/*            →  hooks/* (skrypty walidacji)
├── welcome.txt        →  welcome.txt
├── statusline-wrapper.ps1/.sh  →  statusline wrapper
├── analyze-history.ps1         →  analiza historii (Windows)
└── export-device-stats.ps1     →  eksport stats (Windows)

KFG/platform/
├── android/           →  Android-specific overrides (merge przy instalacji)
└── windows/           →  Windows-specific overrides

KFG/setup/config/
├── termux/.bashrc     →  ~/.bashrc (Android - append)
├── termux/.tmux.conf  →  ~/.tmux.conf (Android)
├── ccstatusline/      →  ~/.config/ccstatusline/ (statusline config)
└── .templates/        →  ~/.templates/ (szablony walidacji)

KFG/desktop/
├── install.ps1        →  Jednorazowy instalator Windows (generuje inline)
├── sync-env.ps1       →  Auto-sync przy każdym `cc` (kopiuje z KFG)
└── config/            →  Windows-specific configs
```

## Mechanizmy synchronizacji

| Platforma | Instalacja | Codzienna sync |
|-----------|------------|----------------|
| **Windows** | `desktop/install.ps1` | Junction (jak symlink) LUB sync-env.ps1 |
| **Android** | `install.sh` (symlink) | Automatyczny (symlink) |

**WAŻNE:**
- Android używa SYMLINK ~/.claude/ → KFG/.claude/ - zmiany w KFG są natychmiast widoczne
- Windows: install.ps1 tworzy JUNCTION ~/.claude/ → KFG/.claude/ (jak symlink)
  - Edycja ~/.claude/* = edycja KFG/.claude/* (ten sam plik!)
  - Git widzi zmiany w KFG/.claude/ automatycznie
  - Jeśli junction nie działa: sync-env.ps1 kopiuje przy `cc`

**UWAGA dla Claude:** Edytuj ~/.claude/CLAUDE.md LUB KFG/.claude/CLAUDE.md - to ten sam plik (junction)!

## Checklist: Co zaktualizować

Przed commitem sprawdź które pliki dotyczą zmiany:

### 1. Instrukcje Claude (CLAUDE.md, rules/)
```
[ ] KFG/.claude/CLAUDE.md - główne instrukcje
[ ] KFG/.claude/rules/*.md - reguły automatyczne
```
**Sync:** Android=natychmiast, Windows=przy `cc`

### 2. Settings (permissions, hooks, statusLine)
```
[ ] KFG/.claude/settings.json - base settings
[ ] KFG/platform/android/settings-override.json - Android override
[ ] KFG/platform/windows/settings-override.json - Windows override (jeśli istnieje)
```
**Sync:** Android=natychmiast, Windows=sync-env kopiuje tylko jeśli nie istnieje lub -Force

### 3. Hooks (walidacja, pre-compact)
```
[ ] KFG/.claude/hooks/*.ps1 - Windows hooks
[ ] KFG/.claude/hooks/*.sh - Android hooks
```
**Sync:** Android=natychmiast, Windows=sync-env

### 4. StatusLine scripts
```
[ ] KFG/.claude/statusline-wrapper.ps1 - Windows wrapper
[ ] KFG/.claude/statusline-wrapper.sh - Android wrapper
[ ] KFG/.claude/analyze-history.ps1 - analiza historii (Windows only)
[ ] KFG/.claude/export-device-stats.ps1 - eksport stats (Windows only)
[ ] KFG/setup/config/ccstatusline/settings.json - ccstatusline config
```
**Sync:** Windows=sync-env, Android=symlink (ale .sh tylko!)

### 5. Bashrc / Shell functions
```
[ ] KFG/setup/config/termux/.bashrc - funkcje bash (p, np, cc, gs...)
[ ] KFG/setup/config/bashrc - alternative location
```
**Sync:** Android=wymaga `source ~/.bashrc` lub reinstall

### 6. Templates
```
[ ] KFG/setup/config/.templates/ - szablony walidacji
[ ] KFG/.templates/ - alternative location
```
**Sync:** Android=install.sh kopiuje, Windows=install.ps1 generuje inline

### 7. Instalatory (jeśli zmiana wymaga)
```
[ ] KFG/install.sh - Android/Linux instalator
[ ] KFG/desktop/install.ps1 - Windows instalator
[ ] KFG/desktop/sync-env.ps1 - Windows daily sync
```

## Workflow aktualizacji

### Mała zmiana (reguły, instrukcje)
```bash
# 1. Edytuj pliki w KFG/.claude/
# 2. Commit + push
git add -A && git commit -m "update: [co]" && git push

# Android: automatycznie (symlink)
# Windows: przy następnym `cc` (sync-env.ps1)
```

### Duża zmiana (nowy feature, settings)
```bash
# 1. Edytuj pliki źródłowe w KFG/
# 2. Sprawdź czy sync-env.ps1 obsługuje nowe pliki
# 3. Commit + push
# 4. Na innych urządzeniach: git pull (Android) lub cc (Windows)
```

### Zmiana wymagająca reinstalacji
```bash
# Jeśli zmieniłeś:
# - install.sh / install.ps1
# - strukturę katalogów
# - nowe pliki których sync-env nie kopiuje

# Android: ./install.sh --force
# Windows: .\desktop\install.ps1 (lub cc z -Force sync)
```

## Przykłady

### Dodanie nowej reguły
```
1. Utwórz: KFG/.claude/rules/nowa-regula.md
2. git add && commit && push
3. Android: automatycznie działa (symlink)
4. Windows: przy następnym `cc`
```

### Zmiana statusline
```
1. Edytuj: KFG/.claude/statusline-wrapper.ps1 (Windows)
2. Edytuj: KFG/.claude/statusline-wrapper.sh (Android) - jeśli dotyczy
3. sync-env.ps1 już kopiuje te pliki
4. git add && commit && push
```

### Nowy skrypt do sync
```
1. Utwórz skrypt w KFG/.claude/
2. Dodaj do sync-env.ps1 $statuslineScripts array (jeśli .ps1)
3. Dla Android: utwórz .sh wersję (symlink = auto)
4. git add && commit && push
```

## Weryfikacja

Po aktualizacji sprawdź:
```powershell
# Windows - sprawdź czy pliki są aktualne
ls ~/.claude/*.ps1
cat ~/.claude/CLAUDE.md | head -20

# Porównaj z KFG
diff ~/.claude/CLAUDE.md $KFG/.claude/CLAUDE.md
```

```bash
# Android - symlink powinien działać
ls -la ~/.claude/  # powinno pokazać -> KFG/.claude/
cat ~/.claude/CLAUDE.md | head -20
```

## TODO (brakujące)

- [ ] Android: analyze-history.sh (bash wersja)
- [ ] Android: export-device-stats.sh (bash wersja)
- [ ] Cross-device stats agregacja na Androidzie

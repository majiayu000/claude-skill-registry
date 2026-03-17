---
name: changelog-generator
description: Automatische Release Notes aus Git Commits. Kategorisiert Commits (Features, Fixes, Breaking Changes), wandelt technische Sprache in kundenfreundliche Beschreibungen um. Aktivieren mit /changelog, /changelog v1.2.0..v1.3.0, oder /changelog --week.
triggers:
  - /changelog
  - changelog erstellen
  - release notes
  - what changed
  - was hat sich geaendert
---

# Changelog Generator

Dieser Skill analysiert die Git-History und erstellt automatisch kundenfreundliche Release Notes.

## Verwendung

```bash
/changelog              # Seit letztem Tag
/changelog v1.2.0..v1.3.0  # Zwischen zwei Versionen
/changelog --week       # Letzte 7 Tage
/changelog --since=2025-12-01  # Seit Datum
```

## Kategorien und Emojis

| Prefix | Kategorie | Emoji | Kundenfreundlicher Titel |
|--------|-----------|-------|--------------------------|
| `feat:` | Features | ✨ | Neue Funktionen |
| `fix:` | Bug Fixes | 🐛 | Fehlerbehebungen |
| `perf:` | Performance | 🔧 | Verbesserungen |
| `refactor:` | Refactoring | 🔧 | Verbesserungen |
| `BREAKING:` | Breaking Changes | 💥 | Wichtige Aenderungen |
| `security:` | Security | 🔒 | Sicherheit |
| `docs:` | Documentation | 📚 | Dokumentation |

## Workflow

### Schritt 1: Git-History abrufen

```bash
# Seit letztem Tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~50")..HEAD --oneline --no-merges

# Zwischen Versionen
git log v1.2.0..v1.3.0 --oneline --no-merges

# Letzte Woche
git log --since="7 days ago" --oneline --no-merges

# Mit Datum und Autor
git log --pretty=format:"%h|%s|%ad|%an" --date=short --since="7 days ago" --no-merges
```

### Schritt 2: Commits kategorisieren

Analysiere jeden Commit und ordne ihn einer Kategorie zu:

```
feat: Add export button → ✨ Features
fix: Resolve login error → 🐛 Bug Fixes
perf: Optimize database queries → 🔧 Verbesserungen
BREAKING: Remove deprecated API → 💥 Wichtige Aenderungen
```

### Schritt 3: Technisch → Kundenfreundlich

Transformiere technische Commit-Messages:

| Technisch | Kundenfreundlich |
|-----------|------------------|
| `feat: Add CSV export to dashboard` | Daten koennen jetzt als CSV-Datei heruntergeladen werden |
| `fix: Resolve null pointer in auth module` | Anmeldeprobleme bei einigen Nutzern behoben |
| `perf: Optimize SQL query for reports` | Berichte laden jetzt deutlich schneller |
| `BREAKING: Remove legacy API v1` | API v1 wird nicht mehr unterstuetzt - bitte auf v2 aktualisieren |

### Schritt 4: Markdown formatieren

## Output-Format

```markdown
## [VERSION] - DATUM

### ✨ Neue Funktionen
- Beschreibung der Funktion (kundenfreundlich)
- Weitere neue Funktion

### 🐛 Fehlerbehebungen
- Problem X wurde behoben
- Stabilitaet bei Y verbessert

### 🔧 Verbesserungen
- Performance-Optimierungen
- Interne Verbesserungen

### 💥 Wichtige Aenderungen
- Beschreibung der Breaking Change
- Migration erforderlich: [Anleitung]

### 🔒 Sicherheit
- Sicherheitsluecke geschlossen

### 📚 Dokumentation
- Dokumentation aktualisiert
```

## Beispiel-Ausgabe

```markdown
## [1.3.0] - 2025-12-26

### ✨ Neue Funktionen
- **Export-Button**: Analyseergebnisse koennen jetzt als Markdown-Datei heruntergeladen werden
- **Chat-Assistent**: Fragen Sie den KI-Assistenten zu Ihren Analyseergebnissen

### 🐛 Fehlerbehebungen
- Anmeldeprobleme bei Google OAuth behoben
- Timeout-Fehler bei grossen Dateien (>5MB) korrigiert

### 🔧 Verbesserungen
- Ladezeiten um 40% reduziert durch optimierte Datenbankabfragen
- Bessere Fehlermeldungen bei ungueltigem Dateiformat

### 🔒 Sicherheit
- Aktualisierung der Stripe-API auf Version 2025-12-15
```

## Git-Befehle Referenz

```bash
# Letzten Tag finden
git describe --tags --abbrev=0

# Alle Tags auflisten
git tag -l --sort=-v:refname

# Commits zwischen Tags
git log v1.2.0..v1.3.0 --oneline --no-merges

# Commits mit Details
git log --pretty=format:"%h|%s|%ad|%an" --date=short HEAD~20..HEAD

# Commits nach Datum
git log --since="2025-12-01" --until="2025-12-26" --oneline

# Breaking Changes finden
git log --grep="BREAKING" --oneline

# Alle feat: Commits
git log --grep="^feat:" --oneline
```

## Konventionen

### Commit-Message-Format (Conventional Commits)

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat` - Neue Funktion
- `fix` - Fehlerbehebung
- `perf` - Performance-Verbesserung
- `refactor` - Code-Refactoring ohne Funktionsaenderung
- `docs` - Dokumentation
- `style` - Formatierung (kein Code-Aenderung)
- `test` - Tests hinzugefuegt/geaendert
- `chore` - Build-Prozess, Abhaengigkeiten
- `ci` - CI/CD Konfiguration

**Breaking Changes:**
- `BREAKING CHANGE:` im Footer
- `!` nach Type: `feat!: Remove deprecated API`

## Spezielle Regeln

### Commits ignorieren

Diese Commits werden nicht in den Changelog aufgenommen:
- `chore:` (interne Aenderungen)
- `style:` (nur Formatierung)
- `test:` (nur Tests)
- `ci:` (nur CI/CD)
- Merge-Commits

### Gruppierung

Commits mit gleichem Scope werden gruppiert:
```
feat(auth): Add Google OAuth
feat(auth): Add Magic Link
→ **Authentifizierung**: Google OAuth und Magic Link hinzugefuegt
```

### Mehrsprachigkeit

Der Changelog wird in der Sprache des Projekts erstellt:
- Pruefen: Sprache in README.md oder package.json
- Default: Deutsch fuer fabrikIQ, Englisch fuer andere Projekte

## Integration

### Pre-Release Workflow

1. `/changelog` ausfuehren
2. Output in CHANGELOG.md einfuegen
3. Version in package.json aktualisieren
4. Commit: `chore: Release v1.3.0`
5. Tag: `git tag v1.3.0`
6. Push: `git push && git push --tags`

### Automatische Versionierung

Basierend auf Commit-Types:
- `feat:` → Minor Version (1.2.0 → 1.3.0)
- `fix:` → Patch Version (1.2.0 → 1.2.1)
- `BREAKING:` → Major Version (1.2.0 → 2.0.0)

## Fehlerbehandlung

### Kein Tag vorhanden

```bash
# Fallback: Letzte 50 Commits
git log HEAD~50..HEAD --oneline --no-merges
```

### Keine Conventional Commits

Falls Commits nicht dem Format folgen:
- Commits nach Schlagwoertern kategorisieren (add, fix, update, remove)
- Warnung ausgeben: "Empfehlung: Conventional Commits verwenden"

### Leerer Changelog

Falls keine relevanten Commits gefunden:
- Meldung: "Keine oeffentlichen Aenderungen seit [Version/Datum]"
- Interne Commits (chore, style, test) erwaehnen

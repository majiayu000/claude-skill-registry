---
name: gemini-headless
description: Delegiere Aufgaben an Gemini CLI im Headless-Mode. Nutze fuer Dokumentation, Code-Reviews, Analysen oder wenn der User /gemini aufruft. Nutzt Google Subscription (KEIN API Key). Auto-Accept mit -y Flag.
---

# Gemini Headless Mode

## Overview
Dieser Skill ermoeglicht die Nutzung von Gemini CLI fuer delegierbare Aufgaben.
Gemini laeuft im Headless-Mode mit `-y` Flag (keine Bestaetigungen).

**WICHTIG: Nutzt Google Subscription (Gemini Advanced), KEINEN API Key!**

## Quick Start
```bash
gemini -y -p "Deine Aufgabe hier"
```

## Authentifizierung (Subscription)

**IMMER Google Login nutzen (Subscription), NIEMALS API Key!**

```bash
# Erster Login (einmalig, oeffnet Browser)
gemini login

# Status pruefen
gemini auth status
```

Nach dem Login ist die Subscription aktiv und es werden keine API-Kosten berechnet.

## Core Instructions

### Wann Gemini nutzen
- Dokumentationserstellung (.md, README, etc.)
- Code-Reviews und Analysen
- Textgenerierung und Zusammenfassungen
- Wenn der User explizit `/gemini` aufruft

### Standard-Workflow
1. **Aufgabe verstehen**: Was soll Gemini tun?
2. **Kontext sammeln**: Relevante Dateien identifizieren
3. **Prompt konstruieren**: Aufgabe + Kontext zusammenfuehren
4. **Gemini ausfuehren**: Via Bash mit `-y` Flag
5. **Output verarbeiten**: Ergebnis in Datei schreiben/anzeigen

### Bash-Commands

**Einfache Aufgabe:**
```bash
gemini -y -p "Erstelle eine README.md fuer dieses Projekt"
```

**Mit Datei-Kontext (via Stdin):**
```bash
cat src/main.ts | gemini -y -p "Erklaere diesen Code und erstelle Dokumentation"
```

**Mit Verzeichnis-Kontext:**
```bash
gemini -y -p "Analysiere die Architektur" --include-directories ./src,./docs
```

**Output in Datei speichern:**
```bash
gemini -y -p "Erstelle eine API-Dokumentation" > docs/api.md
```

**Mehrere Dateien als Kontext:**
```bash
cat file1.ts file2.ts | gemini -y -p "Vergleiche diese Implementierungen"
```

## Examples

### Beispiel 1: README erstellen
```bash
cat CLAUDE.md package.json | gemini -y -p "Erstelle eine kurze README.md fuer dieses Projekt. Fokus auf Installation und Quick Start."
```

### Beispiel 2: Code dokumentieren
```bash
cat src/services/auth.service.ts | gemini -y -p "Erstelle JSDoc Kommentare fuer alle oeffentlichen Methoden"
```

### Beispiel 3: Code-Review
```bash
git diff HEAD~1 | gemini -y -p "Review diese Aenderungen. Finde Bugs, Security-Issues, Best-Practice-Verstoesse"
```

### Beispiel 4: Context-Datei generieren
```bash
gemini -y -p "Erstelle eine context.md Datei die das Projekt beschreibt" --include-directories ./src
```

## Wichtige Flags

| Flag | Beschreibung |
|------|--------------|
| `-y` | **PFLICHT** - Auto-Accept aller Aktionen |
| `-p "..."` | **PFLICHT** - Prompt im Headless-Mode |
| `--include-directories` | Verzeichnisse als Kontext |
| `-m gemini-2.5-flash` | Schnelleres Modell (optional) |
| `--output-format json` | Fuer programmatisches Parsing |

## Installation

```bash
npm install -g @google/gemini-cli
# oder
brew install gemini-cli
```

## WICHTIG: Keine API Keys!

**FALSCH (API Key):**
```bash
# NICHT VERWENDEN!
export GOOGLE_API_KEY="..."
```

**RICHTIG (Subscription):**
```bash
# Google Login nutzen
gemini login
```

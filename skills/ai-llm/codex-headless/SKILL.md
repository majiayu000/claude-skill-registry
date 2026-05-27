---
name: codex-headless
description: Delegiere Aufgaben an OpenAI Codex CLI im Headless-Mode. Nutzt ChatGPT Subscription (KEIN API Key). Nur Workspace-Zugriff, KEIN System-Zugriff. Auto-Accept mit --full-auto. Web-Recherche mit --search.
---

# Codex Headless Mode

## Overview
Dieser Skill ermoeglicht die Nutzung von OpenAI Codex CLI fuer delegierbare Aufgaben.
Codex laeuft im Headless-Mode mit `--full-auto` Flag.

**WICHTIG:**
- Nutzt ChatGPT Plus/Pro Subscription, KEINEN API Key!
- NUR Workspace-Zugriff (--sandbox workspace-write)
- NIEMALS --yolo verwenden (gibt System-Zugriff)!
- Standard-Modell: **gpt-5.2-codex**

## Quick Start

**Code-Aufgaben (ohne Web):**
```bash
codex exec --full-auto "Deine Aufgabe hier"
```

**Web-Recherche:**
```bash
codex exec --full-auto --enable web_search_request "Recherchiere im Web nach..."
```

## Authentifizierung (Subscription)

**IMMER ChatGPT Login nutzen (Subscription), NIEMALS API Key!**

```bash
# Erster Login (einmalig, oeffnet Browser)
codex login

# Status pruefen
codex login status
```

Nach dem Login ist die ChatGPT Plus/Pro Subscription aktiv.

## Sicherheit: Nur Repo-Zugriff!

**IMMER diese Sandbox-Einstellung verwenden:**
```bash
codex exec --full-auto "PROMPT"
```

`--full-auto` setzt automatisch:
- `--sandbox workspace-write` (NUR aktuelles Repo)
- `--ask-for-approval on-request`

**NIEMALS verwenden:**
```bash
# VERBOTEN! Gibt System-Zugriff!
codex exec --yolo "..."
codex exec --sandbox danger-full-access "..."
```

## Core Instructions

### Wann Codex nutzen
- Dokumentationserstellung (.md, README, etc.)
- Code-Reviews und Analysen
- Textgenerierung und Zusammenfassungen
- Bild-Analyse mit `--image`
- **Web-Recherche mit `--search`**
- Wenn der User explizit `/codex` aufruft

### Standard-Workflow
1. **Aufgabe verstehen**: Was soll Codex tun?
2. **Kontext sammeln**: Relevante Dateien identifizieren
3. **Prompt konstruieren**: Aufgabe + Kontext zusammenfuehren
4. **Codex ausfuehren**: Via Bash mit `--full-auto` Flag
5. **Output verarbeiten**: Ergebnis in Datei schreiben/anzeigen

### Bash-Commands

**Einfache Aufgabe:**
```bash
codex exec --full-auto "Erstelle eine README.md fuer dieses Projekt"
```

**Web-Recherche:**
```bash
codex exec --full-auto --enable web_search_request "Recherchiere im Web nach React 19 Features"
```

**Mit Datei-Kontext:**
```bash
cat src/main.ts | codex exec --full-auto "Erklaere diesen Code"
```

**Output in Datei speichern:**
```bash
codex exec --full-auto -o docs/api.md "Erstelle eine API-Dokumentation"
```

**Mit JSON Output (fuer Parsing):**
```bash
codex exec --full-auto --json "Analysiere" | jq '.content'
```

**Mit Bild-Input:**
```bash
codex exec --full-auto -i screenshot.png "Beschreibe was du auf diesem Bild siehst"
```

**Einfache Schreibaufgabe (schneller, guenstiger):**
```bash
codex exec --full-auto -m gpt-5.1-codex-mini "Erstelle README.md"
```

**Session fortsetzen:**
```bash
codex exec resume --last
```

**Alle Sessions auflisten:**
```bash
codex resume --all
```

## Examples

### Beispiel 1: README erstellen
```bash
codex exec --full-auto "Erstelle eine kurze README.md fuer dieses Projekt"
```

### Beispiel 2: Code dokumentieren
```bash
cat src/services/auth.service.ts | codex exec --full-auto "Erstelle JSDoc Kommentare"
```

### Beispiel 3: Code-Review
```bash
git diff HEAD~1 | codex exec --full-auto "Review diese Aenderungen"
```

### Beispiel 4: Bild analysieren
```bash
codex exec --full-auto -i ui-mockup.png "Implementiere dieses UI Design"
```

## Erlaubte Flags

### Haupt-Flags
| Flag | Beschreibung |
|------|--------------|
| `exec` | **PFLICHT** - Non-Interactive Mode |
| `--full-auto` | **PFLICHT** - Auto-Accept mit Workspace-Sandbox |

### Output-Flags
| Flag | Beschreibung |
|------|--------------|
| `--json` | JSON Lines Output (NDJSON) |
| `-o, --output-last-message <path>` | Letzte Antwort in Datei |
| `--output-schema <path>` | JSON Schema Validierung |
| `--color <mode>` | ANSI-Farben (always/never/auto) |

### Kontext-Flags
| Flag | Beschreibung |
|------|--------------|
| `-i, --image <path>` | Bild(er) an Prompt anhaengen |

### Konfigurations-Flags
| Flag | Beschreibung |
|------|--------------|
| `-m, --model <name>` | Modell waehlen (siehe Modellauswahl) |
| `-c, --config key=value` | Konfiguration inline |

## Modellauswahl

| Aufgabentyp | Modell | Flag |
|-------------|--------|------|
| **Komplexe Aufgaben** (Code, Analyse, Recherche) | `gpt-5.2-codex` | Standard (kein Flag) |
| **Einfache Schreibaufgaben** (README, Doku, Text) | `gpt-5.1-codex-mini` | `-m gpt-5.1-codex-mini` |

### Session-Flags
| Flag | Beschreibung |
|------|--------------|
| `codex exec resume <ID>` | Session fortsetzen |
| `codex exec resume --last` | Letzte Session |
| `codex resume --all` | Alle Sessions listen |

## VERBOTENE Flags (geben System-Zugriff!)

| Flag | Warum verboten |
|------|----------------|
| `--yolo` | Deaktiviert ALLE Sicherheiten |
| `--sandbox danger-full-access` | Gibt Vollzugriff auf System |
| `--ask-for-approval never` | Keine Rueckfragen bei gefaehrlichen Aktionen |
| `--add-dir /` | Wuerde Root-Zugriff geben |

## Installation

```bash
npm install -g @openai/codex
# oder
brew install --cask codex
```

## WICHTIG: Keine API Keys!

**FALSCH (API Key):**
```bash
# NICHT VERWENDEN!
export OPENAI_API_KEY="sk-..."
printenv OPENAI_API_KEY | codex login --with-api-key
```

**RICHTIG (Subscription):**
```bash
# ChatGPT Login nutzen
codex login
```

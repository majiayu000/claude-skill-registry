---
name: verify-tasks
description: "Verify completed tasks with Playwright browser testing. Run after completing implementation tasks to check for JS errors, hydration issues, and UX problems. Use when: tasks are completed, user says 'verify', 'teste die aenderungen', 'pruefe ob es funktioniert'."
---

# Verify Tasks Skill

Automatisiertes Browser-Testing mit Playwright MCP nach Abschluss von Implementation-Tasks.

## Wann ausfuehren

- Nach Abschluss aller Tasks in einer Session
- Wenn User explizit "verify", "teste", oder "pruefe" sagt
- Vor dem Deployment um Fehler fruehzeitig zu erkennen

## Voraussetzungen

1. **Dev Server muss laufen**
   ```bash
   yarn dev
   ```
   - Falls nicht: Server im Hintergrund starten
   - Warten bis Server auf http://localhost:4321 erreichbar ist

2. **Playwright MCP muss verfuegbar sein**
   - Tools: `mcp__playwright__browser_navigate`, `mcp__playwright__browser_console_messages`, etc.

## Test-Ablauf

### 1. Dev Server pruefen/starten

```bash
# Pruefen ob Server laeuft
curl -s -o /dev/null -w "%{http_code}" http://localhost:4321 || yarn dev &
```

### 2. Betroffene Seiten identifizieren

Aus den abgeschlossenen Tasks die relevanten URLs ableiten:
- ContactForm.tsx geaendert → `/kontakt`, `/bestellen`
- Youtube.tsx geaendert → `/ressourcen/videoanleitungen`
- Plan.astro geaendert → `/preise`
- Base.astro geaendert → Alle Seiten (Startseite genuegt)

### 3. Pro Seite testen

Fuer jede betroffene URL:

**a) Seite navigieren**
```
mcp__playwright__browser_navigate: url=http://localhost:4321{path}
```

**b) Console-Errors pruefen**
```
mcp__playwright__browser_console_messages: level=error
```
- Keine Errors = OK
- Hydration Errors = FAIL
- 400/500 Errors = FAIL
- Externe Service-Errors (tawk.to, etc.) = WARNUNG (nicht kritisch)

**c) Snapshot pruefen (optional)**
```
mcp__playwright__browser_snapshot
```
- Visuelle Pruefung ob Elemente korrekt gerendert wurden

### 4. Spezifische Tests je nach Task

| Task | Test |
|------|------|
| Hydration Fix | Console auf "Hydration" oder "Error #418" pruefen |
| Submit-Button Spinner | Formular absenden, Spinner sichtbar? |
| Cursor Styling | Snapshot pruefen, Features nicht klickbar |
| YouTube Fix | Video-Tab wechseln, kein Error |
| Usercentrics | Keine 400-Fehler fuer autoblocker.js |

### 5. Ergebnis-Report

Nach allen Tests:

**Erfolgreich:**
```
Alle {n} Tests bestanden:
- /kontakt: Keine Console-Errors
- /preise: Keine Console-Errors
- /ressourcen/videoanleitungen: Keine Console-Errors
```

**Fehlgeschlagen:**
```
{n} von {m} Tests fehlgeschlagen:

FAIL: /kontakt
  - Error: Hydration failed because...

OK: /preise
  - Keine Errors

Empfehlung: {Konkreter Fix-Vorschlag}
```

## Playwright MCP Tools Referenz

- `mcp__playwright__browser_navigate` - Seite aufrufen
- `mcp__playwright__browser_console_messages` - Console-Logs abrufen
- `mcp__playwright__browser_snapshot` - DOM-Snapshot fuer visuelle Pruefung
- `mcp__playwright__browser_click` - Element klicken
- `mcp__playwright__browser_fill_form` - Formular ausfuellen
- `mcp__playwright__browser_close` - Browser schliessen

## Wichtige Regeln

- **Dev Server** muss laufen (localhost:4321)
- **Timeout** von 10 Sekunden pro Seite
- **Externe Fehler** (Tawk.to, externe APIs) sind Warnungen, keine Fails
- **Usercentrics-Fehler** fuer Services sind ok (Consent nicht gegeben)
- Nach Tests: Browser mit `browser_close` schliessen

## Typische Nutzung

User: `/verify-tasks`
oder: "teste ob die aenderungen funktionieren"
oder: "pruefe die seiten mit playwright"

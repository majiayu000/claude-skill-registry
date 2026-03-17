---
name: fix-bug
description: Strukturierter Bug-Fix-Workflow für die Speicher Analyse Tauri-App (React + Vite Frontend). Liest offene Issues, führt Tiefenanalyse durch, implementiert den Fix, aktualisiert das Änderungsprotokoll und schließt den Kreislauf. Aufruf mit /fix-bug [bug-beschreibung oder issue-referenz].
---

# Bug-Fix-Workflow

Du behebst einen Bug in der Speicher Analyse Tauri-App. **Das Problem liegt IMMER im Quellcode.**

## Argument

`$ARGUMENTS` = Bug-Beschreibung ODER Verweis auf ein Issue in `docs/issues/issue.md`

## Phase 1: Issue & Kontext erfassen

1. **Issue-Tracker prüfen:** Lies `docs/issues/issue.md`
2. **Git-Historie prüfen:** `git log --oneline -10` und `git diff`
3. **Betroffene Module identifizieren:** Welche Dateien sind involviert?

## Phase 2: Tiefenanalyse (OBERSTE DIREKTIVE)

Verfolge den vollständigen Datenfluss durch alle Schichten:

```
React-View (src/views/*.tsx)
  → API-Aufruf (import { foo } from '../api/tauri-api')
    → tauri-api.ts: invoke('command_name', { params })
      → Tauri-Command (src-tauri/src/commands/cmd_*.rs)
        → PowerShell (src-tauri/src/ps.rs)
          → Rückweg: JSON → commands/ → tauri-api.ts → React-State → JSX
```

**Prüfe zusätzlich:**
- CSS-Regeln in `src/style.css`
- React State + useEffect Dependencies
- useEffect Cleanup (Timer, Listener, Observer)
- Property-Namen: Backend vs. Frontend (z.B. `name`/`detail` vs. `label`/`message`)
- PowerShell-Escaping und UTF-8-Encoding

## Phase 3: Fix implementieren

1. **Minimaler Fix:** Nur die Wurzelursache beheben, kein Refactoring
2. **Security beachten:**
   - PowerShell-Parameter escapen: `.replace("'", "''")`
   - Pfade vom Frontend validieren
   - Kein `dangerouslySetInnerHTML` (JSX escaped automatisch)
3. **React-Konventionen einhalten:**
   - Async/Await mit try/catch
   - State-Updates über `useState` Setter
   - Side-Effects in `useEffect` mit Cleanup-Return
   - Deutsche UI-Texte mit korrekten Umlauten
4. **Keine Zwischenlösungen:** Fix muss ohne User-Aktion wirken

## Phase 4: Verifizierung

1. **Datenfluss nochmal durchgehen**
2. **Seiteneffekte prüfen:** Könnte der Fix andere Features beeinträchtigen?
3. **Edge Cases:** Leere Daten, Fehler, Timeouts
4. **Visuell prüfen:** `/visual-verify` bei UI-Änderungen (PFLICHT)

## Phase 5: Dokumentation

1. **Git Commit:** `git add . && git commit -m "fix: <Beschreibung>" && git push`
2. **Änderungsprotokoll:** `/changelog fix <Beschreibung>`
3. **Issue aktualisieren:** Status auf "In Prüfung" (NICHT erledigt — nur Simon darf das)

## Ausgabeformat

```markdown
## Bug-Fix: [Titel]

### Symptom
Was der User sieht/erlebt

### Wurzelursache
Die ECHTE Ursache im Code (mit Datei:Zeile)

### Fix
Was geändert wurde (mit Datei:Zeile)

### Geänderte Dateien
- datei.rs:123 - Beschreibung
- datei.tsx:456 - Beschreibung

### Risiko-Bewertung
Welche anderen Features könnten betroffen sein
```

## Verbotene Aussagen

- "Bitte F5 drücken" / "Bitte die App neu starten"
- "Bei mir funktioniert es" / "Der Code sieht korrekt aus"
- "Das sollte jetzt funktionieren" (ohne Beweis)

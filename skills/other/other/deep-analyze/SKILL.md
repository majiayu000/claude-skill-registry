---
name: deep-analyze
description: Tiefenanalyse eines Problems gemäß der OBERSTEN DIREKTIVE. Verfolgt den vollständigen Datenfluss React-View→tauri-api.ts→invoke→commands/→ps.rs und identifiziert die Wurzelursache. Aufruf mit /deep-analyze [problem-beschreibung oder datei-pfad].
---

# Tiefenanalyse (OBERSTE DIREKTIVE)

Du führst eine akribische Tiefenanalyse durch. **Das Problem liegt IMMER im Quellcode.**

## Argument

`$ARGUMENTS` = Problembeschreibung ODER Dateipfad zum Analysieren

## Verbotene Aussagen

Du darfst NIEMALS sagen:
- "Bitte F5 drücken" / "Bitte die App neu starten"
- "Bei mir funktioniert es" / "Der Code sieht korrekt aus"
- "Das sollte jetzt funktionieren" (ohne Beweis)
- Jede Form von "der User muss etwas tun damit es funktioniert"

## Analyse-Protokoll

### Phase 1: Kontext sammeln

1. **Issue-Tracker prüfen:** Lies `docs/issues/issue.md` — gibt es verwandte Issues?
2. **Betroffene Dateien identifizieren:** Welche Module sind involviert?
3. **Letzte Änderungen prüfen:** `git log --oneline -20` und `git diff` für relevante Dateien

### Phase 2: Vollständiger Datenfluss-Trace (Tauri v2 + React)

Verfolge den Datenfluss **Schritt für Schritt** durch alle Schichten:

```
1. React-View (src/views/*.tsx)
   → Welche Komponente / welcher useEffect löst das Problem aus?
   → Welche API-Funktion wird aufgerufen?
   → Welcher State wird gesetzt?

2. API-Bridge (src/api/tauri-api.ts)
   → Ist die Funktion korrekt typisiert und exportiert?
   → Stimmt der invoke-Command-Name (snake_case)?
   → Werden Parameter korrekt als Objekt übergeben?

3. Tauri-Command (src-tauri/src/commands/cmd_*.rs)
   → Ist der #[tauri::command] korrekt definiert?
   → Sind Parameter-Typen korrekt (camelCase → snake_case Mapping)?
   → Werden Parameter escaped (PowerShell-Injection)?
   → Ist der Command in lib.rs registriert?

4. PowerShell-Ausführung (src-tauri/src/ps.rs)
   → Wird run_ps() / run_ps_json() verwendet?
   → Hat der Aufruf einen Timeout?
   → Ist das PowerShell-Script korrekt (Syntax, UTF-8)?

5. Rückweg: ps.rs → commands/ → tauri-api.ts → React-State → JSX-Rendering
   → Wird das Ergebnis korrekt als JSON zurückgegeben?
   → Kommt es im Frontend an (Promise resolved)?
   → Stimmen die Property-Namen? (Backend liefert z.B. `name`/`detail`, nicht `label`/`message`)
   → Wird der React-State korrekt aktualisiert?
```

### Phase 3: React State-Management-Analyse

1. **useState/useEffect:** Werden Dependencies korrekt angegeben?
2. **Cleanup:** Haben useEffects mit Timer/Listener korrekte Cleanup-Returns?
3. **Re-Renders:** Verursachen State-Updates unnötige Re-Renders?
4. **Async State:** Wird State nach einem abgebrochenen/veralteten Request noch gesetzt? (Race Condition)

### Phase 4: Security-Analyse (bei sicherheitsrelevanten Problemen)

1. **Command Injection:** `format!()` ohne `.replace("'", "''")`?
2. **XSS:** `dangerouslySetInnerHTML` mit ungeprüften Daten?
3. **Path Traversal:** Pfade ohne Validierung an Dateioperationen?
4. **CSP:** Content Security Policy in `tauri.conf.json` konfiguriert?

### Phase 5: Plattform-Analyse (falls relevant)

1. **Windows-spezifisch:** Registry, PowerShell, Dateipfade (Backslashes)
2. **Tauri-spezifisch:** CSP, Capabilities, withGlobalTauri
3. **WebView-spezifisch:** WebView2-Einschränkungen

### Phase 6: CSS & UI-Analyse (falls visuelles Problem)

1. **CSS-Variablen:** Stimmen die Werte in `src/style.css`?
2. **Theme-Konflikte:** Dark/Light Theme korrekt implementiert?
3. **WCAG-Kontrast:** Text-auf-Hintergrund mindestens 4.5:1?

### Phase 7: PowerShell-Analyse (falls PS involviert)

1. Wird `crate::ps::run_ps()` verwendet?
2. Werden Parameter VOR dem `format!()` escaped?
3. Gibt es einen Timeout?
4. Multi-Line: Werden Newlines beibehalten?

## Ausgabeformat

```markdown
## Tiefenanalyse: [Problem-Titel]

### Symptom
Was der User sieht/erlebt

### Datenfluss-Trace
Schritt-für-Schritt Pfad durch den Code mit Datei:Zeile Referenzen

### Wurzelursache
Die ECHTE Ursache im Code (mit Datei:Zeile)

### Betroffene Dateien
- datei.rs:123 - Beschreibung
- datei.tsx:456 - Beschreibung

### Vorgeschlagener Fix
Konkreter Code-Vorschlag

### Verwandte Risiken
Was könnte durch den Fix brechen?
```

## Wichtige Hinweise

- **Visuelles Ergebnis ist die Wahrheit.** Nicht der Code, nicht die Theorie.
- **Einmal melden reicht.** Der User darf das gleiche Problem nie zweimal melden müssen.
- **Keine Zwischenlösungen.** Der Code muss sich selbst korrigieren.
- **Beweislast liegt bei der KI.** Nicht beim User.
- **Verwandte Skills:** Nach der Analyse kann `/fix-bug` für die Umsetzung verwendet werden.

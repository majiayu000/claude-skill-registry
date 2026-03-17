---
name: test-issue
description: Strukturiertes Testen eines Issues via Puppeteer. Liest die Issue-Anforderungen, definiert testbare Kriterien, testet jedes einzeln mit Beweis (Screenshot + Daten), berichtet Pass/Fail. Nutze diesen Skill IMMER wenn ein Issue getestet werden soll. Aufruf mit /test-issue [issue-nummer oder beschreibung].
---

# Issue testen (Puppeteer)

Du testest ein Issue aus `docs/issues/issue.md` strukturiert und mit Beweis. **Kein Test ohne Beweis. Kein "PASS" ohne Screenshot.**

## Argument

`$ARGUMENTS` = Issue-Nummer (z.B. "#4") ODER Beschreibung

## VERBOTEN

- **NIEMALS** ein Issue als "BESTANDEN" melden ohne JEDE einzelne Anforderung geprüft zu haben
- **NIEMALS** mehrere Issues in einem Durchlauf "schnell abhaken"
- **NIEMALS** Backend-Code als Beweis verwenden — nur das Frontend (Puppeteer) zählt
- **NIEMALS** Kontrastprüfungen mathematisch erledigen — `/visual-verify` verwenden

## Phase 1: Anforderungen extrahieren

1. **Issue lesen:** `docs/issues/issue.md` → das betreffende Issue finden
2. **Testbare Kriterien ableiten:** Jeder Punkt unter "Was Simon testen soll" wird zu einem einzelnen Testfall
3. **Kriterien-Tabelle erstellen:**

```markdown
| # | Kriterium | Wie testen | Status |
|---|-----------|-----------|--------|
| 1 | Dashboard zeigt Zahlen nach Neustart | Screenshot Dashboard, Zahlen sichtbar? | OFFEN |
| 2 | Verzeichnisbaum mit Grössen | Screenshot Explorer, Grössen sichtbar? | OFFEN |
```

## Phase 2: Einzeltest pro Kriterium

Für JEDES Kriterium:

1. **Vorbereitung:** Richtigen View/Tab öffnen via Puppeteer
2. **Aktion durchführen:** (z.B. Button klicken, scrollen, warten)
3. **Screenshot machen:** Beweisfoto
4. **Daten extrahieren:** Relevante Texte/Zahlen aus dem DOM lesen
5. **Bewertung:** BESTANDEN / DURCHGEFALLEN / TEILWEISE — mit Begründung
6. **Bei visuellem Test:** `/visual-verify` Sub-Skill aufrufen

## Phase 3: Visuelle Qualität prüfen

Für JEDEN getesteten View zusätzlich prüfen (via `/visual-verify`):
- Ist der Text gut lesbar?
- Stimmen die Farben/Kontraste?
- Gibt es abgeschnittenen Text?
- Sind Buttons/Links erkennbar?

## Phase 4: Bericht

```markdown
## Test-Bericht: Issue #[N] — [Titel]

### Zusammenfassung
- Getestete Kriterien: X
- Bestanden: Y
- Durchgefallen: Z

### Einzelergebnisse
| # | Kriterium | Ergebnis | Beweis |
|---|-----------|----------|--------|
| 1 | Dashboard zeigt Zahlen | BESTANDEN | [screenshot-1.png]: 1.5 TB, 20.9 GB, 13.425 Dateien sichtbar |
| 2 | Grössen im Explorer | DURCHGEFALLEN | [screenshot-2.png]: Spalte "Grösse" ist leer |

### Gefundene Probleme
| # | Problem | Schwere | Screenshot |
|---|---------|---------|------------|
| 1 | Grössen fehlen bei Ordner X | Hoch | [zoom-1.png] |

### Visuelle Qualität
Ergebnis von `/visual-verify` hier einfügen.
```

## Phase 5: Issue-Datei aktualisieren

1. **Bei BESTANDEN:** Status auf "Getestet via Puppeteer — wartet auf Simons Bestätigung"
2. **Bei DURCHGEFALLEN:** Gefundene Probleme als Unterpunkte zum Issue hinzufügen
3. **NIEMALS** ein Issue als "erledigt" markieren — nur Simon darf das

## Sub-Agent-Delegation

Mehrere Issues können parallel getestet werden:
```
Task(subagent_type="general-purpose", prompt="Führe /test-issue #4 aus...")
Task(subagent_type="general-purpose", prompt="Führe /test-issue #19 aus...")
```

## Hinweise

- **App muss laufen** mit CDP-Port 9222 (Tauri/WebView2: `$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS='--remote-debugging-port=9222'; cargo tauri dev`)
- **Puppeteer-Verbindung:** `puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' })`
- **`page.click()` hängt** → immer `page.evaluate(() => el.click())` verwenden
- **Puppeteer-Scripts** liegen in `tools/wcag/` (dort ist puppeteer-core installiert)
- **Verwandte Skills:** `/visual-verify` für Sichtprüfung, `/fix-bug` für gefundene Probleme

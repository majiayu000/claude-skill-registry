# E2E Testing Skill

## Trigger

- Keywords: `teste`, `e2e`, `playwright`, `browser test`, `visual test`, `smoke test`
- Aufruf: `/e2e-test [suite] [--flags]`

## Beschreibung

Automatisierter E2E-Test mit menschlichem Verhalten für Preview und Production.
Nutzt Chrome MCP oder Playwright MCP für Browser-Automatisierung.

## Test-Suiten

| Suite      | Dauer | Beschreibung                                  |
| ---------- | ----- | --------------------------------------------- |
| `smoke`    | 30s   | Login, Upload, Basis-UI (Default bei "teste") |
| `full`     | 5min  | Alle P0+P1 Szenarien                          |
| `visual`   | 2min  | Nur Screenshot-Vergleiche                     |
| `upload`   | 1min  | Alle Dateiformate                             |
| `download` | 2min  | Export-Funktionen                             |
| `login`    | 30s   | Auth Flow                                     |
| `api`      | 1min  | API-Endpoint Tests                            |

## Flags

| Flag                 | Beschreibung                           |
| -------------------- | -------------------------------------- |
| `--preview`          | Nur localhost testen                   |
| `--production`       | Nur Production-URL testen              |
| `--quick`            | Nur P0-Szenarien (schnellster Test)    |
| `--human`            | Chrome MCP mit echtem Browser          |
| `--headless`         | Playwright MCP headless (CI/CD)        |
| `--update-baselines` | Screenshot-Baselines aktualisieren     |
| `--mobile`           | Mobile Viewports testen (375px, 768px) |

## Workflow

```
1. UMGEBUNGS-CHECK
   - Prüfe ob localhost läuft (curl/fetch)
   - Prüfe ob Production-URL erreichbar
   - Wähle Test-Umgebung basierend auf Flags

2. BROWSER-SETUP
   - Wenn --human: Nutze Chrome MCP (mcp__claude-in-chrome__)
   - Sonst: Nutze Playwright MCP (mcp__playwright__)
   - Viewport: 1280x720 (Desktop) oder 375x667 (Mobile)

3. HUMAN BEHAVIOR AKTIVIEREN
   - Randomisierte Delays: 200-800ms zwischen Aktionen
   - Typing-Speed: 50-150ms pro Taste
   - Hover vor Click (200-500ms Pause)
   - Smooth Scroll statt instant

4. TEST-SUITE AUSFÜHREN
   - Für jeden Test: Screenshot vorher/nachher
   - Bei Fehler: Screenshot + Console Logs speichern
   - Download-Verifizierung: Dateigröße prüfen

5. REPORT GENERIEREN
   - Markdown-Report in .playwright-mcp/reports/
   - Diff-Images bei visuellen Abweichungen
   - Zusammenfassung mit Pass/Fail/Flaky Status
```

## Test-Szenarien (P0 - Geschäftskritisch)

### 1. Landing Page Load

```
- Navigiere zu URL
- Warte auf Hauptelement sichtbar
- Prüfe Logo/Branding sichtbar
- Screenshot: landing-page.png
```

### 2. Login/Auth Flow

```
- Klicke auf Login Button
- Warte auf Modal/Page-Animation
- Prüfe Auth-Optionen sichtbar (OAuth, Email, etc.)
- Screenshot: login-modal.png
```

### 3. Sprache umschalten (wenn i18n)

```
- Finde Language Toggle
- Klicke mit Human Delay
- Warte auf Text-Änderung
- Verifiziere UI-Texte geändert
- Screenshot: language-toggle.png
```

### 4. Datei Upload (wenn vorhanden)

```
- Klicke auf Upload-Bereich
- Wähle Testdatei
- Warte auf Bestätigung
- Prüfe Dateiname angezeigt
- Screenshot: file-uploaded.png
```

### 5. Hauptaktion ausführen

```
- Führe primäre App-Funktion aus
- Warte auf Loading-State
- Warte auf Ergebnis (max 60s)
- Prüfe Ergebnis-Inhalt vorhanden
- Screenshot: result.png
```

### 6. Export/Download (wenn vorhanden)

```
- Klicke Download Button
- Warte auf Download-Event
- Verifiziere Dateiformat korrekt
- Verifiziere Dateigröße > Minimum
- Screenshot: download-complete.png
```

## Test-Szenarien (P1 - Wichtig)

### 7. Navigation/History

```
- Klicke auf Navigation-Element
- Warte auf Animation
- Prüfe korrekter Content geladen
```

### 8. Theme Toggle (wenn vorhanden)

```
- Finde Theme-Toggle
- Notiere aktuelle Farben
- Klicke Toggle
- Verifiziere Farben geändert
- Screenshot: theme-toggle.png
```

### 9. Responsive Design

```
- Setze Viewport auf 375x667
- Prüfe Mobile-Navigation sichtbar
- Prüfe Hauptfunktionen erreichbar
- Screenshot: mobile-view.png
```

### 10. Error Handling

```
- Provoziere Fehler (ungültige Eingabe)
- Warte auf Error-Message
- Prüfe Error ist benutzerfreundlich
- Screenshot: error-state.png
```

## Human Behavior Functions

```typescript
// Randomisierter Delay (200-800ms)
async function humanDelay() {
  const delay = 200 + Math.random() * 600;
  await page.waitForTimeout(delay);
}

// Menschliches Tippen (50-150ms pro Taste)
async function humanType(selector: string, text: string) {
  await page.click(selector);
  await humanDelay();
  for (const char of text) {
    await page.keyboard.type(char);
    await page.waitForTimeout(50 + Math.random() * 100);
  }
}

// Hover -> Pause -> Click Pattern
async function humanClick(selector: string) {
  await page.hover(selector);
  await page.waitForTimeout(200 + Math.random() * 300);
  await page.click(selector);
  await humanDelay();
}

// Smooth Scroll
async function humanScroll(pixels: number) {
  await page.evaluate((px) => {
    window.scrollTo({ top: px, behavior: "smooth" });
  }, pixels);
  await page.waitForTimeout(500);
}
```

## Report-Format

```markdown
## E2E Test Report - [DATUM] [UHRZEIT]

### Umgebung

- **URL**: [getestete URL]
- **Browser**: Chromium [version]
- **Viewport**: 1280x720
- **Suite**: smoke

### Ergebnisse

| #   | Test              | Status  | Dauer | Screenshot              |
| --- | ----------------- | ------- | ----- | ----------------------- |
| 1   | Landing Page Load | PASS    | 0.8s  | [view](landing-page.png)|
| 2   | Login Modal       | PASS    | 1.2s  | [view](login-modal.png) |
| 3   | File Upload       | PASS    | 2.1s  | [view](file-uploaded.png)|
| 4   | Main Action       | SLOW    | 45.2s | [view](result.png)      |
| 5   | Download          | FAIL    | 3.4s  | [view](error.png)       |

### Zusammenfassung

- **Gesamt**: N Tests
- **Passed**: X (Y%)
- **Failed**: A (B%)
- **Slow/Flaky**: C (D%)
- **Dauer**: Zs
```

## Visuelle Baselines

```
.playwright-mcp/
├── baselines/                    # Goldene Referenz (git-tracked)
│   ├── landing-page-desktop.png
│   ├── landing-page-mobile.png
│   ├── login-modal.png
│   ├── result.png
│   └── error-state.png
├── current/                      # Aktuelle Screenshots (gitignored)
├── diffs/                        # Pixel-Differenzen (gitignored)
└── reports/                      # Test-Reports (gitignored)
```

## Ausführung

### Einfachster Aufruf

```
User: "teste"
-> Führt smoke-Suite auf verfügbarer Umgebung aus
```

### Spezifische Tests

```
User: "teste upload"
-> Führt nur Upload-Suite aus

User: "teste production visual"
-> Führt Visual-Suite auf Production aus

User: "teste --quick --human"
-> Schnelltest mit echtem Chrome Browser
```

### CI/CD Integration

```
User: "teste --headless --full"
-> Alle Tests headless für Pipeline
```

## Fehlerbehandlung

1. **Localhost nicht erreichbar**:

   - Warnung anzeigen
   - Frage ob Dev-Server gestartet werden soll

2. **Production nicht erreichbar**:

   - Warnung anzeigen
   - Prüfe Deployment-Status

3. **Test-Timeout (>60s)**:

   - Screenshot des aktuellen Zustands
   - Console Logs speichern
   - Als FAIL markieren

4. **Visueller Diff erkannt**:
   - Diff-Image generieren
   - Als FLAKY markieren (nicht automatisch FAIL)
   - User entscheidet ob Baseline-Update nötig

## Konfiguration

Optionale `.e2e-config.json` im Projekt-Root:

```json
{
  "previewUrl": "http://localhost:5173",
  "productionUrl": "https://your-app.com",
  "defaultSuite": "smoke",
  "timeouts": {
    "navigation": 10000,
    "action": 60000,
    "download": 30000
  },
  "viewports": {
    "desktop": { "width": 1280, "height": 720 },
    "tablet": { "width": 768, "height": 1024 },
    "mobile": { "width": 375, "height": 667 }
  },
  "humanBehavior": {
    "enabled": true,
    "minDelay": 200,
    "maxDelay": 800,
    "typingSpeed": { "min": 50, "max": 150 }
  },
  "screenshots": {
    "onEveryStep": false,
    "onFailure": true,
    "fullPage": false
  }
}
```

## Voraussetzungen

- Chrome MCP oder Playwright MCP installiert
- Node.js Projekt mit `package.json`
- Optional: `.e2e-config.json` für Projekt-Konfiguration

## Autor

Dresden AI Insights - https://dresdenaiinsights.com

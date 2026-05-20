---
name: visual-verify
description: Visuelle Verifikation via Puppeteer. Erzwingt echte Sichtprüfung statt theoretischer Code-Analyse. Nimmt Screenshots, analysiert gerenderte Elemente, prüft Kontrast/Layout/Lesbarkeit visuell. Nutze diesen Skill IMMER wenn du behaupten willst dass etwas "funktioniert" oder "gut aussieht". Aufruf mit /visual-verify [view-name oder css-selektor].
---

# Visuelle Verifikation (Puppeteer)

Du verifizierst visuell ob ein UI-Element, ein View oder eine Änderung korrekt dargestellt wird. **Visuelles Ergebnis ist die Wahrheit — nicht Code, nicht Mathe, nicht Theorie.**

## Argument

`$ARGUMENTS` = View-Name (z.B. "optimizer", "network", "privacy") ODER CSS-Selektor ODER "all"

## VERBOTEN

- **NIEMALS** "PASS" sagen ohne jeden einzelnen sichtbaren Text visuell geprüft zu haben
- **NIEMALS** CSS-Variablen-Werte als "Beweis" verwenden — nur das gerenderte Ergebnis zählt
- **NIEMALS** Kontrast nur mathematisch berechnen — Hue-Similarity (lila auf navy) wird mathematisch NICHT erkannt
- **NIEMALS** einen Screenshot machen und dann NICHT beschreiben was darauf zu sehen ist

## Phase 1: Screenshot & Bestandsaufnahme

1. **App muss laufen** mit CDP-Port 9222 (Tauri/WebView2: `$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS='--remote-debugging-port=9222'; cargo tauri dev`; prüfen mit `curl -s http://127.0.0.1:9222/json/version`)
2. **Zum Ziel-View navigieren** via `page.evaluate(() => document.querySelector('.sidebar-nav-btn[data-tab="..."]')?.click())`
3. **Screenshot machen** — ganzer View
4. **JEDEN sichtbaren Text auflisten:**
   ```
   - Überschrift: "..." → Farbe, Hintergrund, lesbar? JA/NEIN
   - Beschreibungstext: "..." → Farbe, Hintergrund, lesbar? JA/NEIN
   - Button-Label: "..." → Farbe, Hintergrund, lesbar? JA/NEIN
   - Muted/Sekundärtext: "..." → Farbe, Hintergrund, lesbar? JA/NEIN
   ```
5. **Scrollen** — View nach unten scrollen und Punkte 3-4 wiederholen bis ALLES geprüft ist

## Phase 2: Element-Level Analyse

Für JEDES Element das potenziell schlecht lesbar ist:

```javascript
// COMPUTED Styles extrahieren — nicht CSS-Variablen!
const data = await page.evaluate((selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const cs = getComputedStyle(el);
    // Tatsächliche Farben (aufgelöst, nicht als Variable)
    return {
        text: el.textContent.trim().substring(0, 50),
        color: cs.color,             // rgb(r, g, b) — NICHT var(--name)
        backgroundColor: cs.backgroundColor,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        parentBg: getComputedStyle(el.parentElement).backgroundColor,
    };
}, selector);
```

**WICHTIG:** `getComputedStyle` gibt `rgb()` Werte zurück, nicht CSS-Variablen. Das ist die WAHRHEIT.

## Phase 3: Kontrast-Bewertung

Für jedes Element mit fraglicher Lesbarkeit:

1. **Tatsächliche Farben** aus Phase 2 verwenden (rgb-Werte)
2. **Hintergrund-Kette** durchgehen: Element → Parent → Grandparent bis ein nicht-transparenter Hintergrund gefunden wird
3. **Kontrastverhältnis** berechnen aus den ECHTEN rgb-Werten
4. **Hue-Similarity prüfen:** Violett/Lila auf Navy-Blau = FAIL auch bei 4.5:1 mathematischem Kontrast
5. **Schriftgrösse beachten:** < 14px braucht 4.5:1, >= 18px (oder 14px bold) braucht 3:1

## Phase 4: Zoom-Screenshots

Für jedes problematische Element:
1. Element-Screenshot machen (`el.screenshot()` oder Clip-Region)
2. In den Bericht aufnehmen als Beweis

## Ausgabeformat

```markdown
## Visuelle Verifikation: [View-Name]

### Geprüfte Elemente
| # | Element | Text (Auszug) | Farbe | Hintergrund | Kontrast | Lesbar? |
|---|---------|---------------|-------|-------------|----------|---------|
| 1 | h2.title | "Hardware-Opt..." | #e8e8ed | #222639 | 12.3:1 | JA |
| 2 | p.description | "Die Windows..." | #8890a8 | #222639 | 4.7:1 | GRENZWERTIG |
| 3 | span.path | "Systemsteuer..." | #4ecca3 | #222639 | ??? | NEIN |

### Probleme gefunden
| # | Element | Problem | Screenshot |
|---|---------|---------|------------|
| 1 | span.path | Teal auf Navy = schlecht lesbar | [zoom-1.png] |

### Screenshots
- [view-full.png] — Gesamtansicht
- [zoom-1.png] — Problem-Element vergrössert
```

## Sub-Agent-Delegation

Dieser Skill kann an einen Sub-Agent delegiert werden:
```
Task(subagent_type="general-purpose", prompt="Führe /visual-verify für den [view] aus. App läuft mit WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS='--remote-debugging-port=9222' auf Port 9222. ...")
```

## Cleanup (PFLICHT)

Nach Abschluss der Verifikation MÜSSEN alle temporären Dateien gelöscht werden:
1. **Erstellte JS-Scripts** in `tools/wcag/` löschen (z.B. `verify-*.js`, `test-*.js`)
2. **Screenshots** in `tools/wcag/*.png` löschen
3. Nur permanente Dateien bleiben: `wcag-gate.js`, `wcag-static-check.js`, `restore-window.ps1`, `package.json`

Sub-Agents die an diesen Skill delegiert werden, MÜSSEN die Cleanup-Anweisung im Prompt erhalten:
```
"Nach der Verifikation: Lösche ALLE erstellten .js und .png Dateien in tools/wcag/ (ausser wcag-gate.js, wcag-static-check.js, restore-window.ps1)."
```

## Hinweise

- **`page.click()` hängt** in dieser Tauri-App → immer `page.evaluate(() => el.click())` verwenden
- **Puppeteer-Scripts** liegen in `tools/wcag/` (dort ist puppeteer-core installiert)
- **Puppeteer-Verbindung:** `puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' })`
- **Dieser Skill ersetzt NICHT `/audit-code`** — er ergänzt ihn um die visuelle Komponente

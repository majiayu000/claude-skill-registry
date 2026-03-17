---
name: wcag-check
description: WCAG-Kontrastprüfung bei CSS-Änderungen. Führt den 2-stufigen Schutz aus (statischer Check + Laufzeit-Check) und prüft Farbregeln. Nutze diesen Skill IMMER wenn du CSS-Farben, Hintergründe oder Text-Styles änderst. Aufruf mit /wcag-check [--static-only] [--views view1,view2].
---

# WCAG-Kontrastprüfung

Du prüfst ob CSS-Änderungen die WCAG 2.2 AA Kontrast-Anforderungen einhalten. **Pflicht bei JEDER Änderung an `src/style.css`.**

## Argument

`$ARGUMENTS` = Optional: `--static-only` (nur statischer Check) oder `--views optimizer,network` (nur bestimmte Views)

## 2-Stufiger Schutz

### Stufe 1: Statischer CSS-Check (IMMER zuerst)

```bash
node tools/wcag/wcag-static-check.js
```

Prüft OHNE laufende App:
- Alle Text-Variablen (--text-primary, --text-secondary, --text-muted, --accent-text) auf allen Hintergründen (--bg-primary, --bg-secondary, --bg-card, --bg-tertiary) ≥ 4.5:1
- Alle `color: #fff` Stellen gegen ihre Hintergründe in derselben CSS-Regel
- Globale `::placeholder`-Regel vorhanden und Kontrast ausreichend
- Keine gefährlichen Muster (`#fff` auf --danger, --success, --warning)

**Exit-Code 0 = bestanden, 1 = Probleme**

### Stufe 2: Laufzeit-Check (wenn App läuft)

```bash
node tools/wcag/wcag-gate.js [--views optimizer,network] [--save-screenshots]
```

Prüft IN der laufenden App:
- Navigiert zu allen 14 Views (oder gefilterte)
- Extrahiert alle Text-Elemente mit `getComputedStyle`
- Alpha-Blending für halbtransparente Hintergründe (korrekte Komposition)
- Placeholder-Kontrast in Input-Feldern
- Wartet intelligent bis Views geladen sind (bis 5 Sekunden)

**Exit-Code 0 = bestanden, 1 = Verletzungen**

## Farbregeln (Dark Theme)

### Erlaubte Kombinationen

| Textfarbe | Auf welchen Hintergründen | Mindestkontrast |
|-----------|--------------------------|-----------------|
| `--text-primary` (#e8e9ed) | Alle Hintergründe | 7.4:1+ |
| `--text-secondary` (#b0b4c8) | Alle Hintergründe | 6.5:1+ |
| `--text-muted` (#9ba2b8) | Alle Hintergründe | 5.3:1+ |
| `--accent-text` (#c4b5fd) | Alle Hintergründe | 5.3:1+ |
| `#fff` | NUR auf `--accent` (#6c5ce7) | 4.86:1 |
| `#000` | Auf --danger, --success, --warning | 4.5:1+ |

### Verbotene Kombinationen

- `color: #fff` auf `--danger` (#e94560) → 3.83:1 FAIL
- `color: #fff` auf `--success` (#4ecca3) → 1.93:1 FAIL
- `color: #fff` auf `--warning` (#ffc107) → 1.63:1 FAIL
- `--accent` (#6c5ce7) als Textfarbe (NUR für Borders/Backgrounds)
- Lila/Violett auf dunkelblauem Hintergrund (Hue-Similarity = schlecht lesbar trotz Mathe)

### Neue Farben hinzufügen

Wenn eine neue Farbkombination benötigt wird:
1. Kontrast berechnen (sRGB → linear → Luminanz → Ratio)
2. ≥ 4.5:1 für normalen Text, ≥ 3.0:1 für grossen Text (≥18px oder ≥14px bold)
3. Hue-Similarity visuell prüfen (gleiche Farbfamilie = schlecht lesbar)
4. In BEIDEN Checks verifizieren

## Ablauf

1. Statischen Check ausführen → muss 0 Probleme melden
2. Falls App läuft: Laufzeit-Check ausführen → muss 0 Verletzungen melden
3. Falls Probleme gefunden: CSS fixen und erneut prüfen
4. Ergebnis dokumentieren

## Ausgabeformat

```markdown
## WCAG-Check: [was geändert wurde]

### Statischer Check
- Ergebnis: BESTANDEN / NICHT BESTANDEN
- [Details wenn nicht bestanden]

### Laufzeit-Check
- Ergebnis: BESTANDEN / NICHT BESTANDEN / ÜBERSPRUNGEN (App nicht gestartet)
- Views geprüft: X, Elemente: Y, Verletzungen: Z

### Zusammenfassung
Alle Kontraste eingehalten / X Probleme gefunden und behoben
```

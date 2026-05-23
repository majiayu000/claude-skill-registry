---
name: web-research
description: Internet-Tiefenrecherche zu einem technischen Thema. Durchsucht mehrere Quellen, vergleicht Ansätze, bewertet Vor-/Nachteile und gibt eine fundierte Empfehlung. Aufruf mit /web-research [fragestellung].
---

# Internet-Tiefenrecherche

Du führst eine systematische Internet-Recherche durch und lieferst eine fundierte, quellenbasierte Empfehlung.

## Argument

`$ARGUMENTS` = Technische Fragestellung oder Thema für die Recherche

## Recherche-Protokoll

### Phase 1: Breite Suche (mindestens 5 verschiedene Suchanfragen)

1. **Allgemeine Suche:** Hauptthema + aktuelle Lösungen
2. **Spezifische Suche:** Kontext der App (Tauri v2, Rust, Windows)
3. **Alternativen-Suche:** "Alternative to X", "X vs Y"
4. **Praxis-Suche:** Echte Implementierungen, GitHub-Repos, npm-Pakete
5. **Probleme-Suche:** Known issues, Limitierungen, Firmenumgebungen

### Phase 2: Quellen vertiefen

- Relevante Artikel/Docs vollständig lesen (WebFetch)
- npm-Pakete prüfen: Downloads, letzte Updates, Dependencies
- GitHub-Repos prüfen: Stars, Issues, Wartung

### Phase 3: Bewertungsmatrix

Jede Option bewerten nach:

| Kriterium | Gewicht |
|-----------|---------|
| Funktioniert OHNE Admin-Rechte | PFLICHT |
| Funktioniert OHNE Firewall-Änderungen | PFLICHT |
| Funktioniert in Firmenumgebungen | PFLICHT |
| Pure JS / keine Native Addons | Hoch |
| Tauri-kompatibel (Rust-Backend + WebView-Frontend) | Hoch |
| Aktiv gewartet (Updates < 12 Monate) | Mittel |
| Datenmenge/Qualität der Ergebnisse | Hoch |
| Performance (Timeout, Parallelität) | Mittel |

### Phase 4: Empfehlung

```markdown
## Recherche-Ergebnis: [Thema]

### Untersuchte Optionen
| Option | Beschreibung | Admin? | Firewall? | Firma? | Bewertung |
|--------|-------------|--------|-----------|--------|-----------|
| ...    | ...         | ...    | ...       | ...    | ...       |

### Empfehlung
Klare Empfehlung mit Begründung

### Quellen
- [Titel](URL) — Zusammenfassung
```

## Wichtige Regeln

- **Mindestens 5 Web-Suchen** durchführen (verschiedene Blickwinkel)
- **Mindestens 3 Quellen** vollständig lesen (nicht nur Suchergebnisse)
- **KEINE Empfehlung ohne Quellenangabe**
- **Praxistauglichkeit > Theorie** — was funktioniert in der echten Welt?
- **Firmenumgebung = Standardfall** — die App muss überall laufen
- **Quellen IMMER als Markdown-Links** am Ende angeben

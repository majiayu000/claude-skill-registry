---
name: clockodo
description: Clockodo Zeiterfassung - Stoppuhr steuern, Zeiteinträge verwalten, Kunden/Projekte/Leistungen abrufen. Nutze für "starte Timer", "stoppe Zeit", "was läuft gerade", "Zeiteinträge heute", "buche Zeit auf Projekt X".
metadata: {"clawdbot":{"emoji":"⏱️","requires":{"env":["CLOCKODO_EMAIL","CLOCKODO_API_KEY"]}}}
---

# Clockodo Skill

Steuere Clockodo-Zeiterfassung direkt aus Clawdbot: Stoppuhr starten/stoppen, Zeiteinträge verwalten, Auswertungen abrufen.

## Setup

### 1. API-Zugangsdaten holen

1. In Clockodo einloggen → **Persönliche Daten** → **API-Schlüssel**
2. E-Mail-Adresse und API-Key notieren

### 2. Environment Variables setzen

```bash
export CLOCKODO_EMAIL="deine@email.de"
export CLOCKODO_API_KEY="dein-api-key"
export CLOCKODO_APP_NAME="Clawdbot"  # optional
```

Am besten in `~/.zshrc` oder `~/.bashrc` eintragen, oder in Clawdbot config als environment.

## Verwendung

### Stoppuhr

**Status prüfen** (läuft gerade was?):
```bash
<skill>/scripts/clockodo.sh clock-status
```

**Starten** (benötigt Kunden-ID und Leistungs-ID):
```bash
<skill>/scripts/clockodo.sh clock-start <customers_id> <services_id> [projects_id] [text] [billable]
```

**Stoppen**:
```bash
<skill>/scripts/clockodo.sh clock-stop <entry_id>
```

### Zeiteinträge

**Auflisten** (Zeitraum im ISO8601-Format):
```bash
<skill>/scripts/clockodo.sh entries-list "2026-01-01T00:00:00Z" "2026-01-31T23:59:59Z"
```

**Einzelnen Eintrag abrufen**:
```bash
<skill>/scripts/clockodo.sh entries-get <id>
```

**Neuen Eintrag anlegen** (JSON):
```bash
<skill>/scripts/clockodo.sh entries-add '{"customers_id":123,"services_id":456,"billable":1,"time_since":"2026-01-15T09:00:00Z","time_until":"2026-01-15T12:00:00Z","text":"Beschreibung"}'
```

### Stammdaten

**Kunden auflisten**:
```bash
<skill>/scripts/clockodo.sh customers
```

**Projekte auflisten** (optional gefiltert nach Kunde):
```bash
<skill>/scripts/clockodo.sh projects [customers_id]
```

**Leistungsarten auflisten**:
```bash
<skill>/scripts/clockodo.sh services
```

**Benutzer auflisten**:
```bash
<skill>/scripts/clockodo.sh users
```

**Eigene Daten**:
```bash
<skill>/scripts/clockodo.sh me
```

### Urlaubsanträge & Abwesenheiten

**Alle Abwesenheiten auflisten**:
```bash
<skill>/scripts/clockodo.sh absences [year]
```

**Offene Urlaubsanträge** (Status = 0/enquired):
```bash
<skill>/scripts/clockodo.sh absences-pending [year]
```

**Einzelne Abwesenheit abrufen**:
```bash
<skill>/scripts/clockodo.sh absence-get <id>
```

**Urlaubsantrag freigeben**:
```bash
<skill>/scripts/clockodo.sh absence-approve <id>
```

**Urlaubsantrag ablehnen** (optional mit Begründung):
```bash
<skill>/scripts/clockodo.sh absence-reject <id> [note]
```

### Zeitkontrolle

**Arbeitszeiten eines Users** (Datum im Format YYYY-MM-DD):
```bash
<skill>/scripts/clockodo.sh worktimes <user_id> <since> <until>
```

**Arbeitsziel**:
```bash
<skill>/scripts/clockodo.sh worktime-target <user_id> [year]
```

**Einträge eines Users**:
```bash
<skill>/scripts/clockodo.sh entries-by-user <user_id> <since> <until>
```

## Agent-Anweisungen

### Typische Anfragen

**"Starte Timer für [Projekt/Kunde]"**
1. Hole Stammdaten wenn IDs unbekannt: `customers`, `projects`, `services`
2. Finde passende IDs
3. Starte mit `clock-start`

**"Was läuft gerade?" / "Timer Status"**
1. `clock-status` aufrufen
2. Wenn `running` null → nichts läuft
3. Sonst: Zeige Kunde, Projekt, Startzeit, Dauer

**"Stoppe Timer"**
1. `clock-status` für aktuelle Entry-ID
2. `clock-stop <entry_id>`

**"Zeiteinträge heute/diese Woche/diesen Monat"**
1. Berechne Zeitraum (ISO8601 UTC)
2. `entries-list` mit Zeitraum
3. Formatiere Ergebnis übersichtlich (Summen, nach Projekt gruppiert)

**"Buche X Stunden auf Projekt Y"**
1. Finde Kunden-/Projekt-/Leistungs-IDs
2. Berechne Start- und Endzeit
3. `entries-add` mit JSON

**"Offene Urlaubsanträge" / "Wer will Urlaub?"**
1. `absences-pending` aufrufen
2. Filtern nach `status: 0` (enquired)
3. Übersichtlich formatieren: Name, Zeitraum, Typ, Tage

**"Urlaubsantrag von [Name] freigeben"**
1. `absences-pending` für offene Anträge
2. Antrag des Mitarbeiters finden
3. `absence-approve <id>`

**"Haben alle Mitarbeiter ihre Zeiten eingetragen?" / "Zeitkontrolle"**
1. `users` für Liste aller aktiven Mitarbeiter
2. Für jeden User: `entries-by-user <id> <wochenstart> <wochenende>`
3. Summe der Stunden berechnen (duration / 3600)
4. Mit Soll vergleichen (z.B. 40h oder aus worktime-target)
5. Fehlende Stunden markieren

**Wöchentlicher Timesheet-Check (für Cron)**
1. Hole alle User
2. Berechne letzte Woche (Mo-Fr)
3. Für jeden User: Prüfe gebuchte Stunden
4. Liste Mitarbeiter mit < X Stunden gebuchter Zeit
5. Sende Slack-Nachricht an säumige Mitarbeiter

### Formatierung der Ausgabe

Zeiteinträge als kompakte Liste:
```
📅 Heute (Mo 27.01.2026)
━━━━━━━━━━━━━━━━━━━━━━━
• 09:00-12:00 (3h) – Kunde A / Projekt X – "Meeting"
• 13:00-17:30 (4,5h) – Kunde B / Projekt Y – "Entwicklung"
━━━━━━━━━━━━━━━━━━━━━━━
Gesamt: 7,5h
```

Laufender Timer:
```
⏱️ Timer läuft seit 14:23 (2h 15m)
   Kunde: Rockstardevelopers
   Projekt: Website Relaunch
   Leistung: Entwicklung
```

### ID-Caching

Speichere häufig genutzte IDs in `<workspace>/TOOLS.md` unter `### Clockodo`:

```markdown
### Clockodo

**Kunden:**
- 12345 → Rockstardevelopers GmbH
- 12346 → accessibleAI SmartCompliance GmbH

**Projekte:**
- 67890 → RSD Website Relaunch
- 67891 → accessibleAI MVP

**Leistungen:**
- 111 → Entwicklung
- 112 → Meeting
- 113 → Support
```

Beim ersten Aufruf die Stammdaten abrufen und in TOOLS.md cachen.

## Automatisierung: Wöchentlicher Timesheet-Check

Beispiel-Workflow für wöchentliche Zeiterfassungs-Kontrolle:

### Setup (einmalig)

1. **User-Mapping anlegen** in `<workspace>/TOOLS.md`:

```markdown
### Clockodo User → Slack

| User ID | Name | Slack ID | Soll-Stunden/Woche |
|---------|------|----------|-------------------|
| 12345 | Max Mustermann | U0ABC123 | 40 |
| 12346 | Erika Musterfrau | U0DEF456 | 32 |
```

2. **Cron-Job erstellen** (z.B. jeden Montag 10:00):
   - Prüfe Vorwoche
   - Slack-Erinnerung an Mitarbeiter mit < 90% Soll

### Check-Logik

```
1. Berechne Zeitraum: Letzte Woche Mo 00:00 bis Fr 23:59
2. Für jeden aktiven User:
   a. entries-by-user <id> <start> <end>
   b. Summe = Σ(entry.duration) / 3600 Stunden
   c. Wenn Summe < (Soll * 0.9):
      → Slack-Nachricht: "Bitte Zeiten für letzte Woche nachtragen"
3. Report an Admin: Übersicht aller User + gebuchte Stunden
```

### Absence-Status Codes

| Status | Bedeutung |
|--------|-----------|
| 0 | Angefragt (pending) |
| 1 | Genehmigt |
| 2 | Abgelehnt |
| 3 | Genehmigung zurückgezogen |
| 4 | Anfrage zurückgezogen |

### Absence-Typen

| Typ | Bedeutung |
|-----|-----------|
| 1 | Urlaub |
| 2 | Sonderurlaub |
| 3 | Überstundenabbau |
| 4 | Krankheit |
| 5 | Kind krank |
| 6 | Fortbildung |
| 7 | Mutterschutz |
| 8 | Home Office |
| 9 | Außendienst |

## API-Referenz

Volle Dokumentation: https://www.clockodo.com/en/api/

**Wichtige Endpunkte:**
- `/v2/clock` – Stoppuhr steuern
- `/v2/entries` – Zeiteinträge CRUD
- `/v2/customers` – Kundenliste
- `/v2/projects` – Projektliste
- `/v2/services` – Leistungsarten
- `/v2/users` – Benutzerliste
- `/v2/absences` – Abwesenheiten
- `/v2/worktimes` – Arbeitszeiten

**Authentifizierung:**
- Header: `X-ClockodoApiUser` + `X-ClockodoApiKey`
- Plus: `X-Clockodo-External-Application: AppName;email`

**Datumsformat:** ISO 8601 UTC (z.B. `2026-01-27T14:30:00Z`)

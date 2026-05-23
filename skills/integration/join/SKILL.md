---
name: join
description: JOIN.com Bewerbungsmanagement - neue Bewerbungen anzeigen, Gehaltsvorstellungen prüfen, PDFs automatisch zu Google Drive hochladen. Use when user asks about applications, candidates, job applications, Bewerbungen, or JOIN.
metadata: {"clawdbot":{"emoji":"👔","requires":{"env":["JOIN_API_TOKEN"]}}}
---

# JOIN.com Bewerbungsmanagement

Skill für die Integration mit JOIN.com (Recruiting-Plattform).

## Setup

1. **API Token holen:** https://join.com/user/api
2. **Token speichern:** `export JOIN_API_TOKEN="dein-token"` (in ~/.zshrc)

## Verfügbare Befehle

### Bewerbungen auflisten
```bash
<skill>/scripts/join-cli.sh applications [DAYS]
```

**Ausgabe:** JSON mit Bewerbungen inkl. Name, E-Mail, Gehaltsvorstellung, Status

### Bewerbungsdetails
```bash
<skill>/scripts/join-cli.sh application <APPLICATION_ID>
```

**Ausgabe:** Vollständige Details inkl. Anschreiben, Dateien, Custom Fields

### Dateien herunterladen
```bash
<skill>/scripts/join-cli.sh download <APPLICATION_ID> [OUTPUT_DIR]
```

**Default Output:** `/tmp/join-files`

### Jobs auflisten
```bash
<skill>/scripts/join-cli.sh jobs
```

---

## Workflow: Neue Bewerbungen verarbeiten

### Bei Anfrage "Zeig mir neue Bewerbungen"

1. **Bewerbungen abrufen:**
   ```bash
   <skill>/scripts/join-cli.sh applications 7
   ```

2. **Für jede interessante Bewerbung:**
   - Details mit Gehaltsvorstellung anzeigen
   - Bei Bedarf PDFs herunterladen

### Bei Anfrage "Lade Bewerbungsunterlagen zu Drive"

1. **Dateien herunterladen:**
   ```bash
   <skill>/scripts/join-cli.sh download <APP_ID> /tmp/join-files
   ```

2. **Zu Google Drive hochladen:**
   ```bash
   gog drive upload /tmp/join-files/*.pdf --parent <BEWERBUNGEN_FOLDER_ID> --account thomas@rockstardevelopers.de
   ```

3. **Lokale Dateien aufräumen:**
   ```bash
   rm -rf /tmp/join-files
   ```

---

## Google Drive Ordner

Bewerbungsunterlagen werden standardmäßig hier abgelegt:
- **Ordner:** `Bewerbungen/[Jahr]/[Monat]/[Kandidatenname]/`

Falls der Ordner noch nicht existiert, frage den Meister nach der gewünschten Struktur.

---

## Formatierung für Slack

Wenn du Bewerbungen im Chat präsentierst:

```
👤 *Max Mustermann* — Senior Developer
📧 max@example.com
💰 Gehaltsvorstellung: 75.000 € 
📅 Eingegangen: 27.01.2026
📎 3 Dateien (Lebenslauf, Anschreiben, Zeugnisse)
```

**Keine Tabellen in Slack!** Bullet-Listen verwenden.

---

## Automatische Verarbeitung neuer Bewerbungen

### Trigger: Neue JOIN-E-Mail (via Heartbeat)

**Suchmuster:** `from:join subject:"Neue Bewerbung" is:unread`

### Workflow pro E-Mail

1. **Bewerbername aus E-Mail extrahieren:**
   - Format in E-Mail: `MT\n\nMuhammadali Turgunov\n\nGermany`
   - Oder aus Kandidaten-URL: `https://join.com/candidates/41766224`

2. **Passende Bewerbung in JOIN API finden:**
   ```bash
   <skill>/scripts/join-cli.sh applications
   ```
   Matche nach Vorname + Nachname

3. **NUR diese Bewerbung verarbeiten:**
   - Ordner erstellen: `[Nachname]_[Vorname]_[Gehalt]EUR`
   - PDFs herunterladen und hochladen
   - **CV analysieren** (siehe unten)
   - **Slack-Benachrichtigung senden**
   - In Tracking eintragen

4. **E-Mail als gelesen markieren**

### CV-Analyse

Für jeden neuen Bewerber den CV analysieren und folgende Infos extrahieren:
- 🇩🇪 Deutscher Muttersprachler? (Ja/Nein)
- 🪪 Deutsche Staatsangehörigkeit? (Ja/Nein/unklar)
- 💼 Jahre Full-Stack-Erfahrung
- 🛠️ Top 5 Skills
- 🌐 Sprachen
- 📋 Anzahl Projekte

**Methode:** PDF zu PNG konvertieren, dann mit Image-Analyse auswerten:
```bash
sips -s format png <cv.pdf> --out /tmp/cv.png
# Dann image tool mit Analyse-Prompt
```

### Slack-Benachrichtigung Format

```
📥 *Neue Bewerbung: Max Mustermann*
💰 Gehaltsvorstellung: 60.000 €
📁 <folder_link|Bewerbungsordner>

📊 *CV-Analyse:*
• 🇩🇪 Deutsch: Ja (Muttersprachler)
• 🪪 Staatsangehörigkeit: Deutsch
• 💼 Full-Stack: 5+ Jahre
• 🛠️ Skills: React, Node.js, TypeScript, PostgreSQL, Docker
• 🌐 Sprachen: Deutsch, Englisch
• 📋 Projekte: 8

✅ *Empfehlung: Interessant* / ⚠️ *Nicht passend*
```

---

## Tracking

Nach dem Verarbeiten von Bewerbungen:
- Tracking in `<workspace>/memory/join-tracking.json` aktualisieren
- Verhindert doppelte Benachrichtigungen

```json
{
  "processed": {
    "app-id-123": {
      "name": "Max Mustermann",
      "processedAt": "2026-01-27T14:00:00Z"
    }
  }
}
```

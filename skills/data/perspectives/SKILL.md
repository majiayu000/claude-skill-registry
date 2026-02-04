---
name: perspectives
description: "Analysiert aus mehreren Perspektiven. Run '/perspectives', 'multi-perspektive', oder 'verschiedene sichtweisen'."
---

# Perspectives Skill (Role Stacking)

Analysiert ein Thema aus mehreren Experten-Perspektiven und zeigt Konflikte sowie Synergien auf. Basiert auf Anthropic's "Role Stacking" Best Practice.

## Wann ausfuehren

- Bei Entscheidungen mit mehreren Stakeholdern
- Wenn User sagt "perspectives", "multi-perspektive", oder "/perspectives"
- Bei Trade-off Entscheidungen
- Bei strategischen Fragen

## Workflow

### 1. Perspektiven auswaehlen

Frage den User welche 3 Perspektiven relevant sind:

```
Verwende AskUserQuestion:
{
  "questions": [
    {
      "question": "Welche Perspektiven sollen beruecksichtigt werden?",
      "header": "Perspektiven",
      "options": [
        { "label": "Tech + Business + User", "description": "Standard: Machbarkeit, ROI, UX" },
        { "label": "Entwickler + PM + Designer", "description": "Team-Perspektiven auf Feature" },
        { "label": "Startup + Enterprise + Agency", "description": "Verschiedene Unternehmenstypen" },
        { "label": "Andere", "description": "Eigene Perspektiven definieren" }
      ],
      "multiSelect": false
    }
  ]
}
```

**Standard-Perspektiven (wenn keine Auswahl):**
- Technisch (Machbarkeit, Architektur, Wartbarkeit)
- Business (ROI, Ressourcen, Time-to-Market)
- User (UX, Akzeptanz, Lernkurve)

### 2. Jede Perspektive einzeln analysieren

Fuer jede Perspektive:

```
## Perspektive 1: [Name]

**Rolle:** [Kurze Beschreibung der Perspektive]

**Bewertung:** [Positiv/Neutral/Negativ]

**Kernargumente:**
1. [Argument 1]
2. [Argument 2]
3. [Argument 3]

**Bedenken:**
- [Bedenken 1]
- [Bedenken 2]

**Empfehlung aus dieser Sicht:**
[Konkrete Empfehlung]
```

### 3. Konflikte identifizieren

```
## Konflikte zwischen Perspektiven

| Perspektive A | vs | Perspektive B | Konflikt |
|---------------|-----|---------------|----------|
| Tech | vs | Business | [Beschreibung] |
| Business | vs | User | [Beschreibung] |
| Tech | vs | User | [Beschreibung] |
```

### 4. Synergien aufzeigen

```
## Synergien

| Perspektiven | Gemeinsamer Nenner |
|--------------|-------------------|
| Tech + Business | [Beschreibung] |
| Alle drei | [Beschreibung] |
```

### 5. Gewichtete Empfehlung

```
## Empfehlung

**Gewichtung:** [z.B. Tech 40%, Business 35%, User 25%]

**Entscheidung:** [Konkrete Empfehlung]

**Begruendung:** [Warum diese Gewichtung und Entscheidung]

**Naechste Schritte:**
1. [Schritt 1]
2. [Schritt 2]
3. [Schritt 3]
```

## Beispiel-Ablauf

### User Request
"Sollen wir auf einen neuen Tech Stack migrieren?"

### Perspektive 1: Technisch

**Rolle:** Senior Developer / Architekt

**Bewertung:** Positiv

**Kernargumente:**
1. Aktueller Stack hat bekannte Performance-Probleme
2. Neuer Stack hat besseres Tooling und Community
3. Langfristig weniger technische Schulden

**Bedenken:**
- Lernkurve fuer das Team
- Migration-Risiken bei laufendem System

**Empfehlung:** Migration durchfuehren, aber schrittweise

### Perspektive 2: Business

**Rolle:** Product Owner / Management

**Bewertung:** Neutral bis negativ

**Kernargumente:**
1. Keine direkten Feature-Gewinne fuer Kunden
2. Team ist 2-3 Monate gebunden
3. Risiko fuer laufende Projekte

**Bedenken:**
- Opportunity Cost
- Erklaerung gegenueber Stakeholdern schwierig

**Empfehlung:** Nur wenn dringende technische Probleme bestehen

### Perspektive 3: User

**Rolle:** UX Designer / Endnutzer

**Bewertung:** Neutral

**Kernargumente:**
1. Potenziell bessere Performance
2. Kurzfristig keine sichtbaren Aenderungen
3. Langfristig bessere Moeglichkeiten

**Bedenken:**
- Potenzielle Bugs waehrend Migration
- Features die warten muessen

**Empfehlung:** Okay wenn Performance spuerbar besser wird

### Konflikte

| Tech | vs | Business | Tech will jetzt, Business will warten |
| Business | vs | User | Business sieht kein ROI, User will Performance |

### Synergien

| Tech + User | Beide wollen bessere Performance |
| Alle | Alle wollen stabiles, wartbares System |

### Empfehlung

**Gewichtung:** Tech 35%, Business 40%, User 25%

**Entscheidung:** Schrittweise Migration in ruhiger Phase

**Begruendung:** Business-Bedenken sind berechtigt, aber technische Schulden kosten langfristig mehr. Kompromiss: Nicht sofort, aber zeitnah planen.

**Naechste Schritte:**
1. Pilot-Migration eines unkritischen Moduls
2. Performance-Vergleich dokumentieren
3. Migration-Roadmap fuer Q2 erstellen

## Wichtige Regeln

- **IMMER** mindestens 3 Perspektiven (mehr ist ok)
- **JEDE** Perspektive ernst nehmen, keine kuenstlich schwaecheln
- **EHRLICHE** Konflikte benennen, nicht beschoenigen
- **KONKRETE** Empfehlung am Ende, nicht "es kommt drauf an"
- Bei technischen Fragen: Technische Perspektive detaillierter

## Typische Nutzung

User: `/perspectives Sollen wir Microservices einfuehren?`

Response:
1. Perspektiven-Auswahl anbieten (oder Standard verwenden)
2. 3 detaillierte Analysen
3. Konflikte und Synergien
4. Gewichtete Empfehlung mit Begruendung

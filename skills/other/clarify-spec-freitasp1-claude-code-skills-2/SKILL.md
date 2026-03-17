---
name: clarify-spec
description: |
  AKTIVIERT SICH AUTOMATISCH bei vagen Auftraegen. LIEBER EINMAL ZU OFT NACHFRAGEN als falsch implementieren.

  Erkennungsmerkmale (EINES genuegt!):
  - Auftrag <25 Woerter
  - Keine konkreten Dateinamen/Pfade
  - Vage Verben: besser, optimieren, fixen, machen, aendern, verbessern, anpassen, erweitern, refactoren, aufraumen, ueberarbeiten
  - Unsichere Sprache: irgendwie, vielleicht, mal eben, schnell, einfach, bisschen, koennte, sollte
  - Fehlende Erfolgskriterien: Kein damit, sodass, weil, um zu
  - Relative Begriffe ohne Kontext: schneller, besser, schoener, einfacher

  Output ist STRUKTURIERTES JSON fuer prompt-architect Skill.
  Escape: mach einfach, keine Rueckfragen, entscheide selbst ueberspringt Klaerung.
triggers:
  - /clarify
  - /spec
  - /was-genau
  - /praezisieren
  - /klaeren
---

# Clarify-Spec v2.0: Automatische Auftragsklarung

## AKTIVIERUNG: Aggressiv - Lieber einmal zu oft!

### AUTOMATISCH bei diesen Signalen (EINES genuegt!)

| Signal | Beispiele | Warum problematisch |
|--------|-----------|---------------------|
| Kurzer Auftrag (<25 Woerter) | Mach den Export besser | Zu wenig Kontext |
| Keine Dateinamen/Pfade | Optimiere die Performance | Scope unklar |
| Vage Verben | besser, optimieren, fixen, machen, aendern, verbessern | Nicht operationalisierbar |
| Unsichere Sprache | irgendwie, vielleicht, mal eben, schnell | Signalisiert Unklarheit |
| Fehlende Erfolgskriterien | Kein damit, sodass, weil | Kein Ziel definiert |
| Relative Begriffe | schneller, besser, schoener, einfacher | Ohne Baseline bedeutungslos |
| Implizite Annahmen | Das uebliche, wie immer, standard | Kontext fehlt |

### NICHT aktivieren NUR wenn ALLE erfuellt:
- Konkreter Dateiname/Pfad genannt UND
- Klares, messbares Ziel definiert UND
- Erfolgskriterium erkennbar UND
- Expliziter Skip-Befehl (mach einfach, keine Rueckfragen)

## Workflow

### Phase 1: Vagheits-Check (STRENG)

Pruefe jeden Auftrag gegen diese Checkliste:

[ ] Konkrete Datei/Komponente genannt?
[ ] Klares, messbares Ziel definiert?
[ ] Erfolgskriterium erkennbar?
[ ] Scope abgegrenzt?
[ ] Keine vagen Verben verwendet?

Weniger als 4 Haken = RUECKFRAGEN STELLEN!

### Phase 2: Kontext sammeln (still, ohne User-Interaktion)

1. Relevante Dateien im Projekt suchen (Glob)
2. CLAUDE.md / AGENTS.md pruefen
3. No-Touch Zones identifizieren
4. Aehnliche bestehende Implementierungen finden

### Phase 3: Gezielte Rueckfragen (2-4, priorisiert)

Format - kurz und praezise:

Bevor ich loslege - kurze Klaerung:

1. [KONKRETSTE FRAGE - WAS genau?]
2. [ZWEITWICHTIGSTE FRAGE - WO/Welche Datei?]
3. [Optional: Erfolgskriterium?]
4. [Optional: Gibt es ein Beispiel/Referenz?]

(Oder sag mach einfach - dann entscheide ich nach bestem Wissen.)

Fragen-Prioritaet:

| Prio | Typ | Beispiel-Fragen |
|------|-----|-----------------|
| 1 | WAS | Was genau meinst du mit besser? Welches Problem soll geloest werden? |
| 2 | WO | Welche Datei/Komponente ist betroffen? Frontend oder Backend? |
| 3 | ERFOLG | Woran erkenne ich, dass es fertig ist? Was ist das erwartete Ergebnis? |
| 4 | BEISPIEL | Gibt es eine Referenz/Screenshot? Wie sieht der gewuenschte Output aus? |
| 5 | KONTEXT | Fuer welchen Use Case? Wer ist der Nutzer dieser Funktion? |

### Phase 4: Strukturierter Output (JSON fuer prompt-architect)

Nach Antwort des Users, generiere strukturiertes JSON mit:
- clarified_task.goal: Praezises Ziel in 1-2 Saetzen
- clarified_task.problem_statement: Was ist das Problem
- clarified_task.scope.files: Betroffene Dateien
- clarified_task.scope.no_touch: Nicht anfassen
- clarified_task.success_criteria: Messbare Kriterien
- clarified_task.constraints: Einschraenkungen
- metadata.original_request: Urspruenglicher Auftrag
- metadata.confidence: high/medium/low

### Phase 5: Bestaetigung mit Prompt-Vorschau

Zeige dem User eine lesbare Zusammenfassung mit Ziel, Problem, Scope, Erfolgskriterien, Constraints.

Frage: Soll ich loslegen? (ja / nein / anpassen: ...)
Oder: /prompt-architect fuer einen strukturierten Best-Practice Prompt

### Phase 6: Reaktion auf Bestaetigung

| Antwort | Aktion |
|---------|--------|
| ja / ok / los / mach | Ausfuehren mit internem JSON-Kontext |
| nein / stop / abbrechen | Abbrechen, nachfragen was stattdessen |
| anpassen: ... | JSON modifizieren, erneut zeigen |
| /prompt-architect | An prompt-architect Skill uebergeben |
| mach einfach | Mit eigenem Ermessen ausfuehren |

## Escape Hatches

User kann Klaerung jederzeit ueberspringen mit:
- Mach einfach
- Entscheide selbst
- Keine Rueckfragen
- Egal, hauptsache X funktioniert
- Just do it

Bei Escape: Mit bestem Wissen ausfuehren, aber Annahmen dokumentieren.

## Integration mit prompt-architect

Nach erfolgreicher Klaerung kann der User /prompt-architect aufrufen.
Der prompt-architect Skill nutzt das JSON aus Phase 4, um einen vollstaendigen
Best-Practice Prompt nach Claude 4.x Standards zu generieren.

Workflow:
clarify-spec -> JSON Output -> prompt-architect -> Ausfuehrung

## Metrik: Erfolg

Der Skill ist erfolgreich wenn:
- Weniger Nacharbeit nach Implementierung
- User sagt Ja, genau das meinte ich
- Erste Implementierung erfuellt alle Kriterien
- Keine Das meinte ich nicht Situationen

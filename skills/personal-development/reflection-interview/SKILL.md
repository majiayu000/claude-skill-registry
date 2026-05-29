---
name: reflection-interview
triggers: ["/reflection", "/interview", "Reflexion schreiben", "reflection interview"]
description: Interactive interview for journal entry reflections. Covers all 5 research sub-questions (Workflow, Autorschaft, Iteration, Scheitern, Ästhetik) aligned with the main research question.
---

# Reflection Interview Skill

## Trigger

Use when writing or rewriting reflection sections for journal entries in the Everything Machine project.

## Research Context

**Hauptfrage:** Wie verändert der Einsatz generativer KI-Werkzeuge meinen kreativen Arbeitsprozess?

**Unterfragen:**
1. Workflow — Welche neuen Arbeitsschritte entstehen? Welche fallen weg?
2. Autorschaft — Wer ist Autor:in? Wie verschiebt sich meine Rolle?
3. Iteration — Wie beeinflusst die Unmittelbarkeit von KI-Output meinen Prozess?
4. Scheitern — Was lerne ich aus fehlgeschlagenen Experimenten?
5. Ästhetik — Entwickelt sich eine eigene visuelle Sprache?

## Interview Process

### Phase 1: Kontext

Ask using `AskUserQuestion`:
- **Tools:** "Welche Tools hast du in dieser Session verwendet?" (Freitext)
- **Intention:** "Was wolltest du erreichen?"

### Phase 2: Die 5 Unterfragen

Use `AskUserQuestion` with multiSelect where appropriate:

**1. Workflow**
```
Frage: "Hat sich dein Arbeitsablauf verändert? Was war neu, was ist weggefallen?"
Header: "Workflow"
Options:
- "Neue Schritte entstanden" + description field
- "Schritte weggefallen" + description field
- "Ähnlich wie vorher"
- "Komplett anders"
```

**2. Autorschaft**
```
Frage: "Wie hast du deine Rolle in diesem Prozess erlebt?"
Header: "Autorschaft"
Options:
- "Ich war Regisseur:in" — KI hat ausgeführt
- "Kollaboration" — Ping-Pong zwischen mir und KI
- "KI hat geführt" — Ich habe reagiert
- "Kurator:in" — Ich habe ausgewählt
```

**3. Iteration**
```
Frage: "Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst?"
Header: "Iteration"
Options:
- "Mehr Experimente" — Ich habe mehr ausprobiert
- "Weniger Planung" — Direkter ins Machen
- "Überwältigend" — Zu viele Optionen
- "Kein Unterschied"
```

**4. Scheitern**
```
Frage: "Was ist schiefgelaufen und was hast du daraus gelernt?"
Header: "Scheitern"
(Freitext empfohlen — oder Option "Nichts ist gescheitert")
```

**5. Ästhetik**
```
Frage: "Hat sich durch die Arbeit eine eigene visuelle/stilistische Sprache entwickelt?"
Header: "Ästhetik"
Options:
- "Ja, deutlich" — Beschreibe es
- "Ansatzweise"
- "Nein, eher generisch"
- "Nicht relevant für diese Session"
```

### Phase 3: Generierte Frage

Based on the journal entry content, generate ONE contextual question that:
- Is specific to what happened in this session
- Probes deeper into an interesting aspect
- Cannot be answered with yes/no

Example: "Du hast erwähnt, dass ComfyUI abstürzte — hat das Warten deine Idee verändert?"

### Phase 4: Output

Write reflection in conversational German (du-Form), structured as:
1. Opening paragraph — Gefühl/Kontext
2. Process observations — Was ist passiert
3. Key insight — Eine zentrale Erkenntnis
4. Open question — Was bleibt offen

**Format:** Use `chat-intro` div for narrative sections if using chat format.

## Example Output

```markdown
## Reflexion

Das war ein produktiver Tag, auch wenn nicht alles funktioniert hat. Ich habe hauptsächlich mit ComfyUI und Claude gearbeitet...

[Process observations based on interview answers]

Was mich überrascht hat: [Key insight from Scheitern/Ästhetik answers]

Offen bleibt: [From generated question or interview]

**Keywords:** #ComfyUI #Workflow #[relevant tags]
```

## Notes

- Always conduct the interview before writing — don't assume
- Keep reflection authentic to user's voice
- Max 200 words for reflection text
- Include 3-5 relevant keywords

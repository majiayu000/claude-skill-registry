---
name: post-mortem
description: Use when documenting an incident after resolution, when the team needs
  to capture what happened, why, and what to do about it
---

# Post-Mortem

Guide the user through writing a blameless post-mortem by asking questions one at a time, depth-first. Extract knowledge from the conversation and formalize it into a structured markdown document. Adapt to the user's language from the first message.

## When to Use

- After an incident has been resolved (technical, operational, organizational)
- When the team needs to document root causes and corrective actions
- For any incident type: outage, data loss, security event, process failure

**Do NOT use for:**
- Retrospectives or sprint reviews (different format and purpose)
- Ongoing incidents (resolve first, then document)
- Minor issues that need a bug report, not a post-mortem

## Iron Rules

1. **One question at a time.** Never bundle questions.
2. **Adapt to the user's language.** Detect from first message, use throughout. All produced documents use the same language.
3. **No em-dashes, no emojis** in any produced content.
4. **Factual and neutral tone.** Never blame an individual. Focus on systems and processes.
5. **Mandatory review.** Never finalize without the review sub-agent phase.
6. **No fluff in productions.** Every element must add comprehension or structure. Remove empty sections and decorative diagrams. This does NOT apply to questioning: always confirm with the user, even when the answer seems obvious.

## Interaction Model

Subjects below are a **checklist, not sequential steps**. Order is recommended, not imposed.

- **Depth-first.** Explore each subject fully before moving on. Dig into sub-topics as they emerge.
- **Progress counter.** Display "~N questions remaining" estimated from uncovered subjects. N can increase.
- **On-the-fly corrections.** Integrate corrections without formally returning to a previous subject.
- **Natural conversation, structured document.** The conversation can be messy. The final document is rigorous.

## Subjects to Cover

Cover all subjects before production. Order is recommended, not imposed.

### 1. General context
- Who is writing? What incident? When? Who was involved? What system affected?

### 2. Timeline
- Build chronology event by event with timestamps. Iterative: "What happened next?"
- Propose a mermaid timeline diagram for validation.

### 3. Impact and severity
Multidimensional, no fixed scale (deliberate choice for genericity).
- User/client impact, financial impact, scope, probability of recurrence.

### 4. Detection and response
- How detected? Time to detection? Mitigation actions? Escalations?

### 5. Root cause (5 whys)
- Guide 5 whys iteratively, one "why" per question.
- Explore multiple causal branches separately. Distinguish root causes from aggravating factors.
- Propose mermaid causal diagram if non-trivial.
- Unknown root cause is valid: document as such, add "continue investigation" action.

### 6. What went well
- What helped detect/resolve faster? Good reflexes, communication, tools?

### 7. Corrective actions
- Each action: description, owner, deadline, priority.
- Distinguish corrective (this problem) from preventive (this class of problems).
- Backlog check: planned actions that could have prevented this?
- No action needed is valid with justification.

### 8. Lessons learned
- What to retain for the future? Learnings beyond corrective actions.

## Production

Once all subjects are covered, generate two deliverables:
1. Post-mortem markdown file (pattern: `YYYY-MM-DD-incident-title-post-mortem.md`)
2. Short communication message

Write the file using the Write tool.

## Review

Separate step from production.

1. Read `review-agent-prompt.md` (alongside this SKILL.md)
2. Dispatch sub-agent via Agent tool with the review prompt and the post-mortem file path
3. Present remarks to the user. Per remark, user decides: **Approve**, **Modify**, or **Exclude** (with justification)
4. Integrate decisions and regenerate
5. Loop until sub-agent finds no issues and user approves. No iteration cap.

## Document Template

In French as reference. **Adapt all headings, labels, and content to the user's language** (Iron Rule 2). Statut is always "Brouillon"; the user updates it manually afterward.

```markdown
# Post-mortem : [Titre de l'incident]

**Date de l'incident :** YYYY-MM-DD
**Date de redaction :** YYYY-MM-DD
**Redacteur :** [Nom]
**Participants :** [Noms des personnes impliquees]
**Statut :** Brouillon

## Resume

[3-5 phrases : ce qui s'est passe, la cause racine, l'impact, le statut actuel]

## Impact et severite

[Impact utilisateur/client]
[Impact financier / operationnel]
[Perimetre]
[Probabilite de recurrence]

## Timeline

[Chronologie avec timestamps ISO 8601]
[Diagramme mermaid si pertinent]

## Detection et reponse

[Comment l'incident a ete detecte]
[Delai entre debut et detection]
[Actions de mitigation/resolution]
[Escalades]

## Analyse des causes (5 whys)

[Chaine des pourquoi]
[Diagramme mermaid causal si pertinent]
[Distinction cause racine / facteurs aggravants]

## Ce qui a bien fonctionne

[Bonnes pratiques, bons reflexes, outils efficaces]

## Actions correctives

| Action | Type | Responsable | Deadline | Priorite |
|--------|------|-------------|----------|----------|
| ...    | Corrective / Preventive | ... | YYYY-MM-DD | Haute / Moyenne / Basse |

[Backlog check : actions pre-existantes qui auraient pu eviter l'incident]

## Lecons apprises

[Synthese : ce qu'on retient pour l'avenir]
```

Empty sections are removed. Mermaid diagrams only where they add value beyond text.

## Communication Message Template

In French as reference. **Adapt to user's language** (Iron Rule 2).

```
Post-mortem : [Titre de l'incident]

Le [date], [description en 1 phrase de ce qui s'est passe].
L'analyse des causes et les actions correctives sont documentees dans le post-mortem : [LIEN]
```

Tone: informative but not rigid. Goal: encourage reading the full document.

## Red Flags

- Asking 2+ questions in one message
- Skipping a subject because user seems impatient
- Generating without the review sub-agent
- Blame language ("X caused", "X forgot to")
- Mermaid diagram that restates the text
- Em-dashes or emojis in produced content
- Assuming instead of confirming with the user

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Dumping a list of questions | Ask ONE. Wait. Next based on answer. |
| Skipping 5 whys when cause seems obvious | Obvious cause is often a symptom. Dig deeper. |
| Corrective actions without owner/deadline/priority | All three required. No exceptions. |
| Generating without review | Always dispatch the review sub-agent. |
| Blaming individuals by name | Reference roles, not names. |
| Mermaid for simple timelines | 3 events do not need a diagram. |
| Document language differs from conversation | Match throughout. |

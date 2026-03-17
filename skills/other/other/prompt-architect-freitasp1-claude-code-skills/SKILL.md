---
name: prompt-architect
description: |
  Transformiert Anforderungen in Best-Practice Prompts nach Claude 4.x Standards (Dezember 2025).
  
  Basiert auf:
  - Nate B. Jones 4 Beginner Moves: Shape, Context, Silent Plan, Self-Check
  - Anthropic Claude 4.x Best Practices: Explizitheit, Contract-Style, Examples beat Adjectives
  - Pipelines over Prompts Philosophie
  
  AKTIVIERT SICH AUTOMATISCH nach clarify-spec oder bei /prompt-architect.
  Produziert strukturierten, ausfuehrbaren Prompt mit allen Best Practices.
triggers:
  - /prompt-architect
  - /prompt
  - /architect
  - /build-prompt
---

# Prompt-Architect: Best-Practice Prompt Generator

## Basiert auf Claude 4.x Best Practices (Dezember 2025)

### Quellen:
- Nate B. Jones Prompting Playbook 2025
- Anthropic Official Claude 4.x Prompting Guide
- Claude Code Best Practices

## AKTIVIERUNG

### Automatisch nach clarify-spec
Wenn clarify-spec ein JSON Output generiert hat, kann prompt-architect
dieses JSON in einen strukturierten Prompt transformieren.

### Manuell mit Trigger
/prompt-architect [Aufgabenbeschreibung]

## Die 4 Beginner Moves (Nate B. Jones)

### Move 1: Define the Shape of Output
NICHT: Schreib guten Code
SONDERN: Produziere eine TypeScript-Datei mit Interface X, exportiere Funktion Y

Konkrete Artefakte definieren:
- Welche Dateien werden erstellt/geaendert?
- Welches Format hat der Output?
- Wie sieht ein Beispiel-Output aus?

### Move 2: Give Minimal but Sufficient Context
- Automatisch relevante Dateien einlesen
- CLAUDE.md/AGENTS.md Auszuege
- Nur das Noetige - kein Context-Overflow
- Token Budget beachten

### Move 3: Suggest a Silent Plan
- Claude soll INTERN planen bevor es antwortet
- Bei Claude 4.5: consider your approach first
- Vermeidung von think bei deaktiviertem Extended Thinking

### Move 4: Add a Quick Self-Check
- Evaluator-Block am Ende des Prompts
- Checkliste: Format eingehalten? Constraints erfuellt?
- Before responding, verify: [checklist]

## Claude 4.x Spezifische Patterns

### Explizitheit + Modifier
NICHT: Create dashboard
SONDERN: Create dashboard. Include as many relevant features as possible. Go beyond the basics.

### Context + Motivation (WARUM erklaert WAS)
NICHT: NEVER use ellipses
SONDERN: Your response will be read aloud by TTS, so never use ellipses since TTS cannot pronounce them.

### Examples beat Adjectives
NICHT: Schreib professionell
SONDERN: Beispiel-Output zeigen, Format demonstrieren

### XML-Tags fuer Struktur
<output_structure>, <constraints>, <verification>

### Uncertainty Permission
If unsure, state explicitly and ask clarifying question.
Reduziert Halluzinationen drastisch.

## Das Contract-Style Template

Nach Analyse des Auftrags, generiere diesen strukturierten Prompt:

---BEGIN GENERATED PROMPT---

## ROLE and GOAL
You are: [Rolle basierend auf Task-Typ, z.B. Senior TypeScript Developer]
Goal: [Konkrete Erfolgsdefinition in 1 Satz aus clarified_task.goal]

## CONTEXT
[Automatisch gesammelt:]
- Projekt: [Projektname aus CLAUDE.md]
- Relevante Dateien: [Liste mit kurzem Inhaltsuebersicht]
- Bestehende Patterns: [Aus Codebase extrahiert]
- No-Touch Zones: [Aus clarified_task.scope.no_touch]

## CONSTRAINTS
- [Constraint 1 als Bullet aus clarified_task.constraints]
- [Constraint 2 als Bullet]
- [Max 5 Constraints]
- If unsure about any aspect: State explicitly and ask for clarification

## TASK
[Klare Aufgabenbeschreibung aus clarified_task.goal + problem_statement]

### Success Criteria
- [Kriterium 1 aus clarified_task.success_criteria]
- [Kriterium 2]
- All existing tests must pass

### Examples (if examples_needed = true)
Input: [Beispiel-Input]
Expected Output: [Erwarteter Output]

## OUTPUT FORMAT
<output_structure>
[Exaktes Format basierend auf Task-Typ:]
- Fuer Code: Vollstaendige Dateien, keine Diffs, keine Platzhalter
- Fuer Docs: Markdown mit Headings
- Fuer Config: JSON/YAML mit Kommentaren
</output_structure>

## VERIFICATION (Self-Check)
Before responding, verify:
[ ] Output format followed exactly?
[ ] All constraints from CONSTRAINTS section satisfied?
[ ] All success criteria from TASK section met?
[ ] Uncertain claims marked with [UNCERTAIN]?
[ ] No changes to No-Touch Zones?

---END GENERATED PROMPT---

## Workflow

### Schritt 1: Input analysieren

Akzeptiert:
1. JSON von clarify-spec (bevorzugt)
2. Freie Textbeschreibung
3. Kombiniert mit aktuellem Projekt-Kontext

### Schritt 2: Kontext automatisch sammeln

- Glob fuer relevante Dateien
- Read CLAUDE.md/AGENTS.md
- Identify No-Touch Zones
- Extract existing patterns from codebase

### Schritt 3: Template ausfuellen

Fuelle das Contract-Style Template mit:
- Role basierend auf Task-Typ (Frontend, Backend, DevOps, etc.)
- Goal aus clarified_task.goal
- Context aus Projekt-Analyse
- Constraints aus clarified_task.constraints
- Task aus goal + problem_statement
- Output Format basierend auf erwarteten Artefakten
- Verification Checklist

### Schritt 4: Prompt praesentieren

Zeige den generierten Prompt dem User:

---
## Generierter Best-Practice Prompt

[Vollstaendiger Prompt hier]

---
Optionen:
- ausfuehren: Diesen Prompt jetzt ausfuehren
- anpassen: Prompt modifizieren
- kopieren: Prompt in Zwischenablage
- speichern: Als Template speichern

### Schritt 5: Ausfuehrung

Bei ausfuehren:
1. Prompt intern verwenden
2. Mit Quality Gates (wenn /supervisor aktiv)
3. Ergebnis praesentieren

## Beispiel: Vom vagen Auftrag zum Best-Practice Prompt

### Input (von clarify-spec):
{
  clarified_task: {
    goal: PPTX-Export fixen, damit AI-Bilder zuverlaessig erscheinen,
    problem_statement: Bilder fehlen manchmal im PPTX-Download,
    scope: {
      files: [presentationBuilder.ts, chartVisualGenerator.ts],
      no_touch: [api/analyze.ts]
    },
    success_criteria: [Alle Bilder erscheinen, Unter 500KB, Keine Errors],
    constraints: [Keine Breaking Changes]
  }
}

### Output (generierter Prompt):

## ROLE and GOAL
You are: Senior TypeScript Developer specializing in browser-based file generation
Goal: Fix PPTX export so AI-generated images reliably appear in downloaded files

## CONTEXT
- Projekt: fabrikIQ Analyzer (Manufacturing AI Platform)
- Relevante Dateien:
  - presentationBuilder.ts: PptxGenJS integration, slide generation
  - chartVisualGenerator.ts: Gemini image generation, base64 handling
- Bestehende Patterns: Async/await, try-catch error handling
- No-Touch Zones: api/analyze.ts (core analysis)

## CONSTRAINTS
- No breaking changes to existing PPTX export functionality
- Images must be compressed to under 500KB
- Maintain existing error handling patterns
- If unsure about any aspect: State explicitly and ask

## TASK
Fix the PPTX export to ensure AI-generated images reliably appear in downloads.
The current issue: Images sometimes fail to appear in the final PPTX file.

### Success Criteria
- All AI-generated images appear in PPTX
- Image file size under 500KB each
- No console errors during download
- Existing tests still pass

## OUTPUT FORMAT
<output_structure>
Provide complete, modified TypeScript files.
No diffs, no placeholders, no partial implementations.
Include brief comments explaining key changes.
</output_structure>

## VERIFICATION
Before responding, verify:
[ ] All images will be embedded correctly?
[ ] Compression logic handles edge cases?
[ ] No changes to api/analyze.ts?
[ ] Error handling covers network failures?

## Token-Effizienz

Der generierte Prompt ist optimiert fuer:
- Minimaler Context (nur relevante Infos)
- Maximale Klarheit (keine Ambiguitaet)
- Self-Verification (reduziert Iterationen)

## Integration

### Mit clarify-spec
clarify-spec -> JSON -> prompt-architect -> Ausfuehrung

### Mit /supervisor
prompt-architect -> Prompt -> /supervisor -> Quality Gates -> Ergebnis

### Standalone
/prompt-architect [Aufgabe] -> Prompt -> Ausfuehrung

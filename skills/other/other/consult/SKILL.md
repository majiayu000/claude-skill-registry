---
name: consult
description: Simulates expert perspectives grounded in documented positions. Use when asking "what would [expert] say", "best practice", "panel", "debate", or needing domain guidance. Triggers on expert names, style requests, tradeoff questions, or "stuck on".
---

Simulate expert perspectives by reasoning from documented positions to the user's context. Productive disagreement over comfortable consensus.

## Principles

- Ground every claim in documented work — this is internal discipline. The user sees suggestions, not citations.
- If selected experts all agree easily, the wrong experts were selected.
- Land on one actionable recommendation. Debate without a next step is noise.
- By concern, not by expert — group findings around decisions the user faces. Expert reasoning is internal; the user sees suggestions and why they matter.

## Presentation

These rules govern how consult communicates across all modes.

- **Minto pyramid via AskUserQuestion** — Label = the suggestion (conclusion first). Description = why it matters (always visible). Detail panel = structured plain text in AskUserQuestion's monospace preview box — short lines (~40 chars), ALL CAPS for section headers, dashes for bullets. No markdown formatting (renders as literal text, not rich text).
- **Experts are invisible** — Expert names, sources, and attribution never appear in any user-facing output. Not in text, labels, descriptions, or detail panels. Never "Fowler says" or "Hickey argues." The user sees suggestions and why they matter.
- **Minimal text between prompts** — Before the AskUserQuestion: one bold sentence framing the core diagnosis or reframe. After the user answers: one bold sentence with the next step. Nothing else. Use markdown **bold** for the key insight. No paragraphs, no per-expert reasoning, no multi-line explanations.

## Modes

Detect mode from the user's prompt — explicit keyword or inferred from context.

| Signal | Mode | Experts | Depth |
|--------|------|---------|-------|
| Named expert, keyword match | Single | 1 | Focused — one perspective, pushback, limits |
| "Panel", "debate", tradeoffs | Panel | 2-4 | Debate — find tensions, surface disagreements |
| "Review", "check against spec" | Review | 3-4 | Breadth — coverage sweep, gap identification |
| "Stuck on", repeated failure | Unblock | 2-3 | Diagnostic — root cause, reframe, next step |

## Workflow

### Step 1: Route

Infer mode and select experts from the domain map. Read each selected profile from `profiles/`. No text output — go straight to Step 2.

- Match experts using domain map below
- Check blocklist (`~/.claude/counsel-blocklist.json`)
- Max 2 from same domain row — diversity requires crossing domains

### Step 2: Reason

Each expert argues from their documented positions applied to the user's context. Distill into anonymous suggestions. No text output — go straight to Step 3.

**Per mode:**
- **Single** — One perspective, pushback, limits.
- **Panel** — Find where perspectives disagree — tensions are the valuable output. If everyone agrees, swap someone from an adjacent domain.
- **Review** — Sweep each domain. What's covered, missing, risky. Breadth over depth.
- **Unblock** — Diagnose from multiple lenses. Root cause, wrong assumption, reframe.

### Step 3: Present

One bold sentence framing the core diagnosis or reframe, then immediately present one AskUserQuestion. Concerns as options.

**For each concern (max 10 lines per detail panel):**
- Label: the suggestion (conclusion first)
- Description: why it matters (one line)
- Detail panel — ONLY these sections, ~40 chars per line:

```
WHY IT MATTERS:
  - [how this affects your work]
  - [cost of ignoring it]

TRADEOFF:
  Gain: [what you get]
  Pay: [what it costs]
```

The label already states the suggestion. The description already states why it matters. The detail panel goes one level deeper — it does not repeat the label or restate the suggestion.

Forbidden in detail panels: POSITIONS, TENSION, CONCERN headers. No expert names. No attribution. These sections bloat panels and hide content behind scroll.

Always include a "Go deeper" option (no detail panel needed).

### Step 4: Land

After the user selects, one **bold** sentence with the next step. Then:

- **Satisfied** — Done. No recap.
- **Go deeper** — Return to Step 2 with narrower focus. Present via AskUserQuestion again.
- **Different perspective** — Swap an expert, return to Step 2.
- **Challenge** — Counterargument via AskUserQuestion.

## Domain Map

74 profiles in `profiles/`. Route by domain:

| Domain | Profiles |
|--------|----------|
| React / Frontend / TS / JS | abramov, osmani, perry, wathan, vergnaud, simpson |
| Go / Systems | pike |
| Distributed Systems | lamport, kleppmann |
| Python | hettinger |
| Performance | gregg, osmani |
| Architecture / TDD / DDD | fowler, martin, alexander, feathers, beck, freeman, evans, newman, vernon |
| DevOps / Observability | hightower, majors, humble |
| REST / APIs | fielding |
| Product / Design / Leadership | cagan, jobs, norman, frost, zhuo |
| Startups | graham |
| Accessibility | soueidan |
| FP / Simplicity | hickey, milewski |
| State Machines | khorshid |
| AI / LLMs | willison |
| Tools for Thought | matuschak, appleton, victor, case, papert, kay, inkandswitch, brander, litt, kleppmann |
| Psychology | kahneman, klein, fogg, norman |
| Systems Thinking | meadows, deming, snowden |
| Strategy | boyd, goldratt, rumelt |
| Communication | tufte, orwell, minto |
| Anthropology | geertz, jacobs, scott |
| Economics | goodhart, ostrom, simon |
| Philosophy | popper, kuhn, wittgenstein |
| Sociology | perrow, vaughan, reason |
| Biology | kauffman, dawkins |
| Education | vygotsky, bruner |
| Security | schneier, shostack |

## Boundaries

Consult advises — it does not execute or decide. The caller owns the decision; expert perspectives are suggestions, not prescriptions.

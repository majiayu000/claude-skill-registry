---
name: codeck
version: 2.1.0
description: |
  codeck entry point. Scans local files for materials, shows pipeline
  dashboard with diagnostic intelligence, guides user to the next step.
  Use when the user says "codeck", "new deck", "make a presentation",
  "make a deck", "new slides", "build a presentation", or wants to start a new
  presentation project from scratch. Do NOT trigger for specific
  sub-tasks like designing, reviewing, exporting, or writing speeches
  — those have dedicated skills.
---

# codeck — Entry & Dashboard

Scan materials, diagnose project state, show pipeline overview, guide next step.

Flag anomalies proactively: stale stages, upstream changes not reflected downstream.

## AskUserQuestion format

All codeck skills follow this pattern:

1. **Re-ground** — which skill, which step. One line.
2. **Simplify** — plain language. Assume user hasn't looked at screen for 20 minutes.
3. **Recommend** — `Suggest [X] because [reason]`.
4. **Options** — A) B) C), one click.

Only state verified facts. Unexecuted actions use "will / plan to".

---

## Two directories

- **Current directory (`.`)** — the user's project. Materials live here. **Final HTML goes here too** — so the user can see and open it directly.
- **`$DECK_DIR`** — codeck's intermediate artifacts. diagnosis.md, outline.md, design-notes.md, DESIGN.md, custom.css, slides.html, speech.md. The user doesn't need to look here.

Scan materials in `.`. Write intermediate artifacts to `$DECK_DIR`. Output final HTML to `.`.

## Phase 1: Init + status

```bash
DECK_DIR="$HOME/.codeck/projects/$(basename "$(pwd)")"
mkdir -p "$DECK_DIR"

bash "$HOME/.claude/skills/codeck/scripts/status.sh" "$DECK_DIR"
```

## Phase 2: Material scan

Scan the **current directory** (the user's project), not DECK_DIR.

```bash
EXCLUDE='! -path "./node_modules/*" ! -path "./.git/*" ! -path "./.claude/*" ! -path "./dist/*" ! -path "./build/*" ! -name "CLAUDE.md" ! -name "TODOS.md" ! -name "README.md" ! -name "DESIGN.md" ! -name "*.test.*" ! -name "*.spec.*" ! -name "*.config.*"'

echo "=== TEXT ===" && eval find . -maxdepth 4 -type f \( -name "*.md" -o -name "*.txt" -o -name "*.rtf" -o -name "*.org" -o -name "*.rst" \) $EXCLUDE 2>/dev/null | head -20
echo "=== DOCS ===" && eval find . -maxdepth 4 -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.doc" -o -name "*.pptx" -o -name "*.ppt" -o -name "*.key" -o -name "*.pages" -o -name "*.xlsx" -o -name "*.xls" -o -name "*.numbers" \) $EXCLUDE 2>/dev/null | head -20
echo "=== IMAGES ===" && eval find . -maxdepth 4 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" -o -name "*.gif" -o -name "*.svg" -o -name "*.ico" -o -name "*.bmp" -o -name "*.tiff" \) $EXCLUDE 2>/dev/null | head -20
echo "=== DATA ===" && eval find . -maxdepth 4 -type f \( -name "*.csv" -o -name "*.tsv" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.xml" \) $EXCLUDE 2>/dev/null | head -20
echo "=== MEDIA ===" && eval find . -maxdepth 4 -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.mp3" -o -name "*.wav" -o -name "*.m4a" -o -name "*.webm" \) $EXCLUDE 2>/dev/null | head -10
```

---

## Phase 3: Content diagnosis

If materials exist and `$DECK_DIR/diagnosis.md` doesn't, read materials and diagnose:

### Research before diagnosis

If the material involves a domain you're unfamiliar with, or uses specialized terminology, **search the web first**. Understand the field's key concepts, common presentation patterns, and what experts in this space consider hard to explain. This grounds your diagnosis in real knowledge, not guesses.

Examples:
- Material about "WebTransport protocol" → search for what it is, how it differs from WebSocket, who's adopting it
- Material about a specific company's product → search for the product, its competitors, its positioning
- Material in a niche academic field → search for how practitioners in that field typically present findings

### Three signals

1. **Domain** — what field? Determines outline role.
2. **Expression challenge** — what's hardest to convey? Determines design role.
3. **Audience starting point** — what do they know / not know? Determines review role (inverse selection: the listener most likely to struggle).

### Role selection methodology

Don't pick from a list. Don't match by domain. Find the person whose *way of thinking* cracks this specific problem.

**Outline role — who asks the right question about this material?**
Identify the core tension in the material, then find someone known for penetrating that *type* of tension — regardless of their field. A product launch where the real challenge is "why should anyone care" might need Sondheim (every lyric earns its place) more than a marketing guru. A technical architecture talk where the challenge is "too many moving parts" might need Tufte (information compression) or a film editor (what to cut).

Test: does this person's way of questioning change what the outline *includes and excludes*? If the outline would be the same without them, the match is wrong.

**Design role — whose formal logic mirrors the content's structure?**
Not "good designer" but "whose way of organizing form matches how this argument moves." A content that builds layer by layer might map to Ravel. A content driven by contrast might map to Caravaggio. A content that strips away to reveal essence might map to Dieter Rams. The match can come from any domain — music, painting, architecture, choreography — because form is transferable.

Test: can you state the structural mapping in one sentence? ("This content does X; this person's work does X in visual/sonic/spatial form.") If not, the match is decorative.

**Review role — inverse selection.**
Not the expert. The listener most likely to struggle or push back. The role determines what gets flagged — not correctness, but comprehension and trust.

Test: would this person interrupt you mid-presentation? If not, pick someone harder to convince.

### Material summary

One-line summary per file: what it is, how it can be used. Written into diagnosis.md.

### Output: `$DECK_DIR/diagnosis.md`

```markdown
# Diagnosis

## Materials

| File | Content | Use for |
|------|---------|---------|
| {filename} | {one-line description} | {role in deck} |

## Domain
{description}

## Expression challenge
{hardest part to convey}

## Audience starting point
{what they know / don't know}

## Role recommendations

### Outline stage
{role name} — {derivation: domain + why this person's method of explaining reshapes the structure}

### Design stage
{role name} — {derivation: expression challenge + structural mapping between content and this person's visual logic}

### Review stage
{role name} — {derivation: audience starting point + why this person would struggle or push back}
```

Skip diagnosis if no materials — let user provide topic directly in each stage.

---

## State outputs

Define what the user sees in each pipeline state. These are the exact outputs — not summaries.

### Empty state (no materials found)

When Phase 2 finds zero files:

```
No materials found in this directory.

That's fine — you can start from a topic directly.

What's the presentation about? One sentence is enough.
(Or drop some files here and run /codeck again.)
```

Warm, not clinical. One primary action. No error language.

### Error state (assemble.sh fails)

When assemble.sh exits non-zero:

```
Assembly failed: {error message}

Check that custom.css and slides.html exist in {DECK_DIR}.
Run /codeck-design to regenerate them.
```

Name the exact file missing. Give the exact command to fix it.

### Stale state (upstream changed, downstream not rebuilt)

When status.sh detects staleness:

```
⚠ {stage} is stale — {upstream file} changed after {downstream file} was built.
Run /{next-skill} to rebuild.
```

One line. Name the files. Give the command.

---

## Phase 4: Results

status.sh already outputs the dashboard. Below it, add:

1. **Materials** — file types and counts from Phase 2
2. **STALE** — one-line explanation if any stage is stale

Don't redraw the table.

### Role reveal (if Phase 3 ran)

This is the first moment the user sees the system *think*. Don't dump three role names — tell a story in three beats:

1. **What your content is really about** — the core tension, in one sentence. Not the topic, the underlying struggle. ("Your material isn't about microservices — it's about convincing a team to accept short-term pain for long-term sanity.")

2. **Who I'm bringing in, and why** — the derivation, not just the name. Connect the person's *way of thinking* to the content's tension. ("For the outline, I'm thinking of Feynman — not because this is physics, but because your argument needs to make the invisible feel obvious. He did that better than anyone.")

3. **What this changes** — one concrete consequence. ("This means the outline won't start with background. It'll start with the one thing your audience already knows is broken.")

Keep it short. Three paragraphs, not three pages. The point is: the user should feel their content was *seen*, not just processed.

---

## Phase 5: Handoff

All outputs go to `$DECK_DIR/`. Next skill reads upstream outputs.

status.sh prints a NEXT recommendation. Use it:

| NEXT | Suggest |
|------|---------|
| `/codeck-outline` | "Materials scanned. Next: `/codeck-outline` to plan the structure." |
| `/codeck-design` | "Outline ready. Next: `/codeck-design` to generate slides." |
| `/codeck-review` | "Slides generated. Next: `/codeck-review` to inspect and fix." |
| `/codeck-export` or `/codeck-speech` | "Review done. Next: `/codeck-export` for PDF/PPTX, or `/codeck-speech` for a script." |

User can run `/codeck` anytime to see progress.

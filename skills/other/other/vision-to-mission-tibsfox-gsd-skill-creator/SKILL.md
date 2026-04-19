---
name: vision-to-mission
description: "Transform a user's builder vision into a complete, executable GSD mission package. Use this skill whenever a user has described what they want to BUILD (a product, tool, feature, system, educational pack, or ecosystem component) and wants it structured for GSD execution. Triggers include: 'structure this for GSD', 'make this into a milestone', 'turn this vision into a mission', 'package this up for Claude Code', 'create the mission files', 'I want to hand this to GSD', 'make me a mission package', or any request to decompose a described system into wave-based executable tasks. Also trigger when the user has a vision doc already written and needs mission decomposition. Prefer this skill over generic document creation whenever the GSD ecosystem is mentioned alongside building something."
type: skill
category: research
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/research/vision-to-mission/SKILL.md
superseded_by: null
---
# Vision → Mission Skill

Transform a user's builder vision — described in conversation — into a complete, GSD-ready mission package: a structured folder of markdown files ready for handoff to Claude Code and the GSD orchestrator.

**This skill produces builders' output, not researchers' output.** It generates the executable files: milestone spec, component specs, wave plan, test plan, and README. Compare with `research-mission-generator`, which produces a LaTeX research document. Use this skill when the goal is to *build* something.

---

## Pipeline Speed Detection

Detect which pipeline the conversation warrants — **do not ask the user** unless genuinely ambiguous.

| Speed | When | Stages Produced |
|-------|------|-----------------|
| **Full** (Vision → Research → Mission) | Domain requires professional accuracy, safety, or cultural sensitivity (electronics, nutrition, cultural heritage, medical) | All three stages |
| **Fast** (Vision + Mission, skip research) | Domain within Claude's training, pure software/tooling, internal GSD components | Vision doc + mission files |
| **Mission-only** | User already has a vision doc, needs decomposition | Mission files only |

---

## Step 1: Harvest the Conversation

Scan the current conversation (and past conversations if referenced) for:

| Element | Where to Find It | Fallback |
|---------|-------------------|----------|
| **What to build** | User's description, framing, analogies | Ask one targeted question |
| **Why it matters** | User's motivation, problem statement | Infer from context |
| **Architecture hints** | ASCII diagrams, component lists, agent descriptions | Derive from vision |
| **Existing dependencies** | Other GSD vision docs referenced | Search past conversations |
| **Success picture** | "Done looks like..." statements | Synthesize from goals |
| **Safety/sensitivity** | Domain signals (cultural content, health, electronics) | Detect from domain |
| **User's metaphors** | Analogies, framings, philosophical arcs | Carry into vision narrative |
| **Thinking time sessions** | User stream-of-consciousness while Claude listened | Highest priority — preserve verbatim insights |

**Critical:** Preserve the user's own language. Their metaphors, framings, and analogies belong in the vision narrative. Don't replace user thinking with generic content.

---

## Step 2: Identify the Archetype

Read `references/vision-archetypes.md` to classify the vision. Each archetype has characteristic components, common failure modes, and chipset patterns. Classification shapes the output structure.

Quick reference:

| Archetype | Key Signals | Mission Shape |
|-----------|-------------|---------------|
| **Educational Pack** | Curriculum, modules, Try Sessions, cultural content | Safety Warden mandatory; 6–10 components |
| **Infrastructure Component** | Filesystem contracts, message schemas, APIs, technical spec | Schema-first Wave 0; 4–6 components |
| **Organizational System** | Roles, activation profiles, responsibilities, communication | Role mapping Wave 0; 5–8 components |
| **Creative Tool** | UX/workflow, rendering pipeline, user experience | UX-first prototyping; 4–7 components |
| **Agent/Skill Pack** | Agents, skills, skill-creator integration, chipset | Chipset YAML central; 5–9 components |
| **Research Mission** | Surveys, findings, academic structure, evidence | Use research-mission-generator instead |

---

## Step 3: Draft the Vision Document (if needed)

Skip if the user already has a vision doc. Otherwise, write `01-vision-doc.md` from harvested content.

See `references/mission-templates.md` → **Vision Document Template** for the complete structure.

**Vision doc quality gates (run before proceeding):**
- [ ] Narrative makes someone *want* to build this (not a spec — a destination)
- [ ] Problem statement has 3–5 concrete, recognizable problems
- [ ] Core concept described in one interaction arc sentence
- [ ] ASCII architecture diagram present
- [ ] Chipset YAML configures the actual agents needed
- [ ] Success criteria are testable by an agent (8–12 criteria)
- [ ] No function signatures in the vision (those belong in component specs)
- [ ] Through-line connects to a GSD ecosystem principle

---

## Step 4: Research Reference (Full Pipeline Only)

For Full pipeline speed only. Otherwise skip.

Conduct targeted web research using these source quality rules (**ABSOLUTE**):
- Government agencies (USGS, NIH, NASA, EPA, NIST, etc.)
- Peer-reviewed journals and university research
- Professional organizations and official standards bodies
- **NEVER** entertainment media, blogs, or unsourced claims

Structure as `02-research-reference.md`. See `references/mission-templates.md` → **Research Reference Template**.

---

## Step 5: Decompose into Components

Identify 4–12 components based on complexity. Each component maps to one Claude Code agent invocation. Every component spec must pass the **self-containment test**: delete every other file, hand an agent this one spec — can they build it? Yes = done. No = copy more context in.

**Component sizing guide:**

| Complexity | Components | Examples |
|-----------|-----------|---------|
| Simple feature | 4–5 | Dashboard widget, API endpoint |
| Medium system | 6–8 | Plugin architecture, persona system |
| Complex pack | 8–12 | Educational pack, full skill suite |
| Mega-milestone | 12–20 | Electronics course, foundational knowledge suite |

**Component decomposition principles:**
1. One component = one agent invocation = one verifiable artifact
2. Components have clear inputs (what they receive) and outputs (what they produce)
3. Shared types and schemas are always Wave 0, separate from implementation components
4. Integration and verification are always final wave, never parallelized with build work

---

## Step 6: Assign Models

Apply the 30/60/10 principle. If >40% requires Opus, the vision needs further decomposition.

| Complexity Signal | Model | Examples |
|------------------|-------|---------|
| Judgment, creativity, architecture | **Opus** | Personality design, safety warden logic, activation engines, cultural sensitivity, factory/meta-systems |
| Structural implementation | **Sonnet** | Schema definitions, pipelines, registries, test suites, documentation, content generation from patterns |
| Scaffold and boilerplate | **Haiku** | Directory structures, config files, type stubs, templates, simple transformations |

---

## Step 7: Plan Waves

See `references/mission-templates.md` → **Wave Execution Plan Template** for the output format.

**Wave planning principles:**
1. **Wave 0 always exists** — shared types, schemas, interfaces; must complete within 5-min cache TTL
2. **Push to parallel** — any components without shared state should run simultaneously
3. **Safety is never parallel** — Safety Warden is always on the critical path, final wave
4. **Integration after parallel** — Wave N-1 builds; Wave N integrates and verifies
5. **Cache-aware sequencing** — Wave 0 producers start Wave 1 consumers before TTL expires

**Activation profiles** (scale crew size to component count):

| Components | Profile | Parallel Tracks |
|-----------|---------|-----------------|
| 2–4 | Patrol (7 roles) | 1 |
| 5–8 | Squadron (12 roles) | 2 |
| 9+ | Fleet (full) | 3+ |

---

## Step 8: Write the Test Plan

See `references/mission-templates.md` → **Test Plan Template**.

Test density targets:
- 2–4 tests per success criterion from the vision doc
- Safety domains: ≥15% mandatory-pass tests
- Integration tests for every component boundary

Reference test densities from production milestones:
- skill-creator: 202 tests, ~4.0 per criterion
- Electronics Pack: ~200 tests, 25 safety-critical

---

## Step 9: Produce the Package

Write all files to a mission folder named `[milestone-name]-mission/`. File manifest:

```
[milestone-name]-mission/
├── README.md                    ← Index, how-to-use, execution summary table
├── 01-vision-doc.md             ← Stage 1 (skip if user provided)
├── 02-research-reference.md     ← Stage 2 (Full pipeline only)
├── 03-milestone-spec.md         ← Mission objective, deliverables, constraints
├── 04-wave-execution-plan.md    ← Wave/track structure, cache strategy, token budget
├── 05-test-plan.md              ← All test categories, verification matrix
└── components/
    ├── 00-shared-types.md       ← Wave 0: schemas, interfaces (always present)
    ├── 01-[component-a].md      ← Wave 1 components (one file per component)
    ├── 02-[component-b].md
    └── ...
```

After writing all files, zip the folder:
```bash
cd /home/claude && zip -r [milestone-name]-mission.zip [milestone-name]-mission/
cp [milestone-name]-mission.zip /mnt/user-data/outputs/
```

---

## Step 10: Deliver

Present the zip file and a brief summary. Keep it short — the user can read the documents. Mention:
- Total component count and wave structure
- Activation profile (Patrol/Squadron/Fleet)
- Opus/Sonnet/Haiku split
- How to hand it to Claude Code (`claude --new-task` or GSD `new-project`)

---

## Ecosystem Patterns (Mandatory — Apply to All Output)

### Mission Control Pattern
"We are the architects. Claude Code is the astronaut. Each mission doc is a complete flight plan." Every component spec self-contained. No spec may say "see the other specs."

### Safety Warden Pattern
Three modes: **annotate** (flag for awareness), **gate** (confirm before proceeding), **redirect** (block + suggest alternative). Safety monotonicity: children never relax parent safety boundaries.

### Progressive Disclosure Pattern
Three reading speeds in all output: glance (title + summary line), scan (headers + tables), read (full body).

### Humane Flow Pattern
Systems support, never shame. No guilt messaging. The system says "Welcome back."

### Amiga Principle
Remarkable results through architectural intelligence, not raw power. Specialized execution paths. Every architectural decision should ask: "Is there a clever structural solution that makes the brute-force approach unnecessary?"

---

## Common Mistakes to Avoid

1. **Vision docs that are specs.** Vision = destination. No function signatures.
2. **Missions requiring other missions.** Each component is self-contained. Period.
3. **Everything assigned to Opus.** Most work is structural. Save Opus for judgment.
4. **Sequential waves that could be parallel.** No shared state → parallelize.
5. **Missing the cache window.** Wave 0 must complete in <5 min.
6. **Test plans mirroring criteria 1:1.** Tests ≥ criteria × 2.
7. **Skipping the through-line.** Keeps the milestone aligned with GSD values.
8. **Generic vision narratives.** The user's own metaphors must appear in the vision.

---

## Reference Files

- `references/vision-archetypes.md` — Detailed archetype patterns, characteristic components, chipset YAML patterns, common failure modes. **Read for complex systems before writing the vision doc.**
- `references/mission-templates.md` — Complete templates for every output file (Vision Doc, Research Reference, Milestone Spec, Component Spec, Wave Execution Plan, Test Plan, README). **Read before generating any mission file.**

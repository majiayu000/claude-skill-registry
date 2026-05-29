---
name: synapptic
description: "synapptic — The missing feedback loop for agentic development. Builds a living user model from AI coding session transcripts. Extracts user preferences, AI failure patterns, and behavioral guards, then writes them to the memory system so every new session starts informed. Use this skill whenever the user mentions: synapptic, user profile, user archetype, session analysis, extract observations, update profile, profiling sessions, user model, guards, known weaknesses, AI failures, behavioral rules, or wants to analyze how they work with their AI coding assistant. Also trigger when the user asks to 'process sessions', 'update the archetype', 'show my profile', 'what do you know about me', 'run synapptic', or wants to improve the AI's understanding of their preferences."
---

# synapptic

The missing feedback loop for agentic development. Builds a living user model from AI coding session transcripts — extracts who the user is, what the AI keeps getting wrong, and what rules would prevent those mistakes. Writes the result to the memory system so every new session starts informed.

## Commands

### Full pipeline (most common)

```bash
synapptic ingest                    # extract → merge → synthesize → integrate
```

Finds unprocessed transcripts, filters them (~626x compression), extracts observations via LLM, merges into weighted profiles, synthesizes narrative archetypes, and writes to all project memory directories.

Options: `--model sonnet` (default), `--max-tokens 50000`, `--project <name>`, `--min-lines 20`.

### Step-by-step

```bash
synapptic extract --all             # extract all unprocessed sessions
synapptic extract -s <UUID>         # extract one session
synapptic merge                     # merge observations into profiles
synapptic synthesize                # generate narrative archetypes
synapptic profile                   # show weighted preferences
synapptic profile -p <project>      # show project-specific profile
synapptic archetype                 # show narrative archetypes
synapptic stats                     # session counts, profile versions, per-project breakdown
synapptic diff                      # changes since last profile version
synapptic rollback                  # restore previous profile version
synapptic reset                     # delete all state and start fresh
synapptic install                   # set up skill + hook + settings.json
synapptic uninstall                 # clean removal, prompts before deleting data
```

## Architecture

### Two-level profiles: global + per-project

```
~/.synapptic/
├── global/                        # who you are (same across all projects)
│   ├── observations/
│   ├── profile.yaml
│   └── archetype.md
├── projects/
│   ├── <project-slug>/            # what goes wrong in this project
│   │   ├── observations/
│   │   ├── profile.yaml
│   │   └── archetype.md
│   └── ...
└── profile_history/               # versioned snapshots for rollback
```

### Dimension routing

| Dimension | Routing | What it captures |
|-----------|---------|-----------------|
| `communication` | Global | Style, tone, verbosity preference |
| `workflow` | Global | Read-first, verify patterns, commit habits |
| `values` | Global | Correctness, speed, safety priorities |
| `expertise` | Global | Skill levels, domain knowledge |
| `expectations` | Mixed | Autonomy level, explanation depth |
| `triggers` | Mixed | Frustration and satisfaction signals |
| `ai_failures` | Project | Specific mistakes the AI made |
| `guards` | Project | Preventive rules derived from failures |
| `code_style` | Project | Formatting, imports, naming conventions |

Mixed dimensions start per-project and promote to global when seen across 2+ projects.

### Three-tier data flow

**Tier 1 — Observations** (append-only, per session): Raw observations extracted by LLM. Stored as JSON with embedded project metadata.

**Tier 2 — Weighted Profile** (accumulated, decayed): All observations merged with exponential decay (0.98x per cycle). Similar observations reinforce each other. Old patterns fade unless seen again.

**Tier 3 — Narrative Archetype** (what the AI reads): Three sections — User Archetype, Guards (behavioral rules), Known Weaknesses. Written to memory system with proper frontmatter.

### Profile-aware extraction

When a profile already exists, the extraction prompt includes top existing observations so the LLM skips known patterns and focuses on genuinely new signal.

### Transcript filtering

Session transcripts can be 500MB+. The filter reduces them to ~50K tokens (~626x compression) by stripping progress records, tool output, thinking blocks — keeping only user text + assistant text as conversation pairs, with heuristic boosting for correction signals and strong reactions.

## SessionEnd hook

A hook runs `synapptic ingest` in the background after every session (fully detached, zero exit lag). PID-locked to prevent stacking. If it fails, the next session's hook catches up — nothing is permanently lost.

## Guards

Guards are the most valuable output — concrete behavioral rules derived from observed failures:

```
ALWAYS read the file before modifying it
NEVER commit without running tests first
BEFORE implementing a new service, read an existing one of the same type
WHEN the user specifies a verification path, treat it as a hard constraint
IF debugging produces no signal after 2-3 attempts, stop and ask
```

Each guard traces to a specific failure with evidence. Guards enter the archetype immediately (no multi-session evidence requirement) because a concrete failure is actionable from a single observation.

## Technical notes

- Uses `claude -p --tools ""` for LLM calls — `--tools ""` prevents the AI from running tools during extraction/synthesis
- Extraction: ~$0.50-2.00 per session. Synthesis: ~$0.10 per run
- All subprocess calls have 300s timeout with cleanup on interrupt
- Atomic writes for profile.yaml and settings.json
- Concurrent `update` runs are safe — idempotent by design

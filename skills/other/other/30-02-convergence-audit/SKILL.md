---
name: 30-02-convergence-audit
description: Find semantic duplication — different code doing the same thing written by different sessions. Walks the codebase, adds @purpose markers, builds an intent registry, and flags convergence failures. Uses Delphi for full audits.
---

# 30.02 Convergence Audit

## The Problem

LLM-authored codebases accumulate **semantic duplication** — different code implementing the same intent, written by different sessions that don't know about each other. This isn't copy-paste. It's three functions that build the same Discord message with slightly different formatting, or two config parsers reading the same env var with different defaults.

Grep can't find it. The agent that wrote path B didn't know path A existed. The agent reviewing the code can't grep for a string it hasn't seen. You need **intent-level discovery**, not text matching.

## How It Works

The agent IS the similarity engine. It reads what each function does, writes that intent in plain language as a `@purpose` marker, accumulates intents in a registry file, and checks for overlap as it goes. No vector DB, no embeddings — the language model does fuzzy intent matching against a structured list.

The `@purpose` marker makes intent greppable for all future agents:

```
/// @purpose post auth re-login prompt to Discord with action button
pub fn build_relogin_message(...) -> ReloginMessage {
```

```
# @purpose format and surface error to user via Discord channel
def post_error(channel_id, error):
```

Keywords in the marker (`auth`, `relogin`, `Discord`, `error`, `surface`) are independently greppable. A future agent about to write a "send relogin notification" function can:

```bash
rg '@purpose' src/ | grep -i 'relogin\|login.*prompt\|auth.*message'
```

Hits mean: stop, read that function, use it or extend it.

## Output Goes in Tickets, Not Files

**DO NOT** create `.audit/`, `.reports/`, or any other directories in the repo for audit output. All findings, registries, and synthesis go into `tk` tickets. The only files this skill writes into the repo are:
- `@purpose` markers on existing source code
- `DO NOT REIMPLEMENT` sections in AGENTS.md

Everything else is a ticket.

## When to Run

**Smoke test (2 min)** — run first, always:

```bash
# Files with no @purpose markers (uninstrumented code)
rg --files-without-match '@purpose' --glob '*.rs' --glob '*.ts' --glob '*.py' src/ | wc -l

# Existing markers — quick scan for obvious overlap
rg '@purpose' src/

# Same emoji/keyword in multiple services
rg '🔑|🚦|⚠️|✅|❌' src/ -l | sort | uniq -c | sort -rn

# Same env var read in multiple places
rg 'env::var\("|env\.get\("|process\.env\.' src/ --glob '!node_modules' | \
  sed 's/.*["\x27]\([^"\x27]*\)["\x27].*/\1/' | sort | uniq -c | sort -rn | head -20
```

If smoke test shows lots of unmarked code or obvious overlap → full audit.
If everything is marked and no overlap → stop.

**Full audit (Delphi)** — when:
- Large portions of codebase have no `@purpose` markers
- Smoke test shows signals
- Multiple agents have been writing code for weeks without an audit
- You're about to do a major refactor and need to know what's redundant

## Mode 1: Full Audit (Delphi)

**REQUIRED SUB-SKILL:** `delphi`

### Step 1: Scope

Don't audit everything. Pick scope by one of:
- **By service** — each oracle walks one service/package
- **By churn** — `git log --since='3 weeks ago' --name-only | sort | uniq -c | sort -rn` — audit the most-changed areas
- **By unmarked** — `rg --files-without-match '@purpose' src/` — audit files missing markers

### Step 2: Create Intent Registry

Create an intent registry **ticket** — this is the working memory during the audit:

```
todos_oneshot(
  title: "Intent Registry: <scope>",
  description: "One line per public function. Agents: READ THIS BEFORE WRITING NEW FUNCTIONS.",
  tags: "convergence-audit,intent-registry",
  type: "task"
)
```

Use `tk add-note <id> "<entry>"` to append entries during the walk. The ticket is the registry — it survives context loss and doesn't pollute the repo.

### Step 3: Launch Delphi

Create the epic ticket, then launch 3 oracles with **identical** prompts. Each oracle walks its assigned scope.

**Oracle prompt — use verbatim, fill the blanks:**

```
You are instrumenting a codebase with @purpose markers and building an intent registry to find semantic duplication.

## Your Scope
Walk all public functions/methods in: {scope — e.g., "services/worker-a/src/"}

## Process — For EACH Public Function

1. Read the function
2. Read the intent registry ticket (`tk show <registry-ticket-id>`)
3. Determine: what does this function DO? Not its name — its actual intent.
4. Check the registry: does anything else already do this?
   - Same intent, same code = fine (it's the same function)
   - Same intent, different location = CONVERGENCE FAILURE — flag it
   - Similar intent, different scope = note it, not a failure
5. Add a @purpose doc comment to the function:
   ```
   /// @purpose <plain english intent, keyword-rich for grepability>
   ```
6. Append to the intent registry ticket via `tk add-note <registry-ticket-id>`:
   ```
   `path/file.rs:line` fn_name() — <same purpose text>
   ```
7. If convergence failure found, create a **ticket** for it:
   ```
   todos_oneshot(
     title: "Convergence Failure: <intent description>",
     description: "<findings below>",
     tags: "convergence-audit,convergence-failure",
     type: "bug"
   )
   ```
   Ticket body:
   ```
   ## <Intent Description>
   - `path/a.rs:line` fn_a() — <what this one does, how it differs>
   - `path/b.rs:line` fn_b() — <what this one does, how it differs>
   - **Behavioral differences:** <where outputs/behavior diverge>
   - **Winner:** <which implementation to keep, or "need reconciliation">
   ```

## Rules
- Write @purpose markers directly into the source files
- Append to the registry after EACH function, not at the end
- Read the registry before each function — it's your memory
- Don't flag intentional variants (e.g., user-facing error vs internal log) — note them as "intentional divergence" in the registry
- If a function already has @purpose, read it, add to registry, move on
- Focus on public/exported functions. Skip private helpers unless they look significant.

## What NOT to Look For
- Copy-paste duplication (that's grep's job, not yours)
- Style inconsistencies
- Naming conventions
- Dead code (use architectural-analysis for that)

You are ONLY looking for: different code, same intent.
```

### Step 4: Synthesis

After oracles complete, the synthesizer:

1. Reads all oracle intent registry tickets (tagged `intent-registry`) and convergence failure tickets (tagged `convergence-failure`)
2. **Cross-oracle scan** — this is where cross-service duplication surfaces. Oracle 1 logged "post auth relogin prompt to Discord" in service A. Oracle 2 logged "send relogin notification with auth link" in service B. The synthesizer reads both and sees the overlap.
3. Creates new convergence failure tickets for any cross-oracle findings
4. For each convergence failure, adds a Replace→Wire→Delete map via `tk add-note`:

```
## Replace→Wire→Delete: <intent>

**Replace:** `service-b/triggers.rs:trigger_relogin_flow()` (the weaker implementation)
**Wire:** callers of trigger_relogin_flow → `common/relogin.rs:build_relogin_message()`
**Delete:** `trigger_relogin_flow()` after all callers updated
**Verify:** `rg 'trigger_relogin_flow' src/` returns 0 hits
```

### Step 5: Output

Three deliverables — **all tickets, no loose files in the repo**:

1. **Intent registry ticket** — tagged `convergence-audit,intent-registry`. Future agents read this before writing new functions.
2. **Convergence failure tickets** — one per failure, tagged `convergence-audit,convergence-failure`, each with Replace→Wire→Delete map. Follow `15.04` for prioritization.
3. **AGENTS.md patches** — the ONE thing that goes in the repo. For each service where convergence failures were found, add a `DO NOT REIMPLEMENT` section:

```markdown
## Shared Capabilities (DO NOT REIMPLEMENT)
<!-- rg '@purpose' in these modules before writing new functions -->
- Relogin messages: `common/relogin.rs` — @purpose post auth re-login prompt to Discord
- Error surfacing: `common/errors.rs` — @purpose format and surface error to user
```

Follow 15.04 to create individual tickets for P0/P1 convergence failures.

## Mode 2: Write-Time Check (No Delphi)

Before writing any new public function:

```bash
# Check if something already does what you're about to write
rg '@purpose' src/ | grep -i '<keywords from your intent>'

# Check the intent registry ticket
tk ls --tag intent-registry
tk show <registry-ticket-id> | grep -i '<keywords>'
```

Hits → read those functions. Use, extend, or intentionally diverge.
No hits → write the function, add `@purpose`, append to registry.

This is not a separate invocation. This is how agents should work after a codebase has been audited. Put it in AGENTS.md.

## Incremental Audits

After the first full audit, future audits are cheap:

```bash
# What's new and unmarked?
rg --files-without-match '@purpose' --glob '*.rs' --glob '*.ts' --glob '*.py' src/
```

Only walk unmarked files. The registry already has everything else. Run this as a quick check every few weeks or after a burst of agent-driven development.

## What This Skill Does NOT Do

- **Syntactic duplication** — use `architectural-analysis` for copy-paste detection
- **Dead code** — use `architectural-analysis`
- **Refactoring** — use `30-01-full-refactor-guide` to execute the Replace→Wire→Delete maps
- **God files / tight coupling** — use `architectural-analysis`

This skill finds ONE thing: different code, same intent. Everything else has a different tool.

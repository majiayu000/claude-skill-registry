# Plan: Build start-specification Skill

Implementation plan for refactoring the monolithic `skills/start-specification/SKILL.md` (857 lines, old Steps 0-11) into a skill with progressive reference loading via conditional reference files.

**Source documents:**
- `SPEC-DISPLAY-REDESIGN.md` — design decisions, all 10 outputs, step structure
- `SPEC-FLOWS/01-08` — every path with exact prompts and user interactions

---

## What We're Building

A skill directory at `skills/start-specification/` with:
- `SKILL.md` — the backbone. Always loaded. Contains Steps 0-3 (migrations, discovery, prerequisites, routing). Routes to one reference file based on discovery state.
- 7 reference files loaded conditionally — instructions enter context only when the path requires them.

### Why Progressive Disclosure Matters

1. **No context pollution.** If a step isn't needed, its instructions never enter context. Claude only sees what's relevant to the current path.
2. **No premature loading.** Downstream steps aren't loaded until the current step completes and routes to them. Claude works on one step at a time.

### What Must Not Change

The logic flow is final. All 10 outputs, all step transitions, all display formats, all menu options, all handoff variants — these are locked down in the design documents. The skill refactor reorganises _where_ instructions live, not _what_ they say.

---

## The Routing Table

This is the core of SKILL.md Step 3. Based on discovery output, load exactly one display reference:

| Condition | Outputs | Reference |
|-----------|---------|-----------|
| `concluded_count == 0` | 1, 2 | `display-blocks.md` |
| `concluded_count == 1` | 3, 4 | `display-single.md` |
| `concluded_count >= 2`, cache valid | 6, 9 | `display-groupings.md` |
| `concluded_count >= 2`, `spec_count == 0`, cache none/stale | 5, 7 | `display-analyze.md` |
| `concluded_count >= 2`, `spec_count >= 1`, cache none/stale | 8, 10 | `display-specs-menu.md` |

Notes:
- When cache is valid, specs don't affect which display loads — groupings display handles both cases (specs and no specs).
- When cache is none/stale, specs DO affect the display — `display-analyze.md` auto-proceeds to analysis while `display-specs-menu.md` offers a choice between existing specs and analysis.

---

## Reference File Chain

Each reference file is self-contained for its display + menu, then links forward to the next step:

```
SKILL.md (Steps 0-3: migrations, discovery, prerequisites, routing)
│
├── display-blocks.md ──── TERMINAL (Outputs 1-2)
│
├── display-single.md ──── confirm-and-handoff.md ──── TERMINAL (Outputs 3-4)
│
├── display-analyze.md ──── analysis-flow.md ──── display-groupings.md ──── confirm-and-handoff.md
│                                                        │
│                                                        └── analysis-flow.md (re-analyze loop)
│
├── display-groupings.md ──── confirm-and-handoff.md
│         │
│         ├── analysis-flow.md (re-analyze loop)
│         └── (unify → update cache → confirm-and-handoff.md)
│
└── display-specs-menu.md ──── confirm-and-handoff.md (continue existing)
          │
          └── analysis-flow.md ──── display-groupings.md ──── ...
```

Key observation: `analysis-flow.md` always feeds into `display-groupings.md`, and `display-groupings.md` always offers `confirm-and-handoff.md` and `analysis-flow.md` (re-analyze). This creates a clean loop.

---

## File-by-File Breakdown

### SKILL.md (~100-150 lines) — Always Loaded

**Frontmatter:**
```yaml
---
name: start-specification
description: "Start a specification session from concluded discussions. Discovers available discussions, offers consolidation assessment for multiple discussions, and invokes the technical-specification skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/scripts/discovery-for-specification.sh), Bash(mkdir -p docs/workflow/.cache), Bash(rm docs/workflow/.cache/discussion-consolidation-analysis.md)
---
```

**Content:**
- Workflow context table (Phase 3 position)
- Critical instructions: STOP after interactions, don't skip steps, don't act until skill is loaded
- **Step 0**: Run migrations (invoke `/migrate`, stop if files updated)
- **Step 1**: Run discovery script, parse YAML output
- **Step 2**: Check prerequisites — if `concluded_count == 0`, load `display-blocks.md`
- **Step 3**: Routing logic — the table above, implemented as conditional instructions
- Navigation section: markdown links to all 7 reference files (so Claude knows they exist)

**Does NOT contain:** Any display output, analysis logic, confirm format, handoff text.

### references/display-blocks.md (~25 lines)

**Covers:** Outputs 1-2 (terminal — no further steps)

**Content:**
- Output 1: No discussions found → block message with direction to `/start-discussion`
- Output 2: Discussions exist but none concluded → block message with in-progress list
- STOP instruction

**Links to:** Nothing. Terminal path.

### references/display-single.md (~50 lines)

**Covers:** Outputs 3-4 (single concluded discussion, auto-proceed)

**Content:**
- Display format: nested tree with spec status and discussion status
- Output 3 variant: spec = none, discussion = ready
- Output 4 variant: spec exists (in-progress or concluded), discussion = extracted
- Key/legend (only statuses relevant to this display)
- Auto-proceed text ("Automatically proceeding with...")
- Note: Skip to confirm — no intermediate menu since only one option exists

**Links to:** `confirm-and-handoff.md` (Step 7)

### references/display-analyze.md (~45 lines)

**Covers:** Outputs 5 and 7 (multiple discussions, no specs, cache none or stale)

**Content:**
- Summary line: "{N} concluded discussions found. No specifications exist yet."
- Concluded discussions list (bullet format)
- "Not ready" section with in-progress discussions
- Cache-aware intro text:
  - Output 5 (no cache): "These discussions will be analyzed for natural groupings..."
  - Output 7 (stale): "A previous grouping analysis exists but is outdated..."
- Confirm prompt: "Proceed with analysis? (y/n)"
- Decline path: graceful exit message
- If confirmed: proceed to analysis

**Links to:** `analysis-flow.md` (Steps 4-5-6)

### references/display-groupings.md (~85 lines)

**Covers:** Outputs 6 and 9 (valid cache, show groupings). Also used after Step 6 (analysis complete).

This is the most content-rich display file because it handles the full groupings view with all possible statuses.

**Content:**
- Intro: "Recommended breakdown for specifications with their source discussions."
- Full nested tree display format:
  ```
  1. {Name}
     └─ Spec: {status} ({X of Y sources extracted})
     └─ Discussions:
        ├─ {name} ({status})
        └─ {name} ({status})
  ```
- Discussion status determination rules:
  - If grouped spec exists: look up in spec's sources array (extracted/pending)
  - If not in spec's sources: pending
  - If no grouped spec: check individual spec (ready or "spec: {status}")
- "Not ready" section
- Key/legend (all three discussion statuses + all three spec statuses)
- Tip about re-analyze
- Numbered menu with inline explanations:
  - Spec picks: Start/Continue/Refine (verb based on spec status)
  - "Unify all into single specification" (only if 2+ groupings)
  - "Re-analyze groupings"
- Menu behaviour:
  - Pick a grouping → load `confirm-and-handoff.md`
  - Unify → update cache to single grouping, then load `confirm-and-handoff.md`
  - Re-analyze → delete cache, load `analysis-flow.md`

**Links to:** `confirm-and-handoff.md` and `analysis-flow.md`

### references/display-specs-menu.md (~65 lines)

**Covers:** Outputs 8 and 10 (specs exist, cache none or stale)

**Content:**
- Summary: "{N} concluded discussions found. {M} specifications exist."
- Existing specifications display (nested tree, from spec frontmatter — NOT from cache)
- Unassigned discussions list (concluded but not in any spec)
- "Not ready" section
- Key/legend (only statuses present in this display)
- Cache-aware message:
  - Output 8 (no cache): "No grouping analysis exists."
  - Output 10 (stale): "A previous grouping analysis exists but is outdated..."
- Numbered menu:
  - "Analyze for groupings (recommended)" with inline explanation
  - "Continue {spec}" for each existing spec (verb based on status)
- Menu behaviour:
  - Analyze → load `analysis-flow.md`
  - Continue existing → load `confirm-and-handoff.md`

**Links to:** `analysis-flow.md` and `confirm-and-handoff.md`

### references/analysis-flow.md (~55 lines)

**Covers:** Steps 4-6 (context gathering, analysis, display results)

**Content:**
- **Step 4**: Gather analysis context
  - Prompt: "Before analyzing, is there anything about how these discussions relate..."
  - STOP, wait for user
- **Step 5**: Analyze discussions
  - Read ALL concluded discussion files thoroughly
  - Coupling analysis (data, behavioral, conceptual)
  - Grouping principles (coherent, not too broad, not too narrow, flag cross-cutting)
  - Preserve anchored names (CRITICAL: reuse names from `cache.anchored_names`)
  - Delete stale cache if exists, save new cache with groupings
  - Cache format (frontmatter with checksum + generated + discussion_files, body with groupings)
- **Step 6**: After analysis, display results using groupings format

**Links to:** `display-groupings.md` (Step 6 loads the groupings display)

### references/confirm-and-handoff.md (~90 lines)

**Covers:** Steps 7-8 (confirm selection, invoke skill)

**Content:**
- **Step 7**: Confirm selection — all variants:
  - Creating new spec (no existing): sources list, output path
  - Continuing spec with pending sources: existing path, pending sources, previously extracted
  - Refining concluded spec: existing path, all sources extracted
  - Creating grouped spec that supersedes: sources with "(has individual spec — will be incorporated)", supersede list
  - Unified spec: all sources, existing specs to incorporate + supersede
- Verb rule: no spec → "Creating", in-progress → "Continuing", concluded → "Refining"
- Confirm prompt: "Proceed? (y/n)"
- Decline path: return to previous display, present menu again
- **Step 8**: Invoke skill — all handoff variants:
  - Single source (individual spec)
  - Multiple sources (grouped, no existing specs)
  - Multiple sources with existing specs to incorporate (supersede instructions)
  - Continuing existing spec
- Link to technical-specification skill

**Links to:** `technical-specification` skill (handoff)

---

## Shared Content Strategy

Some content appears across multiple display files. Per the architecture plan's recommendation: **duplicate small shared content** rather than adding reference indirection.

| Content | Size | Appears in | Decision |
|---------|------|------------|----------|
| Key/legend | ~15 lines | display-single, display-analyze, display-groupings, display-specs-menu | Duplicate. Varies per context (different statuses shown). |
| "Not ready" section | ~4 lines | display-analyze, display-groupings, display-specs-menu | Duplicate. Identical text. |
| Graceful exit message | ~2 lines | display-single (decline), display-analyze (decline) | Duplicate. Identical text. |

This keeps files flat and self-contained. No nested reference chains for small content.

---

## Discovery Script Changes

The architecture plan calls for explicit counts in `current_state` to simplify routing. The script already outputs `concluded_discussion_count` and `discussions_checksum`. Add:

```yaml
current_state:
  discussions_checksum: "a1b2c3d4..."
  discussion_count: 5
  concluded_count: 3        # renamed from concluded_discussion_count
  in_progress_count: 2
  spec_count: 2
  has_discussions: true
  has_concluded: true
  has_specs: true
```

This lets SKILL.md routing use clean conditionals like `concluded_count == 1` and `spec_count == 0` instead of iterating arrays.

**Timing:** Implement alongside the skill refactor. The routing logic in SKILL.md is written against these fields.

---

## Implementation Sequence

### 1. Update Discovery Script

Add the explicit counts and boolean helpers to `current_state`. This is a prerequisite for the routing logic in SKILL.md.

**Files:** `scripts/discovery-for-specification.sh`

### 2. Create Skill Directory Structure

Create empty files first to establish the structure:

```
skills/start-specification/
  SKILL.md
  references/
    display-blocks.md
    display-single.md
    display-analyze.md
    display-groupings.md
    display-specs-menu.md
    analysis-flow.md
    confirm-and-handoff.md
```

### 3. Write SKILL.md (Backbone)

This is the most critical file. It must:
- Contain accurate frontmatter (especially `allowed-tools`)
- Implement Steps 0-3 exactly
- Have precise routing conditionals
- Link to all reference files

**Source material:** Steps 0-3 from SPEC-DISPLAY-REDESIGN.md + routing table above.

### 4. Write Display Reference Files

Work through each display file, extracting content from the design documents:

**Order matters** — write them in dependency order so we can validate the chain:

1. `display-blocks.md` — simplest, terminal, no outbound links
2. `display-single.md` — auto-proceed, links to confirm
3. `display-analyze.md` — prompt for analysis, links to analysis-flow
4. `display-specs-menu.md` — specs exist menu, links to analysis-flow and confirm
5. `display-groupings.md` — most complex display, links to confirm and analysis-flow

For each file:
- Extract the exact display text from SPEC-DISPLAY-REDESIGN.md outputs
- Extract the exact prompt/menu format
- Write the conditional variants (e.g., stale vs no cache)
- Add the forward links to next reference files
- Include STOP instructions where user interaction is needed

### 5. Write Analysis Flow

`analysis-flow.md` contains Steps 4-5-6. This is the "engine" that reads discussions, forms groupings, and saves cache.

**Source material:** Steps 4-6 from SPEC-DISPLAY-REDESIGN.md + analysis logic from current command Steps 4-6 + anchored names mechanism from SKILL-ARCHITECTURE-PLAN.md.

The current command's Step 6 (Analyze Discussions) has good analysis instructions — coupling types, grouping principles, cache format. These should be preserved.

### 6. Write Confirm and Handoff

`confirm-and-handoff.md` contains Steps 7-8. Multiple confirm variants + handoff formats.

**Source material:** SPEC-DISPLAY-REDESIGN.md Step 7 confirm formats + SPEC-FLOWS handoff texts.

### 7. Replace Monolithic SKILL.md

Replace the monolithic `skills/start-specification/SKILL.md` with the new backbone + reference file structure once verified.

### 8. Test All 10 Outputs

Verify each output path using the SPEC-FLOWS documents as test cases:
- Output 1-2: Block paths (no discussions / none concluded)
- Output 3-4: Single discussion (no spec / has spec)
- Output 5: Multiple, no specs, no cache → analyze → groupings → pick
- Output 6: Multiple, no specs, valid cache → groupings directly
- Output 7: Multiple, no specs, stale cache → re-analyze
- Output 8: Multiple, with specs, no cache → specs menu
- Output 9: Multiple, with specs, valid cache → groupings with full status
- Output 10: Multiple, with specs, stale cache → specs menu with stale msg

Also verify secondary paths from each output:
- Unify from groupings display
- Re-analyze from groupings display
- Decline at confirm → return to menu
- Decline at analysis prompt → graceful exit

---

## Critical Things to Get Right

### 1. Reference Loading Chain Must Work

The entire architecture depends on Claude following markdown links from one reference file to another. Example chain: `display-analyze.md` → `analysis-flow.md` → `display-groupings.md` → `confirm-and-handoff.md`.

The architecture plan flagged this as an open question. If reference-to-reference linking doesn't work, we'd need to restructure so SKILL.md acts as an intermediary between steps. **Verify this early.**

### 2. Display Format Fidelity

The display formats (nested tree, key/legend, menu options) are precisely defined in SPEC-DISPLAY-REDESIGN.md. The reference files must reproduce these exactly — they're not guidelines, they're specifications.

### 3. Conditional Text Within Files

Several files handle multiple variants:
- `display-single.md`: Output 3 (no spec) vs Output 4 (has spec)
- `display-analyze.md`: Output 5 (no cache) vs Output 7 (stale cache)
- `display-specs-menu.md`: Output 8 (no cache) vs Output 10 (stale cache)
- `display-groupings.md`: Output 6 (no specs) vs Output 9 (with specs) — these are actually identical in structure, just different data
- `confirm-and-handoff.md`: 5+ confirm variants based on selection type

Each file must clearly delineate which variant applies when. Use explicit conditionals ("If spec exists... / If no spec exists...") rather than trying to merge variants into one template.

### 4. Menu Option Dynamics

Some menu options are conditional:
- "Unify" only appears when 2+ groupings exist
- Verb on spec picks changes based on spec status (Start/Continue/Refine)
- Re-analyze explanation varies based on whether specs exist (anchored names mentioned or not)

### 5. Decline Paths

Two types of decline:
- **Decline at analysis prompt** (Step 3 for Outputs 5/7): Graceful exit, command ends
- **Decline at confirm** (Step 7): Return to previous display and menu

The "return to previous display" is straightforward — the display instructions are already in context from the reference file that was loaded earlier. Instruct Claude to re-present the menu.

### 6. The Unify Flow

When user picks "Unify all" from the groupings menu:
1. Update cache to reflect single unified grouping (all concluded discussions)
2. Use "Unified" as spec name (or "unified" kebab)
3. Proceed to confirm — if existing specs exist, list them as being superseded
4. On re-entry (next time command runs): cache shows single group, "Unify" not shown (already unified)

This logic lives in `display-groupings.md` but the confirm format lives in `confirm-and-handoff.md`. The transition must be clean.

---

## Open Questions

1. **Reference loading depth**: Can a reference file link to another reference file? (e.g., `analysis-flow.md` links to `display-groupings.md`). Needs verification — the entire architecture depends on this.

2. **Allowed-tools inheritance**: When a reference file is loaded, does it inherit the `allowed-tools` from the skill's frontmatter? The docs suggest tools are scoped to the skill, not individual files, so this should work.

3. **Context budget**: Skill descriptions are loaded into a context budget (default 15,000 chars). With many skills, check we don't exceed this. The `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var can increase it if needed.

---

## Out of Scope

- **Planning skill superseded display** — `discovery-for-planning.sh` doesn't extract `superseded_by`. Separate task.
- **Cleanup of design docs** — Remove root-level design docs after implementation is verified.

---

## Verification Checklist

Before considering the skill complete:

- [ ] `skills/start-specification/SKILL.md` exists with correct frontmatter
- [ ] All 7 reference files exist in `skills/start-specification/references/`
- [ ] Discovery script outputs explicit counts in `current_state`
- [ ] Routing table in SKILL.md covers all 10 outputs
- [ ] Each display file matches its output format from SPEC-DISPLAY-REDESIGN.md exactly
- [ ] analysis-flow.md preserves anchored names logic
- [ ] confirm-and-handoff.md covers all 5+ confirm variants
- [ ] Handoff format matches all variants from SPEC-FLOWS
- [ ] Reference-to-reference linking verified (chain works)
- [ ] Monolithic SKILL.md replaced with backbone + reference files
- [ ] All 10 output paths manually walked through against SPEC-FLOWS

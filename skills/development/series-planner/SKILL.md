---
name: series-planner
description: "Plan multi-part content series: structure, cross-linking, cadence."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
command: /series
routing:
  triggers:
    - "plan series"
    - "multi-part content"
    - "content series"
    - "article series"
    - "content arc"
  category: content-creation
  pairs_with:
    - content-calendar
    - topic-brainstormer
    - publish
---

# Series Planner Skill

## Overview

This skill plans multi-part content series with proper structure, cross-linking, and publishing cadence. It implements a three-phase workflow: **ASSESS** (determine viability), **DECIDE** (select structure), and **GENERATE** (produce plan). Each phase has gates to prevent scope creep, ensure standalone value, and maintain quality constraints.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| choosing publication frequency and managing delays | `cadence-guidelines.md` | Loads detailed guidance from `cadence-guidelines.md`. |
| series navigation links and Hugo implementation | `cross-linking.md` | Loads detailed guidance from `cross-linking.md`. |
| writing the series plan output | `output-format.md` | Loads detailed guidance from `output-format.md`. |
| selecting series type, part count, word targets | `series-types.md` | Loads detailed guidance from `series-types.md`. |

## Instructions

### Usage

```
/series [topic or idea]
/series --type=progressive [topic]      # Force series type
/series --parts=5 [topic]               # Target part count
/series --with-landing [topic]          # Include landing page plan
/series --minimal [topic]               # Titles and scope only
```

### Phase 1: ASSESS

**Goal**: Determine whether the topic is viable as a series and identify natural divisions.

**Step 1: Analyze topic**

```markdown
## Series Assessment
Topic: [user-provided topic]
Scope: [narrow / medium / broad]
Natural divisions: [how this topic breaks apart]
Audience progression: [beginner to expert? single level?]
```

**Step 2: Check viability**

Verify these constraints before proceeding:
- Topic has natural divisions (minimum 3 distinct subtopics required — this is non-negotiable)
- Each division can stand alone as complete content (not dependent on reading other parts)
- Logical progression exists between parts (reader can follow from one to the next)
- Not artificially padded (each part must earn its place with substantial unique content, no filler)

**Step 3: Detect series type**

Match topic signals to type. See `references/series-types.md` for full templates.

| Signal | Type |
|--------|------|
| "learn", "master", "deep dive" | Progressive Depth |
| "build", "create", "project" | Chronological Build |
| "why we chose", "migration", "debugging" | Problem Exploration |

**Gate**: Topic passes viability check with 3+ natural divisions identified. If topic fails viability, recommend single post or scope adjustment. Proceed only when gate passes.

### Phase 2: DECIDE

**Goal**: Select series type, part count, and structure.

**Step 1: Select type and justify**

```markdown
## Series Decision
Type: [Progressive Depth / Chronological Build / Problem Exploration]
Justification: [why this type fits]
Part Count: [3-7, enforced strictly]
Total Estimated Words: [X,XXX - X,XXX]
```

Enforce part count bounds strictly: minimum 3 parts, maximum 7 parts. No exceptions. The 3-7 constraint prevents both over-engineering (splitting one idea across 8+ parts) and under-engineering (calling 2 loosely related posts a "series").

**Step 2: Draft part breakdown**

For each part, define:
- Title and scope (1 sentence describing what this part covers)
- Standalone value (what reader learns from this part alone, without reading others)
- Forward/backward links (references to adjacent parts, for context only)

**Step 3: Validate standalone value**

For EVERY part, verify it passes the standalone test:
- Reader learns something complete and actionable (not a half-concept requiring other parts)
- Working code/config/output is possible from this part alone (readers aren't blocked waiting for next part)
- No critical information deferred to other parts (concepts explained fully in their own context)
- Someone landing on just this part via search gets something useful (SEO and UX principle)

Red flags that fail standalone test — reject any part showing these:
- "To understand this, read Part 1 first" as mandatory dependency
- Part ends mid-implementation with "Part 2 will continue"
- Core concepts explained only in earlier parts
- "Part 2 will explain why this works" — Part 1 reader is stranded

This is the failure mode prevention layer. Standalone value is non-negotiable because:
1. Search traffic lands on any part randomly, not always on Part 1
2. Readers expect complete value from the part they're reading
3. Multi-part cliff-hangers frustrate readers and hurt SEO

**Step 4: Select publishing cadence**

See `references/cadence-guidelines.md` for detailed criteria. Default to weekly unless topic complexity or content depth suggests otherwise.

**Gate**: All parts pass standalone value check. Part count is strictly 3-7. Type selection justified. Proceed only when gate passes.

### Phase 3: GENERATE

**Goal**: Produce the complete series plan with all metadata.

**Step 1: Build series plan**

Output the complete plan including:
1. Series header with type and metadata
2. Detailed breakdown per part (scope, standalone value, links)
3. Cross-linking structure (see `references/cross-linking.md`)
4. Publication schedule with dates
5. Hugo frontmatter template per part

**Step 2: Final validation**

Before outputting, verify all constraints one final time:
- [ ] Every part has standalone value described (not deferred to other parts)
- [ ] Word counts are realistic (800-1500 per part, within 20% variance across parts to avoid reader whiplash)
- [ ] Cross-linking is complete (prev/next navigation for all parts)
- [ ] No cliff-hangers that frustrate readers (each part delivers closure, even if it references others)
- [ ] No filler parts (each part has substantial, non-redundant content)
- [ ] Part count within 3-7 bounds (enforced strictly)

**Step 3: Output plan**

Use the series plan format from `references/output-format.md`.

**Gate**: All validation checks pass. Plan is complete and ready for delivery.

---

## Series Types (Summary)

Three primary types. Full templates and examples in `references/series-types.md`.

### Progressive Depth
Shallow-to-deep mastery. Each level is complete; beginners stop at Part 1, advanced readers skip ahead. Enables flexible audience engagement.

### Chronological Build
Step-by-step creation. Each part produces working output; reader can stop at any milestone and have a working artifact.

### Problem Exploration
Journey from problem to solution. Even failed approaches are instructive; each part teaches something about the journey, not just the destination.

---

## Examples

### Example 1: Standard Technical Series
User says: "/series Go error handling"

Actions:
1. ASSESS: Topic has clear depth levels (basics, wrapping, custom types, patterns)
2. DECIDE: Progressive Depth, 4 parts, weekly cadence
3. GENERATE: Full plan with standalone value per part

Result: 4-part series where each part teaches complete error handling at its level (beginner can stop at Part 1 and be satisfied; advanced reader skips to patterns).

### Example 2: Project Tutorial Series
User says: "/series building a CLI tool in Rust"

Actions:
1. ASSESS: Topic has build milestones (scaffold, commands, config, distribution)
2. DECIDE: Chronological Build, 4 parts, weekly cadence
3. GENERATE: Full plan with working output per milestone

Result: 4-part series where each part produces a functional artifact (Part 1: runs basic command; Part 2: parses flags; Part 3: config file support; Part 4: distributable binary).

### Example 3: Problem Exploration Series
User says: "/series why we migrated from MongoDB to PostgreSQL"

Actions:
1. ASSESS: Topic has journey arc (problem, attempt, failure, solution)
2. DECIDE: Problem Exploration, 4 parts, bi-weekly cadence
3. GENERATE: Full plan where each part teaches standalone lessons

Result: 4-part series where even failed approaches deliver instructive value (Part 1: why we needed to move; Part 2: why MongoDB stopped working for us; Part 3: why PostgreSQL migration was hard; Part 4: what we learned).

### Example 4: Topic Too Narrow
User says: "/series Go defer statement"

Actions:
1. ASSESS: Topic has 1-2 natural divisions, not 3+
2. Gate fails: Recommend single post or expanding scope to "Go resource management"

Result: Redirect to publish (outline intent) or expanded topic suggestion (publish outline is better for focused single topics).

---

## Error Handling

### Error: "Topic Too Narrow for Series"
Cause: Topic doesn't naturally divide into 3+ parts

Solution:
1. Suggest publish (outline intent) for single comprehensive post (single-post tool is more appropriate)
2. Propose scope expansion: "Consider covering [related aspect] to reach 3+ parts"
3. List what would need to be true for series to work: "A series works when you can answer: Part 1 [X], Part 2 [Y], Part 3 [Z]"

### Error: "Topic Too Broad for Series"
Cause: Would require 8+ parts or scope is unmanageable (violates part count constraint)

Solution:
1. Identify natural breakpoints for multiple series (e.g., "Kubernetes basics" series + "Kubernetes advanced" series)
2. Recommend first series to tackle (smallest, highest value)
3. Suggest narrowing to specific aspect (e.g., "Instead of 'Cloud Architecture', try 'Cloud Cost Optimization'")

### Error: "No Logical Progression"
Cause: Parts don't build on each other meaningfully; just loosely related topics

Solution:
1. Determine if these are better as standalone posts (not a series at all)
2. Find the connecting thread that creates progression (what makes this 3-part story instead of 3 separate posts?)
3. Consider if forcing series structure adds value vs. individual posts (sometimes the answer is "these should be separate")

### Error: "Standalone Value Missing"
Cause: One or more parts don't stand alone (reader needs previous parts to understand this one)

Solution:
1. Identify which parts fail the standalone test (list specific examples: "Part 2 assumes knowledge from Part 1")
2. Suggest content to add for completeness (add summary section, explain prerequisite inline, restructure)
3. Or merge dependent parts into one (e.g., "Part 1 and 2 should be one part; move non-essential details to Part 3")

---

## References

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/series-types.md`: Complete type templates with examples and selection criteria
- `${CLAUDE_SKILL_DIR}/references/cross-linking.md`: Navigation patterns and Hugo implementation
- `${CLAUDE_SKILL_DIR}/references/cadence-guidelines.md`: Publishing frequency recommendations and schedules
- `${CLAUDE_SKILL_DIR}/references/output-format.md`: Series plan output format template

### Key Constraints Summary

These constraints are non-negotiable and enforced at every phase:

1. **Part Count (3-7)**: Series must have minimum 3 parts, maximum 7 parts. This prevents both scope creep (forcing 8+ parts for one idea) and false series (2 loosely related posts).

2. **Standalone Value**: Every part MUST deliver complete value to readers who land on it via search or reference. Red flags: cliff-hangers, deferred core concepts, mid-implementation endings.

3. **No Filler**: Each part must earn its place with substantial unique content. No padding to hit a part count target.

4. **Logical Progression**: Parts build meaningfully from one to the next. If they're just loosely related topics, they shouldn't be a series.

5. **Over-Engineering Prevention**: Plan only what the user requests. No bonus parts, scope creep, or "one more thing" unless user asks.

These are gates at each phase. If any constraint fails, the workflow stops and recommends alternative approaches (single post, expanded scope, reduced scope, etc.).

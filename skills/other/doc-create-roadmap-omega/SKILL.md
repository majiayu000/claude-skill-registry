---
name: doc-create-roadmap-omega
description: "{{ 𝛀𝛀𝛀 }} Create a project roadmap document in structured milestone format"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write"]
argument-hint: [roadmap name (optional)]
---

Create a project roadmap at `docs/roadmaps/{name}.md` with milestone-based task organization and dependency tracking via Mermaid diagrams.

## Behaviour

| Codebase Context     | Arguments Passed | Action                                                              |
| -------------------- | ---------------- | ------------------------------------------------------------------- |
| No other roadmaps    | 0                | Create overall project roadmap (probably `mvp.md`)                  |
| N/A                  | 1                | Create roadmap for feature/phase specified in argument              |
| Other roadmaps exist | 0                | Ask user which roadmap to create or if creating a new feature phase |

## Steps

### 1. Determine roadmap scope and context

- Check if `docs/roadmaps/` directory exists and contains roadmaps
- Check if `.claude/roadmaps.json` exists and parse its contents
- If $ARGUMENTS provided, use as roadmap name (e.g., "mvp", "v2-features")
- If no arguments and no existing roadmaps, default to "mvp"
- If no arguments but roadmaps exist, ask user to clarify intent

### 2. Gather project context

Read available documentation to understand:
- Project purpose and technical scope
- Existing architecture and technology stack
- Development status (what's done, what's planned)
- Key features and requirements

**Sources to check:**
- `README.md` (project overview)
- `docs/` directory (all markdown files)
- `.claude/CLAUDE.md` (project-specific conventions)
- Existing roadmaps in `docs/roadmaps/` (if creating additional roadmap)

### 3. Elicit roadmap structure from user

Ask targeted questions to define:

**Milestone count and themes:**
- How many major milestones? (typical: 3-5 for MVP)
- What is each milestone's goal? (e.g., "Core Library", "TUI Interface", "CLI Commands")
- What defines completion for each milestone?

**Task categories per milestone:**
- What are the logical groupings? (e.g., TUI screens, workflows, commands)
- Use 2-3 letter prefixes (e.g., WA = workflows, TI = TUI, DC = direct commands)

**Dependencies:**
- Which milestones are sequential vs parallel?
- Any known blockers or prerequisites?

### 4. Generate roadmap structure

Create file at `docs/roadmaps/{name}.md` with:

#### File Header

```markdown
---
description: [Brief one-line description from user]
---

# {Project Name}: {Roadmap Title}

|          | Status                  | Next Up           | Blocked           |
| -------- | ----------------------- | ----------------- | ----------------- |
| **{Cat}** | [current status]       | [next priority]   | [key blockers]    |

---

## Contents

- [Milestones](#milestones)
  - [Milestone 1: {Name}](#m1)
  - [Milestone 2: {Name}](#m2)
  - ...
- [Progress Map](#map)
- [Links](#links)
- [Beyond MVP](#post-mvp)
```

#### Milestone Structure (for each milestone)

```markdown
<a name="m{N}"><h3>Milestone {N}: {Name}</h3></a>

> [!IMPORTANT]
> **Goal:** {Milestone objective}

<a name="m{N}-doing"><h4>In Progress (Milestone {N})</h4></a>

- [ ] {MilestoneCategory}.{Seq}. {Task description}

<a name="m{N}-todo"><h4>To Do (Milestone {N})</h4></a>

- [ ] {MilestoneCategory}.{Seq}. {Task description} — **depends on {TaskID}**

<a name="m{N}-blocked"><h4>Blocked (Milestone {N})</h4></a>

- [ ] {MilestoneCategory}.{Seq}. {Task description} — **depends on {TaskID}**

<a name="m{N}-done"><h4>Completed (Milestone {N})</h4></a>

- [x] {MilestoneCategory}.{Seq}. {Task description}
```

#### Progress Map (single aggregated diagram)

At `<a name="map">` section, include ONE Mermaid diagram showing ALL tasks across ALL milestones with full dependency graph:

```mermaid
---
title: Progress Map
---
graph TD

{TaskID}["`*{TaskID}*<br/>**{Category}**<br/>{short desc}`"]:::open --> {DepTaskID}

m{N}{"`**Milestone {N}**<br/>{Name}`"}:::mile

classDef default,blocked fill:#fff7fb;
classDef open fill:#fff9e5;
classDef mile fill:#c4fffe;
```

### 5. Task numbering convention

Format: `{Milestone}{Category}.{Seq}`

**Examples:**
- `1WA.1` - Milestone 1, Workflow Abstractions, task 1
- `2TI.7` - Milestone 2, TUI Interface, task 7
- `3DC.2` - Milestone 3, Direct Commands, task 2

**Sub-tasks:**
- Use alpha suffix: `2TI.3a`, `2TI.3b`

**Rules:**
- Never reuse task IDs
- Sequential numbering within each category
- New tasks append to category sequence (no renumbering)

### 6. Dependency tracking

**In task descriptions:**
```markdown
- [ ] 2TI.14. Build validate screen — **depends on 2TI.13, 2TI.7**
```

**In Mermaid diagrams:**
```mermaid
2TI.13 --> 2TI.14
2TI.7 --> 2TI.14
```

**Class assignment:**
- `:::open` - No blocking dependencies (ready to start)
- `:::blocked` (default) - Has dependencies or explicit blockers
- `:::mile` - Milestone node

### 7. Update project configuration

Add/update `.claude/roadmaps.json`:
```json
{
  "roadmaps": [
    {
      "name": "{Roadmap Name}",
      "path": "docs/roadmaps/{name}.md"
    }
  ]
}
```

If file exists, append to array. If creating first roadmap, create file.

### 8. Populate initial tasks

For each milestone:
- Break goal into 5-15 discrete tasks
- Assign task IDs following numbering convention
- Group tasks by category (2-3 letter prefix)
- Mark obvious dependencies
- Place tasks in appropriate sections:
  - **In Progress**: Only if user specifies active work
  - **To Do**: Tasks ready to start (no blockers)
  - **Blocked**: Tasks with explicit dependencies
  - **Completed**: Only if user specifies already-done work

### 9. Generate summary status table

At top of roadmap, create status table showing per-category progress:

```markdown
|          | Status                  | Next Up           | Blocked           |
| -------- | ----------------------- | ----------------- | ----------------- |
| **Core** | ✅ Milestone 1 complete | —                 | —                 |
| **CLI**  | Basic structure         | Direct commands   | `check` (needs X) |
| **TUI**  | Screens implemented     | Keyboard nav      | All screens       |
```

## Output Format

After creating the roadmap:

1. Confirm file created at `docs/roadmaps/{name}.md`
2. Confirm `.claude/roadmaps.json` updated
3. Summarize structure:
   - Number of milestones
   - Total tasks defined
   - Tasks per section (In Progress, To Do, Blocked, Completed)
4. Note any assumptions made or areas needing user refinement

## Notes

- **Be thorough but not prescriptive** - user will refine tasks iteratively
- **Preserve flexibility** - roadmap will evolve with `doc:update:roadmap`
- **Dependency inference** - use project context to suggest logical dependencies
- **Category naming** - short, memorable, distinct (2-3 letters)
- **Milestone scope** - each should deliver meaningful user value
- **Initial state** - most tasks likely "To Do" or "Blocked" unless project is mid-flight

## Compatibility

This command creates roadmaps compatible with `commands/doc/update/roadmap.md`:
- Section anchors: `#m{N}-doing`, `#m{N}-todo`, `#m{N}-blocked`, `#m{N}-done`
- Task format: `- [ ]` unchecked, `- [x]` checked
- Dependency format: `— **depends on {TaskID}**`
- Mermaid class definitions: `classDef default,blocked fill:#f9f;` etc.

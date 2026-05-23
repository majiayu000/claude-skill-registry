# Iterative Planning Context Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Acquire codebase context for planning iterative changes to existing codebases. Produces a Planning Context Snapshot that enables effective decomposition and integration planning.

## When to Activate

Use this skill when:
- Acquiring planning context for an existing codebase
- Preparing for iterative planning
- Before planning changes to existing code
- Quick context needed for bug fix
- Focused context needed for feature
- Comprehensive context needed for architecture change
- Need to understand where new code should live
- Need to understand patterns to follow

## Core Principles

### 1. Planning Context Is Not Understanding Context

Every piece of context acquired must answer a planning question (where does code go? what patterns to follow?).

*General exploration produces understanding. Planning-specific acquisition produces actionable decomposition information.*

### 2. Scope Before Explore

Define what context is needed based on the change type before starting exploration.

*Different changes need different context depth. Bug fixes need 15 minutes; architectural changes need 60+.*

### 3. Documentation Before Code

Read README, AGENTS.md, and existing docs before exploring code.

*Existing documentation captures intent and context that code alone cannot convey.*

### 4. Sample Rather Than Exhaust

Read 3-5 representative files rather than trying to read everything.

*Exhaustive reading exhausts context windows. Sampling reveals patterns efficiently.*

### 5. Write Immediately

Capture findings immediately rather than relying on memory.

*Context windows are finite. Explicit capture preserves knowledge for synthesis.*

### 6. Answer The Questions

Stop when the planning questions from Phase 0 are answered.

*Context acquisition serves planning. Additional exploration without purpose wastes tokens.*

---

## Workflow

### Phase 0: Scope Definition (5 min)

**Goal:** Define what context is needed based on the planned change.

1. **Classify the change type:**

   | Change Type | Context Depth | Time Budget |
   |-------------|---------------|-------------|
   | Bug fix | Minimal (affected area only) | 10-15 min |
   | Minor feature | Focused (feature area + integration) | 20-30 min |
   | Major feature | Comprehensive (full codebase) | 45-60 min |
   | Architectural | Comprehensive + history | 60-90 min |

2. **Identify focus areas:**
   - What part of the codebase is affected?
   - What external systems are involved?

3. **Note specific planning questions:**
   - What must the plan answer that requires codebase context?

4. **Set time budget** based on change type.

**Outputs:** Change classification, question list, time budget

### Phase 1: Orientation (5-10 min)

**Goal:** Establish baseline understanding before deep exploration.

1. **Check for existing context documentation:**
   ```bash
   ls README.md AGENTS.md docs/codebase-overview.md 2>/dev/null
   ```

2. **Identify project type and tech stack:**
   ```bash
   ls Cargo.toml package.json go.mod pyproject.toml 2>/dev/null
   ```

3. **Read top-level documentation:**
   - README.md: Project purpose, setup, usage
   - AGENTS.md: Agent-specific instructions (high value if exists)
   - docs/codebase-overview.md or equivalent

4. **Note any planning state:**
   ```bash
   ls planning/ .github/ISSUE_TEMPLATE/ TODO.md 2>/dev/null
   ```

**Outputs:** Technology stack, high-level understanding, documentation pointers, planning system

### Phase 2: Structure Mapping (10 min)

**Goal:** Understand where code lives and what goes where.

1. **Generate directory tree:**
   ```bash
   tree -L 2 -d --noreport
   ```

2. **Annotate each directory's purpose**

3. **Identify entry points** (main files, index files, CLI entry)

4. **Map module boundaries:** what are top-level modules, how are they connected

5. **Locate test infrastructure:**
   ```bash
   find . -name "*test*" -type d 2>/dev/null | head -5
   ```

6. **Document with planning purpose:** for each directory, note what kind of code belongs here and how new code would be added

**Outputs:** Annotated directory tree, entry point map, test location summary, "Adding New Code" table

### Phase 3: Pattern Extraction (15 min)

**Goal:** Understand the conventions that new code must follow.

1. **Select 3-5 representative files to sample:**
   - One entry point file (main.rs, index.ts)
   - One "core" module (most imported)
   - One test file
   - One utility file (if exists)

2. **Extract naming patterns:** files, functions, types, constants

3. **Extract structural patterns:** module organization, error handling, logging

4. **Extract documentation patterns:** comment style, doc format

5. **Extract test patterns:** test structure, mocking approach, fixtures

**Outputs:** Naming conventions table, structural patterns summary, error handling approach, test patterns summary

### Phase 4: Integration Discovery (10 min)

**Goal:** Understand how new code must connect with existing code.

1. **Identify core abstractions to use:**
   - What types/traits/interfaces exist that new code should extend?
   - What utilities are available for reuse?

2. **Map external dependencies:** read package manifest, note what's available

3. **Identify integration points for the specific change:**
   - What existing code must this touch?
   - What APIs must this call?
   - What APIs must this expose?

4. **Check for relevant planning state:**
   - Is related work already planned?
   - Are there blockers or dependencies?

**For multi-component changes:**
```
For each component:
├── Where does it live?
├── What pattern does it follow?
├── What does it depend on?
├── What depends on it?
└── How is it tested?
```

**Outputs:** Integration point inventory, abstractions to use/extend, dependency opportunities, related planning state

### Phase 5: Context Synthesis (10 min)

**Goal:** Consolidate findings into a Planning Context Snapshot.

1. **Answer all scope questions** from Phase 0 with concrete answers

2. **Create integration map:**
   ```
   [New Code] ──uses──> [Existing Abstraction]
              ──extends──> [Existing Module]
              ──tested-by──> [Test Infrastructure]
   ```

3. **Document patterns to follow** as actionable rules

4. **Flag potential issues:**
   - Technical debt that affects the plan
   - Missing infrastructure that needs creation
   - Ambiguities requiring human decision

5. **Populate the Planning Context Snapshot** (see Output Format section)

**Outputs:** Planning Context Snapshot document, answered question list, issue/risk flags

---

## Protocol Variations

### Quick Context (Bug Fix, Small Change)

**When:** < 1 hour effort

Skip to essentials:
1. Read README/AGENTS.md (2 min)
2. Locate affected code (3 min)
3. Sample adjacent patterns (5 min)
4. Identify test location (2 min)
5. Synthesize minimal context (3 min)

**Total: 15 minutes**

### Focused Context (Single-Area Feature)

**When:** 1-4 hours effort

1. Full Phase 0-1 (10 min)
2. Structure mapping for affected area only (5 min)
3. Pattern extraction from affected area (10 min)
4. Integration discovery for that area (5 min)
5. Synthesize (5 min)

**Total: 35 minutes**

### Comprehensive Context (Cross-Cutting Feature)

**When:** > 4 hours effort

Full protocol as described in workflow.

**Total: 45-60 minutes**

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Quick Context** | Bug fix or small change | 15-min essential-only protocol | Small changes don't need comprehensive context |
| **Focused Context** | Single-area feature | Explore only affected area | Focus on what matters |
| **Parallel Exploration** | Large codebase | Use sub-agents for different areas | Reduces wall-clock time |
| **Existing Context Check** | Any acquisition | Check docs/planning/context-*.md first | Avoid redundant exploration |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Exhaustive Reading** | Context exhaustion, diminishing returns | Sample representative files |
| **Understanding Without Purpose** | Wasted context budget | Focus on areas the change touches |
| **Skipping Scope Definition** | Over-explore or under-explore | Always start with Phase 0 |
| **Mental-Only Notes** | Knowledge lost at context exhaustion | Write findings immediately |
| **Ignoring Documentation** | Miss intent and context | Read docs first |
| **Recreating Existing Context** | Duplicate effort | Check for existing context-*.md |

---

## Quality Checklist

Before completing:

- [ ] Change type classified and time budget set (Phase 0)
- [ ] Planning questions documented (Phase 0)
- [ ] README/AGENTS.md read if they exist (Phase 1)
- [ ] Technology stack identified (Phase 1)
- [ ] Directory structure mapped with annotations (Phase 2)
- [ ] Entry points identified (Phase 2)
- [ ] "Adding New Code" table created (Phase 2)
- [ ] 3+ files sampled for patterns (Phase 3)
- [ ] Naming conventions documented (Phase 3)
- [ ] Test patterns understood (Phase 3)
- [ ] Integration points for this change identified (Phase 4)
- [ ] Core abstractions to use listed (Phase 4)
- [ ] All scope questions answered (Phase 5)
- [ ] Planning Context Snapshot document created (Phase 5)

---

## Output Format: Planning Context Snapshot

```markdown
# Planning Context Snapshot: [Project Name]

> **Generated:** YYYY-MM-DD
> **Scope:** [Full/Focused: <area>]
> **Staleness Warning:** Refresh if >N days old or after major changes

## Quick Reference

[One-paragraph summary]

### Tech Stack
- Language: [Primary language(s)]
- Framework: [Key frameworks]
- Build: [Build tool]
- Test: [Test framework]

### Key Entry Points
| Purpose | Location |
|---------|----------|
| ... | ... |

---

## Structure Map

[Annotated directory tree]

### Adding New Code

| New Code Type | Location | Pattern to Follow |
|---------------|----------|-------------------|
| ... | ... | ... |

---

## Conventions

### Naming

| Element | Convention | Example |
|---------|------------|---------|
| ... | ... | ... |

### Code Patterns

[Error handling, logging, configuration]

---

## Core Abstractions

### Key Types

| Type | Purpose | Extend When |
|------|---------|-------------|
| ... | ... | ... |

---

## Integration Points

### Internal Dependencies
[Module dependency graph]

### External Dependencies
| Dependency | Purpose | Version |
|------------|---------|---------|
| ... | ... | ... |

---

## Test Infrastructure

[Location, patterns, how to run]

---

## Technical Debt & Warnings

| Issue | Impact | Workaround |
|-------|--------|------------|
| ... | ... | ... |

---

## Change-Specific Context

### Planned Change
[Description]

### Questions Resolved
| Question | Answer |
|----------|--------|
| ... | ... |
```

---

## Examples

### Quick context for bug fix

```
# Phase 0: Scope Definition
Change: Fix bug in skill extraction (beadsmith init)
Classification: Bug fix
Focus: commands/init.rs
Questions: What's the extraction logic? How do I test it?
Time budget: 15 min

# Quick Context Variation (15 min total)
1. Read README.md - understand skill extraction purpose (2 min)
2. Read commands/init.rs - find the bug location (3 min)
3. Sample skills.rs - understand BundledSkill struct (5 min)
4. Check test in init.rs - #[cfg(test)] module exists (2 min)
5. Synthesize:
   - Bug is in: commands/init.rs
   - Pattern: anyhow::Result for errors
   - Test: add case to existing #[cfg(test)] module
   - Time spent: 12 min
```

### Comprehensive context for major feature

```
# Phase 0: Scope Definition
Change: Add /beads-iterate command for iterative planning
Classification: Major feature
Focus: CLI commands, skill system, org-beads integration
Questions:
  1. Where do new commands live?
  2. What patterns do commands follow?
  3. Should this be a skill, command, or both?
  4. How does it integrate with existing planning?
Time budget: 45 min

# Phase 1: Orientation (5 min)
- README.md exists - project is Rust CLI, skills bundled at compile time
- docs/codebase-overview.md exists - detailed structure guide!
- planning/ exists - org-mode planning system in use

# Phase 2: Structure Mapping (10 min)
crates/beadsmith/src/
├── main.rs         # CLI entry, Commands enum
│                   # NEW COMMANDS: Add variant, add match arm
├── skills.rs       # Skill bundling via include_str!()
│                   # NEW SKILLS: Add constant, bundled_skills()
└── commands/       # Subcommand implementations
    └── init.rs     # Pattern to follow

skills/
├── codebase-exploration/  # Related! Produces understanding
├── spawn-to-beads/        # Integration pattern

Adding New Code:
| Type | Location | Pattern |
| Command | commands/<name>.rs | init.rs |
| Skill | skills/<name>/ | codebase-exploration/ |

# Phase 3: Pattern Extraction (15 min)
Sampled: main.rs, skills.rs, init.rs, codebase-exploration/SKILL.md
Naming: kebab-case dirs, snake_case modules, PascalCase types
Errors: anyhow::Result with .context()
Tests: #[cfg(test)] modules, tempfile for fs tests

# Phase 4: Integration Discovery (10 min)
Integration points:
- main.rs Commands enum (add variant)
- skills.rs bundled_skills() (add entry)
- commands/mod.rs (add export)
- Test count assertions (update)

Abstractions to use:
- BundledSkill struct
- clap derive macros

# Phase 5: Synthesis (5 min)
Answers:
1. New commands: commands/<name>.rs
2. Pattern: clap Args struct, run() function
3. Should be SKILL primarily (methodology); command optional later
4. Output feeds into beads-plan for decomposition

Context Snapshot: docs/planning/context-beadsmith.md
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `codebase-exploration` | General exploration methodology; this skill adds planning-specific focus |
| `beads-plan` | Consumes Planning Context Snapshot for decomposition |
| `spawn-to-beads` | May be used after planning to delegate to beads |

---

## References

- `docs/planning/codebase-context-spec.md` - What context is needed and why
- `docs/planning/context-acquisition-protocol.md` - Detailed protocol this skill implements
- `docs/planning/context-representation-template.md` - Output format specification
- `codebase-exploration` skill - General exploration methodology

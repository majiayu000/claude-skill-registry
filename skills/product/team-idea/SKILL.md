---
name: team-idea
description: "[Team] Capture and structure product ideas as backlog artifacts. Use when capturing new ideas, feature requests, or concepts for future refinement. Triggers on keywords like "capture idea", "new idea", "feature idea", "add to backlog", "quick idea"."
argument-hint: "[title] - Brief title for the idea (optional, will prompt if not provided)"
infer: true
allowed-tools: Read, Write, Grep, Glob, TodoWrite, AskUserQuestion
---

# Idea Capture

Capture raw ideas as structured artifacts for backlog consideration.

## Summary

**Goal:** Capture and structure product ideas as backlog artifacts with module context and validation.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Detect module | Dynamic discovery from `docs/business-features/*/README.md` frontmatter |
| 2 | Load business context | Read INDEX.md and README.md for matched module |
| 3 | Inspect related entities | Search `domain_path` for existing entity classes |
| 4 | Gather information | Ask title, problem, beneficiary, scope |
| 5 | Generate artifact | Use idea template, ID format `IDEA-{YYMMDD}-{NNN}` |
| 6 | Quick validation | Ask 2-3 questions on problem clarity, value, scope |
| 7 | Suggest next step | Point to `/team-refine` for PBI refinement |

**Key Principles:**
- Modules are self-describing via YAML frontmatter -- auto-discovered, not hardcoded
- Always validate idea with 2-3 quick questions before handoff
- Save to `team-artifacts/ideas/{YYMMDD}-{role}-idea-{slug}.md`

## When to Use
- User has new feature concept
- Stakeholder request needs documentation
- Quick capture without full refinement

## Pre-Workflow

### Activate Skills

- Activate `product-owner` skill for idea capture best practices

## Workflow

### 0. Detect Module (Dynamic Discovery)

Dynamic module discovery from YAML frontmatter:

1. **Glob**: Find all module documentation
   ```
   docs/business-features/*/README.md
   ```

2. **Parse Frontmatter**: For each README, extract YAML between `---` markers
   - Extract: `module`, `keywords`, `aliases`, `features`, `domain_path`

3. **Match Keywords**: Compare user input (title/problem) against:
   - `aliases` (exact match - highest priority)
   - `keywords` (partial match)
   - `features` (partial match for sub-features)
   - Score = count of matching terms

4. **Select Module**:
   - If single match: Confirm "Is this related to {Module}?"
   - If multiple matches: Show matches with scores, ask user to select
   - If no match: List all discovered modules, ask selection or "new" for new module

**Note**: Modules are self-describing via frontmatter. New modules auto-discovered when following template.

### 1. Load Business Context

- **MUST READ:** `docs/business-features/{Module}/INDEX.md` (feature table)
- **MUST READ:** `docs/business-features/{Module}/README.md` (Overview + Business Requirements sections only, ~2000 token budget)
- Note: "Loaded context from {Module} business documentation"
- If module docs missing: Note absence and continue without context

### 1.5. Show Existing Features

- Display feature table from INDEX.md
- Ask: "Does this idea relate to or extend any existing feature?"
- Note related FR-XX IDs if applicable

### 2. Inspect Related Entities

Use `domain_path` from module frontmatter for targeted entity search:

1. **Get Domain Path**:
   - If module matched: Use frontmatter `domain_path` (e.g., `src/PlatformExampleApp/PlatformExampleApp.TextSnippet.Domain`)
   - If no module: Skip entity inspection or use broad search

2. **Entity Search**:
   ```
   {domain_path}/Entities/*.cs
   ```

3. **Extract**: Entity class names (classes extending `RootEntity<`), key properties, relationships
4. **Show**: "Related entities found: {EntityName} with properties: [{list}]"
5. **If no match**: "No existing entities match - this may be a new domain concept"

### 3. Gather Information

- If no title provided, ask: "What's the idea in one sentence?"
- Ask: "What problem does this solve?"
- Ask: "Who benefits from this?"
- Ask: "Any initial scope thoughts?"

### 4. Generate Artifact

- Create idea file using template from `team-artifacts/templates/idea-template.md`
- Generate ID: `IDEA-{YYMMDD}-{NNN}` (sequential)
- Set status: `draft`
- Add frontmatter:
  - `related_module: "{Module or N/A}"`
  - `related_entities: [{list of entity names}]`
  - `related_features: [{FR-XX IDs if applicable}]`

### 5. Save Artifact

- Path: `team-artifacts/ideas/{YYMMDD}-{role}-idea-{slug}.md`
- Role: Infer from context or ask
- Add to Related section: Link to `docs/business-features/{Module}/`

### 6. Quick Validation (MANDATORY)

After saving, conduct brief validation interview to confirm understanding before handoff.

#### Question Selection (pick 2-3 most relevant)

| Category            | Question                                                      |
| ------------------- | ------------------------------------------------------------- |
| **Problem Clarity** | "Is the problem statement clear? What's the root cause?"      |
| **Value**           | "Who benefits most? What's the business impact if NOT built?" |
| **Scope**           | "Is this one feature or multiple? Should it be split?"        |
| **Timing**          | "Is this urgent or can it wait? Any deadline drivers?"        |
| **Alternatives**    | "Any existing solutions or workarounds today?"                |

#### Validation Process

1. Select 2-3 questions based on idea complexity
2. Use `AskUserQuestion` with concrete options
3. Update idea artifact with clarifications
4. Skip validation only for trivial/obvious ideas

#### Validation Output

Update the `## Quick Validation` section in the idea artifact:

```markdown
## Quick Validation

**Validated:** {date}

- **Problem clarity:** {Confirmed/Clarified: notes}
- **Value confirmed:** {Yes/Needs discussion}
- **Scope check:** {Single feature/Needs splitting}
```

### 7. Suggest Next Step

- Output: "Idea captured and validated! To refine into a PBI, run: `/team-refine {filename}`"

## Output Format

Use template from `team-artifacts/templates/idea-template.md`

Add these fields to frontmatter:
```yaml
related_module: "{Module name or N/A}"
related_entities: []
related_features: []
```

Add to Related section:
```markdown
## Related
- **Module Docs**: [docs/business-features/{Module}/](docs/business-features/{Module}/)
- **Related Features**: {FR-XX IDs from INDEX.md}
- **Related Entities**: {Entity names from codebase}
```

## Module Discovery

Modules are discovered dynamically from `docs/business-features/*/README.md` frontmatter.

See `docs/templates/detailed-feature-docs-template.md` for frontmatter schema.

## Example

```bash
/team-idea "Advanced search filters for snippets"
```

### Example Flow

1. Detects "snippet" + "search" -> TextSnippet module
2. Loads TextSnippet INDEX.md, README.md
3. Shows existing Search Snippets feature (FR-TS-003)
4. Finds TextSnippetEntity with SnippetText, FullText, Tags properties
5. Gathers user input
6. Creates: `team-artifacts/ideas/260119-po-idea-advanced-search-filters.md`
7. **Validates**: Asks 2-3 quick questions about problem clarity, value, scope
8. Updates idea with validation summary

## Related
- **Role Skill:** `product-owner`
- **Next Step:** `/team-refine`

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

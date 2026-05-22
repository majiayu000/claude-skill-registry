---
name: refactor-skill
description: 'Refactor oversized or multi-domain skills into smaller, purpose-built skills while preserving full fidelity and capability coverage. Use when a skill spans too many topics, exceeds ~500 lines, or would benefit from clearer separation of concerns and independent invocation. This skill reviews the existing content, identifies logical boundaries, designs a split plan, generates new SKILL.md files for each extracted skill, and validates that the refactor maintains complete functional and content parity with the original.'
model: opus
argument-hint: "path to skill directory (or plugin) to refactor"
user-invocable: true
---

Refactoring LLM resources and prompts is the intentional restructuring of prompt content, tool definitions, and supporting context (e.g., skills, instructions, examples, guardrails) to improve composability, clarity, reuse, and invocation precision without changing the underlying capabilities, knowledge coverage, or output semantics of the original monolithic prompt.

At the architecture level, this refactoring decomposes a monolithic LLM skill into smaller, purpose-built, independently invocable skills with well-defined responsibilities, inputs, and outputs—reducing coupling and cognitive load, enabling targeted reuse and testing, and preserving behavioral parity through explicit contracts, shared primitives, and regression validation against the original monolith.

## Refactoring Workflow

You are focused on refactoring the skill found at the path: <path>$ARGUMENTS</path>

If no path is provided STOP and say: "No path provided. Please provide a path to a skill or plugin to refactor."
If the path points to a claude code plugin load the Skill `claude-plugins-reference-2026` which provides the current spec and details for how a plugin is defined, when provided a plugin path, you will be refactoring the skills found within the plugin skills/ directory.

The paths provided below, like `references/` are relative to the skill directory.

<workflow>

### Phase 1: Analysis

ANALYZE the source skill thoroughly:

1. **Read the complete SKILL.md** - every line, every section
2. **Read all reference files** in `references/` subdirectory
3. **Identify domains** - distinct topics, use cases, or tool patterns
4. **Map dependencies** - which sections reference others
5. **Assess size** - line counts per section, total complexity
6. **Note frontmatter** - tools, hooks, model requirements per domain

**Domain Identification Criteria:**

| Signal                        | Indicates Separate Skill      |
| ----------------------------- | ----------------------------- |
| Different tool requirements   | `tools` would differ          |
| Different invocation triggers | Description keywords diverge  |
| Independent use cases         | Can be used without the other |
| Different expertise domains   | Distinct knowledge areas      |
| Section size >200 lines       | Too large for single concern  |
| Different hook requirements   | Lifecycle needs differ        |

### Phase 2: Planning

PROPOSE a refactoring plan before executing:

```markdown
## Refactoring Plan: {original-skill-name}

### Current State
- Total lines: N
- Domains identified: N
- Reference files: N

### Proposed Skills

#### 1. {new-skill-name-1}
- **Focus**: {single sentence describing what can be achieved with this skill}
- **Sections to include**: {list}
- **Tools needed**: {list or "none"}
- **Estimated lines**: N
- **Dependencies**: {other new skills it references}

#### 2. {new-skill-name-2}
...

### Cross-Reference Strategy
- {skill-1} will reference {skill-2} for {topic}
- Shared concepts will be in {skill-name}

### Migration Notes
- Original monolithic skill will be: converted to facade/meta-skill that loads all new specialists
- Existing references will: continue to work via the facade (backwards compatible)

### Fidelity Checklist
- [ ] All sections accounted for
- [ ] All reference files (if any) are assigned
- [ ] All tools (if any) are covered
- [ ] All hooks (if any) are migrated
- [ ] No orphaned content
```

**STOP and present plan to user before proceeding.**

### Phase 3: Execution

AFTER user approval, create new skills:

#### 3a. Create Directory Structure

For each new skill:

```
{new-skill-name}/
├── SKILL.md
└── references/
    └── {migrated-files}.md
```

#### 3b. Write SKILL.md Files

Each new SKILL.md MUST have:

**Frontmatter:**

```yaml
---
name: {new-skill-name}
description: {focused description with trigger keywords}
allowed-tools: {only tools this skill needs}
model: {inherit or specific if needed}
user-invocable: true
---
```

**Content Structure:**

```markdown
# {Skill Title}

{One paragraph: what this skill does and when to use it}

## Related Skills

For {topic}, activate `Skill(command: "{related-skill-name}")`.

## {Main Sections}

{Content migrated from original skill}

## References

{Links to ./references/*.md files}
```

#### 3c. Migrate Reference Files

- MOVE relevant reference files to new skill's `references/`
- UPDATE internal links to use correct relative paths
- ADD back-links to parent SKILL.md
- SPLIT shared references if needed (copy with attribution)

#### 3d. Create Cross-References

Between new skills, use skill activation syntax:

```markdown
For advanced {topic}, activate the {skill-name} skill:
Skill(command: "{skill-name}")
```

Within same skill, use relative links:

```markdown
See [Topic Details](./references/topic.md)
```

### Phase 4: Validation

VERIFY refactoring completeness:

#### 4a. Coverage Check

Create a coverage matrix:

| Original Section | New Skill | New Location | Verified |
| ---------------- | --------- | ------------ | -------- |
| {section-name}   | {skill}   | {file:line}  | Y/N      |

**Every original section MUST appear in exactly one new skill.**

#### 4b. Fidelity Validation

For each new skill:

- [ ] Frontmatter valid (name, description present)
- [ ] Description includes trigger keywords
- [ ] Tools match content requirements
- [ ] All internal links resolve
- [ ] Reference files properly linked
- [ ] Cross-references to related skills present
- [ ] Under 500 lines (or justified exception)

#### 4c. No-Loss Verification

Compare capabilities:

```
ORIGINAL SKILL CAPABILITIES:
- {capability 1}
- {capability 2}
...

NEW SKILLS COMBINED CAPABILITIES:
- {capability 1} -> {skill-name}
- {capability 2} -> {skill-name}
...

MISSING: {none or list}
DUPLICATED: {none or list with justification}
```

### Phase 5: Backwards-Compatible Conversion (MANDATORY)

CONVERT the original skill to a facade/meta-skill that loads all new specialist skills:

**CRITICAL: This step is NOT optional. Deleting the original skill is a breaking change.**

1. **Convert original to meta-skill** - REPLACE content with facade that loads all new skills:

```yaml
---
name: {original-name}
description:"{Original description}. Loads focused specialist skills: {skill-1}, {skill-2}, {skill-3}."
user-invocable: true
---

# {Original Name}

This skill loads focused specialist components for comprehensive coverage:

## Specialist Skills

- **{skill-1}**: {description} - `Skill(command: "{skill-1}")` for {use case}
- **{skill-2}**: {description} - `Skill(command: "{skill-2}")` for {use case}
- **{skill-3}**: {description} - `Skill(command: "{skill-3}")` for {use case}

## Usage

**Full coverage**: `Skill(command: "{original-name}")` loads all specialist skills
**Focused work**: Activate specific specialist skill for targeted context

## Quick Reference

{Brief summary of when to use which specialist skill}
```

2. **Verify backwards compatibility**:

   - Search for all references: `grep -r "Skill(command: \"{original-name}\")" .`
   - Search for all slash command invocations: `grep -r "/{original-name}" .`
   - Confirm all existing references will continue to work

3. **Update external references** - other skills/commands can optionally point to specific specialists, but MUST NOT be required to change

</workflow>

## Frontmatter Best Practices

<frontmatter_rules>

### Name Field

- Lowercase letters, numbers, hyphens only
- Max 64 characters
- Descriptive but concise: `python-async`, `git-workflow`, `api-design`

### Description Field

- Max 1024 characters
- Include ACTION verbs: "Generate", "Analyze", "Create", "Debug"
- Include TRIGGER phrases: "Use when", "Activate for", "Helps with"
- Include KEYWORDS users might mention

**Template:**

```
{Action 1}, {Action 2}, {Action 3}. Use when {situation 1}, {situation 2},
or when working with {keywords}. Related to {domain}.
```

**Example:**

```yaml
description: 'Debug Python async code, identify race conditions, fix deadlocks. Use when dealing with asyncio, aiohttp, or concurrent Python code. Helps with coroutines, event loops, and async context managers.'
```

### allowed-tools Field

When making single task skills include tools the skill actually needs to help reduce context noise:
This includes MCP servers, Bash commands, and whatever other tools this skill needs to perform its task.

```yaml
allowed-tools: Read, Grep, Glob, mcp__sequential_thinking__*, mcp__git-forensics__*, mcp__ref__*, mcp__context7__*         # Read-only analysis with web based fact checking
allowed-tools: Bash(pytest:*), Bash(uv run pytest:*)             # Specific command patterns for testing
```

</frontmatter_rules>

## Splitting Strategies

<strategies>

### By Use Case

Split when skill serves multiple distinct user needs:

```
python-development -> python-testing
                   -> python-packaging
                   -> python-async
                   -> python-typing
```

### By Tool Requirements

Split when sections need different tool access:

```
code-review -> code-review-read-only (Read, Grep, Glob, mcp__git-forensics__*, Bash(ruff:*), Bash(pytest:*), Bash(uv run ruff:*), Bash(uv run pytest:*))
            -> code-review-with-fixes (Read, Write, Edit, Bash(ruff:*), Bash(pytest:*), Bash(uv run ruff:*), Bash(uv run pytest:*))
```

### By Expertise Domain

Split when skill covers distinct knowledge areas:

```
web-development -> frontend-react
                -> backend-api
                -> database-design
                -> deployment-docker
```

### By Complexity Level

Split when skill has beginner and advanced content:

```
git-workflow -> git-basics
             -> git-advanced
             -> git-team-workflows
```

### By Lifecycle Phase

Split when skill covers different project phases:

```
project-setup -> project-init
              -> project-config
              -> project-ci-cd
```

</strategies>

## Quality Standards

<quality>

### Each New Skill MUST

1. Have a single, clear focus
2. Be usable independently (or document dependencies)
3. Have description with trigger keywords
4. Be under 500 lines (SKILL.md content)
5. Use progressive disclosure (link to references)
6. Cross-reference related skills appropriately

### Refactoring MUST NOT

1. Lose any information from original
2. Create orphaned reference files
3. Break existing workflows
4. Duplicate content without justification
5. Create circular dependencies
6. Over-fragment (don't create skills <50 lines)
7. **DELETE the original skill** - it MUST become a facade/meta-skill that loads all new specialist skills
8. **INTRODUCE breaking changes** - existing references to the original skill (e.g., `Skill(command: "python3-development")` or `/python3-development`) MUST continue to work

### Minimum Viable Skill Size

A skill should have enough substance to be useful alone:

- At least 50 lines of meaningful content
- At least 2-3 distinct instructions or rules
- Clear value proposition in description

</quality>

## Report Format

<report>

After completing refactoring, produce:

```markdown
# Skill Refactoring Report: {original-skill-name}

## Summary
- **Original**: {lines} lines, {sections} sections
- **Result**: {N} new skills
- **Coverage**: 100% (all content migrated)

## New Skills Created

| Skill | Lines | Focus | Location |
|-------|-------|-------|----------|
| {name} | N | {focus} | `skills/{name}/` |

## Cross-Reference Map

```

{skill-1} <---> {skill-2} (shared: {topic})
{skill-2} ----> {skill-3} (references: {topic})

```

## Migration Details

### {new-skill-1}
- **Source sections**: {list from original}
- **Reference files**: {list}
- **New content added**: {if any}

### {new-skill-2}
...

## Validation Results

| Check | Status |
|-------|--------|
| All sections migrated | PASS/FAIL |
| No orphaned references | PASS/FAIL |
| All links valid | PASS/FAIL |
| Frontmatter valid | PASS/FAIL |
| Size limits respected | PASS/FAIL |

## Action Items

- [ ] Review new skills for accuracy
- [ ] Test skill activation triggers
- [ ] Verify facade/meta-skill loads all new specialists
- [ ] Test backwards compatibility with existing references
- [ ] Test with `claude --plugin-dir ./plugins/plugin-name`
```

</report>

## Example Invocations

```
Task(
  agent="plugin-creator:refactor-skill",
  prompt="Refactor ./plugins/python3-development/skills/python3/SKILL.md into focused skills for testing, async, and packaging"
)
```

```
Task(
  agent="plugin-creator:refactor-skill",
  prompt="The fastmcp-creator skill is too large. Analyze it and propose how to split it into smaller skills"
)
```

```
Task(
  agent="plugin-creator:refactor-skill",
  prompt="Split the git-workflow skill by expertise level: basics, advanced, and team workflows"
)
```

## Interaction Protocol

<interaction>

### Starting Refactoring

WHEN invoked:

1. CONFIRM the skill path
2. READ the complete skill and all references
3. ANALYZE for domains and split points
4. PRESENT refactoring plan

### During Execution

AS you create skills:

- ANNOUNCE each skill: "Creating skill: {name}..."
- SHOW frontmatter for validation
- REPORT reference file migrations
- FLAG any decisions made

### Completion

WHEN finished:

- PRESENT refactoring report
- HIGHLIGHT any concerns or edge cases
- REMIND to test with `claude --plugin-dir ./plugins/plugin-name`
- OFFER to adjust if needed

</interaction>

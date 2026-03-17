---
name: BuildSkill
version: 0.1.0
description: "Create and validate skills for forge modules. USE WHEN create skill, new skill, write skill, validate skill, check skill, skill structure, skill conventions."
---

# BuildSkill

Create and validate skills following forge conventions. Skills are markdown files (SKILL.md) with YAML frontmatter that teach AI coding tools new capabilities.

## Workflow Routing

| Workflow | Trigger | Section |
|----------|---------|---------|
| **Create** | "create a skill", "new skill", "write a skill" | [Create Workflow](#create-workflow) |
| **Validate** | "validate skill", "check skill structure" | [Validate Workflow](#validate-workflow) |

## Skill Conventions

### SKILL.md Structure

Every skill is a single `SKILL.md` file with YAML frontmatter:

```yaml
---
name: SkillName
description: What it does. USE WHEN trigger phrase one, trigger phrase two, or trigger phrase three.
---
```

**Frontmatter rules:**
- `name:` -- PascalCase for multi-word (e.g., `VaultOperations`, `DailyPlan`), natural casing for single words (e.g., `Log`, `Draft`, `Init`)
- `version:` -- semantic version (required for module skills, optional for personal/vault skills)
- `description:` -- single line, under 1024 characters, includes `USE WHEN` with intent-based triggers joined by commas/OR
- Optional: `argument-hint:` for skills invoked with `/SkillName <args>` (e.g., `"[natural language description]"`)
- No separate `triggers:` or `workflows:` arrays in YAML

### Body Structure

```markdown
# SkillName

Brief description of what the skill does.

## Instructions (or ## Usage)

Step-by-step procedure. Use plain numbered lists for sequential operations.

1. First action
2. Second action
3. Third action

## Constraints

- Boundary conditions and rules
- What NOT to do
```

**Instruction format**: Use plain numbered lists (1, 2, 3) — not labeled steps (`### Step 1:`, `### Phase 2:`, `### Step M1:`). Headings within Instructions are for separating modes or major sections, not for individual steps. This follows the Fabric/PAI pattern convention.

**For skills with multiple workflows:** Use `## Workflow Routing` table in the body linking to sections within the same file. Keep everything in one SKILL.md unless it exceeds ~200 lines. Extract reference material (schema templates, configuration examples, lookup tables) into companion files loaded via `@` -- SKILL.md should focus on flow and routing, not static data.

### Where Skills Live

| Location | Purpose |
|----------|---------|
| `skills/SkillName/` | Module skills (shipped with a module) |
| User vault workspace | Personal/experimental skills |

All parent directories must be registered in `plugin.json` under the `skills` array for Claude Code discovery. Other providers (Gemini, Codex, OpenCode) use `make install` from the module's Makefile.

### Naming Conventions

| Component | Convention | Examples |
|-----------|-----------|----------|
| Skill directory | PascalCase | `BuildSkill`, `DailyPlan`, `VaultOperations` |
| Single-word skill | Natural case | `Log`, `Draft`, `Init`, `Update` |
| SKILL.md | Always `SKILL.md` | -- |

### CLI Tool Integration

When a skill wraps a CLI tool (Rust binary, shell script), include:

1. **Tool location** -- where the binary lives
2. **Usage examples** -- concrete `bash` blocks showing invocation
3. **Intent-to-flag mapping** -- table translating natural language to CLI flags
4. **Output format** -- what the tool returns (JSONL, plain text, etc.)

### Canon + Sidecar Pattern

Module skills use two files side by side:

| File | Purpose | Contains |
|------|---------|----------|
| `SKILL.md` | **Canon** -- frontmatter + skill body | `name:`, `description:`, `version:`, instructions |
| `SKILL.yaml` | **Sidecar** -- everything else | `sources:`, provider keys, Obsidian metadata |

**SKILL.yaml must NOT duplicate SKILL.md fields** -- no `name:` or `description:` in the sidecar. It carries supplementary data:

```yaml
sources:                              # upstream documentation links
    - https://example.com/docs

claude:                               # merged into installed SKILL.md frontmatter
    argument-hint: "[file path]"      # hint shown during / autocomplete
    disable-model-invocation: true    # prevents Claude auto-loading
    user-invocable: false             # hides from / menu
    allowed-tools: Read, Grep, Glob   # tools usable without permission
    model: claude-sonnet-4-6          # model override when skill is active
    context: fork                     # run in subagent context
    agent: Explore                    # subagent type (with context: fork)

user:                                 # free-form namespace (personal metadata)
    priority: high
```

**`claude:` key details:** `install-skills` reads all key-value pairs under `claude:` and merges them into the installed SKILL.md frontmatter. Any [Claude Code skill frontmatter field](https://code.claude.com/docs/en/skills) can go here. Put them in the sidecar instead of SKILL.md to protect them from Obsidian Linter reformatting. Codex uses TOML-based [multi-agent configuration](https://developers.openai.com/codex/multi-agent/), not YAML skill frontmatter — check the provider docs for the latest supported keys.

The sidecar is also the landing zone for Obsidian Linter — any `title:`, `aliases:`, `tags:`, or other vault metadata the Linter injects lands here, not in the canon. The `user:` namespace is free-form for personal metadata.

**Minimal sidecar** (skills without external references or provider-specific config):

```yaml
sources: []
```

Every SKILL.yaml must have `sources:` even if empty. Add `claude:` keys only when needed (argument-hint, model override, etc.).

**Why separate files?** Obsidian's Linter reformats frontmatter on save -- it adds `title:`, reorders keys, and may strip unrecognized fields like `name:`. Separating prevents cross-contamination.

### Multi-Provider Routing

Provider routing is controlled by the module's `defaults.yaml`, not by individual SKILL.yaml files. The `install-skills` binary reads provider-keyed allowlists to decide which skills deploy where:

```yaml
# defaults.yaml
skills:
    claude:
        SkillName:
    gemini:
        SkillName:
    codex:
        SkillName:
    opencode:
        SkillName:
```

Skills listed under a provider key are installed for that provider. Skills omitted from a provider's list are skipped. This allows Claude-only skills (e.g., those using TeamCreate or agent teams) to be excluded from Gemini/Codex/OpenCode without per-skill configuration.

---

## Create Workflow

### Step 1: Understand the request

Determine:
1. What does this skill do?
2. What should trigger it? (intent phrases for `USE WHEN`)
3. Does it wrap a CLI tool, or is it purely procedural?
4. Which module should it live in?

If the user hasn't specified, ask using AskUserQuestion.

### Step 2: Write the SKILL.md

Follow the structure from [Skill Conventions](#skill-conventions) above.

**Checklist while writing:**
- [ ] Frontmatter has `name:` and `description:` with `USE WHEN`
- [ ] Description is single-line, under 1024 characters
- [ ] Body starts with `# SkillName` heading
- [ ] Clear step-by-step instructions (numbered steps for sequential operations)
- [ ] If wrapping a CLI tool: usage examples, intent-to-flag mapping, output format
- [ ] Constraints section with boundary conditions
- [ ] No unnecessary complexity -- minimum needed for the task
- [ ] If module skill: SKILL.yaml sidecar with `sources:` field
- [ ] Skill listed in module's `defaults.yaml` under each target provider

### Step 3: Create the skill directory and file

```bash
mkdir -p skills/SkillName
```

Write the SKILL.md using the Write tool.

### Step 4: Register

For Claude Code: ensure the skill's parent directory is listed in `plugin.json` under `skills`.

For other providers: run `make install` from the module's Makefile.

### Step 5: Verify

1. Test invocation: does the description trigger correctly?
2. Review: does the procedure work end-to-end?

---

## Validate Workflow

### Step 1: Read the target skill

Read the SKILL.md file.

### Step 2: Check frontmatter

- [ ] `name:` present and uses correct casing
- [ ] `description:` is single-line with `USE WHEN` clause
- [ ] `description:` is under 1024 characters
- [ ] No deprecated fields (`triggers:`, `workflows:` arrays)
- [ ] Optional fields (`argument-hint:`, `version:`) are correctly formatted

### Step 3: Check body structure

- [ ] Starts with `# SkillName` heading (matches `name:` frontmatter)
- [ ] Has clear instructions (numbered steps, usage section, or workflow routing)
- [ ] If multiple workflows: `## Workflow Routing` table present
- [ ] Constraints or rules section for boundary conditions
- [ ] No unnecessary sections or boilerplate

### Step 4: Check CLI tool integration (if applicable)

- [ ] Tool path is documented
- [ ] Usage examples with `bash` blocks
- [ ] Intent-to-flag mapping table (if tool has flags)
- [ ] Output format described

### Step 5: Report

**COMPLIANT** -- all checks pass.

**NON-COMPLIANT** -- list failures with specific fixes. Offer to fix automatically.

---

## Constraints

- Every skill MUST have `name:` and `description:` in frontmatter
- Description MUST include `USE WHEN` trigger phrases
- PascalCase for multi-word skill names, natural case for single words
- Skill directory name must match the `name:` field
- Prefer one SKILL.md per skill -- split reference material into companion files (`@`) when SKILL.md exceeds ~200 lines or contains dense static data (schema templates, config examples, lookup tables)

---
name: stitch-skill-creator
description: Meta-skill for creating new stitch-kit skills. Enforces naming conventions, SKILL.md structure, examples format, and the Design-First SOP. Use when adding new framework support, a new domain-specific prompt architect, or any new capability to the stitch-kit plugin.
allowed-tools:
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch Skill Creator

A factory for creating new **stitch-kit skills**. Enforces standard structure, naming conventions, and the plugin's architectural patterns.

## When to use this skill

- Adding support for a new framework (e.g. "Astro", "Qwik", "Flutter")
- Creating a domain-specific prompt architect (e.g. `stitch-ui-ecommerce-architect`)
- Adding a new quality tool (e.g. `stitch-performance`, `stitch-seo`)
- Any time you need a new SKILL.md that integrates with the stitch-kit ecosystem

---

## Naming conventions

| Skill type | Name pattern | Example |
|------------|-------------|---------|
| Framework conversion | `stitch-[framework]-components` | `stitch-astro-components` |
| Domain prompt architect | `stitch-ui-[domain]-architect` | `stitch-ui-ecommerce-architect` |
| MCP wrapper | `stitch-mcp-[tool-name]` | `stitch-mcp-edit-screen` |
| Quality / analysis tool | `stitch-[capability]` | `stitch-performance` |
| Meta / utility | `stitch-[name]` | `stitch-setup` |

**Rules:**
- Always kebab-case
- Always starts with `stitch-`
- Framework conversion skills end with `-components`
- MCP wrappers follow `stitch-mcp-{snake_case_tool → kebab}` from `docs/mcp-naming-convention.md`

---

## Required directory structure

```
skills/[skill-name]/
├── SKILL.md              ← Required: frontmatter + workflow (keep under 500 lines)
├── examples/
│   └── usage.md          ← Required: 2+ worked examples
├── resources/            ← Optional: templates, checklists, reference tables
│   ├── component-template.[ext]
│   └── architecture-checklist.md
├── scripts/              ← Optional: bash scripts
│   └── fetch-stitch.sh   ← Copy from stitch-mcp-get-screen/scripts/ if needed
└── references/           ← Optional: style guides, contracts, long reference docs
```

---

## SKILL.md template

```markdown
---
name: stitch-[skill-name]
description: [One clear sentence — when to use this skill and what it does. This is used for routing by the orchestrator and for marketplace display.]
allowed-tools:
  - "stitch*:*"   # Include if skill calls Stitch MCP tools
  - "Bash"        # Include if skill runs shell commands
  - "Read"        # Usually yes
  - "Write"       # Usually yes
---

# Stitch → [Target] [Type]

**Constraint:** Only use this skill when the user explicitly mentions "Stitch" [and any additional trigger condition].

[One sentence explaining what this skill does and who the agent "is" while using it.]

## When to use this skill vs. similar skills

[Table comparing this skill to its nearest alternatives — help the orchestrator route correctly]

## Prerequisites

[What the user/environment needs before this skill can run]

## Step 1: Retrieve the design

1. Run `list_tools` → find Stitch MCP prefix
2. Call `[prefix]:get_screen` with numeric `projectId` and `screenId`
3. Download HTML: `bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"`

## Step 2: [Core conversion / workflow]

[The main logic of this skill]

## Step N: Output

[What the skill produces — files, code, commands]

## Troubleshooting

| Issue | Fix |
|-------|-----|

## References

- `resources/component-template.[ext]` — [description]
- `resources/architecture-checklist.md` — Pre-ship checklist
- `scripts/fetch-stitch.sh` — Reliable GCS HTML downloader
```

---

## Examples template (examples/usage.md)

```markdown
# [Skill Name] — Usage Examples

## Example 1: [Scenario title]

**User:** "[Specific user request]"

**Skill activates because:** [Why this triggers the skill]

**What the skill does:**
1. [Step 1]
2. [Step 2]
3. ...

**Output:**
[Description or code snippet of what gets generated]

---

## Example 2: [Different scenario]

[Same format]
```

---

## Architecture checklist template (resources/architecture-checklist.md)

Adapt this to the target platform/framework:

```markdown
# [Framework] Components — Architecture Checklist

Run through this checklist before marking the task complete.

## Structure
- [ ] [Project structure check]
- [ ] Components are in separate files

## [Framework-specific category]
- [ ] [Framework-specific check]

## TypeScript / Types
- [ ] No `any` types
- [ ] All props have Readonly<> wrapper

## Dark mode
- [ ] Theme tokens used everywhere — no hardcoded colors

## Accessibility
- [ ] All interactive elements are keyboard accessible
- [ ] Images have descriptive alt text

## Performance
- [ ] No console.log in production code
```

---

## Creating a framework conversion skill

For a new framework (e.g. Astro):

### 1. Create the directory

```bash
mkdir -p skills/stitch-astro-components/resources
mkdir -p skills/stitch-astro-components/examples
mkdir -p skills/stitch-astro-components/scripts
```

### 2. Copy the fetch script

```bash
cp skills/stitch-mcp-get-screen/scripts/fetch-stitch.sh \
   skills/stitch-astro-components/scripts/fetch-stitch.sh
```

### 3. Write SKILL.md

Use the template above. Key sections for framework skills:
- **When to use vs. similar skills** — distinguish from Next.js, Svelte, etc.
- **Project structure** — show the file layout
- **HTML → Framework mapping** — table of HTML/CSS patterns → framework equivalents
- **Design tokens** — how to handle Stitch's CSS variables in this framework
- **Dark mode** — how this framework handles it
- **Accessibility** — framework-specific ARIA patterns

### 4. Create component template

Write `resources/component-template.[ext]` — a working boilerplate component that demonstrates:
- Props interface
- Theme token usage
- Dark mode
- Accessibility attributes
- Conditional rendering patterns

### 5. Create architecture checklist

Write `resources/architecture-checklist.md` with framework-specific checks.

### 6. Write examples

At least 2 examples in `examples/usage.md`.

### 7. Register in marketplace.json

Add to the appropriate plugin group in `.claude-plugin/marketplace.json`:
- Web frameworks → `stitch-frameworks`
- Mobile → `stitch-mobile`
- New category → create a new group

### 8. Update docs/skills-index.md

Add the new skill to the table.

### 9. Update README.md

Add to the appropriate layer table.

---

## Creating a domain-specific prompt architect

For a new domain (e.g. e-commerce):

The skill name: `stitch-ui-ecommerce-architect`

This skill **does not generate or execute** — it produces a structured Stitch prompt. Pattern:

1. Identify domain-specific components (product card, cart, checkout flow, review stars, etc.)
2. Define the `[Context] [Layout] [Components]` prompt template for this domain
3. Reference `stitch-ued-guide` for visual vocabulary
4. Output is: a ready-to-use prompt for `stitch-mcp-generate-screen-from-text`

---

## References

- `docs/skills-index.md` — existing skills (check before creating duplicates)
- `docs/mcp-naming-convention.md` — MCP tool naming rules
- `stitch-nextjs-components/SKILL.md` — reference for a well-structured framework conversion skill
- `stitch-swiftui-components/SKILL.md` — reference for a mobile platform skill

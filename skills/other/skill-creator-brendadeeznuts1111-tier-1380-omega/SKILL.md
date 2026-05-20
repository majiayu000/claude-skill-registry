---
name: skill-creator
description: |
  Design effective Claude Code skills with optimal descriptions, progressive disclosure, and error prevention patterns. Covers freedom levels, token efficiency, and quality standards.

  Use when: creating new skills, improving skill descriptions, optimizing token usage, structuring skill content, or debugging why skills aren't being discovered.
user-invocable: true
---

# Skill Creator

**Status**: Production Ready
**Last Updated**: 2026-01-09
**Dependencies**: None
**Reference**: [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator)

---

## Quick Start

**To scaffold a new skill**, use the `/create-skill` command:
```
/create-skill my-new-skill
```

**To design an effective skill**, continue reading this guide.

---

## Core Principles

### 1. The Context Window is a Public Good

Every token in your skill competes with conversation context. Be ruthlessly concise.

**Ask for each paragraph:**
- Does Claude genuinely need this?
- Could this be in `references/` instead of main SKILL.md?
- Is this duplicating information Claude already knows?

### 2. Progressive Disclosure

Load information in layers:

| Layer | When Loaded | Target Size | Content |
|-------|-------------|-------------|---------|
| **Metadata** | Always | 40-55 tokens | name + description |
| **SKILL.md** | When triggered | <5k words | Instructions, patterns |
| **Resources** | As needed | Variable | scripts/, references/, assets/ |

### 3. Freedom Levels

Match instruction specificity to error probability:

**High Freedom** (text instructions)
- For flexible approaches where multiple solutions work
- Example: "Structure components for reusability"

**Medium Freedom** (pseudocode/patterns)
- For preferred patterns with some flexibility
- Example: Show a pattern with `[CUSTOMIZE]` placeholders

**Low Freedom** (specific scripts/templates)
- For fragile operations where exact steps matter
- Example: Exact wrangler.jsonc configuration for D1 binding

---

## Writing Effective Descriptions

The description is **the most critical part** - it determines if your skill gets discovered.

### Target: 250-350 Characters

```yaml
# Too short (loses context):
description: "A skill for Tailwind"  # ❌ 25 chars

# Too long (wastes tokens):
description: "This comprehensive skill provides detailed knowledge..."  # ❌ 500+ chars

# Just right:
description: |
  Build modern UIs with Tailwind v4 + shadcn/ui. Covers CSS variable theming,
  component installation, dark mode, and semantic color tokens.

  Use when: setting up Tailwind v4, adding shadcn components, fixing theme issues,
  or troubleshooting "Cannot find module" errors.
```

### Two-Paragraph Structure

**Paragraph 1**: What you can build + key features (active voice)
**Paragraph 2**: When to use + error keywords for discovery

### Description Checklist

- [ ] Active voice ("Build X" not "This skill provides X")
- [ ] Specific technologies named
- [ ] 3-5 "Use when" scenarios
- [ ] 2-3 distinctive error messages/keywords
- [ ] No meta-commentary about the skill itself
- [ ] 250-350 characters total

### Bad vs Good Examples

```yaml
# ❌ Bad: Passive, vague, no discovery keywords
description: |
  This skill helps you with database operations. It provides patterns
  for working with data and can be useful in many situations.

# ✅ Good: Active, specific, discoverable
description: |
  Build type-safe database queries with Drizzle ORM and Cloudflare D1.
  Covers schema definition, migrations, relations, and transaction patterns.

  Use when: setting up D1 database, writing Drizzle schemas, debugging
  "no such table" or "D1_ERROR" issues.
```

---

## Skill Structure

### Required Files

```
skills/my-skill/
├── SKILL.md          # Main documentation (required)
└── README.md         # Auto-trigger keywords (required)
```

### Optional Resources

```
skills/my-skill/
├── scripts/          # Executable helpers
│   └── setup.sh      # Example: automated setup script
├── references/       # Extended documentation
│   └── api-guide.md  # Loaded when user needs deep details
└── assets/           # Templates, images
    └── config.json   # Template files for output
```

### When to Use Each

**scripts/**: Deterministic tasks that must be exact
- Database migrations
- Project scaffolding
- Configuration generation

**references/**: Extended documentation too long for SKILL.md
- Full API references
- Comprehensive troubleshooting guides
- Migration guides between versions

**assets/**: Template files for output
- Configuration file templates
- Boilerplate code
- Images/diagrams

---

## YAML Frontmatter

### Required Fields

```yaml
---
name: lowercase-hyphen-case
description: |
  [250-350 chars with "Use when:" section]
---
```

### Optional Fields

```yaml
---
name: my-skill
description: |
  [description - max 1024 chars]
allowed-tools:
  - Bash
  - Read
  - Write
---
```

**Note**: `allowed-tools` is an optional field to restrict which tools Claude can use. The `metadata:` field with `keywords:` array is commonly used in this repository for improved discoverability, though it's not officially documented in the Anthropic spec. Fields like `license:` are informational but not functionally used by Claude Code.

### Field Guidelines

- **name**: Lowercase letters, numbers, hyphens only. Max 64 chars. Gerund form recommended (e.g., `processing-pdfs`)
- **description**: Max 1024 chars. Must include what it does AND when to use it. Third-person perspective.
- **allowed-tools**: Restricts which tools Claude can use when skill is active (rare, optional)

---

## Common Mistakes

### 1. Description Too Vague

```yaml
# ❌ Won't be discovered
description: "Helps with authentication"

# ✅ Will be discovered
description: |
  Implement authentication with Clerk - React components, middleware,
  and Cloudflare Workers integration with JWT verification.

  Use when: adding auth to React apps, protecting API routes, or
  troubleshooting "clerk/backend" import errors.
```

### 2. Duplicating Claude's Knowledge

```yaml
# ❌ Claude already knows JavaScript basics
## Variables
Use `const` for constants and `let` for variables...

# ✅ Focus on what Claude might get wrong
## Critical: Cloudflare Workers Differences
- No `process.env` - use `env` parameter from fetch handler
- No Node.js `fs` module - use R2 or KV for storage
```

### 3. Missing Error Keywords

Skills are often triggered when users hit errors. Include common error messages:

```yaml
description: |
  ...
  Use when: troubleshooting "Cannot read properties of undefined",
  "NEXT_REDIRECT" errors, or hydration mismatches.
```

### 4. Overly Rigid Instructions

```markdown
# ❌ Too rigid (breaks if API changes)
Always call api.configure({ version: "2.1.0" }) first.

# ✅ Flexible with rationale
Configure the API client before making calls. The version should match
your installed package version (check package.json).
```

### 5. No Production Validation

Skills should be tested in real projects, not just theoretically correct:

```markdown
## Production Example

Tested in [Project Name]:
- Build time: 45 seconds
- Errors prevented: 6/6 documented issues
- Zero runtime errors after deployment
```

---

## Token Efficiency

### Measuring Efficiency

Compare tokens used with vs without skill:

| Metric | Without Skill | With Skill | Savings |
|--------|---------------|------------|---------|
| Setup tokens | ~15k | ~5k | 67% |
| Errors hit | 2-3 | 0 | 100% |
| Iterations | 3-4 | 1 | 75% |

### Optimization Techniques

1. **Move examples to references/**: Keep SKILL.md under 5k words
2. **Use code blocks strategically**: One good example > three mediocre ones
3. **Link don't duplicate**: Reference official docs instead of copying
4. **Prune ruthlessly**: If Claude knows it, don't include it

---

## Testing Your Skill

### Discovery Test

Ask Claude Code naturally:
```
"Help me set up [technology your skill covers]"
```

Claude should propose using your skill. If not:
- Check description has relevant keywords
- Verify README.md has auto-trigger keywords
- Ensure skill is symlinked to ~/.claude/skills/

### Functionality Test

Build a real project using only the skill's guidance:
- Did you need to search for additional information?
- Did you hit any errors the skill should have prevented?
- Was any instruction unclear or wrong?

### Verification Script

```bash
./scripts/check-metadata.sh <skill-name>
```

---

## Quality Checklist

Before committing a skill:

- [ ] Name is lowercase-hyphen-case, max 40 chars
- [ ] Description is 250-350 chars with "Use when:" section
- [ ] SKILL.md under 5k words
- [ ] All code examples tested and working
- [ ] Package versions verified current
- [ ] Known issues documented with sources (GitHub issues, etc.)
- [ ] Production tested (not just theoretically correct)
- [ ] README.md has auto-trigger keywords
- [ ] Symlinked and discoverable

---

## References

- **Official Spec**: https://github.com/anthropics/skills/blob/main/agent_skills_spec.md
- **Our Standards**: `planning/claude-code-skill-standards.md`
- **Checklist**: `ONE_PAGE_CHECKLIST.md`
- **Example Skills**: `skills/tailwind-v4-shadcn/`, `skills/cloudflare-d1/`

---

## Quick Command Reference

```bash
# Create new skill
/create-skill my-skill-name

# Install skill
./scripts/install-skill.sh my-skill-name

# Verify metadata
./scripts/check-metadata.sh my-skill-name

# Check all skills
./scripts/check-all-versions.sh

# Generate marketplace manifest
./scripts/generate-plugin-manifests.sh my-skill-name
```

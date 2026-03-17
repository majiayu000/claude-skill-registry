# Create Skill

Interactive wizard for creating new Claude Code skills from templates.

---

## Command Usage

`/create-skill [skill-name]`

- With name: `/create-skill cloudflare-analytics`
- Without name: `/create-skill` (interactive mode)

---

## Your Task

Guide the user through creating a new skill with proper structure, then install it for testing.

### Step 1: Gather Information

If skill name not provided as argument, show the interactive prompt:

```
═══════════════════════════════════════════════
   CREATE NEW SKILL
═══════════════════════════════════════════════

I'll help you create a new skill from the template.

What's the skill name?
(lowercase-hyphen-case, e.g., "tanstack-router" or "cloudflare-queues")

Your answer:
```

**Name validation:**
- Lowercase letters, digits, and hyphens only
- Must start with a letter
- Max 40 characters
- No underscores or spaces

If invalid:
```
⚠️  Skill name should be lowercase-hyphen-case.

Examples:
✅ tanstack-query
✅ cloudflare-r2
✅ react-hook-form

❌ TanstackQuery (no capitals)
❌ tanstack_query (no underscores)
❌ tanstack query (no spaces)

Try again:
```

### Step 2: Check if Exists

```bash
ls skills/<skill-name>/ 2>/dev/null
```

If exists:
```
❌ Skill "<skill-name>" already exists at skills/<skill-name>/

Options:
1. Choose a different name
2. Delete existing and start fresh
3. Edit the existing skill instead

Your choice (1-3):
```

### Step 3: Ask Skill Type

```
What type of skill is this?

1. Cloudflare  - Workers, D1, R2, KV, AI, etc.
2. AI/ML       - OpenAI, Anthropic, Gemini, AI SDK
3. Frontend    - React, UI libraries, styling
4. Auth        - Authentication providers
5. Database    - ORMs, data stores
6. Tooling     - CLI tools, build systems, MCPs
7. Generic     - Standard template (no customization)

Your choice [1-7]:
```

### Step 4: Create Skill Directory

```bash
# Copy template
cp -r /home/jez/Documents/claude-skills/templates/skill-skeleton/ /home/jez/Documents/claude-skills/skills/<skill-name>/

# Verify creation
ls -la /home/jez/Documents/claude-skills/skills/<skill-name>/
```

### Step 5: Auto-populate Fields

**In SKILL.md**, replace:
- `name:` → the skill name provided
- `Last Updated` → today's date (YYYY-MM-DD)
- `Verified` date → today's date
- `Status` → Beta

**In README.md**, replace:
- Title → skill name as Title Case
- `Last Updated` → today's date
- `Status` → Beta

### Step 6: Apply Type-Specific Guidance

Based on skill type choice, mention the reference example:

| Type | Reference Skill | Key Reminder |
|------|-----------------|--------------|
| Cloudflare | `skills/cloudflare-d1/` | Check cloudflare-docs MCP, prerequisite: cloudflare-worker-base |
| AI/ML | `skills/ai-sdk-core/` | Verify model names are current, add rate limiting |
| Frontend | `skills/tailwind-v4-shadcn/` | Component patterns, TypeScript types |
| Auth | `skills/clerk-auth/` | Security considerations, token handling |
| Database | `skills/drizzle-orm-d1/` | Schema patterns, migration workflow |
| Tooling | `skills/fastmcp/` | CLI usage patterns, integration examples |
| Generic | `templates/skill-skeleton/` | Standard template |

### Step 7: Run Metadata Check

```bash
./scripts/check-metadata.sh <skill-name>
```

Report any issues found.

### Step 8: Install the Skill

```bash
/plugin install ./skills/<skill-name>
```

---

## Output: Show Summary

After successful creation, display:

```
═══════════════════════════════════════════════
   ✅ SKILL CREATED: <skill-name>
═══════════════════════════════════════════════

Type: [Selected type]
Reference: skills/[reference-skill]/

Created files:
  skills/<skill-name>/
  ├── SKILL.md              ← Main documentation (fill TODOs)
  ├── README.md             ← Auto-trigger keywords
  ├── scripts/              ← Helper scripts (optional)
  ├── references/           ← Reference docs (optional)
  └── assets/               ← Templates/images (optional)

Installed to: ~/.claude/skills/<skill-name>/

═══════════════════════════════════════════════
   NEXT STEPS
═══════════════════════════════════════════════

1. Fill in SKILL.md TODOs:
   • Description with "Use when" scenarios (250-350 chars)
   • Quick Start guide
   • Critical rules (Always Do / Never Do)
   • Known issues with sources (GitHub links)
   • Package versions with verification date

2. Fill in README.md TODOs:
   • Auto-trigger keywords (primary, secondary, error-based)
   • Token efficiency metrics
   • When to use / don't use

3. Add resources (optional):
   • scripts/ - Automation scripts
   • references/ - Docs Claude can load
   • assets/ - Templates, images

4. Test discovery:
   Ask Claude Code: "Help me with <skill topic>"
   Claude should discover and offer to use the skill.

5. Verify with checklist:
   See ONE_PAGE_CHECKLIST.md

6. Commit when ready:
   git add skills/<skill-name>
   git commit -m "Add <skill-name> skill"

═══════════════════════════════════════════════

Would you like me to open SKILL.md to start filling in the TODOs?
```

---

## Error Handling

**If template directory missing:**
```
❌ Template not found at templates/skill-skeleton/

This repo may not be set up correctly.
Run: ls templates/
```

**If install script fails:**
```
⚠️  Skill created but install failed.

Manual install using plugin system:
/plugin install ./skills/<skill-name>

Then restart Claude Code to load the skill.
```

**If metadata check fails:**
```
⚠️  Metadata issues found - fix before committing.

Common issues:
• Missing name: field
• Description too short/long
• Invalid YAML frontmatter
```

---

## Example Session

```
User: /create-skill

Claude:
═══════════════════════════════════════════════
   CREATE NEW SKILL
═══════════════════════════════════════════════

What's the skill name?
(lowercase-hyphen-case, e.g., "tanstack-router")

User: tanstack-router

Claude:
What type of skill is this?

1. Cloudflare  2. AI/ML  3. Frontend  4. Auth  5. Database  6. Tooling  7. Generic

User: 3

Claude: Creating skill "tanstack-router"...

[Creates directory, pre-fills files, installs]

═══════════════════════════════════════════════
   ✅ SKILL CREATED: tanstack-router
═══════════════════════════════════════════════

Type: Frontend
Reference: skills/tailwind-v4-shadcn/

[Shows file structure and next steps]

Would you like me to open SKILL.md to start filling in the TODOs?
```

---

## Important Notes

- Skills are symlinked to `~/.claude/skills/` for Claude Code to discover
- Fill ALL [TODO] markers in SKILL.md before committing
- Description: 250-350 characters with "Use when:" scenarios
- Include keywords IN the description text
- ONLY valid frontmatter fields: `name`, `description`, `allowed-tools`
- Do NOT use `license:` or `metadata:` in frontmatter
- Test with `check-metadata.sh` before committing

---

## Quick Reference

| Item | Location |
|------|----------|
| Template | `templates/skill-skeleton/` |
| Skills | `skills/` |
| Install command | `/plugin install ./skills/<name>` |
| Metadata check | `scripts/check-metadata.sh` |
| Checklist | `ONE_PAGE_CHECKLIST.md` |
| Standards | `planning/claude-code-skill-standards.md` |

---

**Version**: 1.1.0
**Last Updated**: 2025-12-04

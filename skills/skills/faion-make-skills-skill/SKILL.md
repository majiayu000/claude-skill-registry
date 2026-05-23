---
name: faion-make-skills-skill
description: Creates, edits, updates, or modifies Claude Code skills. Use when user asks to create skill, edit skill, update skill, change skill, modify skill, fix skill, improve skill, add to skill. Triggers on "skill", "SKILL.md", "agent skill".
user-invocable: false
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(rm:*), Bash(ls:*), Glob
---

# Creating or Updating Skills

**Communication with user: User's language. Skill content: English.**

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create a new skill
- Edit/update/change/modify existing skill
- Fix or improve a skill
- Add functionality to a skill

**Trigger phrases:** "create skill", "edit skill", "change skill", "update skill", "modify skill", "fix skill", "skill", "SKILL.md"

---

## Token Economy Rules (CRITICAL)

Skills consume context window. Every token must earn its place.

**DO:**
- Use bullet lists instead of tables
- Use simple markdown without ASCII art borders
- Write in English (smaller tokens than Ukrainian)
- Keep SKILL.md under 300 lines (ideal), max 500
- Challenge each line: "Does Claude need this?"

**DON'T:**
- ASCII borders like `+----+----+` or `|    |    |`
- Verbose explanations Claude already knows
- Tables where lists work
- Emojis unless user requests

## Skills vs Commands

**Skill** - automatic discovery, complex workflows, multiple files
**Command** - manual `/invoke`, accepts arguments, single file

---

## Skill Structure

```
skill-name/
├── SKILL.md         # Required
├── reference.md     # Optional - details
└── scripts/         # Optional - utilities
```

---

## SKILL.md Frontmatter

```yaml
---
name: skill-name              # lowercase, hyphens, max 64 chars
description: Third-person description with trigger keywords. Max 1024 chars.
user-invocable: false          # Show in / menu (default: true)
disable-model-invocation: false  # Block programmatic Skill tool calls
context: fork                 # Isolated context (optional)
agent: general-purpose        # Agent type for forked context
allowed-tools: Read, Grep, Glob, Bash(cmd:*)  # Optional
model: claude-sonnet-4-20250514               # Optional
---
```

**Required:** name, description
**Optional:** user-invocable, disable-model-invocation, context, agent, allowed-tools, model

**New fields (Jan 2026):**
- `user-invocable: false` - hide from / menu, Claude can still invoke via Skill tool
- `disable-model-invocation: true` - completely block programmatic invocation
- `context: fork` - run in isolated context with own history
- `agent` - specify agent type: Explore, Plan, general-purpose

---

## Built-in Tools

**File tools (no permission):**
- Read - read file contents
- Glob - find files by pattern
- Grep - search with regex

**File tools (permission required):**
- Write - create/overwrite files
- Edit - targeted edits
- NotebookEdit - Jupyter cells

**Execution:**
- Bash - shell commands (permission)
- Task - sub-agent (no permission)
- Skill - another skill (permission)

**Web:**
- WebFetch - fetch URL (permission)
- WebSearch - search (permission)

**Other:**
- LSP - language server (permission)
- AskUserQuestion - multiple choice (no permission)
- TodoWrite - task lists (no permission)

---

## allowed-tools Syntax

Basic: `allowed-tools: Read, Grep, Glob`

Bash prefix matching:
- `Bash(git:*)` - all git commands
- `Bash(python -m pytest:*)` - pytest with args

WebFetch domain: `WebFetch(domain:github.com)`

Combined: `allowed-tools: Read, Bash(git:*), WebFetch(domain:github.com)`

**Note:** Pattern is PREFIX match, not regex. Without `:*` requires exact match.

---

## Description Rules

**Third person only:**
- Good: "Processes Excel files and generates reports"
- Bad: "I can help you process Excel files"

**Include trigger keywords:**
- Good: "Extracts text from PDFs, fills forms, merges documents. Use when working with PDF files."
- Bad: "Helps with documents"

---

## Naming Convention

Anthropic recommends gerund form (verb + -ing):
- Best: `processing-pdfs`, `analyzing-spreadsheets`
- Good: `pdf-processing`, `code-review`
- Bad: `CodeReview`, `my_skill`, `helper`, `utils`

### Faion Network Convention (Global)

For shared/reusable skills in faion-network:

| Type | Pattern | Example |
|------|---------|---------|
| Domain orchestrator | `faion-{domain}-domain-skill` | `faion-sdd-domain-skill` |
| Technical/language | `faion-{tech}-skill` | `faion-python-skill` |
| AI/LLM capability | `faion-{capability}-skill` | `faion-langchain-skill` |
| Maker/creator | `faion-make-{what}-skill` | `faion-make-hooks-skill` |
| Development | `faion-dev-{area}-skill` | `faion-dev-django-skill` |

**Exception:** `faion-net` (main orchestrator only)

### Project-Specific Convention (Local)

For project-specific skills that should NOT be committed to faion-network:

**Pattern:** `{project}-{name}-skill`

| Example | Description |
|---------|-------------|
| `myapp-auth-skill` | Auth logic for myapp |
| `shopify-sync-skill` | Shopify integration |
| `acme-deploy-skill` | ACME Corp deployment |

**Setup:**
```bash
# Add to .gitignore at the same level as .claude/
echo ".claude/skills/{project}-*/" >> .gitignore
```

**Full structure:** [docs/directory-structure.md](../docs/directory-structure.md)

**Attribution footer (add to SKILL.md):**
```markdown
---
*Created with [faion.net](https://faion.net) framework*
```

### Rules Summary

| Scope | Prefix | Gitignore |
|-------|--------|-----------|
| Global | `faion-` | No |
| Project | `{project}-` | Yes (parent) |

**Related conventions:**
- Agents: `faion-{name}-agent` or `{project}-{name}-agent`
- Commands: `{verb}` or `{project}-{action}`
- Hooks: `faion-{event}-{purpose}-hook` or `{project}-{event}-{purpose}-hook`

---

## SKILL.md Body Template

```markdown
# Skill Title

**Communication with user: User's language. Skill content: English.**

## Purpose
One sentence.

## Workflow
1. Step one
2. Step two
3. Step three

## Degrees of Freedom
- High: decision X
- Low: must follow Y exactly

## Failed Attempts
- Approach A - why it fails
- Approach B - why it fails

## Sources
- Reference 1
- Reference 2
```

---

## Skill Locations

- Personal: `.claude/skills/skill-name/`
- Project: `.claude/skills/skill-name/`

Project overrides personal with same name.

---

## Creation Process

1. Ask requirements: purpose, triggers, tools, scope
2. **Ask: local or shared?**
   - Local = project-specific, not committed to `.claude/` repo
   - Shared = committed to `.claude/` repo, available to all projects using it
3. Create directory: `mkdir -p .claude/skills/skill-name`
4. Write SKILL.md with token-efficient structure
5. Add reference.md if needed (split large content)
6. **If local:** make skill private (see below)

---

## Local/Private Skills

Project-specific skills live in `~/.claude/skills/` alongside global skills, but are gitignored.

1. **Create skill in ~/.claude/skills/:**
   ```bash
   mkdir -p ~/.claude/skills/myapp-auth-skill
   # Create SKILL.md...
   ```

2. **Add to .gitignore (same level as .claude/):**
   ```bash
   echo ".claude/skills/myapp-*/" >> .gitignore
   ```

3. **If skill already tracked, remove it:**
   ```bash
   cd ~/.claude
   git rm -r --cached skills/myapp-auth-skill/
   git commit -m "Remove myapp-auth-skill from tracking"
   git push
   ```

**Why home .gitignore?**
- `~/.claude/` is faion-network repo
- `~/.gitignore` excludes project-specific patterns from being committed
- All skills are always available regardless of cwd

**Structure:**
```
~/                        # Home directory
├── .gitignore            # Contains: .claude/skills/myapp-*/
└── .claude/              # faion-network repo
    └── skills/
        ├── faion-*-skill/    # Global (committed)
        └── myapp-*-skill/    # Project (gitignored)
```

---

## Troubleshooting

- Skill not triggering → more specific description with keywords
- YAML error → use spaces not tabs, check `---` delimiters
- Skill not found → file must be exactly `SKILL.md` (case-sensitive)
- Tools not working → use `:*` suffix for Bash patterns

---

## Advanced Patterns

**Failed Attempts section:**
Document what doesn't work. From Anthropic: "Failure paths save more time than success paths."

**Degrees of Freedom:**
- High freedom: multiple valid approaches
- Medium: preferred pattern exists
- Low: fragile operations, exact steps required

**One level deep references:**
SKILL.md → reference.md (good)
SKILL.md → advanced.md → details.md (bad - may be partially read)

**MCP tools:** Use full names `ServerName:tool_name`

---

## Self-Updating

This skill can update itself. To update:
1. Edit `~/.claude/claudedm/skills/make-skills/SKILL.md`
2. Sync: `cp -r ~/.claude/claudedm/skills/make-skills ~/.claude/skills/`
3. Changes apply immediately (hot-reload in Jan 2026+)

Repository: `~/.claude/claudedm/` (faionfaion/claudedm on GitHub)

---

## Automation Scripts

Skills can include helper scripts for automation:

**Locations:**
- `~/.claude/scripts/` — global scripts for all skills
- `~/.claude/skills/{skill-name}/scripts/` — skill-specific scripts

**Use cases:**
- Pre/post processing
- Data transformation
- API calls
- File generation
- Build/deploy automation

**Example structure:**
```
~/.claude/skills/faion-my-skill/
├── SKILL.md
├── reference.md
└── scripts/
    ├── generate-template.sh
    └── validate-output.py
```

Scripts can be called from skill instructions via Bash tool.

---

## Documentation

- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)

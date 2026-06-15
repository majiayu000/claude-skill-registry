---
name: unikit-rules
description: Add project-specific rules and conventions to .unikit/RULES.md for a {{engine_name}} project. Cross-checks new rules against the knowledge base in .unikit/memory/ (via RULES_INDEX.md) to detect overlap with existing core or stack rules. Use when user says "add rule", "remember this convention", "always do X in code", "never use Y", or wants to codify a coding standard. Also trigger when user corrects agent behavior and wants it remembered as a project rule.
argument-hint: "[rule text or topic]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UniKit Rules — Project Conventions

Add short, actionable rules to `.unikit/RULES.md`. Rules are project-specific overrides that take precedence over the base knowledge rules in `.unikit/memory/core/` and `.unikit/memory/stack/`.

Before adding any rule, cross-check it against RULES_INDEX.md to avoid duplicating what's already covered in the knowledge base. If a rule is already covered — tell the user and skip. If the rule contradicts or extends an existing knowledge base rule — add it as an explicit override to RULES.md with a note about what it overrides.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

Skill-specific rule:
- If the user provides a rule in a non-English language, translate it to English before writing to `.unikit/RULES.md`

## Workflow

### Step 0: Load Skill Context

Read `.unikit/skill-context/unikit-rules/SKILL.md` if it exists. Treat it as project-level overrides — when it conflicts with this SKILL.md, the skill-context wins.

### Step 1: Determine Mode

```
Check $ARGUMENTS:
├── Has text? → Mode A: Direct add
└── No arguments? → Mode B: Interactive
```

**Mode A** — user provided rule text:
```
/unikit-rules Never use var, always explicit types
```
→ Proceed to Step 2 with the provided text.

**Mode B** — no arguments:
→ Ask the user what rule to add. Offer examples relevant to {{engine_name}}/{{engine_code_language}}:
```
What rule or convention would you like to add?

Examples:
- Never use var — always declare explicit types
- MonoBehaviour injection via public Construct() with [Inject]
- All async methods must accept CancellationToken as last parameter
- Use canvas.enabled instead of SetActive for UI toggling
- Factory classes instead of Zenject PlaceholderFactory
```

### Step 2: Cross-Check Against Knowledge Base

This step prevents duplication and helps maintain a clean separation between project rules and knowledge base rules.

1. **Read `.unikit/memory/RULES_INDEX.md`** — get the list of all rule files with their descriptions and "Load When" hints.

2. **Identify potentially overlapping rule files** — based on the topic of the new rule, find rule files from the index that cover the same area. For example:
   - Rule about naming → check `code-style.md`
   - Rule about async/UniTask → check `reactive-async.md`
   - Rule about Zenject → likely already in `RULES.md` (Zenject DI section) or `design-principles.md`
   - Rule about Odin attributes → check `odin.md`

3. **Read the relevant rule file(s)** — only the ones that might overlap (not all of them).

4. **Determine the relationship:**

   | Situation | Action |
   |-----------|--------|
   | Rule already exists with the same meaning | Tell user: "This is already covered in `{file}`: {quote}". Skip. |
   | Rule contradicts an existing knowledge base rule | Add to RULES.md with override note. Tell user what it overrides. |
   | Rule extends/narrows an existing rule | Add to RULES.md. Mention the related base rule for context. |
   | Rule covers a new topic not in knowledge base | Add to RULES.md. |

### Step 3: Read or Create RULES.md

Check if `.unikit/RULES.md` exists.

**If it does NOT exist** → create it:

```markdown
# Project Rules

Project-specific rules that override or extend the base knowledge rules in `.unikit/memory/`.
For base code style see `rules/core/code-style.md`.

---

## General

- [new rule here]
```

**If it exists** → read it, find the appropriate section for the new rule.

### Step 4: Place Rule in the Right Section

RULES.md is organized by topic sections (e.g., `## Type Declarations`, `## Conditions`, `## Zenject DI`). Place the new rule under the section that best matches its topic.

**If a matching section exists** → append the rule at the end of that section as a `- ` list item.

**If no matching section exists** → create a new `## Section` before the last section in the file, then add the rule there. Choose a clear, short section name that describes the topic (e.g., `## Async Patterns`, `## UI Conventions`, `## Testing`).

**Formatting rules:**
- Each rule is a `- ` list item (can span multiple lines for tables/code blocks if needed)
- Keep rules short and actionable — directive language ("Never...", "Always...", "Use...")
- No duplicates — if a rule with the same meaning already exists in RULES.md, tell user and skip
- If user provides multiple rules at once, add each to its appropriate section

### Step 5: Also Check Existing RULES.md

Before writing, verify the new rule doesn't duplicate something already in RULES.md itself (not just the knowledge base). Read through existing rules and check for semantic overlap.

### Step 6: Write and Confirm

Use `Edit` to add the rule(s). Then confirm:

```
✅ Added to .unikit/RULES.md (section: {Section Name}):

- {the rule}

Cross-check: ✅ no overlap found
Cross-check: ⚠️ extends code-style.md rule on X
Cross-check: ⚠️ overrides reactive-async.md default for Y
```

## Priority Reminder

From RULES_INDEX.md, the override priority (highest wins):

1. `.unikit/RULES.md` — project-specific overrides (what this skill writes to)
2. `.unikit/ARCHITECTURE.md` — project architecture decisions
3. `.unikit/memory/core/*.md` — universal best practices
4. `.unikit/memory/stack/*.md` — framework-specific knowledge

Rules added by this skill have the highest priority and override everything below them. This is by design — project rules exist precisely to override defaults when the project needs something different.

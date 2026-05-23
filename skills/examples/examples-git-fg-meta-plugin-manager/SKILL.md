# Example: Basic Skill

This example shows a minimal, well-structured skill following all thecattoolkit_v3 standards.

---

## File Structure

```
skills/hello-world/
└── SKILL.md
```

---

## Complete SKILL.md

```markdown
---
name: hello-world
description: "Greets users with a friendly message. Use when you want to say hello or demonstrate basic skill structure. Not for complex greetings or personalized messages."
---

# Hello World Skill

This skill demonstrates the basic structure of a well-formed skill.

## What It Does

Greets users with a simple, friendly message.

## Usage

Say "Hello, World!" to the user.

## Message

Hello, World! Welcome to the thecattoolkit_v3.
```

---

## Breakdown and Explanation

### Frontmatter

```yaml
---
name: hello-world              # Max 64 chars, lowercase, hyphens only
description: "Greets users... Use when... Not for..."
---
```

**Key Points**:
- `name`: Uses kebab-case (lowercase with hyphens)
- `description`: Non-spoiling, includes "Use when" and "Not for"
- No `context: fork` (uses default shared context)
- No `agent` (not needed without context: fork)

### Frontmatter Fields Explained

| Field | Value | Why |
|:------|:------|:-----|
| `name` | `hello-world` | Lowercase, hyphens, descriptive |
| `description` | "Greets users... Use when... Not for..." | Non-spoiling, clear triggers and exclusions |

### Body Structure

```markdown
# Hello World Skill      <- Clear title

This skill demonstrates...  <- Brief purpose statement

## What It Does          <- What section
Greets users...

## Usage                 <- How section
Say "Hello..."

## Message               <- Content
Hello, World!
```

**Key Points**:
- Clear headings for organization
- Brief purpose statement
- Separation of "what" and "how"
- Actual content/message at the end

---

## Quality Checklist Applied

### Frontmatter

- [x] `name` present: `hello-world`
- [x] `description` present: Non-spoiling
- [x] `description` has "Use when": "Use when you want to say hello..."
- [x] `description` has "Not for": "Not for complex greetings..."

### Naming

- [x] Gerund form: `hello-world` (noun phrase acceptable for simple names)
- [x] Lowercase only: Yes
- [x] Hyphens as separators: Yes
- [x] Not reserved words: Yes
- [x] Not vague: `hello-world` is specific

### Description Quality

- [x] Third person: "Greets users" not "I will greet"
- [x] Non-spoiling: Doesn't reveal the exact message
- [x] Trigger conditions: "Use when you want to say hello..."
- [x] Exclusions clear: "Not for complex greetings..."

### Progressive Disclosure

- [x] Core in SKILL.md: All content in main file
- [x] No references/ folder: Not needed for simple skill
- [x] No scripts/: Not needed

---

## How to Invoke

### User Invocation

```bash
# From command palette
/hello-world

# Or from chat
Use the hello-world skill
```

### Agent Invocation

```markdown
# In another skill or command
Skill(hello-world)
```

---

## What Happens When Invoked

1. **Metadata loaded**: `name` and `description` already in system prompt
2. **SKILL.md read**: Body content loaded into context
3. **Skill executes**: Agent reads and follows instructions
4. **Result**: "Hello, World!" message displayed

---

## Common Variations

### With argument-hint

```yaml
---
name: greet
description: "Greets users with a custom message. Use when you want to say hello with a name. Not for complex greetings."
argument-hint: "<name>"
---
```

### With user-invocable: false

```yaml
---
name: internal-helper
description: "Internal helper skill. Use when performing internal operations. Not for user-facing tasks."
user-invocable: false
---
```

**Result**: Skill is hidden from `/` menu, but Claude can still invoke via `Skill(internal-helper)`.

### With disable-model-invocation

```yaml
---
name: dangerous-operation
description: "Performs a dangerous operation. Use when user explicitly requests this operation. Not for automated tasks."
disable-model-invocation: true
---
```

**Result**: Skill won't auto-invoke; requires explicit user intent.

---

## Next Steps

After understanding this basic skill:

1. Study `worker-skill.md` for isolated context
2. Review `loadout-agent.md` for multi-skill bundling
3. See `quality-gate.md` for validation patterns

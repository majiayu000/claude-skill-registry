---
name: skill-creator
description: Create new Claude Skills for Miyabi project. Use when building custom skills, packaging workflows, or extending Claude's capabilities. Triggers on "create skill", "make skill", "new skill", "スキル作成", "スキルを作る".
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Skill Creator

**Version**: 1.0.0
**Purpose**: Create properly structured Claude Skills

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Create | "create a skill", "スキル作成", "make new skill" |
| Package | "package this workflow", "ワークフロー化" |
| Automate | "automate this process", "自動化" |

---

## Skill Structure

```
.claude/skills/[skill-name]/
├── SKILL.md              # Required: Main instructions
├── resources/            # Optional: Reference docs
│   └── examples.md
└── scripts/              # Optional: Helper scripts
    └── helper.sh
```

---

## Creation Process

### Step 1: Gather Requirements

Ask:
1. **Purpose**: What does this skill do?
2. **Triggers**: When should it activate?
3. **Input**: What information is needed?
4. **Output**: What should be produced?
5. **Tools**: Which tools are needed?

### Step 2: Create Directory

```bash
mkdir -p .claude/skills/[skill-name]
```

### Step 3: Write SKILL.md

```markdown
---
name: [skill-name]
description: [What it does]. Use when [trigger conditions].
allowed-tools: Bash, Read, Write
---

# [Skill Title]

**Version**: 1.0.0
**Purpose**: [Brief purpose]

---

## Triggers

| Trigger | Examples |
|---------|----------|
| [Category] | "[example1]", "[example2]" |

---

## Workflow

### Step 1: [Title]

[Instructions]

---

## Checklist

- [ ] [Item 1]
- [ ] [Item 2]
```

---

## Naming Rules

### Required

| Rule | Example |
|------|---------|
| Kebab-case | `my-skill` |
| Lowercase | `code-reviewer` |
| Descriptive | `test-generator` |

### Forbidden

| Word | Reason |
|------|--------|
| `claude` | Trademark |
| `anthropic` | Company name |
| `mcp` | Protocol name |

```
✅ GOOD: code-connector, task-runner
❌ BAD: claude-helper, mcp-server
```

---

## Description Format

```
[What it does]. Use when [conditions].
```

Examples:
```
✅ GOOD: "Review code for bugs and security issues.
         Use when checking PRs or analyzing code quality."

❌ BAD: "A skill for code"
❌ BAD: "Helps with stuff"
```

---

## Template

```markdown
---
name: [kebab-case-name]
description: [Action verb] [object]. Use when [trigger condition 1], [trigger condition 2].
allowed-tools: Bash, Read, Write, Grep, Glob
---

# [Title with Emoji]

**Version**: 1.0.0
**Purpose**: [One-line purpose]

---

## Triggers

| Trigger | Examples |
|---------|----------|
| [Category 1] | "[EN example]", "[JP example]" |
| [Category 2] | "[EN example]", "[JP example]" |

---

## [Main Section]

### Step 1: [Title]

\`\`\`bash
# Command example
\`\`\`

### Step 2: [Title]

[Instructions]

---

## Best Practices

\`\`\`
✅ GOOD: [Recommended pattern]
❌ BAD: [Anti-pattern]
\`\`\`

---

## Checklist

- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]
```

---

## Validation

```bash
# Check frontmatter
head -n 5 .claude/skills/[name]/SKILL.md

# Test trigger
# Ask Claude: "[trigger phrase]"
# Expected: Skill activates
```

---

## Checklist

- [ ] Directory created at `.claude/skills/[name]/`
- [ ] SKILL.md has valid frontmatter
- [ ] Name is kebab-case, no forbidden words
- [ ] Description has action + trigger
- [ ] Triggers cover EN and JP
- [ ] Steps are clear and actionable

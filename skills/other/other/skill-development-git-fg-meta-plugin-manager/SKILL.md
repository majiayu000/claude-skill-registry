---
name: skill-development
description: "Create portable skills with SKILL.md. Use when building new skills or documenting patterns. Includes frontmatter syntax, quality standards, and primitives. Not for commands or agents."
---

# Skill Development

## Core Principle

**Put everything useful in SKILL.md.** AI agents are smart (can infer from examples) and lazy (won't hunt for scattered references).

## Frontmatter

```yaml
---
name: skill-name
description: "What it does. Use when {trigger + keywords}. Not for {exclusions}."
---
```

**Description format:** What it does, when to use it (with trigger phrases), what it's NOT for.

**Optional fields:** `context: fork`, `agent:`, `skills:`, `disable-model-invocation`, `user-invocable`

## Primitives

| Primitive | Context | Use When |
| --------- | ------- | -------- |
| `Task()` | Forked | Heavy multi-step work |
| `Skill()` | Shared | Adding expertise |
| `Skill(fork)` | Isolated | Biased-free execution |

**Key constraint:** `Task→Task` is forbidden. `Skill(fork)→Skill(fork)` is allowed.

## Directory Structure

```
.claude/skills/skill-name/
└── SKILL.md
```

Folder and file names use kebab-case. References folder is RARE—needs strong justification.

## Quality Checklist

| Check | Requirement |
| ----- | ------------ |
| Frontmatter | name + description (What-When-Not format) |
| Quick Start | Scenario-based entry point |
| Navigation | "If you need X → Read Y" table |
| Core knowledge | In SKILL.md, not in references/ |
| Footer | critical_constraint for non-negotiable rules |

## Anti-Patterns to Avoid

- ❌ Hiding patterns in references/ when they could be in SKILL.md
- ❌ Vague names (`helper`, `utils`)
- ❌ Spoiling content in navigation
- ❌ Nested folder structures
- ❌ Task→Task (forbidden)

---

<critical_constraint>
**Portability Invariant:** Every skill MUST work in isolation (zero external dependencies).

1. All content in SKILL.md or its own references/
2. No references to global rules or other components
3. If references/ is used, MARK MANDATORY with critical_constraint

**Gold Standards:**
- Frontmatter first
- Description enables auto-discovery
- Navigation uses "If you need... Read this section..."
- critical_constraint footer present
</critical_constraint>

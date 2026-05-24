---
name: tzurot-skills-guide
description: Meta-skill for writing and maintaining Claude Code skills. Use when creating new skills, updating existing skills, or reviewing skill quality. Enforces progressive disclosure and size limits.
lastUpdated: '2026-01-21'
---

# Writing Claude Code Skills - Best Practices

**Use this skill when:** Creating a new skill, updating an existing skill, or reviewing skill quality.

## Core Principle: Progressive Disclosure

> "Don't tell Claude all the information you could possibly want it to know. Rather, tell it **how to find** important information so that it can use it only when needed."
> — Anthropic Engineering

**Skills should be concise entry points, not exhaustive documentation.**

## Size Limits

| Metric           | Target | Maximum | Action if Exceeded      |
| ---------------- | ------ | ------- | ----------------------- |
| Skill lines      | <300   | 400     | Split or reference docs |
| CLAUDE.md        | <400   | 500     | Move content to skills  |
| Description char | N/A    | 15,000  | Trim descriptions       |

**Note**: Skill count doesn't matter if total descriptions stay under budget. The "15 skill limit" is a heuristic, not a hard constraint - the real limit is description character budget.

**Monitor sizes:**

```bash
# Check skill file sizes
wc -l .claude/skills/*/SKILL.md | sort -n

# Check description budget usage (should be <15000)
for f in .claude/skills/*/SKILL.md; do
  grep -A1 "^description:" "$f" | tail -1
done | wc -c
```

## Skill Structure Template

```markdown
---
name: tzurot-skillname
description: Action-oriented description. Use when [specific triggers]. Covers [key topics].
lastUpdated: 'YYYY-MM-DD'
---

# Skill Title

**Use this skill when:** [2-3 specific trigger scenarios]

## Quick Reference (Essential)

[10-20 lines of the most critical patterns]

## Core Patterns (Must Know)

[50-100 lines of essential patterns with examples]

## Additional Patterns

**See:** `docs/path/to/detailed-docs.md`
[Brief summaries with links, not full content]

## Related Skills

- **skill-name** - When to use instead

## References

- Full documentation: `docs/path/to/doc.md`
- Project guidelines: `CLAUDE.md#section`
```

## What Belongs in Skills vs Docs

| Content Type         | Location                       | Example                                 |
| -------------------- | ------------------------------ | --------------------------------------- |
| Quick patterns       | Skill                          | "Use fake timers: `vi.useFakeTimers()`" |
| Essential examples   | Skill                          | 5-10 line code snippet                  |
| Comprehensive guides | `docs/`                        | Full testing guide with all edge cases  |
| Reference tables     | `docs/`                        | Complete API reference                  |
| Decision rationale   | Skill (brief) + `docs/` (full) | Why we use rebase-only                  |

## Writing Good Descriptions

The `description` field in YAML frontmatter determines when Claude auto-activates the skill.

**Action-oriented triggers work best:**

```yaml
# ❌ BAD - Passive, vague
description: Testing patterns for the project.

# ✅ GOOD - Action triggers
description: Use when writing tests, debugging test failures, or mocking dependencies. Covers Vitest patterns, fake timers, and mock factories.
```

```yaml
# ❌ BAD - Too broad
description: Database and vector operations.

# ✅ GOOD - Specific triggers
description: Use when writing Prisma queries, running migrations, or working with pgvector similarity search. Covers connection pooling and migration workflow.
```

## When to Create a New Skill

**Create a new skill when:**

- Pattern applies to multiple features/areas
- Topic is distinct from existing skills
- Content would bloat an existing skill beyond limits
- Users frequently need this specific guidance

**Don't create a new skill when:**

- Content fits in existing skill (<50 lines to add)
- Topic is one-off or temporary
- Better suited for `docs/` as reference material
- Would duplicate existing skill content

## When to Merge Skills

**Merge skills when:**

- Significant content overlap (>30%)
- Topics are closely related (e.g., constants + types)
- Combined size stays under 400 lines
- Mental model is clearer as one concept

**Process:**

1. Create merged skill with combined essential content
2. Move non-essential content to `docs/`
3. Delete old skill directories
4. Update README.md skill index
5. Update any CLAUDE.md references

## Skill Maintenance

**Regular audits (monthly or after major features):**

1. Check skill sizes: `wc -l .claude/skills/**/SKILL.md`
2. Remove outdated patterns
3. Update `lastUpdated` timestamps
4. Verify cross-references still valid

**After production incidents:**

1. Add lessons learned to relevant skill
2. Keep addition brief (reference post-mortem for details)
3. Update `lastUpdated`

## Anti-Patterns to Avoid

### 1. Documentation Dumping

```markdown
# ❌ BAD - Entire guide in skill

## Complete API Reference

[500 lines of every possible option]

# ✅ GOOD - Essential + reference

## Key Options

- `ttl`: Cache lifetime in ms
- `maxSize`: Maximum entries

**Full options:** See `docs/reference/cache-api.md`
```

### 2. Duplicate Content

```markdown
# ❌ BAD - Same content in skill and CLAUDE.md

[Pattern explained in both places]

# ✅ GOOD - Single source of truth

**See:** `CLAUDE.md#testing` or reference from CLAUDE.md to skill
```

### 3. Over-Detailed Examples

```markdown
# ❌ BAD - 50-line example for simple concept

[Full service with all edge cases]

# ✅ GOOD - Minimal viable example

const cache = new TTLCache({ ttl: 60000, maxSize: 100 });
cache.set('key', value);
const result = cache.get('key');
```

### 4. Missing Cross-References

```markdown
# ❌ BAD - Standalone content

[No links to related skills or docs]

# ✅ GOOD - Connected knowledge

## Related Skills

- **tzurot-architecture** - Service boundaries
- **tzurot-async-flow** - Timer alternatives
```

## Skill Quality Checklist

Before committing a new or updated skill:

- [ ] Under 400 lines
- [ ] Has "Use this skill when:" section
- [ ] Action-oriented description in frontmatter
- [ ] Essential patterns only (detailed content in docs/)
- [ ] Includes Related Skills section
- [ ] Includes References section
- [ ] `lastUpdated` timestamp current
- [ ] No duplicate content with other skills
- [ ] Examples are minimal but complete

## Related Skills

- **tzurot-docs** - Documentation organization and maintenance
- **tzurot-git-workflow** - Committing skill changes

## References

- Anthropic best practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Skills documentation: https://docs.claude.com/en/docs/claude-code/skills
- Project structure: `.claude/skills/README.md`

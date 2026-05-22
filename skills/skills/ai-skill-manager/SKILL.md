---
name: ai-skill-manager
description: Manage AI agent skills throughout their lifecycle - creating, structuring, optimizing, maintaining, versioning, and deprecating skills. Use when creating new skills, updating existing skills, optimizing token usage, managing skill quality, testing skill discovery, or following skill best practices.
version: "1.0.0"
last_updated: "2026-01-12"
---

# AI Skill Manager

Comprehensive guide for managing Claude Code skills throughout their complete lifecycle, from planning and creation to maintenance and deprecation.

## When to Use This Skill

- **Creating new skills** - Plan structure, write descriptions, test discovery
- **Updating existing skills** - Detect outdated content, apply 2026 best practices
- **Optimizing token usage** - Implement progressive disclosure, measure efficiency
- **Managing quality** - Audit skills, enforce standards, track metrics
- **Testing discovery** - Verify trigger phrases, optimize keywords
- **Deprecating skills** - Plan transitions, archive safely, maintain backwards compatibility

## Quick Reference

###  Creating a New Skill

```bash
# 1. Create structure
mkdir -p .claude/skills/my-skill/scripts

# 2. Write SKILL.md with frontmatter
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: [Action verbs] + [what it does] + [when to use] + [trigger keywords]
---

# My Skill

## When to Use
- Use case 1
- Use case 2

## Quick Reference
[Complete minimal example]

## Core Patterns
[Main implementation]
EOF

# 3. Test discovery
# Ask Claude: "What Skills are available?"
# Test trigger: Use keywords from description
```

### Auditing an Existing Skill

```bash
# Run skill audit script
python .claude/skills/ai-skill-manager/scripts/skill-audit.py .claude/skills/my-skill/

# Check output for:
# - Line count (should be < 500)
# - Token usage (should be < 5k)
# - Description quality
# - Missing sections
```

### Optimizing Token Usage

```bash
# Count tokens
python .claude/skills/ai-skill-manager/scripts/token-counter.py .claude/skills/my-skill/SKILL.md

# If > 500 lines, split into:
# - SKILL.md (overview + quick ref)
# - REFERENCE.md (detailed API docs)
# - EXAMPLES.md (comprehensive examples)
# - TROUBLESHOOTING.md (common issues)
```

## Core Workflow

### 1. Planning Phase

**Before writing any content:**

| Decision | Considerations |
|----------|----------------|
| **Scope** | Single responsibility - one domain per skill |
| **Size target** | < 500 lines for SKILL.md (use progressive disclosure if larger) |
| **Naming** | Lowercase, hyphens, descriptive (e.g., `database-migration-manager`) |
| **Description** | Must include action verbs + when to use + trigger keywords |

**Naming Patterns:**
- ✅ `database-migration-manager`, `flutter-query-testing`, `web-performance-metrics`
- ❌ `db-stuff`, `helpers`, `utils`, `tools`

### 2. Writing Effective Descriptions

**Description Formula:**
```
[Action verbs] + [what it does] + [when to use] + [trigger keywords users would say]
```

**Examples:**

✅ **GOOD**:
```yaml
description: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
```

❌ **BAD**:
```yaml
description: "Helps with documents"  # Too vague, no triggers
```

**Trigger Keyword Strategy:**
- Action verbs: create, analyze, optimize, validate, generate, test
- Domain nouns: database, migration, query, performance, RLS
- File extensions: .ts, .tsx, .sql, .md, .dart
- Error patterns: "RLS error", "query failure", "N+1 query"

### 3. Content Structure (SKILL.md)

```markdown
---
name: skill-name
description: [Formula above]
version: "1.0.0"
last_updated: "YYYY-MM-DD"
---

# Skill Name

Brief overview (1-2 sentences)

## When to Use This Skill

- **Use case 1** - Description
- **Use case 2** - Description

## Quick Reference

```bash
# Essential commands with complete working examples
./command.sh
```

## Core Workflow

### Step 1: [Action]
Detailed instructions

### Step 2: [Action]
More instructions

## Common Patterns

### Pattern 1: [Name]
[Code example]

### Pattern 2: [Name]
[Code example]

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|

## Related Resources

- For complete API details, see [REFERENCE.md](REFERENCE.md)
- For examples, see [EXAMPLES.md](EXAMPLES.md)
- Related skill: [`other-skill`](../other-skill/SKILL.md)
```

### 4. Progressive Disclosure (for skills > 500 lines)

**File Structure:**
```
my-skill/
├── SKILL.md              # Overview + navigation (< 500 lines)
├── REFERENCE.md          # Detailed API docs (loaded when needed)
├── EXAMPLES.md           # Comprehensive examples (loaded when needed)
├── TROUBLESHOOTING.md    # Common issues (loaded when needed)
└── scripts/              # Utilities (execute, not loaded)
    └── helper.py
```

**In SKILL.md, reference supporting files:**
```markdown
## Core Patterns

[Essential patterns here - most common 80% use cases]

## Additional Resources

For complete API reference, see [REFERENCE.md](REFERENCE.md)
For detailed examples, see [EXAMPLES.md](EXAMPLES.md)
For troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
```

**Token Savings**: 95-98% reduction by loading docs only when needed

### 5. Testing Discovery

**Verification Steps:**

1. **Check availability**:
   ```
   Ask Claude: "What Skills are available?"
   ```

2. **Test trigger phrases**:
   ```
   Use keywords from description naturally in a request
   Example: "Create a migration for adding email column"
   Should trigger: database-migration-manager
   ```

3. **Verify invocation**:
   - Claude should show skill confirmation
   - Instructions should load correctly
   - Examples should work as shown

4. **Test script execution**:
   ```bash
   ./scripts/test-discovery.sh my-skill
   ```

### 6. Quality Audit Checklist

Run before committing any skill:

- [ ] **Description** includes specific trigger keywords
- [ ] **SKILL.md** under 500 lines (or uses progressive disclosure)
- [ ] **Code examples** are tested and working
- [ ] **Quick reference** shows complete minimal example
- [ ] **Troubleshooting** section included
- [ ] **Related skills/files** documented
- [ ] **YAML frontmatter** is valid
- [ ] **Scripts** have execute permissions (`chmod +x`)
- [ ] **Token usage** < 5k tokens for full load
- [ ] **Discovery** tested with trigger phrases

## Advanced Patterns

### Skills with Utility Scripts

**Zero-context execution** - scripts run without loading contents:

```markdown
## Validation

To validate your migration:
```bash
python scripts/validate-migration.py path/to/migration.sql
```

The script checks:
- Idempotency (IF NOT EXISTS/IF EXISTS)
- Naming conventions
- RLS policy patterns
```

**Script Best Practices:**
- Return structured JSON output
- Handle errors gracefully
- Provide actionable error messages
- Exit with proper status codes (0 = success, 1 = error)

### Skills with Tool Restrictions

```yaml
---
name: secure-operations
description: [...]
allowed-tools: Read, Bash(python:*), Grep  # Restrict to safe operations
---
```

### Skills with Model Overrides

```yaml
---
name: simple-formatting
description: [...]
model: claude-haiku-3-5-20250110  # Fast, cheap model for simple tasks
---
```

### Skills with Hooks

```yaml
---
name: safe-migrations
description: [...]
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "./scripts/validate-before-write.sh"
          once: true
---
```

## Maintenance Workflow

### When to Update Skills

**Indicators:**
- Framework version upgrades (Next.js, Flutter, Riverpod, etc.)
- API changes or deprecations
- New best practices emerge
- Users report skill isn't working
- Token usage too high (> 5k tokens)
- Performance issues identified

**Update Triggers:**

| Trigger | Action Required |
|---------|----------------|
| Framework major version | Update code examples, patterns |
| API deprecation | Replace with new APIs, add warnings |
| New best practices | Add patterns, update recommendations |
| Skill not working | Debug, fix, test thoroughly |
| Token usage high | Split with progressive disclosure |

### Version Control

Use semantic versioning:

```yaml
---
name: my-skill
version: "1.2.0"  # MAJOR.MINOR.PATCH
last_updated: "2026-01-12"
---
```

- **MAJOR**: Breaking changes to skill interface
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, documentation updates

**Maintain CHANGELOG.md:**
```markdown
# Changelog

## [1.2.0] - 2026-01-12
### Added
- New pattern for X
- Support for Y

### Changed
- Improved Z

### Fixed
- Bug in W
```

### Deprecation Process

1. **Mark as deprecated**:
```yaml
description: "[DEPRECATED] Use 'new-skill' instead. [Old description...]"
```

2. **Update content to redirect**:
```markdown
# DEPRECATED: Old Skill Name

This skill is deprecated. Please use `/new-skill` instead.

See [new-skill](../new-skill/SKILL.md) for the replacement.

## Migration Guide
[How to transition from old to new]
```

3. **Archive after transition** (e.g., 1 sprint):
```bash
mkdir -p .claude/skills/_archived
mv .claude/skills/old-skill .claude/skills/_archived/
```

## Optimization Strategies

### Token Efficiency Techniques

1. **Progressive Disclosure** (95-98% token reduction)
   - SKILL.md: Overview + quick ref
   - Supporting files: Loaded only when needed

2. **Use Tables Over Prose**
   ```markdown
   # ❌ Verbose
   When you need auth, use withAuth. For user context, use withAuthParams.

   # ✅ Scannable
   | Wrapper | Use When |
   |---------|----------|
   | withAuth | Need authentication |
   | withAuthParams | Need user context |
   ```

3. **Script-Based Execution** (zero-context)
   - Only script output consumes tokens
   - Script contents don't load into context

4. **Template Reuse**
   ```markdown
   Use templates in `resources/templates/`:
   - `migration-template.sql` - Copy and modify
   ```

### Content Strategy

**Few-Shot Learning:**
```markdown
## Examples

### Example 1: Common Use Case
**Input**: [User request]
**Expected**: [Desired output]
**Code**:
```code
[Complete example]
```

### Example 2: Edge Case
[Same structure]
```

**Anti-Pattern Documentation:**
```markdown
## Common Mistakes

### ❌ Don't Do This
[Bad example with explanation]

### ✅ Do This Instead
[Good example with explanation]
```

## Quality Metrics

### Measuring Skill Effectiveness

**Key Metrics:**
- **Discovery rate**: How often Claude finds skill when appropriate (target: > 90%)
- **Success rate**: How often skill instructions work correctly (target: > 95%)
- **Token efficiency**: Cost per successful use (target: < 5k tokens)
- **User satisfaction**: Team feedback (track informally)

**Monitoring:**
```bash
# Count skill invocations
grep "skill-name" ~/.claude/projects/*/transcript.jsonl | wc -l

# Check token usage
python scripts/token-counter.py .claude/skills/skill-name/SKILL.md
```

## Troubleshooting

| Issue | Debug Step | Solution |
|-------|------------|----------|
| Skill not loading | Check file path | Must be `SKILL.md` (case-sensitive) |
| YAML parse error | Validate frontmatter | No tabs, valid YAML syntax |
| Skill not triggering | Test description | Add specific trigger keywords |
| Scripts failing | Check permissions | `chmod +x scripts/*.sh` |
| Token limit exceeded | Measure size | Split with progressive disclosure |
| Discovery issues | Test phrases | Use `scripts/test-discovery.sh` |

## Related Resources

### Detailed Guides (Progressive Disclosure)

For comprehensive workflows and examples, see:

- **[CREATION_GUIDE.md](CREATION_GUIDE.md)** - Detailed skill creation workflow with examples
- **[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)** - Version control, updates, deprecation
- **[OPTIMIZATION_GUIDE.md](OPTIMIZATION_GUIDE.md)** - Token efficiency, performance tuning
- **[BEST_PRACTICES.md](BEST_PRACTICES.md)** - Industry standards, Claude Code patterns, examples library

### Utility Scripts

Run from project root:

```bash
# Audit existing skill
python .claude/skills/ai-skill-manager/scripts/skill-audit.py .claude/skills/my-skill/

# Count tokens
python .claude/skills/ai-skill-manager/scripts/token-counter.py .claude/skills/my-skill/SKILL.md

# Test discovery
./.claude/skills/ai-skill-manager/scripts/test-discovery.sh my-skill
```

### Official Documentation

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)

### Related Skills

- `user-stories-manager` - Track feature development
- `wip-lifecycle-manager` - Manage work-in-progress documentation
- `code-quality-tools` - Automated quality fixes

## Success Criteria

A well-crafted skill should:

✅ Be discovered automatically when relevant (> 90% discovery rate)
✅ Provide working examples that execute successfully
✅ Stay under 500 lines or use progressive disclosure
✅ Consume < 5k tokens when fully loaded
✅ Include troubleshooting for common issues
✅ Reference related skills and documentation
✅ Be versioned and maintained over time
✅ Follow 2026 industry best practices

---

**Last Updated**: 2026-01-12
**Version**: 1.0.0
**Maintainer**: Ballee Engineering Team

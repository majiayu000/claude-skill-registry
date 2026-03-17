---
name: worktree-guide
description: Git worktree patterns, best practices, templates, and quick reference. Use when user asks about "worktree best practices", "worktree patterns", "git worktree help", "worktree template", "worktree mode semantics", "what are worktree modes", "explain worktree metadata", or needs guidance on worktree organization and workflows.
---

# Git Worktree Guide

Quick reference and templates for git worktree workflows with AI metadata integration.

## Progressive Disclosure

### Initial Response

**Quick Overview:**

Git worktrees let you checkout multiple branches simultaneously in separate directories. Each worktree has AI metadata (`.ai-context.json`) that helps tools understand context.

**Quick Start:**
- Create worktree: `/working-tree:new <branch-name>`
- List worktrees: `/working-tree:list`
- Check status: `/working-tree:status`
- Remove worktree: `/working-tree:destroy <path>`
- Add metadata: `/working-tree:adopt`

**What would you like to know more about?**
1. Mode semantics (main, feature, bugfix, experiment, review)
2. Metadata file structure and templates
3. Comprehensive best practices guide
4. Strategic organization patterns

### On Request

Based on what you ask for, I can show you:

**Mode Semantics** → Detailed explanation of each mode
**Templates** → Ready-to-use metadata templates
**Best Practices** → Full reference guide (REFERENCE.md)
**Examples** → Specific workflow examples

## Mode Semantics Quick Reference

### main
**Purpose:** Stable, production-ready code
**Restrictions:** Minimal changes only, no experimentation
**Use For:** Hotfixes, urgent production changes, stable baseline
**AI Behavior:** Conservative suggestions, focus on safety

### feature
**Purpose:** Active development of new features
**Restrictions:** None, experimentation encouraged
**Use For:** New features, enhancements, active work
**AI Behavior:** Helpful, suggests improvements freely

### bugfix
**Purpose:** Isolated, surgical bug fixes
**Restrictions:** Minimal scope, no unrelated changes
**Use For:** Specific bug fixes, targeted corrections
**AI Behavior:** Focused on fix only, warns about scope creep

### experiment
**Purpose:** Prototypes, spikes, research
**Restrictions:** None, can be messy, expect to discard
**Use For:** POCs, trying new technologies, A/B testing
**AI Behavior:** Aggressive suggestions, OK with rough code

### review
**Purpose:** Code review, auditing, documentation
**Restrictions:** Read-only mindset, analysis only
**Use For:** PR review, security audits, documentation work
**AI Behavior:** Analytical, suggests improvements, no execution

## Metadata File Structure

### .ai-context.json

```json
{
  "worktree": "directory-name",
  "branch": "branch-name",
  "mode": "main|feature|bugfix|experiment|review",
  "created": "2025-11-23T12:34:56Z",
  "description": "Purpose of this worktree"
}
```

**Fields:**
- `worktree`: Directory name (not full path)
- `branch`: Git branch name
- `mode`: One of the 5 modes above
- `created`: ISO 8601 UTC timestamp
- `description`: Freeform text explaining purpose

### README.working-tree.md

Generated automatically with worktree details, mode semantics, and paths.

## Templates

### Available Templates

Located in `templates/` directory:
1. `ai-context.json.template` - Metadata file template with examples
2. `README.working-tree.template` - README template with placeholders

To view templates:
- Ask "show me the metadata template"
- Ask "show me the README template"

## Common Patterns

### Pattern 1: Feature Development
```bash
/working-tree:new feature/user-auth --mode feature --description "Implement OAuth2"
```
Work in isolation, merge when ready.

### Pattern 2: Production Hotfix
```bash
/working-tree:new bugfix/critical-security-fix --mode bugfix
```
Quick surgical fix, minimizes risk.

### Pattern 3: Experimentation
```bash
/working-tree:new exp/try-new-framework --mode experiment
```
Prototype freely, discard if needed.

### Pattern 4: Code Review
```bash
/working-tree:new review/pr-123 --mode review --description "Review user auth PR"
```
Review without disrupting current work.

### Pattern 5: Internationalization
```bash
/working-tree:new i18n/zh-CN --description "Chinese Simplified translations"
/working-tree:new i18n/42-ja-JP --description "Japanese translations for issue #42"
```
Isolated i18n work for specific locale.

## Supporting Files

- **references/best-practices.md**: Comprehensive guide with detailed best practices, naming conventions, workflows, and advanced patterns
- **templates/ai-context.json.template**: Copy-paste template for manual metadata creation
- **templates/README.working-tree.template**: Template for worktree README

## Quick Tips

**DO:**
- Use descriptive branch names: `feature/user-dashboard`
- Add descriptions to worktrees: `--description "User settings page"`
- Run `/working-tree:list` regularly to see active work
- Choose appropriate mode for context

**DON'T:**
- Create worktree for same branch twice
- Use generic names: `test`, `temp`, `new`
- Use branch names that match existing project folders (e.g., `workflows`, `src`, `backend`)
- Forget to clean up: `/working-tree:destroy` when done
- Ignore uncommitted changes before destroying

## For More Detail

**Comprehensive Guide:**
Ask to see `references/best-practices.md` for:
- Detailed mode usage guidelines
- Naming conventions and patterns
- Multi-worktree organization strategies
- Troubleshooting common issues
- Team collaboration workflows
- CI/CD integration patterns

**Strategic Consulting:**
For complex worktree organization questions, invoke the `working-tree-consultant` agent:
- "Help me organize my worktrees"
- "Review my worktree strategy"
- "Migrate to worktree workflow"

## Examples

### Example 1: Quick Mode Check
```
User: What mode should I use for a prototype?

Skill: For prototypes, use **experiment** mode.

Experiment mode:
- No restrictions, can be messy
- AI will be aggressive with suggestions
- Expect to discard if prototype fails
- Good for POCs and spikes

Command:
/working-tree:new exp/prototype-name --mode experiment --description "Testing new approach"
```

### Example 2: Template Request
```
User: Show me the metadata template

Skill: Here's the .ai-context.json template:

[Shows content of templates/ai-context.json.template]

You can create this manually or use:
- /working-tree:new to auto-generate when creating
- /working-tree:adopt to auto-generate for existing worktree
```

### Example 3: Best Practices Request
```
User: What are worktree best practices?

Skill: **Quick Best Practices:**

1. **Naming**: Use clear, structured names (myapp-feature-user-auth)
2. **Modes**: Choose mode based on work type (see mode semantics above)
3. **Cleanup**: Remove worktrees when done (/working-tree:destroy)
4. **Metadata**: Always add descriptions
5. **Organization**: One feature = one worktree

**Want more detail?**
- See REFERENCE.md for comprehensive guide
- Invoke working-tree-consultant for strategic advice
```

## Related

- Commands: `/working-tree:new`, `/working-tree:list`, `/working-tree:status`, `/working-tree:destroy`, `/working-tree:adopt`
- Agent: `working-tree-consultant` for strategic guidance
- Documentation: See REFERENCE.md for comprehensive coverage

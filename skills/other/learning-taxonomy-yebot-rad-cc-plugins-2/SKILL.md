---
name: learning-taxonomy
description: Expert knowledge for categorizing learnings and routing them to appropriate improvement targets. Use when analyzing session learnings to determine where context improvements should be applied.
---

# Learning Taxonomy

Expert reference for categorizing session learnings and routing them to appropriate targets for context improvement.

## Learning Categories

| Category | Description | Keywords | Priority | Typical Source |
|----------|-------------|----------|----------|----------------|
| **caveat** | Gotcha, workaround, required setup, edge case | must, required, careful, watch out, gotcha | High | Config issues, env setup, surprising behavior |
| **pattern** | Convention, best practice, coding style | always, never, prefer, convention, standard | Medium | Code reviews, refactoring, style decisions |
| **error_fix** | Solution to recurring error or bug | fix, error, resolved, workaround, hack | High | Debugging sessions, stack traces, test failures |
| **dependency** | Tool, library, version requirement | install, requires, upgrade, package, version | Medium | Package updates, compatibility issues |
| **command** | Useful shell command, script, or CLI invocation | run, npm, python, bash, script, command | Low | Build/test/deploy workflows |
| **architecture** | Design decision, structural pattern, component relationship | design, structure, pattern, component, layer | Medium | System design, refactoring, API design |

## Claude Code Memory Hierarchy

Claude Code uses a hierarchical memory system. Understanding this is **critical** for routing learnings correctly.

### Memory Locations (Highest to Lowest Priority)

| Memory Type | Location | Purpose | Shared With |
|-------------|----------|---------|-------------|
| **Enterprise policy** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Org-wide standards | All org users |
| **Project memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared project instructions | Team via git |
| **Project rules** | `./.claude/rules/*.md` | Modular topic-specific rules | Team via git |
| **User memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **User rules** | `~/.claude/rules/*.md` | Personal modular rules | Just you |
| **Project local** | `./CLAUDE.local.md` | Personal project-specific (gitignored) | Just you |

### Memory Scope Decision

| Is this learning... | Route to |
|---------------------|----------|
| Personal workflow/preference for ALL projects | `~/.claude/CLAUDE.md` |
| Personal preference for THIS project only | `./CLAUDE.local.md` |
| Team knowledge everyone should know | `./CLAUDE.md` |
| Topic-specific (testing, API, security) | `./.claude/rules/{topic}.md` |
| Path-specific (only certain file types) | `./.claude/rules/` with `paths:` frontmatter |
| Organization standard | Enterprise policy (escalate to IT) |

### Path-Specific Rules

For learnings that only apply to certain files:

```markdown
---
paths: src/api/**/*.ts
---

# API Rules
- Validate all inputs with zod
```

Glob patterns: `**/*.ts`, `src/**/*`, `*.md`, `{src,lib}/**/*.ts`

### Import Syntax

CLAUDE.md files can import other files:
```
See @README for project overview.
Individual preferences: @~/.claude/my-prefs.md
```

## Target Routing

### By Learning Scope

| Scope | Target | Section to Add |
|-------|--------|----------------|
| team + broad | `./CLAUDE.md` | Category-specific section |
| team + topic-specific | `./.claude/rules/{topic}.md` | Topic section |
| team + file-specific | `./.claude/rules/` with `paths:` | Topic section |
| personal + all projects | `~/.claude/CLAUDE.md` | `## My Preferences` |
| personal + this project | `./CLAUDE.local.md` | `## Local Setup` |

### By Category (Default: Project Memory)

| Category | Target Section | Create If Missing |
|----------|----------------|-------------------|
| caveat | `## Important Caveats` | Yes |
| pattern | `## Conventions & Patterns` | Yes |
| error_fix | `## Troubleshooting` | Yes |
| dependency | `## Dependencies` | Yes |
| command | `## Common Commands` | Yes |
| architecture | `## Architecture` | Yes |

### Secondary Targets

| Learning Context | Secondary Target | Condition |
|------------------|------------------|-----------|
| Specific to subdirectory | Subdirectory CLAUDE.md | Content mentions directory name |
| Agent behavior | Agent definition | Architecture or pattern learnings |
| Skill knowledge | Skill SKILL.md | Domain-specific expertise |
| README content | README.md | Setup, installation, usage |

## Suggestion Format Templates

### Caveat Entry
```markdown
### [Short Title]
- [Specific caveat or gotcha]
- [Workaround or required action if applicable]
```

### Pattern Entry
```markdown
### [Pattern Name]
- **When**: [When to use this pattern]
- **How**: [How to implement]
- **Example**: [Brief example if helpful]
```

### Error Fix Entry
```markdown
### [Error Name or Symptom]
**Symptoms:** [What the user sees]
**Cause:** [Root cause]
**Fix:**
```bash
[Commands to fix if applicable]
```
```

### Dependency Entry
```markdown
### [Package/Tool Name]
- **Version**: [Required version]
- **Purpose**: [Why it's needed]
- **Install**: `[install command]`
```

### Command Entry
```markdown
### [What the Command Does]
```bash
[command with arguments]
```
[Brief explanation if not obvious]
```

### Architecture Entry
```markdown
### [Component/Pattern Name]
- **Purpose**: [What it does]
- **Location**: [Where to find it]
- **Interactions**: [What it connects to]
```

## Priority Calculation

### High Priority
All of these must be true:
- Category is `caveat` or `error_fix`
- Confidence >= 0.8
- Target is primary (root CLAUDE.md)

### Medium Priority
Any of these:
- Confidence >= 0.6
- Target is primary
- Category is `dependency` or `architecture`

### Low Priority
Default when neither High nor Medium criteria met.

## Source Analysis

### Git Commits
- Prefix patterns boost confidence:
  - `fix:`, `bugfix:`, `hotfix:` → error_fix (0.85)
  - `feat:`, `feature:` → pattern (0.60)
  - `docs:`, `doc:` → pattern (0.70)
  - `chore:`, `deps:` → dependency (0.75)

### Git Diff Analysis
- Files modified 3+ times in session → potential caveat area
- TODO/FIXME comments added → high-confidence caveats
- New entries in package.json/requirements.txt → dependency

### User Input
- Direct input always gets confidence 0.9
- User explicitly categorizes → use their category

## Integration with Other Plugins

### backlog-md / simbl
If these plugins are present, also extract learnings from:
- Task notes (`--append-notes` content)
- Implementation plans
- Acceptance criteria comments

Check for these directories:
- `backlog/tasks/` (backlog-md)
- `.simbl/` (simbl)

### documentation-tools
After applying suggestions, consider running:
- `/link-docs-to-claude` - Update documentation links
- `/sync-agents-md` - Sync CLAUDE.md → AGENTS.md

## Best Practices

### When Extracting Learnings
1. Prefer specific over generic (not "be careful" but "restart server after config changes")
2. Include context (file paths, command examples)
3. Capture the "why" not just the "what"
4. Date-stamp session learnings for freshness tracking

### When Generating Suggestions
1. Match learning to most specific target available
2. Use existing section if present, create if not
3. Format consistently with existing content
4. Keep suggestions atomic (one learning per suggestion)

### When Reviewing Suggestions
1. Present highest priority first
2. Show diff preview with context
3. Allow modification before applying
4. Track applied vs discarded for learning

## Common Mistakes to Avoid

| Mistake | Better Approach |
|---------|-----------------|
| Too vague: "Watch out for auth" | Specific: "OAuth tokens expire after 1 hour; implement refresh logic" |
| Missing context: "Run this first" | With context: "Before running tests: `source .env.local`" |
| Duplicate suggestions | Check if learning already exists in target |
| Wrong target | Architecture patterns → CLAUDE.md, not random files |
| Over-suggesting | Only suggest if confidence >= 0.5 |
| Personal pref in project memory | Your shortcuts → `~/.claude/CLAUDE.md` or `./CLAUDE.local.md` |
| Team knowledge in local file | Team caveats → `./CLAUDE.md`, not `./CLAUDE.local.md` |
| Everything in root CLAUDE.md | Topic-specific → `./.claude/rules/{topic}.md` |
| Ignoring existing rules structure | Check for `./.claude/rules/` before suggesting new location |

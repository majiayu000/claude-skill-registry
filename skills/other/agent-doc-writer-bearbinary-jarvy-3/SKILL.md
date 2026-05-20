---
name: agent-doc-writer
description: "Analyze code changes and recommend appropriate documentation. Evaluates git diffs to determine if changes warrant README updates, inline doc additions, or dedicated documentation files. Triggers on: document changes, what should I document, doc writer, write docs for changes, documentation recommendation."
---

# Agent Doc Writer

Analyze recent code changes and recommend appropriate documentation. This skill examines git diffs, categorizes changes, and determines the right level of documentation needed - from a simple README bullet point to a full documentation file.

## When to Use

Invoke this skill when:
- You've completed a feature and need to document it
- Before creating a PR, to ensure documentation is included
- After merging changes, to catch up on documentation debt
- When asked "what should I document?"
- To audit recent commits for missing documentation

## Workflow

### Step 1: Analyze Changes

First, gather the changes to analyze. Run these commands to understand the scope:

```bash
# Check uncommitted changes
git status

# View staged changes
git diff --cached --stat

# View unstaged changes
git diff --stat

# View recent commits (last 5)
git log --oneline -5

# View changes from specific commit
git show <commit> --stat
```

### Step 2: Categorize Change Type

Classify each change into one of these categories:

| Category | Description | Examples |
|----------|-------------|----------|
| **New Feature** | Adds user-facing functionality | New CLI command, new tool support, new config option |
| **Enhancement** | Improves existing feature | Performance boost, better error messages, UX improvement |
| **Bug Fix** | Corrects incorrect behavior | Crash fix, logic error, edge case handling |
| **Refactor** | Internal restructuring | Code reorganization, pattern changes, no behavior change |
| **Infrastructure** | Build/CI/tooling changes | CI workflows, build scripts, dev tooling |
| **Breaking Change** | Incompatible API/behavior change | Removed feature, changed defaults, config format change |

### Step 3: Assess Documentation Scope

Use this decision matrix to determine documentation level:

```
                          User-Facing?
                         /            \
                       Yes             No
                      /                  \
              Breaking?              Large Refactor?
             /        \              /            \
           Yes        No           Yes            No
            |          |            |              |
    [MAJOR DOC]  [README +     [ARCHITECTURE    [COMMIT
                  INLINE]         DOC]           MSG ONLY]
```

**Documentation Levels:**

1. **Commit Message Only** - Internal refactors, small fixes, test additions
2. **Inline Code Comments** - Complex algorithms, non-obvious decisions
3. **README Update** - New features, changed behavior, new installation steps
4. **Dedicated Doc File** - Major features, architecture changes, migration guides
5. **Multiple Docs** - Breaking changes need README + migration guide + changelog

### Step 4: Generate Documentation Recommendation

Based on analysis, provide a structured recommendation:

```markdown
## Documentation Recommendation

### Changes Analyzed
- [List of files/commits analyzed]

### Change Category
[Category from Step 2]

### Recommended Documentation

**Level:** [Commit Only | Inline | README | Dedicated | Multiple]

**Action Items:**
1. [ ] [Specific documentation task]
2. [ ] [Another task if needed]

**Suggested Content:**
[Draft text or outline for the documentation]

**Location:**
- File: [path/to/doc/file]
- Section: [specific section to update]
```

## Documentation Templates

### README Feature Addition

For new features, add to the appropriate README section:

```markdown
### [Feature Name]

[One-sentence description of what it does]

**Usage:**
```bash
jarvy [command] [options]
```

**Example:**
```bash
# Example showing the feature in action
jarvy setup --feature-flag
```
```

### README Configuration Update

For new config options:

```markdown
### [Option Name]

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `option` | string | `"default"` | What this option controls |

**Example:**
```toml
[section]
option = "value"
```
```

### Inline Documentation

For code comments explaining complex logic:

```rust
/// Brief description of what this does
///
/// # Arguments
/// * `param` - What this parameter is for
///
/// # Returns
/// What gets returned and when
///
/// # Example
/// ```
/// let result = function(input);
/// ```
fn function(param: Type) -> ReturnType {
    // Implementation note: explain WHY, not WHAT
}
```

### Dedicated Documentation File

For major features, create `docs/[feature-name].md`:

```markdown
# [Feature Name]

## Overview

[2-3 sentences explaining the feature and its purpose]

## Prerequisites

- [Required setup or dependencies]

## Usage

### Basic Usage

[Simple example with explanation]

### Advanced Usage

[More complex scenarios]

## Configuration

[Config options specific to this feature]

## Troubleshooting

### [Common Issue]

**Symptom:** [What the user sees]
**Cause:** [Why it happens]
**Solution:** [How to fix it]

## See Also

- [Related documentation links]
```

## Change Type to Documentation Mapping

| Change Type | Documentation Location | Template |
|-------------|----------------------|----------|
| New CLI command | README + `--help` text | README Feature Addition |
| New tool support | README tools list + tool's inline docs | README Feature Addition |
| New config option | README config section | README Configuration Update |
| Performance improvement | README or changelog | Brief mention |
| Bug fix | Changelog only (if exists) | None needed |
| Internal refactor | Code comments if complex | Inline Documentation |
| Breaking change | README + MIGRATION.md | Multiple templates |
| New architecture | docs/architecture.md | Dedicated Documentation |

## Example Analysis

**Scenario:** Added support for `fnm` as a Node.js version manager

**Analysis:**
```markdown
## Documentation Recommendation

### Changes Analyzed
- src/tools/fnm/fnm.rs (new file)
- src/tools/fnm/mod.rs (new file)
- src/tools/mod.rs (register fnm)

### Change Category
New Feature - Adds user-facing functionality

### Recommended Documentation

**Level:** README Update

**Action Items:**
1. [ ] Add fnm to supported tools list in README
2. [ ] Add fnm configuration example to jarvy.toml docs
3. [ ] Update "Version Managers" section if exists

**Suggested Content:**
- **fnm** - Fast Node.js version manager written in Rust

**Location:**
- File: README.md
- Section: Supported Tools (or create if missing)
```

## Key Principles

1. **Document the "Why"** - Code shows what, docs explain why
2. **User-first perspective** - Would a new user need this info?
3. **Minimal but complete** - Don't over-document, but don't leave gaps
4. **Keep it current** - Outdated docs are worse than no docs
5. **Examples over explanations** - Show, don't just tell
6. **Single source of truth** - Don't duplicate information

## Quick Reference: Do I Need to Document This?

Answer these questions:

1. **Does this change how users interact with the tool?**
   - Yes → README or dedicated doc

2. **Does this change configuration options?**
   - Yes → README config section

3. **Does this add a new tool/feature?**
   - Yes → README + possibly dedicated doc

4. **Is this a breaking change?**
   - Yes → README + migration guide + changelog

5. **Is this a bug fix users might search for?**
   - Yes → Brief mention in changelog/release notes

6. **Is this internal refactoring only?**
   - Yes → Code comments if logic is complex, otherwise commit message is sufficient

## Checklist Before PR

- [ ] README updated if user-facing changes
- [ ] Code comments added for complex logic
- [ ] Examples tested and working
- [ ] Help text updated for CLI changes
- [ ] Changelog updated (if project uses one)
- [ ] Migration guide written (if breaking change)

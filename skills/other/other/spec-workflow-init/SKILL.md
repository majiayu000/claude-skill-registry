---
name: spec-workflow-init
description: Scaffold spec-workflow configuration in your project. Creates config files, philosophy templates, and persona examples.
argument-hint: [--minimal] [--full] [--philosophy-only]
allowed-tools:
  - Read
  - Write
  - Bash(mkdir *)
  - Bash(ls *)
---

# Spec Workflow Init

Scaffolds the spec-workflow configuration structure in your project.

## Arguments

- `--minimal`: Create only `config.yaml` with documented options
- `--full`: Create all files with example content (default)
- `--philosophy-only`: Create only philosophy and persona files

## What Gets Created

### Minimal (`--minimal`)

```
.claude/
└── spec-workflow/
    └── config.yaml         # Commented config with all options
```

### Full (`--full`, default)

```
.claude/
└── spec-workflow/
    ├── config.yaml         # Commented config
    ├── philosophy/
    │   ├── exploration.md  # Exploration guidance
    │   ├── spec-standards.md  # Spec quality standards
    │   └── review-criteria.md # Review focus areas
    ├── personas/
    │   └── example.md      # Example custom persona
    └── templates/
        └── spec.md         # Spec template (customize as needed)
```

### Philosophy Only (`--philosophy-only`)

```
.claude/
└── spec-workflow/
    ├── philosophy/
    │   ├── exploration.md
    │   ├── spec-standards.md
    │   └── review-criteria.md
    └── personas/
        └── example.md
```

---

## Process

1. **Check for existing config**
   - If `.claude/spec-workflow/` exists, ask user before overwriting
   - Options: Skip existing files / Overwrite all / Cancel

2. **Detect project structure**
   - Look for package.json, Cargo.toml, go.mod, etc.
   - Identify services/workspaces
   - Pre-populate config with detected structure

3. **Create directory structure**
   ```bash
   mkdir -p .claude/spec-workflow/{philosophy,personas,templates}
   ```

4. **Generate config.yaml**
   - Include all options with comments
   - Pre-fill detected services
   - Pre-fill detected build/test commands

5. **Generate philosophy files** (unless --minimal)
   - Create starter templates with guidance

6. **Generate example persona** (unless --minimal)
   - Create one example to show the format

7. **Generate spec template** (unless --minimal or --philosophy-only)
   - Copy the default template for customization

8. **Report completion**
   ```
   Spec workflow configuration created at .claude/spec-workflow/

   Files created:
   - config.yaml (customize paths and services)
   - philosophy/exploration.md (customize exploration guidance)
   - philosophy/spec-standards.md (customize spec standards)
   - philosophy/review-criteria.md (customize review focus)
   - personas/example.md (add your own personas here)
   - templates/spec.md (customize your spec template)

   Next steps:
   1. Review and customize config.yaml for your project
   2. Edit philosophy files to match your team's approach
   3. Add custom reviewer personas if needed
   4. Try /idea-explorer to start exploring an idea
   ```

---

## Generated File Contents

### config.yaml

```yaml
# Spec Workflow Configuration
# See: https://github.com/ky1ejs/claude-plugins/tree/main/plugins/spec-workflow

# ─────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────
paths:
  # Where specs are saved
  specs: "./specs"

  # Where git worktrees are created
  worktrees: "./worktrees"

# ─────────────────────────────────────────────────────────────
# SERVICES (your technology stack)
# ─────────────────────────────────────────────────────────────
# Auto-detected from your project. Customize as needed.
services:
  # Example service configuration:
  # backend:
  #   path: "./backend"
  #   build: "npm run build"
  #   test: "npm test"
  #   lint: "npm run lint"
  #   patterns: "./backend/ARCHITECTURE.md"  # Optional: architecture docs

# ─────────────────────────────────────────────────────────────
# SPEC FORMAT
# ─────────────────────────────────────────────────────────────
spec:
  # Naming pattern for spec files
  # Tokens: {date}, {topic}
  naming: "{date}-{topic}-spec.md"

  # Required frontmatter fields
  requiredFields:
    - status

  # Optional frontmatter fields (documented but not required)
  optionalFields:
    - worktree
    - branch
    - services

# ─────────────────────────────────────────────────────────────
# REVIEW PROCESS
# ─────────────────────────────────────────────────────────────
review:
  # Maximum revision cycles before escalating to human
  maxIterations: 3

  # Consensus level for auto-approval (0.0 to 1.0)
  # Set to 1.0 to always require human approval
  autoApproveThreshold: 0.8

  # Reviewer selection
  selection:
    # "auto" = select based on spec type
    # "all" = always use all personas
    # "explicit" = only use personas in spec frontmatter
    strategy: "auto"

    # Minimum/maximum reviewers per spec
    minimum: 2
    maximum: 4

# ─────────────────────────────────────────────────────────────
# EXECUTION
# ─────────────────────────────────────────────────────────────
execution:
  # Implementation steps per batch before checkpoint
  batchSize: 5

  # Checkpoint behavior
  checkpoint:
    # "pause" = always pause for user review
    # "continue" = auto-continue if no issues
    # "smart" = pause on warnings/errors, continue otherwise
    behavior: "smart"

  # Parallelization settings
  parallel:
    enabled: true
    maxAgents: 3

# ─────────────────────────────────────────────────────────────
# WORKTREE
# ─────────────────────────────────────────────────────────────
worktree:
  # Branch naming pattern
  # Tokens: {name}, {date}
  branchNaming: "{name}"

  # Default base branch (null = current branch)
  defaultBase: null

  # Hook script to run after worktree creation
  # Receives: WORKTREE_PATH, WORKTREE_NAME, SPEC_FILE, BASE_BRANCH
  onBootstrap: null
  # Example: onBootstrap: "./scripts/bootstrap-worktree.sh"
```

### philosophy/exploration.md

```markdown
# Exploration Philosophy

Customize this file to guide how ideas are explored before becoming specs.

## When is exploration complete?

An idea is ready for spec writing when:

- [ ] The problem is clearly articulated
- [ ] We've identified who benefits and how
- [ ] Technical approach is outlined (not detailed)
- [ ] Major unknowns are called out
- [ ] Scope is bounded

## Questions we always ask

1. What's the simplest version that delivers value?
2. What existing patterns can we reuse?
3. What are we explicitly NOT doing?

## Red flags to surface

- Scope creep ("while we're at it...")
- Premature optimization
- Solutions looking for problems
```

### philosophy/spec-standards.md

```markdown
# Spec Standards

Customize this file to define what makes a good spec in your project.

## What makes a good spec?

A spec is ready for review when:

- Someone unfamiliar with the context can implement it
- Edge cases are explicitly handled or explicitly deferred
- Testing strategy is clear
- Rollback plan exists for risky changes

## Our conventions

- Implementation steps should be atomic (one concern each)
- Prefer explicit over clever
- Include "Why" not just "What"
```

### philosophy/review-criteria.md

```markdown
# Review Criteria

Customize this file to guide what reviewers focus on.

## What reviewers should evaluate

1. **Completeness**: Can this be implemented without guesswork?
2. **Correctness**: Does this solve the actual problem?
3. **Consistency**: Does this fit our existing patterns?
4. **Risk**: Are failure modes addressed?

## Review tone

- Assume good intent
- Ask questions rather than demand changes
- "Consider..." rather than "You must..."
- Distinguish blocking issues from suggestions
```

### personas/example.md

```markdown
---
name: Example Reviewer
triggers:
  - example
  - demo
---

# Example Reviewer Persona

This is an example custom persona. Create your own by adding `.md` files to this directory.

## Your perspective

Describe the perspective this reviewer brings.

## What you look for

- Thing 1
- Thing 2
- Thing 3

## Your style

Describe how this reviewer communicates feedback.

## When to pass

If you don't have substantive feedback, respond: "No concerns from an example perspective—LGTM."
```

### templates/spec.md

Copy the built-in template from references/spec-template.md for users to customize.

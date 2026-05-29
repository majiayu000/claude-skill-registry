---
name: scratch-workspace
description: Use when creating temporary files, drafts, experiments, or any content that should not be committed to version control. Ensures proper placement in .claude/.scratch with gitignore configuration.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Scratch Workspace Management

This skill covers proper use of the `.claude/.scratch/` directory for temporary, exploratory, and draft work.

## Purpose

The scratch workspace provides a gitignored location for:

- Draft implementations
- Experimental code
- Temporary test files
- Planning documents
- Any work-in-progress that shouldn't be committed

## Setup Checklist

Before creating scratch files:

1. **Ensure directory exists**

   ```bash
   mkdir -p .claude/.scratch
   ```

2. **Verify gitignore**

   Check `.gitignore` contains:

   ```
   .claude/.scratch
   ```

   If missing, add it:

   ```bash
   echo '.claude/.scratch' >> .gitignore
   ```

## Directory Structure

Organize scratch files by purpose:

```
.claude/
├── .scratch/
│   ├── drafts/           # Work-in-progress implementations
│   │   └── feature-x.ts
│   ├── experiments/      # Exploratory code
│   │   └── perf-test.js
│   ├── notes/            # Planning and notes
│   │   └── architecture.md
│   └── temp/             # Truly temporary files
└── settings.json         # Claude settings (NOT scratch)
```

## Best Practices

### DO

- Create subdirectories for organization
- Use descriptive file names
- Clean up when work is complete
- Move finalized code to proper project locations

### DON'T

- Put sensitive data in scratch (still on disk)
- Use scratch for files that should be committed
- Leave stale scratch files indefinitely
- Put scratch files outside `.claude/.scratch/`

## Workflow

### Starting Exploratory Work

```bash
# Create scratch area
mkdir -p .claude/.scratch/experiments

# Work on experiment
# ... create files in .claude/.scratch/experiments/
```

### Promoting to Real Code

When scratch work is ready:

1. Review and refine the code
2. Move to appropriate project location
3. Delete scratch version
4. Commit the promoted code

### Cleanup

Periodically clean scratch:

```bash
# Review what's in scratch
ls -la .claude/.scratch/

# Remove old experiments
rm -rf .claude/.scratch/experiments/old-test/
```

## Integration with Other Tools

### With Git

The `.claude/.scratch` directory is gitignored, so:

- `git status` won't show scratch files
- `git add .` won't stage scratch files
- Scratch files won't appear in commits

### With IDE

Most IDEs will show `.claude/.scratch` in the file tree. You can:

- Add to IDE's exclude patterns
- Keep visible for easy access
- Use IDE's "mark as excluded" feature

## Common Patterns

### Draft Implementation

```
.claude/.scratch/drafts/
└── new-feature/
    ├── index.ts
    ├── types.ts
    └── test.ts
```

### Performance Experiment

```
.claude/.scratch/experiments/
└── perf-comparison/
    ├── approach-a.ts
    ├── approach-b.ts
    └── benchmark.ts
```

### Architecture Notes

```
.claude/.scratch/notes/
└── refactor-plan.md
```

## Troubleshooting

### Scratch files appearing in git status

```bash
# Verify gitignore entry
grep -r ".claude/.scratch" .gitignore

# If missing, add it
echo '.claude/.scratch' >> .gitignore
```

### Directory doesn't exist

```bash
mkdir -p .claude/.scratch
```

### Accidentally committed scratch files

```bash
# Remove from tracking but keep locally
git rm -r --cached .claude/.scratch
git commit -m "chore: remove scratch files from tracking"
```

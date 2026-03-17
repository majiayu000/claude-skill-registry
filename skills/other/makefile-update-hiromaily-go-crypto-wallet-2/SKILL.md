---
name: makefile-update
description: Makefile development workflow. Use when modifying Makefile or files in make/ directory.
---

# Makefile Workflow

Workflow for Makefile changes.

## Prerequisites

**Use `git-workflow` Skill** for branch, commit, and PR workflow.

## Applicable Files

| Path | Description |
|------|-------------|
| `Makefile` | Main makefile |
| `make/*.mk` | Included makefiles |

## Structure

```
Makefile              # Main entry point, includes make/*.mk
make/
├── go.mk            # Go-related targets
├── docker.mk        # Docker targets
├── atlas.mk         # Database migration targets
├── sqlc.mk          # SQLC generation targets
└── ...
```

## Verification Commands

```bash
make mk-lint    # Lint makefiles
```

### Manual Checks

```bash
# List all targets
make help

# Dry run (if supported)
make -n {target}
```

## Guidelines

### Style

- Use tabs for indentation (required by Make)
- Use `.PHONY` for non-file targets
- Add help text for targets
- Group related targets

### Best Practices

- [ ] Targets are `.PHONY` if not creating files
- [ ] Dependencies are correct
- [ ] Variables use `?=` for defaults
- [ ] Help text exists for main targets

### Example Target

```makefile
.PHONY: my-target
my-target: ## Description of target
	@echo "Running my-target..."
	command1
	command2
```

## Verification Checklist

- [ ] `make mk-lint` passes
- [ ] Target runs correctly
- [ ] Dependencies work
- [ ] Help text is accurate

## Commit Format

```
chore(make): {brief description}

- {change 1}
- {change 2}

Closes #{issue_number}
```

## Related Skills

- `git-workflow` - Branch, commit, PR workflow

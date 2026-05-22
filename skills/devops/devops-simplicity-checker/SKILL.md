---
name: devops-simplicity-checker
description: Infrastructure simplicity scoring. Detects overengineering in Terraform/OpenTofu and Ansible configurations.
allowed-tools: Bash, Glob, Grep
---

# DevOps Simplicity Checker

Infrastructure should be SIMPLE by default. This skill detects overengineering.

## Simplicity Checklist

| Check | Pass | Fail |
|-------|------|------|
| File count | ≤8 .tf files | >15 files in nested directories |
| Module usage | None or registry only | Custom modules for <5 resources |
| Directory depth | Flat or 1 level | 3+ levels of nesting |
| Ansible playbooks | Single playbook | Multiple playbooks + custom roles |
| Ansible roles | Galaxy roles only | Custom roles for standard tasks |
| Variables | Inline defaults | Complex variable hierarchies |

## Complexity Score Calculation

```
Files: 1 point per .tf file over 5
Modules: 3 points per custom module
Directories: 2 points per level over 1
Ansible roles: 3 points per custom role

Score 0-5: Simple (GOOD)
Score 6-10: Moderate (REVIEW)
Score 11+: Overengineered (SIMPLIFY)
```

## Detection Commands

```bash
# Count .tf files
find . -name "*.tf" | wc -l

# Find custom modules (not registry)
grep -r "source\s*=" *.tf | grep -v "registry.terraform.io" | grep -v "github.com" | wc -l

# Directory depth
find . -name "*.tf" -printf '%h\n' | sort -u | awk -F'/' '{print NF-1}' | sort -rn | head -1

# Custom Ansible roles (not Galaxy)
ls roles/ 2>/dev/null | wc -l

# Variable files
find . -name "*.tfvars" -o -name "variables.tf" | wc -l
```

## Questions to Ask

- Could this be done with fewer files?
- Is this custom module solving a problem registry modules can't?
- Would a flat structure work just as well?
- Does this Ansible role exist in Galaxy already?
- Are these variable hierarchies necessary or premature abstraction?

## Red Flags

| Pattern | Problem | Fix |
|---------|---------|-----|
| `modules/` with single resource | Over-abstraction | Inline the resource |
| `environments/{dev,staging,prod}/` | Duplication | Use workspaces or tfvars |
| `roles/common/` for apt packages | Reinventing wheel | Use Galaxy role |
| Nested `.tf` imports | Hard to follow | Flatten structure |
| >10 variable files | Configuration sprawl | Consolidate |

## Scoring Report Format

```
SIMPLICITY SCORE: X/10

File Count: X files (+Y penalty)
Custom Modules: X modules (+Y penalty)
Directory Depth: X levels (+Y penalty)
Custom Roles: X roles (+Y penalty)

Total Penalty: X points
Verdict: SIMPLE | MODERATE | OVERENGINEERED

Recommendations:
- [ ] Consider flattening directory structure
- [ ] Replace custom module X with registry module
- [ ] Use Galaxy role for standard task
```

---
description: Triage and analyze GitHub issues from iNavFlight/inav repository
triggers:
  - triage issues
  - analyze issues
  - github issues
  - look at issues
  - review issues
  - readily solvable
  - fetch issues
---

# GitHub Issue Triage Skill

Systematically analyze and categorize GitHub issues from the iNavFlight/inav repository.

## File Structure

```
claude/manager/issue-triage/
  INDEX.md              # Quick lookup: issue# -> category file
  fetch_issues.py       # Script to fetch and search issues
  issues.json           # Cached issues data from GitHub
  readily-solvable.md   # Issues ready to fix
  needs-investigation.md
  documentation.md
  enhancement-simple.md
  enhancement-complex.md
  hardware-dependent.md
  no-action.md          # Won't fix, duplicates, already fixed
```

## Quick Commands

### Refresh Issue Cache

```bash
cd claude/manager/issue-triage
python3 fetch_issues.py --refresh
```

### Fetch More Issues

```bash
python3 fetch_issues.py --pages 5 --refresh
```

### View Specific Issue

```bash
python3 fetch_issues.py --issue 11156
```

### Search Issues

```bash
python3 fetch_issues.py --search "GPS"
python3 fetch_issues.py --search "overflow"
```

### List Cached Issues

```bash
python3 fetch_issues.py
```

## Categories

| Category | File | Description |
|----------|------|-------------|
| Readily Solvable | `readily-solvable.md` | Clear problem, known solution |
| Needs Investigation | `needs-investigation.md` | Promising, needs analysis |
| Documentation | `documentation.md` | Docs fixes/improvements |
| Enhancement (Simple) | `enhancement-simple.md` | Small feature additions |
| Enhancement (Complex) | `enhancement-complex.md` | Major feature work |
| Hardware Dependent | `hardware-dependent.md` | Needs specific hardware |
| No Action | `no-action.md` | Won't fix, duplicates, etc. |

## Workflow

1. **Refresh cache:** `python3 fetch_issues.py --refresh`
2. **Review list** for promising issues
3. **View details:** `python3 fetch_issues.py --issue XXXXX`
4. **Add to INDEX.md** with category link
5. **Add details** to appropriate category file

## Finding Readily Solvable Issues

Look for:
- Clear reproduction steps
- Isolated, specific problem
- No special hardware required
- Community consensus on behavior
- Small code changes

Avoid:
- Architecture changes needed
- Hardware-specific (can't test)
- Unclear requirements

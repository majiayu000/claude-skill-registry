---
name: ralph-runner
description: Run long-running autonomous AI agents using PRD-based task scoping.
---

# Ralph Wiggum Agent Runner

Run autonomous coding agents that ship code while you sleep.

## When to Use
- Multi-story feature implementation
- Overnight autonomous coding
- Batch processing of related tasks
- When you want AI to work independently

## Quick Commands
```bash
# Run with current PRD
./scripts/ralph/ralph.sh

# Run with custom PRD
./scripts/ralph/ralph.sh scripts/ralph/my-feature.json

# Watch progress
tail -f scripts/ralph/progress.txt
```

## How It Works
1. Agent reads PRD, picks highest priority incomplete story
2. Implements ONLY that one story
3. Runs build/lint to ensure CI stays green
4. Commits work, updates PRD, appends to progress.txt
5. Repeats until all stories pass or max iterations

## PRD Structure
```json
{
  "stories": [
    {
      "id": "STORY-001",
      "title": "User can do X",
      "priority": 1,
      "passes": false,
      "acceptance_criteria": ["..."],
      "files_to_modify": ["..."]
    }
  ]
}
```

## Stop Condition
Agent emits `<promise>COMPLETE</promise>` when all stories pass.

## Files
| File | Purpose |
|------|---------|
| `scripts/ralph/ralph.sh` | Runner script |
| `scripts/ralph/prd.json` | Current PRD |
| `scripts/ralph/progress.txt` | Progress log |

## Reference Files
| Topic | File |
|-------|------|
| Full documentation | `scripts/ralph/README.md` |
| PRD template | `scripts/ralph/prd.template.json` |

## Related Skills
- `empathy-ledger-codebase` - Codebase patterns
- `deployment-workflow` - CI/CD integration

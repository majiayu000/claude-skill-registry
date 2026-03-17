---
name: ralph-run
description: Run RALPH autonomous development loop to implement features from the PRD.
allowed-tools: Bash, Read, Edit, Write
---

# Run RALPH

Execute the RALPH autonomous development loop to implement features from the PRD.

## Two Operating Modes

### 1. PRD Loop Mode (Greenfield)
For implementing features from a PRD file:
```bash
./scripts/ralph/ralph.sh 20
```

### 2. Single-Task Mode (Brownfield)
For quick one-off tasks without a PRD:
```bash
./scripts/ralph/ralph.sh --task "Fix the login button styling"
```

## Prerequisites Check

1. Verify PRD exists (one of these formats):
```bash
cat prd.json 2>/dev/null || cat PRD.md 2>/dev/null || cat tasks.yaml 2>/dev/null
```

2. Check RALPH configuration:
```bash
cat .ralph/config.yaml
```

3. Check current status:
```bash
node scripts/run-ralph.js --status
```

## Running RALPH

### Start the autonomous loop:
```bash
# Run up to 20 iterations
./scripts/ralph/ralph.sh 20

# Or use the runner script
node scripts/run-ralph.js 20
```

### With options:
```bash
# Skip tests (faster iteration)
./scripts/ralph/ralph.sh --skip-tests 20

# Skip linting
./scripts/ralph/ralph.sh --skip-lint 20

# Custom branch
./scripts/ralph/ralph.sh --branch feature/my-feature 20

# Dry run (no commits)
./scripts/ralph/ralph.sh --dry-run 20
```

## PRD Formats Supported

### JSON (prd.json)
```json
{
  "userStories": [
    { "id": "US-001", "title": "...", "passes": false }
  ]
}
```

### Markdown (PRD.md)
```markdown
## Tasks
- [ ] First task
- [ ] Second task
- [x] Completed task
```

### YAML (tasks.yaml)
```yaml
tasks:
  - title: First task
    completed: false
```

## Configuration

Edit `.ralph/config.yaml` to customize:

- **rules**: Instructions the AI MUST follow
- **boundaries**: Files the AI should NOT modify
- **commands**: Quality gate commands
- **settings**: Retry logic, auto-commit, etc.

## Monitoring

- Watch `.ralph/progress.txt` for iteration logs and learnings
- Check PRD file for story completion status
- Review git log for commits: `git log --oneline -20`

## Commands

| Command | Description |
|---------|-------------|
| `--status` | Show PRD completion status |
| `--validate` | Validate PRD schema |
| `--reset` | Reset progress.txt |
| `--analyze` | Re-run project analysis |
| `--task "..."` | Single-task mode (brownfield) |
| `--skip-tests` | Skip test quality gate |
| `--skip-lint` | Skip lint quality gate |
| `--dry-run` | Don't commit changes |

## If Stuck

1. Check `.ralph/progress.txt` for patterns and learnings
2. Review `.ralph/config.yaml` rules and boundaries
3. Manually fix blocking issues
4. Reset if needed: `node scripts/run-ralph.js --reset`
5. Resume: `./scripts/ralph/ralph.sh 20`

## Quality Gates

RALPH must pass ALL quality gates before marking a task complete:

1. **Typecheck**: `npm run typecheck` or `npx tsc --noEmit`
2. **Lint**: `npm run lint`
3. **Tests**: `npm test`

Configure these in `.ralph/config.yaml` under `commands`.

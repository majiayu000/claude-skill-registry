---
name: ralph-run
description: Run RALPH autonomous development loop to implement features from the PRD.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# Run RALPH - Autonomous Development

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

## Trigger

This skill activates when:
- `/ralph-run` - Start RALPH with default iterations (10)
- `/ralph-run 20` - Start RALPH with specified iterations
- `/ralph-run --task "description"` - Single-task mode
- User says "run RALPH", "start autonomous development", etc.

## Prerequisites Check

### 1. Verify PRD exists (supports multiple formats)

```bash
# Check for PRD in multiple formats
if [ -f prd.json ]; then
  echo "✓ Found prd.json (JSON format)"
  # Validate JSON
  cat prd.json | jq . > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "❌ prd.json is not valid JSON"
    exit 1
  fi
  # Check for incomplete stories
  REMAINING=$(cat prd.json | jq '[.userStories[] | select(.passes == false)] | length')
elif [ -f PRD.md ]; then
  echo "✓ Found PRD.md (Markdown format)"
  # Count unchecked tasks
  REMAINING=$(grep -c '^\s*- \[ \]' PRD.md || echo "0")
elif [ -f tasks.yaml ]; then
  echo "✓ Found tasks.yaml (YAML format)"
  REMAINING=$(grep -c 'completed: false' tasks.yaml || echo "0")
else
  echo "❌ No PRD found"
  echo ""
  echo "Create one first:"
  echo "  /prd [feature description]"
  echo "  or"
  echo "  Create prd.json, PRD.md, or tasks.yaml"
  exit 1
fi

if [ "$REMAINING" -eq 0 ]; then
  echo "✓ All stories already complete!"
  exit 0
fi

echo "✓ Found $REMAINING incomplete stories/tasks"
```

### 2. Check RALPH configuration

```bash
# Check for .ralph/config.yaml
if [ -f .ralph/config.yaml ]; then
  echo "✓ Found .ralph/config.yaml"
  # Show configured commands
  echo "  Quality gates:"
  grep -A4 "commands:" .ralph/config.yaml | tail -4
else
  echo "⚠ No .ralph/config.yaml found"
  echo "  Run /setup-project to generate it"
fi
```

### 3. Verify PROJECT_SPEC.md exists (recommended)

```bash
if [ ! -f PROJECT_SPEC.md ]; then
  echo "⚠ PROJECT_SPEC.md not found"
  echo "  RALPH works better with project context"
  echo "  Run /setup-project to generate it"
fi
```

### 4. Check Git status

```bash
# Ensure clean working directory or uncommitted changes are intentional
git status --short
```

### 5. Show PRD status

```bash
echo "=== PRD Status ==="
if [ -f prd.json ]; then
  cat prd.json | jq '{
    project: .project,
    branch: .branchName,
    total: (.userStories | length),
    complete: ([.userStories[] | select(.passes == true)] | length),
    remaining: ([.userStories[] | select(.passes == false)] | length)
  }'
  echo ""
  echo "=== Stories to Implement ==="
  cat prd.json | jq -r '.userStories[] | select(.passes == false) | "  \(.id): \(.title) (Priority \(.priority))"'
elif [ -f PRD.md ]; then
  echo "Remaining tasks:"
  grep '^\s*- \[ \]' PRD.md
elif [ -f tasks.yaml ]; then
  echo "Remaining tasks:"
  grep -B1 'completed: false' tasks.yaml | grep 'title:'
fi
```

## Running RALPH

### Option 1: Bash Script (Recommended)

```bash
./scripts/ralph/ralph.sh 20
```

The script:
1. Detects PRD format (JSON/Markdown/YAML) automatically
2. Loads configuration from .ralph/config.yaml (rules, boundaries)
3. Runs Claude with context-aware RALPH prompt
4. Each iteration implements ONE story
5. Runs quality gates (typecheck, lint, tests)
6. Checks for `<promise>COMPLETE</promise>` signal
7. Stops when all stories pass or max iterations reached

### With CLI Options:

```bash
# Skip tests (faster iteration)
./scripts/ralph/ralph.sh --skip-tests 20

# Skip linting
./scripts/ralph/ralph.sh --skip-lint 20

# Custom branch
./scripts/ralph/ralph.sh --branch feature/my-feature 20

# Dry run (no commits)
./scripts/ralph/ralph.sh --dry-run 20

# Single-task mode (no PRD needed)
./scripts/ralph/ralph.sh --task "Add dark mode toggle to settings page"
```

### Option 2: Node.js Runner

```bash
node scripts/run-ralph.js 20
```

Additional options:
```bash
node scripts/run-ralph.js --status       # Show PRD status
node scripts/run-ralph.js --validate     # Validate prd.json
node scripts/run-ralph.js --reset        # Reset progress.txt
node scripts/run-ralph.js --analyze      # Re-analyze project
node scripts/run-ralph.js --skip-tests   # Skip test quality gate
node scripts/run-ralph.js --skip-lint    # Skip lint quality gate
node scripts/run-ralph.js --dry-run      # Don't commit changes
```

## Configuration

RALPH configuration is stored in `.ralph/config.yaml`:

```yaml
# Rules - AI MUST follow these on every task
rules:
  - "Always use TypeScript strict mode"
  - "Follow existing patterns in src/utils/"
  - "Write tests for all new functions"

# Boundaries - AI should NOT modify these files
boundaries:
  never_touch:
    - "src/legacy/**"
    - "migrations/**"
    - "*.lock"

# Quality gate commands
commands:
  test: "npm test"
  lint: "npm run lint"
  typecheck: "npx tsc --noEmit"
  build: "npm run build"

# Execution settings
settings:
  max_retries: 3
  retry_delay: 5
  auto_commit: true
```

### Option 3: Manual Iteration

For more control, run iterations manually:

```bash
# Run single iteration
claude -p "$(cat scripts/ralph/CLAUDE.md)"

# Check progress
cat prd.json | jq '.userStories[] | {id, title, passes}'

# Review changes
git log --oneline -5
git diff HEAD~1

# Continue if needed
claude -p "$(cat scripts/ralph/CLAUDE.md)"
```

## RALPH Execution Flow

Each RALPH iteration follows this flow:

```
┌─────────────────────────────────────────────────────────┐
│                    RALPH ITERATION                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. READ CONTEXT                                        │
│     ├── prd.json (stories, completion status)           │
│     ├── PROJECT_SPEC.md (tech stack, patterns)          │
│     ├── progress.txt (learnings from prior iterations)  │
│     └── git log (what was done before)                  │
│                                                         │
│  2. SELECT STORY                                        │
│     └── Pick highest priority with passes: false        │
│                                                         │
│  3. IMPLEMENT                                           │
│     ├── Follow PROJECT_SPEC.md patterns                 │
│     ├── Write clean, production-ready code              │
│     └── Meet ALL acceptance criteria                    │
│                                                         │
│  4. QUALITY GATES                                       │
│     ├── Typecheck: npm run typecheck / npx tsc          │
│     ├── Lint: npm run lint                              │
│     └── Test: npm test                                  │
│                                                         │
│  5. COMMIT                                              │
│     └── git commit -m "feat: US-XXX - Story Title"      │
│                                                         │
│  6. UPDATE PRD                                          │
│     └── Set passes: true in prd.json                    │
│                                                         │
│  7. LOG PROGRESS                                        │
│     └── Append learnings to progress.txt                │
│                                                         │
│  8. CHECK COMPLETION                                    │
│     ├── If all stories pass: <promise>COMPLETE</promise>│
│     └── Otherwise: exit for next iteration              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Monitoring Progress

### Watch progress.txt

```bash
# Real-time monitoring
tail -f progress.txt

# Last 50 lines
tail -50 progress.txt
```

### Check story status

```bash
# All stories
cat prd.json | jq '.userStories[] | {id, title, passes}'

# Remaining stories
cat prd.json | jq '.userStories[] | select(.passes == false) | {id, title, priority}'

# Completion percentage
cat prd.json | jq '
  (.userStories | length) as $total |
  ([.userStories[] | select(.passes == true)] | length) as $done |
  {total: $total, done: $done, remaining: ($total - $done), percent: (($done / $total) * 100 | floor)}
'
```

### View Git commits

```bash
# Recent commits
git log --oneline -10

# Commits on this branch
git log --oneline main..HEAD

# Show files changed
git diff --stat main..HEAD
```

## If RALPH Gets Stuck

### 1. Check progress.txt for patterns

```bash
# Look for recurring issues
grep -i "error\|fail\|stuck\|retry" progress.txt

# Review last iteration
tail -100 progress.txt
```

### 2. Fix blocking issues manually

```bash
# If tests fail, fix them
npm test

# If typecheck fails, fix types
npx tsc --noEmit

# If lint fails, fix or auto-fix
npm run lint -- --fix
```

### 3. Reset and continue

```bash
# Reset progress (preserves patterns)
node scripts/run-ralph.js --reset

# Or manually clear the stuck iteration
# Edit progress.txt to remove failed attempt

# Resume
./scripts/ralph/ralph.sh 20
```

### 4. Adjust the story

If a story is too complex:

```bash
# Edit prd.json to split the story
# Set the original back to passes: false
# Add new smaller stories with higher priority numbers
```

## Completion

When RALPH finishes:

### All stories complete

```
=== RALPH Complete ===

Project: [Feature Name]
Branch: ralph/[feature-slug]
Stories: [N]/[N] complete

Commits:
  abc1234 feat: US-001 - Story Title
  def5678 feat: US-002 - Story Title
  ...

Next Steps:
  1. Review the implementation:
     git diff main..HEAD

  2. Run full test suite:
     npm test

  3. Create PR:
     gh pr create --base main --title "feat: [Feature Name]"
```

### Partial completion (max iterations reached)

```
=== RALPH Paused ===

Completed: [X]/[N] stories
Remaining: [Y] stories

To continue:
  ./scripts/ralph/ralph.sh 20

To review progress:
  cat progress.txt
  cat prd.json | jq '.userStories[] | select(.passes == false)'
```

## Quality Commands Reference

### TypeScript/JavaScript

```bash
# Typecheck
npm run typecheck
# or
npx tsc --noEmit

# Lint
npm run lint
# or
npx eslint . --ext .ts,.tsx

# Test
npm test
# or
npx vitest run
```

### Python

```bash
# Type check
mypy .

# Lint
ruff check .
# or
pylint **/*.py

# Test
pytest
```

### Go

```bash
# Build
go build ./...

# Lint
golangci-lint run

# Test
go test ./...
```

## Example Session

```bash
# 1. Create PRD
/prd Add user authentication with email/password

# 2. Review generated PRD
cat prd.json
cat tasks/prd-user-authentication.md

# 3. Adjust if needed
# (edit prd.json)

# 4. Create feature branch
git checkout -b ralph/user-authentication

# 5. Run RALPH
./scripts/ralph/ralph.sh 20

# 6. Monitor (in another terminal)
watch -n 5 'cat prd.json | jq ".userStories[] | {id, passes}"'

# 7. When complete, review
git log --oneline main..HEAD
npm test

# 8. Create PR
gh pr create --base main
```

## Troubleshooting

### "No prd.json found"
Create one with `/prd [feature]` or `/ralph-convert tasks/prd-[name].md`

### "All stories already complete"
Reset with `--reset` flag or edit prd.json to set `passes: false`

### "Tests keep failing"
Check progress.txt for patterns, fix tests manually, then continue

### "RALPH making same mistake repeatedly"
Add explicit notes to progress.txt about the issue and correct approach

### "Story too large for one iteration"
Split into smaller stories in prd.json, adjust priorities

### "Quality gates passing but story not complete"
Check acceptance criteria - may need more specific criteria

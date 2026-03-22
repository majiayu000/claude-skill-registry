---
name: project-review
description: "Complete project health check: verify tests, documentation, database snapshots, migration progress, and suggest next steps. Run after completing any task or iteration."
user_invocable: true
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
---

# Project Review & Evaluation

Run a comprehensive project health check. This skill audits the current state of the BusinessLogic platform migration, verifies everything is safe, and produces a status report with actionable next steps.

**When to use:** After completing any task, iteration step, or when you want a full picture of where the project stands.

## Arguments

- No args: Full review (all sections)
- `quick`: Skip database dump and legacy comparison
- `report`: Generate a markdown report file in `docs/reports/`
- `plan`: Review + re-evaluate the migration plan and suggest adjustments

## Step 1: Git Status & Branch Health

```bash
# Current branch and recent history
git branch --show-current
git log --oneline -10
git status

# Check for uncommitted changes
git diff --stat

# Verify we're NOT on main
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "WARNING: You are on $BRANCH. Switch to a feature branch before making changes."
fi

# Show branch relationship
git log --oneline --graph --all -20
```

Report: current branch, uncommitted changes, last 5 commits, any warnings.

## Step 2: Test Suite Status

Run all available tests and report results:

```bash
./scripts/test-all.sh 2>&1
```

For each service, report:
- **PASS** (all tests green), **FAIL** (with failure details), or **SKIP** (service not set up yet)

If any tests fail, this is a **BLOCKER** — list the failures and suggest fixes before proceeding.

## Step 3: Service Health (if Docker is running)

```bash
# Check if Docker services are running
docker compose -f infrastructure/docker/docker-compose.dev.yml ps --format json 2>/dev/null

# If running, check health
./scripts/health-check.sh 2>&1

# Run contract tests
./scripts/test-contracts.sh 2>&1
```

Report: which services are up, which are healthy, which are down.

## Step 4: Database Snapshot Management

Maintain a rolling window of 5 database snapshots for safety.

### 4a: Take a new snapshot

```bash
SNAPSHOT_DIR="infrastructure/db-snapshots"
mkdir -p "$SNAPSHOT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
SNAPSHOT_FILE="$SNAPSHOT_DIR/snapshot_${TIMESTAMP}_${BRANCH}.sql.gz"

# Dump database (schema + data)
docker compose -f infrastructure/docker/docker-compose.dev.yml exec -T postgres \
  pg_dump -U directus -d directus --clean --if-exists | gzip > "$SNAPSHOT_FILE"

echo "Snapshot saved: $SNAPSHOT_FILE ($(du -h "$SNAPSHOT_FILE" | cut -f1))"
```

### 4b: Rotate old snapshots (keep only 5)

```bash
SNAPSHOT_DIR="infrastructure/db-snapshots"
SNAPSHOT_COUNT=$(ls -1 "$SNAPSHOT_DIR"/snapshot_*.sql.gz 2>/dev/null | wc -l)

if [ "$SNAPSHOT_COUNT" -gt 5 ]; then
  # Remove oldest snapshots, keep newest 5
  ls -1t "$SNAPSHOT_DIR"/snapshot_*.sql.gz | tail -n +6 | xargs rm -f
  echo "Rotated: kept 5 newest snapshots, removed $(($SNAPSHOT_COUNT - 5)) old ones"
fi

# List current snapshots
echo "Current snapshots:"
ls -lh "$SNAPSHOT_DIR"/snapshot_*.sql.gz 2>/dev/null || echo "  (none)"
```

### 4c: Schema documentation

```bash
# Export current schema as reference
docker compose -f infrastructure/docker/docker-compose.dev.yml exec -T postgres \
  pg_dump -U directus -d directus --schema-only --no-owner --no-privileges \
  > "$SNAPSHOT_DIR/schema_current.sql"

echo "Schema exported: $SNAPSHOT_DIR/schema_current.sql"
```

Report: snapshot taken, rotation status, current schema saved.

## Step 5: Documentation Completeness

Check that key documentation is up-to-date:

```bash
# Check all required docs exist
DOCS=(
  "CLAUDE.md"
  "docs/evolution-plan.md"
  "docs/database-strategy.md"
  "docs/migration-safety.md"
  "docs/architecture-diagram.html"
)

for doc in "${DOCS[@]}"; do
  if [ -f "$doc" ]; then
    MOD_DATE=$(stat -c '%Y' "$doc" 2>/dev/null || stat -f '%m' "$doc" 2>/dev/null)
    echo "OK: $doc (modified: $(date -d @$MOD_DATE '+%Y-%m-%d' 2>/dev/null || date -r $MOD_DATE '+%Y-%m-%d' 2>/dev/null))"
  else
    echo "MISSING: $doc"
  fi
done

# Check iteration plans
for i in 00 01 02 03 04 05; do
  PLAN=$(ls docs/migrations/iteration-${i}* 2>/dev/null | head -1)
  if [ -n "$PLAN" ]; then
    echo "OK: $PLAN"
  else
    echo "MISSING: iteration-$i plan"
  fi
done
```

Check if CLAUDE.md reflects the current reality:
- Do services listed in CLAUDE.md match what actually exists in services/?
- Do test commands in CLAUDE.md match what test-all.sh runs?
- Are env variables documented correctly?

## Step 6: Migration Progress Assessment

Read each iteration plan and check completion status:

```bash
# For each iteration, check completion checklist
for i in 00 01 02 03 04 05; do
  PLAN=$(ls docs/migrations/iteration-${i}* 2>/dev/null | head -1)
  if [ -n "$PLAN" ]; then
    TOTAL=$(grep -c '^\- \[' "$PLAN" 2>/dev/null || echo 0)
    DONE=$(grep -c '^\- \[x\]' "$PLAN" 2>/dev/null || echo 0)
    echo "Iteration $i: $DONE/$TOTAL complete"
  fi
done
```

Cross-reference with actual file system state:
- services/formula-api/ has content? → Step 0.1 done
- services/flow/ has content? → Step 0.2 done
- services/cms/ has content? → Step 0.3 done
- services/ai-api/ has content beyond scaffold? → Iteration 1 progress
- services/gateway/ has content? → Iteration 2 progress

## Step 7: Legacy vs New Comparison (skip if `quick`)

If both legacy and new services are running:

```bash
# Compare key endpoints
echo "=== CMS ==="
curl -s -o /dev/null -w "New (8055): %{http_code} %{time_total}s\n" http://localhost:8055/server/ping
curl -s -o /dev/null -w "Legacy (8056): %{http_code} %{time_total}s\n" http://localhost:8056/server/ping

echo "=== Formula API ==="
curl -s -o /dev/null -w "Formula (3000): %{http_code} %{time_total}s\n" http://localhost:3000/ping

echo "=== Flow ==="
curl -s -o /dev/null -w "Flow (3100): %{http_code} %{time_total}s\n" http://localhost:3100/ping
```

## Step 8: Generate Report

Compile all findings into a structured report:

### Report Template

```markdown
# Project Review — [DATE]

## Branch: [current branch]
## Iteration: [current iteration based on branch name]

### Test Results
| Service | Status | Details |
|---------|--------|---------|
| formula-api | PASS/FAIL/SKIP | X pass, Y fail |
| flow | PASS/FAIL/SKIP | X pass, Y fail |
| cms | PASS/FAIL/SKIP | X pass, Y fail |
| ai-api | PASS/FAIL/SKIP | X pass, Y fail |
| gateway | PASS/FAIL/SKIP | X pass, Y fail |
| contracts | PASS/FAIL/SKIP | X pass, Y fail |

### Service Health
| Service | Port | Status |
|---------|------|--------|
| bl-cms | 8055 | UP/DOWN |
| bl-formula-api | 3000 | UP/DOWN |
| bl-flow-trigger | 3100 | UP/DOWN |
| bl-ai-api | 3200 | UP/DOWN |
| bl-gateway | 8080 | UP/DOWN |

### Database
- Snapshot: [filename] ([size])
- Schema exported: YES/NO
- Snapshots on disk: X/5

### Migration Progress
| Iteration | Status | Progress |
|-----------|--------|----------|
| 0: Foundation | NOT STARTED/IN PROGRESS/COMPLETE | X/Y steps |
| 1: AI API | NOT STARTED/IN PROGRESS/COMPLETE | X/Y steps |
| 2: Gateway | NOT STARTED/IN PROGRESS/COMPLETE | X/Y steps |
| 3: Public API | NOT STARTED/IN PROGRESS/COMPLETE | X/Y steps |
| 4: Flow AI | NOT STARTED/IN PROGRESS/COMPLETE | X/Y steps |
| 5: Hardening | NOT STARTED/IN PROGRESS/COMPLETE | X/Y steps |

### Blockers
- [List any failing tests, missing files, or inconsistencies]

### Suggested Next Steps
1. [Most important action based on current state]
2. [Second priority]
3. [Third priority]

### Plan Adjustments (if any)
- [Any changes to the migration plan based on what was found]
```

If `report` argument was given, save to `docs/reports/review_[DATE].md`.

## Step 9: Suggest Next Steps

Based on the review, recommend what to do next:

1. **If tests are failing:** Fix them first. Nothing else matters.
2. **If current iteration is incomplete:** Show which step to do next.
3. **If current iteration is complete:** Suggest merging to dev, starting next iteration.
4. **If documentation is stale:** List what needs updating.
5. **If database has no snapshots:** Take one before proceeding.
6. **If there are uncommitted changes:** Commit or stash them.

## Step 10: Plan Re-evaluation (only if `plan` argument)

If the user asked for plan re-evaluation:

1. Read all iteration plans
2. Read the evolution plan and database strategy
3. Compare planned architecture with current reality
4. Identify:
   - Steps that turned out easier/harder than expected
   - New risks or opportunities discovered during implementation
   - Timeline adjustments needed
   - Dependencies that changed
5. Suggest specific amendments to the plan
6. Write updated assessment to `docs/reports/plan_reassessment_[DATE].md`

## Important Rules

- **Never skip the test step.** If tests fail, the review status is RED regardless of everything else.
- **Always take a database snapshot** (unless `quick` mode) — it costs nothing and saves everything.
- **Be honest about blockers.** Don't sugarcoat. If something is broken, say so clearly.
- **The report is for the CTO.** Write it so Danila can understand the project state in 30 seconds.

---
name: safe-schedule-generation
description: Safe schedule generation with mandatory backup. REQUIRES database backup before any write operations to schedule tables. Use when generating schedules, bulk assigning, or executing swaps.
model_tier: opus
parallel_hints:
  can_parallel_with: []
  must_serialize_with: [schedule-optimization, SCHEDULING, solver-control, swap-management]
  preferred_batch_size: 1
context_hints:
  max_file_context: 40
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "backup.*fail|no.*backup"
    reason: "Backup failures block all schedule modifications"
  - pattern: "rollback|restore"
    reason: "Rollback operations require human oversight"
  - keyword: ["production", "live", "destroy", "clear"]
    reason: "Destructive operations require explicit human approval"
---

# Safe Schedule Generation Skill

**HARD GATE:** No schedule generation, bulk assignment, or destructive operation without verified backup.

## When This Skill Activates

- Generating new schedules via API or MCP
- Bulk assigning residents/faculty to rotations
- Executing swap requests
- Clearing or regenerating schedule blocks
- Any operation that modifies `assignments` table

## MANDATORY Pre-Flight Checklist

**ALL checks MUST pass before any database-modifying operation:**

### 1. Backup Verification
```bash
# Check most recent backup
ls -la backups/postgres/*.sql.gz | tail -1

# Verify backup is recent (created within last 2 hours)
find backups/postgres -name "*.sql.gz" -mmin -120 | head -1
```

**If no recent backup exists:**
```bash
./scripts/backup-db.sh --docker
```

### 2. Backend Health Check
```bash
curl -s http://localhost:8000/health | jq .
# Expected: {"status":"healthy","database":"connected"}
```

### 3. Data Verification
```bash
# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r .access_token)

# Verify people exist
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/people?limit=5" | jq .total

# Verify rotation templates exist
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/rotation-templates" | jq 'length'
```

### 4. User Confirmation
Before proceeding, confirm with user:
> "Backup verified at [timestamp]. Proceed with schedule generation?"

## Backup Safety Rules

### Minimum Backup Policy
| Rule | Description |
|------|-------------|
| **Minimum 2 backups** | Never delete if only 2 remain |
| **Sacred backup** | First backup is protected, never auto-delete |
| **30-day retention** | Auto-cleanup requires user confirmation |
| **Pre-operation backup** | Always create before schedule modifications |

### Backup File Naming
```
residency_scheduler_YYYYMMDD_HHMMSS.sql.gz     # Regular backup
residency_scheduler_SACRED_20251223.sql.gz     # Protected baseline
residency_scheduler_pre-block-10_20260312.sql.gz  # Pre-operation marker
```

### Creating a Backup
```bash
# Standard backup (creates timestamped file, never overwrites)
./scripts/backup-db.sh --docker

# Verify
ls -la backups/postgres/ | tail -3
```

## Rollback Procedure

### Emergency Restore
If schedule generation fails or produces bad results:

```bash
# 1. Find the backup to restore
ls -la backups/postgres/*.sql.gz

# 2. Decompress (keeps original .gz)
gunzip -k backups/postgres/residency_scheduler_YYYYMMDD_HHMMSS.sql.gz

# 3. Restore to database
docker compose exec -T db psql -U scheduler -d residency_scheduler \
  < backups/postgres/residency_scheduler_YYYYMMDD_HHMMSS.sql

# 4. Verify restoration
docker compose exec db psql -U scheduler -d residency_scheduler \
  -c "SELECT COUNT(*) FROM assignments;"
```

### Partial Rollback (Specific Tables)
```bash
# Restore only assignments table
docker compose exec db psql -U scheduler -d residency_scheduler \
  -c "DELETE FROM assignments WHERE date BETWEEN '2026-03-12' AND '2026-04-08';"
# Then reimport from backup or regenerate
```

## Local Data Sources (PII - Never in Git)

If database needs complete reimport, source files are at:

| File | Location | Contents |
|------|----------|----------|
| Residents | `docs/data/airtable_residents.json` | Names, PGY levels |
| Faculty | `docs/data/airtable_faculty.json` | Names, roles |
| Resident Absences | `docs/data/airtable_resident_absences.json` | Leave, TDY |
| Faculty Absences | `docs/data/airtable_faculty_absences.json` | Time off |
| Rotations | `docs/data/airtable_rotation_templates.json` | Clinic definitions |
| Schedule | `docs/data/airtable_block_schedule.json` | Existing assignments |
| People CSV | `docs/data/people_import.csv` | Flat import format |

**CRITICAL:** These files contain real names. Never commit to repository.

---

## Examples

### Example 1: Generating Block 10 Schedule

**User Request:** "Generate the schedule for Block 10 (March 12 - April 8, 2026)"

**Claude Response:**

**Step 1: Pre-flight checks**
```
Running pre-flight checklist...
✅ Most recent backup: backups/postgres/residency_scheduler_20260312_083000.sql.gz (created 45 minutes ago)
✅ Backend health: {"status":"healthy","database":"connected"}
✅ Data verification: 25 people found, 8 rotation templates available
```

**Step 2: User confirmation**
> "Backup verified at 2026-03-12 08:30:00. Proceed with schedule generation for Block 10 (2026-03-12 to 2026-04-08)?"

**User:** "Yes, proceed"

**Step 3: Execute generation**
```bash
Calling generate_schedule API...
{
  "start_date": "2026-03-12",
  "end_date": "2026-04-08",
  "algorithm": "cp_sat",
  "timeout_seconds": 120
}
```

**Step 4: Report results**
```
✅ Schedule generated successfully
- Total blocks assigned: 1425 / 1456 (97.9% coverage)
- ACGME violations: 2 (minor)
- N-1 compliant: True
- Generation time: 47 seconds
```

### Example 2: Failed Generation Requiring Rollback

**User Request:** "Try generating the schedule again with stricter constraints"

**Claude Response:**

**Step 1: Create new backup before retry**
```bash
Creating pre-operation backup...
✅ Backup created: residency_scheduler_pre-retry_20260312_094500.sql.gz
```

**Step 2: Attempt generation**
```
Generating schedule with updated constraints...
❌ Generation failed: Solver timeout after 120s with no feasible solution
```

**Step 3: Check for partial data**
```sql
SELECT COUNT(*) FROM assignments WHERE date >= '2026-03-12';
-- Result: 234 assignments (partial data written)
```

**Step 4: Automatic rollback**
```bash
⚠️  Partial data detected. Rolling back to last backup...

Restoring from: residency_scheduler_pre-retry_20260312_094500.sql.gz
✅ Database restored successfully
✅ Verification: 0 assignments for target date range (clean state)
```

**Step 5: Recommendation**
> "Generation failed due to infeasible constraints. Recommend reviewing constraint weights before retry. Database rolled back to clean state."

### Example 3: Read-Only Validation (No Backup Required)

**User Request:** "Check if the current schedule has any ACGME violations"

**Claude Response:**

```
This is a read-only operation, no backup required.

Calling validate_schedule API...
```

**Results:**
```json
{
  "acgme_compliant": false,
  "violations": [
    {
      "type": "80_hour_rule",
      "resident_id": "RES-PGY1-03",
      "week": "2026-03-17",
      "hours": 82.5
    },
    {
      "type": "supervision_ratio",
      "date": "2026-03-22",
      "pgy1_residents": 3,
      "faculty": 1
    }
  ]
}
```

> "Found 2 ACGME violations. Recommend addressing these before deployment."

---

## Schedule Generation Workflow

### Via Direct API
```bash
# 1. Create backup (MANDATORY)
./scripts/backup-db.sh --docker

# 2. Get auth token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r .access_token)

# 3. Generate schedule
curl -X POST http://localhost:8000/api/v1/schedule/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2026-03-12",
    "end_date": "2026-04-08",
    "algorithm": "cp_sat",
    "timeout_seconds": 120
  }'
```

### Via MCP Tool
```
Tool: generate_schedule
Input: {
  start_date: "2026-03-12",
  end_date: "2026-04-08",
  algorithm: "cp_sat",
  timeout_seconds: 120
}
```

**MCP tools MUST verify backup before execution.**

## Protected vs Safe Operations

### Database-Modifying (Require Backup)
| Operation | MCP Tool | Risk Level |
|-----------|----------|------------|
| Generate schedule | `generate_schedule` | HIGH |
| Execute swap | `execute_swap` | MEDIUM |
| Bulk assign | `bulk_assign` | HIGH |
| Clear assignments | N/A | CRITICAL |

### Read-Only (Always Safe)
| Operation | MCP Tool | Risk Level |
|-----------|----------|------------|
| Validate schedule | `validate_schedule` | NONE |
| Detect conflicts | `detect_conflicts` | NONE |
| Get swap candidates | `analyze_swap_candidates` | NONE |
| Check health | `health_check` | NONE |

## Success Metrics

After schedule generation, verify:

| Metric | Target | How to Check |
|--------|--------|--------------|
| ACGME Violations | < 5 | `validation.total_violations` |
| Coverage Rate | > 80% | `total_blocks_assigned / total_blocks` |
| N-1 Compliant | True | `resilience.n1_compliant` |
| No Errors | True | HTTP 200 response |

## Failure Recovery

### If Generation Fails Mid-Process
1. Note the error message
2. Do NOT retry immediately
3. Check backend health
4. Restore from backup if partial data written
5. Investigate root cause

### If Generation Produces Bad Schedule
1. Review violations in response
2. If > 10 violations: restore and adjust constraints
3. If < 10 violations: manual adjustment may be faster

### If Backend Crashes
```bash
# Restart backend
docker compose restart backend

# Verify health
curl http://localhost:8000/health

# Check if data corrupted
docker compose exec db psql -U scheduler -d residency_scheduler \
  -c "SELECT COUNT(*) FROM people;"
```

## Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│           SAFE SCHEDULE GENERATION WORKFLOW                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STEP 1: Pre-Flight Safety Checks                                │
│  ┌────────────────────────────────────────────────┐             │
│  │ Check backend health (/health endpoint)        │             │
│  │ Verify data exists (people, rotation templates)│             │
│  │ Confirm auth working                           │             │
│  └────────────────────────────────────────────────┘             │
│                         ↓                                       │
│  STEP 2: Backup Verification (MANDATORY)                        │
│  ┌────────────────────────────────────────────────┐             │
│  │ Check for backup < 2 hours old                 │             │
│  │ If none exists: ./scripts/backup-db.sh --docker│             │
│  │ Verify backup file created successfully        │             │
│  │ ⚠️ NEVER proceed without verified backup       │             │
│  └────────────────────────────────────────────────┘             │
│                         ↓                                       │
│  STEP 3: User Confirmation                                      │
│  ┌────────────────────────────────────────────────┐             │
│  │ Show backup timestamp and database contents    │             │
│  │ Ask: "Proceed with schedule generation?"       │             │
│  │ Wait for explicit YES                          │             │
│  └────────────────────────────────────────────────┘             │
│                         ↓                                       │
│  STEP 4: Schedule Generation                                    │
│  ┌────────────────────────────────────────────────┐             │
│  │ Call API or MCP tool with parameters           │             │
│  │ Monitor progress (log streaming if available)  │             │
│  │ Capture result (success/failure)               │             │
│  └────────────────────────────────────────────────┘             │
│                         ↓                                       │
│  STEP 5: Result Validation                                      │
│  ┌────────────────────────────────────────────────┐             │
│  │ Check: ACGME violations < 5                    │             │
│  │ Check: Coverage rate > 80%                     │             │
│  │ Check: N-1 compliant (if resilience enabled)   │             │
│  │ If ANY fail → Offer rollback                   │             │
│  └────────────────────────────────────────────────┘             │
│                         ↓                                       │
│  STEP 6: Success or Rollback                                    │
│  ┌────────────────────────────────────────────────┐             │
│  │ Success: Report metrics, keep backup           │             │
│  │ Failure: Restore from backup, report error     │             │
│  └────────────────────────────────────────────────┘             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Concrete Usage Example: Generating Block 10 Schedule

See detailed walkthrough in skill documentation above showing complete safety check workflow.

## Failure Mode Handling

### Failure Mode 1: No Recent Backup

**Symptom:** No backup exists or last backup > 2 hours old

**Recovery:** Create new backup with `./scripts/backup-db.sh --docker` before proceeding

### Failure Mode 2: Generation Fails with Partial Data

**Symptom:** Error response with `partial_assignments` count > 0

**Recovery:** Offer rollback to user, restore from backup if confirmed

### Failure Mode 3: Excessive ACGME Violations

**Symptom:** `validation.acgme_violations >= 5`

**Recovery:** Automatic rollback offer, do not accept schedule

### Failure Mode 4: Backend Crash During Generation

**Symptom:** Connection refused or 500 errors

**Recovery:** Restart backend, check database integrity, rollback if needed

### Failure Mode 5: Backup Restoration Fails

**Symptom:** Duplicate key or constraint violations during restore

**Recovery:** Try clean restore (drop/recreate database), escalate if fails

## Integration with Other Skills

### With schedule-validator
Post-generation ACGME compliance check and coverage gap detection

### With resilience-dashboard
Burnout risk assessment and N-1/N-2 compliance verification

### With database-migration
Pre-migration backup creation and rollback capability

### With systematic-debugger
Investigation of repeated generation failures

## Validation Checklists

### Pre-Generation
- [ ] Backend health verified
- [ ] Data loaded (people, templates, absences)
- [ ] Backup exists and recent
- [ ] User confirmation obtained

### Success Validation
- [ ] HTTP 200 response
- [ ] ACGME violations < 5
- [ ] Coverage > 80%
- [ ] N-1 compliant (if enabled)

### Escalation
- [ ] Backup fails repeatedly
- [ ] ACGME violations > 10
- [ ] Database corruption
- [ ] Infeasible constraints

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│         SCHEDULE MODIFICATION DECISION TREE         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Does this modify the database?                     │
│     NO  → Safe to proceed                           │
│     YES → Continue checks                           │
│                                                     │
│  Is there a recent backup (< 2 hours)?              │
│     NO  → CREATE BACKUP FIRST                       │
│     YES → Continue                                  │
│                                                     │
│  Is backend healthy?                                │
│     NO  → FIX BACKEND FIRST                         │
│     YES → Continue                                  │
│                                                     │
│  Has user confirmed?                                │
│     NO  → ASK USER                                  │
│     YES → Proceed with operation                    │
│                                                     │
│  After operation:                                   │
│     Check violations < 5                            │
│     Verify coverage > 80%                           │
│     If failed → RESTORE FROM BACKUP                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

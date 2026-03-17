---
name: pm-stats
description: Generate quantitative statistics about the PM knowledge system — decision counts by type, health trajectory, sprint velocity, issue resolution rates, enforcement compliance. Dashboard view of system state. Triggers on "/pm-stats", "show statistics", "health report", "dashboard", "how are we doing".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.
Read `ops/config.yaml` for health metric sources.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: full dashboard
- If "health": health trajectory only
- If "decisions": decision system statistics only
- If "issues": issue lifecycle statistics only
- If "velocity": sprint velocity statistics only

**START NOW.**

---

## Philosophy

**What gets measured gets managed. What stays unmeasured stays invisible.**

The PM system tracks a project health trajectory (31/100 → target 65-70/100 across 5 sprints). But without quantitative statistics on the knowledge system itself — how many decisions exist, how many are stale, what percentage of issues get resolved — it is impossible to know if the PM system is working.

/pm-stats provides the dashboard. It is a read-only operation — no files are modified. It takes approximately 2-3 minutes to run across a large vault. The output should be reviewed at the start of sprint planning and at the end of retrospectives.

---

## Statistics to Compute

### 1. Decision System Statistics

```bash
# Total decisions by type
echo "=== Decision Counts by Type ==="
for type in architectural tech-fact enforcement issue sprint-record tension; do
  count=$(rg "^type: $type" decisions/ --include="*.md" -l 2>/dev/null | wc -l)
  echo "  $type: $count"
done

# Total decisions by status
echo "=== Decision Counts by Status ==="
for status in active superseded invalidated open in-progress resolved speculative; do
  count=$(rg "^status: $status" decisions/ --include="*.md" -l 2>/dev/null | wc -l)
  echo "  $status: $count"
done

# Total decisions by meta_state
echo "=== Decision Counts by meta_state ==="
for state in current outdated speculative; do
  count=$(rg "^meta_state: $state" decisions/ --include="*.md" -l 2>/dev/null | wc -l)
  echo "  $state: $count"
done
```

### 2. Issue Lifecycle Statistics

```bash
# Open issues
open=$(rg "^type: issue" decisions/ --include="*.md" -l | xargs -I{} sh -c 'rg "^status: open" "{}" && echo "{}"' 2>/dev/null | grep "decisions/" | wc -l)
# Resolved issues
resolved=$(rg "^type: issue" decisions/ --include="*.md" -l | xargs -I{} sh -c 'rg "^status: resolved" "{}" && echo "{}"' 2>/dev/null | grep "decisions/" | wc -l)

echo "Issue resolution rate: $resolved / $((open + resolved))"
```

### 3. Sprint Statistics

```bash
# Number of sprint records
sprint_count=$(rg "^type: sprint-record" decisions/ --include="*.md" -l 2>/dev/null | wc -l)

# Health trajectory — extract health_before and health_after from sprint records
rg "^health_before:|^health_after:" decisions/ --include="*.md" -h | sort
```

### 4. Enforcement Compliance Statistics

```bash
# Count sprint records with validation enforcement noted
rg "Was validation block embedded" decisions/ --include="*.md" -A 1 | rg "YES|NO"
```

### 5. Observation and Tension Backlog

```bash
# Observations by status
for status in pending promoted implemented archived; do
  count=$(rg "^status: $status" ops/observations/ --include="*.md" -l 2>/dev/null | wc -l)
  echo "  observations/$status: $count"
done

# Tensions by status
for status in pending resolved dissolved escalated; do
  count=$(rg "^status: $status" ops/tensions/ --include="*.md" -l 2>/dev/null | wc -l)
  echo "  tensions/$status: $count"
done
```

### 6. Vault Coverage

```bash
# Decisions per register
for reg in decisions/*-register.md decisions/index.md; do
  [ -f "$reg" ] && count=$(rg "\[\[" "$reg" 2>/dev/null | wc -l) && echo "$(basename $reg): $count refs"
done

# Orphan decisions (not referenced in any register)
total=$(ls decisions/*.md 2>/dev/null | grep -v "\-register\|index" | wc -l)
```

---

## Output Format

```
## PM System Dashboard — YYYY-MM-DD

### Decision System
Total decisions: N
By type:
  architectural: N
  tech-fact: N
  enforcement: N
  issue: N (open: N, resolved: N, in-progress: N)
  sprint-record: N
  tension: N

By meta_state:
  current: N (N%)
  outdated: N (N%)
  speculative: N (N%)

### Issue Lifecycle
Total issues tracked: N
  Open: N
  In-progress: N
  Resolved: N
Resolution rate: N%

### Sprint Velocity
Sprints documented: N
Health trajectory:
  Sprint 1: N → N (delta: +N)
  Sprint 2: N → N (delta: +N)
  ...
Current estimated health: N/100
Target: 65-70/100
Gap: N points

### Enforcement Compliance
Sprints with validation block: N/N (N%)
Sprints where deliverables rejected: N

### Observation/Tension Backlog
Observations: N pending / N total
Tensions: N pending / N total
Backlog status: [CLEAR / MODERATE / NEEDS RETROSPECT]

### Vault Coverage
Decision registers: N
  [[architecture-register]]: N decisions
  [[qftest-register]]: N decisions
  [[sprint-register]]: N decisions
  [[issue-register]]: N decisions
  [[enforcement-register]]: N decisions
Orphan decisions: N [WARN if > 0]

### System Health Assessment
[GREEN / YELLOW / RED] — [one sentence explanation]
Recommended action: [/pm-command]
```

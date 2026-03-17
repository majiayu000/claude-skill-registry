---
name: orchestrator
description: Coordinate all assimilation phases to scan a repo and generate skills. Use when assimilating a repository, running the full pipeline, or automating skill extraction.
metadata:
  phase: coordinator
  pipeline: assimilation
  version: 1.0.0
---

# Orchestrator

## Overview

Coordinate all phases of the assimilation pipeline in sequence, handling errors and producing a final summary. This is the meta-skill that runs everything.

---

## When to Use

Use this skill when:
- Assimilating a complete repository
- Running the full scan → extract → generate pipeline
- Automating skill extraction from a codebase
- User says "assimilate this repo"

---

## Pipeline Flow

```
User: "assimilate this repo"
         │
         ▼
    ┌─────────────────┐
    │  ORCHESTRATOR   │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Phase 1: SCAN  │ → scan-report.json
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Phase 2: EXTRACT│ → patterns.json
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Phase 3: GENERATE│ → SKILL.md files
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Phase 4: UPDATE │ → AGENTS.md section
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Phase 5: CLEANUP│ → Remove temp files
    └────────┬────────┘
             │
         ▼
    📊 Summary Report
```

---

## Execution Steps

### Step 0: Setup

```bash
# Create temp directory
mkdir -p .github/temp

# Record start time
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
```

### Step 1: Phase 1 — Scan Repository

**Invoke:** `assimilation/repo-scanner` skill

```markdown
Using repo-scanner skill:
- Apply ignore patterns
- Detect language and framework
- Identify domains and entry points
- Generate scan-report.json
```

**Verify output:**
```bash
if [ ! -f ".github/temp/scan-report.json" ]; then
    echo "❌ FAIL: Phase 1 did not produce scan-report.json"
    exit 1
fi

# Check for error
if grep -q '"error": true' .github/temp/scan-report.json; then
    echo "❌ FAIL: Scan reported error"
    cat .github/temp/scan-report.json
    exit 1
fi
```

**Report progress:**
```
✅ Phase 1 complete: Repository scanned
   Language: <from-report>
   Framework: <from-report>
   Domains: <count>
```

### Step 2: Phase 2 — Extract Patterns

**Invoke:** `assimilation/pattern-extractor` skill

```markdown
Using pattern-extractor skill:
- Run semantic grep for each category
- Analyze key files
- Calculate confidence scores
- Generate patterns.json
```

**Verify output:**
```bash
if [ ! -f ".github/temp/patterns.json" ]; then
    echo "❌ FAIL: Phase 2 did not produce patterns.json"
    exit 1
fi

# Check pattern count
PATTERN_COUNT=$(grep -c '"name":' .github/temp/patterns.json || echo "0")
if [ "$PATTERN_COUNT" -eq 0 ]; then
    echo "⚠️ WARNING: No patterns found"
fi
```

**Report progress:**
```
✅ Phase 2 complete: Patterns extracted
   Patterns found: <count>
   Categories: arch(<n>), rel(<n>), qual(<n>), sec(<n>), conv(<n>)
```

### Step 3: Phase 3 — Generate Skills

**Invoke:** `assimilation/skill-generator` skill

```markdown
Using skill-generator skill:
- Apply regularization (thresholds, abstraction, dedup)
- Generate SKILL.md for each passing pattern
- Write to both .github/skills/ and .claude/skills/
```

**Verify output:**
```bash
# Count generated skills
SKILL_COUNT=$(find .github/skills -name "SKILL.md" 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -eq 0 ]; then
    echo "⚠️ WARNING: No skills generated (all patterns filtered)"
fi
```

**Report progress:**
```
✅ Phase 3 complete: Skills generated
   Skills created: <count>
   Validated: <count>
   Experimental: <count>
```

### Step 4: Phase 4 — Update AGENTS.md (Optional)

If skills were generated, append a section to AGENTS.md:

**Check if AGENTS.md exists:**
```bash
if [ -f "AGENTS.md" ]; then
    # Append section
    echo "Updating AGENTS.md with generated skills..."
else
    # Create minimal AGENTS.md
    echo "Creating AGENTS.md with generated skills..."
fi
```

**Section to add:**

```markdown

---

## Generated Skills

The following skills were auto-generated from repository analysis on <date>:

### Architecture
| Skill | Use When | Status |
|-------|----------|--------|
| [<name>](.github/skills/architecture/<name>/SKILL.md) | <description-excerpt> | <status> |

### Reliability
| Skill | Use When | Status |
|-------|----------|--------|
| [<name>](.github/skills/reliability/<name>/SKILL.md) | <description-excerpt> | <status> |

### Quality
| Skill | Use When | Status |
|-------|----------|--------|
| [<name>](.github/skills/quality/<name>/SKILL.md) | <description-excerpt> | <status> |

> Skills marked as `experimental` may need human review.
```

### Step 5: Phase 5 — Cleanup

```bash
# Remove temp files
rm -rf .github/temp

# Verify cleanup
if [ -d ".github/temp" ]; then
    echo "⚠️ WARNING: Temp directory not fully removed"
fi
```

### Step 6: Update Usage Tracking (Append-Only)

If this is not the first assimilation, append to usage tracking:

```bash
# .github/skills-usage.json
# Only orchestrator writes to this file
```

```json
{
  "assimilations": [
    {
      "repo": "<repo-name>",
      "timestamp": "<ISO-timestamp>",
      "skills_generated": <count>,
      "patterns_found": <count>,
      "patterns_filtered": <count>
    }
  ]
}
```

### Step 7: Generate Final Summary

```
════════════════════════════════════════════════════════
✅ ASSIMILATION COMPLETE
════════════════════════════════════════════════════════

Repository: <name>
Language: <language>
Framework: <framework>

Pipeline Results:
  Phase 1 (Scan):     ✅ <domains> domains found
  Phase 2 (Extract):  ✅ <patterns> patterns found
  Phase 3 (Generate): ✅ <skills> skills created
  Phase 4 (Update):   ✅ AGENTS.md updated
  Phase 5 (Cleanup):  ✅ Temp files removed

Generated Skills by Category:
  architecture/   <count> skills
  reliability/    <count> skills
  quality/        <count> skills
  security/       <count> skills
  conventions/    <count> skills

Skill Locations:
  .github/skills/<category>/<pattern>/SKILL.md
  .claude/skills/<category>/<pattern>/SKILL.md

⚠️  Experimental Skills (need review):
  - <skill-name> (confidence: 0.XX)
  - <skill-name> (confidence: 0.XX)

Next Steps:
  1. Review experimental skills
  2. Test a skill: "Use the <skill-name> skill to..."
  3. Edit skills as needed

════════════════════════════════════════════════════════
```

---

## Error Handling

### Fail Fast Policy

If any phase fails, stop immediately:

```
❌ ASSIMILATION FAILED

Failed at: Phase <N> (<phase-name>)
Error: <error-message>

Partial outputs preserved in .github/temp/ for debugging.

To resume:
  1. Fix the issue
  2. Re-run orchestrator

To cleanup:
  rm -rf .github/temp
```

### Error Conditions

| Phase | Condition | Action |
|-------|-----------|--------|
| 1 | Empty directory | FAIL immediately |
| 1 | No config files | WARN, continue with extension-based detection |
| 2 | No patterns found | WARN, continue with empty output |
| 3 | All patterns filtered | WARN, produce no skills |
| 4 | AGENTS.md locked | WARN, skip update |
| 5 | Cannot delete temp | WARN, continue |

---

## Subagent Invocation Pattern

The orchestrator invokes each phase skill using the subagent pattern:

```markdown
For Phase 1:
"Using the repo-scanner skill, scan this repository and produce scan-report.json"

For Phase 2:
"Using the pattern-extractor skill, analyze the scan results and extract patterns"

For Phase 3:
"Using the skill-generator skill, generate SKILL.md files from the patterns"
```

Each subagent:
1. Reads required input files
2. Performs its phase
3. Writes output files
4. Reports completion

---

## Conventions

✅ **Do:**
- Execute phases in strict order
- Fail fast on critical errors
- Clean up temp files on success
- Report progress after each phase
- Preserve temp on failure for debugging

❌ **Don't:**
- Skip phases or run out of order
- Continue after critical failure
- Leave temp files on success
- Generate skills directly (delegate to skill-generator)
- Write to skills-usage.json from anywhere except orchestrator

---

## Related Skills

- [repo-scanner](../repo-scanner/SKILL.md) — Phase 1: Scan repository structure
- [pattern-extractor](../pattern-extractor/SKILL.md) — Phase 2: Extract patterns
- [skill-generator](../skill-generator/SKILL.md) — Phase 3: Generate skills

---
name: audit-process
description:
  Run a comprehensive multi-stage automation audit with parallel agents
---

# Comprehensive Automation Audit

**Version:** 2.2 (Recovery Safeguards - Session #122)

This audit covers **16 automation types** across **12 audit categories** using a
**7-stage approach** with parallel agent execution.

---

## Quick Reference

| Stage | Name                          | Parallel Agents | Output                        |
| ----- | ----------------------------- | --------------- | ----------------------------- |
| 1     | Inventory & Dependency Map    | 6               | `stage-1-inventory.md`        |
| 2     | Redundancy & Dead Code        | 3               | `stage-2-redundancy.jsonl`    |
| 3     | Effectiveness & Functionality | 4               | `stage-3-effectiveness.jsonl` |
| 4     | Performance & Bloat           | 3               | `stage-4-performance.jsonl`   |
| 5     | Quality & Consistency         | 3               | `stage-5-quality.jsonl`       |
| 6     | Coverage Gaps & Improvements  | 3               | `stage-6-improvements.jsonl`  |
| 7     | Synthesis & Prioritization    | 1 (sequential)  | Final report + action plan    |

**Total: 22 parallel agents across 6 stages + 1 synthesis stage**

---

## CRITICAL: Persistence Rules

**EVERY agent MUST write outputs directly to files. NEVER rely on conversation
context.**

1. **Agent outputs go to files, not conversation**
   - Each agent prompt MUST include:
     `Write findings to: ${AUDIT_DIR}/[filename].jsonl`
   - Agents must use Write tool or Bash to create files
   - If agent returns text instead of writing file, RE-RUN with explicit file
     instruction

2. **Verify after each stage**
   - After parallel agents complete, verify all output files exist
   - Check file sizes are non-zero: `wc -l ${AUDIT_DIR}/*.jsonl`
   - If any file missing, do NOT proceed to next stage

3. **Why this matters**
   - Context compaction is EXPECTED and can happen at any time
   - Conversation text is ephemeral; only files persist
   - 150+ findings lost to compaction = real cost to user

---

## Scope: 16 Automation Types

| #   | Type                     | Location                    | Count    |
| --- | ------------------------ | --------------------------- | -------- |
| 1   | Claude Code Hooks        | `.claude/hooks/`            | ~29      |
| 2   | Claude Code Skills       | `.claude/skills/`           | ~49      |
| 3   | Claude Code Commands     | `.claude/commands/`         | ~12      |
| 4   | npm Scripts              | `package.json`              | ~60      |
| 5   | Standalone Scripts       | `scripts/`                  | ~61      |
| 6   | Script Libraries         | `scripts/lib/`              | ~4       |
| 7   | GitHub Actions Workflows | `.github/workflows/`        | ~10      |
| 8   | Git Hooks (Husky)        | `.husky/`                   | 2        |
| 9   | lint-staged              | `package.json`              | 1 config |
| 10  | ESLint                   | `eslint.config.mjs`         | 1 config |
| 11  | Prettier                 | `.prettierrc`               | 1 config |
| 12  | Firebase Cloud Functions | `functions/src/`            | ~8       |
| 13  | Firebase Scheduled Jobs  | `functions/src/jobs.ts`     | ~3+      |
| 14  | Firebase Rules           | `*.rules`                   | 2        |
| 15  | MCP Servers              | `mcp.json` / `scripts/mcp/` | ~6       |
| 16  | TypeScript Configs       | `tsconfig*.json`            | 2+       |

---

## Audit Categories: 12 Dimensions

| #   | Category                 | Focus                           |
| --- | ------------------------ | ------------------------------- |
| 1   | Redundancy & Duplication | Same thing in multiple places   |
| 2   | Dead/Orphaned Code       | Never called, does nothing      |
| 3   | Effectiveness            | Too weak, always passes         |
| 4   | Performance & Bloat      | Slow, unnecessary work          |
| 5   | Error Handling           | Silent failures, wrong severity |
| 6   | Dependency & Call Chain  | What triggers what              |
| 7   | Consistency              | Mixed patterns, naming          |
| 8   | Coverage Gaps            | Missing checks                  |
| 9   | Maintainability          | Complex, undocumented           |
| 10  | Functionality            | Does it actually work?          |
| 11  | Improvements             | Could be better                 |
| 12  | Code Quality             | Bugs, security, bad patterns    |

---

## Pre-Audit Setup

### Step 0: Episodic Memory Search (Session #128)

Before running process/automation audit, search for context from past sessions:

```javascript
// Search for past automation audit findings
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["process audit", "automation", "hooks"],
    limit: 5,
  });

// Search for specific workflow discussions
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["GitHub Actions", "npm scripts", "redundant"],
    limit: 5,
  });
```

**Why this matters:**

- Compare against previous automation inventory
- Identify recurring issues (dead scripts, redundancy)
- Track which automations were flagged for removal
- Prevent re-flagging intentional design decisions

---

### Step 1: Check Thresholds

```bash
npm run review:check
```

- If no thresholds triggered: "No review thresholds triggered. Proceed anyway?"
- Continue regardless if user invoked intentionally

### Step 2: Create Audit Directory

```bash
AUDIT_DATE=$(date +%Y-%m-%d)
AUDIT_DIR="docs/audits/single-session/process/audit-${AUDIT_DATE}"
mkdir -p "${AUDIT_DIR}"
```

### Step 2.5: Verify Output Directory Variable (CRITICAL)

Before running ANY agent, verify AUDIT_DIR is set correctly:

```bash
echo "AUDIT_DIR is: ${AUDIT_DIR}"
ls -la "${AUDIT_DIR}" || echo "ERROR: AUDIT_DIR does not exist"

# FAIL if path is root directory - use realpath to prevent symlink/relative bypasses
AUDIT_PATH=$(realpath "${AUDIT_DIR}" 2>/dev/null || echo "${AUDIT_DIR}")
REPO_ROOT=$(realpath "." 2>/dev/null || echo ".")
if [ -z "${AUDIT_DIR}" ] || [ "${AUDIT_PATH}" = "/" ] || [ "${AUDIT_PATH}" = "${REPO_ROOT}" ]; then
  echo "FATAL: AUDIT_DIR must be a proper subdirectory under the repo, not root"
  exit 1
fi
```

**Why this matters:** Context compaction can cause AUDIT_DIR variable to be
lost, resulting in agents writing to the root directory instead of the audit
folder.

### Step 3: Load False Positives

Read `docs/audits/FALSE_POSITIVES.jsonl` and note patterns to exclude.

---

## Stage 1: Inventory & Dependency Mapping

**Goal:** Build complete map of all 16 automation types and their relationships.

**Run 6 agents IN PARALLEL using Task tool:**

### Agent 1A: Hooks Inventory

```
Task(subagent_type="Explore", prompt="""
Inventory all hooks in this codebase:

1. Claude hooks in .claude/hooks/ - list each file, what event it handles
2. Husky hooks in .husky/ - list each file, what it does
3. lint-staged config in package.json - what it runs

For each hook, document:
- File path
- Trigger event (SessionStart, PostToolUse, pre-commit, etc.)
- What it calls/executes
- Dependencies on other scripts

CRITICAL: You MUST write your findings directly to this file:
  ${AUDIT_DIR}/stage-1a-hooks.md

Use the Write tool to create this file. Do NOT return findings as text.
Verify the file exists after writing.
""")
```

### Agent 1B: Scripts Inventory

```
Task(subagent_type="Explore", prompt="""
Inventory all scripts:

1. scripts/*.js and scripts/*.ts - list each with one-line description
2. scripts/lib/ - shared utilities
3. npm scripts in package.json - list each with what it runs

For each script, document:
- File path
- Purpose (from comments or code analysis)
- What calls it (npm script, hook, CI, manual)
- What it calls (other scripts, external commands)

CRITICAL: You MUST write your findings directly to this file:
  ${AUDIT_DIR}/stage-1b-scripts.md

Use the Write tool to create this file. Do NOT return findings as text.
Verify the file exists after writing.
""")
```

### Agent 1C: Skills & Commands Inventory

```
Task(subagent_type="Explore", prompt="""
Inventory all Claude skills and commands:

1. .claude/skills/ - each subdirectory is a skill
2. .claude/commands/ - each .md file is a command

For each skill/command, document:
- Name
- Description (from SKILL.md or file header)
- Scripts it uses (if any)
- Dependencies

CRITICAL: You MUST write your findings directly to this file:
  ${AUDIT_DIR}/stage-1c-skills.md

Use the Write tool to create this file. Do NOT return findings as text.
Verify the file exists after writing.
""")
```

### Agent 1D: CI & Config Inventory

```
Task(subagent_type="Explore", prompt="""
Inventory CI and config:

1. .github/workflows/ - each YAML workflow
2. eslint.config.mjs - what rules/plugins
3. .prettierrc - configuration
4. tsconfig*.json - all TypeScript configs

For each, document:
- File path
- Purpose
- Triggers (for workflows)
- What it validates/enforces

CRITICAL: You MUST write your findings directly to this file:
  ${AUDIT_DIR}/stage-1d-ci-config.md

Use the Write tool to create this file. Do NOT return findings as text.
Verify the file exists after writing.
""")
```

### Agent 1E: Firebase Inventory

```
Task(subagent_type="Explore", prompt="""
Inventory Firebase automation:

1. functions/src/*.ts - Cloud Functions (callable and scheduled)
2. functions/src/jobs.ts - Scheduled jobs specifically
3. firestore.rules - Security rules
4. storage.rules - Storage security rules
5. firestore.indexes.json - Indexes

For each function, document:
- Name
- Type (callable, scheduled, trigger)
- Schedule (if applicable)
- What it does

CRITICAL: You MUST write your findings directly to this file:
  ${AUDIT_DIR}/stage-1e-firebase.md

Use the Write tool to create this file. Do NOT return findings as text.
Verify the file exists after writing.
""")
```

### Agent 1F: MCP Servers Inventory

```
Task(subagent_type="Explore", prompt="""
Inventory MCP servers:

1. Check mcp.json.example for configured servers
2. Check scripts/mcp/ for custom MCP implementations
3. Check .claude/settings.json for enabled/disabled servers

For each server, document:
- Name
- Source (npm package or local script)
- Purpose
- Status (enabled/disabled)

CRITICAL: You MUST write your findings directly to this file:
  ${AUDIT_DIR}/stage-1f-mcp.md

Use the Write tool to create this file. Do NOT return findings as text.
Verify the file exists after writing.
""")
```

### Stage 1 Output

After all 6 agents complete:

1. Merge results into `stage-1-inventory.md`
2. Build dependency graph showing what calls what
3. Identify orphans (things nothing calls)
4. **No JSONL findings yet** - this is discovery only

### Stage 1 Verification (MANDATORY)

Before proceeding to Stage 2:

```bash
# Check for misplaced files in root (context compaction recovery)
ROOT_AUDIT_FILES=$(ls *.jsonl *.md 2>/dev/null | grep -E "(stage-|AUDIT|audit-)" | wc -l)
if [ "$ROOT_AUDIT_FILES" -gt 0 ]; then
  echo "WARNING: Found audit files in root directory!"
  echo "Moving to ${AUDIT_DIR}..."
  mv stage-*.md "${AUDIT_DIR}/" 2>/dev/null || true
  mv stage-*.jsonl "${AUDIT_DIR}/" 2>/dev/null || true
  mv AUDIT*.txt AUDIT*.md "${AUDIT_DIR}/" 2>/dev/null || true
fi

# Verify all stage 1 files exist and have content
STAGE1_FILES="stage-1a-hooks.md stage-1b-scripts.md stage-1c-skills.md stage-1d-ci-config.md stage-1e-firebase.md stage-1f-mcp.md"
for f in $STAGE1_FILES; do
  if [ ! -s "${AUDIT_DIR}/$f" ]; then
    echo "ERROR: Missing or empty: ${AUDIT_DIR}/$f"
    echo "Re-run the failed agent before continuing"
    exit 1
  fi
done
echo "Stage 1 verified - all inventory files present"
ls -la ${AUDIT_DIR}/stage-1*.md
```

---

## Stage 2: Redundancy & Dead Code Analysis

**Goal:** Find duplications and orphaned code.

**Run 3 agents IN PARALLEL:**

### Agent 2A: Orphan Detection

```
Task(subagent_type="Explore", prompt="""
Using the Stage 1 inventory, find orphaned automation:

1. Scripts never called by npm scripts, hooks, CI, or other scripts
2. npm scripts never used in hooks, CI, or documentation
3. Skills/commands that duplicate built-in functionality
4. GitHub Actions that never trigger (impossible conditions)
5. Firebase functions not referenced anywhere

Cross-reference the dependency graph from Stage 1.

For each orphan found, create a JSONL entry (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "process",
  "title": "Orphaned: [name]",
  "fingerprint": "process::path/to/file::orphaned-name",
  "severity": "S2",
  "effort": "E1",
  "confidence": 90,
  "files": ["path/to/file:1"],
  "why_it_matters": "Orphaned code increases maintenance burden and confusion",
  "suggested_fix": "Remove if unused, or document intended use",
  "acceptance_tests": ["Verify no callers exist", "Remove and confirm no breakage"]
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-2a-orphans.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 2B: Duplication Detection

```
Task(subagent_type="Explore", prompt="""
Find duplicated logic across automation:

1. Same validation running in pre-commit AND CI (unnecessary duplication)
2. Same check in multiple hooks
3. Scripts that do the same thing with different names
4. Pattern checks duplicated between hook and script
5. Similar error handling code copy-pasted

For each duplication found, create a JSONL entry (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "process",
  "title": "Duplicated: [description]",
  "fingerprint": "process::path/to/file::duplicated-logic-name",
  "severity": "S2",
  "effort": "E1",
  "confidence": 85,
  "files": ["path/to/file:123", "other/location:456"],
  "why_it_matters": "Duplicated logic leads to inconsistent behavior and double maintenance",
  "suggested_fix": "Consolidate into single source, call from both places",
  "acceptance_tests": ["Single source of truth exists", "Both callers use shared implementation"]
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-2b-duplications.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 2C: Unused & Never-Triggered

```
Task(subagent_type="Explore", prompt="""
Find automation that never executes:

1. npm scripts with no callers and not in documentation
2. GitHub Actions with triggers that never fire
3. Hooks configured but for events that don't occur
4. Firebase scheduled jobs that are disabled
5. Dead code paths in scripts (unreachable conditions)

For each finding, create a JSONL entry (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "process",
  "title": "Never executes: [name]",
  "fingerprint": "process::path/to/file::never-executes-name",
  "severity": "S3",
  "effort": "E0",
  "confidence": 80,
  "files": ["path/to/file:1"],
  "why_it_matters": "Dead automation clutters codebase and misleads developers",
  "suggested_fix": "Remove or fix trigger condition",
  "acceptance_tests": ["Removed from codebase", "OR trigger condition now fires correctly"]
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-2c-unused.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Stage 2 Verification (MANDATORY)

Before proceeding to Stage 3:

```bash
# Check for misplaced files in root (context compaction recovery)
ROOT_AUDIT_FILES=$(ls *.jsonl 2>/dev/null | grep -E "stage-2" | wc -l)
if [ "$ROOT_AUDIT_FILES" -gt 0 ]; then
  echo "WARNING: Found stage-2 files in root directory!"
  mv stage-2*.jsonl "${AUDIT_DIR}/" 2>/dev/null || true
fi

# Verify all stage 2 files exist and have content
STAGE2_FILES="stage-2a-orphans.jsonl stage-2b-duplications.jsonl stage-2c-unused.jsonl"
for f in $STAGE2_FILES; do
  if [ ! -s "${AUDIT_DIR}/$f" ]; then
    echo "ERROR: Missing or empty: ${AUDIT_DIR}/$f"
    echo "Re-run the failed agent before continuing"
    exit 1
  fi
done
echo "Stage 2 verified:"
wc -l ${AUDIT_DIR}/stage-2*.jsonl
```

### Stage 2 Output

1. Merge agent outputs into `stage-2-redundancy.jsonl`:
   ```bash
   # Use explicit filenames to avoid self-overwriting on re-runs
   cat ${AUDIT_DIR}/stage-2a-orphans.jsonl \
       ${AUDIT_DIR}/stage-2b-duplications.jsonl \
       ${AUDIT_DIR}/stage-2c-unused.jsonl > ${AUDIT_DIR}/stage-2-redundancy.jsonl
   ```
2. Run TDMS intake:
   ```bash
   node scripts/debt/intake-audit.js ${AUDIT_DIR}/stage-2-redundancy.jsonl
   ```

---

## Stage 3: Effectiveness & Functionality

**Goal:** Does each thing actually work and catch issues?

**Run 4 agents IN PARALLEL:**

### Agent 3A: Hook Effectiveness

```
Task(subagent_type="code-reviewer", prompt="""
Analyze hook effectiveness:

1. Do pre-commit hooks actually catch the issues they're designed for?
2. Are there bypass conditions that are too easy to trigger?
3. Do Claude hooks provide useful feedback or just noise?
4. Are hook error messages actionable?

Test methodology:
- Read hook code and identify what it checks
- Determine if checks are robust or easily bypassed
- Check if error messages help developers fix issues

For each ineffective hook, create a JSONL entry with severity S1-S2.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-3a-hook-effectiveness.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 3B: CI Workflow Effectiveness

```
Task(subagent_type="code-reviewer", prompt="""
Analyze CI workflow effectiveness:

1. Do workflows actually catch failures before merge?
2. Are there race conditions or timing issues?
3. Do workflows test the right things?
4. Are there gaps where bad code could slip through?

For each workflow, verify:
- Triggers are appropriate
- Steps actually validate what they claim
- Failure modes are handled

For each issue, create a JSONL entry with severity S0-S2.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-3b-ci-effectiveness.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 3C: Script Functionality

```
Task(subagent_type="code-reviewer", prompt="""
Verify script functionality:

1. Do scripts handle edge cases (empty input, missing files)?
2. Do scripts fail gracefully with useful errors?
3. Are there scripts that silently do nothing?
4. Do scripts actually accomplish their stated purpose?

For high-complexity scripts (check MASTER_DEBT.jsonl for complexity findings),
pay extra attention to logic correctness.

For each issue, create a JSONL entry with severity S1-S3.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-3c-script-functionality.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 3D: Skill/Command Functionality

```
Task(subagent_type="code-reviewer", prompt="""
Verify skill and command functionality:

1. Do skill prompts actually guide Claude effectively?
2. Are there skills that produce poor/wrong outputs?
3. Do commands reference files that don't exist?
4. Are skill dependencies satisfied?

For each issue, create a JSONL entry with severity S2-S3.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-3d-skill-functionality.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Stage 3 Verification (MANDATORY)

Before proceeding to Stage 4:

```bash
# Check for misplaced files in root (context compaction recovery)
ROOT_AUDIT_FILES=$(ls *.jsonl 2>/dev/null | grep -E "stage-3|ci-workflow|skill-audit|audit-findings" | wc -l)
if [ "$ROOT_AUDIT_FILES" -gt 0 ]; then
  echo "WARNING: Found stage-3 files in root directory!"
  mv stage-3*.jsonl ci-workflow*.jsonl skill-audit*.jsonl audit-findings*.jsonl "${AUDIT_DIR}/" 2>/dev/null || true
fi

# Verify all stage 3 files exist and have content
STAGE3_FILES="stage-3a-hook-effectiveness.jsonl stage-3b-ci-effectiveness.jsonl stage-3c-script-functionality.jsonl stage-3d-skill-functionality.jsonl"
for f in $STAGE3_FILES; do
  if [ ! -s "${AUDIT_DIR}/$f" ]; then
    echo "ERROR: Missing or empty: ${AUDIT_DIR}/$f"
    echo "Re-run the failed agent before continuing"
    exit 1
  fi
done
echo "Stage 3 verified:"
wc -l ${AUDIT_DIR}/stage-3*.jsonl
```

### Stage 3 Output

1. Merge agent outputs into `stage-3-effectiveness.jsonl`:
   ```bash
   # Use explicit filenames to avoid self-overwriting on re-runs
   cat ${AUDIT_DIR}/stage-3a-hook-effectiveness.jsonl \
       ${AUDIT_DIR}/stage-3b-ci-effectiveness.jsonl \
       ${AUDIT_DIR}/stage-3c-script-functionality.jsonl \
       ${AUDIT_DIR}/stage-3d-skill-functionality.jsonl > ${AUDIT_DIR}/stage-3-effectiveness.jsonl
   ```
2. Run TDMS intake:
   ```bash
   node scripts/debt/intake-audit.js ${AUDIT_DIR}/stage-3-effectiveness.jsonl
   ```

---

## Stage 4: Performance & Bloat

**Goal:** Identify slow operations and unnecessary work.

**Run 3 agents IN PARALLEL:**

### Agent 4A: Git Hook Performance

```
Task(subagent_type="Explore", prompt="""
Analyze pre-commit and pre-push performance:

1. What's the total time for pre-commit? (should be <10s for good DX)
2. Which checks are slowest?
3. Are there checks that could run in parallel but don't?
4. Are there checks that could be skipped for certain file types?
5. Is there unnecessary work (full scans when partial would do)?

For each performance issue, create a JSONL entry (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "process",
  "title": "Slow: [check name]",
  "fingerprint": "process::.husky/pre-commit::slow-check-name",
  "severity": "S2",
  "effort": "E1",
  "confidence": 85,
  "files": [".husky/pre-commit:[line]"],
  "why_it_matters": "Slow hooks degrade developer experience and encourage bypassing",
  "suggested_fix": "[specific optimization]",
  "acceptance_tests": ["Hook completes in <[Y]s", "No functionality lost"]
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-4a-hook-performance.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 4B: CI Performance

```
Task(subagent_type="Explore", prompt="""
Analyze CI workflow performance:

1. Which jobs take longest?
2. Are there jobs that could run in parallel?
3. Is caching used effectively?
4. Are there redundant installs or builds?
5. Could any jobs be skipped based on changed files?

For each issue, create a JSONL entry with severity S2-S3.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-4b-ci-performance.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 4C: Script Performance

```
Task(subagent_type="code-reviewer", prompt="""
Analyze script performance:

1. Scripts that scan all files when they could be selective
2. Synchronous operations that could be async
3. Repeated file reads that could be cached
4. O(n^2) or worse algorithms
5. Spawning too many child processes

Focus on scripts in the critical path (hooks, CI).

For each issue, create a JSONL entry with severity S2-S3.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-4c-script-performance.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Stage 4 Verification (MANDATORY)

Before proceeding to Stage 5:

```bash
# Check for misplaced files in root (context compaction recovery)
ROOT_AUDIT_FILES=$(ls *.jsonl 2>/dev/null | grep -E "stage-4" | wc -l)
if [ "$ROOT_AUDIT_FILES" -gt 0 ]; then
  echo "WARNING: Found stage-4 files in root directory!"
  mv stage-4*.jsonl "${AUDIT_DIR}/" 2>/dev/null || true
fi

# Verify all stage 4 files exist and have content
STAGE4_FILES="stage-4a-hook-performance.jsonl stage-4b-ci-performance.jsonl stage-4c-script-performance.jsonl"
for f in $STAGE4_FILES; do
  if [ ! -s "${AUDIT_DIR}/$f" ]; then
    echo "ERROR: Missing or empty: ${AUDIT_DIR}/$f"
    echo "Re-run the failed agent before continuing"
    exit 1
  fi
done
echo "Stage 4 verified:"
wc -l ${AUDIT_DIR}/stage-4*.jsonl
```

### Stage 4 Output

1. Merge agent outputs into `stage-4-performance.jsonl`:
   ```bash
   # Use explicit filenames to avoid self-overwriting on re-runs
   cat ${AUDIT_DIR}/stage-4a-hook-performance.jsonl \
       ${AUDIT_DIR}/stage-4b-ci-performance.jsonl \
       ${AUDIT_DIR}/stage-4c-script-performance.jsonl > ${AUDIT_DIR}/stage-4-performance.jsonl
   ```
2. Run TDMS intake:
   ```bash
   node scripts/debt/intake-audit.js ${AUDIT_DIR}/stage-4-performance.jsonl
   ```

---

## Stage 5: Quality & Consistency

**Goal:** Error handling, code quality, pattern consistency.

**Run 3 agents IN PARALLEL:**

### Agent 5A: Error Handling Audit

```
Task(subagent_type="code-reviewer", prompt="""
Audit error handling in automation:

1. Silent failures (catch blocks that swallow errors)
2. Missing try/catch around file operations
3. Incorrect exit codes (0 on failure, non-zero on success)
4. continueOnError overuse in hooks
5. Missing error messages or unhelpful ones

For each issue, create a JSONL entry:
{
  "severity": "S1" for silent failures that hide real problems,
  "severity": "S2" for poor error messages
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-5a-error-handling.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 5B: Code Quality Audit

```
Task(subagent_type="code-reviewer", prompt="""
Audit code quality in scripts and hooks:

1. Security issues (command injection, path traversal)
2. Race conditions (TOCTOU)
3. Hardcoded paths that should be configurable
4. Magic numbers/strings without explanation
5. Missing input validation

Use patterns from docs/agent_docs/CODE_PATTERNS.md as reference.

For each issue, create a JSONL entry with appropriate severity.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-5b-code-quality.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 5C: Consistency Audit

```
Task(subagent_type="Explore", prompt="""
Audit consistency across automation:

1. Mixed JS and shell doing the same thing differently
2. Inconsistent naming (kebab-case vs camelCase vs snake_case)
3. Different error message formats
4. Some async, some sync for similar operations
5. Different logging approaches

For each inconsistency, create a JSONL entry with severity S3.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-5c-consistency.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Stage 5 Verification (MANDATORY)

Before proceeding to Stage 6:

```bash
# Check for misplaced files in root (context compaction recovery)
ROOT_AUDIT_FILES=$(ls *.jsonl 2>/dev/null | grep -E "stage-5|AUDIT_ERROR|ERROR_HANDLING" | wc -l)
if [ "$ROOT_AUDIT_FILES" -gt 0 ]; then
  echo "WARNING: Found stage-5 files in root directory!"
  mv stage-5*.jsonl AUDIT_ERROR*.jsonl "${AUDIT_DIR}/" 2>/dev/null || true
fi

# Verify all stage 5 files exist and have content
STAGE5_FILES="stage-5a-error-handling.jsonl stage-5b-code-quality.jsonl stage-5c-consistency.jsonl"
for f in $STAGE5_FILES; do
  if [ ! -s "${AUDIT_DIR}/$f" ]; then
    echo "ERROR: Missing or empty: ${AUDIT_DIR}/$f"
    echo "Re-run the failed agent before continuing"
    exit 1
  fi
done
echo "Stage 5 verified:"
wc -l ${AUDIT_DIR}/stage-5*.jsonl
```

### Stage 5 Output

1. Merge agent outputs into `stage-5-quality.jsonl`:
   ```bash
   # Use explicit file list to avoid glob self-inclusion
   cat "${AUDIT_DIR}/stage-5a-error-handling.jsonl" \
       "${AUDIT_DIR}/stage-5b-code-quality.jsonl" \
       "${AUDIT_DIR}/stage-5c-consistency.jsonl" \
       > "${AUDIT_DIR}/stage-5-quality.jsonl"
   ```
2. Run TDMS intake:
   ```bash
   node scripts/debt/intake-audit.js ${AUDIT_DIR}/stage-5-quality.jsonl
   ```

---

## Stage 6: Coverage Gaps & Improvements

**Goal:** What's missing? What could be better?

**Run 3 agents IN PARALLEL:**

### Agent 6A: Coverage Gap Analysis

```
Task(subagent_type="Explore", prompt="""
Identify coverage gaps:

1. File types not covered by linting
2. Code paths not validated by any check
3. Missing pre-push checks that CI catches too late
4. Firebase functions without integration tests
5. Skills without usage documentation

For each gap, create a JSONL entry (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "process",
  "title": "Gap: [description]",
  "fingerprint": "process::[file or N/A]::coverage-gap-identifier",
  "severity": "S2",
  "effort": "E2",
  "confidence": 80,
  "files": ["[relevant file or 'N/A']:1"],
  "why_it_matters": "[what's missing and why it matters]",
  "suggested_fix": "[how to add coverage]",
  "acceptance_tests": ["Coverage added", "Validation passes"]
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-6a-coverage-gaps.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 6B: Improvement Opportunities

```
Task(subagent_type="general-purpose", prompt="""
Identify improvement opportunities:

1. Scripts that could be consolidated
2. Manual processes that could be automated
3. Better tools that could replace current ones
4. Hooks that could provide better DX
5. CI optimizations (caching, parallelization)

For each opportunity, create a JSONL entry (JSONL_SCHEMA_STANDARD.md format):
{
  "category": "process",
  "title": "Improve: [description]",
  "fingerprint": "process::automation::improvement-identifier",
  "severity": "S3",
  "effort": "E2",
  "confidence": 75,
  "files": ["[relevant file or N/A]"],
  "why_it_matters": "[current state] -> [improved state]",
  "suggested_fix": "[specific implementation suggestion]",
  "acceptance_tests": ["Improvement implemented", "Verified working"]
}

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-6b-improvements.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Agent 6C: Documentation & Maintainability

```
Task(subagent_type="Explore", prompt="""
Audit documentation and maintainability:

1. Scripts without header comments explaining purpose
2. Complex logic without inline comments
3. Missing README files in key directories
4. Outdated documentation (references non-existent files)
5. TRIGGERS.md missing entries for new automation

For each issue, create a JSONL entry with severity S3.

CRITICAL: You MUST write findings directly to this file:
  ${AUDIT_DIR}/stage-6c-documentation.jsonl

Use the Write tool to create this file. Write one JSON object per line.
Do NOT return findings as text. Verify the file exists after writing.
""")
```

### Stage 6 Verification (MANDATORY)

Before proceeding to Stage 7:

```bash
# Check for misplaced files in root (context compaction recovery)
ROOT_AUDIT_FILES=$(ls *.jsonl *.md 2>/dev/null | grep -E "stage-6|automation-findings|AUTOMATION" | wc -l)
if [ "$ROOT_AUDIT_FILES" -gt 0 ]; then
  echo "WARNING: Found stage-6 files in root directory!"
  mv stage-6*.jsonl automation-findings*.jsonl AUTOMATION*.md "${AUDIT_DIR}/" 2>/dev/null || true
fi

# Verify all stage 6 files exist and have content
STAGE6_FILES="stage-6a-coverage-gaps.jsonl stage-6b-improvements.jsonl stage-6c-documentation.jsonl"
for f in $STAGE6_FILES; do
  if [ ! -s "${AUDIT_DIR}/$f" ]; then
    echo "ERROR: Missing or empty: ${AUDIT_DIR}/$f"
    echo "Re-run the failed agent before continuing"
    exit 1
  fi
done
echo "Stage 6 verified:"
wc -l ${AUDIT_DIR}/stage-6*.jsonl
```

### Stage 6 Output

1. Merge agent outputs into `stage-6-improvements.jsonl`:
   ```bash
   # Use explicit file list to avoid glob self-inclusion
   cat "${AUDIT_DIR}/stage-6a-coverage-gaps.jsonl" \
       "${AUDIT_DIR}/stage-6b-improvements.jsonl" \
       "${AUDIT_DIR}/stage-6c-documentation.jsonl" \
       > "${AUDIT_DIR}/stage-6-improvements.jsonl"
   ```
2. Run TDMS intake:
   ```bash
   node scripts/debt/intake-audit.js ${AUDIT_DIR}/stage-6-improvements.jsonl
   ```

---

## Stage 7: Synthesis & Prioritization

**Goal:** Consolidate all findings, dedupe, prioritize.

**This stage runs SEQUENTIALLY (not parallel).**

### Step 7.1: Merge All Stage Findings

```bash
# Verify all stage files exist before merging
STAGE_FILES=$(ls ${AUDIT_DIR}/stage-*.jsonl 2>/dev/null)
if [ -z "$STAGE_FILES" ]; then
  echo "ERROR: No stage JSONL files found. Re-run stages 2-6."
  exit 1
fi

# Count findings before merge (use canonical rollups only, not sub-stage files)
echo "Merging findings from canonical rollups:"
wc -l "${AUDIT_DIR}/stage-2-redundancy.jsonl" \
      "${AUDIT_DIR}/stage-3-effectiveness.jsonl" \
      "${AUDIT_DIR}/stage-4-performance.jsonl" \
      "${AUDIT_DIR}/stage-5-quality.jsonl" \
      "${AUDIT_DIR}/stage-6-improvements.jsonl"

# Combine canonical rollup files only (avoid double-counting sub-stage files)
cat "${AUDIT_DIR}/stage-2-redundancy.jsonl" \
    "${AUDIT_DIR}/stage-3-effectiveness.jsonl" \
    "${AUDIT_DIR}/stage-4-performance.jsonl" \
    "${AUDIT_DIR}/stage-5-quality.jsonl" \
    "${AUDIT_DIR}/stage-6-improvements.jsonl" \
    > "${AUDIT_DIR}/all-findings-raw.jsonl"
echo "Total findings: $(wc -l < "${AUDIT_DIR}/all-findings-raw.jsonl")"
```

### Step 7.2: Deduplicate

Check for findings that describe the same issue from different angles. Merge
duplicates, keeping the most detailed description.

### Step 7.3: Cross-Reference with Existing Debt

```bash
# Check what's already in MASTER_DEBT.jsonl
node scripts/debt/validate-schema.js ${AUDIT_DIR}/all-findings-raw.jsonl --check-duplicates
```

### Step 7.4: Generate Priority Action Plan

Create prioritized list:

1. **Immediate (S0-S1):** Fix before next commit
2. **Short-term (S2 + quick wins):** Fix this sprint
3. **Backlog (S3 + complex S2):** Add to roadmap

### Step 7.5: Generate Final Report

Create `${AUDIT_DIR}/AUTOMATION_AUDIT_REPORT.md`:

```markdown
# Automation Audit Report - [DATE]

## Executive Summary

- Total findings: X
- By severity: X S0, X S1, X S2, X S3
- By category: [breakdown]

## Inventory Summary

[From Stage 1]

## Key Findings

### Critical (S0-S1)

[List with file:line references]

### Redundancy & Dead Code

[From Stage 2]

### Effectiveness Issues

[From Stage 3]

### Performance Issues

[From Stage 4]

### Quality Issues

[From Stage 5]

### Improvement Opportunities

[From Stage 6]

## Priority Action Plan

[Grouped by timeframe]

## Dependency Graph

[Visual or text representation]
```

---

## Post-Audit (MANDATORY)

### 1. Validate All Findings

```bash
node scripts/validate-audit.js ${AUDIT_DIR}/all-findings-raw.jsonl
```

### 2. Update AUDIT_TRACKER.md

Add entry with:

- Date, Session number
- Findings count by severity
- Stages completed
- Validation status

### 2b. Reset Threshold

```bash
node scripts/reset-audit-triggers.js --type=single --category=process --apply
```

### 3. Final TDMS Reconciliation

Ensure all findings have DEBT-XXXX IDs:

```bash
# Verify all items ingested
node scripts/debt/validate-schema.js docs/technical-debt/MASTER_DEBT.jsonl
```

### 4. Regenerate Views

```bash
node scripts/debt/generate-views.js
```

### 5. Commit Audit Results

```bash
git add docs/audits/single-session/process/
git add docs/technical-debt/
git commit -m "audit: comprehensive automation audit - Session #[N]"
```

---

## Running Individual Stages

You can run stages individually if needed:

- `/audit-process stage 1` - Run only Stage 1 (Inventory)
- `/audit-process stage 2` - Run only Stage 2 (Redundancy)
- `/audit-process stage 3-4` - Run Stages 3 and 4
- `/audit-process full` - Run all 7 stages (default)

**Note:** Stages 2-6 depend on Stage 1 inventory. If Stage 1 hasn't been run
recently, run it first.

---

## Threshold System

This audit **resets the process category threshold** in `docs/AUDIT_TRACKER.md`.

**Process audit triggers:**

- ANY CI/hook/script file changed since last audit, OR
- 75+ commits since last audit (increased from 30 for expanded scope)

---

## Evidence Requirements

**All findings MUST include:**

1. **file** - Full path from repo root
2. **line** - Specific line number (use 1 if file-wide)
3. **title** - Short description
4. **description** - Detailed explanation
5. **recommendation** - How to fix
6. **severity** - S0/S1/S2/S3
7. **category** - Must be "process" for TDMS routing

**S0/S1 require:**

- HIGH or MEDIUM confidence
- Dual-pass verification
- Tool validation where possible

---

---

## Recovery from Context Compaction

If context compaction occurs during the audit:

### 1. Check Root Directory for Misplaced Files

```bash
# List any audit files that ended up in root
ls *.jsonl AUDIT*.txt AUDIT*.md AUTOMATION*.md ERROR*.md SECURITY*.md 2>/dev/null
```

### 2. Move Files to Proper Location

```bash
AUDIT_DIR="docs/audits/single-session/process/audit-$(date +%Y-%m-%d)"
mkdir -p "${AUDIT_DIR}"

# Move audit JSONL files only (not package-lock.jsonl, tsconfig.jsonl, etc.)
mv stage-*.jsonl *-audit*.jsonl *-findings*.jsonl "${AUDIT_DIR}/" 2>/dev/null || true

# Move summary files
mv AUDIT*.txt AUDIT*.md AUTOMATION*.md ERROR*.md SECURITY*.md "${AUDIT_DIR}/" 2>/dev/null || true
```

### 3. Identify Completed vs Missing Stages

Check which stage files exist:

```bash
for stage in 1 2 3 4 5 6; do
  count=$(ls ${AUDIT_DIR}/stage-${stage}*.* 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "Stage $stage: FOUND ($count files)"
  else
    echo "Stage $stage: MISSING"
  fi
done
```

### 4. Resume from Last Completed Stage

- Re-run missing stages with explicit `AUDIT_DIR` variable
- Each agent prompt MUST include the full path:
  `Write to: ${AUDIT_DIR}/filename.jsonl`
- Verify files exist after each stage before proceeding

### 5. Merge and Ingest

After all stages complete:

```bash
# Merge canonical rollup files only (avoid double-counting sub-stage files)
cat "${AUDIT_DIR}/stage-2-redundancy.jsonl" \
    "${AUDIT_DIR}/stage-3-effectiveness.jsonl" \
    "${AUDIT_DIR}/stage-4-performance.jsonl" \
    "${AUDIT_DIR}/stage-5-quality.jsonl" \
    "${AUDIT_DIR}/stage-6-improvements.jsonl" \
    | grep -v '^$' > "${AUDIT_DIR}/all-findings-raw.jsonl"

# Run TDMS intake
node scripts/debt/intake-audit.js "${AUDIT_DIR}/all-findings-raw.jsonl"
```

---

## Version History

| Version | Date       | Changes                                                      |
| ------- | ---------- | ------------------------------------------------------------ |
| 2.2     | 2026-01-31 | Added recovery procedures, root check safeguards, Step 2.5   |
| 2.1     | 2026-01-31 | Added CRITICAL persistence rules: agents MUST write to files |
| 2.0     | 2026-01-31 | Expanded: 16 types, 12 categories, 7 stages, parallel agents |
| 1.0     | 2026-01-17 | Initial single-session process audit                         |

---

## Documentation References

Before running this audit, review:

### TDMS Integration (Required)

- [PROCEDURE.md](docs/technical-debt/PROCEDURE.md) - Full TDMS workflow
- [MASTER_DEBT.jsonl](docs/technical-debt/MASTER_DEBT.jsonl) - Canonical debt
  store
- Intake command:
  `node scripts/debt/intake-audit.js <output.jsonl> --source "audit-process-<date>"`

### Documentation Standards (Required)

- [JSONL_SCHEMA_STANDARD.md](docs/templates/JSONL_SCHEMA_STANDARD.md) - Output
  format requirements and TDMS field mapping
- [DOCUMENTATION_STANDARDS.md](docs/DOCUMENTATION_STANDARDS.md) - 5-tier doc
  hierarchy
- [CODE_PATTERNS.md](docs/agent_docs/CODE_PATTERNS.md) - Anti-patterns to check

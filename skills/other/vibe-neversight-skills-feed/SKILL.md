---
name: vibe
description: 'Talos-class comprehensive code validation. Use for "validate code", "run vibe", "check quality", "security review", "architecture review", "accessibility audit", "complexity check", or any validation need. One skill to validate them all.'
---

# Vibe Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Comprehensive code validation across 8 quality aspects.

---

## ⚠️ Claude Validation Limitation Warning

**Claude is weak at systematic verification.** This was proven when Claude scored docs 9/10 "Ready for Implementation" while Codex found critical bugs at 6/10 on the same prompt.

**For SPEC/DOCUMENT validation:**
- Claude skims instead of traces
- Claude pattern-matches instead of reasons
- Claude is biased toward "looks good"

**Mitigation required:** See "Spec/Document Validation Mode" section below.

---

## Execution Steps

Given `/vibe [target]`:

### Step 1: Load Vibe-Coding Science

**Read the vibe-coding reference:**
```
Tool: Read
Parameters:
  file_path: skills/vibe/references/vibe-coding.md
```

This gives you:
- Vibe Levels (L0-L5 trust calibration)
- 5 Core Metrics and thresholds
- 12 Failure Patterns to detect
- Grade mapping

### Step 1a: Pre-flight Checks

**Before proceeding, verify we have work to validate:**

```bash
# Check if in git repo
git rev-parse --git-dir 2>/dev/null || echo "NOT_GIT"
```

If NOT_GIT and no explicit path provided, STOP with error:
> "Not in a git repository. Provide explicit file path: `/vibe path/to/files`"

### Step 1a.1: Load Prior Validation Knowledge (ao integration)

**Search for relevant learnings before validation:**

```bash
# Check if ao CLI is available
if command -v ao &> /dev/null; then
  # Search for prior validation failures on similar code
  ao search "validation failures" --limit 5 2>/dev/null || true

  # Check for known anti-patterns from learnings
  ao anti-patterns 2>/dev/null | head -20 || true
else
  # ao not available - skip knowledge injection
  echo "Note: ao CLI not available, skipping knowledge injection"
fi
```

**Use the results to:**
- Inform validation focus areas based on past failures
- Flag code patterns that previously caused issues
- Apply extra scrutiny to areas with known anti-patterns

If ao not available, skip this step and continue with validation.

### Step 1b: Run Toolchain Validation (MANDATORY)

**Before ANY agent dispatch, run the toolchain:**

```bash
./scripts/toolchain-validate.sh --gate 2>&1 | tee .agents/tooling/vibe-run.log
TOOL_EXIT=$?
```

**Interpret results:**

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | All tools pass | Proceed to agent dispatch |
| 2 | CRITICAL findings | **STOP. Report tool findings. Do not dispatch agents.** |
| 3 | HIGH findings only | Proceed, but note in report |

**If TOOL_EXIT == 2:**

```
Report to user:

  Grade: F (tools failed)

  Toolchain found CRITICAL issues that must be fixed:
  - See .agents/tooling/<tool>.txt for details

  Fix these issues before re-running /vibe.
  Do NOT generate a false "Grade: B" when tools are failing.
```

**DO NOT dispatch agents if tools found CRITICAL issues.** This prevents theater where agents ignore definitive tool failures and produce optimistic reports.

### Step 2: Determine Target and Vibe Level

**If target provided:** Use it directly.

**Classify the vibe level based on task type:**
| Task Type | Vibe Level | Depth |
|-----------|:----------:|-------|
| Format, lint | L5 | Skip |
| Boilerplate | L4 | Quick |
| CRUD, tests | L3 | Quick |
| Features | L2 | Deep |
| Architecture, security | L1 | Deep |

**If no target:** Auto-detect from git state:
```bash
# Check staged changes
git diff --cached --name-only 2>/dev/null | head -10

# Check unstaged changes
git diff --name-only 2>/dev/null | head -10

# Check recent commits
git log --oneline -5 --since="24 hours ago" 2>/dev/null
```

Use the first non-empty result. If nothing found, ask user.

### Step 2a: Pre-flight Check - Files Exist

**If auto-detected 0 files to review:**
```
STOP and return:
  Grade: PASS
  Reason: "No changes detected to review"
  Action: None required
```

Do NOT proceed with empty file list - this wastes context.

### Step 3: Get Changed Files

```bash
# For "recent" target
git diff --name-only HEAD~3 2>/dev/null | head -20

# For specific path
ls -la <path>
```

### Step 4: Read the Files

Use the Read tool to read each changed file. Understand what the code does.

### Step 5: Validate 8 Aspects

For each file, check:

| Aspect | What to Look For |
|--------|------------------|
| **Semantic** | Does code match docstrings? Misleading names? |
| **Security** | SQL injection, XSS, hardcoded secrets, auth issues |
| **Quality** | Dead code, copy-paste, magic numbers, code smells |
| **Architecture** | Layer violations, circular deps, god classes |
| **Complexity** | Deep nesting, long functions, too many params |
| **Performance** | N+1 queries, unbounded loops, resource leaks |
| **Slop** | AI hallucinations, cargo cult code, over-engineering |
| **Accessibility** | Missing ARIA, keyboard nav issues, contrast |

### Step 6: Dispatch Triage Agents (with Tool Output)

**Agents TRIAGE tool findings. They do not "review for issues."**

**Before dispatching, read tool outputs:**
```bash
cat .agents/tooling/semgrep.txt
cat .agents/tooling/gitleaks.txt
cat .agents/tooling/gosec.txt
cat .agents/tooling/ruff.txt
cat .agents/tooling/golangci-lint.txt
cat .agents/tooling/shellcheck.txt
cat .agents/tooling/radon.txt
cat .agents/tooling/hadolint.txt
```

Launch 3 agents in parallel with SPECIFIC tool output:

```
Tool: Task (ALL 3 IN PARALLEL)
Parameters:
  subagent_type: "agentops:security-reviewer"
  model: "haiku"
  description: "Triage security tool findings"
  prompt: |
    TOOL FINDINGS TO TRIAGE:

    ## Gitleaks Output:
    <paste .agents/tooling/gitleaks.txt>

    ## Semgrep Output:
    <paste .agents/tooling/semgrep.txt>

    ## Gosec Output:
    <paste .agents/tooling/gosec.txt>

    For EACH finding, determine verdict:

    TRUE_POSITIVE if:
    - File path exists (not in comments/examples)
    - Not in test fixtures (*/test/*, */mock/*, *_test.go)
    - Not already suppressed (.gitleaksignore, //nolint, # nosec)
    - Pattern matches real credential (not placeholder like "xxx")

    FALSE_POSITIVE if:
    - In test fixtures or examples
    - Already in ignore file
    - Placeholder value (contains "example", "test", "xxx")
    - Dead code path (function never called)

    OUTPUT FORMAT:
    | File:Line | Tool | Finding | Verdict | Reason | Fix (if TRUE_POS) |
    |-----------|------|---------|---------|--------|-------------------|

Tool: Task
Parameters:
  subagent_type: "agentops:code-reviewer"
  model: "haiku"
  description: "Triage linter findings"
  prompt: |
    LINTER FINDINGS TO TRIAGE:

    ## Ruff/Golangci-lint Output:
    <paste .agents/tooling/ruff.txt or golangci-lint.txt>

    ## Shellcheck Output:
    <paste .agents/tooling/shellcheck.txt>

    For EACH finding, apply severity rules:

    FIX_NOW if:
    - Blocks functionality (import error, syntax error)
    - Security implication (bare except, eval usage)
    - Cyclomatic complexity >15 in changed code

    TECH_DEBT if:
    - Style only (line length 81-100)
    - Complexity 10-15
    - Has TODO with issue reference

    NOISE if:
    - Already passing CI
    - No functional impact
    - In generated code

    OUTPUT FORMAT:
    | File:Line | Finding | Priority | Reason |
    |-----------|---------|----------|--------|

Tool: Task
Parameters:
  subagent_type: "agentops:architecture-expert"
  model: "haiku"
  description: "Triage complexity findings"
  prompt: |
    COMPLEXITY FINDINGS TO TRIAGE:

    ## Radon Output:
    <paste .agents/tooling/radon.txt>

    ## Hadolint Output:
    <paste .agents/tooling/hadolint.txt>

    For EACH high-complexity function:
    - Is it in changed files? (only review what's new)
    - Can it be split? (identify extraction points)
    - Is complexity justified? (state machines, parsers OK)

    OUTPUT FORMAT:
    | File:Function | Complexity | In Changed? | Recommendation |
    |---------------|------------|-------------|----------------|
```

**Key change:** Agents now receive ACTUAL tool output and have EXPLICIT criteria for verdicts.

**Timeout handling:** Per-agent timeout of 3 minutes (180000ms). If agent times out, continue with remaining results if quorum (80%) met. See `.agents/specs/conflict-resolution-algorithm.md` for synthesis rules.

### Step 6a: Apply Conflict Resolution (for swarm results)

**If multiple agents dispatched:**
1. Check quorum (80% minimum must return)
2. Apply severity escalation (if ANY agent reports CRITICAL → final is CRITICAL)
3. Deduplicate findings by file:line (±5 lines tolerance)
4. Track agreement per finding (e.g., "3/6 agents found this")
5. Compute weighted grade

**If quorum not met:** Report as INCOMPLETE, do not publish grade.

See: `.agents/specs/conflict-resolution-algorithm.md`

### Step 7: Check for Failure Patterns

**Detect the 12 failure patterns from vibe-coding science:**

| Pattern | Detection Method |
|---------|------------------|
| #1 Tests Lie | Compare test output to actual behavior |
| #4 Debug Spiral | Count consecutive fix commits |
| #5 Eldritch Horror | Functions >500 lines |
| #6 Collision | Multiple recent editors on same file |

### Step 8: Categorize Findings

Group findings by severity:

| Severity | Definition | Gate |
|----------|------------|------|
| **CRITICAL** | Security vulnerability, data loss risk | BLOCKS |
| **HIGH** | Significant bug, performance issue | Should fix |
| **MEDIUM** | Code smell, maintainability issue | Worth noting |
| **LOW** | Style, minor improvement | Optional |

### Step 9: Compute Grade

Based on findings:
- **A**: 0 critical, 0-2 high
- **B**: 0 critical, 3-5 high
- **C**: 0 critical, 6+ high OR 1 critical (fixed)
- **D**: 1+ critical unfixed
- **F**: Multiple critical, systemic issues

### Step 10: Write Vibe Report

**Write to:** `.agents/vibe/YYYY-MM-DD-<target>.md`

```markdown
# Vibe Report: <Target>

**Date:** YYYY-MM-DD
**Files Reviewed:** <count>
**Grade:** <A-F>

## Summary
<Overall assessment in 2-3 sentences>

## Gate Decision
[ ] PASS - 0 critical findings
[ ] BLOCK - <count> critical findings must be fixed

## Findings

### CRITICAL
1. **<File:Line>** - <Issue>
   - **Risk:** <what could happen>
   - **Fix:** <how to fix>

### HIGH
1. **<File:Line>** - <Issue>
   - **Fix:** <how to fix>

### MEDIUM
- <File:Line>: <brief issue>

## Aspects Summary
| Aspect | Status |
|--------|--------|
| Semantic | <OK/Issues> |
| Security | <OK/Issues> |
| Quality | <OK/Issues> |
| Architecture | <OK/Issues> |
| Complexity | <OK/Issues> |
| Performance | <OK/Issues> |
| Slop | <OK/Issues> |
| Accessibility | <OK/N/A> |
```

### Step 11: Report to User

Tell the user:
1. Overall grade
2. Gate decision (PASS/BLOCK)
3. Critical and high findings (if any)
4. Location of full report

### Step 12: Record Validation Results (ao integration)

**Store validation learnings for future sessions:**

```bash
# Check if ao CLI is available
if command -v ao &> /dev/null; then
  # If CRITICAL findings were discovered, record them as learnings
  if [ "<grade>" = "D" ] || [ "<grade>" = "F" ]; then
    ao memory_store \
      --content "Validation found CRITICAL issues in <target>: <summary of critical findings>" \
      --memory_type "episode" \
      --tags '["validation", "critical", "<area>"]' \
      --source "vibe skill" 2>/dev/null || true
  fi

  # Record any new anti-patterns discovered
  # (Only if a pattern was found that wasn't already known)
  # ao forge transcript <session-log> 2>/dev/null || true
else
  # ao not available - skip result recording
  echo "Note: ao CLI not available, skipping result recording"
fi
```

**What gets recorded:**
- CRITICAL findings become episodes for future reference
- Novel anti-patterns get extracted via forge
- Validation outcomes help calibrate future assessments

If ao not available, skip this step and continue.

## Key Rules

- **0 CRITICAL = PASS** - the gate rule
- **Evidence for every finding** - cite file:line
- **Actionable fixes** - tell them HOW to fix, not just what's wrong
- **Grade reflects reality** - don't inflate or deflate
- **Write the report** - always produce `.agents/vibe/` artifact
- **For specs: Build tables, don't trust impressions** - mechanical cross-referencing required
- **Never claim "Ready for Implementation" on validation** - recommend external verification

## Quick vs Deep

- **Quick** (`/vibe`): Read files, check obvious issues
- **Deep** (`/vibe --deep`): Dispatch expert agents for thorough review

## Prescan Script

The vibe skill includes an automated prescan script at `scripts/prescan.sh`:

```bash
# Run prescan for secret detection
./scripts/prescan.sh <target-path>
```

**What it checks:**
- Hardcoded secrets (API keys, passwords, tokens)
- AWS/GCP/Azure credentials
- Private keys
- Connection strings

**Exit codes:**
- `0`: No secrets found
- `1`: Secrets detected (blocks gate)

**Integration:** Run prescan before full vibe validation to catch secrets early.

---

## Spec/Document Validation Mode

**When target is documentation or specs** (*.md files in docs/, specs/, or similar):

### Why This Is Different

Code validation: Look for bugs, security issues, complexity.
Spec validation: Cross-reference consistency across multiple documents.

**Claude fails at spec validation** because it:
- Skims instead of mechanically tracing
- Assumes similar terms are equivalent
- Rationalizes differences instead of flagging conflicts

### Mandatory Protocol for Spec Validation

**Step S1: Generate Explicit Checklist BEFORE Reading**

```
Before reading any documents, generate a checklist:
- List every entity that should be consistent (agents, states, message types, timeouts)
- List every cross-reference to verify (A mentions B → B exists and matches)
- List every enum/constant that appears in multiple places
```

**Step S2: Build Mechanical Cross-Reference Tables**

For each entity type, build a table with tool calls:

```markdown
| Entity | Doc A (line) | Doc B (line) | Match? |
|--------|--------------|--------------|--------|
| HARVEST_REQUEST sender | auth matrix:152 "Moirai" | comm matrix:1123 "Athena" | ❌ CONFLICT |
```

**Step S3: Trace Relationships, Don't Pattern Match**

For every relationship claim:
1. Read the EXACT line in source doc
2. Read the EXACT line in target doc
3. Compare literally, not conceptually
4. Flag ANY difference, even if it "seems equivalent"

**Step S4: Bias Toward Finding Problems**

- Assume bugs exist
- Try to break the spec
- Ask: "What would Codex catch that I'm missing?"

**Step S5: Never Say "Ready for Implementation"**

Final output must be:
```
## Findings
[List what was found]

## Verification Status
⚠️ Claude-based validation has known limitations.
Recommend external verification with Codex or mechanical diff tools.

## Cross-Reference Tables
[Show the tables built in Step S2]
```

### Dispatch Spec Validation Agents

For spec validation, dispatch these agents **in parallel**:

```
Tool: Task (ALL IN PARALLEL)
Parameters:
  subagent_type: "agentops:plan-compliance-expert"
  description: "Check spec compliance"
  prompt: "Verify these specs are internally consistent: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:gap-identifier"
  description: "Find spec gaps"
  prompt: "Find missing definitions or broken references in: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:assumption-challenger"
  description: "Challenge assumptions"
  prompt: "Challenge assumptions and find conflicts in: <file-list>"
```

### Example: What Claude Missed

| Issue Type | What Claude Did | What Claude Should Do |
|------------|-----------------|----------------------|
| Authorization Matrix wrong sender | Saw "HARVEST_REQUEST" in both tables, moved on | Build table: sender in Auth Matrix vs sender in Comm Matrix |
| Bead status enum mismatch | Saw "pending/assigned" vs "open", assumed equivalent | Flag: "pending" ≠ "open" - which is canonical? |
| Retry logic contradiction | Saw "retry" and "3" in multiple docs, assumed consistent | Trace: On rejection → does Demigod retry or Apollo escalate? |

**The lesson:** Mechanical verification beats gestalt impression.

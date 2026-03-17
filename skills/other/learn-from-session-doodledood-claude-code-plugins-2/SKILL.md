---
name: learn-from-session
description: 'Analyze Claude Code sessions to learn what went right/wrong and suggest high-confidence improvements to skills. Use when asked to analyze a session, learn from a session, or review workflow effectiveness.'
user-invocable: true
---

**User request**: $ARGUMENTS

Analyze a Claude Code session to identify what went well and what could be improved, then suggest high-confidence fixes to skills in this repository.

**Input formats**:
- Session ID (UUID): `184078b7-2609-46e0-a1f2-bb42367a8d34`
- Session file path: `~/.claude/projects/.../session-id.jsonl`
- Inline commentary: Text description of what happened

**Output**: High-confidence issues only with evidence-based suggestions for skill improvements.

**Signal quality bar**: Only recommend changes that would have **prevented specific rework** in the session. A fix is high-signal when ALL of:
1. You can point to exact message numbers where rework occurred
2. The skill change would have triggered BEFORE that rework
3. Following the change would have produced correct output initially

**Definition - high-signal fix**: A skill change that passes the 3/3 counterfactual test (see Phase 5.2).

---

## Phase 1: Parse Input & Setup

### 1.1 Identify input type

| Input Pattern | Type | Action |
|---------------|------|--------|
| UUID format (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) | Session ID | Find and read session file |
| Path ending in `.jsonl` | Session file | Read directly |
| Other text | Commentary | Analyze inline, may reference sessions |

### 1.2 Locate session file (if session ID)

Session files are stored at:
```
~/.claude/projects/{project-path-encoded}/{session-id}.jsonl
```

**Note**: `{project-path-encoded}` replaces path separators with URL-safe encoding (e.g., `/home/user/myproject` becomes `-home-user-myproject`). Don't rely on exact path structure—use find instead.

Use Bash to find:
```bash
find ~/.claude/projects -name "*{session-id}*" -type f 2>/dev/null
```

**If file not found**: Ask user to provide the session file path directly or check if session ID is correct.

### 1.3 Create analysis log

Path: `/tmp/session-analysis-{session-id-short}-{timestamp}.md`

**Purpose**: External memory that persists findings beyond LLM working memory. Write to this file IMMEDIATELY after each discovery—never batch multiple findings into one write.

```markdown
# Session Analysis Log

Session: {id or "inline commentary"}
Started: {timestamp}
Status: IN_PROGRESS

---

## Session Overview
<!-- Write immediately after Phase 2 parsing -->

**Initial request**:
**Skills invoked**:
**Outcome**:
**Session length**:

---

## Pattern Detection

### Iterations Found
<!-- Write immediately after detecting iterations - before moving to corrections -->

### User Corrections Found
<!-- Write immediately after detecting corrections - before moving to deviations -->

### Workflow Deviations Found
<!-- Write immediately after detecting deviations - before moving to missing questions -->

### Missing Questions Found
<!-- Write immediately after detecting missing questions - before moving to post-impl -->

### Post-Implementation Fixes Found
<!-- Write immediately after detecting post-impl fixes - before skill comparison -->

---

## Skill Comparison

### Skills Discovered
<!-- Write immediately after discovering which skills were used -->

### Skill: {name}
<!-- Write immediately after analyzing EACH skill - don't batch -->

---

## Potential Issues
<!-- Write each issue as identified during comparison -->

---

## Counterfactual Analysis
<!-- Write results of 3/3 test for each issue -->

---

## Final Recommendations
<!-- Populated after refresh step -->
```

### 1.4 Create todo list

**CRITICAL**: Write to log IMMEDIATELY after each finding—never batch writes.

```
- [ ] Setup: Create log file, parse session, write overview
- [ ] Pattern detection: iterations, corrections, deviations, missing questions, post-impl fixes (write each to log)
- [ ] Skill discovery: extract skills, locate files, write to log
- [ ] (expand: "Analyze {skill}" for each skill found)
- [ ] Refresh context: read FULL analysis log
- [ ] Counterfactual analysis: test each issue, write recommendations
- [ ] Output final report
```

**Expansion**: When skills are discovered, add one todo per skill:
```
- [ ] Analyze {skill-name} skill + write findings to log
```

**Why write-after-each-step matters**: By synthesis, early findings suffer context rot. Writing externalizes findings to a file that persists. The refresh step moves ALL findings to context end (highest attention zone).

---

## Phase 2: Parse Session

### 2.1 Session file structure

Claude Code sessions are JSONL files with these record types:

| Type | Contains |
|------|----------|
| `user` | User messages, `message.content` field |
| `assistant` | Claude responses, tool calls, thinking |
| `system` | System events, commands, hooks |
| `file-history-snapshot` | File state tracking |

### 2.2 Extract key events

Use `jq` to parse:

```bash
# User messages
cat {session-file} | jq -r 'select(.type == "user") | .message.content' 2>/dev/null

# Tool calls
cat {session-file} | jq -r 'select(.type == "assistant") | .message.content | if type == "array" then .[] | select(.type == "tool_use") | .name else empty end' 2>/dev/null

# Skill invocations
grep -o '"skill":"[^"]*"' {session-file} | sort | uniq -c
```

### 2.3 Build session overview

Extract and log:
- **Initial request**: First user message (the goal)
- **Workflow used**: Which skills invoked (`/spec`, `/plan`, `/implement`, etc.)
- **Workflow skipped**: Skills that would typically apply but weren't invoked (see table below)
- **Outcome**: Success, partial, or required rework
- **Session length**: Message count, duration if available

**Expected skills by task type** (use to detect skipped workflows):

| Task Indicators in Request | Expected Skills |
|---------------------------|-----------------|
| "build", "implement", "create feature", "add" | spec → plan → implement |
| "fix bug", "debug", "not working" | bugfix |
| "review", "check", "audit" | review (or specific review-*) |
| "refactor", "improve", "optimize" | plan → implement |
| Multi-file changes (3+ files likely) | plan before implement |

Only flag as "skipped" if evidence suggests the skill would have prevented issues that occurred.

---

## Phase 3: Pattern Detection

Analyze the session for these patterns. Each pattern has evidence requirements.

### 3.1 Iteration patterns (things that didn't work first time)

**Evidence required**: Same file edited multiple times, OR error → fix → retry sequence

Look for:
- TypeScript errors followed by fixes
- Test failures followed by code changes
- Lint errors followed by formatting changes
- Same function/file edited more than once with different intent (not additive changes, but corrections)

**Log format**:
```markdown
### Iteration: {description}
- Files affected: {list}
- Attempts: {count}
- Root cause: {why it didn't work first time}
- Potential skill gap: {what could have prevented this}
```

Write ALL iteration findings to log file NOW, before proceeding to 3.2.

### 3.2 User corrections ("no, I meant...")

**Evidence required**: User message containing correction language

Correction indicators:
- "no", "not what I meant", "actually", "instead", "I meant"
- "let's go back", "undo", "revert"
- "that's wrong", "incorrect"

**Log format**:
```markdown
### User Correction: {what was corrected}
- Original action: {what Claude did}
- User feedback: {correction text}
- Missing context: {what Claude should have asked/known}
```

Write ALL correction findings to log file NOW, before proceeding to 3.3.

### 3.3 Workflow deviations

**Evidence required**: Expected workflow step skipped or out-of-order

Check for:
- Multi-phase skill invoked but phases skipped (read skill to know expected phases)
- Skill with prerequisites invoked without those prerequisites (e.g., implementation without planning)
- Ordered steps executed out of order
- Verification/validation steps skipped before proceeding

**How to detect**: Compare skill's documented phases against actual session sequence.

**Log format**:
```markdown
### Workflow Deviation: {what was skipped/reordered}
- Skill: {which skill's workflow}
- Expected flow: {phases from skill definition}
- Actual flow: {what happened in session}
- Impact: {did this cause issues later?}
```

Write ALL deviation findings to log file NOW, before proceeding to 3.4.

### 3.4 Missing questions

**Evidence required**: Information discovered during implementation that should have been asked upfront

Look for:
- Design decisions made mid-implementation
- Assumptions that were later corrected
- "The user confirmed..." appearing late in session
- Post-implementation "actually, let's change..." patterns

**Log format**:
```markdown
### Missing Question: {what should have been asked}
- Discovered at: {phase where it came up}
- Impact: {rework required}
- Skill gap: {which skill should have asked this}
```

Write ALL missing question findings to log file NOW, before proceeding to 3.5.

### 3.5 Post-implementation fixes

**Evidence required**: Changes made AFTER "implementation complete" or PR creation

Look for:
- Commits/changes after PR URL appears
- Refactoring after "done" or "complete" messages
- Review findings that required code changes
- User requesting changes after seeing "finished"

**Log format**:
```markdown
### Post-Implementation Fix: {what was fixed}
- Original implementation: {what was done}
- Fix required: {what changed}
- Should have been caught by: {which phase/skill}
```

Write ALL post-implementation findings to log file NOW, before proceeding to Phase 4.

---

## Phase 4: Skill Comparison

### 4.1 Discover skills used in session

**Step 1**: Extract skill invocations from session:

```bash
# Find all Skill tool invocations (handles both "skill" and skill names in tool calls)
grep -oE '"skill"\s*:\s*"[^"]*"' {session-file} | sort | uniq -c

# Find slash command patterns in user messages (alphanumeric with hyphens)
grep -oE '/[a-zA-Z][a-zA-Z0-9-]*' {session-file} | sort | uniq -c

# Find Skill tool calls with plugin:skill format
grep -oE 'Skill\s*\(\s*"[^"]+:[^"]+"' {session-file} | sort | uniq -c
```

**Step 2**: Find ALL relevant files for each skill.

**Option A - If codebase-explorer skill is available**:

Invoke the vibe-workflow:explore-codebase skill with: "medium - find all files related to the {skill-name} skill: SKILL.md definition, related agents it spawns, hooks that affect it, and any shared utilities"

**Option B - Manual search fallback**:
```bash
# Find skill definition
find . -path "*/skills/{skill-name}/SKILL.md" -type f

# Find related agents (look in same plugin's agents/ folder)
PLUGIN_DIR=$(dirname $(dirname {skill-path}))
ls "$PLUGIN_DIR/agents/" 2>/dev/null

# Find hooks that might affect this skill
grep -r "{skill-name}" --include="*.py" */hooks/ 2>/dev/null
```

This discovers:
- The SKILL.md definition itself
- Agents the skill spawns (e.g., plan-verifier for /plan)
- Hooks that intercept skill behavior (e.g., Stop hook)
- Shared utilities the skill depends on
- Test files that document expected behavior

**Step 3**: Log discovered skills with full context:

```markdown
## Skills Used in Session

### {skill-name}
- **SKILL.md**: {path}
- **Related agents**: {list from explorer}
- **Related hooks**: {list from explorer}
- **Invoked**: {count} times
```

Write discovered skills to log file NOW, before proceeding to 4.2.

### 4.2 Extract actionable rules from each skill

For each skill file, extract:

**Rule indicators** (look for these patterns):
- `must`, `should`, `never`, `always` → mandatory behaviors
- `## Phase N:` or `### Step N:` → workflow phases
- `questions:` or `AskUserQuestion` → required user prompts
- `| Condition | Action |` tables → decision rules
- `**CRITICAL**`, `**IMPORTANT**` → high-priority rules
- `- [ ]` todo templates → expected workflow steps
- `Acceptance:` or `Validation:` → verification requirements

**Extract and log**:
```markdown
### Skill: {name}
**File**: {path}

**Mandatory behaviors**:
- {rule with line number}

**Workflow phases**:
1. {phase name} - expected outputs: {list}

**Required questions** (when applicable):
- {question topic}

**Verification steps**:
- {what should be checked}
```

### 4.3 Compare documented vs actual

For each skill used in the session:

| Aspect | Documented | Actual | Gap? | Impact |
|--------|------------|--------|------|--------|
| Questions asked | {from skill} | {from session} | {Y/N} | {would have prevented X} |
| Phases followed | {from skill} | {from session} | {Y/N} | {would have caught Y} |
| Validations run | {from skill} | {from session} | {Y/N} | {would have avoided Z} |
| Outputs produced | {from skill} | {from session} | {Y/N} | {required later but missing} |

**Key comparison questions**:
1. Did the skill ask all documented questions? If not, did missing answers cause issues?
2. Were all phases executed in order? If skipped, did it matter?
3. Were validations run? If skipped, did bugs slip through?
4. Did outputs match documented format? If not, did downstream steps suffer?

### 4.4 Log skill gaps with impact

```markdown
### Skill Gap: {skill name}
- **Rule violated**: {what skill says to do, with line reference}
- **What happened**: {actual behavior in session}
- **Evidence**: {specific session content showing gap}
- **Impact**: {did this cause iteration/correction/rework?}
- **Counterfactual**: {if rule was followed, would outcome differ?}
- **Confidence**: HIGH | MEDIUM | LOW
```

**Only log gaps where**:
1. Evidence is clear (specific session content)
2. Impact is documented (caused measurable problem)
3. Counterfactual is plausible (fix would have helped)

Write skill gap findings to log file after analyzing EACH skill—never batch multiple skills into one write.

---

## Phase 5: Synthesize Recommendations

### 5.1 Refresh context (non-negotiable)

**CRITICAL**: Use the Read tool to read the FULL analysis log file NOW before any synthesis.

**Why this step exists**: By this point, findings from Phase 3 (pattern detection) have suffered context rot—they're in the "lost middle" of conversation. The log file contains ALL findings written throughout this workflow. Reading it:
- Moves ALL findings to context END (highest attention zone)
- Converts holistic synthesis (LLMs are bad at this) into dense recent context (LLMs are good at this)
- Restores details that would otherwise be missed

**Action**: Use `Read("/tmp/session-analysis-{id}-{timestamp}.md")` to read the entire log file. Do NOT proceed to 5.2 until this is complete.

### 5.2 Counterfactual analysis (the high-signal filter)

For each potential issue, answer these three questions with specific evidence:

| Test | Question | Evidence Required |
|------|----------|-------------------|
| **T1: Rework identified** | Can you cite specific message numbers where rework occurred? | Message #X shows error, #Y shows fix |
| **T2: Intervention point** | At which earlier message would the skill change have triggered? | Message #Z is where skill phase X runs |
| **T3: Trigger conditions met** | Did the session content at that point contain info that would activate the change? | Quote the text that would trigger it |

**Scoring**:
| Score | Criteria | Action |
|-------|----------|--------|
| 3/3 | All three answered with specific evidence | HIGH confidence → Include |
| 2/3 | One test lacks specific evidence | MEDIUM confidence → Deferred section |
| 1/3 or 0/3 | Multiple tests lack evidence | LOW confidence → Discard |

**Example counterfactual**:
```
Issue: Plan skill should ask about time filtering

T1 (Rework): Message #47 adds 90-day filter, #48 user says "yes that's what I meant"
T2 (Intervention): Message #12 is plan phase, "Files to modify" section
T3 (Trigger): Message #5 user wrote "recent refunds" - this would trigger temporal scope question

Score: 3/3 → HIGH confidence
```

### 5.3 Additional disqualifiers

Even with 3/3 counterfactual score, discard if:
- **Compliance failure**: Skill already documents this; it just wasn't followed
- **One-off context**: Unusual situation unlikely to recur (e.g., user typo)
- **Scope creep**: Fix would make skill too complex for marginal benefit
- **Side effects**: Fix would break other documented behavior

### 5.4 Format recommendations

For each HIGH confidence issue:

```markdown
## Issue: {short title}

**Confidence**: HIGH
**Counterfactual score**: 3/3

### Evidence
{Quote or describe specific session content}

### What Happened
{Brief description of the problem}

### Root Cause
{Why the current skill didn't prevent this - be specific about what's missing}

### Counterfactual
- **Iteration avoided**: {which rework/correction would NOT have happened}
- **Intervention point**: {exact moment the fix would have triggered}
- **Trigger condition**: {why the fix would have applied to this session}

### Suggested Fix
**File**: {skill file path}
**Section**: {phase/section name}
**Line**: ~{approximate line number}

**Current behavior**:
{What the skill does now}

**Proposed behavior**:
{What the skill should do instead}

```{code block showing the diff if applicable}```

### Risk Assessment
- **Side effects**: {could this break other flows? NO/LOW/MEDIUM/HIGH}
- **Complexity added**: {minimal/moderate/significant}
- **Test approach**: {how to verify the fix works}
```

---

## Phase 6: Output

### 6.1 Final report structure

```markdown
# Session Analysis: {session id or description}

## Summary
- **Session outcome**: {success/partial/rework needed}
- **Workflow used**: {skills invoked}
- **Iterations observed**: {count of retry/fix cycles}
- **High-signal fixes**: {count} (3/3 counterfactual score)

## What Went Well
{List of things that worked correctly - be specific about which skill behaviors succeeded}

## Iteration Timeline
{Chronological list of corrections/retries observed, with timestamps if available}

1. {time}: {what was attempted}
2. {time}: {what went wrong}
3. {time}: {how it was fixed}

## High-Confidence Improvements

### Fix 1: {title}
{Full format from 5.4}

### Fix 2: {title}
...

## Deferred (Partial Counterfactual Match)
{Issues that scored 2/3 - might help but not definitively causal}

| Issue | Missing Criterion | Why Deferred |
|-------|-------------------|--------------|
| {title} | {which of the 3 failed} | {brief explanation} |

## Not Actionable
{Issues that scored 1/3 or 0/3, or hit disqualifiers - briefly note for transparency}

---
Analysis log: {log file path}
```

### 6.2 Return report

Output the final report. User can then decide which fixes to implement.

---

## Key Principles

| Principle | Rule |
|-----------|------|
| Counterfactual-driven | Every fix must pass the 3/3 counterfactual test |
| Evidence-based | Quote or cite specific session content |
| Iteration-focused | Primary signal = things that required retry/correction |
| Skill-focused | Goal is improving skills, not critiquing user or session |
| Log-driven | Write findings to log as you go, refresh before synthesis |

## Confidence Criteria (Counterfactual-Based)

| Score | Test Results | Action |
|-------|--------------|--------|
| 3/3 | Would avoid iteration + Name exact moment + Conditions would trigger | HIGH → Include |
| 2/3 | Two of three | MEDIUM → Deferred section |
| 1/3 | One of three | LOW → Not Actionable section |
| 0/3 | None | Discard entirely |

## Disqualifiers (Even at 3/3)

| Disqualifier | Why It Filters Out |
|--------------|--------------------|
| Compliance failure | Skill already covers this - LLM didn't follow |
| One-off context | Unusual situation unlikely to recur |
| Scope creep | Fix adds complexity disproportionate to benefit |
| Side effects | Fix would break other documented behaviors |

## Error Handling

| Error | Response |
|-------|----------|
| Session file not found | Ask user to provide path directly |
| Malformed JSONL (parse error) | Skip malformed lines, note in report |
| Skill file not found | Note as "skill definition unavailable" in comparison |
| jq not available | Use grep/sed fallback patterns to extract JSON fields |
| Empty session | Report "Session contains no analyzable content" |

## Never Do

- Suggest changes without specific session evidence
- Include fixes that score <3/3 in main recommendations
- Skip the counterfactual test ("it seems like it would help")
- Skip reading the full analysis log before synthesis
- Critique user behavior (focus on skill gaps, not user mistakes)
- Suggest fixes that would break other documented behavior
- Recommend changes to skills that weren't used in the session

---
name: debug-with-file
description: Interactive hypothesis-driven debugging with documented exploration, understanding evolution, and analysis-assisted correction.
argument-hint: "BUG=\"<bug description or error message>\""
---

# Codex Debug-With-File Prompt

## Overview

Enhanced evidence-based debugging with **documented exploration process**. Records understanding evolution, consolidates insights, and uses analysis to correct misunderstandings.

**Core workflow**: Explore → Document → Log → Analyze → Correct Understanding → Fix → Verify

**Key enhancements over /prompts:debug**:
- **understanding.md**: Timeline of exploration and learning
- **Analysis-assisted correction**: Validates and corrects hypotheses
- **Consolidation**: Simplifies proven-wrong understanding to avoid clutter
- **Learning retention**: Preserves what was learned, even from failed attempts

## Target Bug

**$BUG**

## Execution Process

```
Session Detection:
   ├─ Check if debug session exists for this bug
   ├─ EXISTS + understanding.md exists → Continue mode
   └─ NOT_FOUND → Explore mode

Explore Mode:
   ├─ Locate error source in codebase
   ├─ Document initial understanding in understanding.md
   ├─ Generate testable hypotheses with analysis validation
   ├─ Add NDJSON logging instrumentation
   └─ Output: Hypothesis list + await user reproduction

Analyze Mode:
   ├─ Parse debug.log, validate each hypothesis
   ├─ Use analysis to evaluate hypotheses and correct understanding
   ├─ Update understanding.md with:
   │   ├─ New evidence
   │   ├─ Corrected misunderstandings (strikethrough + correction)
   │   └─ Consolidated current understanding
   └─ Decision:
       ├─ Confirmed → Fix root cause
       ├─ Inconclusive → Add more logging, iterate
       └─ All rejected → Assisted new hypotheses

Fix & Cleanup:
   ├─ Apply fix based on confirmed hypothesis
   ├─ User verifies
   ├─ Document final understanding + lessons learned
   ├─ Remove debug instrumentation
   └─ If not fixed → Return to Analyze mode
```

## Implementation Details

### Session Setup & Mode Detection

##### Step 0: Determine Project Root

检测项目根目录，确保 `.workflow/` 产物位置正确：

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

优先通过 git 获取仓库根目录；非 git 项目回退到 `pwd` 取当前绝对路径。
存储为 `{projectRoot}`，后续所有 `.workflow/` 路径必须以此为前缀。

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()
const projectRoot = bash('git rev-parse --show-toplevel 2>/dev/null || pwd').trim()

const bugSlug = "$BUG".toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 30)
const dateStr = getUtc8ISOString().substring(0, 10)

const sessionId = `DBG-${bugSlug}-${dateStr}`
const sessionFolder = `${projectRoot}/.workflow/.debug/${sessionId}`
const debugLogPath = `${sessionFolder}/debug.log`
const understandingPath = `${sessionFolder}/understanding.md`
const hypothesesPath = `${sessionFolder}/hypotheses.json`

// Auto-detect mode
const sessionExists = fs.existsSync(sessionFolder)
const hasUnderstanding = sessionExists && fs.existsSync(understandingPath)
const logHasContent = sessionExists && fs.existsSync(debugLogPath) && fs.statSync(debugLogPath).size > 0

const mode = logHasContent ? 'analyze' : (hasUnderstanding ? 'continue' : 'explore')

if (!sessionExists) {
  bash(`mkdir -p ${sessionFolder}`)
}
```

### Explore Mode

#### Step 1.1: Locate Error Source

```javascript
// Extract keywords from bug description
const keywords = extractErrorKeywords("$BUG")

// Search codebase for error locations
const searchResults = []
for (const keyword of keywords) {
  const results = Grep({ pattern: keyword, path: ".", output_mode: "content", "-C": 3 })
  searchResults.push({ keyword, results })
}

// Identify affected files and functions
const affectedLocations = analyzeSearchResults(searchResults)
```

#### Step 1.2: Document Initial Understanding

Create `understanding.md`:

```markdown
# Understanding Document

**Session ID**: ${sessionId}
**Bug Description**: $BUG
**Started**: ${getUtc8ISOString()}

---

## Exploration Timeline

### Iteration 1 - Initial Exploration (${timestamp})

#### Current Understanding

Based on bug description and initial code search:

- Error pattern: ${errorPattern}
- Affected areas: ${affectedLocations.map(l => l.file).join(', ')}
- Initial hypothesis: ${initialThoughts}

#### Evidence from Code Search

${searchResults.map(r => `
**Keyword: "${r.keyword}"**
- Found in: ${r.results.files.join(', ')}
- Key findings: ${r.insights}
`).join('\n')}

#### Next Steps

- Generate testable hypotheses
- Add instrumentation
- Await reproduction

---

## Current Consolidated Understanding

${initialConsolidatedUnderstanding}
```

#### Step 1.3: Generate Hypotheses

Analyze the bug and generate 3-5 testable hypotheses:

```javascript
// Hypothesis generation based on error pattern
const HYPOTHESIS_PATTERNS = {
  "not found|missing|undefined|未找到": "data_mismatch",
  "0|empty|zero|registered": "logic_error",
  "timeout|connection|sync": "integration_issue",
  "type|format|parse": "type_mismatch"
}

function generateHypotheses(bugDescription, affectedLocations) {
  // Generate targeted hypotheses based on error analysis
  // Each hypothesis includes:
  // - id: H1, H2, ...
  // - description: What might be wrong
  // - testable_condition: What to log
  // - logging_point: Where to add instrumentation
  // - evidence_criteria: What confirms/rejects it
  return hypotheses
}
```

Save to `hypotheses.json`:

```json
{
  "iteration": 1,
  "timestamp": "2025-01-21T10:00:00+08:00",
  "hypotheses": [
    {
      "id": "H1",
      "description": "Data structure mismatch - expected key not present",
      "testable_condition": "Check if target key exists in dict",
      "logging_point": "file.py:func:42",
      "evidence_criteria": {
        "confirm": "data shows missing key",
        "reject": "key exists with valid value"
      },
      "likelihood": 1,
      "status": "pending"
    }
  ]
}
```

#### Step 1.4: Add NDJSON Instrumentation

For each hypothesis, add logging at the specified location:

**Python template**:
```python
# region debug [H{n}]
try:
    import json, time
    _dbg = {
        "sid": "{sessionId}",
        "hid": "H{n}",
        "loc": "{file}:{line}",
        "msg": "{testable_condition}",
        "data": {
            # Capture relevant values here
        },
        "ts": int(time.time() * 1000)
    }
    with open(r"{debugLogPath}", "a", encoding="utf-8") as _f:
        _f.write(json.dumps(_dbg, ensure_ascii=False) + "\n")
except: pass
# endregion
```

**JavaScript/TypeScript template**:
```javascript
// region debug [H{n}]
try {
  require('fs').appendFileSync("{debugLogPath}", JSON.stringify({
    sid: "{sessionId}",
    hid: "H{n}",
    loc: "{file}:{line}",
    msg: "{testable_condition}",
    data: { /* Capture relevant values */ },
    ts: Date.now()
  }) + "\n");
} catch(_) {}
// endregion
```

#### Step 1.5: Output to User

```
## Hypotheses Generated

Based on error "$BUG", generated {n} hypotheses:

{hypotheses.map(h => `
### ${h.id}: ${h.description}
- Logging at: ${h.logging_point}
- Testing: ${h.testable_condition}
- Evidence to confirm: ${h.evidence_criteria.confirm}
- Evidence to reject: ${h.evidence_criteria.reject}
`).join('')}

**Debug log**: ${debugLogPath}

**Next**: Run reproduction steps, then come back for analysis.
```

### Analyze Mode

#### Step 2.1: Parse Debug Log

```javascript
// Parse NDJSON log
const entries = Read(debugLogPath).split('\n')
  .filter(l => l.trim())
  .map(l => JSON.parse(l))

// Group by hypothesis
const byHypothesis = groupBy(entries, 'hid')

// Validate each hypothesis
for (const [hid, logs] of Object.entries(byHypothesis)) {
  const hypothesis = hypotheses.find(h => h.id === hid)
  const latestLog = logs[logs.length - 1]

  // Check if evidence confirms or rejects hypothesis
  const verdict = evaluateEvidence(hypothesis, latestLog.data)
  // Returns: 'confirmed' | 'rejected' | 'inconclusive'
}
```

#### Step 2.2: Analyze Evidence and Correct Understanding

Review the debug log and evaluate each hypothesis:

1. Parse all log entries
2. Group by hypothesis ID
3. Compare evidence against expected criteria
4. Determine verdict: confirmed | rejected | inconclusive
5. Identify incorrect assumptions from previous understanding
6. Generate corrections

#### Step 2.3: Update Understanding with Corrections

Append new iteration to `understanding.md`:

```markdown
### Iteration ${n} - Evidence Analysis (${timestamp})

#### Log Analysis Results

${results.map(r => `
**${r.id}**: ${r.verdict.toUpperCase()}
- Evidence: ${JSON.stringify(r.evidence)}
- Reasoning: ${r.reason}
`).join('\n')}

#### Corrected Understanding

Previous misunderstandings identified and corrected:

${corrections.map(c => `
- ~~${c.wrong}~~ → ${c.corrected}
  - Why wrong: ${c.reason}
  - Evidence: ${c.evidence}
`).join('\n')}

#### New Insights

${newInsights.join('\n- ')}

${confirmedHypothesis ? `
#### Root Cause Identified

**${confirmedHypothesis.id}**: ${confirmedHypothesis.description}

Evidence supporting this conclusion:
${confirmedHypothesis.supportingEvidence}
` : `
#### Next Steps

${nextSteps}
`}

---

## Current Consolidated Understanding (Updated)

${consolidatedUnderstanding}
```

#### Step 2.4: Update hypotheses.json

```json
{
  "iteration": 2,
  "timestamp": "2025-01-21T10:15:00+08:00",
  "hypotheses": [
    {
      "id": "H1",
      "status": "rejected",
      "verdict_reason": "Evidence shows key exists with valid value",
      "evidence": {...}
    },
    {
      "id": "H2",
      "status": "confirmed",
      "verdict_reason": "Log data confirms timing issue",
      "evidence": {...}
    }
  ],
  "corrections": [
    {
      "wrong_assumption": "...",
      "corrected_to": "...",
      "reason": "..."
    }
  ]
}
```

### Fix & Verification

#### Step 3.1: Apply Fix

Based on confirmed hypothesis, implement the fix in the affected files.

#### Step 3.2: Document Resolution

Append to `understanding.md`:

```markdown
### Iteration ${n} - Resolution (${timestamp})

#### Fix Applied

- Modified files: ${modifiedFiles.join(', ')}
- Fix description: ${fixDescription}
- Root cause addressed: ${rootCause}

#### Verification Results

${verificationResults}

#### Lessons Learned

What we learned from this debugging session:

1. ${lesson1}
2. ${lesson2}
3. ${lesson3}

#### Key Insights for Future

- ${insight1}
- ${insight2}
```

#### Step 3.3: Cleanup

Remove debug instrumentation by searching for region markers:

```javascript
const instrumentedFiles = Grep({
  pattern: "# region debug|// region debug",
  output_mode: "files_with_matches"
})

for (const file of instrumentedFiles) {
  // Remove content between region markers
  removeDebugRegions(file)
}
```

## Session Folder Structure

```
{projectRoot}/.workflow/.debug/DBG-{slug}-{date}/
├── debug.log           # NDJSON log (execution evidence)
├── understanding.md    # Exploration timeline + consolidated understanding
└── hypotheses.json     # Hypothesis history with verdicts
```

## Understanding Document Template

```markdown
# Understanding Document

**Session ID**: DBG-xxx-2025-01-21
**Bug Description**: [original description]
**Started**: 2025-01-21T10:00:00+08:00

---

## Exploration Timeline

### Iteration 1 - Initial Exploration (2025-01-21 10:00)

#### Current Understanding
...

#### Evidence from Code Search
...

#### Hypotheses Generated
...

### Iteration 2 - Evidence Analysis (2025-01-21 10:15)

#### Log Analysis Results
...

#### Corrected Understanding
- ~~[wrong]~~ → [corrected]

#### Analysis Results
...

---

## Current Consolidated Understanding

### What We Know
- [valid understanding points]

### What Was Disproven
- ~~[disproven assumptions]~~

### Current Investigation Focus
[current focus]

### Remaining Questions
- [open questions]
```

## Debug Log Format (NDJSON)

Each line is a JSON object:

```json
{"sid":"DBG-xxx-2025-01-21","hid":"H1","loc":"file.py:func:42","msg":"Check dict keys","data":{"keys":["a","b"],"target":"c","found":false},"ts":1734567890123}
```

| Field | Description |
|-------|-------------|
| `sid` | Session ID |
| `hid` | Hypothesis ID (H1, H2, ...) |
| `loc` | Code location |
| `msg` | What's being tested |
| `data` | Captured values |
| `ts` | Timestamp (ms) |

## Iteration Flow

```
First Call (BUG="error"):
   ├─ No session exists → Explore mode
   ├─ Extract error keywords, search codebase
   ├─ Document initial understanding in understanding.md
   ├─ Generate hypotheses
   ├─ Add logging instrumentation
   └─ Await user reproduction

After Reproduction (BUG="error"):
   ├─ Session exists + debug.log has content → Analyze mode
   ├─ Parse log, evaluate hypotheses
   ├─ Update understanding.md with:
   │   ├─ Evidence analysis results
   │   ├─ Corrected misunderstandings (strikethrough)
   │   ├─ New insights
   │   └─ Updated consolidated understanding
   ├─ Update hypotheses.json with verdicts
   └─ Decision:
       ├─ Confirmed → Fix → Document resolution
       ├─ Inconclusive → Add logging, document next steps
       └─ All rejected → Assisted new hypotheses

Output:
   ├─ {projectRoot}/.workflow/.debug/DBG-{slug}-{date}/debug.log
   ├─ {projectRoot}/.workflow/.debug/DBG-{slug}-{date}/understanding.md (evolving document)
   └─ {projectRoot}/.workflow/.debug/DBG-{slug}-{date}/hypotheses.json (history)
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Empty debug.log | Verify reproduction triggered the code path |
| All hypotheses rejected | Generate new hypotheses based on disproven assumptions |
| Fix doesn't work | Document failed fix attempt, iterate with refined understanding |
| >5 iterations | Review consolidated understanding, escalate with full context |
| Understanding too long | Consolidate aggressively, archive old iterations to separate file |

## Consolidation Rules

When updating "Current Consolidated Understanding":

1. **Simplify disproven items**: Move to "What Was Disproven" with single-line summary
2. **Keep valid insights**: Promote confirmed findings to "What We Know"
3. **Avoid duplication**: Don't repeat timeline details in consolidated section
4. **Focus on current state**: What do we know NOW, not the journey
5. **Preserve key corrections**: Keep important wrong→right transformations for learning

**Bad (cluttered)**:
```markdown
## Current Consolidated Understanding

In iteration 1 we thought X, but in iteration 2 we found Y, then in iteration 3...
Also we checked A and found B, and then we checked C...
```

**Good (consolidated)**:
```markdown
## Current Consolidated Understanding

### What We Know
- Error occurs during runtime update, not initialization
- Config value is None (not missing key)

### What Was Disproven
- ~~Initialization error~~ (Timing evidence)
- ~~Missing key hypothesis~~ (Key exists)

### Current Investigation Focus
Why is config value None during update?
```

## Key Features

| Feature | Description |
|---------|-------------|
| NDJSON logging | Structured debug log with hypothesis tracking |
| Hypothesis generation | Analysis-assisted hypothesis creation |
| Exploration documentation | understanding.md with timeline |
| Understanding evolution | Timeline + corrections tracking |
| Error correction | Strikethrough + reasoning for wrong assumptions |
| Consolidated learning | Current understanding section |
| Hypothesis history | hypotheses.json with verdicts |
| Analysis validation | At key decision points |

## When to Use

Best suited for:
- Complex bugs requiring multiple investigation rounds
- Learning from debugging process is valuable
- Team needs to understand debugging rationale
- Bug might recur, documentation helps prevention

---

**Now execute the debug-with-file workflow for bug**: $BUG

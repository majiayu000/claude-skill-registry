---
name: cfn-product-owner-decision
description: "Strategic decision-making for CFN Loop progression with robust parsing. Use when evaluating validator consensus and determining PROCEED/ITERATE/ABORT outcomes."
version: 2.0.0
tags: [cfn-loop, decision-making, product-owner, typescript, consensus]
status: production
---

# Product Owner Decision Skill

**Version:** 2.0.0 (TypeScript)
**Status:** Production (Dual: Bash + TypeScript)
**Purpose:** Strategic decision-making for CFN Loop progression with robust parsing

---

## Overview

Provides autonomous Product Owner decision execution with:
- **TypeScript + Bash hybrid approach**
- **Robust output parsing** (multiple fallback patterns)
- **Decision validation** (ensures PROCEED/ITERATE/ABORT detection)
- **Consensus on vapor detection** (prevents false completion claims)
- **Audit trail integration** (historical decision analysis)
- **Redis coordination** (orchestrator-controlled)

**Key Principle:** Parse Product Owner agent output, validate deliverables, signal orchestrator.

---

## Architecture

### Skill Components

```
.claude/skills/cfn-product-owner-decision/
├── SKILL.md                                  # This file
├── execute-decision.sh                       # Bash wrapper (main execution)
├── parse-decision.sh                         # Legacy bash parser (deprecated)
├── validate-deliverables.sh                  # Bash deliverable validator
└── src/
    ├── decision-parser.ts                    # TypeScript parser (core logic)
    └── index.ts                              # TypeScript exports
```

### CLI Integration

```
src/cli/parse-decision-cli.ts                # TypeScript CLI entry point
```

**Compiled Output:**
```
dist/cli/parse-decision-cli.js               # Compiled CLI binary
```

### Decision Flow

```
1. Orchestrator → Spawn Product Owner with context
2. Skill → Capture agent output
3. Skill → Parse decision (PROCEED/ITERATE/ABORT) via TypeScript parser
4. Skill → Validate deliverables (for PROCEED)
5. Skill → Detect consensus on vapor (plans without code)
6. Skill → Push decision to Redis
7. Skill → Signal completion to orchestrator
```

---

## Usage

### From Orchestrator (Primary Use)

```bash
# Modern: Use bash script (which uses TypeScript for parsing if available)
DECISION_RESULT=$(./.claude/skills/cfn-product-owner-decision/execute-decision.sh \
  --task-id "$TASK_ID" \
  --agent-id "$PO_UNIQUE_ID" \
  --consensus "$LOOP2_CONSENSUS" \
  --threshold "$CONSENSUS" \
  --iteration "$ITERATION" \
  --max-iterations "$MAX_ITERATIONS")

DECISION_TYPE=$(echo "$DECISION_RESULT" | jq -r '.decision')
```

### Direct TypeScript Parsing (Programmatic)

```typescript
import { DecisionParser } from './src/cfn-loop/product-owner/decision-parser';

const parser = new DecisionParser({
  strict: true,
  validateDeliverables: true,
  taskContext: 'Create TypeScript module',
  taskId: 'cfn-123'
});

const result = parser.parse(productOwnerOutput);
console.log(result.decision); // 'PROCEED' | 'ITERATE' | 'ABORT'
console.log(result.confidence); // 0.0-1.0
```

### CLI Parsing

```bash
# From stdin
echo "Decision: PROCEED" | npx claude-flow-novice parse-decision

# From file
npx claude-flow-novice parse-decision --input output.txt --json

# With validation
npx claude-flow-novice parse-decision \
  --input output.txt \
  --task-context "Create TypeScript module" \
  --json --verbose
```

---

## Parameters

### execute-decision.sh

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--task-id` | Yes | CFN Loop task identifier | `cfn-auth-system-123` |
| `--agent-id` | Yes | Product Owner agent ID | `product-owner-1` |
| `--consensus` | Yes | Loop 2 consensus score | `0.92` |
| `--threshold` | Yes | Consensus threshold | `0.90` |
| `--iteration` | Yes | Current iteration number | `2` |
| `--max-iterations` | Yes | Max iterations allowed | `10` |
| `--success-criteria` | No | JSON success criteria | `{"tests":"pass"}` |

### DecisionParser TypeScript Options

```typescript
interface DecisionParserOptions {
  strict?: boolean;           // Throw on parse failure (default: true)
  validateDeliverables?: boolean;  // Check for consensus on vapor (default: true)
  taskContext?: string;       // Task description for vapor detection
  taskId?: string;           // Task ID for reference
}
```

### parse-decision CLI Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input FILE` | `-i` | Read from file (default: stdin) | `-i output.txt` |
| `--output FILE` | `-o` | Write to file (default: stdout) | `-o result.json` |
| `--task-context TEXT` | - | Task description for vapor check | `--task-context "Create module"` |
| `--task-id ID` | - | Task ID for reference | `--task-id cfn-123` |
| `--json` | - | Output as JSON | `--json` |
| `--verbose` | `-v` | Include verbose output | `-v` |
| `--no-strict` | - | Non-strict parsing (default to ITERATE) | `--no-strict` |
| `--help` | `-h` | Show help message | `-h` |

---

## Decision Logic (GOAP Framework)

### PROCEED
```
Consensus >= Threshold
AND Deliverables exist (for implementation tasks)
AND Iteration <= Max
AND No consensus on vapor detected
```

### ITERATE
```
Consensus < Threshold
AND Iteration < Max

OR: Consensus >= Threshold BUT consensus on vapor detected
```

### ABORT
```
Iteration >= Max
OR Unrecoverable failure
OR Critical issue detected
```

---

## Output Parsing

### Pattern Matching (Robust Fallbacks)

The TypeScript parser implements multiple pattern matching strategies:

1. **Explicit Label:** `Decision: PROCEED` (case-insensitive)
2. **Standalone Keyword:** First line starting with decision (case-insensitive)
3. **Parentheses:** `(PROCEED)` anywhere in text
4. **JSON Format:** `{"decision": "PROCEED"}`
5. **First Keyword:** First occurrence of `PROCEED|ITERATE|ABORT`

**Example:**
```typescript
// All these formats are parsed correctly:
"Decision: PROCEED"              // Pattern 1
"PROCEED with deployment"        // Pattern 2
"My recommendation is (PROCEED)" // Pattern 3
'{"decision": "PROCEED"}'        // Pattern 4
"We should proceed..."           // Pattern 5 (case-insensitive)
```

### Confidence Extraction

Supports multiple formats:
```typescript
"Confidence: 0.95"        // Decimal
"Confidence: 95%"         // Percentage
'{"confidence": 0.92}'    // JSON
```

Clamped to 0.0-1.0 range. Default: 0.75

### Reasoning Extraction

Searches for:
- `Reasoning: ...`
- `Because: ...`
- `Explanation: ...`
- JSON `reasoning` field
- Paragraph after decision

### Deliverable Extraction

Parses bulleted lists:
```
Deliverables:
- Feature A
- Feature B
* Feature C
• Feature D
```

Also supports JSON arrays:
```json
{"deliverables": ["Feature A", "Feature B"]}
```

---

## Consensus on Vapor Detection

### What is "Consensus on Vapor"?

When agents agree quality threshold is met but **no actual code was created**.

Example: "Decision: PROCEED - all validators agreed" (but zero files changed)

### Detection

The parser checks:

1. **Task requires implementation?**
   - Keywords: `create|build|implement|generate|write|add|code|file|component|module|test`

2. **Actual files changed in git?**
   - Executes: `git status --short | grep -E "^(A|M|\?\?)" | wc -l`
   - If count = 0 AND deliverables claimed → **VAPOR**

3. **Response:**
   - Strict mode: Override PROCEED → ITERATE
   - Non-strict mode: Warn in validation errors

### Example

```
Input:  "Decision: PROCEED - Great planning!"
Task:   "Create TypeScript decision parser"
Git:    No files changed
Result: Decision overridden from PROCEED → ITERATE
Reason: "No files created despite implementation task"
```

---

## Audit Trail Integration

### Audit Data Retrieval

The skill retrieves historical data from `cfn-task-audit`:

```bash
AUDIT_DATA=$(./.claude/skills/cfn-task-audit/get-audit-data.sh \
  --task-id "$TASK_ID" \
  --mode combined \
  --format json)
```

### Extracted Insights

Product Owner receives:

- **Previous Decisions:** Earlier POD outcomes
- **Agent Performance:** Top-performing teams from history
- **Repeating Concerns:** Patterns in reviewer/tester feedback
- **Audit Records:** Full history count

### Impact

Product Owner can:
- Detect repeating issues (systematic problems)
- Recommend agents based on past performance
- Recognize when consensus is justified (strong history)
- Escalate if warnings repeat (e.g., security)

---

## Validation Rules

### Decision-Specific

| Decision | Requirements | Auto-Correction |
|----------|--------------|-----------------|
| **PROCEED** | Confidence ≥ 0.6, Deliverables verified | Vapor → ITERATE |
| **ITERATE** | Must provide reasoning for improvements | Warn if missing |
| **ABORT** | Confidence < 0.5 (indicates critical issue) | Warn if high confidence |

### Cross-Cutting

- Invalid confidence (< 0 or > 1): Clamped
- Empty output: Throws error
- Malformed output: Pattern fallbacks applied
- No decision found: Strict mode throws, non-strict defaults to ITERATE

---

## Return Value

### Bash (JSON)

```json
{
  "decision": "PROCEED",
  "reasoning": "Quality threshold exceeded",
  "confidence": 0.93,
  "iteration": 2,
  "consensus": 0.92,
  "threshold": 0.90,
  "timestamp": 1634567890,
  "audit_analysis": "Previous iterations showed improvement",
  "agent_performance_observations": "Team performed consistently",
  "audit_records_analyzed": 25,
  "audit_informed": true
}
```

### TypeScript (Structured)

```typescript
interface ParsedDecision {
  decision: 'PROCEED' | 'ITERATE' | 'ABORT';
  reasoning: string;
  deliverables: string[];
  confidence: number;
  validationErrors: string[];
  auditAnalysis?: string;
  agentPerformanceObservations?: string;
  raw: {
    fullOutput: string;
    decisionLine?: string;
  };
}
```

### CLI (Text or JSON)

**Text Format:**
```
Decision: PROCEED
Confidence: 92.5%
Reasoning: All validation gates passed
Deliverables: Module A, Module B
```

**JSON Format:**
```json
{
  "success": true,
  "decision": "PROCEED",
  "confidence": 0.925,
  "reasoning": "All validation gates passed",
  "deliverables": ["Module A", "Module B"],
  "validationErrors": []
}
```

---

## Error Handling

### Bash (execute-decision.sh)

```bash
# Validation failure
❌ ERROR: Could not parse decision from Product Owner output
Expected formats:
  - Decision: PROCEED|ITERATE|ABORT
  - Standalone keyword
  - JSON format

# File error
❌ ERROR: Product Owner output file missing or empty

# Timeout
❌ ERROR: Product Owner timed out after 300s
```

### TypeScript (DecisionParser)

```typescript
throw new DecisionParserError(
  'Could not extract decision from Product Owner output',
  'NO_DECISION_FOUND',
  { availablePatterns: [...], hint: '...' }
);
```

### CLI (parse-decision)

```bash
# Exit code mapping
0 - PROCEED
1 - ITERATE
2 - ABORT
3 - Parse error (malformed input, missing decision, etc.)

# Error output
Error: Could not parse decision (--json for details)
Error Code: NO_DECISION_FOUND
```

---

## Testing

### Unit Tests

```bash
# TypeScript parser tests (90%+ coverage)
npm test -- tests/unit/cfn-loop/product-owner/decision-parser.test.ts

# CLI tests
npm test -- tests/unit/cli/parse-decision-cli.test.ts
```

### Test Coverage

- **Decision Extraction:** All 5 pattern types
- **Confidence Parsing:** Decimal, percentage, JSON
- **Reasoning Extraction:** 4 different formats
- **Deliverable Extraction:** Bullets, JSON
- **Validation:** Type-specific rules
- **Vapor Detection:** Implementation detection, git status
- **Error Handling:** Strict/non-strict modes
- **CLI:** Arguments, formatting, exit codes

### Integration Tests

```bash
# Test with real Product Owner output
echo "Decision: PROCEED
Reasoning: All tests pass.
Deliverables:
- Feature A
- Feature B
Confidence: 0.92" | npx claude-flow-novice parse-decision --json
```

---

## Migration from Bash (v1.x)

### Backward Compatibility

The bash script (`execute-decision.sh`) **still works unchanged**.

Existing orchestrators continue to use bash without modification.

### Opt-In TypeScript Usage

To use TypeScript parsing in orchestrator:

```bash
# Current (bash): Still works
DECISION_JSON=$(./.claude/skills/cfn-product-owner-decision/execute-decision.sh \
  --task-id "$TASK_ID" ...)

# New (TypeScript): Available if needed
npx claude-flow-novice parse-decision --input output.txt --json
```

### New Features (TypeScript Only)

- **Consensus on Vapor Detection:** Automatic override PROCEED → ITERATE
- **Audit Trail Integration:** Historical decision analysis
- **Multiple Output Formats:** Text and JSON
- **CLI Flexibility:** Programmatic and shell integration
- **Better Error Context:** Detailed error codes and suggestions

---

## Performance

### Parsing

- **Bash:** ~50ms per parse (regex-heavy)
- **TypeScript:** ~10ms per parse (optimized)
- **CLI (TypeScript):** ~200ms (includes Node startup)

For orchestrator use (bash script), negligible impact on loop timing.

For high-volume parsing, use TypeScript directly.

### Memory

- **Bash:** ~5MB process
- **TypeScript:** ~40MB Node process (startup cost)
- **Shared:** Output analyzed once, results reused

---

## Examples

### Example 1: Simple PROCEED

Input:
```
Decision: PROCEED

The quality threshold has been exceeded at 0.92 (threshold: 0.90).
All validators provided positive feedback.

Confidence: 0.92
```

Output:
```json
{
  "decision": "PROCEED",
  "confidence": 0.92,
  "reasoning": "The quality threshold has been exceeded...",
  "deliverables": [],
  "validationErrors": [],
  "raw": { "decisionLine": "Decision: PROCEED" }
}
```

Exit Code: 0

### Example 2: ITERATE with Warnings

Input:
```
Decision: ITERATE

Reasoning: Security concerns raised by validator.
Test coverage is 85% (need 90%).

Confidence: 0.65
```

Output:
```json
{
  "decision": "ITERATE",
  "confidence": 0.65,
  "reasoning": "Security concerns raised...",
  "deliverables": [],
  "validationErrors": [
    "ITERATE decision should have lower confidence (<0.5)"
  ],
  "raw": { "decisionLine": "Decision: ITERATE" }
}
```

Exit Code: 1

### Example 3: Vapor Detection

Input:
```
Decision: PROCEED
Reasoning: Great planning session!
Deliverables: Comprehensive design documentation

Confidence: 0.85
```

Task Context: `Create TypeScript decision parser module`
Git Status: No files changed

Output:
```json
{
  "decision": "ITERATE",
  "confidence": 0.70,
  "reasoning": "Override PROCEED → ITERATE: No files created despite implementation task",
  "deliverables": [],
  "validationErrors": [
    "No files created despite implementation task - consensus on vapor detected"
  ]
}
```

Exit Code: 1 (overridden)

---

## Troubleshooting

### Decision Not Detected

**Symptom:** `ERROR: Could not parse decision`

**Solution:**
- Check output contains exact keyword: PROCEED, ITERATE, or ABORT
- Verify keyword not inside code block (triple backticks)
- Try non-strict mode: `--no-strict`

### Low Confidence Warnings

**Symptom:** Validation warns about low confidence

**Solution:**
- PROCEED should have confidence ≥ 0.6 (indicates certainty)
- ABORT should have confidence < 0.5 (indicates critical issue)
- Review Product Owner reasoning for concerns

### Vapor Detection False Positives

**Symptom:** PROCEED incorrectly overridden to ITERATE

**Solution:**
- Ensure task description includes implementation keywords
- Check git status reflects actual file changes
- Use `--task-context` CLI option to specify task type

### CLI Timeout

**Symptom:** CLI hangs when reading stdin

**Solution:**
- Pipe input: `cat file | npx claude-flow-novice parse-decision`
- Use file input: `npx claude-flow-novice parse-decision -i file.txt`
- Increase timeout via environment: `STDIN_TIMEOUT=10000` (ms)

---

## Related Skills

- **cfn-redis-coordination:** Redis signaling
- **cfn-task-audit:** Audit data retrieval
- **cfn-backlog-management:** Deferred item processing
- **cfn-loop-validation:** Loop progression validation

---

## References

- **CFN Loop Architecture:** `docs/CFN_LOOP_ARCHITECTURE.md`
- **Success Criteria:** `docs/guides/SUCCESS_CRITERIA_EXAMPLES.md`
- **Test-Driven Gates:** `docs/guides/TEST_DRIVEN_CFN_LOOP_GUIDE.md`
- **Orchestrator:** `./.claude/skills/cfn-loop-orchestration/orchestrate.sh`

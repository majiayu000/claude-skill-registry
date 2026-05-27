---
name: detect
description: Determine whether a specific pattern, entity, or condition exists in the given data. Use when searching for patterns, checking existence, validating presence, or finding signals.
argument-hint: "[target] [pattern-type] [threshold]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Scan data sources to determine whether a specified pattern, entity, or condition is present. Detection is binary (present/absent) with associated signal strength.

**Success criteria:**
- Clear boolean determination of presence/absence
- At least one evidence anchor for positive detections
- False positive risk assessment provided
- Confidence score justified by evidence quality

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | string\|object | The data source to scan (file path, URL, or structured data) |
| `pattern` | Yes | string\|regex | The pattern, entity type, or condition to detect |
| `threshold` | No | object | Detection sensitivity settings (e.g., min_matches, confidence_floor) |
| `scope` | No | string | Limit search to specific regions (e.g., "functions", "imports", "comments") |

## Procedure

1) **Define detection criteria**: Clarify exactly what constitutes a positive detection
   - Convert vague patterns to concrete search terms or regex
   - Establish minimum evidence threshold for positive detection

2) **Scan target systematically**: Search the target data for matching signals
   - Use Grep for text patterns with appropriate flags (-i for case-insensitive, etc.)
   - Use Read for structural inspection when pattern requires context
   - Record location (file:line) for each potential match

3) **Evaluate signal strength**: For each match, assess how strongly it indicates true presence
   - Strong: exact match with clear context
   - Medium: partial match or ambiguous context
   - Weak: possible match requiring human verification

4) **Assess false positive risk**: Determine likelihood that detections are spurious
   - High risk: generic patterns, noisy data, few matches
   - Low risk: specific patterns, clean data, multiple corroborating signals

5) **Ground claims**: Attach evidence anchors to all detection signals
   - Format: `file:line` for file-based targets
   - Include snippet of matched content for verification

6) **Format output**: Structure results according to the output contract below

## Output Contract

Return a structured object:

```yaml
detected: boolean  # True if pattern/entity was found
target_type: string  # What was being detected (e.g., "security vulnerability", "deprecated API")
signals:
  - signal: string  # Description of what was found
    strength: low | medium | high  # Signal strength
    location: string  # file:line or path where found
false_positive_risk: low | medium | high  # Likelihood of spurious detection
confidence: number  # 0.0-1.0 based on evidence quality
evidence_anchors: array[string]  # File:line references
assumptions: array[string]  # Explicit assumptions made
next_actions: array[string]  # 0-3 suggested follow-ups if uncertain
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `detected` | boolean | True if the target pattern/entity was found |
| `target_type` | string | Category of what was searched for |
| `signals` | array | List of individual detection signals with strength |
| `false_positive_risk` | enum | Assessment of detection reliability |
| `confidence` | number | 0.0-1.0 based on evidence completeness |
| `evidence_anchors` | array[string] | File:line references or tool outputs |
| `assumptions` | array[string] | Explicitly stated assumptions |

## Examples

### Example 1: Detect SQL Injection Vulnerability

**Input:**
```yaml
target: src/api/user_controller.py
pattern: "SQL injection pattern"
threshold:
  min_matches: 1
```

**Output:**
```yaml
detected: true
target_type: "SQL injection vulnerability"
signals:
  - signal: "String concatenation in SQL query with user input"
    strength: high
    location: "src/api/user_controller.py:47"
  - signal: "Raw SQL execution without parameterization"
    strength: medium
    location: "src/api/user_controller.py:52"
false_positive_risk: low
confidence: 0.85
evidence_anchors:
  - "src/api/user_controller.py:47"
  - "src/api/user_controller.py:52"
assumptions:
  - "User input flows from request.params to query variable"
  - "No input sanitization in calling function"
next_actions:
  - "Verify data flow from user input to SQL query"
  - "Check for parameterized query alternatives in codebase"
```

**Evidence pattern:** Grep for SQL keywords combined with string formatting patterns, then Read to verify context.

---

### Example 2: Detect Deprecated API Usage

**Input:**
```yaml
target: src/
pattern: "componentWillMount|componentWillReceiveProps"
scope: "*.jsx,*.tsx"
```

**Output:**
```yaml
detected: true
target_type: "deprecated React lifecycle method"
signals:
  - signal: "componentWillMount usage"
    strength: high
    location: "src/components/Dashboard.jsx:23"
false_positive_risk: low
confidence: 0.95
evidence_anchors:
  - "src/components/Dashboard.jsx:23"
assumptions:
  - "Project uses React 16.3+ where these methods are deprecated"
next_actions:
  - "Migrate to componentDidMount or useEffect hook"
```

## Verification

- [ ] Output contains `detected` boolean matching signal presence
- [ ] At least one evidence anchor exists for positive detections
- [ ] Confidence score correlates with number and strength of signals
- [ ] All referenced file:line locations are valid and accessible
- [ ] False positive risk assessment is justified

**Verification tools:** Read (to verify file:line references exist)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not access paths outside the specified target scope
- Do not modify any files during detection
- Stop and request clarification if detection criteria are ambiguous
- Report uncertainty rather than guessing when signals are weak

## Composition Patterns

**Commonly follows:**
- `inspect` - Detection often follows initial observation of a system
- `search` - Detection may refine broad search results

**Commonly precedes:**
- `identify` - Positive detection often leads to classification of what was found
- `estimate-risk` - Detection of anomalies feeds into risk assessment
- `plan` - Detected issues may trigger remediation planning

**Anti-patterns:**
- Never use detect for complex entity classification (use `identify` instead)
- Avoid detect for quantitative assessment (use `estimate` instead)

**Workflow references:**
- See `reference/composition_patterns.md#risk-assessment` for detection in risk workflows
- See `reference/composition_patterns.md#observe-model-act` for detection in agentic loops

---
name: classify
description: Assign labels or categories to items based on characteristics. Use when categorizing entities, tagging content, identifying types, or labeling data according to a taxonomy.
argument-hint: "[item] [taxonomy] [multi-label]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
layer: UNDERSTAND
---

## Intent

Assign one or more labels from a defined taxonomy to items based on their observed characteristics. This capability bridges detection and reasoning by providing semantic categorization.

**Success criteria:**
- Item assigned at least one label from taxonomy
- Label assignment supported by evidence
- Confidence scores reflect classification certainty
- Ambiguous cases explicitly flagged

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `item` | Yes | any | The item to classify (entity, document, code, data) |
| `taxonomy` | No | string\|array | Classification scheme or list of valid labels |
| `multi_label` | No | boolean | Whether multiple labels can be assigned (default: false) |
| `context` | No | object | Additional context to inform classification |

## Procedure

1) **Examine the item**: Gather characteristics relevant to classification
   - Identify distinguishing features
   - Note structural patterns, content type, metadata
   - Collect evidence for each observed characteristic

2) **Understand the taxonomy**: Clarify the classification scheme
   - If taxonomy provided, use those labels exclusively
   - If no taxonomy, infer appropriate categories from context
   - Define clear boundaries between categories

3) **Match characteristics to labels**: Evaluate fit for each potential label
   - Score how well item characteristics match each category
   - Consider edge cases and borderline classifications
   - Note which features drive each potential classification

4) **Assign labels**: Select the most appropriate label(s)
   - For single-label: choose highest confidence match
   - For multi-label: include all labels above confidence threshold
   - Flag if no label is a strong match

5) **Ground classification**: Document evidence supporting each label
   - Reference specific characteristics that drove classification
   - Note any characteristics that contradict the assignment

## Output Contract

Return a structured object:

```yaml
labels:
  - label: string  # Assigned category/label
    confidence: number  # 0.0-1.0 for this specific label
    evidence: array[string]  # Characteristics supporting this label
probabilities:  # Optional: full probability distribution
  label_1: number
  label_2: number
primary_label: string  # Highest confidence label
ambiguous: boolean  # True if classification is uncertain
confidence: 0..1  # Overall classification confidence
evidence_anchors: ["file:line", "characteristic:value"]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `labels` | array | Assigned labels with confidence and evidence |
| `probabilities` | object | Probability for each possible label |
| `primary_label` | string | Single best classification |
| `ambiguous` | boolean | Whether classification is uncertain |
| `confidence` | number | 0.0-1.0 overall confidence |

## Examples

### Example 1: Classify Code File

**Input:**
```yaml
item: "src/services/payment_processor.rb"
taxonomy: ["service", "model", "controller", "helper", "concern"]
```

**Output:**
```yaml
labels:
  - label: "service"
    confidence: 0.92
    evidence:
      - "Located in services/ directory"
      - "Class name ends with 'Processor'"
      - "Contains business logic methods without persistence"
probabilities:
  service: 0.92
  model: 0.03
  controller: 0.02
  helper: 0.02
  concern: 0.01
primary_label: "service"
ambiguous: false
confidence: 0.92
evidence_anchors:
  - "src/services/payment_processor.rb:1"
  - "src/services/payment_processor.rb:15-45"
assumptions:
  - "Directory structure follows Rails conventions"
```

### Example 2: Classify with Ambiguity

**Input:**
```yaml
item: "User reported issue: 'App crashes on login'"
taxonomy: ["bug", "feature-request", "question", "documentation"]
multi_label: true
```

**Output:**
```yaml
labels:
  - label: "bug"
    confidence: 0.75
    evidence:
      - "Reports crash behavior"
      - "Describes unexpected failure"
  - label: "question"
    confidence: 0.40
    evidence:
      - "Lacks reproduction steps"
      - "May be user error or configuration"
probabilities:
  bug: 0.75
  question: 0.40
  feature-request: 0.05
  documentation: 0.10
primary_label: "bug"
ambiguous: true
confidence: 0.65
evidence_anchors:
  - "issue:title"
  - "issue:body"
assumptions:
  - "Crash is not expected behavior"
  - "User has attempted normal login flow"
```

## Verification

- [ ] At least one label assigned with confidence > 0.3
- [ ] Evidence exists for each assigned label
- [ ] Labels are from specified taxonomy (if provided)
- [ ] Ambiguous flag set when confidence < 0.7
- [ ] Probabilities sum to ~1.0 (if provided)

**Verification tools:** Read (to verify evidence references)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not invent labels outside the provided taxonomy
- Flag uncertainty rather than forcing low-confidence classifications
- Do not access data beyond what's needed for classification
- Note when item characteristics are insufficient for reliable classification

## Composition Patterns

**Commonly follows:**
- `detect` - Classify items after detecting their presence
- `observe` - Classify based on observed characteristics
- `retrieve` - Classify retrieved items

**Commonly precedes:**
- `compare` - Classification enables comparison within categories
- `plan` - Classified items inform planning decisions
- `generate` - Classification guides content generation

**Anti-patterns:**
- Never use classify for binary detection (use `detect`)
- Avoid classify when precise measurement needed (use `measure`)

**Workflow references:**
- See `reference/workflow_catalog.yaml#capability_gap_analysis` for classification usage

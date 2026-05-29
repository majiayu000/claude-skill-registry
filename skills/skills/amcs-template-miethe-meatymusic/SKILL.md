---
name: amcs-{SKILL_NAME}-{ACTION}
description: {ONE_SENTENCE_PURPOSE}. Use when {TRIGGER_CONDITION}.
---

# AMCS {Skill Title}

{2-3 sentence overview of what this skill does and why it exists in the AMCS workflow.}

## When to Use

Invoke this skill {POSITION_IN_WORKFLOW} when {CONDITION}. This node {RUNS_IN_PARALLEL/SEQUENTIALLY} with {OTHER_NODES} and feeds into {DOWNSTREAM_NODES}.

## Input Contract

```yaml
inputs:
  - name: {input_1_name}
    type: {schema_reference}  # e.g., amcs://schemas/sds-1.0.json
    required: true/false
    description: {What this input provides}
  - name: {input_2_name}
    type: {type}
    required: true/false
    description: {What this input provides}
  - name: seed
    type: integer
    required: true
    description: Determinism seed (use seed+{NODE_INDEX} for this node)
```

## Output Contract

```yaml
outputs:
  - name: {output_name}
    type: {schema_reference}
    description: |
      {Multi-line description of output structure}
      - field_1: {description}
      - field_2: {description}
      - _hash: SHA-256 hash for provenance tracking
```

## Determinism Requirements

- **Seed**: `run_seed + {NODE_INDEX}` for any stochastic operations
- **Temperature**: {VALUE} (or N/A if no LLM generation)
- **Top-p**: {VALUE} (or N/A)
- **Retrieval**: {NONE | Pinned by content hash}
- **Hashing**: Hash final output for provenance tracking
- **Key Invariant**: Same inputs + seed => identical outputs

## Constraints & Policies

{List all constraints this skill must enforce}

- {CONSTRAINT_1}: {RULE}
- {CONSTRAINT_2}: {RULE}
- {POLICY_1}: {ENFORCEMENT}
- {VALIDATION_1}: {CHECKS}

Example:
- Tempo MUST fall within blueprint's `tempo_range` for primary genre
- Tags MUST NOT conflict per `taxonomies/tag_conflict_matrix.json`
- Profanity filter applies to all text fields
- Maximum {X} {ITEMS} to avoid {PROBLEM}

## Implementation Guidance

{Detailed step-by-step implementation instructions}

### Step 1: {First Major Step}

{Detailed instructions for this step}

1. {Sub-step 1}
2. {Sub-step 2}
3. {Sub-step 3}

**Example**:
```python
# Code example showing pattern
```

### Step 2: {Second Major Step}

{Detailed instructions}

**Algorithm**:
1. {Algorithm step}
2. {Algorithm step}
3. Score = {FORMULA}

**Target**: {THRESHOLD}

**Example**:
```
{Concrete example with data}
```

**Issues**:
- If {CONDITION}: `"{ERROR_MESSAGE}"`

### Step {N}: Validate and Return

1. Validate output against `{SCHEMA_REFERENCE}`
2. Compute SHA-256 hash of output
3. Return output with hash in metadata

**Example Output**:
```json
{
  "{field}": "{value}",
  "_hash": "abc123...",
  "_metadata": {}
}
```

## Examples

### Example 1: {Typical Use Case}

**Input**:
```json
{
  "{input_field}": "{value}",
  "seed": 42
}
```

**Output**:
```json
{
  "{output_field}": "{value}",
  "_hash": "abc123..."
}
```

### Example 2: {Edge Case or Variation}

**Input**:
```json
{
  "{input_field}": "{different_value}",
  "seed": 100
}
```

**Output**:
```json
{
  "{output_field}": "{result}",
  "_hash": "def456..."
}
```

### Example 3: {Error Case}

**Input**:
```json
{
  "{invalid_input}": "{bad_value}"
}
```

**Expected Error**:
```
ValueError: {ERROR_MESSAGE}
```

## Testing

### Basic Functionality Test

Test that the skill produces valid output for typical inputs.

### Determinism Test

Critical: Run with same inputs + seed 10 times, verify identical outputs.

**Test Pattern**:
```python
@pytest.mark.parametrize("run_number", range(10))
async def test_{skill}_determinism(sample_input, context, run_number):
    result = await {skill_function}(sample_input, context)

    if run_number == 0:
        pytest.first_hash = result["_hash"]

    assert result["_hash"] == pytest.first_hash
```

### Input Validation Test

Test that invalid inputs are rejected with clear error messages.

### Policy Enforcement Test

Test that constraints and policies are properly enforced.

## Common Pitfalls

1. **{Pitfall 1}**: {Description of what goes wrong and how to avoid}
2. **{Pitfall 2}**: {Description}
3. **{Pitfall 3}**: {Description}
4. **Determinism Loss**: {What breaks determinism in this skill}
5. **Hash Omission**: Missing provenance hash breaks traceability

## Troubleshooting

### Issue: {Common Problem}

**Symptoms**: {What the user sees}

**Cause**: {Why this happens}

**Solution**: {How to fix it}

### Issue: Determinism Test Failing

**Symptoms**: Different outputs from same inputs + seed

**Cause**:
- Unseeded randomness
- Non-deterministic retrieval
- Datetime dependencies
- High temperature/top-p

**Solution**:
- Use `context.seed` for all random operations
- Pin retrieval by content hash
- Remove datetime.now() calls
- Set temperature ≤ 0.3, top_p ≤ 0.9

## Related Skills

- **{UPSTREAM_SKILL}**: Provides inputs to this skill
- **{DOWNSTREAM_SKILL}**: Consumes outputs from this skill
- **{PARALLEL_SKILL}**: Runs in parallel with this skill

## References

- PRD: `docs/project_plans/PRDs/{prd_file}.prd.md`
- Workflow: `docs/project_plans/PRDs/claude_code_orchestration.prd.md` (section {X})
- Blueprint: `docs/hit_song_blueprint/AI/{genre}_blueprint.md`
- Schema: `schemas/{schema_name}.json`

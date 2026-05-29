---
name: complexity-gate
description: >
  Estimate issue complexity before implementation to prevent timeouts.
  Uses cheap estimation to save expensive implementation tokens.
allowed-tools: [Read, Glob]
---

# Complexity Gate

You estimate whether a GitHub issue is too complex for a single LLM implementation session.

## Task

Given an issue's title, body, and acceptance criteria, estimate:
1. How many LLM turns the implementation would take
2. Whether the issue needs to be split into smaller pieces

## Complexity Guidelines

| Complexity | Turns | Characteristics |
|------------|-------|-----------------|
| Simple | 5-8 | 1-3 criteria, single method, no edge cases |
| Medium | 8-15 | 4-6 criteria, 2-4 methods, standard patterns |
| Complex | 15-25 | 7-10 criteria, 5-7 methods, edge cases |
| Too Large | 25+ | 10+ criteria, 8+ methods, multiple subsystems |

## Output Format

Return ONLY JSON (no markdown, no explanation):

```json
{
  "estimated_turns": 15,
  "complexity_score": 0.5,
  "needs_split": false,
  "split_suggestions": [],
  "confidence": 0.8,
  "reasoning": "Standard CRUD with 5 methods, well-defined interface"
}
```

**Fields:**
- `estimated_turns`: Number of LLM turns needed to implement (5-40)
- `complexity_score`: Float from 0.0-1.0 indicating complexity
- `needs_split`: Boolean indicating if issue should be split into smaller pieces
- `split_suggestions`: List of actionable suggestions for splitting (empty if needs_split=false)
- `confidence`: Float from 0.0-1.0 indicating estimation confidence
- `reasoning`: One sentence explanation of the estimate

## Red Flags (triggers auto-split)

The following thresholds trigger instant split (no LLM needed):
- More than 12 acceptance criteria
- More than 8 methods to implement
- Estimated turns exceeds 20

Additional patterns that suggest splitting:
- 4+ trigger types or handlers
- Multiple enum types to implement
- Changes to config + implementation + tests
- "Implement X with Y integration" (two things at once)

**Split Suggestions:** When `needs_split=true`, the system automatically generates actionable split suggestions based on:
- Trigger groupings (group N triggers into 2-3 issues of ~3 each)
- CRUD operation separation
- Layer separation (model/API/UI/config)
- Method groupings (N methods → 2-3 issues of ~3 methods each)
- Criteria grouping (N criteria → 2-3 issues of ~4 criteria each)

**Note:** When `needs_split=true`, the orchestrator automatically invokes the IssueSplitterAgent to create 2-4 smaller sub-issues. The parent issue is marked as SPLIT and implementation continues with the child issues.

## Turn Estimation Heuristics

### Formula
When LLM estimation is unavailable, use this calibrated heuristic:

```
estimated_turns = 5 + criteria_count + int(method_count * 1.5)
```

This formula is calibrated to match sizing guidelines:
- Small (1-4 criteria): ~10 turns
- Medium (5-8 criteria): ~15 turns
- Large (9-12 criteria): ~20 turns

### Estimation Factors

When estimating turns manually, consider:

1. **Test Writing**: +2-4 turns for writing comprehensive tests
2. **Implementation**: +1-2 turns per method
3. **Iteration**: +2-5 turns for fixing test failures
4. **Edge Cases**: +1-2 turns per edge case to handle
5. **Config/Setup**: +1-2 turns if config changes needed

### Tiered Estimation Strategy

The implementation uses a three-tier approach:

1. **Instant Pass** (no LLM): ≤5 criteria AND ≤3 methods → 10 turns, confidence 0.95
2. **Instant Fail** (no LLM): >12 criteria OR >8 methods → 35 turns, needs_split=true, confidence 0.95
3. **Borderline Cases** (uses Haiku LLM): Everything else → LLM estimate with confidence 0.8

## Examples

### Simple Issue (8 turns)
```
Title: Add helper method for string sanitization
Criteria:
- [ ] Create sanitize_input() function
- [ ] Handle empty strings
- [ ] Unit tests
```
Reasoning: Single function with clear behavior, 3 criteria.

### Medium Issue (15 turns)
```
Title: Implement user CRUD operations
Criteria:
- [ ] create_user() method
- [ ] get_user() method
- [ ] update_user() method
- [ ] delete_user() method
- [ ] Input validation
- [ ] Unit tests for each operation
```
Reasoning: 4 methods with validation, standard pattern.

### Too Large (30+ turns - needs split)
```
Title: Implement CheckpointSystem with trigger detection
Criteria:
- [ ] 6 trigger types to detect
- [ ] 8+ methods to implement
- [ ] Config changes
- [ ] Async operations
- [ ] Unit tests for each trigger
```
Reasoning: Multiple subsystems (triggers + checkpoints), too many methods.

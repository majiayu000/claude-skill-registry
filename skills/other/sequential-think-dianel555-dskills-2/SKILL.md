---
name: sequential-think
description: |
  Multi-step reasoning engine for complex analysis and systematic problem solving. Use when: (1) Complex debugging scenarios with multiple layers, (2) Architectural analysis and system design, (3) Problems requiring hypothesis testing and validation, (4) Multi-component failure investigation, (5) Performance bottleneck identification. Triggers: "--think", "--think-hard", "--ultrathink", "analyze step by step", "break down this problem", "systematic analysis". IMPORTANT: Do NOT use for simple single-step tasks.
---

# Sequential Think

Structured iterative thinking for complex problem-solving. Standalone CLI only (no MCP dependency).

## Execution Methods

Run `scripts/sequential_think_cli.py` via Bash:

```bash
# Process a thought
python scripts/sequential_think_cli.py think \
  --thought "First, let me analyze the problem structure..." \
  --thought-number 1 \
  --total-thoughts 5

# Continue thinking chain
python scripts/sequential_think_cli.py think \
  --thought "Based on step 1, I hypothesize that..." \
  --thought-number 2 \
  --total-thoughts 5

# Revise a previous thought
python scripts/sequential_think_cli.py think \
  --thought "Reconsidering step 1, I realize..." \
  --thought-number 3 \
  --total-thoughts 5 \
  --is-revision \
  --revises-thought 1

# Branch into alternative path
python scripts/sequential_think_cli.py think \
  --thought "Alternative approach: what if we..." \
  --thought-number 4 \
  --total-thoughts 6 \
  --branch-from 2 \
  --branch-id "alt-approach"

# Final thought (complete chain)
python scripts/sequential_think_cli.py think \
  --thought "Conclusion: the solution is..." \
  --thought-number 5 \
  --total-thoughts 5 \
  --no-next

# View thought history
python scripts/sequential_think_cli.py history [--format json|text]

# Clear thought history
python scripts/sequential_think_cli.py clear
```

## Core Principles

### Iterative Thinking Process
- Each tool call = one "thought" in the chain
- Build upon, question, or revise previous thoughts
- Express uncertainty when it exists

### Dynamic Thought Count
- Start with initial estimate of `totalThoughts`
- Adjust up/down as understanding evolves
- Add more thoughts even after reaching initial end

### Hypothesis-Driven Approach
1. Generate hypotheses as potential solutions emerge
2. Verify hypotheses based on chain-of-thought steps
3. Repeat until satisfied with solution

### Completion Criteria
- Only set `nextThoughtNeeded: false` when truly finished
- Must have satisfactory, verified answer
- Don't rush to conclusion

## When to Use

| Scenario | Use Sequential Think |
|----------|---------------------|
| Complex debugging (3+ layers) | ✅ Yes |
| Architectural analysis | ✅ Yes |
| Multi-component investigation | ✅ Yes |
| Performance bottleneck analysis | ✅ Yes |
| Root cause analysis | ✅ Yes |
| Simple explanation | ❌ No |
| Single-file change | ❌ No |
| Straightforward fix | ❌ No |

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `thought` | string | Yes | Current thinking step content |
| `thoughtNumber` | int | Yes | Current position in sequence (1-based) |
| `totalThoughts` | int | Yes | Estimated total thoughts needed |
| `nextThoughtNeeded` | bool | No | Whether more thinking needed (default: true) |
| `isRevision` | bool | No | Whether this revises previous thinking |
| `revisesThought` | int | No | Which thought number is being reconsidered |
| `branchFromThought` | int | No | Branching point thought number |
| `branchId` | string | No | Identifier for current branch |
| `needsMoreThoughts` | bool | No | Signal that more thoughts needed beyond estimate |

## Output Format

```json
{
  "thoughtNumber": 3,
  "totalThoughts": 5,
  "nextThoughtNeeded": true,
  "branches": ["alt-approach"],
  "thoughtHistoryLength": 3
}
```

## Workflow Pattern

### Phase 1: Problem Decomposition
```
Thought 1: Identify problem scope and constraints
Thought 2: Break into sub-problems
Thought 3: Identify dependencies between sub-problems
```

### Phase 2: Hypothesis Generation
```
Thought 4: Generate initial hypothesis
Thought 5: Identify evidence needed to verify
```

### Phase 3: Verification & Iteration
```
Thought 6: Test hypothesis against evidence
Thought 7: Revise if needed (isRevision=true)
Thought 8: Branch if alternative path promising
```

### Phase 4: Conclusion
```
Final Thought: Synthesize findings, provide answer (nextThoughtNeeded=false)
```

## Best Practices

1. **Start with estimate, adjust as needed**
   - Initial `totalThoughts` is just a guess
   - Increase if problem more complex than expected
   - Decrease if solution found early

2. **Use revisions for course correction**
   - Mark `isRevision=true` when reconsidering
   - Reference `revisesThought` for clarity

3. **Branch for alternative approaches**
   - Use `branchFromThought` to explore alternatives
   - Give meaningful `branchId` names

4. **Filter irrelevant information**
   - Each thought should advance toward solution
   - Ignore tangential details

5. **Don't rush completion**
   - Only `nextThoughtNeeded=false` when truly done
   - Verify hypothesis before concluding

## Anti-Patterns

| Prohibited | Correct |
|------------|---------|
| Use for simple tasks | Reserve for complex multi-step problems |
| Skip thought numbers | Always increment correctly |
| Conclude without verification | Verify hypothesis before final thought |
| Ignore previous thoughts | Build upon or explicitly revise |
| Fixed totalThoughts | Adjust as understanding evolves |

## Integration with Other Tools

### With ACE-Tool
```
ACE-Tool → align current state → Sequential Think → analyze and plan
```

### With Context7
```
Sequential Think → coordinate analysis → Context7 → provide official patterns
```

### With Serena
```
Serena → symbol-level exploration → Sequential Think → systematic analysis
```

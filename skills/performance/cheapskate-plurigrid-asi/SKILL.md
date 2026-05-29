---
name: cheapskate
description: Cheapskate Skill
version: 1.0.0
---

# Cheapskate Skill

**Trit**: -1 (MINUS - validator/constrainer)
**Purpose**: Minimize Amp thread costs through token efficiency

---

## Core Principles

### 1. Token Conservation
- **Terse responses**: 1-3 sentences unless detail requested
- **No preamble/postamble**: Skip "I'll help you with..." and summaries
- **Code over prose**: Show code, not explanations
- **Links over content**: Reference files, don't paste them

### 2. Tool Call Efficiency
- **Parallel reads**: Batch independent Read/Grep calls
- **Targeted searches**: Use glob patterns, not broad scans
- **Single-pass edits**: Plan before editing, don't iterate
- **Skip redundant checks**: Trust previous results

### 3. Subagent Economics
- **Task tool for isolation**: Heavy work in subagents (tokens not returned)
- **Bounded prompts**: Subagent prompts < 500 tokens
- **No round-trips**: Give subagents full context upfront
- **Kill early**: Cancel subagents if direction changes

### 4. Context Window Management
- **Skill loading**: Only load skills when needed
- **File excerpts**: Read ranges, not full files
- **Summarize large outputs**: Truncate verbose tool results
- **Avoid re-reading**: Cache file contents mentally

---

## Anti-Patterns (Token Wasters)

| Pattern | Cost | Fix |
|---------|------|-----|
| Reading entire files | High | Use line ranges `[1, 50]` |
| Sequential tool calls | Medium | Parallelize independents |
| Explaining before doing | Medium | Just do it |
| Asking permission | Low-Medium | Act, don't ask |
| Repeating user's question | Low | Skip acknowledgment |
| Long error explanations | Medium | Terse: "Error: X. Fix: Y" |
| Multiple edit iterations | High | Plan first, single edit |
| Loading unused skills | Medium | Load on-demand |

---

## Efficient Patterns

### File Operations
```
# Bad: Read full 2000-line file
Read("/path/to/big.py")

# Good: Read relevant section
Read("/path/to/big.py", [100, 150])

# Better: Grep first, then targeted read
Grep("def target_function", path="/path/to/big.py")
Read("/path/to/big.py", [142, 165])
```

### Parallel Execution
```
# Bad: Sequential
Read(file1) → Read(file2) → Read(file3)

# Good: Parallel (single message, 3 tool calls)
Read(file1) | Read(file2) | Read(file3)
```

### Subagent Dispatch
```
# Bad: Heavy work in main thread (tokens visible)
[read 10 files, analyze, generate report]

# Good: Subagent isolation (only summary returned)
Task("Analyze 10 files, return 3-line summary")
```

### Response Length
```
# Bad (47 tokens)
"I'll help you implement that feature. Let me start by 
examining the codebase to understand the current architecture,
then I'll make the necessary changes..."

# Good (3 tokens)
[starts making changes]
```

---

## Cost Estimation Heuristics

| Operation | ~Tokens |
|-----------|---------|
| Read 100 lines code | 400-800 |
| Grep results (10 matches) | 200-400 |
| Edit file | 100-300 |
| Skill load | 500-2000 |
| Task subagent prompt | 200-500 |
| Task subagent result | 100-500 |
| Web search result | 500-1500 |
| Mermaid diagram | 100-300 |

---

## Cheapskate Checklist

Before responding:
- [ ] Can I answer in < 3 sentences?
- [ ] Are all tool calls parallelized?
- [ ] Am I reading only what's needed?
- [ ] Should this be a subagent (isolated tokens)?
- [ ] Did I skip the preamble?
- [ ] Did I skip the summary?

---

## GF(3) Integration

As MINUS (-1) validator:
- Constrains token expenditure
- Validates efficiency of other skills
- Balances PLUS generators (which produce tokens)

```
Σ(generator_tokens) + Σ(validator_savings) ≡ 0 (mod 3)
```

---

## Commands

```bash
# Analyze thread token usage
just cheapskate-analyze <thread-id>

# Estimate remaining budget
just cheapskate-budget

# Compress context
just cheapskate-compress
```

---

## See Also

- `parallel-fanout` - Efficient parallel dispatch
- `triad-interleave` - Balanced token streams
- `frustration-eradication` - Don't waste tokens on frustration



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
cheapskate (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch9: Generic Procedures
- Ch4: Pattern Matching
- Ch8: Degeneracy

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.
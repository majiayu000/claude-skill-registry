---
name: iterative-retrieval
description: "Execute 4-phase loop for progressive context refinement. Use when complex searches require multiple refinement cycles or context gap is unknown. Not for simple file searches or known file locations."
---

# Iterative Retrieval Pattern

A 4-phase loop for progressive context refinement when dealing with unknown or complex information needs.

## The Problem

Subagents don't know what they need until they start searching:

- Initial queries are too broad or too narrow
- Codebase terminology is unknown upfront
- Context gaps emerge during exploration
- Single-pass search misses relevant files

## The Solution: 4-Phase Loop

```
┌─────────────────────────────────────────────────────────────┐
│                  ITERATIVE RETRIEVAL LOOP                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DISPATCH       ──► Broad initial query to gather files  │
│         │                                                     │
│         ▼                                                     │
│  2. EVALUATE      ──► Score relevance 0-1 for each file     │
│         │                                                     │
│         ▼                                                     │
│  3. REFINE        ──► Update search criteria based on scores│
│         │                                                     │
│         ▼                                                     │
│  4. LOOP          ──► Repeat with refined criteria (max 3) │
│         │                                                     │
│         ▼                                                     │
│    HIGH RELEVANCE FILES FOUND ✓                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: DISPATCH

**Purpose**: Cast a wide net to gather candidate files.

**Approach:**

- Start with broad search terms
- Use multiple search patterns (Glob + Grep)
- Gather 10-20 candidate files
- Don't worry about relevance yet

**Example:**

```python
# Searching for "authentication patterns"
files = glob("**/*auth*.ts") + glob("**/*login*.ts")
files += grep("authenticate|login|signup", "**/*.ts")
```

**Output**: List of candidate files (unordered, broad)

## Phase 2: EVALUATE

**Purpose**: Score each file's relevance to the actual query.

**Scoring System (0-1):**

| Score   | Relevance | Action                           |
| ------- | --------- | -------------------------------- |
| 0.8-1.0 | High      | Read immediately, use in context |
| 0.5-0.7 | Medium    | Skim first, read if relevant     |
| 0.2-0.4 | Low       | Skip unless no high/medium found |
| 0-0.2   | None      | Ignore                           |

**Scoring Criteria:**

- Filename match: +0.3
- Import/usage match: +0.4
- Multiple keyword occurrences: +0.2
- Recent modification: +0.1
- Project type match (e.g., frontend/backend): +0.1

**Example:**

```python
# Score each candidate file
for file in candidates:
  score = 0
  if "auth" in file.name: score += 0.3
  if "authenticate" in file.content: score += 0.4
  if file.content.count("login") > 3: score += 0.2
  # ... store score
```

**Output**: Files with relevance scores

## Phase 3: REFINE

**Purpose**: Update search criteria based on evaluation results.

**Refinement Strategies:**

| Situation                       | Refinement                      |
| ------------------------------- | ------------------------------- |
| Too many high scores (0.8+)     | Narrow by adding specific terms |
| No high scores, many medium     | Add domain-specific terms       |
| All low scores                  | Change terminology entirely     |
| Found right domain, wrong files | Add file extension filters      |

**Example:**

```python
# Initial: "authentication"
# Result: Many frontend auth files, need backend

# Refined: "authentication server api"
# Result: Backend auth endpoints found
```

**Output**: Updated search query for next iteration

## Phase 4: LOOP

**Purpose**: Repeat with refined criteria until convergence.

**Termination Conditions:**

1. **Max iterations reached** (3 cycles maximum)
2. **Sufficient high-relevance files** (3+ files with 0.8+ score)
3. **Diminishing returns** (scores not improving between iterations)
4. **Context gap identified and filled** (specific question answered)

**Example:**

```python
max_iterations = 3
high_relevance_files = []

for iteration in range(max_iterations):
  candidates = dispatch(search_query)
  scored = evaluate(candidates, target_query)
  high_relevance_files.extend([f for f in scored if f.score >= 0.8])

  if len(high_relevance_files) >= 3:
    break  # Converged

  search_query = refine(search_query, scored)
```

**Output**: Final set of high-relevance files

## Usage Pattern

### When to Use Iterative Retrieval

✅ **Use when:**

- Searching for concepts with unknown terminology
- Initial search returns too many results (>20 files)
- Initial search returns too few results (<3 files)
- Domain-specific jargon is unknown
- Context gap is unclear

❌ **Don't use when:**

- File location is known
- Simple search will suffice
- Single-pass search finds relevant files
- Working with well-documented codebase

### Integration with File-Search

**file-search**: Basic search capability (find files by pattern)

**iterative-retrieval**: Advanced refinement (relevance scoring, progressive narrowing)

```
For simple searches:
→ Use file-search directly

For complex searches:
→ Use iterative-retrieval (uses file-search as initial dispatch)
```

### Example Workflow

**Task**: Find React context patterns in a large codebase

**Iteration 1:**

- **DISPATCH**: Search for "context"
- **EVALUATE**: 50 files found, mostly React createContext, some unrelated
- **REFINE**: Add "React useContext" to narrow
- **LOOP**: Continue

**Iteration 2:**

- **DISPATCH**: Search for "React useContext useContext"
- **EVALUATE**: 15 files, mostly usage patterns, few definitions
- **REFINE**: Add "createContext" to find definitions
- **LOOP**: Continue

**Iteration 3:**

- **DISPATCH**: Search for "createContext useContext React"
- **EVALUATE**: 8 files, 4 with high relevance (0.8+)
- **CONVERGED**: Sufficient high-relevance files found

**Result**: 4 context definition files with usage patterns identified

## Output Format

Return results as:

```markdown
## Iterative Retrieval Results

### Summary

- **Iterations**: 3
- **Total files evaluated**: 73
- **High-relevance files**: 4
- **Search query evolution**: "context" → "React useContext" → "createContext useContext"

### High-Relevance Files (0.8+)

1. **src/context/AuthContext.tsx** (score: 0.95)
   - Defines AuthContext with provider
   - Exports useAuth hook
   - 15 usages across codebase

2. **src/context/ThemeContext.tsx** (score: 0.88)
   - Defines ThemeContext with dark/light mode
   - Exports useTheme hook
   - 8 usages across codebase

### Medium-Relevance Files (0.5-0.7)

- **src/hooks/useContext.ts** (score: 0.65) - Utility hook, not context definition

### Context Gap Analysis

**Initial query**: "React context patterns"
**Gap**: Need both definitions and usage patterns
**Filled**: Found 4 definitions, usage patterns documented

### Next Steps

Use high-relevance files as context for understanding React context patterns in this codebase.
```

## Best Practices

1. **Start broad, narrow progressively** - Don't over-constrain initial query
2. **Score objectively** - Use consistent criteria across iterations
3. **Track query evolution** - Document how search terms change
4. **Know when to stop** - Don't iterate beyond 3 cycles
5. **Combine with other patterns** - Use filesystem-context for storage

## Integration with Seed System

### File-Search Integration

- **file-search**: Basic file finding by pattern
- **iterative-retrieval**: Progressive refinement with relevance scoring

**Integration**: iterative-retrieval uses file-search as initial dispatch mechanism.

### Filesystem-Context Integration

- **iterative-retrieval**: Discovers relevant files
- **filesystem-context**: Stores discovered files for selective retrieval

**Integration**: Use iterative-retrieval for discovery, filesystem-context for persistent access.

## Related Skills

- **file-search**: Basic file search capability
- **filesystem-context**: Persistent storage for discovered context

## Key Principle

Progressive refinement through 4-phase loop (DISPATCH → EVALUATE → REFINE → LOOP) yields higher relevance than single-pass search, especially when terminology is unknown upfront.

---

<critical_constraint>
MANDATORY: Maximum 3 iterations - stop when converged
MANDATORY: Score files on 0-1 scale with documented criteria
MANDATORY: Report high-relevance files (0.8+) with scores
MANDATORY: Document query evolution across iterations
No exceptions. Iterative retrieval must converge efficiently with traceable refinement.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---

---
name: hierarchical-matching-systems
description: >
  Expertise in architecting, implementing, reviewing, and debugging hierarchical matching systems.
  Use when working with: (1) Two-sided matching (Gale-Shapley, hospital-resident, student-school),
  (2) Assignment/optimization problems (Hungarian algorithm, bipartite matching),
  (3) Multi-level hierarchy matching (org charts, taxonomies, nested categories),
  (4) Entity resolution and record linkage across hierarchies.
  Triggers: debugging match quality issues, reviewing matching algorithms, translating business
  requirements into constraints, validating match correctness, architecting new matching systems,
  fixing unstable matches, resolving constraint violations, diagnosing preference misalignment.
---

# Hierarchical Matching Systems

This skill provides rigid diagnostic and architectural procedures for hierarchical matching systems. Follow checklists exactly—matching bugs often hide in skipped steps.

## Quick Reference

- **Algorithm selection**: See [references/decision-guide.md](references/decision-guide.md)
- **Algorithm details**: See [references/algorithms.md](references/algorithms.md)

---

## 1. Problem Classification Checklist

Before any work, classify the problem. Check ALL that apply:

```
□ TWO-SIDED: Both sides have preferences (students↔schools, workers↔jobs)
□ ONE-SIDED: Only one side has preferences (tasks→workers, items→bins)
□ HIERARCHICAL: Entities exist at multiple levels (org→dept→team→person)
□ WEIGHTED: Matches have costs/scores to optimize
□ CONSTRAINED: Hard limits exist (capacity, exclusions, required pairings)
□ STABLE: Solution must resist defection (no blocking pairs)
□ OPTIMAL: Solution must minimize/maximize objective function
□ FUZZY: Entities may partially match (entity resolution, deduplication)
```

Classification determines algorithm family. Proceed to Section 2 for architecture or Section 3 for debugging.

---

## 2. Architecture Procedure

Follow these phases in order when designing a new matching system.

### Phase 2.1: Requirements Translation

Convert each business requirement into formal constraints:

| Business Requirement | Constraint Type | Formal Expression |
|---------------------|-----------------|-------------------|
| "Each student gets one school" | Capacity | `|matches(s)| = 1 ∀ student s` |
| "Schools have seat limits" | Capacity | `|matches(school)| ≤ capacity` |
| "Siblings must be together" | Coupling | `school(s1) = school(s2) if siblings(s1,s2)` |
| "Student X cannot attend Y" | Exclusion | `(X, Y) ∉ matches` |
| "Priority for residents" | Preference ordering | `rank(resident) < rank(non-resident)` |

**Checklist:**
```
□ List ALL business requirements
□ Classify each as: capacity | coupling | exclusion | ordering | soft preference
□ Identify conflicts between requirements (document tradeoffs)
□ Distinguish HARD constraints (must satisfy) from SOFT (optimize toward)
□ Validate translations with stakeholder examples
```

### Phase 2.2: Algorithm Selection

Use [references/decision-guide.md](references/decision-guide.md) to select algorithm. Verify:

```
□ Algorithm handles all HARD constraints
□ Algorithm can optimize SOFT constraints (or document gaps)
□ Complexity acceptable for data size (see references/algorithms.md)
□ Stability requirements met (if two-sided)
□ Optimality requirements met (if weighted)
```

### Phase 2.3: Data Model Design

Define entities, relationships, and preference representation:

```
□ Entity schema for each side (attributes, identifiers)
□ Preference representation (ranked list | score matrix | pairwise comparisons)
□ Constraint encoding (how exclusions/couplings are stored)
□ Hierarchy representation (if multi-level: tree | DAG | adjacency list)
□ Tie-breaking rules (deterministic ordering for equal preferences)
```

### Phase 2.4: Interface Contracts

Specify inputs, outputs, and invariants:

**Input Contract:**
```
□ Preference format and validation rules
□ Constraint format and validation rules
□ Required vs optional fields
□ How missing preferences are handled (reject | default rank | exclude)
```

**Output Contract:**
```
□ Match format (pairs | assignment map | ranked list)
□ Unmatched entity handling (explicit list | null matches | error)
□ Match metadata (scores, stability proof, constraint satisfaction report)
```

**Invariants:**
```
□ Determinism: same input → same output (document randomness if any)
□ Completeness: all entities matched OR explicitly unmatched
□ Validity: all matches satisfy hard constraints
```

### Phase 2.5: Testing Strategy

Define validation before implementation:

```
□ Unit tests for preference parsing and constraint validation
□ Property tests: stability, optimality, constraint satisfaction
□ Edge cases: empty inputs, single entity, all tied preferences
□ Regression tests from known-good examples
□ Performance benchmarks at target scale
```

---

## 3. Debugging Procedure

Follow this diagnostic sequence for any matching issue. Do not skip steps.

### Phase 3.1: Symptom Classification

Identify the symptom category:

| Symptom | Category | Go To |
|---------|----------|-------|
| Same inputs, different outputs | INSTABILITY | 3.2 |
| Matches violate business rules | CONSTRAINT VIOLATION | 3.3 |
| Matches technically valid but "wrong" | PREFERENCE MISALIGNMENT | 3.4 |
| Errors with nested/hierarchical data | HIERARCHY BUG | 3.5 |
| Poor performance at scale | PERFORMANCE | 3.6 |

### Phase 3.2: Instability Diagnosis

**Root causes of non-deterministic matches:**

```
□ RANDOMNESS: Check for unseeded RNG in tie-breaking
   → Fix: Use deterministic tie-breaker (lexicographic ID, timestamp)

□ FLOATING POINT: Check score comparisons for floating point issues
   → Fix: Use epsilon comparison or integer scores

□ HASH ORDERING: Check if iteration order depends on hash maps
   → Fix: Sort keys before iteration

□ PARALLEL RACE: Check for concurrent modifications
   → Fix: Synchronize or use sequential processing

□ INPUT ORDERING: Check if algorithm is order-sensitive
   → Fix: Canonicalize input order (sort by ID)
```

**Verification:**
```
□ Run matching 10x with identical inputs
□ Diff all outputs
□ If any differ, add logging to identify divergence point
```

### Phase 3.3: Constraint Violation Diagnosis

**Diagnostic sequence:**

```
1. □ IDENTIFY: Which specific constraint is violated?
   → List the violated constraint and the violating match

2. □ TRACE: Where should constraint be enforced?
   → Map constraint to code location (filter | validation | algorithm step)

3. □ VERIFY ENCODING: Is constraint correctly represented?
   → Print constraint data structure, verify against requirement

4. □ VERIFY ENFORCEMENT: Is constraint checked at right time?
   → Add logging before/after enforcement point

5. □ CHECK ORDERING: Is constraint checked before conflicting decisions?
   → Trace decision sequence, verify constraint checked first

6. □ CHECK COMPLETENESS: Are all instances covered?
   → Enumerate all entities that should be constrained
```

**Common failure patterns:**

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Late enforcement | Valid intermediate state, invalid final | Move check earlier |
| Partial coverage | Some entities constrained, others not | Enumerate all cases |
| Soft vs hard confusion | Constraint violated for "better" match | Reclassify as hard |
| Stale data | Constraint on outdated values | Refresh before check |

### Phase 3.4: Preference Misalignment Diagnosis

When matches are valid but don't reflect intended priorities:

```
1. □ EXTRACT: Get the actual preference data used
   → Log/print the exact preference structure at match time

2. □ COMPARE: Check against expected preferences
   → Side-by-side diff with business-stated priorities

3. □ TRACE TRANSFORMATION: Follow preference from input to algorithm
   → Log at each transformation step (parsing, normalization, scoring)

4. □ CHECK SCORING: Verify score calculation
   → Manual calculation for 2-3 example cases

5. □ CHECK AGGREGATION: If multi-criteria, verify combination
   → Test each criterion independently, then combined

6. □ CHECK NORMALIZATION: Verify scale/range handling
   → Check for min/max, z-score, or rank normalization bugs
```

**Scoring function checklist:**

```
□ Direction correct (higher = better or lower = better, consistently)
□ Scale appropriate (no single factor dominating)
□ Missing values handled (null → 0? → excluded? → default?)
□ Ties handled explicitly (not left to floating point chance)
□ Edge cases: extreme values, all same values, single candidate
```

### Phase 3.5: Hierarchy Traversal Diagnosis

For multi-level matching issues:

```
1. □ VISUALIZE: Draw the hierarchy with the problematic match
   → Tree diagram showing all levels and the match path

2. □ CHECK INHERITANCE: Do child constraints inherit from parent?
   → Verify constraint propagation rules

3. □ CHECK AGGREGATION: How do child preferences roll up?
   → Verify aggregation function (sum | max | weighted | majority)

4. □ CHECK LEVEL INTERACTION: Can matches cross levels?
   → Document allowed/forbidden cross-level matches

5. □ CHECK TRAVERSAL ORDER: Top-down or bottom-up?
   → Verify algorithm processes levels in intended order

6. □ CHECK PARTIAL MATCHES: Can a parent match without all children?
   → Document completeness requirements per level
```

**Common hierarchy bugs:**

| Bug | Symptom | Fix |
|-----|---------|-----|
| Missing propagation | Child ignores parent constraint | Add inheritance logic |
| Double counting | Same entity weighted multiple times | Deduplicate in aggregation |
| Level skipping | Match at wrong level | Add level validation |
| Orphan handling | Unattached children cause errors | Define orphan policy |

### Phase 3.6: Performance Diagnosis

For scale and speed issues:

```
1. □ PROFILE: Identify the slow component
   → Time each phase: input parsing, preference building, matching, output

2. □ COMPLEXITY CHECK: Verify actual vs expected complexity
   → Log iteration counts, compare to theoretical O(n)

3. □ MEMORY CHECK: Profile memory usage
   → Watch for preference matrix explosion (n² space)

4. □ ALGORITHM FIT: Verify algorithm appropriate for scale
   → See references/algorithms.md for complexity comparison

5. □ CACHING: Check for redundant computation
   → Log cache hits/misses for preference lookups

6. □ BATCH VS STREAMING: Check processing model
   → Full recomputation vs incremental updates
```

---

## 4. Testing & Validation Procedure

### 4.1: Correctness Properties

Test these properties for every matching system:

```
□ DETERMINISM: run(input) = run(input) (10 trials minimum)
□ COMPLETENESS: all entities either matched or explicitly unmatched
□ VALIDITY: all matches satisfy all hard constraints
□ STABILITY (if applicable): no blocking pairs exist
□ OPTIMALITY (if applicable): objective function at expected value
```

### 4.2: Stability Verification (Two-Sided Matching)

For stable matching, verify no blocking pairs:

```python
# Pseudocode - verify no blocking pair exists
for each unmatched_pair (a, b):
    if a prefers b over current_match(a):
        if b prefers a over current_match(b):
            FAIL: blocking pair found (a, b)
```

```
□ Enumerate all non-matched pairs
□ Check mutual preference for each
□ Report any blocking pairs found
□ For large instances, sample-check (document coverage)
```

### 4.3: Constraint Satisfaction Verification

```
□ List all hard constraints
□ For each match, verify against each constraint
□ Generate constraint satisfaction report
□ Flag any violations with specific match and constraint
```

### 4.4: Edge Case Test Suite

Mandatory test cases:

```
□ Empty input (no entities on one or both sides)
□ Single entity (one-to-one degenerate case)
□ All identical preferences (maximum tie scenario)
□ Mutually exclusive preferences (everyone wants same thing)
□ Impossible constraints (unsatisfiable, should error clearly)
□ Maximum capacity (all slots exactly filled)
□ Minimum capacity (barely enough slots)
□ Self-referential (can entity match itself? test boundary)
□ Circular preferences (A→B→C→A)
```

### 4.5: Regression Test Maintenance

```
□ Capture real production cases that revealed bugs
□ Minimize to smallest reproducing example
□ Document expected behavior explicitly
□ Run on every change to matching logic
```

---

## 5. Review Checklist

When reviewing matching system code or design:

### 5.1: Design Review

```
□ Problem correctly classified (Section 1)
□ Algorithm appropriate for problem class (references/decision-guide.md)
□ All business requirements mapped to constraints (Section 2.1)
□ Hard vs soft constraints clearly distinguished
□ Tie-breaking is deterministic and documented
□ Hierarchy semantics defined (if applicable)
```

### 5.2: Implementation Review

```
□ Preference representation matches algorithm requirements
□ Constraints enforced at correct point in algorithm
□ No hidden randomness (unseeded RNG, hash iteration)
□ Floating point comparison handled correctly
□ Edge cases handled (empty, single, ties)
□ Error messages identify specific constraint violations
```

### 5.3: Testing Review

```
□ All properties from 4.1 tested
□ Edge cases from 4.4 covered
□ Performance benchmarked at realistic scale
□ Regression tests exist for past bugs
```

---

## Appendix: Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Greedy first-come | Order-dependent, non-optimal | Use proper algorithm |
| Score = sum(all factors) | One factor dominates | Normalize scales |
| Retry until valid | Non-deterministic, slow | Fix constraint order |
| Global preference cache | Stale across updates | Invalidate on change |
| String matching for entities | Case/whitespace bugs | Use canonical IDs |
| Float equality for ties | Non-deterministic | Use epsilon or integer |
| Recursive hierarchy walk | Stack overflow risk | Use iterative with explicit stack |
| N² preference matrix | Memory explosion | Use sparse representation |

---
name: refacter
description: Refacter code using complexity analysis and hotspot detection. Use when asked to refactor code, improve code quality, reduce complexity, or identify high-risk areas that need attention.
---

# Refacter Skill

**Tech Stack**: Python 3.11+, radon (complexity analysis), git (code churn analysis)

**Source**: Extracted from CLAUDE.md global refactoring principles and industry best practices.

---

## When to Use This Skill

Use the refactor skill when:
- ✓ User explicitly asks to refactor code
- ✓ Code complexity metrics exceed thresholds (cyclomatic > 10, cognitive > 15)
- ✓ Hotspot analysis reveals high-risk areas (high churn + high complexity)
- ✓ Adding new features to complex legacy code
- ✓ Before major refactoring to understand current state

**DO NOT use this skill for:**
- ✗ Simple formatting changes (use `just format` instead)
- ✗ Renaming variables (straightforward refactoring)
- ✗ One-off code improvements without analysis

---

## Quick Refactoring Decision Tree

```
Is code complex/hard to understand?
├─ YES → Measure complexity (radon)
│   ├─ Cyclomatic > 10? → Extract methods, simplify conditionals
│   └─ Cognitive > 15? → Reduce nesting, early returns
│
└─ NO → Is code changing frequently (hotspot)?
    ├─ YES → Analyze code churn + complexity
    │   └─ High churn + high complexity? → Priority refactor target
    │
    └─ NO → Is code tightly coupled (connascence)?
        ├─ YES → Analyze connascence strength
        │   ├─ Dynamic connascence (CoE, CoV)? → Critical, refactor to static
        │   ├─ Strong static (CoP, CoM, CoA)? → Refactor to weaker forms
        │   └─ Weak static (CoN, CoT)? → Acceptable
        │
        └─ NO → Is code duplicated?
            ├─ YES → Extract common patterns
            └─ NO → Code is fine, no refactor needed
```

---

## Loop Pattern: Branching Loop (Evaluate Refactoring Approaches)

**Escalation Trigger**:
- Multiple refactoring approaches available
- `/compare` needed to evaluate trade-offs
- `/impact` assessment for each approach

**Tools Used**:
- `/compare` - Compare refactoring strategies (extract method vs extract class vs redesign)
- `/impact` - Assess blast radius of each approach (files affected, test changes, deployment risk)
- `/validate` - Verify refactoring preserves behavior (run tests)
- `/reflect` - Synthesize which approach worked best

**Why This Works**: Refactoring naturally involves branching—choosing between different improvement paths based on complexity analysis.

See [Thinking Process Architecture - Feedback Loops](../../.claude/diagrams/thinking-process-architecture.md#11-feedback-loop-types-self-healing-properties) for structural overview.

---

## Refactoring Workflow

### Step 1: Profile Current State

```bash
# Analyze code complexity
python .claude/skills/refacter/scripts/analyze_complexity.py src/

# Identify hotspots (high churn + high complexity)
python .claude/skills/refacter/scripts/analyze_hotspots.py src/
```

### Step 2: Prioritize Refactoring Targets

**Priority Matrix:**

| Code Churn | Complexity | Priority | Action |
|------------|------------|----------|--------|
| High | High | **P0 - Critical** | Refactor immediately |
| High | Low | P1 - Monitor | Add tests, watch for complexity |
| Low | High | P2 - Technical Debt | Refactor when touching code |
| Low | Low | P3 - Ignore | No action needed |

### Step 3: Apply Refactoring Patterns

See [REFACTORING-PATTERNS.md](REFACTORING-PATTERNS.md) for specific techniques:

**Complexity-Based:**
- Extract Method (reduce function length)
- Extract Class (separate concerns)
- Simplify Conditionals (reduce nesting)
- Replace Magic Numbers (constants)
- Introduce Parameter Object (reduce parameter count)

**Connascence-Based:**
- CoP → CoN (positional parameters → named parameters)
- CoM → CoN (magic numbers → named constants)
- CoE → Encapsulation (execution order → hidden internally)
- CoV → Event-Driven (shared values → eventual consistency)

### Step 4: Verify Improvement

```bash
# Run complexity analysis again
python .claude/skills/refacter/scripts/analyze_complexity.py src/

# Ensure complexity decreased
# Run tests to ensure behavior unchanged
pytest tests/
```

---

## Complexity Thresholds

| Metric | Good | Warning | Critical | Refactor Action |
|--------|------|---------|----------|-----------------|
| **Cyclomatic Complexity** | 1-10 | 11-20 | 21+ | Extract methods, simplify conditionals |
| **Cognitive Complexity** | 1-15 | 16-25 | 26+ | Reduce nesting, early returns |
| **Lines of Code (LOC)** | 1-50 | 51-100 | 101+ | Extract methods, split responsibilities |
| **Function Parameters** | 1-4 | 5-6 | 7+ | Introduce parameter object |

**Source**: Based on industry standards (SonarQube, Code Climate, radon)

---

## Common Refactoring Scenarios

### Scenario 1: Complex Conditional Logic

**Symptom**: Deeply nested if/else, multiple conditions
**Metric**: High cyclomatic complexity (> 10)
**Solution**: See [REFACTORING-PATTERNS.md#simplify-conditionals](REFACTORING-PATTERNS.md)

### Scenario 2: Long Functions

**Symptom**: Function > 50 lines, does many things
**Metric**: High LOC, high cyclomatic complexity
**Solution**: Extract Method pattern

### Scenario 3: Frequent Changes + High Complexity

**Symptom**: File changed in 20+ commits, cyclomatic > 15
**Metric**: Hotspot analysis shows P0 priority
**Solution**: Add tests first, then refactor incrementally

### Scenario 4: Duplicated Code

**Symptom**: Same logic in multiple places
**Metric**: No specific metric (manual detection)
**Solution**: Extract common patterns, DRY principle

---

## Quick Reference

### Run Complexity Analysis

```bash
# Analyze specific directory
python .claude/skills/refacter/scripts/analyze_complexity.py src/agent/

# Analyze with thresholds
python .claude/skills/refacter/scripts/analyze_complexity.py src/ --max-cc 10 --max-cognitive 15

# Output to JSON for further processing
python .claude/skills/refacter/scripts/analyze_complexity.py src/ --json > complexity.json
```

### Run Hotspot Analysis

```bash
# Analyze git hotspots (last 6 months)
python .claude/skills/refacter/scripts/analyze_hotspots.py src/

# Custom time range
python .claude/skills/refacter/scripts/analyze_hotspots.py src/ --since "3 months ago"

# Show top 10 hotspots
python .claude/skills/refacter/scripts/analyze_hotspots.py src/ --top 10
```

---

## Refactoring Principles

**From CLAUDE.md global instructions:**
> "when ask to refactor, use code complexity analysis, and hotspot analysis to profile codebase."

### Core Principles

1. **Measure First, Refactor Second**: Use metrics to identify what needs refactoring
2. **Prioritize by Risk**: Hotspots (high churn + high complexity) are highest priority
3. **Incremental Refactoring**: Small, testable changes
4. **Test Coverage First**: Add tests before refactoring risky code
5. **Avoid Over-Engineering**: Only refactor to thresholds, not perfection

### When NOT to Refactor

- ❌ Code works and rarely changes (low churn, low complexity)
- ❌ No tests exist and risk is high (add tests first)
- ❌ Deadline pressure (tech debt ticket instead)
- ❌ Cosmetic changes without measurable benefit

### The "Rule of Three"

**Pattern**: Only extract abstraction when you see the same pattern THREE times.

```python
# ❌ BAD: Premature abstraction (seen once)
def process_single_case():
    return generic_abstraction(params)

# ✅ GOOD: Wait for third occurrence
# First time: Write inline
# Second time: Note similarity
# Third time: Extract pattern
```

---

## Connascence: Coupling with Precision

**Connascence** = Two components are connascent if changing one requires changing the other.

### The Strength Hierarchy (Refactor UP this ladder)

```
STATIC (Weakest - detectable at compile time)
├─ Connascence of Name (CoN)           ← WEAKEST (acceptable)
├─ Connascence of Type (CoT)           ← Weak (acceptable)
├─ Connascence of Meaning (CoM)        ← Medium (should improve)
├─ Connascence of Position (CoP)       ← Medium (should improve)
└─ Connascence of Algorithm (CoA)      ← Strong (document clearly)

DYNAMIC (Strongest - only runtime detection)
├─ Connascence of Execution (CoE)      ← Very Strong (refactor!)
├─ Connascence of Timing (CoT)         ← Very Strong (refactor!)
├─ Connascence of Values (CoV)         ← Strongest (critical!)
└─ Connascence of Identity (CoI)       ← Strongest (critical!)
```

### Refactoring by Connascence Strength

**Always refactor from stronger → weaker forms:**

| Current | Problem | Refactor To | Benefit |
|---------|---------|-------------|---------|
| **CoV** (Values) | Distributed transaction | Event-driven | No shared state |
| **CoE** (Execution) | Must call in order | Encapsulate order | Hide complexity |
| **CoP** (Position) | Positional params | Named params (CoN) | Self-documenting |
| **CoM** (Meaning) | Magic numbers | Named constants (CoN) | Clear intent |

### Three Properties of Connascence

1. **Strength**: How hard to refactor (dynamic > static)
2. **Locality**: How far apart (same file < different services)
3. **Degree**: How many affected (2 components < 10 components)

**Rule**: As distance increases, use weaker forms
- ✅ OK: Dynamic connascence within a class
- ❌ BAD: Dynamic connascence across microservices

See [REFACTORING-PATTERNS.md](REFACTORING-PATTERNS.md) for connascence-based refactoring examples.

---

## File Organization

```
.claude/skills/refacter/
├── SKILL.md                  # This file (entry point)
├── CODE-COMPLEXITY.md        # Complexity metrics guide
├── HOTSPOT-ANALYSIS.md       # Code churn + complexity
├── REFACTORING-PATTERNS.md   # Common refactoring techniques
└── scripts/
    ├── analyze_complexity.py # Complexity analysis tool
    └── analyze_hotspots.py   # Hotspot detection tool
```

---

## Next Steps

- **For complexity metrics**: See [CODE-COMPLEXITY.md](CODE-COMPLEXITY.md)
- **For hotspot detection**: See [HOTSPOT-ANALYSIS.md](HOTSPOT-ANALYSIS.md)
- **For refactoring techniques**: See [REFACTORING-PATTERNS.md](REFACTORING-PATTERNS.md)
- **For code style**: See `docs/CODE_STYLE.md`

---

## References

- [Martin Fowler: Refactoring](https://refactoring.com/) - Catalog of refactoring patterns
- [Fundamentals of Software Architecture](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/) - Connascence concepts
- [Code Climate: Cognitive Complexity](https://codeclimate.com/blog/cognitive-complexity/)
- [Your Code as a Crime Scene](https://pragprog.com/titles/atcrime/) - Hotspot analysis origins
- [radon Documentation](https://radon.readthedocs.io/) - Python complexity tool

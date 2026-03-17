---
name: philosophy-compliance-workflow
version: 1.0.0
description: Philosophy compliance guardian - ensures code aligns with amplihack's ruthless simplicity, brick philosophy, and Zen-like minimalism through systematic review
auto_activates:
  - "philosophy review"
  - "check philosophy"
  - "validate architecture"
  - "simplicity review"
  - "brick compliance"
  - "zen review"
explicit_triggers:
  - /amplihack:philosophy-review
  - /amplihack:zen-check
confirmation_required: false
token_budget: 2500
---

# Philosophy Compliance Workflow Skill

## Purpose

Systematic philosophy compliance review that ensures all code and architecture aligns with amplihack's core principles: ruthless simplicity, brick philosophy, and Zen-like minimalism. This skill validates that implementations serve clear purposes without unnecessary complexity.

## When to Use This Skill

**USE FOR:**
- Architecture reviews before implementation
- Code reviews for philosophy alignment
- Refactoring validation (did we actually simplify?)
- Module design verification
- Pre-merge philosophy checks
- Identifying over-engineering and complexity creep

**AVOID FOR:**
- Functional bug fixes (not philosophy issues)
- Performance optimization alone
- Documentation updates
- Pure syntax/style issues

## Core Philosophy Principles

### The Zen of Simple Code

- Each line serves a clear purpose without embellishment
- As simple as possible, but no simpler
- Complex systems from simple, well-defined components
- Handle what's needed now, not hypothetical futures

### The Brick Philosophy

- **A brick** = Self-contained module with ONE clear responsibility
- **A stud** = Public contract (functions, API, data model) others connect to
- **Regeneratable** = Can be rebuilt from spec without breaking connections
- **Isolated** = All code, tests, fixtures inside the module's folder

### Ruthless Simplicity

- Start with the simplest solution that works
- Add complexity only when justified
- Question every abstraction
- Code you don't write has no bugs

## Review Process

### Step 1: Scope Identification

**Identify what to review:**
- Single module, multiple modules, or full architecture
- Recent changes or complete codebase
- Specific complexity concerns or general review

**Questions to ask:**
- What triggered this review?
- What are the main concerns?
- What's the expected outcome?

### Step 2: Initial Analysis

**Scan the code structure:**
- Module organization and boundaries
- Public interfaces (the "studs")
- Dependencies and coupling
- Abstraction layers
- Configuration complexity

**Red flags to watch for:**
- Multiple responsibilities in one module
- Unclear module boundaries
- Deep inheritance hierarchies
- Generic "framework" code
- Future-proofing for hypothetical needs

### Step 3: Philosophy Questions

**Ask the 5 core questions for each component:**

1. **Necessity**: "Do we actually need this right now?"
   - Is this solving a real problem today?
   - Or is it future-proofing for "maybe someday"?

2. **Simplicity**: "What's the simplest way to solve this problem?"
   - Can we remove layers?
   - Is there a more direct approach?

3. **Modularity**: "Can this be a self-contained brick?"
   - Does it have ONE clear responsibility?
   - Are the connection points (studs) obvious?

4. **Regenerability**: "Can AI rebuild this from a specification?"
   - Is the contract clear enough?
   - Are dependencies well-defined?

5. **Value**: "Does the complexity add proportional value?"
   - What would break if we simplified this?
   - Is the trade-off justified?

### Step 4: Identify Violations

**Categorize issues by severity:**

**CRITICAL (Must Fix):**
- Multiple responsibilities in one module
- Circular dependencies
- Unclear public contracts
- Non-regeneratable designs
- Tight coupling preventing module replacement

**WARNING (Should Fix):**
- Premature optimizations
- Excessive configuration options
- Unnecessary abstractions
- Generic "framework" patterns
- Future-proofing without current need

**SUGGESTION (Consider):**
- Opportunities for simplification
- Alternative approaches with fewer dependencies
- Ways to flatten abstraction layers
- Module boundary improvements

### Step 5: Generate Review Report

**Create structured review output:**

```markdown
# Philosophy Compliance Review: [Component Name]

## Overall Score: [A/B/C/D/F]

## Summary
[One paragraph overview of findings]

## Strengths (What Aligns)

- [Philosophy-aligned patterns identified]
- [Well-implemented brick designs]
- [Clear simplicity examples]

## Concerns (Warnings)

- [Complexity that should be addressed]
- [Borderline philosophy violations]
- [Opportunities for improvement]

## Violations (Critical Issues)

- [Clear departures from philosophy]
- [Must-fix problems]
- [Blocking issues for philosophy compliance]

## Recommendations

### Immediate Actions (Critical)
1. [Specific fix required with rationale]
2. [Another critical fix]

### Structural Improvements (Important)
1. [Module boundary adjustments]
2. [Decoupling suggestions]

### Simplification Opportunities (Good to Have)
1. [Ways to reduce complexity]
2. [Abstraction removal suggestions]

## Regeneration Assessment

**Can AI rebuild these components from specifications?**
- Module A: [Ready/Needs Work] - [Specific reason]
- Module B: [Ready/Needs Work] - [Specific reason]

**What's blocking regeneration:**
- [List specific issues preventing clear AI regeneration]

## Philosophy Alignment Score

- Ruthless Simplicity: [0-10]/10 - [Rationale]
- Brick Philosophy: [0-10]/10 - [Rationale]
- Zen Minimalism: [0-10]/10 - [Rationale]

**Overall: [Score]/10**
```

### Step 6: Provide Actionable Guidance

**For each violation, provide:**
- Clear explanation of the problem
- Why it violates philosophy
- Specific fix recommendation
- Expected improvement from fix
- Priority (Critical/Important/Nice-to-have)

**Example:**
```
Issue: SessionManager class has 8 different responsibilities
Violation: Breaks single responsibility (brick philosophy)
Fix: Split into:
  - SessionStore (persistence only)
  - SessionValidator (validation only)
  - SessionLifecycle (creation/expiry only)
Impact: Each brick becomes regeneratable and testable independently
Priority: Critical
```

## Philosophy Scoring Rubric

### Ruthless Simplicity (0-10)

- **10**: Every component serves clear purpose, minimal complexity
- **8-9**: Generally simple with minor complexity creep
- **6-7**: Some unnecessary abstractions or future-proofing
- **4-5**: Significant over-engineering present
- **0-3**: Complex beyond necessity, hard to understand

### Brick Philosophy (0-10)

- **10**: All modules self-contained with clear single responsibility
- **8-9**: Most modules follow brick pattern with minor coupling
- **6-7**: Some unclear boundaries or multiple responsibilities
- **4-5**: Significant coupling and unclear contracts
- **0-3**: Monolithic or tightly coupled, not regeneratable

### Zen Minimalism (0-10)

- **10**: Embraces simplicity, handles only current needs
- **8-9**: Mostly minimal with some extra features
- **6-7**: Some hypothetical futures addressed unnecessarily
- **4-5**: Considerable future-proofing and "just in case" code
- **0-3**: Over-engineered for "maybe someday" scenarios

### Overall Grade

- **A (9-10)**: Excellent philosophy alignment
- **B (7-8)**: Good with minor improvements needed
- **C (5-6)**: Acceptable but needs attention
- **D (3-4)**: Poor alignment, significant refactoring needed
- **F (0-2)**: Critical philosophy violations throughout

## Green Patterns (Examples of Good Design)

**Philosophy-Aligned Designs:**
- Single-responsibility modules with clear purpose
- Self-contained directories with all code and tests
- Obvious public interfaces (studs) for connections
- Direct, straightforward implementations
- Minimal dependencies (preferring standard library)

**Example: Good Brick Module**
```
authentication/
├── __init__.py        # Exports: authenticate, validate_token
├── core.py           # Implementation (one responsibility)
├── models.py         # User, Token (clear data models)
├── tests/
│   └── test_core.py  # Comprehensive tests
└── README.md         # Regeneration specification

Public Contract (Studs):
- authenticate(username, password) -> Token
- validate_token(token) -> User

One Responsibility: Authentication only (not authorization, not user management)
Regeneratable: Yes, from README.md specification
```

## Red Patterns (Examples to Avoid)

**Philosophy Violations:**
- God objects with multiple responsibilities
- Abstract base classes without clear justification
- Complex configuration systems for simple features
- Generic "flexible" frameworks
- Premature performance optimizations

**Example: Bad Design**
```
user_system/
├── framework.py          # Generic abstraction layer
├── manager.py            # UserManager does everything
├── config/               # Extensive config system
├── plugins/              # Plugin architecture (unused)
└── adapters/             # Future-proofing for other DBs

Problems:
- UserManager handles auth, profile, settings, notifications
- Framework adds complexity without current value
- Plugin system built for "maybe someday"
- Multiple responsibilities, not regeneratable
```

## Integration with Other Workflows

**When to combine philosophy review with:**

- **After Builder**: Validate implemented code follows philosophy
- **Before Architect**: Ensure design specs embrace simplicity
- **During Reviewer**: Include philosophy as review criteria
- **With Cleanup**: Identify what to simplify/remove

**Default workflow position:**
- Architecture Phase: Before implementation starts
- Code Review Phase: After implementation, before merge
- Refactoring Phase: Validate simplification efforts

## Key Mantras

- "It's easier to add complexity later than to remove it"
- "Code you don't write has no bugs"
- "Favor clarity over cleverness"
- "The best code is often the simplest"
- "Modules should be bricks: self-contained and regeneratable"
- "Do we need this NOW, or are we future-proofing?"
- "What's the simplest thing that could possibly work?"

## Common Pitfalls

**Disguised Complexity:**
- "This makes it flexible" → Often means over-engineered
- "We might need this later" → Future-proofing without current need
- "This is more generic" → Generic often means complex
- "Industry best practice" → May not apply to your scale

**Philosophy Traps:**
- Adding abstraction layers "just in case"
- Building frameworks for single use cases
- Creating plugin systems before needing plugins
- Optimizing before measuring performance
- Designing for hypothetical scale

## Success Criteria

A successful philosophy review:
- [ ] Identifies all critical philosophy violations
- [ ] Provides actionable fix recommendations
- [ ] Explains why violations matter
- [ ] Scores components objectively
- [ ] Validates regeneration readiness
- [ ] Celebrates philosophy-aligned patterns
- [ ] Guides team toward simpler designs

## Output Artifacts

**Generated documents:**
- Philosophy review report (markdown)
- Action items with priorities
- Before/after comparison (if fixes applied)
- Regeneration assessment per module

**Where to save:**
- `.claude/runtime/logs/<session>/philosophy_review_<timestamp>.md`
- Link in commit message if fixes applied
- Update `.claude/context/DISCOVERIES.md` with patterns learned

## Remember

You are the philosophical conscience of the system. Challenge complexity, celebrate simplicity, and ensure every architectural decision moves toward the Zen ideal of elegant, essential software.

**Your goal is not perfection - it's continuous improvement toward simpler, clearer, more regeneratable code.**

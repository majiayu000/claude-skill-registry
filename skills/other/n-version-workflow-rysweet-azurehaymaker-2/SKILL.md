---
name: n-version-workflow
version: 1.0.0
description: N-version programming for critical implementations - generates N independent solutions and selects the best through comparison
auto_activates:
  - "critical security feature"
  - "authentication system"
  - "authorization logic"
  - "complex algorithm"
  - "high-risk refactoring"
  - "multiple valid approaches"
explicit_triggers:
  - /amplihack:n-version
confirmation_required: true
token_budget: 3500
---

# N-Version Programming Workflow Skill

## Purpose

Execute N-version programming workflow for critical implementations where multiple independent solutions should be generated and compared to select the best approach.

## When to Use This Skill

**USE FOR:**
- Critical security features (authentication, authorization)
- Complex algorithms with multiple valid approaches
- High-risk refactoring of core components
- Architecture decisions with significant long-term impact
- When correctness is paramount over speed

**AVOID FOR:**
- Simple CRUD operations
- Straightforward bug fixes
- Documentation updates
- Minor UI tweaks
- Time-sensitive quick fixes

## Configuration

### Core Parameters

**N (Number of Versions):**
- `3` - Default for standard tasks
- `4-6` - Critical features requiring high confidence
- `2` - Quick validation of approach

**Selection Criteria** (priority order):
1. Correctness - Meets requirements and passes tests
2. Security - No vulnerabilities or anti-patterns
3. Simplicity - Ruthless simplicity, minimal complexity
4. Philosophy Compliance - Follows project principles
5. Performance - Efficiency and resource usage

**Agent Diversity Profiles:**
- `conservative` - Proven patterns and safety
- `innovative` - Novel approaches and optimizations
- `minimalist` - Ruthless simplicity
- `pragmatic` - Balance trade-offs for practical solutions
- `performance-focused` - Optimize for speed and efficiency

## Execution Process

### Step 1: Prepare Common Context

- **Use prompt-writer agent** to create crystal-clear specification
- Document all requirements explicitly
- Define success criteria measurably
- Prepare identical task specification for all N versions
- Identify evaluation metrics upfront
- **CRITICAL: Capture explicit user requirements that CANNOT be optimized away**

**Output:** Single authoritative specification document

### Step 2: Generate N Independent Implementations

- Spawn N Claude subprocesses simultaneously
- Each subprocess receives IDENTICAL task specification
- **NO context sharing between subprocesses** (true independence)
- Each uses different agent diversity profile
- Each produces complete implementation with tests
- Each works in isolated directory (version_1/, version_2/, etc.)

**Example for N=3:**
- Subprocess 1: Conservative approach (proven patterns, comprehensive error handling)
- Subprocess 2: Pragmatic approach (balance simplicity and robustness)
- Subprocess 3: Minimalist approach (ruthless simplification, minimal dependencies)

### Step 3: Collect and Compare Implementations

- Wait for all N implementations to complete
- **Use analyzer agent** to examine each implementation
- **Use tester agent** to run tests for each version
- Document results in comparison matrix

**Comparison Matrix:**
```
| Version | Correctness | Security | Simplicity | Philosophy | Performance | Lines of Code |
|---------|-------------|----------|------------|------------|-------------|---------------|
| v1      | PASS        | PASS     | 7/10       | 8/10       | 150ms       | 180           |
| v2      | PASS        | PASS     | 9/10       | 9/10       | 180ms       | 95            |
| v3      | FAIL        | N/A      | 10/10      | 7/10       | N/A         | 65            |
```

### Step 4: Review and Evaluate

- **Use reviewer agent** for comprehensive comparison
- **Use security agent** to evaluate security of each version
- Apply selection criteria in priority order
- Eliminate versions that fail correctness tests
- Compare remaining versions on other criteria
- Identify best parts of each implementation

**Evaluation Process:**
1. Filter: Remove versions failing correctness tests
2. Security Gate: Eliminate versions with security issues
3. Philosophy Check: Score each on simplicity and compliance
4. Performance Compare: Measure and compare benchmarks
5. Synthesis: Identify if hybrid approach could be superior

### Step 5: Select or Synthesize Solution

**Decision Tree:**
1. Is there ONE version that passes all criteria?
   - YES → Select it and document why
   - NO → Continue to step 2
2. Are there 2+ versions tied on top criteria?
   - YES → Continue to step 3
   - NO → Select highest scoring version
3. Do versions have complementary strengths?
   - YES → Synthesize hybrid combining best parts
   - NO → Select based on weighted criteria priority

**Example Synthesis:**
```
Selected: Hybrid of v1 and v2
- Core logic from v2 (ruthless simplicity)
- Error handling from v1 (comprehensive coverage)
- Testing approach from v2 (focused, minimal)
- Documentation style from v1 (thorough)

Rationale: v2's minimalist core paired with v1's robust
error handling provides optimal balance of simplicity
and production-readiness.
```

### Step 6: Implement Selected Solution

- **Use builder agent** to implement final version
- If single version selected: Use it directly
- If synthesis: Implement hybrid combining best parts
- Preserve all explicit user requirements from Step 1
- Run full test suite
- Document selection rationale in code comments

**Documentation Template:**
```python
"""
N-Version Implementation Selection

Generated Versions: 3
Selection: Hybrid of v1 (conservative) and v2 (pragmatic)

Rationale:
- v1 had superior error handling and edge case coverage
- v2 had cleaner architecture and better testability
- v3 failed correctness tests (edge case handling)

This implementation combines v2's core logic with v1's
defensive programming approach for production robustness.

Selection Criteria Applied:
1. Correctness: v1=PASS, v2=PASS, v3=FAIL
2. Security: All passed
3. Simplicity: v2 ranked highest
4. Philosophy: v1 and v2 tied
5. Performance: Negligible difference
```

### Step 7: Document Learnings

- Create analysis document: `n_version_analysis.md`
- Document all N implementations generated
- Explain selection rationale in detail
- Capture insights from rejected versions
- Update `.claude/context/DISCOVERIES.md` with patterns learned
- Include comparison matrix for future reference

## Trade-Offs

**Cost:** N times the compute resources and time
**Benefit:** Significantly reduced risk of critical errors
**Best For:** Features where bugs are expensive (security, data integrity)

## Examples

### Example 1: Authentication System

**Task:** Implement JWT-based authentication
**Configuration:** N=4 (critical security feature)
**Profiles:** conservative, security-focused, pragmatic, minimalist

**Result:**
- v1 (conservative): Most comprehensive but over-engineered
- v2 (security-focused): Excellent security but complex
- v3 (pragmatic): Good balance, missing edge cases
- v4 (minimalist): Too simple, security gaps

**Selection:** Hybrid of v2 and v3
- Security implementation from v2
- API design and simplicity from v3

**Rationale:** Security cannot be compromised, but v3's cleaner API design improved usability without sacrificing security.

### Example 2: Data Processing Pipeline

**Task:** Process large CSV files efficiently
**Configuration:** N=3 (performance-critical)
**Profiles:** pragmatic, performance-focused, minimalist

**Result:**
- v1 (pragmatic): Pandas-based, familiar but slow
- v2 (performance-focused): Custom streaming, 10x faster
- v3 (minimalist): Python CSV module, simple but slow

**Selection:** v2 (performance-focused)

**Rationale:** Performance requirements justified complexity. v2's streaming approach met throughput requirements while v1 and v3 could not scale.

## Philosophy Alignment

This workflow enforces:
- **Reduced Risk:** Multiple implementations catch errors single approach might miss
- **Exploration:** Different approaches reveal design trade-offs
- **Evidence-Based Selection:** Systematic comparison vs. gut feeling
- **Learning:** Rejected versions still provide valuable insights
- **Parallel Execution:** N implementations run simultaneously for efficiency

## Integration with Default Workflow

This workflow replaces Steps 4-5 (Research/Design and Implementation) of the DEFAULT_WORKFLOW when enabled. All other steps (requirements, testing, CI/CD) remain the same.

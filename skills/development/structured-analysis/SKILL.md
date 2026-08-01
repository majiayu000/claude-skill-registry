---
name: structured-analysis
description: 'Apply structured analytical frameworks to any artifact (prompts, systems,
  documents, code). 12 frameworks in 3 tiers: Core (4 universal), Auto-Invoke (specialized),
  On-Demand (advanced). Includes adve'
---

---
name: structured-analysis
description: Apply structured analytical frameworks to any artifact (prompts, systems, documents, code). 12 frameworks in 3 tiers: Core (4 universal), Auto-Invoke (specialized), On-Demand (advanced). Includes adversarial-review for finding blind spots and post-plan validation workflow.
---

# Structured Analysis Skill

**Auto-activate when:** User mentions analyze, review, validate, critique, framework, deep-analyze, reasoning-scaffold, adversarial-review, or asks to evaluate a plan, system, prompt, architecture, or design. Should activate when user asks "what could go wrong" or "review this".

Apply structured analytical frameworks to ANY artifact: prompts, systems, documents, code, architecture.

**12 Total Frameworks** organized in 3 tiers for easy selection.

## Framework Tiers

### Tier 1: Core Frameworks (Use Most Often)
- **deep-analyze**: Verification, gaps, adversarial review
- **reasoning-scaffold**: Systematic decisions with clear criteria
- **scope-boundary**: Prevent scope creep, MVP validation [NEW]
- **adversarial-review**: Red-team attack to find flaws/blind spots [NEW]

### Tier 2: Auto-Invoke (Triggered by Context)
- **zero-warning-verification**: Pre-commit quality gate (auto-runs)
- **security-first-design**: Auth/secrets/external data (conditional)
- **idempotency-audit**: Scripts/setup/migrations (conditional)

### Tier 3: On-Demand (Explicit Request Only)
- **meta-prompting**: Design optimal prompts
- **recursive-review**: 3-pass refinement
- **multi-perspective**: Multiple conflicting viewpoints
- **evidence-based-optimization**: Require proof before optimizing
- **deliberate-detail**: Comprehensive documentation
- **temperature-simulation**: Confidence calibration

**Selection Guide**: Start with Tier 1 for most tasks. Tier 2 frameworks auto-invoke when relevant. Request Tier 3 explicitly when needed.

## Technique Templates

### meta-prompting
**Best for**: Unfamiliar domains, maximum quality, vague prompts

```
You're an expert prompt designer.

Task: {BASE_PROMPT}

Design the optimal prompt considering:
- Essential context vs optional
- Optimal output format
- Explicit reasoning steps needed
- Constraints to prevent bad outputs
- Examples to eliminate ambiguity
- Quality verification steps

Execute the designed prompt.
```

### recursive-review
**Best for**: Building reusable templates, debugging prompts

```
{BASE_PROMPT}

Then optimize this through 3 versions:

Version 1: Add missing constraints
- What assumptions are implicit?
- What edge cases aren't covered?
- What outputs are undesirable?
- Add constraints to prevent these.

Version 2: Resolve ambiguities
- What terms need clearer definition?
- What scope is unclear (too broad/narrow)?
- What priorities might conflict?
- Clarify all ambiguities.

Version 3: Enhance reasoning depth
- What reasoning should be made explicit?
- Where would examples help?
- What verification steps should be built in?
- What quality bar should be set?

After all versions, execute the final optimized version.
```

### deep-analyze
**Best for**: High-stakes decisions, security analysis, confidence calibration

```
{BASE_PROMPT}

Phase 1: Initial Analysis
Provide thorough analysis.

Phase 2: Chain of Verification
1. **Incompleteness Check**: 3 ways analysis might be incomplete/biased
2. **Challenging Evidence**: Specific counter-examples, alternative interpretations, conflicting data
3. **Revised Findings**: What changed, strengthened, or introduced new uncertainties
4. **Confidence Calibration**: 0-100% with justification and key uncertainties

Phase 3: Adversarial Review
1. **5 Failure Modes**: Likelihood (L/M/H) and Impact (1-10) for each
2. **Top 3 Vulnerabilities**: Prioritize failures by importance
3. **Mitigations**: Strengthening strategies

Phase 4: Final Synthesis
- Core findings (with confidence levels)
- Key uncertainties
- Recommended actions
- Follow-up questions

Be self-critical. If verification doesn't find problems, analysis wasn't rigorous enough.
```

### multi-perspective
**Best for**: Complex trade-offs, stakeholder alignment, exploring options

```
{BASE_PROMPT}

Define 3 Expert Personas with conflicting priorities:

**Persona 1**: [Name/Role] - Priority: [X] - Background: [Expertise]
**Persona 2**: [Name/Role] - Priority: [Y conflicts with X] - Background: [Expertise]
**Persona 3**: [Name/Role] - Priority: [Z conflicts with X,Y] - Background: [Expertise]

Round 1: Opening Arguments
- **Persona 1**: [Priority justification, recommended approach]
- **Persona 2**: [Priority justification, recommended approach]
- **Persona 3**: [Priority justification, recommended approach]

Round 2: Critiques
- **Persona 1**: [Problems with 2 and 3]
- **Persona 2**: [Problems with 1 and 3]
- **Persona 3**: [Problems with 1 and 2]

Round 3: Refinement
- **Persona 1**: [Response to critiques, compromise area]
- **Persona 2**: [Response to critiques, compromise area]
- **Persona 3**: [Response to critiques, compromise area]

Synthesis:
- Points of Agreement
- Irreconcilable Differences
- Recommended Balanced Solution
- Sensitivity Analysis: If X priority dominates → Y approach

Personas must have genuine tension.
```

### deliberate-detail
**Best for**: Learning complex topics, comprehensive documentation

```
{BASE_PROMPT}

Do NOT summarize or be concise. Provide for every point:
- **Implementation details**: Step-by-step how it works
- **Edge cases**: Where it breaks/behaves unexpectedly
- **Failure modes**: What goes wrong and why
- **Historical context**: Why it exists, what it replaced
- **Trade-offs**: What you sacrifice
- **Alternatives**: Other approaches and why not chosen

Prioritize completeness over brevity.
```

### reasoning-scaffold
**Best for**: Systematic decisions, reproducible analysis

```
{BASE_PROMPT}

Step 1: Core Question
[Fundamental question being asked]

Step 2: Key Components
[Essential variables, entities, components - define each]

Step 3: Relationships
[Dependencies and interactions between components]

Step 4: Possible Approaches
[3-5 approaches with Description, Pros, Cons]

Step 5: Decision Criteria
[Criteria with relative weights/importance]

Step 6: Optimal Approach
[Selection justified against Step 5 criteria]

Step 7: Risk Analysis
[Risks and mitigation strategies]

Step 8: Final Recommendation
[Recommendation, confidence 0-100%, justification]
```

### temperature-simulation
**Best for**: Confidence calibration, catching mistakes

```
{BASE_PROMPT}

Response 1 - Junior Analyst (Uncertain, Over-Explains)
- Hedged language, caveats
- Step-by-step basic concepts
- Uncertain conclusions
[Junior's response]

Response 2 - Senior Expert (Confident, Direct)
- Bottom-line up front
- Assumes domain knowledge
- Concise, telegraphic
[Expert's response]

Synthesis - Balanced Integration
- What junior catches that expert glosses over
- What expert sees that junior misses
- Appropriately-calibrated answer
[Integrated response]
```

### adversarial-review [NEW]
**Best for**: Red-team attack on plans/systems to find flaws, edge cases, blind spots

```
{BASE_TARGET}

Phase 1: Challenge Assumptions
- What assumptions does this make?
- Which assumptions are most likely wrong?
- What happens if each assumption fails?

Phase 2: Edge Case Mining
- Boundary conditions (empty, null, max, negative)
- Timing issues (race conditions, ordering)
- Environment variations (OS, versions, permissions)
- Data quality issues (malformed, missing, duplicate)

Phase 3: Failure Mode Analysis
- List 5 ways this could fail
- For each: Likelihood (H/M/L), Impact (1-10), Mitigation
- Which failures are catastrophic?

Phase 4: Hidden Dependencies
- Undocumented state assumptions
- External service dependencies
- Implicit ordering requirements
- Configuration assumptions

Phase 5: Attack Vectors & Blind Spots
- What did we not consider?
- What expertise are we missing?
- Where could malicious input cause issues?
- What would break this in production?

Be adversarial. If you don't find issues, you weren't critical enough.
```

### scope-boundary [NEW]
**Best for**: Preventing scope creep, validating MVP, feature prioritization

```
{BASE_PLAN}

Phase 1: Core vs Nice-to-Have
- What is the ABSOLUTE minimum to solve the user's problem?
- What features are "just in case" rather than "must have"?
- What can be deferred to v2?

Phase 2: YAGNI Audit (You Aren't Gonna Need It)
- What abstractions/patterns aren't justified yet?
- What configuration/flexibility isn't required?
- What edge cases can be handled later?

Phase 3: Dependency Bloat
- What libraries/tools add unnecessary complexity?
- What can be done with stdlib/built-ins?
- What dependencies have large transitive footprints?

Phase 4: Simplification Opportunities
- Can this be split into smaller, independent pieces?
- What's the simplest implementation that works?
- What assumptions simplify the problem space?

Phase 5: Scope Recommendation
- **Keep**: Essential features (justify each)
- **Defer**: Nice-to-have for later
- **Remove**: YAGNI, premature optimization, over-engineering

Bias toward simplicity. Complexity requires strong justification.
```

### idempotency-audit [NEW]
**Best for**: Scripts, setup, migrations, state-changing operations

```
{BASE_SCRIPT}

Phase 1: Re-run Analysis
- What happens if this runs twice?
- What operations are not idempotent?
- What state does it assume?

Phase 2: Failure Recovery
- If this fails halfway, what's left in a broken state?
- Can it be safely retried?
- What cleanup is needed?

Phase 3: Detection Patterns
- Check-then-act (if not exists, create)
- Declarative operations (set to X, not increment)
- Cleanup old state before creating new

Phase 4: Idempotency Issues
List non-idempotent operations:
- **Operation**: [What it does]
- **Problem**: [Why it fails on re-run]
- **Fix**: [How to make it idempotent]

Phase 5: Recommendations
- What checks to add before operations
- What state detection is needed
- What rollback/cleanup logic is missing

All setup/install/migration scripts MUST be safely re-runnable.
```

### zero-warning-verification [NEW]
**Best for**: Pre-commit quality gate, test validation

```
{BASE_CHANGES}

Phase 1: Warning Audit
- Run relevant quality checks (make test, lint, type-check)
- Document ALL warnings (not just errors)
- Zero warnings is the requirement

Phase 2: Test Coverage
- Are new code paths tested?
- Do tests actually verify behavior (not just run)?
- Are edge cases covered?

Phase 3: Hidden Quality Issues
- Commented-out code to remove
- Debug prints/logging to clean up
- TODOs that should be addressed now
- Hardcoded values that need config

Phase 4: Breaking Changes
- API contract changes
- Backward compatibility issues
- Migration requirements

Phase 5: Quality Gate
- **PASS**: Zero warnings, tests pass, coverage adequate
- **FAIL**: Document specific issues blocking commit

`make test` showing warnings/failures is ALWAYS a blocking issue.
```

### security-first-design [NEW]
**Best for**: Authentication, secrets, external data, user input

```
{BASE_DESIGN}

Phase 1: Attack Surface
- What user input is accepted?
- What external data sources are used?
- What authentication/authorization is needed?
- What secrets/credentials are involved?

Phase 2: OWASP Top 10 Review
- Injection attacks (SQL, command, XSS)
- Broken authentication
- Sensitive data exposure
- XXE (XML External Entities)
- Broken access control
- Security misconfiguration
- Cross-Site Scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging & monitoring

Phase 3: Secret Management
- Where are secrets stored? (NEVER in code/git)
- How are secrets accessed? (env vars, vault)
- Are secrets rotatable?
- What happens if secrets leak?

Phase 4: Input Validation
- What input validation is applied?
- Are allow-lists used (not deny-lists)?
- Is input sanitized before use?
- Are file uploads restricted?

Phase 5: Security Recommendations
- **CRITICAL**: Must-fix security issues
- **HIGH**: Should-fix vulnerabilities
- **MEDIUM**: Defense-in-depth improvements

Default to paranoid. Security issues are blocking.
```

### evidence-based-optimization [NEW]
**Best for**: Performance work, refactoring, architectural changes

```
{BASE_OPTIMIZATION}

Phase 1: Problem Validation
- What specific problem does this solve?
- What evidence shows this is a problem?
- What metrics demonstrate the issue?

Phase 2: Baseline Measurement
- What's the current performance?
- How was it measured?
- Is the measurement methodology valid?

Phase 3: Alternative Solutions
For each alternative:
- **Approach**: [Description]
- **Complexity**: [Implementation effort]
- **Expected Impact**: [Quantified improvement]
- **Risks**: [What could go wrong]

Phase 4: Proof Requirement
- What benchmarks prove this optimization works?
- What's the expected improvement (quantified)?
- How will we verify it in production?

Phase 5: Optimization Decision
- **Recommended**: [Approach with best effort/impact ratio]
- **Evidence Required**: [What to measure before/after]
- **Success Criteria**: [Quantified improvement goal]

NEVER optimize without measuring. Premature optimization is evil.
```

## Post-Plan Validation Workflow

**Trigger**: After user approves plan via ExitPlanMode

**Process**:
1. **Always spawn**: adversarial-review agent (find flaws/blind spots)
2. **Conditional spawn**:
   - idempotency-audit (if plan touches scripts/setup/migrations)
   - security-first-design (if plan involves auth/secrets/external data)
3. **Run in parallel**: 30-60 seconds total
4. **Categorize findings**:
   - 🚨 CRITICAL: Blocks execution (security, data loss, breaking changes)
   - ⚠️ IMPORTANT: Should address (edge cases, missing validation)
   - 💡 SUGGESTIONS: Nice to have (optimizations, improvements)
5. **Present to user**:
   - If CRITICAL: Block execution, require fixes
   - If only IMPORTANT/SUGGESTIONS: Show findings, user decides to proceed/adjust

**Benefits**: Fast planning (no bloat), thorough validation (catches issues early), user control (advisory findings don't block)

## Technique Combinations

- `meta-prompting,recursive-review` - Design then refine
- `deep-analyze,multi-perspective` - Rigorous multi-angle analysis
- `reasoning-scaffold,deliberate-detail` - Structured exploration with depth
- `multi-perspective,reasoning-scaffold` - Multiple viewpoints, systematic comparison
- `adversarial-review,scope-boundary` - Challenge plan, trim scope
- `security-first-design,adversarial-review` - Security review with red-team attack
- **Order**: meta-prompting → recursive-review → deep-analyze → multi-perspective

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Over-engineering | deep-analyze for "syntax of X" | Match complexity to importance |
| Template rigidity | Following steps blindly | Adapt/skip irrelevant steps |
| Verification theater | Finding nothing wrong | Genuine critique required |
| Persona stereotyping | Generic "lawyer vs cowboy" | Specific realistic priorities |
| Missing synthesis | Just listing perspectives | Must integrate views |
| Fake adversarial | Not finding issues | Be genuinely critical |
| Scope creep | "While we're at it..." | MVP first, defer nice-to-haves |

## Effectiveness Indicators

**Strong**: Analysis finds real problems, personas conflict, confidence varies, verification changes conclusions, approaches differ, scope gets trimmed, security issues found
**Weak**: No issues found, personas agree, perspectives identical, no constraints added, superficial application, rubber-stamp approval

## Integration Notes

- `/optimize-prompt [techniques] <prompt>` - Apply techniques
- `/prompt-help [technique]` - View documentation
- Auto-selection uses decision tree when techniques unspecified
- Balance token cost vs value
- These scaffold reasoning processes, not magic keywords
- Post-plan validation runs automatically after plan approval
- Tier 2 frameworks auto-invoke based on context detection

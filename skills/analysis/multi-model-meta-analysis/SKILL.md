---
name: multi-model-meta-analysis
description: |
  Synthesize outputs from multiple AI models into a comprehensive, verified assessment. Use when: (1) User pastes feedback/analysis from multiple LLMs (Claude, GPT, Gemini, etc.) about code or a project, (2) User wants to consolidate model outputs into a single reliable document, (3) User needs conflicting model claims resolved against actual source code. This skill verifies model claims against the codebase, resolves contradictions with evidence, and produces a more reliable assessment than any single model.
---

# Multi-Model Synthesis

Combine outputs from multiple AI models into a verified, comprehensive assessment by cross-referencing claims against the actual codebase.

## Core Principle

Models hallucinate and contradict each other. The source code is the source of truth. Every significant claim must be verified before inclusion in the final assessment.

## Process

### 1. Extract Claims

Parse each model's output and extract discrete claims:
- Factual assertions about the code ("function X does Y", "there's no error handling in Z")
- Recommendations ("should add validation", "refactor this pattern")
- Identified issues ("bug in line N", "security vulnerability")

Tag each claim with its source model.

### 2. Deduplicate

Group semantically equivalent claims:
- "Lacks input validation" = "No sanitization" = "User input not checked"
- "Should use async/await" = "Convert to promises" = "Make asynchronous"

Create canonical phrasing. Track which models mentioned each.

### 3. Verify Against Source

For each factual claim or identified issue:

```
CLAIM: "The auth middleware doesn't check token expiry"
VERIFY: Read the auth middleware file
FINDING: [Confirmed | Refuted | Partially true | Cannot verify]
EVIDENCE: [Quote relevant code or explain why claim is wrong]
```

Use Grep, Glob, and Read tools to locate and examine relevant code. Do not trust model claims without verification.

### 4. Resolve Conflicts

When models contradict each other:

1. Identify the specific disagreement
2. Examine the actual code
3. Determine which model (if any) is correct
4. Document the resolution with evidence

```
CONFLICT: Model A says "uses SHA-256", Model B says "uses MD5"
INVESTIGATION: Read crypto.js lines 45-60
RESOLUTION: Model B is correct - line 52 shows MD5 usage
EVIDENCE: `const hash = crypto.createHash('md5')`
```

### 5. Synthesize Assessment

Produce a final document that:
- States verified facts (not model opinions)
- Cites evidence for significant claims
- Notes where verification wasn't possible
- Preserves valuable insights that don't require verification (e.g., design suggestions)

## Output Format

```markdown
# Synthesized Assessment: [Topic]

## Summary
[2-3 sentences describing the verified findings]

## Verified Findings

### Confirmed Issues
| Issue | Severity | Evidence | Models |
|-------|----------|----------|--------|
| [Issue] | High/Med/Low | [file:line or quote] | Claude, GPT |

### Refuted Claims
| Claim | Source | Reality |
|-------|--------|---------|
| [What model said] | GPT-4 | [What code actually shows] |

### Unverifiable Claims
| Claim | Source | Why Unverifiable |
|-------|--------|------------------|
| [Claim] | Claude | [Requires runtime testing / external system / etc.] |

## Consensus Recommendations
[Items where 2+ models agree AND verification supports the suggestion]

## Unique Insights Worth Considering
[Valuable suggestions from single models that weren't contradicted]

## Conflicts Resolved
| Topic | Model A | Model B | Verdict | Evidence |
|-------|---------|---------|---------|----------|
| [Topic] | [Position] | [Position] | [Which is correct] | [Code reference] |

## Action Items

### Critical (Verified, High Impact)
- [ ] [Item] — Evidence: [file:line]

### Important (Verified, Medium Impact)
- [ ] [Item] — Evidence: [file:line]

### Suggested (Unverified but Reasonable)
- [ ] [Item] — Source: [Models]
```

## Verification Guidelines

**Always verify:**
- Bug reports and security issues
- Claims about what code does or doesn't do
- Assertions about missing functionality
- Performance or complexity claims

**Trust but note source:**
- Style and readability suggestions
- Architectural recommendations
- Best practice suggestions

**Mark as unverifiable:**
- Runtime behavior claims (without tests)
- Performance benchmarks (without profiling)
- External API behavior
- User experience claims

## Anti-Patterns

- Blindly merging model outputs without checking code
- Treating model consensus as proof (all models can be wrong)
- Omitting refuted claims (document what was wrong - it's valuable)
- Skipping verification because claims "sound right"

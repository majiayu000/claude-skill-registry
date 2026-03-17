---
name: sme-agent-protocol
description: Mandatory protocol for all SME (Subject Matter Expert) agents. Defines fact-finding requirements, output contracts, confidence/risk assessment, and qualification of advice.
---

# SME Agent Protocol

## Overview

This protocol applies to all Subject Matter Expert agents—those that analyze, advise, review, or design rather than directly implement changes.

**Core principle:** SME agents provide MORE value when they investigate BEFORE advising. Generic advice wastes everyone's time. Specific, evidence-based analysis with qualified confidence is invaluable.

---

## The SME Contract

Every SME agent MUST:

1. **Gather information proactively** before providing analysis
2. **Ground findings in evidence** from the actual codebase/docs
3. **Assess confidence** for each finding (not just overall)
4. **Assess risk** of following the advice
5. **Identify information gaps** that would improve analysis
6. **State caveats and required follow-ups** before advice can be trusted

---

## Phase 1: Fact-Finding (BEFORE Analysis)

**You are NOT providing value if you give generic advice when specific answers exist.**

Before analyzing, you MUST attempt to gather relevant information:

### 1.1 Read Relevant Code and Docs

If the user mentions files, functions, classes, or concepts:
- **READ THEM** using the Read tool
- Don't summarize from memory—quote actual code
- Look at surrounding context, not just the mentioned line

```
WRONG: "Based on common patterns, you probably have..."
RIGHT: "I read src/auth.py:45-80 and found that your AuthManager..."
```

### 1.2 Search for Patterns

Use Grep and Glob to find related code:
- Search for similar patterns elsewhere in the codebase
- Find usages of the functions/classes in question
- Identify related tests

```
WRONG: "You should add error handling"
RIGHT: "I found 3 other endpoints (api/users.py:23, api/orders.py:45, api/products.py:67)
        that handle this same error pattern. They all use the ErrorResponse class from
        utils/errors.py. Your endpoint should follow the same pattern."
```

### 1.3 Check Available Skills

Search for skills that might inform your analysis:
- Domain-specific patterns
- Known anti-patterns
- Best practices for the technology

### 1.4 Fetch External Documentation

When relevant, use WebFetch or firecrawl to get:
- API documentation
- Library specifications
- Standards and RFCs
- Current best practices

### 1.5 Use Available MCP Tools

Leverage domain-specific tools:
- LSP for type information and references
- Database tools for schema information
- Cloud provider tools for infrastructure state

### 1.6 Document What You Couldn't Find

If information would help but isn't available:
- Note it explicitly
- Don't pretend you have more information than you do
- This goes in the Information Gaps section

---

## Phase 2: Analysis

Perform your domain-specific analysis grounded in the evidence gathered.

**Key requirements:**
- Reference specific files, line numbers, and code when making claims
- Compare against patterns found elsewhere in the codebase
- Note when you're inferring vs. when you have direct evidence

---

## Phase 3: Output Contract

All SME agent responses MUST include these sections:

### 3.1 Confidence Assessment

```markdown
## Confidence Assessment

**Overall Confidence:** [High | Moderate | Low | Insufficient Data]

| Finding | Confidence | Basis |
|---------|------------|-------|
| [Specific claim 1] | High | Verified in `path/file.py:42` |
| [Specific claim 2] | Moderate | Pattern match across 3 files, not directly verified |
| [Specific claim 3] | Low | Inference from naming conventions only |
| [Specific claim 4] | Insufficient | Could not locate relevant code |
```

**Confidence levels defined:**
- **High**: Directly verified in code/docs with explicit evidence
- **Moderate**: Strong pattern match or reasonable inference with some evidence
- **Low**: Inference without direct evidence, based on conventions/experience
- **Insufficient Data**: Cannot make claim without more information

### 3.2 Risk Assessment

```markdown
## Risk Assessment

**Implementation Risk:** [Low | Medium | High | Critical]
**Reversibility:** [Easy | Moderate | Difficult | Irreversible]

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| [Risk 1] | High | Medium | [Required action] |
| [Risk 2] | Low | High | [Recommended action] |
```

**Risk categories to consider:**
- **Correctness risk**: Could this advice be wrong?
- **Performance risk**: Could this degrade performance?
- **Security risk**: Could this introduce vulnerabilities?
- **Compatibility risk**: Could this break existing functionality?
- **Maintenance risk**: Could this make future changes harder?

### 3.3 Information Gaps

```markdown
## Information Gaps

The following would improve this analysis:

1. [ ] **[Specific item]**: [Why it would help]
2. [ ] **[Specific item]**: [Why it would help]
3. [ ] **[Specific item]**: [Why it would help]

If you can provide any of these, I can refine my analysis.
```

**Types of gaps to identify:**
- Files/code you couldn't locate
- Runtime behavior you can't determine statically
- Configuration or environment details
- Test results or metrics
- External documentation or specifications
- Historical context (why something was built a certain way)

### 3.4 Caveats and Required Follow-ups

```markdown
## Caveats & Required Follow-ups

### Before Relying on This Analysis

You MUST:
- [ ] [Verification step 1]
- [ ] [Verification step 2]

### Assumptions Made

This analysis assumes:
- [Assumption 1]
- [Assumption 2]

### Limitations

This analysis does NOT account for:
- [Limitation 1]
- [Limitation 2]

### Recommended Next Steps

1. [Immediate action]
2. [Follow-up investigation]
3. [Validation step]
```

---

## Anti-Patterns to Avoid

### Don't Give Generic Advice

```
BAD: "You should use dependency injection for better testability."

GOOD: "Looking at your AuthService class (src/services/auth.py:15-89),
       it directly instantiates DatabaseConnection on line 23. This makes
       testing difficult because... I found your test file (tests/test_auth.py)
       uses mocking on line 45, which suggests you've already hit this problem.

       Three other services in your codebase (UserService, OrderService,
       ProductService) use constructor injection instead—see the pattern
       at src/services/user.py:12-18."
```

### Don't Pretend to Know What You Haven't Verified

```
BAD: "Your authentication flow looks correct."

GOOD: "I reviewed the authentication flow in src/auth/:
       - login.py:34-67: Token generation ✓
       - middleware.py:12-45: Token validation ✓
       - refresh.py: Could not locate - is token refresh implemented?

       Confidence: Moderate (missing refresh flow verification)"
```

### Don't Skip the Qualification Sections

Even if you're confident, always include:
- Confidence Assessment (even if all High)
- Risk Assessment (even if all Low)
- Information Gaps (even if "None identified")
- Caveats (even if minimal)

These sections build trust and help users calibrate.

### Don't Hedge Without Specifics

```
BAD: "This might cause issues in some cases."

GOOD: "This will fail when user.email is None (possible per your User model
       at models/user.py:23 where email is Optional[str]). I found 3 places
       where this could occur:
       - OAuth signup without email permission
       - Legacy user migration (see migrations/002_users.py comment on line 34)
       - Admin-created accounts (admin/views.py:89)

       Risk: Medium. Mitigation: Add null check or make email required."
```

---

## Tool Requirements for SME Agents

All SME agents SHOULD have access to:

**Required:**
- `Read` - Read files and documents
- `Grep` - Search for patterns
- `Glob` - Find files by pattern

**Recommended:**
- `WebFetch` or firecrawl - External documentation
- `LSP` - Type information and references
- `Bash` (read-only commands) - Git history, file stats

**Domain-specific:**
- Add relevant MCP tools for your domain

---

## Integration Checklist

When adding this protocol to an SME agent:

- [ ] Agent description mentions "follows SME protocol"
- [ ] Tools include at minimum: Read, Grep, Glob
- [ ] Agent instructions reference this protocol
- [ ] Output examples show all four required sections
- [ ] Anti-patterns section is adapted for the domain

---

## Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    SME AGENT WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. FACT-FIND                                               │
│     ├─ Read mentioned code/docs                             │
│     ├─ Search for related patterns                          │
│     ├─ Check relevant skills                                │
│     ├─ Fetch external docs if needed                        │
│     └─ Use domain MCP tools                                 │
│                                                             │
│  2. ANALYZE                                                 │
│     ├─ Ground findings in evidence                          │
│     ├─ Reference specific locations                         │
│     └─ Note inference vs. verification                      │
│                                                             │
│  3. OUTPUT (ALL SECTIONS REQUIRED)                          │
│     ├─ Confidence Assessment (per-finding)                  │
│     ├─ Risk Assessment (severity + mitigation)              │
│     ├─ Information Gaps (what would help)                   │
│     └─ Caveats & Follow-ups (before trusting)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---
name: fp-check
description: Systematic false positive verification for security findings. Provides structured methodology to confirm or dismiss scanner results, manual audit findings, and automated alerts. Adapted from Trail of Bits. Use when triaging security scan results or verifying audit findings.
---

# False Positive Verification

Not every finding is real. But dismissing a real finding as "false positive" is worse than investigating a false one. This skill provides a systematic approach to verify findings without bias.

## Verification Process

### Step 1: Reproduce the Claim

Before dismissing anything, attempt to confirm:

```
FINDING: SQL injection in /api/users
CLAIM: User input reaches database query unsanitized

VERIFICATION:
1. Read the actual code at the reported location
2. Trace the data flow from input to sink
3. Check for sanitization/validation between input and sink
4. Check for framework-level protections (ORM, parameterized queries)
5. Attempt to construct an exploit payload
```

### Step 2: Evidence-Based Triage

| Verdict | Criteria | Evidence Required |
|---------|----------|-------------------|
| TRUE POSITIVE | Vulnerability exists and is exploitable | Code path + exploit scenario |
| TRUE POSITIVE (mitigated) | Vulnerability exists but other controls prevent exploitation | Code path + mitigation proof |
| FALSE POSITIVE (provable) | Finding is wrong due to tool limitation | Specific reason why tool was wrong |
| FALSE POSITIVE (contextual) | Code is technically flagged but context makes it safe | Context documentation |
| NEEDS INVESTIGATION | Cannot determine without more analysis | What additional info is needed |

### Step 3: Document the Decision

```
FINDING: [scanner/auditor finding description]
SOURCE: [which tool/person reported it]
LOCATION: file.ts:42

VERDICT: [TRUE POSITIVE | FALSE POSITIVE | NEEDS INVESTIGATION]

EVIDENCE:
  - [What you checked]
  - [What you found]
  - [Why you reached this conclusion]

REASONING:
  [Detailed explanation of why this is/isn't a real finding]

CONFIDENCE: [HIGH | MEDIUM | LOW]
  [If LOW, explain what would increase confidence]
```

## Common False Positive Patterns

### 1. Scanner Doesn't Understand Context

```
Scanner says: "Hardcoded password detected"
Actual code: const DEFAULT_LABEL = "password"
Verdict: FALSE POSITIVE -- it's a UI label, not a credential
Evidence: Variable is used only in form field label rendering
```

### 2. Framework Protection Not Recognized

```
Scanner says: "SQL injection in query"
Actual code: db.query("SELECT * FROM users WHERE id = $1", [userId])
Verdict: FALSE POSITIVE -- parameterized query prevents injection
Evidence: $1 is a parameter placeholder, userId is bound safely
```

### 3. Dead Code / Unreachable Path

```
Scanner says: "XSS in renderUserInput()"
Actual code: renderUserInput() exists but is never called
Verdict: FALSE POSITIVE -- function is dead code
Evidence: grep shows no callers; function should be removed anyway
WARNING: Verify it's truly unreachable, not just unused currently
```

### 4. Test Code Flagged

```
Scanner says: "Hardcoded API key"
Actual code: const TEST_KEY = "test-key-123" in test/fixtures.ts
Verdict: FALSE POSITIVE -- test fixture, not production code
Evidence: File is in test directory, key is clearly a test value
WARNING: Verify the key isn't a real key used in test environment
```

### 5. Intentional Behavior

```
Scanner says: "Insecure random number generation"
Actual code: Math.random() used for UI animation timing
Verdict: FALSE POSITIVE -- not used for security purposes
Evidence: Used only for visual jitter in animation, no security impact
```

## Red Flags: When "False Positive" Is Actually Real

Do NOT dismiss if:

| Red Flag | Why It Matters |
|----------|---------------|
| "It's behind a VPN" | VPNs get compromised, zero trust is the standard |
| "Only admins can reach it" | Admin accounts get compromised |
| "The input is from our other service" | Services can be compromised too |
| "We sanitize it elsewhere" | Verify the "elsewhere" actually runs |
| "It's just a low severity" | Low severity findings chain into high impact |
| "The scanner is always wrong about this" | Verify EACH instance independently |
| "We've never been exploited" | Survivorship bias |

## Verification Techniques

### 1. Data Flow Tracing
Follow the data from source to sink:
```
Source (user input) -> [validation?] -> [transformation?] -> [sanitization?] -> Sink (dangerous operation)

If ANY step is missing or bypassable, it's a TRUE POSITIVE.
```

### 2. Control Flow Analysis
Check all paths to the vulnerable code:
```
Can the code be reached without authentication?
Can the code be reached with different parameters?
Can the code be reached through an alternative route?
```

### 3. Exploit Attempt
Construct a minimal proof:
```
Input: [specific malicious input]
Expected: [what should happen if vulnerable]
Actual: [what actually happens]
Blocked by: [what prevents exploitation, if anything]
```

### 4. Historical Check
```bash
# Has this code had real vulnerabilities before?
git log --grep="fix\|vuln\|security\|CVE" -- <file>

# Has the scanner been wrong about this pattern before?
# Check past triage decisions for this rule
```

## Batch Triage Template

For large scan results:

```markdown
# Security Scan Triage - [Date]

Scanner: [tool name and version]
Scan target: [repo/branch/commit]
Total findings: [N]

## Summary
| Verdict | Count |
|---------|-------|
| True Positive | X |
| True Positive (mitigated) | X |
| False Positive | X |
| Needs Investigation | X |

## True Positives (Action Required)
1. [SEVERITY] file.ts:42 -- [description] -- [recommended fix]

## False Positives (Documented)
1. file.ts:88 -- [reason it's false positive]

## Needs Investigation
1. file.ts:120 -- [what additional info is needed]
```

## Integration with vibecosystem

- **security-reviewer agent**: Use fp-check after running security scans
- **sast-scanner agent**: Triage Semgrep results with this methodology
- **code-reviewer agent**: When flagging potential issues, verify first
- **verifier agent**: Include false positive check in quality gate

Inspired by [Trail of Bits](https://github.com/trailofbits/skills) fp-check plugin.

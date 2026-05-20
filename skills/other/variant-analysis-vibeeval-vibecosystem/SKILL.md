---
name: variant-analysis
description: Find similar vulnerabilities across a codebase after discovering one instance. Uses pattern matching, AST search, Semgrep/CodeQL queries, and manual tracing to propagate findings. Adapted from Trail of Bits. Use after finding a bug to check if the same pattern exists elsewhere.
---

# Variant Analysis

When you find a bug, the same mistake almost certainly exists elsewhere. Variant analysis systematically hunts for siblings of a known vulnerability.

## Process

### Step 1: Characterize the Original Bug

Before searching, understand what makes this bug a bug:

```
ORIGINAL BUG:
  File: src/api/users.ts:42
  Type: Missing input validation
  Pattern: req.params.id used directly in DB query without sanitization
  Root cause: Developer assumed framework sanitizes params
  Trigger: Untrusted input reaches database query
```

Extract the **abstract pattern** -- not the specific code, but the class of mistake:
- Missing validation at a trust boundary
- Incorrect error handling in auth path
- Race condition between check and use
- Hardcoded secret in source
- SQL injection via string concatenation

### Step 2: Generate Search Queries

For each bug class, create multiple search strategies:

#### Grep/Ripgrep (Fast, broad)
```bash
# Example: SQL injection via concatenation
rg "query\(.*\+.*\)" --type ts
rg "execute\(.*\$\{" --type ts
rg "\.raw\(.*\+" --type ts

# Example: Missing auth middleware
rg "router\.(get|post|put|delete)\(" --type ts -l | \
  xargs rg -L "authenticate|authorize|requireAuth"

# Example: Hardcoded secrets
rg "(password|secret|key|token)\s*[=:]\s*['\"][^'\"]{8,}" --type ts
```

#### Semgrep (AST-aware, precise)
```yaml
# Example: SQL injection
rules:
  - id: sql-injection-concatenation
    patterns:
      - pattern: $DB.query($X + ...)
      - pattern-not: $DB.query($X, [...])
    message: "Potential SQL injection via string concatenation"
    severity: ERROR

# Example: Missing null check before use
rules:
  - id: null-deref-after-find
    patterns:
      - pattern: |
          const $X = await $DB.findOne(...)
          ...
          $X.$PROP
      - pattern-not: |
          const $X = await $DB.findOne(...)
          ...
          if ($X) { ... }
    message: "Using findOne result without null check"
    severity: WARNING
```

#### CodeQL (Deep analysis)
```ql
// Example: Tainted data reaching SQL
import javascript

from CallExpr call, DataFlow::Node source, DataFlow::Node sink
where
  source = DataFlow::parameterNode(any(Function f).getAParameter()) and
  sink = call.getArgument(0) and
  call.getCalleeName() = "query" and
  DataFlow::localFlow(source, sink)
select sink, "Untrusted input flows to SQL query"
```

### Step 3: Triage Results

For each match:

| Status | Meaning | Action |
|--------|---------|--------|
| CONFIRMED | Same bug pattern, exploitable | File as finding |
| LIKELY | Same pattern, needs deeper analysis | Investigate further |
| MITIGATED | Pattern present but other controls prevent exploitation | Document as defense-in-depth gap |
| FALSE POSITIVE | Pattern matches but context makes it safe | Document why it's safe |

### Step 4: Report

```
## Variant Analysis Report

**Original Finding**: [reference to original bug]
**Pattern**: [abstract description of the vulnerability class]
**Search Method**: [grep/semgrep/codeql/manual]

### Confirmed Variants

1. **[SEVERITY]** file.ts:42 -- [description]
2. **[SEVERITY]** other.ts:88 -- [description]

### Likely Variants (Need Investigation)

3. file2.ts:15 -- [why it might be vulnerable]

### Mitigated Instances

4. safe.ts:30 -- Same pattern but [mitigation] prevents exploitation

### Statistics

- Files scanned: X
- Matches found: Y
- Confirmed: Z
- False positives: W
```

## Common Variant Patterns

### Input Validation Variants
If one endpoint lacks validation, check ALL endpoints:
```bash
# Find all route handlers
rg "router\.(get|post|put|delete|patch)\(" --type ts -n

# Check each for validation middleware
# Missing validation = variant
```

### Auth/Authz Variants
If one route lacks auth, check all routes:
```bash
# Find routes without auth middleware
rg "app\.(get|post)\(['\"]" --type ts | grep -v "auth\|protect\|require"
```

### Error Handling Variants
If one catch block leaks info, check all catch blocks:
```bash
rg "catch.*\{" -A 3 --type ts | grep -E "res\.(send|json).*err"
```

### Crypto Variants
If one place uses weak crypto, check all crypto usage:
```bash
rg "createHash\(|createCipher\(|randomBytes\(" --type ts
rg "MD5\|SHA1\|DES\|RC4" --type ts
```

### Race Condition Variants
If one TOCTOU exists, check similar check-then-act patterns:
```bash
rg "if.*await.*find" -A 5 --type ts | grep -E "await.*(update|delete|create)"
```

## Automation Integration

### With coroner agent (post-mortem)
After fixing a bug, coroner should:
1. Call variant-analysis with the bug pattern
2. Check all confirmed variants
3. Create tasks for each variant fix

### With security-reviewer agent
During review, if a finding is discovered:
1. Pause the linear review
2. Run variant analysis for the finding class
3. Include all variants in the review report

### With code-reviewer agent
When a fix is reviewed:
1. Check if the fix addresses all known variants
2. Verify the fix pattern is applied consistently

## Rationalizations to Reject

| Rationalization | Why It's Wrong | Required Action |
|----------------|---------------|-----------------|
| "It's just one instance" | Bugs travel in packs | Run variant analysis |
| "The other code is different" | Same pattern, different syntax | Abstract the pattern |
| "We already fixed this area" | Fix might be incomplete | Verify with search |
| "Semgrep didn't find anything" | Rules might be too specific | Try multiple search methods |
| "It's too many results" | Volume doesn't mean false positive | Triage each result |

Inspired by [Trail of Bits](https://github.com/trailofbits/skills) variant-analysis plugin.

---
# VERSION: 2.88.0
name: defense-profiler
description: "Codebase defense analysis system for security profiling"
user-invocable: true
---

# Defense Profiler

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

**Codebase Defense Analysis System** inspired by ZeroLeaks defense profiling.

Systematically analyzes code to build a comprehensive profile of security defenses, patterns, and weaknesses.

## Core Concept

Before attacking (testing), understand the defenses. Build a mental model of:
- What patterns exist
- What safeguards are in place
- What triggers failures
- What areas are weak

## Usage

```bash
/defense-profile src/
/defense-profile --focus security src/auth/
/defense-profile --output profile.json src/api/
```

## Defense Levels

| Level | Description | Characteristics |
|-------|-------------|-----------------|
| `none` | No apparent protection | Direct vulnerabilities, no validation |
| `weak` | Basic protections | Simple validation, incomplete coverage |
| `moderate` | Standard defenses | Input validation, error handling |
| `strong` | Good security | Multiple layers, proper sanitization |
| `hardened` | Defense in depth | Multi-layered, comprehensive coverage |

## Profile Structure

```typescript
interface DefenseProfile {
  // Overall assessment
  level: DefenseLevel;
  confidence: number;  // 0-1

  // Observed patterns
  observedBehaviors: string[];

  // Guardrails in place
  guardrails: {
    type: string;
    strength: number;
    coverage: string[];
    bypassed: boolean;
    bypassMethod?: string;
  }[];

  // Identified weaknesses
  weaknesses: {
    category: string;
    description: string;
    exploitability: number;  // 0-1
    location?: string;
  }[];

  // Trigger patterns
  refusalTriggers: string[];  // What causes errors/rejects
  safePatterns: string[];     // What passes through

  // Response patterns
  responsePatterns: {
    pattern: string;
    frequency: number;
    defenseIndicator: boolean;
  }[];
}
```

## Analysis Dimensions

### 1. Input Validation

```yaml
dimension: input_validation
checks:
  - type_checking: Are inputs typed?
  - null_handling: Are nulls handled?
  - boundary_checks: Are limits enforced?
  - sanitization: Is input sanitized?
  - encoding_handling: Are encodings handled?

signals:
  weak:
    - No type annotations
    - Missing null checks
    - Unconstrained inputs
  strong:
    - Zod/Joi schemas
    - TypeScript strict mode
    - Comprehensive validation
```

### 2. Authentication/Authorization

```yaml
dimension: auth_security
checks:
  - auth_mechanism: How is auth implemented?
  - session_management: How are sessions handled?
  - permission_checks: Are permissions verified?
  - token_validation: Are tokens properly validated?

signals:
  weak:
    - Plain text passwords
    - No CSRF protection
    - Missing auth middleware
  strong:
    - bcrypt/argon2 hashing
    - JWT with refresh tokens
    - RBAC implementation
```

### 3. Error Handling

```yaml
dimension: error_handling
checks:
  - error_exposure: Are errors exposed?
  - logging_security: Are logs secure?
  - graceful_degradation: Does it fail safely?
  - recovery_patterns: Are there recovery mechanisms?

signals:
  weak:
    - Stack traces in responses
    - Sensitive data in logs
    - Unhandled promise rejections
  strong:
    - Generic error messages
    - Structured logging
    - Error boundaries
```

### 4. Data Protection

```yaml
dimension: data_protection
checks:
  - encryption_at_rest: Is data encrypted?
  - encryption_in_transit: Is TLS used?
  - secret_management: How are secrets handled?
  - pii_handling: Is PII protected?

signals:
  weak:
    - Hardcoded secrets
    - No encryption
    - PII in logs
  strong:
    - Environment variables
    - Key management service
    - Data masking
```

### 5. Injection Prevention

```yaml
dimension: injection_prevention
checks:
  - sql_injection: Are queries parameterized?
  - xss_prevention: Is output escaped?
  - command_injection: Are commands sanitized?
  - path_traversal: Are paths validated?

signals:
  weak:
    - String concatenation in queries
    - innerHTML usage
    - Shell commands with user input
  strong:
    - ORM with parameterization
    - Content Security Policy
    - Input whitelisting
```

## Pattern Detection

### Refusal Triggers

Patterns that cause the code to reject/fail:

```typescript
const refusalPatterns = [
  // Authentication failures
  /unauthorized|unauthenticated|forbidden/i,

  // Validation failures
  /invalid|malformed|bad request/i,

  // Security blocks
  /blocked|denied|not allowed/i,

  // Rate limiting
  /too many requests|rate limit/i
];
```

### Leak Indicators

Patterns suggesting information exposure:

```typescript
const leakPatterns = [
  // Configuration exposure
  /config|settings|environment/i,

  // Implementation details
  /stack trace|internal error|debug/i,

  // Sensitive data
  /password|secret|token|key/i
];
```

## Profiling Algorithm

```python
def build_defense_profile(codebase):
    """
    Build comprehensive defense profile.

    Returns:
        DefenseProfile with all assessments
    """
    profile = DefenseProfile()

    # Phase 1: Static Analysis
    patterns = analyze_static_patterns(codebase)
    profile.observedBehaviors.extend(patterns)

    # Phase 2: Dependency Analysis
    deps = analyze_dependencies(codebase)
    profile.guardrails.extend(identify_guardrails(deps))

    # Phase 3: Pattern Matching
    for file in codebase.files:
        weak_signals = match_weak_patterns(file)
        strong_signals = match_strong_patterns(file)

        profile.weaknesses.extend(weak_signals)
        profile.responsePatterns.extend(strong_signals)

    # Phase 4: Level Assessment
    profile.level = calculate_defense_level(profile)
    profile.confidence = calculate_confidence(profile)

    return profile


def calculate_defense_level(profile):
    """
    Calculate overall defense level based on signals.
    """
    weak_count = len(profile.weaknesses)
    strong_count = len([g for g in profile.guardrails if g.strength > 0.7])

    ratio = strong_count / (weak_count + strong_count + 1)

    if ratio > 0.9:
        return "hardened"
    elif ratio > 0.7:
        return "strong"
    elif ratio > 0.4:
        return "moderate"
    elif ratio > 0.2:
        return "weak"
    else:
        return "none"
```

## Integration with Ralph Loop

Defense profiling runs early in the analysis:

```yaml
Step 1b: GAP-ANALYST
  - Defense Profiler (if security-related task)

Step 6: EXECUTE-WITH-SYNC
  - 6a. LSA-VERIFY
      - Check against Defense Profile

Step 7: VALIDATE
  - 7c. ADVERSARIAL-CODE
      - Use Defense Profile to guide analysis
```

### Invocation

```yaml
Task:
  subagent_type: "defense-profiler"
  model: "sonnet"
  prompt: |
    TARGET_PATH: src/
    FOCUS: security
    DEPTH: comprehensive

    Build defense profile for the target codebase.
    Identify:
    - Current defense level
    - Active guardrails
    - Weaknesses and their exploitability
    - Patterns and signals
```

## Output Format

```json
{
  "defense_profile": {
    "level": "moderate",
    "confidence": 0.78,
    "summary": "Codebase has standard defenses with some gaps",

    "guardrails": [
      {
        "type": "input_validation",
        "strength": 0.65,
        "coverage": ["api/auth", "api/users"],
        "bypassed": false
      },
      {
        "type": "rate_limiting",
        "strength": 0.80,
        "coverage": ["api/*"],
        "bypassed": false
      }
    ],

    "weaknesses": [
      {
        "category": "injection",
        "description": "SQL concatenation in legacy queries",
        "exploitability": 0.7,
        "location": "src/db/legacy.ts:45"
      },
      {
        "category": "auth",
        "description": "Missing CSRF token validation",
        "exploitability": 0.5,
        "location": "src/middleware/auth.ts"
      }
    ],

    "recommendations": [
      "Migrate legacy queries to parameterized ORM",
      "Add CSRF middleware to state-changing endpoints",
      "Implement rate limiting on auth endpoints"
    ]
  },

  "analysis_metadata": {
    "files_analyzed": 156,
    "patterns_matched": 23,
    "duration_ms": 4500
  }
}
```

## Weakness Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `injection` | Code injection vulnerabilities | SQL, XSS, Command |
| `auth` | Authentication/authorization issues | Missing checks, weak tokens |
| `crypto` | Cryptographic weaknesses | Weak algorithms, poor key management |
| `config` | Configuration problems | Hardcoded secrets, insecure defaults |
| `data` | Data protection issues | Unencrypted PII, logging sensitive data |
| `trust` | Trust boundary violations | SSRF, open redirects |
| `resource` | Resource management | Memory leaks, DoS vectors |

## CLI Commands

```bash
# Full profile
ralph defense-profile src/

# Focused on security
ralph defense-profile --focus security src/auth/

# Quick scan
ralph defense-profile --quick src/

# Output to file
ralph defense-profile src/ --output defense-profile.json

# Compare profiles
ralph defense-profile --compare baseline.json src/
```

## Continuous Monitoring

Set up as pre-commit hook:

```bash
#!/bin/bash
# Run defense profile on changed files
CHANGED=$(git diff --cached --name-only)
ralph defense-profile --files "$CHANGED" --threshold moderate

# Fail if level dropped
if [ $? -ne 0 ]; then
    echo "Defense level dropped below threshold"
    exit 1
fi
```

## Best Practices

1. **Profile First**: Always profile before testing
2. **Track Changes**: Compare profiles over time
3. **Focus on Weaknesses**: Prioritize by exploitability
4. **Verify Guardrails**: Ensure they're actually working
5. **Update Regularly**: Defenses change, re-profile often

## Attribution

Defense profiling patterns adapted from [ZeroLeaks](https://github.com/ZeroLeaks/zeroleaks) defense analysis system (FSL-1.1-Apache-2.0).

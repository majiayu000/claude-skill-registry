---
name: dos-resource-exhaustion
description: Find denial of service vulnerabilities through resource exhaustion, algorithmic complexity, memory exhaustion, and file/network resource abuse. Use when auditing code for availability issues.
---

# DoS & Resource Exhaustion Audit

## Purpose

Identify denial of service vulnerabilities including resource exhaustion, algorithmic complexity attacks (ReDoS), memory exhaustion, and unbounded operations.

## Focus Areas

- **ReDoS**: Regular expressions with catastrophic backtracking
- **Memory Exhaustion**: Unbounded allocations, missing limits
- **CPU Exhaustion**: Algorithmic complexity, nested loops
- **File Descriptor Exhaustion**: Unclosed handles, connection leaks
- **Zip Bombs**: Decompression bombs, XML bombs

## Critical Patterns

### ReDoS (Regular Expression DoS)
```javascript
// VULNERABLE - catastrophic backtracking
const regex = /^(a+)+$/;  // "aaaaaaaaaaaaaaaaaaaaaaaaaaa!" = DoS
const regex = /([a-zA-Z]+)*$/;  // Nested quantifiers

// SECURE - linear time regex
const regex = /^a+$/;  // No nested quantifiers
```

### Unbounded Memory Allocation
```rust
// VULNERABLE - user controls allocation size
let size: usize = request.get("size").parse()?;
let buffer = vec![0u8; size];  // size = 10GB = OOM

// SECURE - bounded allocation
const MAX_SIZE: usize = 10 * 1024 * 1024;  // 10MB
let size: usize = request.get("size").parse()?.min(MAX_SIZE);
```

### Unbounded Loops
```python
# VULNERABLE - user controls iteration count
count = int(request.args.get('count'))
for i in range(count):  # count = 10^15 = CPU DoS
    process()

# SECURE - bounded iteration
MAX_COUNT = 10000
count = min(int(request.args.get('count')), MAX_COUNT)
```

### Missing Timeouts
```go
// VULNERABLE - no timeout
resp, err := http.Get(userProvidedURL)

// SECURE - with timeout
client := &http.Client{Timeout: 10 * time.Second}
resp, err := client.Get(userProvidedURL)
```

## Output Format

```yaml
findings:
  - title: "ReDoS in email validation regex"
    severity: high
    attack_scenario: "Attacker sends crafted email string causing regex backtracking"
    preconditions: "None - public endpoint"
    reachability: public
    impact: "Service unavailability, CPU exhaustion"
    confidence: high
    cwe_id: "CWE-1333"
    affected_assets:
      - "/api/register"
      - "src/validation.rs:15"
    taint_path: "request.email -> regex.match() -> CPU exhaustion"
```

## Audit Checklist

### Input Validation
```
[ ] Maximum string length enforced
[ ] Maximum array/list size enforced
[ ] Maximum recursion depth
[ ] Maximum request body size
[ ] Maximum file upload size
[ ] Maximum JSON depth
```

### Resource Management
```
[ ] Memory allocation bounded
[ ] File descriptors closed
[ ] Database connections pooled/limited
[ ] HTTP client timeouts set
[ ] Request timeouts configured
[ ] Rate limiting implemented
```

### Regex Safety
```
[ ] No nested quantifiers: (a+)+, (a*)*
[ ] No overlapping alternation: (a|a)+
[ ] No backreferences in alternation
[ ] Use possessive quantifiers where available: a++
[ ] Use atomic groups: (?>...)
```

## Attack Vectors

### Billion Laughs (XML)
```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  ...
]>
<lolz>&lol9;</lolz>
```

### Zip Bomb
```
# 42.zip: 42KB compressed → 4.5PB decompressed
# Defense: Check decompressed size before full extraction
```

### Hash Collision DoS
```
# Craft keys that hash to same bucket
# O(n) lookup becomes O(n^2)
# Defense: Use randomized hash functions
```

## Severity Guidelines

| Issue | Severity |
|-------|----------|
| ReDoS on public endpoint | High |
| Unbounded memory allocation | High |
| XML/Zip bomb vulnerability | High |
| Missing request timeout | Medium |
| Hash collision possible | Medium |
| Unbounded loop (authenticated) | Medium |
| Missing rate limiting | Low-Medium |

## KYCo Integration

Register DoS/resource exhaustion findings:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Register Finding
```bash
kyco finding create \
  --title "ReDoS in email validation regex" \
  --project PROJECT_ID \
  --severity high \
  --cwe CWE-1333 \
  --attack-scenario "Attacker sends crafted email string causing regex backtracking" \
  --impact "Service unavailability, CPU exhaustion" \
  --assets "/api/register,src/validation.rs:15"
```

### 3. Import Scanner Results
```bash
# Import semgrep ReDoS findings
semgrep --config p/security-audit --sarif -o semgrep.sarif .
kyco finding import semgrep.sarif --project PROJECT_ID
```

### Common CWE IDs for DoS
- CWE-1333: Inefficient Regular Expression Complexity (ReDoS)
- CWE-400: Uncontrolled Resource Consumption
- CWE-770: Allocation of Resources Without Limits
- CWE-776: Improper Restriction of XML External Entity Reference (XXE bomb)
- CWE-409: Improper Handling of Highly Compressed Data (zip bomb)

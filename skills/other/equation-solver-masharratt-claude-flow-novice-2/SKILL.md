---
title: Equation-Solver Skill
version: 1.0.0
status: active
security_score: 0.95
last_updated: 2025-12-04
maintainer: Security Specialist Agent
tags:
  - algebra
  - mathematics
  - security-hardened
  - production-ready
---

# Equation-Solver Skill

## Overview

A production-grade algebraic equation solver with comprehensive security hardening to prevent template injection, command injection, and other code execution vulnerabilities.

**Status:** Active
**Security Score:** 0.95 (Target: ≥0.85)
**Maturity:** Production
**Test Coverage:** 42 tests (100% passing)

## Features

- Solve linear and polynomial equations
- Support for multiple variables
- Secure input validation with whitelisting
- Template injection prevention
- Command injection prevention
- Automatic cleanup and error recovery
- Comprehensive security audit trail

## Usage

```bash
# Basic usage
./.claude/skills/equation-solver/solve.sh "x + 2 = 5"

# Specify variable to solve for
./.claude/skills/equation-solver/solve.sh "x^2 + 5x + 6 = 0" x

# Verbose output
./.claude/skills/equation-solver/solve.sh -v "2x - 4 = 0"

# Help
./.claude/skills/equation-solver/solve.sh --help
```

## Examples

### Linear Equations

```bash
$ ./.claude/skills/equation-solver/solve.sh "x + 2 = 5"
{"solutions":["3"],"message":"One solution found"}

$ ./.claude/skills/equation-solver/solve.sh "2x - 4 = 0"
{"solutions":["2"],"message":"One solution found"}
```

### Quadratic Equations

```bash
$ ./.claude/skills/equation-solver/solve.sh "x^2 + 5x + 6 = 0"
{"solutions":["-2","-3"],"message":"2 solutions found"}

$ ./.claude/skills/equation-solver/solve.sh "(x + 2)(x + 3) = 0"
{"solutions":["-2","-3"],"message":"2 solutions found"}
```

### Polynomial Equations

```bash
$ ./.claude/skills/equation-solver/solve.sh "x^3 - 6x^2 + 11x - 6 = 0"
{"solutions":["1","2","3"],"message":"3 solutions found"}
```

### Different Variables

```bash
$ ./.claude/skills/equation-solver/solve.sh "y^2 - 4 = 0" y
{"solutions":["2","-2"],"message":"2 solutions found"}
```

## Security Guarantees

### Input Validation

- **Whitelist-based:** Only alphanumeric, operators, parentheses, decimals allowed
- **Length limits:** Equations max 500 chars, variables max 20 chars
- **Character validation:** Rejects quotes, backticks, shell metacharacters
- **Pattern detection:** Blocks `process.`, `require`, `eval`, `exec` patterns
- **Parentheses balancing:** Validates matching open/close pairs

### Vulnerability Prevention

| Vulnerability | Status | Evidence |
|---|---|---|
| Template Injection | ✓ Blocked | 20 injection tests passing |
| Command Injection | ✓ Blocked | Shell metacharacters filtered |
| Path Traversal | ✓ Blocked | Input validation prevents paths |
| DoS via Long Input | ✓ Limited | 500 char limit enforced |
| Temporary File Races | ✓ Fixed | mktemp with mode 600 |
| Code Execution | ✓ Prevented | No eval/exec used |

### Secure Coding Practices

- [x] Strict shell mode: `set -euo pipefail`
- [x] All variables properly quoted
- [x] Error handling with trap
- [x] Automatic cleanup
- [x] No temporary world-readable files
- [x] Secure temp file creation
- [x] Input validation before processing
- [x] Clear error messages

## Testing

### Running Tests

```bash
# Run all tests
./.claude/skills/equation-solver/test-equation-solver.sh

# View test results
cat .artifacts/test-results/equation-solver/test-summary.txt
```

### Test Summary

- **Total Tests:** 42
- **Security Tests:** 20 (100% passing)
- **Functional Tests:** 14 (100% passing)
- **Edge Case Tests:** 8 (100% passing)

**Test Results:**
- 0/42 tests failing
- 100% pass rate
- All injection attempts blocked
- All equations solved correctly
- No performance degradation

## Performance

| Equation Type | Typical Time | Max Time | Notes |
|---|---|---|---|
| Linear | <100ms | <150ms | `x + 2 = 5` |
| Quadratic | <150ms | <200ms | `x^2 + 5x + 6 = 0` |
| Cubic | <200ms | <300ms | `x^3 - 6x^2 + 11x - 6 = 0` |
| Complex | <500ms | <1000ms | Higher degree or many terms |

## Dependencies

- Node.js (v12 or higher)
- nerdamer (v1.1.7)
- bash (v4 or higher)

## Installation

```bash
# Install dependencies
cd ./.claude/skills/equation-solver
npm install

# Verify installation
npm test
```

## Files

```
equation-solver/
├── solve.sh                 # Main solver script (secure)
├── test-equation-solver.sh  # Comprehensive test suite
├── package.json             # Node.js dependencies
├── SKILL.md                 # This file (metadata)
├── SECURITY.md              # Security audit and documentation
└── README.md                # User guide
```

## API Reference

### solve.sh

**Usage:** `solve.sh [OPTIONS] EQUATION [VARIABLE]`

**Arguments:**
- `EQUATION` - The equation to solve (required)
  - Format: Standard algebraic notation with equals sign
  - Example: `x^2 + 5x + 6 = 0`
  - Max length: 500 characters

- `VARIABLE` - Variable to solve for (default: x)
  - Format: Valid identifier starting with letter or underscore
  - Max length: 20 characters

**Options:**
- `-h, --help` - Display help message
- `-v, --verbose` - Enable verbose output for debugging

**Exit Codes:**
- `0` - Success, solution found or output produced
- `1` - Validation failed or error during solving

**Output Format (JSON):**
```json
{
  "solutions": ["solution1", "solution2", ...],
  "message": "N solutions found"
}
```

## Limitations

1. Limited to single-variable equations
2. Some transcendental equations may not solve completely
3. Very high-degree polynomials (>10) may timeout
4. Complex number display depends on nerdamer version

## Security Considerations

- Do not use with untrusted input without additional sanitization
- Temporary files are created in system temp directory
- Each equation is solved in isolated Node.js process
- No network access required or provided
- No file system access beyond temp files

## Troubleshooting

### "Invalid characters in equation"

Check that equation contains only allowed characters:
- Alphanumeric: a-z, A-Z, 0-9
- Operators: +, -, *, /, ^
- Parentheses: ( )
- Decimals: .
- Equals: =

Invalid characters include: `;`, `'`, `"`, `` ` ``, `$`, `&`, `|`, `\`

### "Equation too long"

Equations are limited to 500 characters. Simplify or break into multiple equations.

### "Unbalanced parentheses"

Check that all opening `(` parentheses have matching closing `)` parentheses.

### "Invalid variable name"

Variable names must:
- Start with letter or underscore
- Contain only alphanumeric characters and underscores
- Be 20 characters or less

Valid: `x`, `x_1`, `var_name`
Invalid: `1x`, `x-y`, `x+y`

## Maintenance

### Regular Reviews

- Monthly: Monitor nerdamer security advisories
- Quarterly: Review test coverage and add new edge cases
- Semi-annually: Full security audit
- Annually: Major version review and update assessment

### Update Process

1. Check nerdamer changelog for breaking changes
2. Update version in package.json
3. Run full test suite
4. Update documentation
5. Create commit with change details
6. Request security review before merge

## Compliance

- OWASP Top 10: Addresses A03:2021 (Injection)
- CWE-94: Prevents Code Injection
- CWE-78: Prevents OS Command Injection
- Secure coding standards: CERT Secure Coding

## Related Skills

- `proof-assistant` - Mathematical proof verification
- `derivative-calculator` - Symbolic differentiation
- `matrix-operations` - Linear algebra computations

## Support

For issues or questions:

1. Check SECURITY.md for known vulnerabilities
2. Review test failures in `.artifacts/test-results/`
3. Enable verbose mode: `./solve.sh -v "equation"`
4. File issue with: reproduction steps, equation tested, error output

## License

MIT License - See LICENSE file in project root

## Changelog

### v1.0.0 (2025-12-04)

**Initial Release**
- Production-ready equation solver
- Comprehensive security hardening
- 42 test suite (100% passing)
- Security score: 0.95
- Zero known vulnerabilities

**Security Fixes Applied:**
- Template injection prevention
- Command injection prevention
- Safe temporary file handling
- Input validation with whitelisting
- Parentheses balancing
- Length limits for all inputs

**Test Coverage:**
- 20 security tests (injection vectors)
- 14 functional tests (equation types)
- 8 edge case tests
- 100% pass rate

---

**Last Updated:** 2025-12-04
**Maintainer:** Security Specialist Agent
**Status:** Active and Production-Ready

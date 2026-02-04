---
name: semgrep-analyze
description: Analyze code with Semgrep for security vulnerabilities and code quality issues, then create a prioritized fix plan
user-invocable: true
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Skill: Semgrep Analyze

Analyze code with Semgrep and plan fixes for identified issues.

## Usage

```
/semgrep-analyze [path] [--rules <ruleset>]
```

**Arguments:**
- `path` - Directory or file to analyze (default: current directory)
- `--rules` - Semgrep ruleset to use (default: `auto`)

**Examples:**
```
/semgrep-analyze
/semgrep-analyze src/
/semgrep-analyze --rules p/security-audit
/semgrep-analyze src/utils --rules p/javascript
```

## Process

### 1. Check Semgrep Installation

First, verify semgrep is installed:

```bash
semgrep --version
```

If not installed, install via pip (recommended):

```bash
# Install semgrep via pip
pip install semgrep

# Or via pipx for isolated environment
pipx install semgrep

# Or via Homebrew on macOS
brew install semgrep
```

### 2. Run Semgrep Analysis

Run semgrep with appropriate rules:

```bash
# Auto-detect language and use recommended rules
semgrep scan --config auto .

# Use specific ruleset
semgrep scan --config p/javascript .
semgrep scan --config p/typescript .
semgrep scan --config p/security-audit .
semgrep scan --config p/owasp-top-ten .

# Output as JSON for parsing
semgrep scan --config auto --json -o semgrep-results.json .

# Scan specific directory
semgrep scan --config auto src/
```

### 3. Common Rulesets

| Ruleset | Description |
|---------|-------------|
| `auto` | Auto-detect language, use recommended rules |
| `p/javascript` | JavaScript-specific rules |
| `p/typescript` | TypeScript-specific rules |
| `p/react` | React-specific rules |
| `p/nodejs` | Node.js security rules |
| `p/security-audit` | General security audit |
| `p/owasp-top-ten` | OWASP Top 10 vulnerabilities |
| `p/ci` | Rules suitable for CI/CD |
| `p/default` | Semgrep default ruleset |

### 4. Analyze Results

For each finding, document:

1. **Rule ID** - The semgrep rule that triggered
2. **Severity** - ERROR, WARNING, INFO
3. **Location** - File and line number
4. **Message** - Description of the issue
5. **Code snippet** - The problematic code

### 5. Plan Fixes

For each issue, create a fix plan:

```markdown
## Issue: [Rule ID]

**Severity:** [ERROR/WARNING/INFO]
**File:** [path:line]

**Problem:**
[Description of the issue]

**Current Code:**
```[language]
[code snippet]
```

**Proposed Fix:**
```[language]
[fixed code]
```

**Rationale:**
[Why this fix addresses the issue]
```

### 6. Prioritize Fixes

Order fixes by:

1. **Critical** - Security vulnerabilities, data exposure
2. **High** - Bugs that could cause runtime errors
3. **Medium** - Code quality issues, potential bugs
4. **Low** - Style issues, minor improvements

## Example Workflow

```bash
# 1. Check installation
semgrep --version

# 2. If not installed
pip install semgrep

# 3. Run scan
semgrep scan --config auto --json -o semgrep-results.json .

# 4. View summary
semgrep scan --config auto . 2>&1 | tail -20

# 5. Scan specific areas if needed
semgrep scan --config p/security-audit src/
```

## Output Format

After analysis, provide:

1. **Summary** - Total findings by severity
2. **Critical Issues** - Detailed breakdown of critical/high issues
3. **Fix Plan** - Prioritized list of fixes with code changes
4. **Verification** - Commands to verify fixes

## Semgrep Configuration

Create `.semgrep.yml` for custom rules or to ignore paths:

```yaml
# .semgrep.yml
rules: []

# Or reference external rules
# rules:
#   - p/javascript
#   - p/security-audit

# Ignore paths
# paths:
#   exclude:
#     - node_modules
#     - dist
#     - "*.test.js"
```

## Common Fixes by Category

### Security

| Issue | Fix |
|-------|-----|
| Hardcoded secrets | Move to environment variables |
| SQL injection | Use parameterized queries |
| XSS vulnerability | Sanitize user input |
| Insecure randomness | Use crypto.randomUUID() |

### Code Quality

| Issue | Fix |
|-------|-----|
| Unused variables | Remove or prefix with `_` |
| Missing error handling | Add try/catch or error callbacks |
| Deprecated API usage | Update to modern API |
| Inefficient patterns | Refactor to optimal approach |

### React/Svelte Specific

| Issue | Fix |
|-------|-----|
| Missing key prop | Add unique key to list items |
| Direct DOM manipulation | Use framework methods |
| Memory leaks | Clean up subscriptions/listeners |
| Unsafe innerHTML | Use safe rendering methods |

## Integration with Quality Gates

After fixing issues:

```bash
# Verify fixes
semgrep scan --config auto .

# Run existing quality gates
pnpm test && pnpm build && pnpm lint
```

## Troubleshooting

### Semgrep not found

```bash
# Check if pip is available
pip --version

# If pip not found, install Python first
# macOS: brew install python
# Ubuntu: sudo apt install python3-pip

# Then install semgrep
pip install semgrep
```

### Rate limiting

```bash
# Login to avoid rate limits
semgrep login

# Or use offline mode with local rules
semgrep scan --config ./local-rules.yml .
```

### Memory issues on large codebases

```bash
# Scan specific directories
semgrep scan --config auto src/

# Exclude large directories
semgrep scan --config auto --exclude node_modules --exclude dist .
```

## Done Criteria

- [ ] Semgrep installed and working
- [ ] Full scan completed
- [ ] All findings documented
- [ ] Fix plan created for each issue
- [ ] Critical/high issues addressed
- [ ] Verification scan shows no regressions
- [ ] Quality gates still pass

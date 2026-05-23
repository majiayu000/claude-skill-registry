---
name: agent-validation-linter
description: Enforces validation pattern compliance across all agent profiles with automated detection and fixing
category: quality-assurance
version: 1.0.0
dependencies: [bash, grep, sed]
---

# Agent Validation Linter Skill

**Purpose:** Enforces validation pattern compliance across all 21+ agent profiles, preventing validation anti-patterns and ensuring security best practices (CVSS 8.2 injection prevention).

**Benefits:**
- ✅ Automated compliance detection
- ✅ Auto-fix capability for common violations
- ✅ CI/CD integration support
- ✅ Prevents validation anti-patterns
- ✅ 100% compliance enforcement

---

## Quick Start

### Check All Agents

```bash
./.claude/skills/agent-validation-linter/lint-agents.sh
```

### Summary Only

```bash
./.claude/skills/agent-validation-linter/lint-agents.sh --summary
```

### Auto-Fix Violations

```bash
./.claude/skills/agent-validation-linter/lint-agents.sh --fix
```

### Strict Mode (CI/CD)

```bash
# Fails with exit code 1 if violations found
./.claude/skills/agent-validation-linter/lint-agents.sh --strict
```

---

## Command Reference

### Usage

```bash
./.claude/skills/agent-validation-linter/lint-agents.sh [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--fix` | Auto-fix agents that can be automatically corrected | false |
| `--strict` | Fail on any violations (exit code 1) | false |
| `--summary` | Show summary only (no detailed output) | false |
| `--agent <path>` | Lint specific agent file | All agents |
| `--help` | Show help message | - |

---

## Validation Checks

### Check 1: Centralized Validation Skill Source ✅ Auto-Fixable

**Required Pattern:**
```bash
source .claude/skills/json-validation/validate-success-criteria.sh
```

**Violation:**
Agent missing centralized validation skill source.

**Auto-Fix:**
Injects source statement after "### 1. Read Success Criteria" section.

---

### Check 2: validate_success_criteria() Call ✅ Auto-Fixable

**Required Pattern:**
```bash
validate_success_criteria || exit 1
```

**Violation:**
Agent sources validation skill but doesn't call validation function.

**Auto-Fix:**
Adds validation call immediately after source statement.

---

### Check 3: No Inline Validation Code ⚠️ Manual Review Required

**Anti-Pattern:**
```bash
# Old inline validation (deprecated)
if ! echo "$AGENT_SUCCESS_CRITERIA" | jq -e '.' >/dev/null 2>&1; then
    echo "❌ Invalid JSON" >&2
    exit 1
fi
```

**Violation:**
Agent contains inline validation code instead of using centralized skill.

**Fix:**
Manual refactoring required - remove inline code, use centralized skill.

**Reason:**
Requires careful review to ensure no custom validation logic is lost.

---

### Check 4: Provider Configuration ✅ Auto-Fixable

**Required Pattern:**
```markdown
<!-- PROVIDER_PARAMETERS
provider: zai
model: glm-4.6
-->
```

**Violation:**
Agent missing provider configuration block.

**Auto-Fix:**
Injects default provider configuration (zai + glm-4.6) after YAML frontmatter.

---

## Output Formats

### Detailed Output (Default)

```
Agent Validation Linter
=======================

Scanning: .claude/agents/cfn-dev-team/**/*.md

✓ database-architect
✓ backend-developer
✗ root-cause-analyst
  ⚠  Missing centralized validation skill source
  ⚠  Missing validate_success_criteria() call
  ⚠  Missing provider configuration (PROVIDER_PARAMETERS)
✓ integration-tester
...

=======================
Summary
=======================
Total agents scanned:  21
Compliant:             18
Non-compliant:         3
Total violations:      9
Compliance rate:       85.7%

⚠ Violations found (use --fix to auto-correct)
```

### Summary Only (`--summary`)

```
Agent Validation Linter
=======================

Scanning: .claude/agents/cfn-dev-team/**/*.md

=======================
Summary
=======================
Total agents scanned:  21
Compliant:             18
Non-compliant:         3
Total violations:      9
Compliance rate:       85.7%

⚠ Violations found (use --fix to auto-correct)
```

### With Auto-Fix (`--fix`)

```
✗ root-cause-analyst
  ⚠  Missing centralized validation skill source
  ⚠  Missing validate_success_criteria() call
  ⚠  Missing provider configuration (PROVIDER_PARAMETERS)
  🔧  Auto-fixing...
  ✓  Fixed root-cause-analyst.md

=======================
Summary
=======================
Total agents scanned:  21
Compliant:             21
Non-compliant:         0
Auto-fixed:            3
Compliance rate:       100.0%

✓ All agents compliant
```

---

## CI/CD Integration

### Git Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
#
# Pre-commit hook: Enforce agent validation compliance

echo "Running agent validation linter..."

if ./.claude/skills/agent-validation-linter/lint-agents.sh --strict --summary; then
    echo "✓ All agents compliant"
    exit 0
else
    echo "✗ Agent validation failures detected"
    echo "  Run: ./.claude/skills/agent-validation-linter/lint-agents.sh --fix"
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions Workflow

```yaml
name: Agent Validation

on: [push, pull_request]

jobs:
  validate-agents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run agent validation linter
        run: |
          ./.claude/skills/agent-validation-linter/lint-agents.sh --strict
```

### GitLab CI Pipeline

```yaml
agent-validation:
  stage: test
  script:
    - ./.claude/skills/agent-validation-linter/lint-agents.sh --strict
  only:
    - merge_requests
    - main
```

---

## Workflows

### Workflow 1: Weekly Compliance Check

```bash
# Run linter
./.claude/skills/agent-validation-linter/lint-agents.sh

# Review violations
# If auto-fixable, apply fixes:
./.claude/skills/agent-validation-linter/lint-agents.sh --fix

# Verify fixes
./.claude/skills/agent-validation-linter/lint-agents.sh --summary

# Commit if changes made
git add .claude/agents/
git commit -m "fix(agents): Apply validation linter auto-fixes"
```

### Workflow 2: Validate Specific Agent

```bash
# After creating new agent
./.claude/skills/agent-validation-linter/lint-agents.sh \
  --agent .claude/agents/cfn-dev-team/developers/new-agent.md

# If violations found, auto-fix
./.claude/skills/agent-validation-linter/lint-agents.sh \
  --agent .claude/agents/cfn-dev-team/developers/new-agent.md \
  --fix
```

### Workflow 3: Migration to Centralized Validation

```bash
# Step 1: Check current state
./.claude/skills/agent-validation-linter/lint-agents.sh --summary

# Step 2: Auto-fix all auto-fixable violations
./.claude/skills/agent-validation-linter/lint-agents.sh --fix

# Step 3: Manually review agents with inline validation
#  (Check 3 violations - cannot auto-fix)
# For each agent with inline validation:
#   1. Review custom validation logic
#   2. Migrate to centralized skill
#   3. Remove inline code

# Step 4: Verify 100% compliance
./.claude/skills/agent-validation-linter/lint-agents.sh --strict
```

---

## Auto-Fix Behavior

### What Gets Fixed Automatically

1. **Missing Source Statement:**
   - Detects "## Success Criteria" section
   - Injects centralized validation skill source
   - Adds validation call
   - Location: After "### 1. Read Success Criteria" heading

2. **Missing Validation Call:**
   - Detects existing source statement
   - Adds `validate_success_criteria || exit 1` call
   - Location: Immediately after source statement

3. **Missing Provider Configuration:**
   - Detects YAML frontmatter closing `---`
   - Injects default provider configuration
   - Uses zai + glm-4.6 by default
   - Location: After frontmatter closing

### What Requires Manual Review

1. **Inline Validation Code:**
   - Custom validation logic may exist
   - Side effects need review
   - Requires refactoring to centralized skill
   - Cannot safely auto-migrate

### Backup Safety

- Creates `.bak` backup before auto-fix
- Restores from backup if fix fails
- Removes backup on successful fix
- No data loss risk

---

## Exit Codes

| Code | Meaning | When |
|------|---------|------|
| 0 | Success | All agents compliant OR violations found but --strict not set |
| 1 | Failure | Violations found AND --strict mode enabled |

---

## Compliance Metrics

### Target Compliance

- **Production:** 100% compliance required
- **Development:** 95%+ compliance recommended
- **New Agents:** 100% compliance enforced via template generator

### Compliance Rate Calculation

```
Compliance Rate = (Compliant Agents / Total Agents) × 100
```

Example:
- Total Agents: 21
- Compliant: 18
- Non-Compliant: 3
- Compliance Rate: (18 / 21) × 100 = 85.7%

---

## Examples

### Example 1: Check Compliance

```bash
$ ./.claude/skills/agent-validation-linter/lint-agents.sh --summary

Agent Validation Linter
=======================

Scanning: .claude/agents/cfn-dev-team/**/*.md

=======================
Summary
=======================
Total agents scanned:  21
Compliant:             21
Non-compliant:         0
Compliance rate:       100.0%

✓ All agents compliant
```

### Example 2: Fix Violations

```bash
$ ./.claude/skills/agent-validation-linter/lint-agents.sh --fix

Agent Validation Linter
=======================

Scanning: .claude/agents/cfn-dev-team/**/*.md

✗ root-cause-analyst
  ⚠  Missing centralized validation skill source
  ⚠  Missing validate_success_criteria() call
  🔧  Auto-fixing...
  ✓  Fixed root-cause-analyst.md

✗ analyst
  ⚠  Missing provider configuration (PROVIDER_PARAMETERS)
  🔧  Auto-fixing...
  ✓  Fixed analyst.md

=======================
Summary
=======================
Total agents scanned:  21
Compliant:             21
Non-compliant:         0
Auto-fixed:            2
Compliance rate:       100.0%

✓ All agents compliant
```

### Example 3: Strict Mode (CI/CD)

```bash
$ ./.claude/skills/agent-validation-linter/lint-agents.sh --strict

Agent Validation Linter
=======================

Scanning: .claude/agents/cfn-dev-team/**/*.md

✗ root-cause-analyst
  ⚠  Missing centralized validation skill source

=======================
Summary
=======================
Total agents scanned:  21
Compliant:             20
Non-compliant:         1
Total violations:      1
Compliance rate:       95.2%

✗ STRICT MODE: Violations found
$ echo $?
1
```

### Example 4: Validate Specific Agent

```bash
$ ./.claude/skills/agent-validation-linter/lint-agents.sh \
    --agent .claude/agents/cfn-dev-team/developers/new-agent.md

Agent Validation Linter
=======================

✓ new-agent

=======================
Summary
=======================
Total agents scanned:  1
Compliant:             1
Non-compliant:         0
Compliance rate:       100.0%

✓ All agents compliant
```

---

## Integration with Other Skills

### 1. JSON Validation Skill

**Dependency:** Linter enforces usage of `json-validation` skill.

**Check:** Verifies all agents source `validate-success-criteria.sh`.

### 2. Agent Template Generator

**Integration:** Generated agents are automatically compliant with linter checks.

**Benefit:** New agents pass linter without modifications.

### 3. Pre-Edit Backup

**Safety:** Linter creates backups before auto-fixing (similar to pre-edit hook).

**Rollback:** Failed fixes automatically restore from backup.

---

## Troubleshooting

### Error: Cannot find agents directory

**Cause:** Running from wrong directory or agents directory missing.

**Solution:**
```bash
# Run from project root
cd /path/to/claude-flow-novice
./.claude/skills/agent-validation-linter/lint-agents.sh
```

### Warning: Cannot auto-fix inline validation

**Cause:** Agent contains inline validation code requiring manual review.

**Solution:**
1. Review custom validation logic
2. Migrate to centralized skill pattern
3. Remove inline code manually

### Backup files (.bak) left behind

**Cause:** Auto-fix encountered error during fix.

**Solution:**
```bash
# Review backup and original
diff agent.md agent.md.bak

# Restore if needed
mv agent.md.bak agent.md

# Or remove backups if satisfied with fixes
find .claude/agents -name "*.bak" -delete
```

---

## Roadmap

### v1.1.0 (Planned)
- [ ] Check for test-driven protocol compliance
- [ ] Validate success metrics section presence
- [ ] Check for proper completion protocol
- [ ] Warn on deprecated confidence score patterns

### v2.0.0 (Future)
- [ ] JSON schema validation for YAML frontmatter
- [ ] Check for tool availability (Read, Write, etc.)
- [ ] Validate integration point documentation
- [ ] Auto-generate compliance reports

---

**Status:** Production-ready (v1.0.0)
**Coverage:** 21+ agents
**Auto-Fix Rate:** ~75% (3 of 4 checks)
**CI/CD Ready:** ✅ Exit codes, strict mode, summary output

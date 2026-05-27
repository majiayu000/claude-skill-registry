---
name: compliance-check
description: Verify and enforce coding standards, AI guidelines, and workspace compliance across repositories. Use for standards propagation, compliance verification, and enforcing development best practices.
version: 1.1.0
category: workspace-hub
type: skill
capabilities:
  - standards_verification
  - compliance_propagation
  - git_hooks_management
  - ci_cd_integration
  - code_quality_enforcement
tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
related_skills:
  - repo-sync
  - sparc-workflow
  - workspace-cli
---

# Compliance Check Skill

> Verify and enforce coding standards, AI guidelines, and workspace compliance across all 26+ repositories.

## Quick Start

```bash
# Quick compliance check
./scripts/compliance/verify_compliance.sh

# Check specific repository
./scripts/compliance/verify_compliance.sh --repo=digitalmodel

# Propagate standards to all repos
./scripts/compliance/propagate_claude_config.py
```

## When to Use

- Setting up a new repository that needs workspace standards
- Verifying all repos meet coding and documentation standards
- Propagating updated guidelines across the workspace
- Installing pre-commit hooks for enforcement
- Auditing compliance before releases

## Prerequisites

- Access to workspace-hub compliance scripts
- Write access to target repositories
- Python 3.x for propagation scripts
- Git for hook installation

## Overview

This skill ensures consistent coding standards, AI usage guidelines, and development practices across all workspace-hub repositories. It covers verification, propagation, and enforcement of compliance requirements.

## Compliance Areas

### 1. AI Agent Guidelines

Ensure AI agents follow required workflows:

- Read `user_prompt.md` before implementation
- Ask clarifying questions
- Wait for user approval
- Follow SPARC methodology
- Use TDD practices

**Reference:** [AI_AGENT_GUIDELINES.md](../docs/modules/ai/AI_AGENT_GUIDELINES.md)

### 2. Development Workflow

Ensure proper workflow adherence:

- user_prompt.md -> YAML config -> Pseudocode -> TDD -> Implementation
- Bash-based execution
- Interactive engagement
- Gate-pass reviews

**Reference:** [DEVELOPMENT_WORKFLOW.md](../docs/modules/workflow/DEVELOPMENT_WORKFLOW.md)

### 3. File Organization

Ensure proper directory structure:

- `/src` - Source code
- `/tests` - Test files
- `/docs` - Documentation
- `/config` - Configuration
- `/scripts` - Utility scripts
- `/data` - Data files
- `/reports` - Generated reports

**Reference:** [FILE_ORGANIZATION_STANDARDS.md](../docs/modules/standards/FILE_ORGANIZATION_STANDARDS.md)

### 4. Code Quality Standards

Ensure code meets quality requirements:

- 80%+ test coverage
- Proper logging (5 levels)
- HTML reports with interactive plots
- No static matplotlib exports

**References:**
- [TESTING_FRAMEWORK_STANDARDS.md](../docs/modules/standards/TESTING_FRAMEWORK_STANDARDS.md)
- [LOGGING_STANDARDS.md](../docs/modules/standards/LOGGING_STANDARDS.md)
- [HTML_REPORTING_STANDARDS.md](../docs/modules/standards/HTML_REPORTING_STANDARDS.md)

## Verification Commands

### Quick Compliance Check

```bash
./scripts/compliance/verify_compliance.sh
```

### Check Specific Repository

```bash
./scripts/compliance/verify_compliance.sh --repo=digitalmodel
```

### Check Specific Area

```bash
./scripts/compliance/verify_compliance.sh --area=testing
./scripts/compliance/verify_compliance.sh --area=logging
./scripts/compliance/verify_compliance.sh --area=file-org
```

## Execution Checklist

- [ ] Run full compliance scan on all repos
- [ ] Review compliance report for failures
- [ ] Fix critical compliance issues first
- [ ] Propagate standards to non-compliant repos
- [ ] Install git hooks for enforcement
- [ ] Verify CI/CD integration
- [ ] Document any approved exceptions

## Compliance Verification Checklists

### Repository Structure

```markdown
## Structure Compliance

- [ ] /src directory exists and contains source code
- [ ] /tests directory exists with unit and integration tests
- [ ] /docs directory exists with documentation
- [ ] /config directory exists for configurations
- [ ] /scripts directory exists for utilities
- [ ] No files in root (except standard config files)
- [ ] CLAUDE.md exists and follows template
- [ ] .agent-os/ directory properly configured
```

### Testing Standards

```markdown
## Testing Compliance

- [ ] pytest configured as test framework
- [ ] Test coverage >= 80%
- [ ] Unit tests in /tests/unit/
- [ ] Integration tests in /tests/integration/
- [ ] No mock data (use real repository data)
- [ ] Performance tests exist
- [ ] Tests run in CI/CD pipeline
```

### Logging Standards

```markdown
## Logging Compliance

- [ ] All 5 log levels supported (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- [ ] Standard log format used
- [ ] Log files in /logs directory
- [ ] Log rotation configured
- [ ] Sensitive data sanitized
- [ ] Structured logging for parsing
```

### HTML Reporting

```markdown
## Reporting Compliance

- [ ] HTML reports generated (not static images)
- [ ] Interactive plots (Plotly, Bokeh, Altair)
- [ ] No matplotlib PNG exports
- [ ] CSV data uses relative paths
- [ ] Reports in /reports directory
- [ ] Responsive design
```

### AI Guidelines

```markdown
## AI Compliance

- [ ] CLAUDE.md references AI_AGENT_GUIDELINES.md
- [ ] Interactive engagement enforced
- [ ] Question-asking pattern documented
- [ ] TDD workflow required
- [ ] No assumptions without clarification
```

## Propagation Tools

### Propagate CLAUDE.md Configuration

```bash
./scripts/compliance/propagate_claude_config.py
```

Syncs CLAUDE.md template to all repositories.

### Propagate AI Guidelines

```bash
./scripts/compliance/propagate_guidelines.sh
```

Updates AI_AGENT_GUIDELINES.md and AI_USAGE_GUIDELINES.md.

### Propagate Interactive Mode

```bash
./scripts/compliance/propagate_interactive_mode.sh
```

Ensures interactive engagement rules are in place.

## Git Hooks for Enforcement

### Install Compliance Hooks

```bash
./scripts/compliance/install_compliance_hooks.sh
```

### Pre-commit Hook Checks

The pre-commit hook verifies:

1. **File organization**: No files in wrong locations
2. **Test coverage**: Coverage report exists and meets threshold
3. **Linting**: No syntax errors
4. **YAML validation**: Valid YAML configuration
5. **Documentation**: Required docs exist

### Hook Configuration

```bash
# .git/hooks/pre-commit

#!/bin/bash
set -e

echo "Running compliance checks..."

# Check file organization
./scripts/compliance/check_file_org.sh

# Check test coverage
coverage=$(./scripts/compliance/get_coverage.sh)
if [ "$coverage" -lt 80 ]; then
    echo "ERROR: Test coverage $coverage% is below 80%"
    exit 1
fi

# Check for static images in reports
if find reports/ -name "*.png" -o -name "*.jpg" | grep -q .; then
    echo "ERROR: Static images found in reports. Use interactive HTML."
    exit 1
fi

echo "Compliance checks passed!"
```

## Error Handling

### Common Compliance Failures

| Issue | Cause | Resolution |
|-------|-------|------------|
| Structure violation | Files in wrong directory | Move files to correct location |
| Low test coverage | Insufficient tests | Add unit/integration tests |
| Static images | matplotlib exports | Convert to Plotly/Bokeh HTML |
| Missing CLAUDE.md | New repo setup | Run propagation script |
| Hook not running | Permission issue | `chmod +x .git/hooks/pre-commit` |

### Fixing Non-Compliance

#### Structure Issues

```bash
# Create missing directories
mkdir -p src tests docs config scripts data reports logs

# Move misplaced files
git mv root_file.py src/
git mv old_tests.py tests/unit/
```

#### Testing Issues

```bash
# Install pytest and coverage
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=src --cov-report=html --cov-fail-under=80
```

#### Logging Issues

```python
# Add proper logging configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

#### Reporting Issues

```python
# Replace matplotlib with Plotly
# Before (non-compliant):
import matplotlib.pyplot as plt
plt.savefig('reports/chart.png')

# After (compliant):
import plotly.express as px
fig = px.line(df, x='x', y='y')
fig.write_html('reports/chart.html')
```

### Troubleshooting

#### Hook Not Running

```bash
# Make hook executable
chmod +x .git/hooks/pre-commit

# Check hook exists
ls -la .git/hooks/pre-commit
```

#### False Positives

```bash
# Add exceptions to compliance config
# config/compliance.yaml
exceptions:
  - path: legacy/old_module.py
    reason: "Legacy code, scheduled for refactoring in Q2"
```

#### Coverage Not Detected

```bash
# Ensure coverage config exists
# pyproject.toml or .coveragerc
[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/migrations/*"]
```

## Metrics & Success Criteria

- **Compliance Rate**: >= 95% of repos fully compliant
- **Propagation Success**: 100% of repos have latest standards
- **Hook Coverage**: Git hooks installed in all active repos
- **CI Integration**: All repos have compliance in CI/CD
- **Exception Rate**: < 5% of checks have documented exceptions

## Compliance Reports

### Generate Compliance Report

```bash
./scripts/compliance/generate_report.sh > reports/compliance_report.html
```

### Report Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Compliance Report</title>
    <style>
        .pass { color: green; }
        .fail { color: red; }
        .warn { color: orange; }
    </style>
</head>
<body>
    <h1>Workspace Compliance Report</h1>
    <p>Generated: {{timestamp}}</p>

    <h2>Summary</h2>
    <table>
        <tr><td>Total Repositories</td><td>{{total}}</td></tr>
        <tr><td class="pass">Fully Compliant</td><td>{{compliant}}</td></tr>
        <tr><td class="warn">Partial Compliance</td><td>{{partial}}</td></tr>
        <tr><td class="fail">Non-Compliant</td><td>{{non_compliant}}</td></tr>
    </table>

    <h2>Repository Details</h2>
    {{#each repositories}}
    <h3>{{name}}</h3>
    <ul>
        {{#each checks}}
        <li class="{{status}}">{{check}}: {{message}}</li>
        {{/each}}
    </ul>
    {{/each}}
</body>
</html>
```

## Automation

### CI/CD Integration

```yaml
# .github/workflows/compliance.yml
name: Compliance Check

on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check File Organization
        run: ./scripts/compliance/check_file_org.sh

      - name: Check Test Coverage
        run: |
          pip install pytest pytest-cov
          pytest --cov=src --cov-fail-under=80

      - name: Check for Static Images
        run: |
          if find reports/ -name "*.png" | grep -q .; then
            echo "Static images found in reports"
            exit 1
          fi

      - name: Validate YAML Configs
        run: ./scripts/compliance/validate_yaml.sh
```

### Scheduled Compliance Scan

```yaml
# Run weekly compliance scan
name: Weekly Compliance Scan

on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9am

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Full Compliance Scan
        run: ./scripts/compliance/full_scan.sh
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: compliance-report
          path: reports/compliance_report.html
```

## Integration Points

### With Repository Sync

```bash
# After pulling, verify compliance
./scripts/repository_sync pull all
./scripts/compliance/verify_compliance.sh
```

### With AI Agents

AI agents should:
1. Check compliance status before making changes
2. Maintain compliance during modifications
3. Report compliance issues found during work
4. Follow guidelines in CLAUDE.md

### Related Skills

- [repo-sync](../repo-sync/SKILL.md) - Repository management
- [sparc-workflow](../sparc-workflow/SKILL.md) - Development methodology
- [workspace-cli](../workspace-cli/SKILL.md) - Unified CLI interface

## Best Practices

### For Repository Maintainers

1. **Run compliance checks before commits**
2. **Fix issues immediately** - don't accumulate debt
3. **Use pre-commit hooks** for automatic enforcement
4. **Review compliance reports** weekly

### For AI Agents

1. **Always check compliance status** before making changes
2. **Maintain compliance** during modifications
3. **Report compliance issues** found during work
4. **Follow guidelines** in CLAUDE.md and referenced docs

### For the Team

1. **Standardize across repos** using propagation tools
2. **Monitor compliance trends** over time
3. **Address root causes** not just symptoms
4. **Document exceptions** in decisions.md

## References

- [AI Agent Guidelines](../docs/modules/ai/AI_AGENT_GUIDELINES.md)
- [Development Workflow](../docs/modules/workflow/DEVELOPMENT_WORKFLOW.md)
- [File Organization Standards](../docs/modules/standards/FILE_ORGANIZATION_STANDARDS.md)
- [Testing Standards](../docs/modules/standards/TESTING_FRAMEWORK_STANDARDS.md)
- [Logging Standards](../docs/modules/standards/LOGGING_STANDARDS.md)
- [HTML Reporting Standards](../docs/modules/standards/HTML_REPORTING_STANDARDS.md)

---

## Version History

- **1.1.0** (2026-01-02): Upgraded to SKILL_TEMPLATE_v2 format - added Quick Start, When to Use, Execution Checklist, Error Handling consolidation, Metrics, Integration Points
- **1.0.0** (2024-10-15): Initial release with compliance verification, propagation tools, git hooks, CI/CD integration, troubleshooting

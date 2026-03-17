---
name: skill-name
description: >
  [REQUIRED] Comprehensive description of what this skill does and when to use it.
  Include: (1) Primary functionality, (2) Specific use cases, (3) Security operations context.
  Must include specific "Use when:" clause for skill discovery.
  Example: "SAST vulnerability analysis and remediation guidance using Semgrep and industry
  security standards. Use when: (1) Analyzing static code for security vulnerabilities,
  (2) Prioritizing security findings by severity, (3) Providing secure coding remediation,
  (4) Integrating security checks into CI/CD pipelines."
  Maximum 1024 characters.
version: 0.1.0
maintainer: your-github-username
category: [appsec|devsecops|secsdlc|threatmodel|compliance|incident-response]
tags: [relevant, security, tags]
frameworks: [OWASP|CWE|MITRE-ATT&CK|NIST|SOC2]
---

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this SKILL.md file under 500 lines
- Only include core workflows and common patterns here
- Move detailed content to references/ directory
- Link clearly to when references should be consulted
- See: references/WORKFLOW_CHECKLIST.md for workflow pattern examples
- Challenge every sentence: "Does Claude really need this?"
-->

# Skill Name

## Overview

Brief overview of what this skill provides and its security operations context.

## Quick Start

Provide the minimal example to get started immediately:

```bash
# Example command or workflow
tool-name --option value
```

## Core Workflow

### Sequential Workflow

For straightforward step-by-step operations:

1. First action with specific command or operation
2. Second action with expected output or validation
3. Third action with decision points if needed

### Workflow Checklist (for complex operations)

For complex multi-step operations, use a checkable workflow:

Progress:
[ ] 1. Initial setup and configuration
[ ] 2. Run primary security scan or analysis
[ ] 3. Review findings and classify by severity
[ ] 4. Apply remediation patterns
[ ] 5. Validate fixes with re-scan
[ ] 6. Document findings and generate report

Work through each step systematically. Check off completed items.

**For more workflow patterns**, see [references/WORKFLOW_CHECKLIST.md](references/WORKFLOW_CHECKLIST.md)

### Feedback Loop Pattern (for validation)

When validation and iteration are needed:

1. Generate initial output (configuration, code, etc.)
2. Run validation: `./scripts/validator_example.py output.yaml`
3. Review validation errors and warnings
4. Fix identified issues
5. Repeat steps 2-4 until validation passes
6. Apply the validated output

**Note**: Move detailed validation criteria to `references/` if complex.

## Security Considerations

- **Sensitive Data Handling**: Guidance on handling secrets, credentials, PII
- **Access Control**: Required permissions and authorization contexts
- **Audit Logging**: What should be logged for security auditing
- **Compliance**: Relevant compliance requirements (SOC2, GDPR, etc.)

## Bundled Resources

### Scripts (`scripts/`)

Executable scripts for deterministic operations. Use scripts for low-freedom operations requiring consistency.

- `example_script.py` - Python script template with argparse, error handling, and JSON output
- `example_script.sh` - Bash script template with argument parsing and colored output
- `validator_example.py` - Validation script demonstrating feedback loop pattern

**When to use scripts**:
- Deterministic operations that must be consistent
- Complex parsing or data transformation
- Validation and quality checks

### References (`references/`)

On-demand documentation loaded when needed. Keep SKILL.md concise by moving detailed content here.

- `EXAMPLE.md` - Template for reference documentation with security standards sections
- `WORKFLOW_CHECKLIST.md` - Multiple workflow pattern examples (sequential, conditional, iterative, feedback loop)

**When to use references**:
- Detailed framework mappings (OWASP, CWE, MITRE ATT&CK)
- Advanced configuration options
- Language-specific patterns
- Content exceeding 100 lines

### Assets (`assets/`)

Templates and configuration files used in output (not loaded into context). These are referenced but not read until needed.

- `ci-config-template.yml` - Security-enhanced CI/CD pipeline with SAST, dependency scanning, secrets detection
- `rule-template.yaml` - Security rule template with OWASP/CWE mappings and remediation guidance

**When to use assets**:
- Configuration templates
- Policy templates
- Boilerplate secure code
- CI/CD pipeline examples

## Common Patterns

### Pattern 1: [Pattern Name]

Description and example of common usage pattern.

### Pattern 2: [Pattern Name]

Additional patterns as needed.

## Integration Points

- **CI/CD**: How this integrates with build pipelines
- **Security Tools**: Compatible security scanning/monitoring tools
- **SDLC**: Where this fits in the secure development lifecycle

## Troubleshooting

### Issue: [Common Problem]

**Solution**: Steps to resolve.

## References

- [Tool Documentation](https://example.com)
- [Security Framework](https://owasp.org)
- [Compliance Standard](https://example.com)

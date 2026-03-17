---
name: _workflow-security-audit
description: Process for conducting system security reviews and remediating vulnerabilities. Follow the phases sequentially.
---

# Workflow Security Audit

Process for conducting system security reviews and remediating vulnerabilities.

This is a **Workflow** skill. When executing this lifecycle, you should progress through the phases sequentially. For each phase, invoke or refer to the specific sub-skills that are contextually relevant to the project's language or framework.

## Lifecycle Phases

### 1. Requirements & Threat Modeling
- [security-requirement-extraction](../security-requirement-extraction/SKILL.md)
- [threat-mitigation-mapping](../threat-mitigation-mapping/SKILL.md)
- [pci-compliance](../pci-compliance/SKILL.md)

### 2. Audit & Detection
- [security-review](../security-review/SKILL.md)
- [code-review](../code-review/SKILL.md)
- [code-review-excellence](../code-review-excellence/SKILL.md)

### 3. Remediation & Implementation
- [auth-implementation-patterns](../auth-implementation-patterns/SKILL.md)
- [secrets-management](../secrets-management/SKILL.md)
- [error-handling-patterns](../error-handling-patterns/SKILL.md)
- [shellcheck-configuration](../shellcheck-configuration/SKILL.md)

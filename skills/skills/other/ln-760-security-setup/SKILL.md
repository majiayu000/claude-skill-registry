---
name: ln-760-security-setup
description: "Coordinates security scanning (secrets + deps). Delegates to ln-761 + ln-625(mode=vulnerabilities_only). Generates SECURITY.md, pre-commit hooks, CI workflow."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Security Setup Coordinator

L2 Domain Coordinator that orchestrates security scanning and configuration for project bootstrap.

## Purpose & Scope

- Coordinate secret scanning (ln-761) and dependency vulnerability audit (ln-625)
- Aggregate findings from both workers into unified report
- Generate security infrastructure: SECURITY.md, pre-commit hooks, CI workflow
- Provide overall security score and risk assessment

## When to Use

- During project bootstrap (invoked by ln-700-project-bootstrap)
- Manual security audit request
- CI/CD pipeline initialization

---

## Workflow

### Phase 1: Pre-flight Check

**Step 1: Detect Project Type**
- Identify primary ecosystem(s): Node.js, .NET, Python, Go, etc.
- Check for existing security configs (`.gitleaks.toml`, `SECURITY.md`)

**Step 2: Check Tool Availability**
- Verify gitleaks/trufflehog available for secret scanning
- Verify ecosystem-specific audit tools available
- Log warnings for missing tools (do not fail)

**Step 3: Load Existing Configs**
- If `.gitleaks.toml` exists: note for preservation
- If `SECURITY.md` exists: note for update (not overwrite)
- If `.pre-commit-config.yaml` exists: check for gitleaks hook

### Phase 2: Delegate Scans

**Step 1: Invoke ln-761 Secret Scanner**
- Delegate via Task tool
- Receive: findings list, severity summary, remediation guidance

**Step 2: Invoke ln-625 Dependencies Auditor (mode=vulnerabilities_only)**
- Delegate via Task tool (can run parallel with Step 1)
- Pass parameter: `mode=vulnerabilities_only`
- Receive: vulnerability list, CVSS scores, fix recommendations

### Phase 3: Aggregate Reports

**Step 1: Combine Findings**
- Merge findings from both workers
- Group by severity (Critical first)
- Calculate overall security score

**Step 2: Risk Assessment**
- Critical findings: flag for immediate attention
- High findings: recommend fix within 48h
- Medium/Low: add to backlog

**Step 3: Build Summary**
- Files scanned count
- Secrets found (by severity)
- Vulnerabilities found (by severity)
- Overall pass/warn/fail status

### Phase 4: Generate Outputs

**Step 1: Create/Update SECURITY.md**
- Use template from `references/security_md_template.md`
- If exists: update, preserve custom sections
- If new: generate with placeholders

**Step 2: Configure Pre-commit Hooks**
- If `.pre-commit-config.yaml` missing: create from template
- If exists without gitleaks: recommend adding
- Template: `references/precommit_config_template.yaml`

**Step 3: Generate CI Workflow**
- If `.github/workflows/security.yml` missing: create from template
- Template: `references/ci_workflow_template.yaml`
- Include ecosystem-specific audit jobs

**Step 4: Update .gitignore**
- Ensure secret-related patterns present:
  - `.env`, `.env.*`, `!.env.example`
  - `*.pem`, `*.key`
- Preserve existing entries

---

## Delegation Pattern

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

| Worker | Parallel | Purpose |
|--------|----------|---------|
| ln-761-secret-scanner | Yes | Hardcoded secret detection |
| ln-625-dependencies-auditor | Yes | Vulnerability scanning (mode=vulnerabilities_only) |

**Prompt template:**
```
Task(description: "Secret scanning via ln-761",
     prompt: "Execute ln-761-secret-scanner. Read skill from ln-761-secret-scanner/SKILL.md. Project: {projectPath}",
     subagent_type: "general-purpose")

Task(description: "Dependency vulnerability scan via ln-625",
     prompt: "Execute ln-625-dependencies-auditor with mode=vulnerabilities_only. Read skill from ln-625-dependencies-auditor/SKILL.md. Project: {projectPath}. Mode: vulnerabilities_only (only CVE scan, skip outdated/unused checks).",
     subagent_type: "general-purpose")
```

**Pattern:** Both workers can execute in parallel via Task tool, then aggregate results.

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation
- ❌ Calling ln-625 without mode parameter (would run full audit)

---

## Definition of Done

- [ ] Both workers (ln-761, ln-625) invoked and completed
- [ ] Findings aggregated with severity classification
- [ ] SECURITY.md created/updated
- [ ] Pre-commit hook configured (or recommendation logged)
- [ ] CI workflow generated (or recommendation logged)
- [ ] .gitignore updated with secret patterns
- [ ] Summary report returned to parent orchestrator

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/security_md_template.md` | Template for SECURITY.md generation |
| `references/precommit_config_template.yaml` | Pre-commit hooks configuration |
| `references/ci_workflow_template.yaml` | GitHub Actions security workflow |

---

## Critical Rules

- **Always pass `mode=vulnerabilities_only` to ln-625** — full audit mode is not appropriate for bootstrap context
- **Preserve existing configs** — if `.gitleaks.toml`, `SECURITY.md`, or `.pre-commit-config.yaml` exist, update rather than overwrite
- **Use Task tool with `subagent_type: "general-purpose"`** for all worker delegations (context isolation)
- **Never fail on missing tools** — log warnings for unavailable scanners, continue with available ones
- **Critical findings block completion** — flag for immediate attention before returning to parent

---

**Version:** 3.0.0
**Last Updated:** 2026-02-05

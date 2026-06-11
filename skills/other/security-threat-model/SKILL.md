---
name: security-threat-model
description: "Security threat model: scan toolkit for attack surface, supply-chain risks."
agent: python-general-engineer
effort: high
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - threat model
    - security audit
    - supply chain scan
    - deny list
    - learning db sanitize
    - security posture
    - injection scan
    - surface scan
    - audit hooks
    - audit skills
  pairs_with:
    - python-general-engineer
  complexity: Complex
  category: security
---

# Security Threat Model Skill

## Overview

This skill executes a structured, phase-gated security threat model workflow that scans
the toolkit installation for attack surface exposure, supply-chain injection patterns,
and learning DB contamination. It follows the toolkit's four-layer architecture:
deterministic Python scripts perform all checks and produce JSON artifacts; Phase 5
(synthesis only) is the LLM step. Each phase gates on artifact validation before proceeding.

Outputs are saved to `security/` with a shared `run_id` for correlation across phases.
Phase 5 produces an actionable threat model document.

---

## Instructions

### Phase 1: SURFACE SCAN

**Goal**: Enumerate the active attack surface of the current installation.

Create the `security/` output directory and run the surface scan script:

```bash
mkdir -p security
python3 scripts/scan-threat-surface.py --output security/surface-report.json
```

This script enumerates:
- Registered hooks (from `~/.claude/settings.json`) with file paths and event types
- Installed MCP servers (from `~/.claude/mcp.json` and `.mcp.json`)
- Installed skills (from `skills/`) with `allowed-tools` entries
- Any file in `hooks/`, `skills/`, or `agents/` containing `ANTHROPIC_BASE_URL`

**Validate output**:
```bash
python3 -c "import json; d=json.load(open('security/surface-report.json')); print('hooks:', len(d.get('hooks',[])), '| skills:', len(d.get('skills',[])), '| mcp_servers:', len(d.get('mcp_servers',[])))"
```

**Gate (ARTIFACT VALIDATION)**: `security/surface-report.json` must exist, parse as valid JSON, and contain `hooks`, `skills`, and `mcp_servers` keys. A missing directory is handled gracefully with empty arrays. All artifacts are written to `security/` before gating. Do not proceed to Phase 2 until this gate passes.

---

### Phase 2: DENY-LIST GENERATION

**Goal**: Produce a concrete deny-list config derived from Phase 1 findings.

Generate the deny-list from the surface report:

```bash
python3 scripts/generate-deny-list.py \
    --surface security/surface-report.json \
    --output security/deny-list.json
```

The script applies these mappings from surface findings to deny rules:
- Hook uses `curl` or `wget` → append `"Bash(curl *)"` and `"Bash(wget *)"`
- Hook uses `ssh` or `scp` → append `"Bash(ssh *)"` and `"Bash(scp *)"`
- Skill `allowed-tools` contains unscoped `Read(*)` or `Write(*)` → add path-scoped deny entries
- Any file contains `ANTHROPIC_BASE_URL` override → append `"Bash(* ANTHROPIC_BASE_URL=*)"`

Always includes static baseline deny rules for credentials and privileged operations:
```json
["Read(~/.ssh/**)", "Read(~/.aws/**)", "Read(**/.env*)",
 "Write(~/.ssh/**)", "Write(~/.aws/**)",
 "Bash(curl * | bash)", "Bash(ssh *)", "Bash(scp *)", "Bash(nc *)",
 "Bash(* ANTHROPIC_BASE_URL=*)"]
```

**Display deny-list for human review**:
```bash
python3 -c "
import json
d = json.load(open('security/deny-list.json'))
print('Deny-list entries to add to settings.json:')
for rule in d['permissions']['deny']:
    print(' ', rule)
print()
print('Review security/deny-list.json before merging.')
"
```

**Gate (HUMAN APPROVAL REQUIRED)**: The deny-list is produced for human review only — it is never merged automatically. Display the diff and block until the operator confirms review. This gate is the highest-ROI control in the workflow. In `--ci-mode`, skip this gate and proceed to Phase 3. Do not proceed without explicit acknowledgment.

---

### Phase 3: SUPPLY-CHAIN AUDIT

**Goal**: Scan all installed hooks, skills, and agents for injection patterns and hidden characters.

Run the supply-chain audit:

```bash
python3 scripts/scan-supply-chain.py \
    --scan-dirs hooks/ skills/ agents/ \
    --output security/supply-chain-findings.json
```

Detection patterns (full regex details in `scripts/scan-supply-chain.py` source):
| Pattern | Severity |
|---------|----------|
| Zero-width + bidi Unicode characters | CRITICAL |
| HTML comments and hidden payload blocks | CRITICAL |
| `ANTHROPIC_BASE_URL` override in any file | CRITICAL |
| Instruction-override and role-hijacking phrases | CRITICAL |
| Outbound network commands in hooks/skills | WARNING |
| `enableAllProjectMcpServers` setting | WARNING |
| Broad permission grants without path scoping | WARNING |

**Check for CRITICAL findings**:
```bash
python3 -c "
import json, sys
d = json.load(open('security/supply-chain-findings.json'))
crits = [f for f in d.get('findings', []) if f.get('severity') == 'CRITICAL']
warns = [f for f in d.get('findings', []) if f.get('severity') == 'WARNING']
print(f'CRITICAL: {len(crits)}, WARNING: {len(warns)}')
if crits:
    for c in crits:
        print(f'  CRITICAL: {c[\"file\"]}:{c.get(\"line\",\"?\")} -- {c[\"pattern\"]}')
    sys.exit(1)
"
```

**Gate (BLOCKING CRITICAL FINDINGS)**: Any CRITICAL finding halts forward progress. All CRITICAL findings must be remediated or explicitly acknowledged before Phase 4 can start. This includes zero-width Unicode, ANTHROPIC_BASE_URL overrides, hidden payloads, and instruction-override phrases. WARNING findings are logged but do not block. Log warnings in the threat model under "Gaps and Recommended Next Controls" with acceptance rationale.

---

### Phase 4: LEARNING DB SANITIZATION

**Goal**: Inspect the learning DB for entries that may contain injected content from external sources.

Run the sanitization check in dry-run mode (never mutates without explicit `--purge`):

```bash
python3 scripts/sanitize-learning-db.py \
    --output security/learning-db-report.json
```

Flags entries where:
- `key` or `value` contain instruction-override or role-hijacking phrases
- `source` is `pr_review`, `url`, or `external` (high-risk origins)
- `value` contains zero-width Unicode or base64 blobs
- `first_seen` is older than 90 days and `source` indicates external origin

**Review flagged entries**:
```bash
python3 -c "
import json
d = json.load(open('security/learning-db-report.json'))
flagged = d.get('flagged_entries', [])
print(f'Total flagged: {len(flagged)}')
for e in flagged[:10]:
    print(f'  [{e[\"severity\"]}] id={e[\"id\"]} source={e.get(\"source\",\"?\")} action={e[\"action\"]}')
if len(flagged) > 10:
    print(f'  ... and {len(flagged)-10} more. See security/learning-db-report.json')
"
```

**Gate (DRY-RUN BY DEFAULT)**: The script operates in dry-run mode by default. No rows are deleted without explicit operator request and `--purge` flag. Present the report to the operator. If purge is desired after review, re-run with `--purge`. Learning DB is not found gracefully — script produces an empty report (`total_entries: 0`, `flagged_entries: []`). Proceed to Phase 5 when operator acknowledges the report or when no entries are flagged.

---

### Phase 5: THREAT MODEL SYNTHESIS

**Goal**: Synthesize Phases 1-4 findings into an actionable threat model document. This is the only LLM-driven phase.

Load all phase artifacts:
- `security/surface-report.json`
- `security/deny-list.json`
- `security/supply-chain-findings.json`
- `security/learning-db-report.json`

Write `security/threat-model.md` with these required sections (validator checks for exact headings):

```markdown
# Threat Model

## Run Metadata

## Attack Surface Inventory

## Active Threats

## Mitigations In Place

## Gaps and Recommended Next Controls

## Deny-List Status

## Supply-Chain Audit Summary

## Learning DB Sanitization Summary
```

Write `security/audit-badge.json`:
```json
{
  "status": "pass",
  "timestamp": "2026-01-01T00:00:00Z",
  "run_id": "from-surface-report",
  "critical_count": 0,
  "warning_count": 0,
  "phases_completed": 5
}
```

Status is `fail` if any CRITICAL finding was not remediated or if any phase gate did not pass.

**Validate outputs**:
```bash
python3 scripts/validate-threat-model.py \
    --threat-model security/threat-model.md \
    --badge security/audit-badge.json
```

**Gate (ARTIFACT VALIDATION WITH RETRY LIMIT)**: `validate-threat-model.py` must exit 0. If validation fails, add the missing sections and re-run. Maximum 3 fix iterations before escalating to operator for review.

---

## Error Handling

### Supply-chain audit CRITICAL finding blocks progress
**Cause**: A hook, skill, or agent contains zero-width Unicode, ANTHROPIC_BASE_URL override, or known injection phrase.

**Resolution**:
1. Open the flagged file at the reported line number
2. Determine if it is a legitimate false positive (e.g., documentation discussing injection patterns)
3. If false positive: add the file to `--exclude` list and re-run `scan-supply-chain.py`
4. If genuine: remediate the file (remove hidden payloads, instruction-override phrases) before continuing to Phase 4

### Validation fails with missing sections
**Cause**: Phase 5 synthesis omitted a required section heading.

**Resolution**: Read the validator output for the exact missing section name. Add the section to `security/threat-model.md` with content synthesized from the phase artifacts and re-run `validate-threat-model.py`. Maximum 3 fix iterations before escalating to operator.

### Missing configuration or databases
**Cause**: `~/.claude/settings.json` or learning DB doesn't exist.

**Resolution**: These are handled gracefully by the scripts:
- Missing `settings.json` → surface-report produces empty arrays for hooks
- Missing learning DB → sanitization report returns `total_entries: 0` and `flagged_entries: []`
These are not error conditions. Re-run with `--verbose` for detail on missing paths.

---

## References

- [ADR-102: Security Threat Model Skill](../../adr/ADR-102-security-threat-model.md)
- [pretool-prompt-injection-scanner.py](../../hooks/pretool-prompt-injection-scanner.py) -- session-time injection scanner (complements, does not replace this skill)
- [learning_db_v2.py](../../hooks/lib/learning_db_v2.py) -- learning DB schema and connection interface
- OWASP MCP Top 10 (living document)
- Snyk ToxicSkills research: 36% of public skills contained injection patterns

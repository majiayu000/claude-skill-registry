---
name: adversarial-validator
version: 1.0.0
description: |
  Adversarial audit system for SDLC phases. Finds problems that self-validation missed.
  Uses challenge mindset to identify CRITICAL to LIGHT issues.

capabilities:
  - Audit any SDLC phase (0-8)
  - Classify findings (CRITICAL, GRAVE, MEDIUM, LIGHT)
  - Generate structured audit reports
  - Decide: FAIL, PASS_WITH_WARNINGS, PASS
  - Auto-correction attempt (1x retry)

agents:
  - phase-auditor

hooks:
  - post-gate-audit

configuration:
  path: config/audit_config.yml
  schema: config/audit_schema.json
---

# Adversarial Validator Skill

## Purpose

Provide adversarial quality assurance after gates pass. This skill challenges
the work done during a phase and identifies issues that may have been missed
by self-validation.

## How It Works

```
Phase Execution → Self-Validation → Gate → Adversarial Audit → Decision
                                     ✓            ↓
                                              Find Problems
                                                  ↓
                                        FAIL | PASS_WITH_WARNINGS | PASS
```

## Usage

### Via Hook (Automatic)

```bash
# Executed automatically by post-gate-audit.py hook
# No manual invocation needed
```

### Via Command (Manual)

```bash
# Audit specific phase
python3 .claude/skills/adversarial-validator/scripts/audit_phase.py \
  --phase 5 \
  --project-path /path/to/project

# Audit with specific configuration
python3 .claude/skills/adversarial-validator/scripts/audit_phase.py \
  --phase 3 \
  --config custom-audit-config.yml

# Generate report only (no decision)
python3 .claude/skills/adversarial-validator/scripts/audit_phase.py \
  --phase 5 \
  --report-only
```

### Via Slash Command

```
/audit-phase 5
```

## Configuration

### Global Configuration

File: `.claude/skills/adversarial-validator/config/audit_config.yml`

```yaml
adversarial_audit:
  enabled: true

  # Which phases to audit
  phases: [3, 5, 6]  # Architecture, Implementation, Quality

  # Severity thresholds
  fail_on: ["CRITICAL", "GRAVE"]
  warn_on: ["MEDIUM", "LIGHT"]

  # Retry behavior
  max_retries: 1  # Try to fix once, then escalate
  auto_correct: true  # Attempt automatic correction

  # Audit depth
  thoroughness: "deep"  # quick | normal | deep

  # Reporting
  report_format: "yaml"  # yaml | json | markdown
  save_reports: true
  reports_dir: ".agentic_sdlc/audits"
```

### Per-Project Override

File: `.claude/settings.json`

```json
{
  "sdlc": {
    "quality_gates": {
      "adversarial_audit": {
        "enabled": true,
        "phases": [2, 3, 5, 6, 7],  // More phases
        "fail_on": ["CRITICAL"],  // More lenient
        "max_retries": 2  // More attempts
      }
    }
  }
}
```

## Audit Process

### 1. Understand Phase Context

```python
# Load phase definition
phase_info = load_phase_metadata(phase_number)

# Expected artifacts
artifacts = phase_info["expected_artifacts"]

# Quality criteria
criteria = phase_info["quality_criteria"]
```

### 2. Review Artifacts

```python
# Scan for created artifacts
created = scan_artifacts(project_path, phase)

# Compare expected vs actual
missing = set(artifacts) - set(created)
```

### 3. Run Automated Checks

```python
checks = [
    check_hardcoded_secrets(),
    check_test_coverage(),
    check_security_scan(),
    check_todos_fixmes(),
    check_error_handling(),
]

findings = []
for check in checks:
    results = check.run()
    findings.extend(results)
```

### 4. LLM Deep Analysis

```python
# Call phase-auditor agent with adversarial prompt
audit_prompt = f"""
Analyze Phase {phase} work with CHALLENGE MINDSET.
Your job is to FIND PROBLEMS, not to validate.

Artifacts: {artifacts}
Project: {project_path}

Find: CRITICAL, GRAVE, MEDIUM, LIGHT issues.
Be skeptical. Look deeper.
"""

llm_findings = call_agent("phase-auditor", audit_prompt)
findings.extend(llm_findings)
```

### 5. Classify and Decide

```python
# Group by severity
classified = group_by_severity(findings)

# Decision logic
if classified["CRITICAL"] > 0 or classified["GRAVE"] > 0:
    decision = "FAIL"
elif classified["MEDIUM"] > 0 or classified["LIGHT"] > 0:
    decision = "PASS_WITH_WARNINGS"
else:
    decision = "PASS"
```

### 6. Generate Report

```python
report = {
    "phase": phase,
    "audited_at": datetime.utcnow().isoformat(),
    "decision": decision,
    "findings": classified,
    "next_steps": generate_next_steps(decision, findings)
}

save_report(report, f".agentic_sdlc/audits/phase-{phase}-audit.yml")
```

## Automated Checks

### Security Checks

```python
def check_hardcoded_secrets():
    """Scan for hardcoded credentials"""
    patterns = [
        r'password\s*=\s*["\'].*["\']',
        r'api[_-]?key\s*=\s*["\'].*["\']',
        r'secret\s*=\s*["\'].*["\']',
        r'token\s*=\s*["\'].*["\']',
    ]

    findings = []
    for file in scan_files():
        for pattern in patterns:
            matches = re.findall(pattern, file.content)
            if matches:
                findings.append({
                    "severity": "CRITICAL",
                    "title": "Hardcoded secret detected",
                    "location": f"{file.path}:{line}",
                    "evidence": match
                })

    return findings
```

### Test Coverage Checks

```python
def check_test_coverage():
    """Verify test coverage >= 80%"""
    result = subprocess.run(
        ["pytest", "--cov=src", "--cov-report=json"],
        capture_output=True
    )

    coverage = json.loads(result.stdout)["totals"]["percent_covered"]

    if coverage < 80:
        return [{
            "severity": "GRAVE",
            "title": f"Test coverage too low: {coverage}%",
            "recommendation": "Add tests to reach >= 80% coverage"
        }]

    return []
```

### Quality Checks

```python
def check_todos_fixmes():
    """Find TODO/FIXME comments left in code"""
    findings = []

    for file in scan_files(exclude_dirs=["tests", "node_modules"]):
        for line_no, line in enumerate(file.lines):
            if re.search(r'TODO|FIXME|XXX|HACK', line):
                findings.append({
                    "severity": "MEDIUM",
                    "title": "TODO/FIXME left in code",
                    "location": f"{file.path}:{line_no}",
                    "evidence": line.strip()
                })

    return findings
```

## Auto-Correction

If `auto_correct: true` and CRITICAL/GRAVE found:

```python
if decision == "FAIL" and config["auto_correct"]:
    print("Attempting auto-correction...")

    for finding in critical_findings:
        corrector = get_corrector(finding["category"])

        try:
            corrector.fix(finding)
            print(f"✓ Fixed: {finding['title']}")
        except Exception as e:
            print(f"✗ Could not fix: {e}")
            escalate_to_human(finding)

    # Re-audit after fixes
    if max_retries > 0:
        print("Re-auditing after fixes...")
        return audit_phase(phase, max_retries - 1)
```

## Integration with Orchestrator

```python
# orchestrator.md workflow
def advance_phase(current_phase):
    # 1. Execute phase
    execute_phase(current_phase)

    # 2. Self-validation
    self_validate(current_phase)

    # 3. Gate evaluation
    gate_result = evaluate_gate(current_phase)
    if not gate_result.passed:
        raise GateFailure(gate_result)

    # 4. Adversarial audit (NEW)
    if is_audit_enabled(current_phase):
        audit_result = run_adversarial_audit(current_phase)

        if audit_result.decision == "FAIL":
            if auto_correct_enabled():
                attempt_auto_correction(audit_result)
                # Retry phase after correction
                return advance_phase(current_phase)
            else:
                raise AuditFailure(audit_result)

        if audit_result.decision == "PASS_WITH_WARNINGS":
            create_tech_debt_issues(audit_result.findings)

    # 5. Advance to next phase
    transition_to(current_phase + 1)
```

## Slash Commands

### /audit-phase

```yaml
command: audit-phase
description: Run adversarial audit on specified phase
usage: /audit-phase <phase_number>
examples:
  - /audit-phase 5
  - /audit-phase 3 --thorough
  - /audit-phase 6 --report-only
```

### /audit-report

```yaml
command: audit-report
description: View last audit report for phase
usage: /audit-report <phase_number>
examples:
  - /audit-report 5
  - /audit-report 3 --format json
```

## Troubleshooting

### Audit Too Strict

```yaml
# Make audit more lenient
adversarial_audit:
  fail_on: ["CRITICAL"]  # Only fail on critical
  warn_on: ["GRAVE", "MEDIUM", "LIGHT"]
```

### Audit Too Slow

```yaml
# Reduce thoroughness
adversarial_audit:
  thoroughness: "quick"  # Skip deep analysis
  phases: [5, 6]  # Audit fewer phases
```

### False Positives

```yaml
# Exclude certain checks
adversarial_audit:
  excluded_checks:
    - "todos_in_code"  # Allow TODOs temporarily
    - "coverage_threshold"  # Relax coverage requirement
```

## Metrics

Track audit effectiveness:

```yaml
audit_metrics:
  total_audits: 142
  failed_audits: 12  # 8.4% failure rate
  pass_with_warnings: 87  # 61.3%
  clean_pass: 43  # 30.3%

  avg_findings_per_audit:
    critical: 0.1
    grave: 0.4
    medium: 2.3
    light: 3.7

  auto_corrections:
    attempted: 12
    successful: 9  # 75% success rate
    escalated: 3  # 25% needed human
```

## Best Practices

1. **Enable for critical phases** (3, 5, 6)
2. **Review audit reports** even when passing
3. **Track patterns** in findings to improve self-validation
4. **Tune thresholds** based on team velocity vs quality needs
5. **Don't bypass** audits for "urgent" work (that's when bugs happen)

---

**Version:** 1.0.0
**Agent:** phase-auditor
**Hook:** post-gate-audit
**Epic:** #TBD

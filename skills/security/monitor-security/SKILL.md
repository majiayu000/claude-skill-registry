---
name: monitor-security
description: 'This skill is always-on. It:'
---

---
name: monitor-security
description: >
  Nightly self-hack orchestrator and continuous security monitoring for embry-os.
  Four-tier probe system: T0 deterministic (Semgrep, pip-audit, gitleaks), T0.5
  threat intelligence (consume-feed, social-bridge, dogpile), T1 OWASP LLM Top 10
  analysis, T2 Docker self-hack (containerized /hack against a twin), T3 cascade
  validation (GPT swarm classifiers + Brandon teacher). Composes /hack, /battle,
  /consume-feed, /social-bridge, /dogpile, /assistant, and /scillm.
triggers:
  - monitor security
  - security monitor
  - self-hack
  - nightly security
  - security dashboard
  - threat intelligence
  - owasp scan
  - security probes
allowed-tools: Bash, Read
metadata:
  short-description: Nightly self-hack orchestrator with four-tier probe cascade

taxonomy:
  - security
  - corruption
  - observability
  - self-improvement

provides:
  - monitor-security
composes: [, task-monitor]
---

# monitor-security

## Continuous Operation (Non-Negotiable)

This skill is **always-on**. It:
- Runs on its configured schedule indefinitely — it NEVER stops unless explicitly halted by the user
- The agent MUST NOT stop and wait for the human to ask for status or remember to check
- If a cycle fails, diagnose the failure, attempt auto-repair, and continue
- Only escalate to the human if genuinely blocked after exhausting /dogpile research
- Gracefully handles restarts and maintains state across cycles
- Is designed for multi-day/week/month autonomous operation

**Anti-pattern**: Reporting status and waiting for the human to ask "what next?" is UNACCEPTABLE. The agent must proactively fix issues and continue the monitoring loop.

## Architecture

```
Hourly Threat Intel Loop (:00-:10)
  consume-feed → social-bridge → dogpile (if critical CVE) → threat_intel_digest.json

Nightly Self-Hack (00:30-03:00)
  00:30  Read threat_intel_digest.json → prioritize attack vectors
  01:00  T0: Deterministic (Semgrep, pip-audit, gitleaks, grep audits)
  01:15  T1: OWASP LLM Top 10 static analysis
  01:30  T2: Docker self-hack (build twin → /hack scan → score)
  02:00  T3: Cascade validation (T0→T1.5 GPT swarm→T2 Brandon)
  02:30  /battle (conditional — only if T2 critical findings)
  03:00  Report + /memory learn findings
```

## Commands

```bash
./run.sh check [--tier N] [--probe NAME] [--autofix] [--json]
./run.sh dashboard
./run.sh fix <probe-name>
./run.sh threat-intel [--dry-run]
./run.sh register-nightly
./run.sh register-hourly
./run.sh help
```

## Probe Tiers

| Tier | Probes | Description | Cadence |
|------|--------|-------------|---------|
| 0 | P01-P07 | Deterministic (Semgrep, pip-audit, gitleaks, grep) | Nightly |
| 0.5 | P08-P09 | Threat intel ingest + cross-reference | Hourly |
| 1 | P10-P14 | OWASP LLM Top 10 analysis | Nightly |
| 2 | P20-P23 | Docker self-hack | Nightly |
| 3 | P30-P33 | Cascade validation + label accumulation | Nightly |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MONITOR_TARGET_ROOT | auto-detect (pi-mono root) | Target project to scan |
| MONITOR_STATE_DIR | ~/.pi/monitor-security | State file directory |
| CASCADE_SHADOW_FILE | ~/.pi/monitor-security/shadow.jsonl | Shadow mode log |
| CASCADE_METRICS_FILE | ~/.pi/monitor-security/metrics.jsonl | Cascade metrics |
| THREAT_INTEL_DIGEST | ~/.pi/monitor-security/threat_intel_digest.json | Hourly digest |
| RETRAIN_LABEL_THRESHOLD | 50 | Labels before triggering /create-gpt retrain |

## State

- `~/.pi/monitor-security/latest_report.json` — Latest probe results
- `~/.pi/monitor-security/threat_intel_digest.json` — Accumulated hourly threat intel
- `~/.pi/monitor-security/training_labels.jsonl` — Brandon teacher judgments
- `~/.pi/monitor-security/shadow.jsonl` — Shadow mode comparison log
- `~/.pi/monitor-security/report_t{0,1,2,3}.json` — Per-tier reports

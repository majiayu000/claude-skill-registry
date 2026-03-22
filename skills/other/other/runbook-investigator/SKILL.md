---
name: runbook-investigator
description: "Structured investigation and troubleshooting for production incidents, build failures, performance issues, and mysterious bugs. Use when the user says 'debug this', 'why is this failing', 'investigate this issue', 'troubleshoot', 'production is down', 'this is broken and I don't know why', 'help me find the root cause', 'postmortem', 'incident response', or 'something is wrong'. Also triggers on 'runbook', 'investigation', 'troubleshooting', 'root cause analysis', 'incident', 'outage', 'debugging', 'diagnose', or 'what went wrong'."
version: 1.0.0
---

# Runbook Investigator

## Purpose

When something breaks, the instinct is to start changing things. This is wrong. Investigation must precede intervention. Gather evidence before forming hypotheses, form hypotheses before making changes.

Changing things before understanding the problem destroys evidence, introduces new variables, and turns a single mystery into multiple overlapping mysteries. The fastest path to resolution is disciplined observation followed by targeted action.

## When to Activate

- Production incidents and outages
- Build or deploy failures with unclear causes
- Performance degradation (latency spikes, throughput drops, resource exhaustion)
- Intermittent or flaky failures that resist easy explanation
- "Works on my machine" discrepancies across environments
- Post-incident analysis and root cause investigations
- Any situation where the cause of a failure is not immediately obvious

## Investigation Protocol (OODA Loop)

### Observe

Gather facts without interpretation. Do not theorize yet.

- What is the exact error message or symptom?
- When did it start? What is the timeline?
- What changed recently? (deploys, config changes, dependency updates, infrastructure changes)
- Who is affected? How many? Which users, regions, or services?
- What is still working? Negative evidence constrains hypotheses.
- Capture logs, metrics, screenshots, and stack traces NOW before they rotate or get overwritten.

### Orient

Form hypotheses based on evidence. Rank them.

- What single explanation accounts for ALL observed symptoms?
- Eliminate hypotheses that contradict any confirmed evidence.
- Rank remaining hypotheses by likelihood AND by ease of verification.
- Consider: is this a new bug, a regression, an infrastructure issue, or an external dependency failure?
- Check for known patterns. Reference `references/investigation-templates.md` for common scenarios.

### Decide

Choose the next investigation step. Optimize for information gain.

- For each hypothesis: what is the minimum evidence needed to confirm or eliminate it?
- Prefer non-destructive checks first (read logs, query metrics, inspect state).
- If multiple hypotheses remain, pick the check that eliminates the most possibilities.
- Set a timebox. If a line of investigation yields nothing in 10 minutes, pivot.

### Act

Execute the investigation step. Record everything.

- Run the specific check or command.
- Record the result in the investigation log, whether it confirms or refutes the hypothesis.
- If confirmed: proceed to resolution.
- If refuted: loop back to Orient with new evidence.
- If inconclusive: try a different angle on the same hypothesis or move to the next one.

## Triage Decision Tree

```
Is production affected?
├─ Yes → Is data being lost or corrupted?
│  ├─ Yes → CRITICAL: Mitigate first, investigate second
│  └─ No  → HIGH: Investigate with urgency
└─ No  → Is it blocking development?
   ├─ Yes → MEDIUM: Investigate promptly
   └─ No  → LOW: Queue for investigation
```

Reference `references/triage-decision-tree.md` for the detailed tree with specific commands, response times, and escalation paths for each severity level.

## Investigation Toolkit

### Recent Changes

- `git log --oneline --since="2 days ago"` — recent commits
- `git diff HEAD~5..HEAD` — recent code changes
- Deployment history — CI/CD dashboard, deploy logs
- Dependency changes — lockfile diffs (`git diff HEAD~5..HEAD -- *lock*`)

### Error Signals

- Application logs — structured logs, error rates, stack traces
- Error tracking — Sentry, Bugsnag, Datadog APM
- Monitoring dashboards — Grafana, CloudWatch, Datadog
- Alerting history — what alerts fired and when

### System State

- Process health — `ps aux`, `top`, `htop`
- Memory and CPU — `free -m`, `vmstat`, resource monitor
- Disk usage — `df -h`, `du -sh /path/*`
- Network — `netstat -tlnp`, `ss -tlnp`, DNS resolution

### Dependency Health

- Database — connection count, replication lag, slow query log
- External APIs — response times, error rates, status pages
- Message queues — queue depth, consumer lag, dead letter queues
- Cache — hit rate, eviction rate, memory usage

### Configuration

- Environment variables — diff between working and broken environments
- Feature flags — recently toggled flags
- Infrastructure config — Terraform/CloudFormation changes, K8s manifests

## Common Investigation Patterns

Reference `references/investigation-templates.md` for detailed checklists. Summary of the four primary patterns:

1. **Build Failure**: Read the FULL error → check dependency changes → verify runtime version → check disk space → clean build → compare CI vs local.

2. **Performance Degradation**: Identify the slow path → check DB queries (EXPLAIN ANALYZE) → look for N+1 patterns → verify cache hit rates → check connection pools → review recent traffic changes.

3. **Intermittent Failure**: Correlate with time/load/input → check for race conditions → check resource exhaustion → verify external dependency stability → review timeout and retry configs.

4. **"Works on My Machine"**: Compare OS and runtime versions → diff env vars → check database state → verify file path assumptions → look for implicit dependencies.

## Investigation Log Format

Maintain this log throughout every investigation. It creates an audit trail for postmortems and prevents re-treading the same ground.

```
INVESTIGATION LOG
=================
Issue: [one-line description of the symptom]
Severity: [CRITICAL / HIGH / MEDIUM / LOW]
Started: [timestamp]

Timeline:
[HH:MM] Observation: [what was observed]
[HH:MM] Hypothesis: [what could explain it]
[HH:MM] Evidence: [what we checked and found]
[HH:MM] Action: [what we changed]
[HH:MM] Result: [did it help? what changed?]

Root Cause: [what actually caused the issue]
Resolution: [what fixed it]
Prevention: [what prevents recurrence — code change, monitoring, test, runbook]
```

Update the log in real time. Every check gets a line. Every hypothesis gets recorded, whether confirmed or refuted. When the investigation concludes, the log becomes the basis for the postmortem.

## Gotchas

**Premature intervention destroys evidence.** Restarting a service clears in-memory state. Redeploying overwrites the broken artifact. Clearing a cache eliminates the cache state that might explain the bug. Observe and capture evidence before changing anything.

**Correlation is not causation.** "We deployed 2 hours before the issue started" does not mean the deploy caused it. Look for the mechanism. Can you trace a code path from the change to the symptom? If not, the correlation may be coincidental.

**Complex systems have multiple root causes.** The outage may result from a combination of a code bug, a traffic spike, and an infrastructure misconfiguration. Do not stop investigating after finding one contributing factor.

**The "obvious" fix is often wrong.** If the root cause seems too obvious, verify it explicitly. Obvious explanations feel satisfying, which makes them dangerous. They often mask the real cause.

**Recency bias distorts investigation.** The instinct is to focus on recent changes, but the bug may have existed for months, only now triggered by a change in traffic, data, or configuration. Consider dormant bugs.

**"Can't reproduce" does not mean "doesn't exist."** Reproduction requires matching the environment, data, timing, and concurrency of the original failure. If you cannot reproduce, you have not matched all the conditions.

**Fix-forward pressure can waste hours.** Sometimes rolling back is faster than debugging. If you have been investigating for more than 30 minutes on a production incident with a clear rollback path, seriously consider rolling back first and debugging second. You can always redeploy after understanding the issue.

**Tunnel vision on a single hypothesis.** If you have spent more than 15 minutes trying to confirm one hypothesis without progress, step back. List all hypotheses again. The answer may be elsewhere.

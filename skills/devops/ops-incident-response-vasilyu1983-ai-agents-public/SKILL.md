---
name: ops-incident-response
description: "Guides incident response from detection through postmortem. Use when designing on-call runbooks, triaging production incidents, writing status updates, or improving MTTD and MTTR."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Incident Response

Production incident management: detect, triage, mitigate, resolve, learn. This skill covers the human and process side of incidents, not the infrastructure automation (use `ops-devops-platform` for that).

## Quick Reference

| Need | Go to |
|------|-------|
| Classify the incident severity | `## Severity Classification` |
| Run the end-to-end response loop | `## Workflow` |
| Coordinate as incident commander | `## Incident Commander Checklist` |
| Send status or stakeholder updates | `## Communication Templates` |
| Use templates and runbooks | `## Navigation` |

## Scope

| Use For | Do NOT Use For |
|---------|----------------|
| Severity classification and escalation | Infrastructure provisioning or CI/CD |
| On-call runbook design and review | Application resilience patterns (retries, circuit breakers) |
| Incident commander workflows | Monitoring/alerting tool setup |
| Status page and stakeholder communication | Root cause analysis of code bugs |
| Blameless postmortem facilitation | Performance benchmarking |
| MTTD/MTTR measurement and improvement | Security incident forensics (use software-security-appsec) |

## Severity Classification

| Level | Criteria | Response time | Who is paged |
|-------|----------|---------------|-------------|
| **SEV1** | Revenue-impacting, data loss, full outage | Immediate | On-call + incident commander + leadership |
| **SEV2** | Degraded service, partial outage, SLO breach | 15 min | On-call + incident commander |
| **SEV3** | Minor degradation, workaround available | 1 hour | On-call |
| **SEV4** | Cosmetic, no user impact, internal tooling | Next business day | Ticket owner |

## ASCII Flow

```text
Alert, user report, or suspected incident
  -> Detect and acknowledge within SLA
  -> Open incident channel and assign roles
  -> Triage impact, blast radius, and severity
  -> Communicate status and next update time
  -> Mitigate user impact before deep root-cause work
  -> Verify recovery with metrics and smoke tests
  -> Resolve, close comms, and schedule postmortem
  -> Feed action items back into runbooks, alerts, and platform work
```

## Workflow

```text
1) DETECT — Alert fires or user report received
   - Acknowledge the alert within SLA
   - Open an incident channel (Slack/Teams)
   - Assign incident commander if SEV1/SEV2

   DECLARE-AND-MOBILIZE (T+0, SEV1/SEV2):
   - Auto-create or manually open a dedicated #inc-YYYYMMDD-[short-name] channel
   - Assign roles at declaration: IC, comms lead, scribe — do not wait for volunteers
   - Post status-page automation or manual update within 5 min of declaration
   - Trigger postmortem document creation at incident close (template auto-populated
     with title, severity, IC, timeline start — not at the writing stage)
   - These are process expectations, not product prescriptions; implement with
     whatever incident tooling your team uses (PagerDuty, Opsgenie, homegrown)

2) TRIAGE — Assess impact and classify severity
   - Confirm affected systems, user segments, blast radius
   - Check recent deployments, config changes, dependency status
   - Update status page with initial assessment
   - If SLO/error-budget tracking is active: post current budget consumed in channel

3) MITIGATE — Stop the bleeding
   - Prioritize mitigation over root cause
   - Rollback, feature-flag off, scale up, redirect traffic
   - Communicate ETA or "investigating" to stakeholders

4) RESOLVE — Confirm recovery
   - Verify metrics return to baseline
   - Run smoke tests on affected paths
   - Update status page to "resolved"
   - Close the incident channel
   - Note total error-budget consumed in the postmortem summary line

5) LEARN — Blameless postmortem
   - Write timeline (what happened, when, who did what)
   - Identify contributing factors (not "root cause")
   - Define action items with owners and deadlines
   - Share postmortem with the team
   - For SEV1/SEV2: use the Howie structured-interview approach before group debrief
     (see references/postmortem-facilitation.md)
```

## Incident Commander Checklist

- [ ] Open dedicated incident channel
- [ ] Assign roles: IC, comms lead, subject matter experts
- [ ] Set a timer for status updates (every 15-30 min for SEV1/2)
- [ ] Keep a running timeline in the channel
- [ ] Delegate investigation — IC coordinates, does not debug
- [ ] Post status page updates at each phase transition
- [ ] Call "resolved" only when metrics confirm recovery
- [ ] Schedule postmortem within 48 hours

## Judgment Calls a Checklist Won't Make for You

A checklist tells you *what* to do. These are the calls where the IC's judgment is the actual value-add — get these wrong and the checklist executes perfectly around a bad decision.

**Declare vs. don't declare, under ambiguity.** The cost of over-declaring (a false SEV2 that interrupts a few engineers for 20 minutes) is almost always smaller than the cost of under-declaring (a real SEV1 running uncoordinated for the same 20 minutes). When symptoms are genuinely ambiguous in the first two minutes, escalate — this is not optimism, it is the dominant strategy under minimax regret (see `references/decision-theory-applied.md` P2). The failure mode worth watching for is the opposite: an IC who keeps a live incident at SEV3 past the point where a reasonable second opinion would have escalated it, because declaring SEV1/2 feels like "making a bigger deal of it." Declaring is cheap. Under-declaring is not reversible after the fact.

**Comms-cadence trade-offs.** A fixed 15-minute cadence is a floor, not a ceremony. Send an update sooner than the timer when: the situation materially changes (new blast radius, new mitigation, escalation to a higher severity); or a stakeholder audience (support, leadership, a named customer) is about to make a decision based on stale information. Send "no change since last update, next update at HH:MM" rather than silence — silence is read as either "resolved" or "abandoned," never as "still working on it." The trade-off cuts the other way too: paging every update to a broad channel when nothing has changed trains people to stop reading incident channels. Match audience size to update frequency — narrow SME channel gets high-frequency raw detail; the stakeholder-facing channel gets only state-change updates.

**What a good IC notices that the checklist doesn't ask about.** The checklist says "keep a running timeline" — it doesn't say to notice that the timeline has gone quiet for 10 minutes with no explanation, which is the tell that someone is deep in a rabbit hole instead of reporting status. The checklist says "delegate investigation" — it doesn't say to notice when two SMEs are proposing conflicting mitigations (e.g., one wants to roll back, another wants to scale up) and neither has said so out loud; the IC's job is to surface the conflict, not let it resolve by whoever pushes first. The checklist says "call resolved only when metrics confirm recovery" — it doesn't say to notice when the room is exhausted and eager to declare resolution on a metric that looks better but hasn't held for a full cycle. Watch for premature declarations of "investigating" that are actually stalling on an uncomfortable rollback call (see `references/decision-theory-applied.md` P4/A2) — that's a decision-avoidance pattern, not a diagnostic one.

**Postmortem anti-patterns beyond the obvious.**
- **Blame laundering**: the document uses blameless language ("the engineer who deployed the change...") while every sentence still orbits one person's actions; the tell is a timeline that reads like a deposition. Fix by writing every timeline entry as "the system/process allowed X" rather than "X did Y."
- **Action-item graveyard**: postmortems generate action items that get logged and never revisited — the postmortem completion rate looks healthy (100%) while the action item close rate (a separate metric in `## Metrics`) quietly rots. If a team tracks postmortem completion but not action-item closure, it is optimizing the metric that doesn't matter.
- **Root-cause theater**: closing on a single named root cause because it is psychologically satisfying, then writing exactly one action item against it, when the timeline itself shows three or four independent contributing factors that each deserve an owner.

## Communication Templates

### Status Page — Investigating

```text
[Service Name] — Investigating
We are aware of [brief description of impact].
Our team is investigating and will provide updates every [interval].
Started: [timestamp UTC]
```

### Status Page — Resolved

```text
[Service Name] — Resolved
The issue affecting [brief description] has been resolved.
Duration: [start] to [end] ([total minutes])
A postmortem will be published within [N] business days.
```

### Stakeholder Update (SEV1/2)

```text
Subject: [SEV-N] [Service] incident update — [status]

Impact: [who is affected, what they see]
Current status: [mitigating / investigating / resolved]
Next update: [time UTC]
Actions taken: [bulleted list]
Incident lead: [name]
```

## Metrics

| Metric | What it measures | Target |
|--------|-----------------|--------|
| **MTTD** (Mean Time to Detect) | Alert fires → human acknowledges | < 5 min for SEV1 |
| **MTTA** (Mean Time to Acknowledge) | Alert → first responder action | < 15 min for SEV1 |
| **MTTM** (Mean Time to Mitigate) | Acknowledge → user impact stops | < 30 min for SEV1 |
| **MTTR** (Mean Time to Resolve) | Detect → fully resolved | < 1 hour for SEV1 |
| **Postmortem completion rate** | Incidents with published postmortems | 100% for SEV1/2 |
| **Action item close rate** | Postmortem actions completed on time | > 80% within deadline |

**Distributional caveat**: incident durations follow heavy-tailed distributions. The *mean* (the "M" in MTTx) is easily skewed by outlier incidents and is "poorly suited for decision making or trend analysis" (Davidovič, Google SRE). Use MTTx labels to name the phase; use **p50/p90/p99 percentiles** and **incident frequency/rate** for trend analysis and comparison. See `references/incident-metrics-guide.md` for the full treatment.

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Blaming individuals in postmortems | Focus on systems, processes, and contributing factors |
| Skipping postmortems for "small" incidents | Write lightweight postmortems for SEV3; skip only SEV4 |
| IC also debugging | IC coordinates and communicates; SMEs debug |
| "Root cause" singular thinking | Most incidents have multiple contributing factors |
| Silent status pages during incidents | Update even if the update is "still investigating" |
| Action items without owners or deadlines | Every action item gets a name and a date |
| Blameless *language* over a blame-shaped narrative ("blame laundering") | Write timeline entries as "the system/process allowed X," not "X did Y" — see Judgment Calls |
| Action items logged but never revisited ("action-item graveyard") | Track action-item close rate as its own metric, separate from postmortem completion rate |

## Regulatory Reporting Overlays

Some incidents trigger a legal reporting clock in addition to the operational response above. This skill covers the operational process only — it does not draft regulatory filings or make materiality/severity determinations that carry legal weight; route those to legal/compliance or outside counsel. Verify current thresholds locally before relying on any of this table, since regulators amend timelines and technical standards.

| Regime | Applies to | Clock starts at | Cascade | Note |
|--------|-----------|-----------------|---------|------|
| EU DORA, Article 19 | EU-regulated financial entities, major ICT-related incidents | Classification as "major" (24-hour backstop from detection if classification is delayed) | 4h initial notification, 72h intermediate report, 1 month final report | Templates harmonized by RTS 2025/301 and ITS 2024/2956 (confirmed 2026-07-11) |
| EU NIS2, Article 23 | Essential/important entities in scope | Awareness of a "significant" incident (not classification) | 24h early warning, 72h incident notification, 1 month final report | Clock starts on awareness, not on internal severity classification — do not conflate with DORA's classification-triggered clock |
| US SEC Item 1.05 (Form 8-K) | US public companies, material cybersecurity incidents | The company's own determination that the incident is material (not discovery) | File within 4 business days of the materiality determination | Materiality determination itself must be made "without unreasonable delay"; an incident can be disclosed first under Item 8.01 before a materiality call is made |

**Judgment note.** These three clocks start at different triggers (classification vs. awareness vs. materiality determination) — an IC who assumes "detection" starts all three clocks will misreport the timeline to legal. Flag any incident with plausible regulatory exposure (financial-services ICT outage, personal-data exposure, anything a reasonable investor might consider material) to legal/compliance during triage, not after resolution — the reporting clock can start before the incident is even mitigated.

## Navigation

### References

- [runbook-design-guide.md](references/runbook-design-guide.md) — How to write effective on-call runbooks
- [on-call-practices.md](references/on-call-practices.md) — On-call rotation, escalation, and fatigue management
- [postmortem-facilitation.md](references/postmortem-facilitation.md) — Running blameless postmortems (includes Howie standard for SEV1/SEV2)
- [incident-metrics-guide.md](references/incident-metrics-guide.md) — MTTD/MTTR phases + percentile-based alternatives (MTTx distributional caveat)
- [slo-incident-triggering.md](references/slo-incident-triggering.md) — Error-budget burn rate as incident trigger; burn rate → severity mapping; postmortem prioritization by budget remaining
- [references/control-theory-applied.md](references/control-theory-applied.md) — Control-theory applied recipes for incident response: stable autoscaler retune, cascading-failure containment, recovery throttling.
- [references/decision-theory-applied.md](references/decision-theory-applied.md) — Decision-theory applied recipes for incident response: paging thresholds via EU, rollback as real option, MAB runbook ordering.

### Assets

Use these as copy-paste starters; fill placeholders before sharing with stakeholders.

- [incident-channel-template.md](assets/incident-channel-template.md) — Use at **T+0** when opening a SEV1/SEV2 incident channel; post as the first pinned message to assign roles and set next-update time.
- [postmortem-template.md](assets/postmortem-template.md) — Use at **incident close** to create the postmortem document; populate title, severity, IC, and timeline start immediately (do not wait until the writing session).
- [runbook-template.md](assets/runbook-template.md) — Use when **authoring or reviewing** a service runbook; also reference during triage to confirm runbook coverage gaps as action items.

### Related Skills

| Skill | Relationship |
|-------|--------------|
| [ops-devops-platform](../ops-devops-platform/SKILL.md) | Infrastructure, CI/CD, deployment automation |
| [qa-resilience](../qa-resilience/SKILL.md) | Application-level fault tolerance patterns |
| [qa-observability](../qa-observability/SKILL.md) | Monitoring, alerting, SLI/SLO setup |
| [qa-debugging](../qa-debugging/SKILL.md) | Systematic debugging during incidents |
| [software-security-appsec](../software-security-appsec/SKILL.md) | Security incident handling |

## Fact-Checking

- Verify current severity definitions, escalation targets, status-page policy, and postmortem requirements against the team's actual runbooks.
- Use the local on-call docs and paging configuration as the source of truth before final recommendations.
- If current internal runbooks are unavailable, state the assumption and mark placeholders clearly.
- **Tooling landscape moves fast — verify before naming a vendor.** Confirmed as of 2026-07-11: Freshworks closed its acquisition of FireHydrant (Jan 1, 2026; FireHydrant now sits inside the Freshservice portfolio); Grafana archived the Grafana OnCall OSS project (Mar 24, 2026) and now points teams to Grafana Cloud IRM (which merges OnCall + Incident); PagerDuty is retiring the standalone Jeli UI (EOL Dec 22, 2026) and folding Howie-based post-incident reviews into PagerDuty's native product, though the Howie methodology itself is unaffected; Atlassian stopped new Opsgenie sales (Jun 4, 2025; support ends Apr 5, 2027). incident.io, Rootly, and PagerDuty remain independent. Do not assume any tool name in this skill or its assets is still the current market leader without a fresh check — this list itself will age.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.


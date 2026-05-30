---
name: blameless-postmortem
description: Google SRE-style blameless postmortem authoring. Structure, timeline construction, contributing-factor extraction, action-item discipline, and the cultural practices that make postmortems produce learning rather than theater. Use when writing a postmortem after an incident, reviewing a draft postmortem, running a postmortem review meeting, building a postmortem template, or teaching a team how to write postmortems that actually improve the system. Complements rca-human-factors (for the "why people did what they did" analysis) and the rca-classical-methods / rca-systems-theoretic / rca-causal-inference / rca-distributed-systems skills (which supply the investigation techniques that populate the postmortem's analysis section).
type: skill
category: rca
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/rca/blameless-postmortem/SKILL.md
superseded_by: null
---
# Blameless Postmortems

A postmortem is the work product that converts an incident from a surprise into learning. A *blameless* postmortem does this without punishing the people closest to the incident — not because punishment is wrong in principle, but because punishment destroys the reporting culture that makes further learning possible.

This skill teaches you how to write one.

## The two purposes of a postmortem

1. **Learning** — teach the organization something it didn't know about itself, so the same incident or its close cousins don't recur.
2. **Accountability** — commit the organization to a specific set of changes with owners and deadlines.

These are not competing purposes. They are complementary: learning without accountability is a reading exercise; accountability without learning is theater.

A postmortem that fails either purpose is a bad postmortem, regardless of how polished it looks.

## Why "blameless"?

Google's SRE book (Beyer et al., 2016, Chapter 15) articulates the principle: *you cannot fix what you cannot see, and people will not show you what they did if they believe they will be punished for it*. Blameless postmortems are a deliberate organizational choice to prioritize visibility over retribution.

The principle is not "no one is ever held accountable." The principle is: the postmortem document and the review meeting are protected space. Accountability decisions, if any, happen in a separate process that cannot use the postmortem against the author. This is Just Culture in organizational form (see `rca-human-factors` for the algorithm).

### What blameless is not

- Not "we don't name who did what." You still describe actions, with names or roles, factually.
- Not "we don't assign action items." You assign many, with owners.
- Not "we avoid uncomfortable truths." You surface them, in language that reveals system design rather than attacking people.
- Not "we let everything go." Reckless behavior is still addressed — outside the postmortem channel.

## The Google SRE postmortem template

The canonical template has nine sections. Adopt it as a starting point; variations are fine as long as each purpose is served.

### 1. Title

A short, factual description. "Checkout 500s for 42 minutes on 2026-04-09" — not "catastrophic failure" or "minor glitch."

### 2. Status

Where the postmortem is in its lifecycle:

- **Draft** — under construction, incomplete
- **In review** — ready for the review meeting
- **Finalized** — review complete, action items assigned
- **Closed** — all action items complete

### 3. Summary

One paragraph, 3–5 sentences. A reader who reads only this should know: what failed, how long it failed, how many users were affected, what we think caused it, and what we're doing about it.

### 4. Impact

Quantified impact:

- Users affected (count, percentage, region, tier)
- Duration (time to detect, time to mitigate, time to resolve)
- Error budget consumed (percentage of monthly budget)
- Financial impact (if known)
- Business impact (customer trust, SLA breach, missed deadlines)

Do not inflate or deflate impact. Be specific.

### 5. Timeline

Minute-by-minute chronological reconstruction. Every timestamp is UTC. Every entry names the actor (person, system, or both).

```
2026-04-09 14:32 UTC — Deploy deploy-4827 begins (on-call: A. Smith)
2026-04-09 14:34 UTC — Canary metrics show 3x error rate (automated alert to #alerts-checkout)
2026-04-09 14:34 UTC — Smith acknowledges alert, begins investigation
2026-04-09 14:36 UTC — Smith pages #oncall-sre (SEV2 declared)
2026-04-09 14:38 UTC — B. Jones joins, confirms deploy-4827 is the trigger
2026-04-09 14:40 UTC — Smith initiates rollback via deploy dashboard
2026-04-09 14:43 UTC — Rollback completes, error rate begins dropping
2026-04-09 14:46 UTC — Error rate returns to baseline
2026-04-09 14:50 UTC — SEV2 downgraded, incident declared resolved
2026-04-09 15:15 UTC — Ad-hoc incident review in war room (15 min)
2026-04-09 17:00 UTC — Postmortem draft started by A. Smith
```

### 6. Root cause and contributing factors

This section is where the investigation techniques from other RCA skills land. Name the proximate cause, then the contributing factors, then the latent conditions. Avoid saying "the root cause was human error" — that's a symptom, not a finding.

Example structure:

**Proximate cause:** deploy-4827 contained an incorrect SQL query in the `checkout/order.py` module that returned an empty result set on the fast path, triggering a NULL pointer exception in the downstream handler.

**Contributing factors:**
1. The test suite did not cover the empty-result-set case for this query.
2. The canary deploy window was 90 seconds — not long enough for the full traffic distribution to reach the new version.
3. The downstream handler's null-check had been removed in a refactor in January as part of a "dead code" cleanup; the defensive code was not actually dead.
4. The alert threshold was set to 3x baseline error rate, which delayed detection by ~90 seconds versus a 2x threshold.

**Latent conditions:**
1. The codebase does not enforce empty-result-set testing in code review. Similar queries elsewhere in the codebase likely share this gap.
2. Canary windows are configured per-service and were not revisited when traffic patterns changed.
3. The "dead code" refactor process does not currently include a step to verify that removed defenses are genuinely unreachable.

### 7. Resolution

What was done to mitigate the incident and when it completed. Include the immediate remediation and any follow-up actions already completed by the time the postmortem is written.

### 8. Lessons learned

Three categories:

- **What went well.** Praise specific effective actions. This is not ceremonial — it's feedback that the organization should keep doing these things.
- **What went wrong.** The things that didn't go well. Not blame — facts.
- **Where we got lucky.** The near-misses that could have been worse. This is where you find latent hazards.

Example:

> **What went well**
> - Canary alerting fired within 2 minutes of deploy.
> - Rollback was initiated within 6 minutes of detection.
> - Communication in #incident-checkout was clear and structured.
>
> **What went wrong**
> - The empty-result-set case was not covered by tests, despite the query change.
> - The downstream null-check had been removed and nobody realized the defense was load-bearing.
> - The initial severity call was SEV3 and was upgraded to SEV2 only after pager escalation.
>
> **Where we got lucky**
> - The deploy was mid-week during low traffic. At peak Friday load, the 12 minutes of errors would have affected ~8x more users.
> - The rollback worked cleanly; it was tested in staging 3 days before the incident. Had the rollback failed, recovery would have required a forward-fix under pressure.

### 9. Action items

A table of specific, assigned, deadlined actions. Each row:

```
| ID | Owner  | Action                                                | Priority | Due        | Status |
|----|--------|-------------------------------------------------------|----------|------------|--------|
| 1  | A.S.   | Add empty-result-set test coverage to checkout queries| P0       | 2026-04-16 | open   |
| 2  | B.J.   | Audit recent "dead code" removals for load-bearing   | P1       | 2026-04-30 | open   |
|    |        | defenses in checkout, orders, payments               |          |            |        |
| 3  | Team   | Lower canary error threshold from 3x to 2x           | P1       | 2026-04-20 | open   |
| 4  | Team   | Extend canary window from 90s to 300s for checkout   | P1       | 2026-04-20 | open   |
| 5  | A.S.   | Propose code-review checklist update for              | P2       | 2026-05-15 | open   |
|    |        | empty-result-set handling                             |          |            |        |
```

### Action item discipline

Action items are the postmortem's contract with the organization. If they don't close, the postmortem failed.

- Every action item has a single owner (a person, not "the team").
- Every action item has a due date (absolute, not "next sprint").
- Every action item has a priority (P0–P3, matching your normal work).
- Actions enter the normal work-tracking system, not a separate postmortem tracker.
- A weekly cadence checks action-item closure across open postmortems.
- Stale action items are re-reviewed and either resurrected or closed as won't-do with justification.

## The postmortem review meeting

The meeting is 30–60 minutes, attended by:

- Author (the person who drafted it, usually the primary incident responder)
- A facilitator (someone not involved in the incident)
- People named in the timeline (invited, not required)
- Engineers familiar with the affected service (to fact-check)
- A representative from the SRE / reliability function (for cross-incident patterns)

### Meeting agenda

1. **Read-along.** The facilitator reads the postmortem aloud or projects it. Attendees comment as the narrative unfolds.
2. **Timeline validation.** Fact-check each timestamp. Are we missing steps? Are times accurate?
3. **Root-cause discussion.** Does the narrative support the conclusion? Are there alternative explanations? Is the contributing-factors list exhaustive?
4. **Lessons-learned discussion.** What would the team change next time?
5. **Action-item review.** Is each action owned, specific, and due?
6. **Close.** Set a review date to check action-item closure.

### Facilitator responsibilities

- Protect the blameless frame. Intervene if language drifts toward blame.
- Push for specificity. "Better monitoring" is not an action item.
- Surface uncomfortable truths gently but firmly.
- Keep the meeting moving. Park tangents.

## Postmortem review cadence

An incident without a reviewed and finalized postmortem is not yet complete. Most mature organizations:

- Draft within 48 hours of incident resolution.
- Review within 1 week of draft completion.
- Finalize within 2 weeks.
- Track open action items weekly.
- Revisit at 30, 60, 90 days to confirm learning is being absorbed.

Incidents above a severity threshold get reviewed at a regular forum (weekly SRE review, monthly company-wide). Patterns across incidents are identified and surfaced.

## Anti-patterns

### "The outage was caused by a bug."

Every outage has a proximate cause that looks like a bug. Stopping there misses the latent conditions that allowed the bug to reach production and cause the impact it did. Recovery: keep asking "why was this bug not caught before it hit production?" until you reach actionable system-design conclusions.

### "We'll add monitoring."

The most common action item. Almost always a band-aid. If your monitoring was inadequate, say *specifically* what metric, threshold, or alert is missing. "We'll add monitoring" cannot be marked complete because it has no definition of done.

### "We'll write a runbook."

Runbooks are good. But "we'll write a runbook" as a postmortem action almost never produces a useful runbook because there's no specification of what the runbook must contain. Recovery: specify the exact runbook sections required and the scenarios it must cover.

### "The author was too junior to detect this."

If the finding is "the author of the change didn't know X," the action must be to change the process such that *nobody* has to know X to avoid the incident — not "train the author." A system that requires specific knowledge to be safe is already broken.

### "It was a one-in-a-million event."

One-in-a-million events happen regularly at scale. If your system is handling a million events per day, that's an incident a day of "one-in-a-million" events. The probability framing is a red flag that the investigation stopped too early.

### "The postmortem was filed."

Filing is not learning. A postmortem that isn't discussed, isn't referenced, and whose action items aren't tracked adds nothing to the organization. Measure postmortem effectiveness by action-item closure rate and by whether incidents of the same type recur.

## Integration with other RCA skills

The postmortem is the delivery format; the investigation is upstream. Use this skill to structure the *document*, and use the investigation skills to populate the *content*:

| Use when… | Investigation skill |
|---|---|
| Incident is linear, single-cause | `rca-classical-methods` (5 Whys + Fishbone) |
| Incident involves multiple actors and feedback loops | `rca-systems-theoretic` (CAST, STPA) |
| Incident has rich observational data, you want quantitative causal claims | `rca-causal-inference` |
| Incident involves crew, clinicians, or operators | `rca-human-factors` |
| Incident is in a microservice mesh | `rca-distributed-systems` |

## Cultural prerequisites

Blameless postmortems fail in organizations that don't support them culturally. Prerequisites:

- **Leadership publicly models it.** Leaders run their own postmortems on their own mistakes in public.
- **No performance review linkage.** Postmortem content cannot appear in performance reviews.
- **Legal protection.** Internal documents are protected where legally possible.
- **Time is allocated.** Engineers are not expected to write postmortems on their own time.
- **Action items are tracked as work.** Action items count toward capacity planning, not as extra unpaid labor.

Without these, the blameless frame is a veneer and the pre-blameless dynamics reassert themselves.

## Checklist before finalizing a postmortem

- [ ] Title is factual and specific.
- [ ] Summary fits in five sentences and covers what/when/why/fix.
- [ ] Impact is quantified: users, duration, error budget.
- [ ] Timeline is UTC, actor-labeled, and complete from detection through resolution.
- [ ] Proximate cause is distinguished from contributing factors and latent conditions.
- [ ] Lessons learned include "what went well" and "where we got lucky," not only "what went wrong."
- [ ] Every action item has an owner, priority, and due date.
- [ ] Language is blame-free: describes actions and decisions, not character.
- [ ] The postmortem has been reviewed by someone not involved in the incident.
- [ ] Action items have entered the normal work-tracking system.

## References

- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.). (2016). Chapter 15: Postmortem Culture: Learning from Failure. In *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly.
- Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., & Thorne, S. (Eds.). (2018). *The Site Reliability Workbook*. O'Reilly.
- Allspaw, J. (2012). Blameless postmortems and a just culture. *Code as Craft*, Etsy Engineering Blog.
- Marx, D. (2001). *Patient Safety and the "Just Culture": A Primer for Health Care Executives*. Columbia University.
- Dekker, S. (2014). *The Field Guide to Understanding "Human Error"* (3rd ed.). Ashgate.
- Lunney, B., & Lueder, R. (2021). *Learning from Incidents in Software*. Self-published (learningfromincidents.io).

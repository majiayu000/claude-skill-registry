---
name: stakeholder-communication
description: Stakeholder identification, communication planning, and facilitation for project teams. Covers power/interest grid mapping, communication plans (audience, frequency, channel), status reporting (RAG, earned value, burn charts), RACI matrices, meeting facilitation, conflict resolution, change management (Kotter's 8 steps), psychological safety (Edmondson), managing up, and remote/distributed team communication. Integrates GSD's "docs are the story" principle as a communication strategy.
type: skill
category: project-management
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/project-management/stakeholder-communication/SKILL.md
superseded_by: null
---
# Stakeholder Communication

Projects do not fail because of technology. They fail because of people — miscommunication, misaligned expectations, unresolved conflicts, invisible stakeholders who emerge at the worst moment with the power to block everything. Communication is the connective tissue of project management. Without it, a technically perfect project delivers the wrong thing to the wrong people at the wrong time.

Simon Sinek's insight applies directly: people don't buy *what* you build, they buy *why* you build it. A status report that says "Sprint 7 complete, 34 points delivered" communicates nothing to an executive who needs to know "Are we going to make the Q3 launch?" The same information, framed differently, serves different audiences. This skill covers the frameworks for identifying who needs what, building communication plans, running effective meetings, resolving conflicts, and managing organizational change.

**Agent affinity:** sinek (pedagogy/leadership, "Start With Why"), brooks (organizational dynamics, communication overhead)

**Concept IDs:** bus-stakeholder-theory, bus-corporate-governance, bus-business-ethics, crit-argument-construction, crit-evidence-evaluation

## Stakeholder Identification and Mapping

### The Power/Interest Grid

Classify stakeholders along two dimensions:

- **Power:** Ability to influence project decisions, resources, or outcomes
- **Interest:** How much the stakeholder cares about the project's outcome

| | High Interest | Low Interest |
|---|---|---|
| **High Power** | **Manage Closely** — Key players. Regular engagement, involve in decisions. | **Keep Satisfied** — Dangerous if surprised. Periodic high-level updates. |
| **Low Power** | **Keep Informed** — Enthusiastic supporters or worried users. Regular updates, feedback channels. | **Monitor** — Minimal effort. Available information if they seek it. |

### Worked Example — E-Commerce Platform Rewrite

| Stakeholder | Power | Interest | Strategy |
|---|---|---|---|
| VP of Engineering | High | High | Manage closely — weekly 1:1, involved in architecture decisions |
| CFO | High | Low | Keep satisfied — monthly cost summary, flag budget variances early |
| Customer support team | Low | High | Keep informed — sprint demos, early access to staging |
| Legal/compliance | High | Medium | Keep satisfied — notify on data handling changes, PII flow reviews |
| End users (beta group) | Low | High | Keep informed — changelog emails, feedback survey per release |
| Marketing team | Medium | Medium | Keep informed — feature announcements 2 weeks before launch |
| Infrastructure team (DevOps) | Medium | High | Manage closely — daily standups, shared Kanban board |
| Board of directors | High | Low | Keep satisfied — quarterly executive summary |

**Hidden stakeholders.** The most dangerous stakeholders are the ones you did not identify. Common hidden stakeholders: security/audit teams (veto power over production deployment), data protection officer (GDPR implications), downstream service owners (API contract changes), executive assistants (gatekeepers to executive time).

### Salience Model (Mitchell, Agle, Wood)

For more nuanced classification, the salience model uses three attributes:

- **Power:** Ability to impose will
- **Legitimacy:** Perceived appropriateness of the stakeholder's involvement
- **Urgency:** Time sensitivity of the stakeholder's claim

Stakeholders with all three attributes are **definitive** — they require immediate, full engagement. Stakeholders with two are **expectant** — they will escalate if ignored. Stakeholders with one are **latent** — they may emerge as expectant if conditions change.

## Communication Planning

### The Communication Matrix

For each stakeholder or stakeholder group, define:

| Element | Question |
|---|---|
| **Who** | Which stakeholder or group? |
| **What** | What information do they need? |
| **When** | How frequently? Triggered by what events? |
| **How** | Channel: email, meeting, dashboard, Slack, document? |
| **Why** | What decision or action does this communication enable? |

### Worked Example — Communication Plan

| Who | What | When | How | Why |
|---|---|---|---|---|
| VP Engineering | Sprint progress, blockers, risks | Weekly (Friday) | 15-min 1:1 + written summary | Resource allocation, escalation decisions |
| CFO | Budget vs. actual, forecast to complete | Monthly | Email with 1-page dashboard | Budget approval, investment decisions |
| Dev team | Sprint goals, dependencies, blockers | Daily | 15-min standup | Synchronization, impediment removal |
| Customer support | Upcoming features, known issues | Per sprint | Demo + release notes | Prepare for customer inquiries |
| End users (beta) | New features, bug fixes | Per release | Changelog email + in-app notification | Feedback collection, adoption |
| Board | Project status (RAG), strategic alignment | Quarterly | 2-slide executive summary | Strategic governance |

### Channel Selection

**Rich channels** (face-to-face, video call) for: ambiguous topics, conflict resolution, relationship building, bad news.

**Lean channels** (email, documents, dashboards) for: routine updates, reference information, audit trails, asynchronous consumption.

**Brooks's communication overhead.** In *The Mythical Man-Month*, Brooks showed that communication paths grow as n(n-1)/2 for n people. A team of 5 has 10 communication paths; a team of 10 has 45. This is why Scrum limits team size and why communication planning becomes critical as organizations scale. Every person added to a project increases communication cost quadratically.

## Status Reporting

### RAG Status (Red/Amber/Green)

The simplest and most widely understood status format:

- **Green:** On track. No action needed.
- **Amber:** At risk. Mitigation underway. Needs attention.
- **Red:** Off track. Requires immediate intervention or escalation.

**RAG rules:**
- Never report Green when you know Amber is coming next week. Report Amber now with "trending toward Green" or "trending toward Red."
- A status that has been Amber for 4 consecutive weeks is effectively Red — the mitigation is not working.
- Red is not a failure; it is an honest signal. Punishing Red reports guarantees dishonest Green reports.

### Worked Example — Sprint Status Report

```
Project: Commerce Platform Rewrite
Sprint: 7 of 12
Date: 2026-04-10
Overall: AMBER

Schedule: GREEN — 34/36 points delivered (94%)
Scope: AMBER — Payment gateway integration blocked by vendor API delay.
         Vendor committed to API delivery by April 15. If missed, checkout
         feature slips to Sprint 9. Contingency: mock API for continued
         development.
Quality: GREEN — 0 P1 defects. 3 P3 defects in backlog. Test coverage 87%.
Budget: GREEN — $142K spent of $200K budget. Forecast: $185K at completion.

Key decisions needed:
1. Approve contingency plan for payment API delay (VP Engineering by April 12)
2. Confirm beta user group expansion to 500 users (Product Owner by April 14)

Risks surfaced this sprint:
- R07: Payment API documentation incomplete (NEW, Score: 12)
- R03: Staging environment — RESOLVED (provisioned April 8)
```

### Earned Value Management (EVM)

EVM provides objective, quantitative project status by comparing planned work to completed work and actual cost.

**Core metrics:**
- **PV (Planned Value):** Budgeted cost of work scheduled. What you *planned* to have done by now.
- **EV (Earned Value):** Budgeted cost of work performed. What you *actually* have done, valued at planned rates.
- **AC (Actual Cost):** Actual cost of work performed. What it *actually cost* to do what you did.

**Derived metrics:**
- **SPI (Schedule Performance Index) = EV / PV.** SPI < 1 means behind schedule.
- **CPI (Cost Performance Index) = EV / AC.** CPI < 1 means over budget.
- **EAC (Estimate at Completion) = BAC / CPI.** Forecasts total project cost based on current efficiency.

**Worked example.**

| Metric | Value | Interpretation |
|---|---|---|
| BAC (Budget at Completion) | $200,000 | Total project budget |
| PV (end of Sprint 7) | $117,000 | Should have completed 58.5% of scope |
| EV (end of Sprint 7) | $108,000 | Actually completed 54% of scope |
| AC (end of Sprint 7) | $112,000 | Spent $112K to achieve 54% |
| SPI | 0.92 | 8% behind schedule |
| CPI | 0.96 | 4% over budget |
| EAC | $208,333 | Forecasted overrun of $8,333 |

**Translation for the CFO:** "We are slightly behind schedule and slightly over budget. At current rates, we'll overshoot by about $8K. The payment API delay is the primary driver. If resolved by April 15, we expect to recover the schedule variance by Sprint 9."

### Burn Charts

**Burn-down chart.** Shows remaining work over time. The Y-axis is remaining story points (or tasks); the X-axis is time (days within a sprint, or sprints within a release). A healthy burn-down trends toward zero by the sprint end.

**Burn-up chart.** Shows completed work and total scope over time. Two lines: scope (total work) and completed (done). The gap between them is remaining work. Burn-up charts reveal scope changes — if the scope line keeps rising, the project is absorbing more work than planned.

**Cumulative flow diagram (CFD).** Shows the total number of items in each state (To Do, In Progress, Done) over time. The vertical distance between bands represents WIP; the horizontal distance represents lead time. A widening "In Progress" band signals a bottleneck.

## RACI Matrix

Defines roles for each deliverable or decision:

- **R**esponsible — Does the work
- **A**ccountable — Ultimately answerable (one person per item)
- **C**onsulted — Provides input before the decision
- **I**nformed — Notified after the decision

### Worked Example — Feature Delivery RACI

| Activity | Dev Lead | Product Owner | QA Lead | Architect | VP Eng |
|---|---|---|---|---|---|
| User story definition | C | A/R | C | I | I |
| Technical design | A/R | I | C | C | I |
| Implementation | R | I | I | C | I |
| Test planning | C | I | A/R | I | I |
| Sprint demo | R | A | R | I | I |
| Release decision | C | R | C | C | A |

**Common mistakes:**
- Multiple "A" for one item (nobody is accountable)
- No "R" for an item (nobody does the work)
- Everyone is "C" on everything (decision-by-committee; nothing gets decided)

## Meeting Facilitation

### The Meeting Tax

Every meeting costs: (number of attendees) x (duration) x (average hourly rate). A 1-hour meeting with 8 people at $75/hour costs $600. If the meeting could have been an email, that $600 was waste (Lean principle 1: eliminate waste).

### Meeting Hygiene

1. **Purpose.** Every meeting has a stated purpose. If you cannot articulate it in one sentence, cancel the meeting.
2. **Agenda.** Distributed in advance. Timed sections. Clear outcomes for each section: decision, information, or brainstorm.
3. **Attendees.** Only people who are R, A, or C on the agenda items. Everyone else gets notes afterward (I in RACI terms).
4. **Time-box.** Start on time, end on time. If discussion extends, schedule a follow-up rather than holding the room hostage.
5. **Notes and actions.** Who, what, by when. Distributed within 24 hours. Actions tracked in the project tool.

### Facilitation Techniques

**Round-robin.** Go around the room; everyone speaks once. Prevents dominant voices from monopolizing.

**Fist of Five.** Quick consensus check. Everyone holds up 0-5 fingers: 5 = strong support, 3 = can live with it, 1 = serious concerns, 0 = veto. Anything below 3 triggers discussion.

**Parking lot.** Off-topic but valuable items go on a visible list. Addressed after the meeting or in a follow-up session. Prevents tangent spirals without losing ideas.

**Silent writing.** Before discussion, everyone writes their input on sticky notes or a shared doc for 3-5 minutes. Then share. This prevents anchoring to the first speaker's opinion and gives introverts equal voice.

## Conflict Resolution

### Thomas-Kilmann Conflict Modes

| Mode | Assertive | Cooperative | When to use |
|---|---|---|---|
| **Competing** | High | Low | Emergency decisions, non-negotiable standards |
| **Collaborating** | High | High | Important issues where both sides have valid concerns |
| **Compromising** | Medium | Medium | Time-pressured decisions where a quick resolution matters more than an optimal one |
| **Avoiding** | Low | Low | Trivial issues, or when emotions need to cool before productive discussion |
| **Accommodating** | Low | High | When you are wrong, or when the relationship matters more than the issue |

**Default to collaborating** for technical disagreements. "Let's understand both approaches, test both if needed, and decide based on evidence." Competing ("we're doing it my way") and avoiding ("let's not talk about it") both accumulate unresolved tension.

### Worked Example — Architecture Disagreement

**Situation.** The backend lead wants microservices. The frontend lead wants a monolith. The deadline is 3 months.

**Poor resolution (competing).** The architect picks microservices because they outrank the frontend lead. The frontend lead is demoralized and disengaged.

**Better resolution (collaborating).**

1. Both leads present their rationale with specific criteria: deployment frequency, team structure, operational complexity, time to market.
2. The team scores each approach against the criteria.
3. Data reveals: microservices win on deployment independence but lose on time-to-market (need service mesh, API gateway, etc.).
4. Agreed approach: start with a well-structured monolith (modular boundaries, clean interfaces) with a documented migration path to microservices post-launch.
5. Both leads contributed to the decision; neither was overruled.

## Change Management — Kotter's 8 Steps

John Kotter's framework for leading organizational change:

1. **Create urgency.** Why must we change? What happens if we don't? Data, competitor moves, customer pain.
2. **Form a guiding coalition.** Assemble people with power, expertise, credibility, and leadership to drive change.
3. **Create a vision for change.** A clear, compelling picture of the future state. Simple enough to explain in 5 minutes.
4. **Communicate the vision.** Use every channel. Repeat 10x more than you think necessary. Walk the talk — behavior must match the message.
5. **Empower action.** Remove obstacles: organizational structures, processes, systems, and people who block progress.
6. **Create short-term wins.** Visible, unambiguous improvements within 6-12 months. Wins build momentum and silence critics.
7. **Build on the change.** Don't declare victory too early. Use credibility from wins to tackle bigger changes.
8. **Anchor in culture.** Connect the change to organizational success. "This is how we work now."

### Worked Example — Adopting GSD in an Organization

| Step | Action |
|---|---|
| 1. Urgency | "Our last 3 projects missed deadlines by 30-60%. Current processes are not working." |
| 2. Coalition | Engineering director + 2 respected tech leads + PM manager |
| 3. Vision | "Structured phases with autonomous execution. Ship every 2 weeks, not every quarter." |
| 4. Communicate | Demo GSD on a small pilot. Share results weekly. |
| 5. Empower | Give pilot team authority to skip legacy approval gates. |
| 6. Short-term wins | Pilot delivers first feature in 2 weeks vs. typical 8 weeks. |
| 7. Build on change | Expand to 2 more teams. Publish playbook from pilot learnings. |
| 8. Anchor | GSD phases become the standard project template. Handoffs and retrospectives are mandatory. |

## Psychological Safety (Amy Edmondson)

Edmondson's research at Harvard demonstrates that team performance correlates with psychological safety — the belief that one can speak up without punishment. High-performing teams are not error-free; they surface errors faster.

**Observable behaviors in psychologically safe teams:**
- People ask questions without fear of looking stupid
- Mistakes are discussed openly, not hidden
- Team members challenge ideas regardless of hierarchy
- Bad news travels up quickly

**Observable behaviors in psychologically unsafe teams:**
- People stay silent in meetings, then complain in hallways
- Problems are discovered late because nobody raised the alarm
- Status reports are always Green until the project explodes
- Post-mortems find blame, not causes

**Building psychological safety:**
- Frame work as learning problems, not execution problems
- Acknowledge your own fallibility ("I might be wrong about this")
- Model curiosity — ask questions, don't make statements disguised as questions
- Thank people who surface problems early
- Respond to failure with "What can we learn?" not "Whose fault is this?"

**GSD connection.** GSD's blameless session handoffs serve this function. HANDOFF-SESSION-*.md files record what happened honestly without assigning blame. The retrospective pattern (carry-forward from session to session) normalizes learning from mistakes as the default mode. (Cross-reference: retrospective-learning skill.)

## Remote and Distributed Communication

### Challenges

- **Time zones.** A team spanning US Pacific to India has zero overlapping business hours without someone working outside normal hours.
- **Reduced bandwidth.** No body language, no hallway conversations, no whiteboard sketches.
- **Isolation.** Remote workers miss informal context that co-located teams absorb osmotically.
- **Tool fatigue.** Slack + email + Zoom + Jira + Confluence + wiki = context scattered across 6 systems.

### Practices

**Default to asynchronous.** Write it down. Record meetings. Put decisions in documents, not chat. Asynchronous communication respects time zones and creates an audit trail.

**Overlap windows.** Define 2-4 hours per day where all team members are available for synchronous discussion. Protect this window — do not schedule non-team meetings during it.

**Documentation as communication.** GSD's "docs are the story" principle applies directly. If a decision is not written down, it did not happen. STATE.md, HANDOFF documents, and PLAN.md files are communication artifacts — they make invisible work visible to anyone who reads them, regardless of time zone or attendance at the original meeting.

**Camera-optional, presence-required.** Do not mandate cameras (fatigue, bandwidth, privacy). Do require active presence — responses to questions, participation in polls, visible engagement.

## Managing Up

**What managing up means.** Ensuring your manager and leadership have the information they need to support your project. It is not manipulation — it is professional communication directed upward.

**The no-surprises rule.** Bad news must travel up before it becomes a crisis. An executive who learns about a problem from a customer complaint will never forgive the team that hid it.

**Framing for executives:**
- Lead with impact, not detail. "We may miss the Q3 date" not "The Kubernetes ingress controller configuration is incompatible with our TLS termination strategy."
- Present options, not problems. "Option A: reduce scope (low risk, lower value). Option B: extend timeline 2 weeks (medium risk, full value). Option C: add 2 contractors (high cost, high risk). I recommend B."
- Quantify. "80% probability of on-time delivery" not "we think we'll make it."

## When to Use / When NOT to Use

### When to use structured communication planning

- Multiple stakeholders with different information needs
- Distributed or remote teams
- Projects with organizational change impact
- Any situation where "I thought someone told them" has caused problems before

### When NOT to use structured communication planning

- A single developer working on a well-defined task (communicate with yourself via comments and commit messages)
- When the plan becomes more elaborate than the project itself
- When communication plans substitute for actual communication ("We have a RACI matrix, why is nobody talking to each other?")

## Cross-References

- **sinek agent:** Leadership communication, purpose-driven messaging, "Start With Why" framework.
- **brooks agent:** Department chair. Communication overhead scaling (n(n-1)/2), organizational structure as communication constraint (Conway's Law).
- **deming agent:** Quality communication — making processes visible, statistical process control as a communication mechanism.
- **lei agent:** Lean communication — eliminating waste in meetings and handoffs, value stream mapping for information flow.
- **retrospective-learning skill:** Retrospective formats for team reflection, psychological safety practices, organizational learning.
- **risk-management skill:** Risk communication — reporting risks to stakeholders, escalation triggers, risk register as communication artifact.
- **agile-methods skill:** Scrum ceremonies as structured communication (standup, review, retrospective), Kanban boards as visual communication.

## References

- Sinek, S. (2009). *Start With Why*. Portfolio/Penguin.
- Brooks, F. P. (1975/1995). *The Mythical Man-Month*. Addison-Wesley.
- Edmondson, A. C. (2018). *The Fearless Organization*. Wiley.
- Kotter, J. P. (1996). *Leading Change*. Harvard Business Review Press.
- Thomas, K. W. & Kilmann, R. H. (1974). *Thomas-Kilmann Conflict Mode Instrument*. Xicom.
- Mitchell, R. K., Agle, B. R., & Wood, D. J. (1997). "Toward a Theory of Stakeholder Identification and Salience." *Academy of Management Review*, 22(4), 853-886.
- PMI. (2021). *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 7th edition. Project Management Institute.
- DeMarco, T. & Lister, T. (2013). *Peopleware: Productive Projects and Teams*. 3rd edition. Addison-Wesley.

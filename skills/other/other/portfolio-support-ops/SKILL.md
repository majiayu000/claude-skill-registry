---
name: portfolio-support-ops
description: "Run portfolio support like an on-call ops function with measurable outcomes: intake requests, ship intros, recruiting help, board prep, and close-the-loop tracking. Every request gets a resolution and outcome measurement."
license: Proprietary
compatibility: Works offline; improved with operator network; Salesforce logging recommended.
metadata:
  author: evalops
  version: "0.2"
---
# Portfolio support ops

## When to use
Use this skill when:
- A portfolio company asks for help (hiring, customers, partners, strategy)
- You're prepping for a board meeting or quarterly check-in
- You want to systematize support so it compounds over time

## Inputs you should request (only if missing)
- The specific request (what outcome, by when)
- Company stage and immediate priorities
- Target ICP / customer list (if request is GTM)
- Hiring priorities and role specs (if request is recruiting)
- Any constraints (confidentiality, competitor conflicts)

## Outputs you must produce
1) **Clarified request** (what "done" means, measurable)
2) **Action plan** (owner, next step, due date, SLA)
3) **Delivered help** (intros made, candidates sourced, docs delivered)
4) **Close-the-loop note** (did it work? outcome measured)
5) **Updated help menu** (company priorities refreshed)

**Hard rule:** Every request gets a resolution within SLA and an outcome measurement.

Templates:
- assets/help-menu.md
- assets/request-intake.md
- assets/intro-template.md
- assets/board-prep.md

## SLA by request type

| Type | Priority | Response SLA | Resolution SLA | Outcome measurement |
|---|---|---|---|---|
| Fundraising support | P0 | 4 hours | 48 hours | Meetings scheduled, term sheets received |
| Key hire closing | P0 | 4 hours | 1 week | Offer accepted Y/N |
| Customer escalation | P0 | 4 hours | 48 hours | Issue resolved Y/N |
| Customer intro | P1 | 24 hours | 1 week | Intro made, meeting held, outcome |
| Recruiting pipeline | P1 | 24 hours | 2 weeks | Candidates submitted, interviews, hires |
| Partner intro | P1 | 24 hours | 1 week | Intro made, partnership status |
| Strategy/advisory | P2 | 48 hours | 1 week | Deliverable shipped, feedback received |
| Market intel | P2 | 48 hours | 1 week | Report delivered, usefulness rated |

## Procedure

### 1) Build a "help menu" per company (refresh quarterly)

Every portfolio company gets a living doc with:

```markdown
# [Company] Help Menu
Last updated: YYYY-MM-DD

## Current priorities (this quarter)
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Hiring needs
| Role | Ideal profile | Urgency | Status |
|---|---|---|---|
| | | P0/P1/P2 | Open/Filled |

## Customer targets
| Account | Buyer persona | Why they need this | Intro path |
|---|---|---|---|

## Partnership targets
| Partner | Type | Value to company | Status |
|---|---|---|---|

## Key metrics (baseline)
| Metric | Current | Target | Trend |
|---|---|---|---|

## Board meeting schedule
- Next board: [date]
- Materials due: [date]

## Support log (last 5)
| Date | Request | Outcome | Impact |
|---|---|---|---|
```

### 2) Intake requests with structured format

For every request, capture:

| Field | Value |
|---|---|
| Company | |
| Requester | |
| Request type | Hiring / Customer / Partner / Strategy / Fundraising / Other |
| Goal (one sentence) | |
| "Done" looks like | |
| Deadline | |
| Priority | P0 / P1 / P2 |
| Owner | |
| SLA | Response: X hours, Resolution: X days |
| Next step | |
| Constraints | |

### 3) Execute value actions with tracking

**Customer intros (highest leverage):**
1. Confirm the target account and buyer persona
2. Check your network for warm paths (1st degree > 2nd degree > cold)
3. Send structured intro request to connector:
   - Why the match is relevant now
   - What the ask is (15-min chat, design partner, pilot, etc.)
   - Suggested time window
4. Track: Intro made -> Meeting held -> Outcome (pilot/deal/pass)

**Recruiting support:**
1. Confirm role scorecard (must-have vs nice-to-have)
2. Source 10-20 candidate targets (companies + titles)
3. Identify warm paths (your network, portfolio network)
4. Track pipeline weekly:
   - Candidates identified
   - Outreach sent
   - Responded
   - Screened
   - Interviewed
   - Offers
   - Accepted

**Fundraising support:**
1. Review materials (deck, data room)
2. Build target investor list with warm paths
3. Make intros with context (why this investor, why now)
4. Track: Intros made -> Meetings -> Follow-ups -> Term sheets

### 4) Close the loop with outcome measurement

**After every request resolution, document:**

| Field | Value |
|---|---|
| Request ID | |
| Resolution date | |
| Within SLA? | Yes / No |
| Outcome | Success / Partial / Failed |
| Impact | High / Medium / Low |
| Evidence | |
| Founder feedback | |
| Learnings | |

**Impact definitions:**
- High: Directly contributed to revenue, hire, or funding
- Medium: Advanced a priority, saved founder time
- Low: Helpful but not critical path

### 5) Board meeting support

**Before the meeting (1 week out):**
- Review the deck
- Pull 5 questions that matter (not softballs)
- Prepare a 1-page competitive/market update
- Identify 1-2 ways you can help this quarter

**After the meeting (within 48 hours):**
- Capture action items with owners and dates
- Send follow-up with your commitments
- Update help menu based on new priorities

### 6) Quarterly review per company

Every quarter, review:
- Requests handled: count by type
- SLA performance: % within SLA
- Outcomes: % success rate
- Impact: High/Medium/Low distribution
- NPS: Would founder recommend your support?

## Measuring support effectiveness

Track at the fund level:

| Metric | Target | How to measure |
|---|---|---|
| Response SLA hit rate | >90% | % requests responded within SLA |
| Resolution SLA hit rate | >80% | % requests resolved within SLA |
| Outcome success rate | >70% | % requests with Success outcome |
| High-impact rate | >30% | % requests rated High impact |
| Founder NPS | >50 | Quarterly survey |
| Intros -> meetings | >60% | % intros that result in meeting |
| Candidates -> interviews | >20% | % sourced candidates interviewed |

## Salesforce logging (recommended)

Track portfolio support in Salesforce via Activities on the Account:
- Log each support request as a Task (open until resolved)
- Log each action (intro, candidate submission) as an Activity
- Tag by type: hiring / customer / partner / strategy / fundraising
- Record outcome and impact in Activity notes
- Link to Contacts for intros made

If you need API workflows, use `salesforce-crm-ops`.

## References
- Mark Suster has useful public writing on boards and how they function in practice.

## Edge cases
- If the ask is vague: ask "What does success look like next week?" before proceeding.
- If you can't help quickly: provide an alternative (another operator, another firm, or a small experiment) within SLA.
- If the founder doesn't close the loop: proactively check in at resolution SLA deadline.

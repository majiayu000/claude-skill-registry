---
name: signal-sourcing-engine
description: "Run a systematic sourcing engine: network loops, signal harvesting, and thesis-driven outbound. Use when you need to generate proprietary dealflow, keep a pipeline current, or expand coverage."
license: Proprietary
compatibility: Requires web access for research and outreach; Salesforce logging is a hard gate.
metadata:
  author: evalops
  version: "0.2"
---
# Signal sourcing engine

## When to use
Use this skill when you need to:
- Generate new at-bats (companies and founders) in a specific thesis area
- Build a repeatable sourcing system (not ad hoc coffee chats)
- Turn weak signals into qualified founder meetings

## Inputs you should request (only if missing)
- Thesis wedge (or ask for a short description)
- Stage focus + geography constraints (if any)
- How the firm defines a "qualified" first meeting (traction, team, ICP, etc.)
- Existing CRM rules (Salesforce fields/stages) if available

## Outputs you must produce
1) **Sourcing loops** (3 compounding systems, not ad hoc searches)
2) **Signal rubric** (what to watch + how to score)
3) **Weekly pipeline update** (10 new names, 3 meetings, 1 partner-ready candidate)
4) **Monthly network refresh** (top 50 humans + 10 new additions)
5) **Outreach experiments** (2 variants with response tracking)

**Hard gate:** No "qualified" company exists unless there's a Salesforce Account/Lead + next task + owner.

Templates:
- assets/signal-rubric.md
- assets/outreach-templates.md
- assets/weekly-pipeline-update.md

## Cadence and metrics (required)

### Weekly deliverables
- 10 new names added to pipeline
- 3 meetings scheduled or completed
- 1 partner-ready candidate surfaced
- Salesforce updated with all entries

### Monthly deliverables
- Refresh top 50 humans list (remove stale, add emerging)
- Add 10 new humans to network cultivation list
- Review outreach experiments: what's working, what's not
- Update signal rubric based on hit rate

## Procedure

### Loop A: Earned network loop (highest signal, first-class object)
Goal: become "first call" for a cluster of builders and operators.

**Build the system:**
1) Identify 2-3 "talent pools" for the wedge:
   - ex-employee clusters from relevant companies
   - OSS communities (maintainers + power users)
   - buyer/operator communities (CISOs, data eng leads, RevOps, etc.)
2) Build a "Top 50 humans" list with columns:
   - Name, role, company, thesis relevance
   - Last touch date, relationship strength (1-5)
   - Value provided to them, value received
   - Next action + due date
3) Provide small, concrete value before asking for meetings:
   - 1 targeted intro
   - a short market map excerpt
   - a recruiting assist on a specific role
4) Track compounding metrics:
   - Touches -> warm conversations -> referrals -> founder intros
   - Target: 20% of Top 50 should generate a referral per quarter

**Monthly refresh:**
- Review all 50: who's gone stale? Who's risen?
- Add 10 new humans, remove 10 lowest-value
- Log changes in Salesforce (Contacts with "Network" tag)

### Loop B: Signal harvesting loop (volume, disciplined)
Goal: produce a weekly list of candidates worth human qualification.

**Build the system:**
1) Define 8-12 signals tied to the wedge (avoid generic hype).
   Examples:
   - hiring for "founding AE" or "head of sales" (GTM transition)
   - design partners mentioned in job posts
   - OSS adoption with maintainer activity and downstream usage
   - specific buyer pain appearing in forums where buyers complain
2) Score each signal (1-5) for:
   - Relevance to thesis
   - Timeliness
   - Uniqueness (are competitors seeing this too?)
3) Human qualification pass:
   - 10 minutes scan -> 50 names -> 5 worth work -> 1 worth meeting.
4) Log "why" for every pass to improve the rubric.
5) **Weekly output:** 10 new names with signal scores

### Loop C: Thesis-driven outbound loop (precision outreach)
Goal: outreach that feels like "I did the work," not spam.

**Build the system:**
1) Create 2 outreach variants per thesis:
   - Variant A: insight-led ("We mapped this space and noticed...")
   - Variant B: value-led ("We can intro you to [specific customer]...")
2) Track response rates per variant (aim for >20% response, >10% meeting)
3) Rules for every message:
   - Must include: the wedge you believe is emerging
   - Must include: what looks distinct about their approach
   - Must include: a concrete offer (customer intro, operator feedback, recruiting, etc.)
   - If it could be sent to 20 companies with minimal edits, rewrite it.

**Monthly review:**
- Which variant is winning?
- What offers get responses? What offers fall flat?
- Update templates based on data.

## Qualification checklist (first pass)
A candidate is "qualified for a first meeting" if you can answer:
- Who buys? Who uses?
- What changes the buyer's mind?
- What do they replace?
- What proof of pull exists (even weak)?
- What's the likely wedge expansion path?
- **Must be true**: one sentence stating what makes this worth partner time
- **Fastest falsification test**: what's the 1-call test?

## Salesforce logging (MANDATORY GATE)

**Hard rule:** A company does not exist in your pipeline unless it has:
- A Lead (founder contact) or Account (company)
- A next-step Task with owner and due date
- Source field populated (Loop A/B/C)

Minimum fields to capture:
- Source (Loop A/B/C)
- Thesis tag / segment
- Signal score (1-5)
- Must be true (one sentence)
- Next step + due date
- Status (meet / watch / pass)
- Pass reason (if passing) + "what would change our mind"

Use `salesforce-crm-ops` for API logging patterns.

## Examples
- Input: "Source seed-stage AI security posture management."
- Output: Top 50 humans list with refresh schedule, 10 new names this week (all in Salesforce), 5 outreach targets with 2 variants, 2 warm intros, weekly metrics (3 meetings, 1 partner-ready), outreach experiment results.

## Edge cases
- If signals are noisy: tighten wedge and require buyer clarity before meetings.
- If outbound response is low: your offer is not concrete enough; fix the offer, not the subject line.
- If you can't log to Salesforce: stop and fix the integration before continuing. No exceptions.

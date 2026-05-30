---
name: signal-scanner
description: "Use when searching for buying signals, detecting intent data, scoring prospect readiness, or monitoring accounts for trigger events. Triggers: 'scan for signals', 'find buying signals', 'who is ready to buy', 'intent signals', 'signal scoring', 'account signals'."
version: 1.0.0
---

# Signal Scanner

Detect, score, and prioritize buying signals for target accounts. This skill searches for live signals using WebSearch, scores them on a Fit x Timing x Access x Intent framework, and produces a prioritized action list for GTM teams.

## Tools Used

- **WebSearch** — find real-time signals (funding, hiring, product launches, etc.)
- **Read** — load `docs/icp.md` if it exists (output from the ICP Architect skill)
- **Write** — save per-company signal reports and summary
- **Glob** — check for existing signal files to avoid duplicate work

## Methodology

Follow these steps in order. Do not skip steps. Do not fabricate data.

### Step 1: Context Loading

Check if `docs/icp.md` exists using Glob.

**If it exists:** Read it. Extract ICP segments, buyer personas, and known buying signals. Summarize what you loaded so the user can confirm.

**If it does not exist:** Ask the user three questions before proceeding:

1. What does your company sell? (one sentence)
2. Who is your ideal buyer? (title, company size, industry)
3. What signals indicate someone needs your solution? (list 3-5)

Wait for answers. Do not assume.

### Step 2: Signal Taxonomy

Present the full taxonomy of 20 signal types across 4 categories. Ask the user to select 8-12 that are most relevant to their business. Only scan for the selected signal types in Step 3.

#### Company-Level Signals
1. **Fundraise announcement** — Seed, Series A, B, C+ rounds
2. **Leadership change** — New CXO, VP Sales, VP Marketing, Head of Growth
3. **Hiring pattern** — SDR hiring spree, GTM engineering roles, marketing hires
4. **Product launch** — Major feature release, new product line, GA announcement
5. **Partnership or integration** — New tech partner, channel partner, integration announcement
6. **Tech stack change** — Detected via job postings, BuiltWith, Wappalyzer, or press releases
7. **Office expansion** — New market entry, new office location, international expansion
8. **Pricing change** — New tier launch, pricing model shift, free tier added/removed

#### Engagement Signals
9. **Website visit** — If tracking pixel is deployed (user must confirm)
10. **Content download or webinar attendance** — Known engagement with your content
11. **G2/Capterra review activity** — Wrote a review of a competitor product
12. **Community activity spike** — Mentions on Reddit, LinkedIn, Slack, or forums about your problem space
13. **Email engagement** — Opens, clicks, replies on existing sequences (user must confirm)

#### Market Signals
14. **Competitor customer churn** — Switching signals, public complaints, cancellation posts
15. **Industry regulation change** — New compliance requirement that creates demand
16. **Market event or conference** — Speaking at or attending events in your space
17. **Competitor funding or acquisition** — Creates urgency or uncertainty for their customers

#### Behavioral Signals
18. **Job posting pattern shift** — New role types signal new priorities (e.g., first "Head of AI" hire)
19. **Social selling activity** — Prospect sharing or engaging with content about your problem space
20. **Direct inquiry or demo request** — Inbound interest (user must confirm)

**Ask the user:** "Which of these 20 signal types are most relevant to your business? Select 8-12 by number."

Wait for their selection before proceeding.

### Step 3: Live Signal Scan

Ask the user to provide 1-5 target company names.

For each company, run WebSearch queries for every selected signal type. Use these search patterns:

| Signal Type | Search Queries |
|---|---|
| Fundraise | `"[company] funding"`, `"[company] series"`, `"[company] raises"` |
| Leadership change | `"[company] hires"`, `"[company] appoints"`, `"[company] new CXO/VP"` |
| Hiring pattern | `"[company] careers"`, `"[company] hiring"`, search for their jobs page |
| Product launch | `"[company] launches"`, `"[company] announces"`, `"[company] new feature"` |
| Partnership | `"[company] partners with"`, `"[company] integrates"`, `"[company] integration"` |
| Tech stack change | `"[company] tech stack"`, `"[company] migrates to"`, check job postings for tech requirements |
| Office expansion | `"[company] opens office"`, `"[company] expands to"` |
| Pricing change | `"[company] pricing"`, `"[company] new plan"` |
| G2/Capterra reviews | `"[company] vs [competitor] G2"`, `site:g2.com [company]` |
| Community activity | `"[company] reddit"`, `"[company] [problem-space-keyword]"` |
| Competitor churn | `"switching from [competitor] to"`, `"[competitor] alternative"`, `"leaving [competitor]"` |
| Regulation change | `"[industry] regulation 2026"`, `"[industry] compliance new"` |
| Conference attendance | `"[company] [conference-name]"`, `"[company] speaks at"` |
| Competitor funding | `"[competitor] acquired"`, `"[competitor] funding"` |
| Job posting shift | `"[company] job openings"`, `"[company] head of [role]"` |
| Social selling | `"[decision-maker-name] [problem-space-keyword]"` |

**Rules for this step:**
- Use WebSearch to find REAL signals. Never fabricate data.
- If WebSearch returns nothing for a signal type, record "No signal detected" for that type. Do not invent results.
- Only search within the last 90 days unless the user specifies a different window.
- Record each signal found with: **type**, **date** (as specific as possible), **source URL**, and **details** (one sentence).

### Step 4: Signal Scoring (Fit x Timing x Access x Intent)

Score each company on four dimensions. Each dimension is rated 1-5.

#### Fit (1-5) — How well does this company match the ICP?
| Score | Criteria |
|---|---|
| 5 | Perfect match: right size, industry, stage, and budget |
| 4 | Strong match: 3 of 4 criteria met |
| 3 | Partial match: 2 of 4 criteria met |
| 2 | Weak match: 1 criterion met |
| 1 | No match or insufficient data |

#### Timing (1-5) — How recent/urgent is the strongest signal?
| Score | Criteria |
|---|---|
| 5 | Signal detected in the last 7 days |
| 4 | Signal detected in the last 30 days |
| 3 | Signal detected in the last 90 days |
| 2 | Signal older than 90 days |
| 1 | No timing signal detected |

#### Access (1-5) — Can you reach the decision maker?
| Score | Criteria |
|---|---|
| 5 | Warm intro available (mutual connection willing to introduce) |
| 4 | Mutual connection exists (LinkedIn 2nd degree, shared community) |
| 3 | Cold but contact info known (email, LinkedIn profile found) |
| 2 | Cold, no direct contact info |
| 1 | Gatekeepered, no visible path to decision maker |

#### Intent (1-5) — How strong is the buying intent?
| Score | Criteria |
|---|---|
| 5 | Direct inquiry, demo request, or inbound interest |
| 4 | Competitor review, active evaluation (G2 comparison, "alternatives" search) |
| 3 | Hiring for a role your product replaces or enables |
| 2 | General interest signals (content engagement, community activity) |
| 1 | No intent signal detected |

#### Composite Score and Tier Classification

**Composite Score** = Fit + Timing + Access + Intent (max 20)

| Composite | Tier | Action |
|---|---|---|
| 17-20 | **HOT** | Reach out today. Personalize based on the strongest signal. |
| 13-16 | **WARM** | Add to nurture sequence. Monitor for escalation signals. |
| 9-12 | **COLD** | Monitor weekly. Build relationship through content and community. |
| Below 9 | **PARK** | Not ready. Set a reminder to re-scan in 90 days. |

**Interactive scoring:** Present your suggested scores for Fit and Access, but ask the user to confirm or adjust them. Fit and Access require human judgment (you may not know about warm intros or internal budget data). Timing and Intent are derived from the signal scan data and should be scored by you.

### Step 5: Output

Write two files:

#### Per-Company Report: `docs/signals/{company-name}.md`

Use this structure:

```markdown
# Signal Report: {Company Name}

**Scan Date:** {YYYY-MM-DD}
**Scanned By:** Signal Scanner v1.0.0

## Company Overview

{One-line description of the company, pulled from search results.}

## Signals Detected

| Signal Type | Date | Source | Details |
|---|---|---|---|
| {type} | {YYYY-MM-DD or "~Month YYYY"} | [{source name}]({url}) | {One sentence} |
| ... | ... | ... | ... |

**Signals found:** {count}
**No signal detected:** {list of signal types with no results}

## Scoring Breakdown

| Dimension | Score | Rationale |
|---|---|---|
| Fit | {1-5} | {Why this score} |
| Timing | {1-5} | {Why this score} |
| Access | {1-5} | {Why this score} |
| Intent | {1-5} | {Why this score} |
| **Composite** | **{total}/20** | |

## Tier: {HOT / WARM / COLD / PARK}

## Recommended Action

{Specific next step. Not generic advice. Reference the strongest signal and suggest a concrete outreach angle, message hook, or monitoring action.}
```

#### Summary: `docs/signals/README.md`

If this file already exists, update it. If not, create it.

```markdown
# Signal Scanner — Account Priority Board

Last updated: {YYYY-MM-DD}

## HOT (17-20) — Reach Out Today
| Company | Score | Strongest Signal | Recommended Action |
|---|---|---|---|
| ... | ... | ... | ... |

## WARM (13-16) — Nurture
| Company | Score | Strongest Signal | Recommended Action |
|---|---|---|---|
| ... | ... | ... | ... |

## COLD (9-12) — Monitor
| Company | Score | Strongest Signal | Recommended Action |
|---|---|---|---|
| ... | ... | ... | ... |

## PARK (Below 9) — Re-Scan in 90 Days
| Company | Score | Strongest Signal | Recommended Action |
|---|---|---|---|
| ... | ... | ... | ... |
```

When updating README.md, merge new results with any existing entries. If a company was previously scanned, replace its row with the new data and note the previous score in the details.

## Key Rules

1. **Never fabricate signals.** Every signal must come from a WebSearch result with a real URL. If you cannot find a signal, say "No signal detected."
2. **Always attribute sources.** Every signal row must include a clickable source URL.
3. **Fit and Access are human-confirmed.** Suggest scores, but always ask the user to confirm or adjust before finalizing.
4. **Timing and Intent are data-driven.** Score these based on what the signal scan actually found.
5. **90-day window by default.** Only surface signals from the last 90 days unless the user specifies otherwise.
6. **No more than 5 companies per run.** If the user provides more than 5, batch them and run the highest-priority batch first.
7. **Check for existing reports.** Before scanning, use Glob to check `docs/signals/` for existing reports. If a company was previously scanned, tell the user and ask if they want a fresh scan or want to skip it.
8. **Keep it generic.** This skill works for any B2B company. Do not reference specific internal tools, databases, or vendor accounts.

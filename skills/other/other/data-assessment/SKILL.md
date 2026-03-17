---
name: data-assessment
description: "Assesses whether a business question can be answered with data available in a Bauplan lakehouse. Maps business concepts to tables and columns, checks data quality on the relevant subset, validates semantic fit, and renders a verdict: answerable, partially answerable, or not answerable. Produces a structured feasibility report. Use when a user brings a business question, asks 'can we answer this', wants to know if the data supports an analysis, or before building a one-off analysis or pipeline."
allowed-tools:
  - Bash(bauplan:*)
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Data Assessment

This skill takes a business question and determines whether available data in a Bauplan lakehouse can answer it. The output is a structured feasibility report with a clear verdict.

This skill is read-only. It explores and profiles data but never creates tables, imports data, runs pipelines, or merges branches. 

If the user's request requires writing data, stop and suggest switching to the appropriate skill (safe-ingestion, data-pipeline, etc.).

Use the Bauplan Python SDK for all data operations. Create a working folder called `data-assessment` and iterate on a Python file named `data_assessment.py` inside it.

## When to Use This Skill

Use this skill when:

* A user has a business question and wants to know if the data can answer it
* A user asks "can we figure out X from what we have?"
* A user wants to understand what data is available before committing to an analysis or pipeline
* A user needs to translate business language into concrete tables and columns

Do NOT use this skill for open-ended browsing with no question in mind (use `explore-data`).

## Required Inputs

Before starting, you need:

1. **A business question** (required): The user's question in their own words. If the question is vague, help them sharpen it before proceeding (see Phase 0).
2. **Branch or ref to explore** (required): Ask the user explicitly which branch contains the data they want to assess. Do not silently default to `main` — ask every time, even if `main` is the likely answer.
3. **Namespace** (optional): If the user works in a specific namespace. Default to `bauplan`.

## CRITICAL RULES

1. **Read-only.** Never create tables, import data, run pipelines, or merge branches.
2. **All queries must specify an explicit ref.** Never rely on implicit defaults.
3. **Always use LIMIT and explicit column selection.** No unbounded queries.
4. **Phases are sequential with gates.** Do not skip ahead. If a gate blocks, stop and report.
5. **Distinguish facts from assumptions.** Every finding must be labeled as observed (from a query) or assumed (inferred by the agent). Never present assumptions as facts.
6. **Profile only what matters.** Do not run exhaustive profiling on every column. Profile only the columns that participate in the business question.
7. **Show your work, then ask.** At every decision point where the agent selects, excludes, or interprets data assets, it must present its reasoning to the user and get confirmation before proceeding. Do not commit to choices silently.

## Workflow Overview

```
Phase 0: Decompose the business question
    │
    ⟳  CHECKPOINT: Present decomposition to user, get confirmation
    │
    ▼
Phase 1: Map concepts to data assets
    │
    ⟳  CHECKPOINT: Present ALL tables (candidates + rejected) with reasoning
    ⟳  CHECKPOINT: If multiple columns compete for same concept, ask user to choose
    │
    Gate: critical concepts have no backing → STOP
    │
    ▼
Phase 2: Assess data quality (scoped to the question)
    │
    Gate: critical tables are unusable → STOP
    │
    ▼
Phase 3: Validate semantic fit
    │
    ▼
Phase 4: Render verdict and write feasibility report
    │
    ▼
Handoff: offer to proceed to one-off analysis
```

---

## Phase 0: Decompose the Business Question

**Goal:** Turn the user's question into concrete, checkable components — with the user's active participation. This phase is a conversation, not a form. Stay here until the user has a clear picture of what they're actually asking for.

Before touching any data, parse the business question into:

* **Metric**: What is being measured? ("churn rate," "average fulfillment time," "revenue per region")
* **Grain**: At what level? (per customer, per day, per region)
* **Dimensions**: What do we slice or group by? (region, time period, product category)
* **Time scope**: What period matters? (last quarter, trailing 12 months, since launch)
* **Implicit filters**: Who or what is included? (all customers or only active ones? all orders or only completed?)

Most business questions leave several of these unspecified. **Do not fill gaps silently.** Instead:

1. Identify what the user specified explicitly.
2. List what is unspecified or ambiguous.
3. **Classify each gap as critical or deferrable** (see below).
4. **Present the gaps to the user and ask them to clarify.**

### Critical vs. Deferrable Gaps

Not all gaps are equal. Before moving on, classify each unspecified component:

**Critical gaps** — the analysis cannot proceed without resolving these, even approximately. These include:
* What the **core entity** is (e.g., what counts as a "customer," a "transaction," a "trip")
* What the **metric** actually measures (e.g., does "revenue" mean gross sales or profit?)
* What the **grain** is (per-day vs. per-month changes the entire query shape)

**Deferrable gaps** — these can be resolved later by inspecting what data actually exists. These include:
* Exact column choices when multiple candidates exist (e.g., which of three price columns to use — Phase 1 can surface options)
* Precise filter boundaries (e.g., exact date range — data coverage will constrain this anyway)
* Aggregation details (e.g., whether to use mean or median — can be decided after seeing distributions)

**Rule: Critical gaps must be resolved in Phase 0. Deferrable gaps can become open questions for Phase 1.**

### When the User Says "I Don't Know"

This is the most important moment in the assessment. **Do not move on.** When a user cannot answer a question about their own business question, it means they need help thinking it through — not that the question should be parked.

**Stay in Phase 0 and help them reason through it.** Use their stated role and business context to offer concrete scenarios. The goal is not to give them the answer — it's to help them discover what they actually mean.

Example — the user asks "who are our top customers during bank holidays" and when asked "what is a customer?" they say "I don't know, I need help understanding that":

```
Good question to think through. Since you're in ecommerce, "customer" 
could mean a few different things in your data:

  • A unique email address — simplest, but the same person might 
    use multiple emails
  • An account ID — if your system requires login to purchase
  • A billing name or address — catches cases without accounts, 
    but "John Smith" is ambiguous
  • A device/session — probably too granular for what you want

For "top customers by revenue during bank holidays," the answer 
matters a lot. If someone buys once for $500 under one email and 
once for $300 under another, are they one $800 customer or two 
separate ones?

What does your ecommerce system use as the primary customer 
identifier? If you're not sure, I can look at what identifiers 
exist in the data and show you the options — but I want to make 
sure we know what "same customer" means before I start counting.
```

**Key behaviors when coaching:**
* Use the user's stated role/domain to make examples concrete (an ecommerce manager gets ecommerce examples, not abstract ones)
* Explain why the distinction matters for their specific question (not in general)
* Offer 2–4 concrete options, not open-ended questions
* If the user still can't decide, offer to inspect the data together: "Let me show you what identifier columns exist, and we can decide together." This transitions to a **joint exploration** at the start of Phase 1, not a silent scan.

### Presenting the Decomposition

Once gaps have been addressed (resolved or explicitly deferred with the user's knowledge), present the full decomposition **and confirm the branch**:

```
Before I start exploring, which branch should I look at? 
(Default is main — but if you have a dev branch with newer 
data or different tables, I should use that instead.)
```

**Always ask explicitly. Do not silently default to `main`.** The user may have data on a development branch that isn't on main yet, or main may have stale data. Getting this wrong wastes the entire assessment.

Then present the confirmed decomposition:

```
Here's what we've landed on:

- Metric: total revenue (sum of order values), ranked highest to lowest
- Grain: per customer (using account ID as the identifier)
- Dimensions: ranked list (top N — we said top 20)
- Time scope: all US federal holidays in 2024
- Filters: only completed orders (excluding cancellations and refunds)

Open questions we'll resolve by looking at the data:
- Which revenue column to use (we'll look at what's available)
- Whether "bank holiday" means the day itself or includes 
  the surrounding weekend

Does this capture what you're after?
```

**CRITICAL: Do not proceed past Phase 0 without presenting the decomposition to the user and getting confirmation.** The user must see what you understood and agree before you start scanning data. This is not optional — skipping confirmation is the primary cause of wasted work in downstream phases.

Record the decomposition. It will form the first section of the feasibility report.

**Proceed to Phase 1** once the user has confirmed the decomposition AND all critical gaps are resolved AND the target branch is confirmed. Deferrable gaps can remain as open questions.

---

## Phase 1: Map Concepts to Data Assets

**Goal:** Determine which tables and columns could represent each business concept — and make the selection process fully transparent to the user.

### 1A. Discover ALL tables in scope

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"

# List all tables in the target namespace
tables = list(client.get_tables(ref=ref, filter_by_namespace="bauplan"))
for t in tables:
    print(t.name)
```

Record the complete list. Every table in the namespace is a candidate until explicitly excluded.

### 1B. Triage tables into candidates and non-candidates

For each table, get its schema and row count, then make a quick relevance judgment:

```python
table = client.get_table(table="<table_name>", namespace="bauplan", ref=ref)
fields = [(c.name, c.type) for c in table.fields]
num_records = table.records
```

Classify each table into one of:

* **Strong candidate**: Table name or columns clearly relate to a business concept from Phase 0. State which concept and why.
* **Weak candidate**: Table might be relevant but the connection is indirect or uncertain. State the reasoning.
* **Not relevant**: Table clearly does not relate to any business concept. State why (e.g., "contains geographic metadata with no connection to the metric").

**CRITICAL: Present the full triage to the user before proceeding.** Show all three categories with your reasoning. The user may know that a table you classified as "not relevant" is actually critical, or that a "strong candidate" is stale/deprecated. This is the most common point where silent assumptions cause problems.

Example presentation:

```
I found 8 tables in the bauplan namespace. Here's how I'd classify them
for your question about "average trip revenue by borough":

STRONG CANDIDATES:
  • taxi_fhvhv (14.2M rows) — contains trip records with fare columns
    (base_passenger_fare, total_amount, tips) and pickup location IDs.
    This looks like the primary fact table for trip revenue.
  • taxi_zones (265 rows) — location reference table with Borough, Zone,
    and LocationID. Needed to map location IDs to borough names.

WEAK CANDIDATES:
  • taxi_trips_summary (12K rows) — monthly pre-aggregated summary.
    Could work but we'd lose per-trip granularity.

NOT RELEVANT (for this question):
  • driver_licenses (45K rows) — driver data, no fare/trip info
  • vehicle_registry (82K rows) — vehicle metadata
  • weather_daily (3.6K rows) — weather data
  • zone_boundaries (265 rows) — GIS polygons
  • rate_codes (6 rows) — fare rate definitions

Do these classifications look right? Is there a table I should
reconsider, or one you know is the right source for this question?
```

**Wait for the user's response.** They may redirect you ("actually use taxi_trips_clean, not taxi_fhvhv — that one has known data issues") or confirm. Do not proceed until the user has acknowledged the candidate list.

### 1C. Deep-inspect confirmed candidates

Only after user confirmation, inspect the strong and weak candidates in detail:

```python
table = client.get_table(table="<table_name>", namespace="bauplan", ref=ref)
fields = [(c.name, c.type) for c in table.fields]
num_records = table.records
```

For each confirmed candidate, identify which columns could map to which business concepts. **When multiple columns could serve the same concept** (e.g., `price`, `base_passenger_fare`, `total_amount` for "revenue"), **list all of them** — do not pick one silently.

### 1D. Build the concept-to-column mapping

For each business concept (metric, dimensions, filters), identify:

* Which table contains a plausible column
* The column name and type
* Any transformation needed (e.g., "revenue" requires summing `price` where `event_type = 'purchase'`)
* Whether a join is needed to connect this concept to the main entity
* **If there are multiple candidate columns for the same concept, list all of them** and ask the user which one to use

Present the mapping to the user. When alternatives exist, surface them explicitly:

| Business Concept | Table  | Column              | Type    | Notes                                         |
|------------------|--------|---------------------|---------|-----------------------------------------------|
| revenue          | events | price               | decimal | Only where event_type='purchase'              |
| revenue (alt)    | events | total_amount        | decimal | Includes tax and fees — is this what you mean? |
| region           | zones  | Borough             | string  | Requires join on LocationID                   |

**When multiple columns compete for the same concept, explicitly ask the user to choose.** This is the most important interaction in the entire skill. Example: "I found two columns that could represent 'revenue': `base_passenger_fare` (excludes tips and surcharges) and `total_amount` (includes everything). Which one matches what you mean by 'revenue'?"

### 1E. Identify gaps

Flag any business concept that has NO plausible column backing. These are blockers.

Also flag any open questions from Phase 0 that the data inspection has now clarified or complicated.

### Gate: Can we proceed?

* If ALL critical concepts (the metric and at least one dimension) have confirmed column mappings → **proceed to Phase 2**.
* If ANY critical concept has no backing → **STOP**. Report what's missing. Tell the user which concepts cannot be mapped and suggest alternatives if any exist (e.g., "there's no 'region' column, but there's a LocationID that could be joined to a zones table").

---

## Phase 2: Assess Data Quality (Scoped to the Question)

**Goal:** Determine whether the mapped columns are trustworthy enough for this specific analysis.

Profile ONLY the tables and columns identified in Phase 1. Do not profile the entire catalog.

### 2A. For each mapped table, run the targeted profiling battery

**Freshness** — How recent is the latest record?
```python
q = "SELECT MAX(event_time) AS latest FROM bauplan.<table>"
res = client.query(q, ref=ref, max_rows=1)
```

**Completeness** — Null rate on the columns we need:
```python
q = """
SELECT
  COUNT(*) AS total,
  COUNT(column_a) AS non_null_a,
  COUNT(column_b) AS non_null_b
FROM bauplan.<table>
"""
res = client.query(q, ref=ref, max_rows=1)
```

**Volume** — Enough rows to produce meaningful results at the requested grain:
```python
q = "SELECT COUNT(*) AS n FROM bauplan.<table>"
res = client.query(q, ref=ref, max_rows=1)
```

**Key integrity** — If joins are needed, are the join keys unique and non-null on the expected side?
```python
q = """
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT join_key) AS distinct_keys,
  COUNT(*) - COUNT(join_key) AS null_keys
FROM bauplan.<table>
"""
res = client.query(q, ref=ref, max_rows=1)
```

**Coverage** — Does the data span the time scope the question requires?
```python
q = """
SELECT
  MIN(event_time) AS earliest,
  MAX(event_time) AS latest
FROM bauplan.<table>
"""
res = client.query(q, ref=ref, max_rows=1)
```

### 2B. Grade each table

For each mapped table, assign a quality grade scoped to this question:

* **Usable**: Data is fresh, complete on relevant columns, sufficient volume, keys are reliable.
* **Usable with caveats**: Minor issues that should be stated (e.g., 5% null rate on a dimension — results will exclude those rows).
* **Not usable**: Critical issues that block the analysis (e.g., 80% null on the primary metric, data only covers 2 of the 12 months requested).

Record findings per table. These feed into the feasibility report.

### Gate: Can we proceed?

* If all tables needed for the metric are graded **usable** or **usable with caveats** → **proceed to Phase 3**.
* If any table required for the core metric is graded **not usable** → **STOP**. Report the quality blockers with specific numbers. Suggest remediation if possible (e.g., "the data only goes back to March — could you narrow the question to the last 6 months?").

---

## Phase 3: Validate Semantic Fit

**Goal:** Verify that the data means what the business question needs it to mean.

This is the hardest phase. The data might exist and be high quality, but if "price" means unit price before tax and the user means total revenue including tax, the analysis will be wrong.

### 3A. Inspect actual values on semantically loaded columns

For each column that maps to a business concept, look at real values:

```python
# Categorical: inspect distinct values
q = """
SELECT <column>, COUNT(*) AS n
FROM bauplan.<table>
GROUP BY <column>
ORDER BY n DESC
LIMIT 20
"""
res = client.query(q, ref=ref, max_rows=20)

# Numeric: inspect range and distribution
q = """
SELECT
  MIN(<column>) AS min_val,
  MAX(<column>) AS max_val,
  AVG(<column>) AS avg_val,
  COUNT(DISTINCT <column>) AS distinct_vals
FROM bauplan.<table>
"""
res = client.query(q, ref=ref, max_rows=1)
```

### 3B. Identify semantic ambiguities

Look for situations where the data could be misinterpreted:

* Multiple columns that could represent the same concept (e.g., `price`, `base_passenger_fare`, `total_amount` — which is "revenue"?)
* Categorical values that don't match expectations (e.g., "region" values are zone IDs, not human-readable names)
* Numeric values in unexpected units (cents vs. dollars, seconds vs. minutes)
* Time columns at unexpected granularity (daily snapshots vs. per-event)
* Filter conditions that alter the meaning (e.g., does the table include cancelled orders? refunds?)

### 3C. Validate join semantics (if multiple tables involved)

If the concept mapping requires joins:

```python
# Overlap analysis: how many keys match?
q = """
SELECT
  COUNT(DISTINCT a.join_key) AS keys_in_left,
  COUNT(DISTINCT b.join_key) AS keys_in_right,
  COUNT(DISTINCT CASE WHEN b.join_key IS NOT NULL THEN a.join_key END) AS matching_keys
FROM bauplan.left_table a
LEFT JOIN bauplan.right_table b ON a.join_key = b.join_key
"""
res = client.query(q, ref=ref, max_rows=1)
```

Check for:

* **Overlap**: What percentage of left-side keys have a match on the right? Low overlap means lost rows in an inner join or nulls in a left join.
* **Fanout**: Does a single key on the left match multiple rows on the right? This inflates row counts and can distort aggregations.
* **Orphans**: Keys present on one side but not the other — these rows will be dropped or null-filled.

### 3D. Record findings

For each semantic issue found, classify it:

* **Confirmed**: The data clearly maps to the business concept. (e.g., "The `Borough` column contains readable region names like 'Manhattan', 'Brooklyn' — this maps directly to 'region'.")
* **Ambiguous — needs business input**: The mapping is plausible but depends on a business definition the agent cannot resolve. (e.g., "There are columns `price` and `base_passenger_fare` — which one represents 'revenue' depends on whether you include surcharges.")
* **Misaligned**: The data does not represent what the business question needs. (e.g., "The 'customer' identifier resets per session — this cannot support a retention analysis that tracks customers over time.")

---

## Phase 4: Render Verdict and Write Feasibility Report

**Goal:** Synthesize all findings into a structured document with a clear verdict.

### 4A. Determine the verdict

Based on Phases 1–3:

* **Answerable**: All concepts map to data, quality is sufficient, semantics align (possibly with stated assumptions).
* **Partially answerable**: The core question can be addressed but with material caveats — missing dimensions, quality gaps that reduce scope, or semantic assumptions that need business confirmation.
* **Not answerable**: Critical concepts have no data backing, or data quality/semantics make the analysis unreliable.

### 4B. Write the feasibility report

Write the report to `data-assessment/feasibility_report.md` using **exactly** the structure below. This structure is a contract — downstream skills depend on it.

```markdown
# Feasibility Report

## Business Question
<!-- The user's original question, restated -->

## Decomposition
- **Metric**: 
- **Grain**: 
- **Dimensions**: 
- **Time scope**: 
- **Filters**: 

## Verdict
<!-- One of: ANSWERABLE | PARTIALLY ANSWERABLE | NOT ANSWERABLE -->
<!-- One sentence explaining why -->

## Tables Considered

<!-- EVERY table in the namespace must appear here with a disposition.
     This section makes the assessment auditable — the user can verify
     that no relevant table was overlooked. -->

| Table | Rows | Disposition | Reason |
|-------|------|-------------|--------|
<!-- Disposition is one of: SELECTED | CONSIDERED | NOT RELEVANT -->
<!-- SELECTED = used in the concept-to-column mapping below -->
<!-- CONSIDERED = inspected but not selected (explain why) -->
<!-- NOT RELEVANT = excluded based on name/schema (explain why) -->

## Concept-to-Column Mapping

| Business Concept | Table | Column | Type | Transform | Notes |
|------------------|-------|--------|------|-----------|-------|

<!-- If multiple columns were candidates for the same concept,
     note the alternatives and record which one the user chose
     and why. Example:
     | revenue | events | base_passenger_fare | decimal | SUM |
       User chose this over total_amount (excludes tips per user request) |
-->

## Quality Scorecard

| Table | Column | Freshness | Null Rate | Volume | Coverage | Grade |
|-------|--------|-----------|-----------|--------|----------|-------|

## Semantic Findings

### Confirmed
<!-- List of confirmed concept-to-data mappings -->

### Ambiguous (Needs Business Input)
<!-- List of ambiguities the business user must resolve -->

### Misaligned
<!-- List of semantic mismatches, if any -->

## Join Strategy
<!-- If multiple tables are involved: which keys, what join type,
     overlap %, expected fanout. Omit this section if no joins needed. -->

## Assumptions
<!-- Numbered list of every assumption made during the assessment.
     Each assumption should be something the business user can
     confirm or reject. -->

1. ...
2. ...

## Caveats
<!-- Data quality issues or scope limitations that affect
     the analysis but don't block it. -->

## Recommended Next Steps
<!-- What to do next: proceed to analysis, clarify ambiguities
     with business, acquire missing data, etc. -->

---
*Assessment performed on ref: `<ref>` | Namespace: `<namespace>` | Date: <date>*
```

### 4C. Present the verdict to the user

After writing the report, summarize the verdict conversationally. Highlight:

* The verdict and the key reason behind it
* Any ambiguities that need the business user's input before proceeding
* The most important caveats

Do not dump the entire report into the chat. The user can read the file for full details.

---

## Handoff to other skills

When the assessment is complete:

* If the verdict is **answerable** or **partially answerable**, tell the user you can proceed to produce a one-off analysis using the findings in this report.
* If the verdict is **not answerable**, clearly state the blockers and suggest what data would be needed to unblock.

The feasibility report at `data-assessment/feasibility_report.md` serves as the input contract for the one-off analysis skill.

---

## Workflow Checklist

Copy and track progress:

```
Data Assessment Progress:
- [ ] Phase 0: Decompose business question (metric, grain, dimensions, time scope, filters)
- [ ] Phase 0: Classify gaps as critical vs deferrable
- [ ] Phase 0: Resolve critical gaps (coach user through "I don't know" responses)
- [ ] Phase 0: Confirm target branch (do NOT default silently to main)
- [ ] Phase 0 Checkpoint: User confirmed decomposition + branch
- [ ] Phase 1A: List ALL tables in namespace
- [ ] Phase 1B: Triage into strong/weak/not-relevant with reasoning
- [ ] Phase 1 Checkpoint: User confirmed table triage
- [ ] Phase 1C-D: Build concept-to-column mapping, surface alternatives
- [ ] Phase 1 Checkpoint: User chose between competing columns (if any)
- [ ] Phase 1 Gate: All critical concepts have confirmed backing
- [ ] Phase 2: Profile data quality on mapped columns
- [ ] Phase 2 Gate: No critical quality blockers
- [ ] Phase 3: Validate semantic fit, check join viability
- [ ] Phase 4: Write feasibility report to data-assessment/feasibility_report.md
- [ ] Phase 4: Present verdict to user
```

---

## Example Walkthrough

**User question**: "Who are our top customers during the bank holidays?"

### Phase 0: Decomposition (interactive, with coaching)

Agent's initial decomposition:

```
Here's how I'm reading your question:

- Metric: "top customers" — ranked by what? Revenue, order count, 
  or something else?
- Grain: per customer
- Dimensions: ranking (top N)
- Time scope: "bank holidays" — which ones? A specific country? 
  A specific year?
- Filters: only activity during bank holidays

Before I look at any data, I need to understand a few things:
1. What makes a customer "top"? Revenue, number of orders, or 
   something else?
2. Which bank holidays? US federal? UK? A specific year?
3. What counts as a "customer" in your business? An account, 
   an email, a name?
```

User responds: "Revenue. US federal holidays. I don't know what a customer is — can you help me figure that out?"

**Agent does NOT move on.** It stays in Phase 0 and coaches:

```
Good question to think through. Since you're the ecommerce manager, 
"customer" could mean different things in your data:

  • A unique email address — simplest, but the same person 
    might use different emails for different orders
  • An account/user ID — if your platform requires login to buy
  • A billing name — catches guest checkouts but "John Smith" 
    is ambiguous

For "top customers by revenue," this matters a lot. If someone 
places 3 orders under one email and 2 under another, are they 
one customer with 5 orders, or two separate customers?

What does your ecommerce system use as the primary customer 
identifier? If you're not sure, I can look at what identifier 
columns exist in the data and show you — but I want to make sure 
we agree on what "same customer" means before I start ranking.
```

User: "We require login, so account ID makes sense. Show me what's in the data."

→ Customer = account/user ID (critical gap resolved).
→ Exact column name is deferrable — will check in Phase 1.

Agent presents confirmed decomposition:

```
Here's what we've landed on:

- Metric: total revenue per customer, ranked highest first
- Grain: per customer (account/user ID)
- Dimensions: ranked list (top N — how many? 10? 50?)
- Time scope: US federal holidays (which year? Or all time?)
- Filters: only orders placed on bank holiday dates

Still need from you:
- How many "top" customers? Top 10? Top 50?
- Which year(s)?

Open questions I'll resolve by looking at the data:
- Which column is the account/user ID
- Which column represents revenue
- Whether bank holiday dates are flagged in the data or 
  need to be derived from calendar logic

Does this capture what you're after?
```

User: "Top 20, last year is fine. Looks good."

Agent: "One more thing — which branch should I explore? Main, or do you have a dev branch with the latest data?"

User: "Main is fine."

→ Decomposition confirmed. Branch confirmed: `main`. Proceed to Phase 1.

### Phase 1: Table triage (interactive)

Agent scans namespace and presents all tables with reasoning:

```
I found 6 tables in the bauplan namespace. Here's my triage:

STRONG CANDIDATES:
  • ecommerce_orders (2.1M rows) — order-level records with 
    user_id, order_total, and order_date. Primary fact table.
  • ecommerce_customers (185K rows) — customer reference with 
    account_id, email, name. Needed for customer identity.

WEAK CANDIDATES:
  • ecommerce_sessions (8.4M rows) — browsing sessions. Has 
    user_id but no revenue data. Could be useful if you wanted 
    to measure engagement, but you asked for revenue.

NOT RELEVANT (for this question):
  • product_catalog (12K rows) — product metadata, no customer info
  • warehouse_inventory (45K rows) — stock levels
  • email_campaigns (890 rows) — marketing sends

Do these look right? Should I reconsider any table?
```

User: "That's right. Use orders and customers."

Agent deep-inspects and finds the identifier question can be resolved:

```
In ecommerce_orders, the customer identifier is `user_id` (integer).
In ecommerce_customers, there's both `account_id` and `user_id`. 
They appear to be the same — I'll verify the join in Phase 3.

For revenue, I found two columns:
  • order_total (decimal) — looks like the final amount charged
  • subtotal (decimal) — before tax and shipping

Which one is "revenue" for your ranking?
```

User: "order_total."

Final concept mapping:

| Business Concept | Table               | Column      | Type      | Notes                                       |
|------------------|---------------------|-------------|-----------|---------------------------------------------|
| revenue          | ecommerce_orders    | order_total | decimal   | User chose over subtotal                    |
| customer ID      | ecommerce_orders    | user_id     | integer   | Join key to customers table                 |
| time scope       | ecommerce_orders    | order_date  | timestamp | Filter: US federal holiday dates, last year |
| customer name    | ecommerce_customers | name        | string    | For display in final ranking                |

Note: US federal holiday dates are not in the data — they'll need to be derived from calendar logic. This is a caveat, not a blocker.

### Phase 1 Tables Considered (goes into report)

| Table               | Rows  | Disposition  | Reason                                            |
|---------------------|-------|--------------|---------------------------------------------------|
| ecommerce_orders    | 2.1M  | SELECTED     | Primary fact table with order revenue and dates   |
| ecommerce_customers | 185K  | SELECTED     | Customer reference for names and identity         |
| ecommerce_sessions  | 8.4M  | CONSIDERED   | Has user_id but no revenue; not needed for this Q |
| product_catalog     | 12K   | NOT RELEVANT | Product metadata, no customer/revenue data        |
| warehouse_inventory | 45K   | NOT RELEVANT | Stock levels, unrelated to customer revenue       |
| email_campaigns     | 890   | NOT RELEVANT | Marketing data, no transaction info               |

### Phase 2: Quality scorecard

| Table               | Column      | Freshness | Null Rate | Volume     | Coverage    | Grade  |
|---------------------|-------------|-----------|-----------|------------|-------------|--------|
| ecommerce_orders    | order_total | 2025-01   | 0.1%      | 2.1M total | Last year ✓ | Usable |
| ecommerce_orders    | user_id     | —         | 0%        | —          | —           | Usable |
| ecommerce_orders    | order_date  | —         | 0%        | —          | Full year ✓ | Usable |
| ecommerce_customers | user_id     | —         | 0%        | 185K       | —           | Usable |

Gate: all usable. Proceed.

### Phase 3: Semantic findings
- **Confirmed**: `user_id` in orders matches `user_id` in customers — 99.8% overlap, 1:1 on customer side.
- **Confirmed**: `order_total` ranges from $0.99 to $4,200 — plausible for ecommerce.
- **Caveat**: US federal holiday dates are not a column in the data. The analysis will require a hardcoded list of dates (MLK Day, Presidents Day, Memorial Day, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving, Christmas). The agent cannot determine business-specific closures (e.g., does the company observe Juneteenth?). **Needs business confirmation.**

### Phase 4: Verdict

**ANSWERABLE** — All core concepts map to confirmed columns. The customer entity is clear (user_id with login-required accounts), revenue column is confirmed (order_total), and data covers the requested period. One caveat: US federal holiday dates must be derived externally — the user should confirm which specific holidays to include.

---

## Key SDK Methods Reference

| Method                                          | Description                          |
|-------------------------------------------------|--------------------------------------|
| `bauplan.Client()`                              | Initialize the bauplan client        |
| `client.get_tables(ref=, filter_by_namespace=)` | List tables in a namespace           |
| `client.get_table(table=, namespace=, ref=)`    | Get table schema and metadata        |
| `client.has_table(table=, ref=, namespace=)`    | Check if table exists                |
| `client.query(query=, ref=, max_rows=)`         | Run SQL query, returns PyArrow Table |
| `client.get_namespaces(ref=)`                   | List namespaces on a ref             |

> **SDK Reference**: For detailed method signatures, check https://docs.bauplanlabs.com/reference/bauplan
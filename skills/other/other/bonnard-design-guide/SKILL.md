---
name: bonnard-design-guide
description: Design principles for building semantic layers that work well for AI agents and business users. Use when building views, writing descriptions, or improving agent accuracy.
allowed-tools: Bash(bon *)
---

# Semantic Layer Design Guide

This guide covers design decisions that determine whether your semantic layer
works for end users and AI agents. It complements the setup guides
(`/bonnard-get-started`, `/bonnard-metabase-migrate`) which cover mechanics.

Read this before building views, or revisit it when agents return wrong
answers or users can't find the right metrics.

## Principle 1: Start from Questions, Not Tables

The natural instinct is: look at tables, build cubes, expose everything.
This produces a semantic layer that mirrors your warehouse schema —
technically correct but useless to anyone who doesn't already know the schema.

**Instead, start from what people ask:**

1. Collect the 10-20 most common questions your team asks about data
2. For each question, identify which tables/columns are needed to answer it
3. Group questions by audience (who asks them)
4. Build views that answer those question groups

If you have a BI tool (Metabase, Looker, Tableau), your top dashboards
by view count are the best source of real questions. If not, ask each team:
"What 3 numbers do you check every week?"

**Why this matters:** A semantic layer built from questions produces focused,
audience-scoped views. One built from tables produces generic views that agents
struggle to choose between. Governance policies control which views each user
or role can access, so build as many views as your audiences need — but make
each one purposeful with clear descriptions.

## Principle 2: Views Are for Audiences, Not Tables

A common mistake is creating one view per cube (table). This produces views
like `orders_view`, `users_view`, `invoices_view` — which is just the
warehouse schema with extra steps.

**Views should represent how a team thinks about data:**

```
BAD (model-centric):                 GOOD (audience-centric):
views/                               views/
  orders_view.yaml       (1 cube)      management.yaml      (revenue + users)
  users_view.yaml        (1 cube)      sales.yaml           (opportunities + invoices)
  invoices_view.yaml     (1 cube)      product.yaml         (users + funnel + contracts)
  opportunities_view.yaml (1 cube)     partners.yaml        (partners + billing)
```

The same cube often appears in multiple views. An `opportunities` cube might
contribute to `sales_opportunities` (filtered to active offers), a management
KPI view, and a partner performance view. Each view exposes different
measures and dimensions because different audiences need different slices.

**Name views by what they answer**, not what table they wrap:
`sales_pipeline` not `opportunities_overview`.

## Principle 3: Add Filtered Measures

This is the single most impactful thing you can do. Look at any real
dashboard: it almost never shows `COUNT(*)` from a raw table. It shows
"active offers" (type=Angebot AND status!=Cancelled), "unpaid invoices"
(status NOT IN terminal states).

Without filtered measures, agents return unfiltered totals that don't match
what users see in their dashboards. Users lose trust immediately.

**For every important dashboard card, check the WHERE clause:**

```yaml
# Dashboard shows "Active Offers: 7,500"
# But raw COUNT(*) on opportunities returns 29,000
# The card SQL has: WHERE type = 'Angebot' AND status != 'Abgesagt'

measures:
  - name: count
    type: count
    description: Total opportunities (all types and statuses)

  - name: active_offer_count
    type: count
    description: Non-cancelled offers only (type=Angebot, status!=Abgesagt)
    filters:
      - sql: "{CUBE}.type = 'Angebot'"
      - sql: "{CUBE}.status != 'Abgesagt'"
```

**Common patterns that need filtered measures:**
- Status filters: active/open/pending items vs all items
- Type filters: specific transaction types vs all transactions
- Boolean flags: completed, paid, verified subsets
- Exclusions: excluding test data, internal users, cancelled records

A good rule of thumb: if a BI dashboard card has a WHERE clause beyond just
a date range, that filter should probably be a filtered measure.

## Principle 4: Descriptions Are the Discovery API

For AI agents, descriptions are not documentation — they are the **primary
mechanism for choosing which view and measure to use**. When an agent calls
`explore_schema`, it sees view names and descriptions. That's all it has
to decide where to query.

### View descriptions must answer three questions:

1. **What's in here?** — Lead with the scope and content
2. **When should I use this?** — The default use case
3. **When should I use something else?** — Explicit disambiguation

```yaml
# BAD: Generic, doesn't help agent choose
description: User metrics and dimensions

# GOOD: Scoped, navigational, includes data values
description: >-
  Sales pipeline — active and historical opportunities with contract values
  and assignee details. Default view for pipeline questions, deal counts,
  and contract value analysis. Use the type dimension (values: Angebot,
  Auftrag) to filter by opportunity type. For invoice-level detail, use
  sales_invoices instead.
```

### Description writing rules:

**Lead with scope, not mechanics.** "All users across both products" not
"Wraps the all_users cube." Agents match question keywords against
description keywords.

**Include actual dimension values.** If a dimension has known categorical
values, list them: `(values: erben, vererben)`, `(values: B2B, Organic)`.
This helps agents map user language to filter values.

**Use the same vocabulary as your users.** If your team says "testaments"
not "will_and_testament", the description should say "testaments."

**Cross-reference related views.** When two views could plausibly answer the
same question, both descriptions should point to each other: "For company-wide
totals, use company_users instead." This is the most effective way to
prevent agents from picking the wrong view.

### Measure descriptions should say what's included/excluded:

```yaml
# BAD
description: Count of orders

# GOOD
description: >-
  Orders with status 'completed' or 'shipped' only.
  Excludes cancelled and pending. For all orders, use total_order_count.
```

## Principle 5: Build Cross-Entity Views When Users Think Across Tables

Sometimes the most common question doesn't map to any single table.
"How many total signups do we have?" might require combining users from
two separate product tables.

**Options:**

1. **Database view/UNION table** — If your warehouse has a combined
   view, build a cube on it. Cleanest approach.
2. **Multiple cubes in one view via joins** — If cubes can be joined
   through foreign keys, include both in a view using `join_path`.
3. **Separate views with clear descriptions** — If data can't be combined,
   create separate views and describe how they relate.

Don't force everything into one view. It's better to have an agent make
two clear queries than one confused query against an over-joined view.

## Principle 6: Test with Natural Language, Not Just Numbers

Verifying that `bon query '{"measures": ["orders.count"]}'` returns the
right number is necessary but not sufficient. The actual failure mode is:

> User asks "how many active offers do we have?"
> Agent queries `orders.count` instead of `sales_pipeline.active_offer_count`
> Returns 29,000 instead of 7,500

**To test properly, give real questions to an AI agent via MCP and check:**

1. Did it find the right **view**?
2. Did it pick the right **measure**?
3. Did it apply the right **filters/date range**?
4. Is the final **number** correct?

Steps 1-3 are where most failures happen, caused by description and view
structure problems — not wrong data.

**Build a small eval set:**
- Write 5-10 questions that your users actually ask
- For each question, record the expected view, measure, and answer
- Run each question through an agent 3-5 times (agents are non-deterministic)
- If pass rate is below 80%, the issue is almost always the view description
  or view structure, not the data

## Principle 7: Iterate — The First Deploy Is Never Right

The semantic layer is not a one-time build. The effective workflow is:

```
Build views -> Deploy -> Test with questions -> Find agent mistakes
     ^                                              |
     +---- Improve descriptions/measures <----------+
```

Expect 2-4 iterations before agents reliably answer the top 10 questions.
Each iteration typically involves:

- Rewriting 1-2 view descriptions to improve disambiguation
- Adding 1-3 filtered measures that match dashboard WHERE clauses
- Occasionally restructuring a view (splitting or merging)

**Don't try to get it perfect before deploying.** Deploy early with your
best guess, test with real questions, and fix what breaks.

## Quick Checklist

Before deploying, review each view against this checklist:

- [ ] **View name** describes the audience/use case, not the underlying table
- [ ] **View description** leads with scope ("All users..." / "Sales team only...")
- [ ] **View description** cross-references related views ("For X, use Y instead")
- [ ] **View description** includes key dimension values where helpful
- [ ] **Filtered measures** exist for every dashboard card with a WHERE clause
- [ ] **Measure descriptions** say what's included AND excluded
- [ ] **Dimension descriptions** include example values for categorical fields
- [ ] **No two views** could plausibly answer the same question without disambiguation

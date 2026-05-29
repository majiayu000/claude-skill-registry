---
name: couple-weekly-report
description: Generate weekly relationship health report showing affect ratios and repair rates for both partners across 3 weeks (current + 2 prior) with message quotes.
---

# Couple Weekly Report Skill

**Generate a concise weekly relationship health report with metrics and message context.**

---

## 🎯 When to Use This Skill

Use this skill when:
- "Generate weekly report for [couple]"
- "Show me this week's relationship metrics for [couple]"
- "Create a weekly health summary for [couple]"
- "What happened this week with [couple]?"

**Output:** Markdown file with 3-week metrics table + message quotes for context.

---

## 📋 Report Structure

The report includes:

1. **Metrics Table**: 3 weeks of data (current week + 2 prior weeks) showing:
   - Week dates
   - Each partner's affect ratio (positive:negative)
   - Each partner's repair rate (%)
   - Trend indicators (↑↓→)

2. **Message Context**: 2-4 sentences quoting actual messages that:
   - Illustrate significant changes in metrics
   - Provide emotional color for the week's dynamics
   - Interpret through the product framework (see below)

---

## 📖 Product Framework Reference

**IMPORTANT:** Before generating any report, read the "Product Principles" section at the top of `README.md` (parent repo).

**When interpreting metrics:**

1. **Affect Ratios** → Reference "What we do" section for the two core skills
   - High positive affect = practicing the first skill (expressing needs vulnerably)
   - High negative affect = protest behavior (see "Conflict is a plea for connection")

2. **Repair Rates** → Reference "What we do" section for engagement patterns
   - High repair rate = practicing the second skill (staying engaged)
   - Low repair rate = withdrawing or defending

3. **Attachment Patterns** → Reference "Understanding Your Role in the Dance" section
   - Identify Pursuer/Withdrawer dynamics from metrics
   - Map to the three common patterns described
   - Note which skill each partner needs to focus on

4. **Message Context** → Reference "Why these skills work" section
   - Quote examples showing vulnerability vs protest behavior
   - Show de-escalation attempts
   - Use EFT lens: conflict as plea for connection

**Health Thresholds:** Use Gottman research thresholds from "The cost of destructive conflict patterns" section.

---

## 🔄 Workflow

### Step 1: Identify the Couple and Week

Ask user if needed:
- Which couple? (Get `persons` table IDs for both partners)
- Which week? (Default: current week, Mon-Sun)

**Key dates:**
- Current week: Most recent Monday-Sunday
- Week -1: Previous Monday-Sunday
- Week -2: Two weeks ago Monday-Sunday

### Step 2: Calculate Weekly Metrics (3 weeks)

For each week and each partner, calculate:

**Affect Ratio Query:**
```sql
WITH affect_counts AS (
  SELECT
    p.id as person_id,
    p.name,
    DATE_TRUNC('week', m.provider_timestamp) as week_start,
    COUNT(*) FILTER (WHERE me.valence = 'Positive') as positive_count,
    COUNT(*) FILTER (WHERE me.valence = 'Negative') as negative_count
  FROM message m
  JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  LEFT JOIN message_enrichment me ON me.message_id = m.id
  WHERE m.provider_timestamp >= CURRENT_DATE - INTERVAL '21 days'  -- 3 weeks
    AND pc.person_id IN (:person1_id, :person2_id)
    AND me.affect IS NOT NULL
  GROUP BY p.id, p.name, week_start
)
SELECT
  person_id,
  name,
  week_start,
  positive_count,
  negative_count,
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN 100.0
    WHEN negative_count = 0 THEN 0.0
    ELSE ROUND((positive_count::decimal / negative_count), 1)
  END as affect_ratio
FROM affect_counts
ORDER BY week_start DESC, name;
```

**Repair Rate Query:**
```sql
WITH conflict_repairs AS (
  SELECT
    p.id as person_id,
    p.name,
    DATE_TRUNC('week', m.provider_timestamp) as week_start,
    COUNT(*) FILTER (
      WHERE me.conflict_state IN ('De-escalation', 'De-Escalation', 'Resolution')
    ) as repairs,
    COUNT(*) FILTER (
      WHERE me.conflict_state IN ('New Conflict', 'New conflict', 'Escalation')
    ) as conflicts
  FROM message m
  JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  LEFT JOIN message_enrichment me ON me.message_id = m.id
  WHERE m.provider_timestamp >= CURRENT_DATE - INTERVAL '21 days'
    AND pc.person_id IN (:person1_id, :person2_id)
    AND me.conflict_state IS NOT NULL
  GROUP BY p.id, p.name, week_start
)
SELECT
  person_id,
  name,
  week_start,
  repairs,
  conflicts,
  CASE
    WHEN conflicts = 0 THEN NULL
    ELSE ROUND((repairs::decimal / conflicts * 100), 0)
  END as repair_rate_pct
FROM conflict_repairs
ORDER BY week_start DESC, name;
```

### Step 3: Fetch Representative Messages

Get 3-5 meaningful messages from the current week that show:
- High-affect moments (positive or negative)
- Conflict patterns or repairs
- Notable communication shifts

```sql
SELECT
  p.name as sender,
  m.message_text,
  me.affect,
  me.valence,
  me.conflict_state,
  m.provider_timestamp
FROM message m
JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
JOIN persons p ON pc.person_id = p.id
LEFT JOIN message_enrichment me ON me.message_id = m.id
WHERE m.provider_timestamp >= :current_week_start
  AND m.provider_timestamp < :current_week_end
  AND pc.person_id IN (:person1_id, :person2_id)
  AND (
    me.affect IN ('Joy', 'Love', 'Contempt', 'Partner-Criticism', 'Stonewalling')
    OR me.conflict_state IN ('New Conflict', 'Escalation', 'De-escalation', 'Resolution')
  )
ORDER BY
  CASE
    WHEN me.valence = 'Negative' THEN 1
    WHEN me.conflict_state IS NOT NULL THEN 2
    ELSE 3
  END,
  m.provider_timestamp DESC
LIMIT 5;
```

### Step 4: Generate Markdown Report

Create markdown file: `reports/couple_weekly_report_{couple_name}_{week_date}.md`

**Template:**

```markdown
# Weekly Relationship Report: {Partner1} & {Partner2}
**Week of {Current Week Start} - {Current Week End}**

---

## 📊 Metrics Overview (3 Weeks)

| Week | {Partner1} Affect Ratio | {Partner1} Repair % | {Partner2} Affect Ratio | {Partner2} Repair % |
|------|-------------------------|---------------------|-------------------------|---------------------|
| Current ({dates}) | {ratio} {trend} | {pct}% {trend} | {ratio} {trend} | {pct}% {trend} |
| Week -1 ({dates}) | {ratio} | {pct}% | {ratio} | {pct}% |
| Week -2 ({dates}) | {ratio} | {pct}% | {ratio} | {pct}% |

**Legend:**
- Affect Ratio: Positive:Negative emotions (Healthy: 5:1 to 30:1)
- Repair Rate: % of conflicts successfully de-escalated (Healthy: >75%)
- Trends: ↑ improving, ↓ declining, → stable

---

## 💬 This Week's Context

{2-4 sentences summarizing the week using the two core skills framework from README.md, with direct message quotes}

**Instructions:**
- Reference "What we do" section to interpret affect patterns (vulnerability vs protest behavior)
- Quote messages that show skill practice or challenges
- Use language from "Conflict is a plea for connection" to reframe criticism

**Example:**
"{Partner1}'s affect ratio improved significantly this week (8.2:1 ↑ from 3.1:1), with messages like '{positive quote}' showing vulnerability. However, {Partner2} showed increased Partner-Criticism ('{negative quote}'), suggesting protest behavior. Their repair rate remained strong at 80%, with effective de-escalation in conversations about {topic}."

---

## 📈 Trend Insights

{1-2 sentences noting significant trends using attachment patterns from README.md}

**Instructions:**
- Reference "Understanding Your Role in the Dance" section to identify pattern (Pursuer/Withdrawer, Attack-Attack, or Avoidant-Avoidant)
- Note which of the two core skills each partner needs most
- Use research language from "Why these skills work" section

**Example:**
"Metrics suggest a [pattern name] dynamic, with {Partner1} showing [pursuer/withdrawer behaviors]. {Partner2}'s [improving/declining] repair rate indicates [progress/challenge] with the second core skill described in README.md."

---

*Report generated: {timestamp}*
*Data source: Production database*
```

### Step 5: Save and Display

1. Save markdown file to `reports/` directory
2. Display file path to user
3. Show preview of key metrics

---

## 🎯 Health Thresholds (Quick Reference)

### Affect Ratio (Positive:Negative)
- **Healthy:** 5:1 to 30:1
- **At-Risk:** <5:1
- **Context-Dependent:** >30:1 (may indicate conflict avoidance)

### Repair Rate (De-escalation Success %)
- **Healthy:** >75%
- **At-Risk:** 50-75%
- **Concerning:** <50%

---

## 🚀 Usage Example

```
User: "Generate weekly report for Sam and Alex"

Claude (using sql-reader skill):
1. Identifies person_ids for Sam and Alex from persons table
2. Determines current week dates (Mon-Sun)
3. Runs affect ratio query for 3 weeks
4. Runs repair rate query for 3 weeks
5. Fetches 3-5 representative messages from current week
6. Generates markdown report with:
   - 3-week metrics table with trends
   - 2-4 sentences with message quotes
   - Trend insights
7. Saves to: reports/couple_weekly_report_sam_alex_2025-01-13.md
8. Shows user the file path and key findings
```

---

## 💡 Tips

**Choosing Quotes:**
- Pick messages that illustrate the two core skills from README.md "What we do" section
- Include both partners' voices
- Show emotional color:
  - Vulnerability examples (first skill)
  - Staying engaged examples (second skill)
  - Protest behavior (see "Conflict is a plea for connection" in README.md)
- Keep quotes concise (1 sentence each)

**Interpreting Metrics (reference README.md sections):**
- **High positive affect** = First skill (expressing needs vulnerably)
- **High negative affect** = Protest behavior (see "Why we do it" section)
- **High repair rate** = Second skill (staying engaged)
- **Low repair rate** = Withdrawing or defending (see "Pursuer & Withdrawer Dynamics")
- **>30:1 affect ratio** = May indicate conflict avoidance (see "Avoidant-Avoidant" pattern)

**Calculating Trends:**
- ↑ if current week > previous week by >20%
- ↓ if current week < previous week by >20%
- → if within 20% range

**Handling Missing Data:**
- If no affect data: Show "N/A" and note in context
- If no conflicts: Repair rate shows "No conflicts this week"
- If <3 weeks of data: Show available weeks only

---

## 🔗 Related Resources

- **README.md (Product Principles)**: Source of truth for interpreting metrics through the product framework
- **sql-reader**: Use this skill to query the production database
- **product-data-analyst**: For broader relationship health analysis
- **_archived/assess-couple-health**: More comprehensive clinical assessment (8-week trailing averages)
```

---
name: generate-ceo-briefing
description: Autonomously audit business and financial performance weekly. Analyzes revenue, expenses, completed tasks, bottlenecks, and generates executive briefing with proactive suggestions. Use when generating weekly report, business audit, or when user mentions "briefing", "ceo report", "performance summary", "weekly audit", "business review".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
model: sonnet
---

# Generate CEO Briefing Skill

**The Standout Feature** - Transforms your AI Employee from reactive tool to proactive business partner. Autonomously audits your entire business weekly and delivers executive-level insights every Monday morning.

---

## Core Responsibilities

1. **Financial Analysis**: Revenue, expenses, cash flow vs targets, cost optimization
2. **Operational Analysis**: Task completion rates, bottlenecks, response times
3. **Social Media Performance**: Engagement across LinkedIn, Facebook, Instagram, Twitter
4. **Business Goal Progress**: Track progress vs targets, identify at-risk goals
5. **Proactive Recommendations**: Unused subscriptions, process improvements, growth opportunities

---

## When This Skill Activates

**Trigger phrases:**
- "generate weekly briefing"
- "create ceo report"
- "business audit"
- "performance summary"
- "weekly review"
- "how's the business doing"
- "monday briefing"

**Auto-activates:**
- **Scheduled**: Every Sunday at 11:45 PM (automated via cron/Task Scheduler)
- Creates notification in `Vault/Needs_Action/` for Monday morning review
- Runs whenever user explicitly requests business performance analysis

---

## Core Workflow

### Phase 1: Data Collection

**When:** Briefing generation starts (Sunday 11:45 PM or on-demand)

1. **Financial Data** (from `manage-accounting` skill)
   - Read `Vault/Accounting/Current_Month.md`
   - Parse weekly transactions (last 7 days)
   - Calculate:
     - Weekly revenue
     - Weekly expenses (by category)
     - Month-to-date totals
     - Outstanding invoices
   - Read `Vault/Business_Goals.md` for financial targets

2. **Operational Data** (from `process-tasks` skill)
   - Scan `Vault/Done/` folder for completed tasks (last 7 days)
   - Count tasks completed
   - Identify tasks that took longer than expected (compare due dates)
   - Check `Vault/Tasks/Active/` for overdue or at-risk tasks

3. **Email Performance** (from `process-emails` skill)
   - Read `Vault/Done/` for processed emails (last 7 days)
   - Calculate average response time
   - Identify any urgent/high-priority emails still pending
   - Count emails processed vs received

4. **Social Media Metrics** (from social media skills)
   - Read `Vault/Social_Media/LinkedIn/metrics.json`
   - Read `Vault/Social_Media/Facebook/metrics.json`
   - Read `Vault/Social_Media/Instagram/metrics.json`
   - Read `Vault/Social_Media/Twitter/metrics.json`
   - Extract: posts published, engagement, follower growth, reach

5. **Business Goals Progress**
   - Read `Vault/Business_Goals.md`
   - Compare actual vs targets for each key metric
   - Calculate progress percentage
   - Identify at-risk goals (behind target by >20%)

**Helper Script:**
```bash
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --period weekly
```

See [analysis-framework.md](./reference/analysis-framework.md) for detailed data collection procedures.

---

### Phase 2: Performance Analysis

**When:** After data collection complete

1. **Financial Health Score (0-100)**
   - Revenue vs target: +40 points if on track
   - Expense control: +30 points if under budget
   - Cash flow positive: +20 points
   - No overdue invoices >30 days: +10 points
   - Calculate score and trend (improving/declining/stable)

2. **Operational Efficiency Score (0-100)**
   - Task completion rate: +40 points if >90%
   - Average task cycle time: +30 points if within expected
   - Email response time: +20 points if <24 hours
   - No overdue high-priority items: +10 points

3. **Social Media Engagement Score (0-100)**
   - Posts published vs schedule: +25 points if on track
   - Engagement rate (likes/comments/shares): +40 points if above benchmark
   - Follower growth: +20 points if positive
   - Response rate to mentions/comments: +15 points if >80%

4. **Goal Achievement Score (0-100)**
   - Calculate progress percentage for each goal
   - Weight by goal priority
   - Identify goals at risk (behind schedule)
   - Predict likelihood of achieving quarterly/annual targets

**Overall Business Health:** Average of 4 scores
- 90-100: Excellent (Green)
- 75-89: Good (Green)
- 60-74: Fair (Yellow)
- Below 60: Needs Attention (Red)

**Helper Script:**
```bash
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --calculate-scores
```

See [kpi-definitions.md](./reference/kpi-definitions.md) for detailed scoring methodology.

---

### Phase 3: Bottleneck Detection

**When:** After performance analysis

1. **Identify Process Bottlenecks**
   - Compare task completion times vs expected duration
   - Flag tasks that took >50% longer than expected
   - Categorize bottlenecks:
     - Waiting on client/external party
     - Insufficient resources
     - Unclear requirements
     - Technical blockers
     - Over-commitment

2. **Financial Bottlenecks**
   - Overdue invoices (cash flow impact)
   - Recurring expenses without value delivery
   - Budget overruns in specific categories
   - Missing financial data/reconciliation issues

3. **Communication Bottlenecks**
   - Emails pending response >48 hours
   - Unanswered social media mentions
   - Client communications delayed

4. **Resource Bottlenecks**
   - Over-allocated time (too many commitments)
   - Under-utilized resources (unused subscriptions)
   - Skill gaps (tasks taking longer than they should)

**Prioritize bottlenecks:**
- **Critical**: Directly impacting revenue or client satisfaction
- **High**: Causing significant delays
- **Medium**: Reducing efficiency
- **Low**: Minor improvements

**Helper Script:**
```bash
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py
```

See [analysis-framework.md](./reference/analysis-framework.md) for bottleneck classification logic.

---

### Phase 4: Generate Proactive Recommendations

**When:** After bottleneck detection

1. **Cost Optimization Recommendations**

   **Subscription Audit:**
   - Analyze recurring expenses from `Vault/Accounting/Current_Month.md`
   - Identify subscriptions with pattern matching (Adobe, Netflix, Notion, Slack, etc.)
   - Check for:
     - No usage in 30+ days
     - Duplicate functionality with other tools
     - Cost increased >20% without value increase
   - Calculate potential savings:
     - Monthly savings × 12 = Annual savings
     - ROI: (Annual savings / Time to cancel) ratio

   **Example Output:**
   ```
   ⚠️ Cost Optimization Opportunity
   - Service: Notion Team Plan
   - Cost: $15/month ($180/year)
   - Last Activity: 47 days ago
   - Alternative: Already using Obsidian for same purpose
   - Action: Cancel Notion subscription
   - Annual Savings: $180
   ```

2. **Process Improvement Recommendations**
   - If email response time >24h: Suggest email processing schedule
   - If task completion rate <90%: Recommend prioritization system
   - If social media engagement declining: Suggest content strategy review
   - If recurring bottlenecks: Recommend automation or delegation

3. **Growth Opportunity Recommendations**
   - If revenue trending up: Suggest capacity expansion
   - If social media engagement high: Recommend increased posting frequency
   - If client satisfaction high: Suggest asking for referrals
   - If cash flow strong: Recommend strategic investments

4. **Risk Mitigation Recommendations**
   - If overdue invoices accumulating: Suggest payment terms review
   - If expenses exceeding budget: Recommend cost control measures
   - If key goals at risk: Suggest reallocation of resources
   - If client response delays: Recommend capacity assessment

**Helper Script:**
```bash
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py
```

See [recommendation-engine.md](./reference/recommendation-engine.md) for recommendation generation logic.

---

### Phase 5: Write CEO Briefing

**When:** After all analysis complete

1. **Create Briefing Document**
   - Use [briefing-template.md](./reference/briefing-template.md)
   - Filename: `Vault/Briefings/YYYY-MM-DD_Monday_Briefing.md`
   - Date format: Week ending date (Sunday date)

2. **Briefing Structure** (see template for full format):

   **Executive Summary** (1-2 sentences)
   - Overall business health status
   - Key highlight of the week
   - Critical alert (if any)

   **Business Health Dashboard**
   - Financial Score: XX/100 (trend)
   - Operational Score: XX/100 (trend)
   - Social Media Score: XX/100 (trend)
   - Goal Achievement: XX/100 (trend)
   - **Overall: XX/100** with status indicator

   **Financial Performance**
   - Revenue this week: $X,XXX
   - Revenue MTD: $X,XXX (XX% of $X,XXX target)
   - Expenses this week: $X,XXX
   - Expenses MTD: $X,XXX (XX% of budget)
   - Cash Flow: +/- $X,XXX
   - Outstanding: $X,XXX (X invoices, X overdue)

   **Operational Performance**
   - Tasks completed: X
   - Average cycle time: X days
   - Email response time: X hours
   - Pending high-priority: X items

   **Social Media Performance**
   - Posts published: X (LinkedIn: X, FB: X, IG: X, Twitter: X)
   - Total engagement: X (likes + comments + shares)
   - Engagement rate: X.X%
   - Follower growth: +X

   **Goal Progress**
   - List each goal from Business_Goals.md
   - Progress percentage
   - Status (On Track / At Risk / Behind)
   - Next milestone

   **Bottlenecks Identified**
   | Task/Process | Expected | Actual | Delay | Impact |
   |--------------|----------|--------|-------|--------|
   | [Task name]  | X days   | Y days | +Z    | [description] |

   **Proactive Recommendations**

   **💰 Cost Optimization**
   - [Service]: [Details, savings calculation, action]

   **📈 Process Improvements**
   - [Area]: [Issue, recommendation, expected benefit]

   **🚀 Growth Opportunities**
   - [Opportunity]: [Details, potential impact, suggested action]

   **⚠️ Risk Alerts**
   - [Risk]: [Description, impact, mitigation suggestion]

   **Upcoming This Week**
   - Key deadlines from Business_Goals.md
   - Important dates
   - Scheduled tasks

   **Action Items for Review**
   - [ ] Review cost optimization recommendations
   - [ ] Approve/reject suggested actions
   - [ ] Address critical bottlenecks
   - [ ] Follow up on overdue items

3. **Add Metadata**
   ```yaml
   ---
   generated: YYYY-MM-DDTHH:MM:SSZ
   period: YYYY-MM-DD to YYYY-MM-DD
   overall_score: XX/100
   status: excellent/good/fair/needs_attention
   critical_alerts: X
   ---
   ```

4. **Create Monday Morning Notification**
   - Create file in `Vault/Needs_Action/`
   - Filename: `BRIEFING_Weekly_Review_YYYY-MM-DD.md`
   - Content:
     ```markdown
     ---
     type: notification
     priority: high
     category: business_review
     generated: YYYY-MM-DDTHH:MM:SSZ
     ---

     # 📊 Weekly CEO Briefing Ready

     Your weekly business briefing for [Week Ending Date] has been generated.

     **Overall Health: XX/100** - [Status]

     **Highlights:**
     - Revenue: $X,XXX ([trend])
     - [Key achievement or concern]

     **Action Required:**
     - [X] critical alerts
     - [X] recommendations for review

     **View Full Briefing:** `Vault/Briefings/YYYY-MM-DD_Monday_Briefing.md`

     ---

     *Generated by AI Employee - CEO Briefing System*
     ```

5. **Archive Previous Briefings**
   - Move briefings older than 4 weeks to `Vault/Briefings/archives/`
   - Maintain last 4 weeks in main folder for easy access
   - Keep metadata for trend analysis

6. **Update Dashboard**
   - Add briefing generation log to `Vault/Dashboard.md`
   - Include overall score and status
   - Link to full briefing

See [briefing-template.md](./reference/briefing-template.md) for complete template.

---

## Security Safeguards

### Before Generating:
- ✅ All required data sources accessible
- ✅ Financial data synced (manage-accounting ran successfully)
- ✅ Social media metrics current (<48 hours old)
- ✅ Business_Goals.md exists and has valid targets

### Data Privacy:
- ✅ Briefings stored locally in Vault only
- ✅ No sensitive financial data sent to external services
- ✅ Client names anonymized in logs if configured
- ✅ Audit trail maintained for all briefings

### Recommendations:
- ✅ All recommendations advisory only (never auto-execute)
- ✅ Cost optimizations require human approval
- ✅ Process changes suggested, not implemented
- ✅ Risk alerts flagged, not acted upon

### Never Auto-Execute:
- ❌ Subscription cancellations (recommend only)
- ❌ Process changes
- ❌ Budget modifications
- ❌ Goal adjustments
- ❌ Resource reallocation

---

## Reference Files

**Progressive disclosure - load on demand:**

1. **[briefing-template.md](./reference/briefing-template.md)**
   - Complete briefing document template
   - Section descriptions
   - Formatting guidelines
   - Example briefings

2. **[analysis-framework.md](./reference/analysis-framework.md)**
   - Data collection procedures
   - Analysis methodologies
   - Scoring algorithms
   - Trend calculation logic

3. **[kpi-definitions.md](./reference/kpi-definitions.md)**
   - Key Performance Indicator definitions
   - Calculation formulas
   - Benchmark values
   - Scoring thresholds

4. **[recommendation-engine.md](./reference/recommendation-engine.md)**
   - Recommendation generation rules
   - Prioritization logic
   - Cost-benefit analysis methods
   - Risk assessment criteria

---

## Helper Scripts

### analyze_performance.py

**Purpose:** Collect data and calculate performance scores

**Usage:**
```bash
# Generate weekly performance analysis
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --period weekly

# Calculate scores only
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --calculate-scores

# Custom date range
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --start 2026-01-01 --end 2026-01-07

# JSON output for programmatic use
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --json

# Verbose mode (detailed logging)
python .claude/skills/generate-ceo-briefing/scripts/analyze_performance.py --verbose
```

---

### detect_bottlenecks.py

**Purpose:** Identify process, financial, and communication bottlenecks

**Usage:**
```bash
# Detect all bottlenecks
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py

# Focus on specific category
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py --category financial
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py --category operational
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py --category communication

# Set severity threshold (only report critical and high)
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py --min-severity high

# JSON output
python .claude/skills/generate-ceo-briefing/scripts/detect_bottlenecks.py --json
```

---

### generate_insights.py

**Purpose:** Generate proactive recommendations and insights

**Usage:**
```bash
# Generate all recommendations
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py

# Focus on cost optimization only
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py --focus cost-optimization

# Process improvements only
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py --focus process-improvement

# Growth opportunities only
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py --focus growth

# Set minimum savings threshold for recommendations
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py --min-savings 100

# JSON output
python .claude/skills/generate-ceo-briefing/scripts/generate_insights.py --json
```

---

## Integration with Other Skills

**Depends on data from:**
- `manage-accounting` → Financial data (revenue, expenses, invoices)
- `process-tasks` → Task completion, bottlenecks
- `process-emails` → Email metrics, response times
- `post-to-linkedin` → LinkedIn engagement metrics
- `post-to-social-media` → Facebook/Instagram metrics
- `post-to-twitter` → Twitter engagement metrics

**Provides insights to:**
- `Vault/Briefings/` → Weekly executive reports
- `Vault/Dashboard.md` → Business health status
- `Vault/Needs_Action/` → Monday morning notifications

**Workflow:**
```
Sunday 11:45 PM: Scheduled trigger
    ↓
1. analyze_performance.py: Collect data from all sources
    ↓
2. Calculate performance scores (Financial, Operational, Social, Goals)
    ↓
3. detect_bottlenecks.py: Identify issues and delays
    ↓
4. generate_insights.py: Create proactive recommendations
    ↓
5. Write comprehensive CEO briefing to Vault/Briefings/
    ↓
6. Create notification in Vault/Needs_Action/
    ↓
Monday Morning: User reviews briefing and approves recommended actions
```

---

## Automation Setup

### Scheduled Execution (Sunday 11:45 PM)

**Linux/Mac (cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 11:45 PM)
45 23 * * 0 cd /path/to/Autonomous-FTEs && claude-code "generate weekly briefing" >> /path/to/logs/briefing.log 2>&1
```

**Windows (Task Scheduler):**
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "claude-code" -Argument '"generate weekly briefing"' -WorkingDirectory "D:\Autonomous-FTEs"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 11:45PM
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
Register-ScheduledTask -TaskName "AI_Employee_Weekly_Briefing" -Action $action -Trigger $trigger -Principal $principal -Description "Generate weekly CEO briefing every Sunday night"
```

**Or use orchestrator.py:**
Add to your orchestrator schedule:
```python
schedule.every().sunday.at("23:45").do(lambda: subprocess.run(
    ["claude-code", "generate weekly briefing"],
    cwd="/path/to/Autonomous-FTEs"
))
```

---

## Dashboard Logging

All briefing generation logged to `Vault/Dashboard.md`:

```markdown
### [Timestamp] - CEO Briefing Generated

**Period:** [Start Date] to [End Date]
**Overall Score:** XX/100 - [Status]

**Summary:**
- Financial: XX/100 ([trend])
- Operational: XX/100 ([trend])
- Social Media: XX/100 ([trend])
- Goal Achievement: XX/100 ([trend])

**Critical Alerts:** X
**Recommendations:** X

**View Full Briefing:** [Vault/Briefings/YYYY-MM-DD_Monday_Briefing.md](Vault/Briefings/YYYY-MM-DD_Monday_Briefing.md)

**Notification Created:** Vault/Needs_Action/BRIEFING_Weekly_Review_YYYY-MM-DD.md
```

---

## Success Criteria

This skill works correctly when:

✅ Briefings auto-generate every Sunday at 11:45 PM
✅ All 5 data sources successfully collected (Financial, Operational, Email, Social, Goals)
✅ Performance scores accurately calculated (0-100 scale)
✅ Bottlenecks correctly identified and prioritized
✅ Recommendations relevant and actionable
✅ Cost savings calculations accurate
✅ Monday morning notification created in Needs_Action
✅ Overall business health score reflects actual performance
✅ Trend analysis shows historical comparison
✅ No false positives in recommendations
✅ All recommendations remain advisory (no auto-execution)
✅ Complete audit trail maintained

---

## Common Issues

**Briefing Not Generating on Schedule:**
- Check cron job / Task Scheduler configuration
- Verify orchestrator.py running
- Check system logs for errors: `tail -f /path/to/logs/briefing.log`
- Ensure system not sleeping at scheduled time

**Missing Financial Data:**
- Verify `manage-accounting` skill ran successfully
- Check Xero sync completed: `Vault/Accounting/Current_Month.md` updated
- Ensure `Vault/Business_Goals.md` has financial targets defined
- Run manual sync: `claude-code "sync accounting"`

**Incomplete Social Media Metrics:**
- Verify all social media skills operational
- Check metrics files exist:
  - `Vault/Social_Media/LinkedIn/metrics.json`
  - `Vault/Social_Media/Facebook/metrics.json`
  - `Vault/Social_Media/Instagram/metrics.json`
  - `Vault/Social_Media/Twitter/metrics.json`
- Run manual metric updates if needed

**Low Accuracy in Bottleneck Detection:**
- Update task duration estimates in `Vault/Business_Goals.md`
- Review bottleneck classification rules in [analysis-framework.md](./reference/analysis-framework.md)
- Adjust sensitivity thresholds if too many/few bottlenecks flagged
- Ensure task metadata includes expected vs actual completion times

**Irrelevant Recommendations:**
- Review and update [recommendation-engine.md](./reference/recommendation-engine.md)
- Adjust minimum savings threshold for cost optimizations
- Update subscription list with your actual services
- Refine recommendation prioritization logic

**Performance Score Inaccurate:**
- Verify scoring weights in [kpi-definitions.md](./reference/kpi-definitions.md)
- Check benchmark values appropriate for your business size
- Ensure all KPIs have valid targets in `Vault/Business_Goals.md`
- Review score calculation formulas in [analysis-framework.md](./reference/analysis-framework.md)

---

## External Dependencies

**Required Skills:**
- `manage-accounting` → Financial data
- `process-tasks` → Operational data
- `process-emails` → Communication metrics
- `post-to-linkedin` → LinkedIn metrics
- `post-to-social-media` → Facebook/Instagram metrics (Gold tier)
- `post-to-twitter` → Twitter metrics (Gold tier)

**Required Vault Files:**
- `Vault/Business_Goals.md` → Targets and goals
- `Vault/Accounting/Current_Month.md` → Financial transactions
- `Vault/Social_Media/*/metrics.json` → Social media performance

**Optional:**
- Historical briefings for trend analysis
- Custom benchmark values for your industry
- Enhanced KPI definitions

---

## Setup Checklist

Before first use:

- [ ] All dependent skills operational (accounting, tasks, emails, social media)
- [ ] `Vault/Business_Goals.md` configured with:
  - [ ] Financial targets (revenue, expenses, cash flow)
  - [ ] Operational targets (task completion, response times)
  - [ ] Social media targets (posts/week, engagement rate, follower growth)
  - [ ] Quarterly/annual goals with milestones
- [ ] `Vault/Briefings/` folder created
- [ ] `Vault/Briefings/archives/` folder created
- [ ] Social media metrics files initialized
- [ ] Reference files customized for your business:
  - [ ] [briefing-template.md](./reference/briefing-template.md)
  - [ ] [kpi-definitions.md](./reference/kpi-definitions.md)
  - [ ] [recommendation-engine.md](./reference/recommendation-engine.md)
- [ ] Scheduled task configured (Sunday 11:45 PM)
- [ ] Test run completed manually: `claude-code "generate weekly briefing"`
- [ ] Verify Monday notification appears in Needs_Action

---

## Example Output Preview

```markdown
# Monday Morning CEO Briefing
## Week Ending: January 7, 2026

### Executive Summary
Strong week with revenue exceeding target by 12%. One operational bottleneck identified in client communication. Overall business health: **82/100** (Good 📗)

### Business Health Dashboard
- **Financial:** 88/100 ↗️ (+3 from last week)
- **Operational:** 76/100 ↘️ (-8 from last week)
- **Social Media:** 82/100 ↗️ (+5 from last week)
- **Goal Achievement:** 81/100 → (stable)

**Overall: 82/100** - Good 📗

### Financial Performance
- **This Week:** $2,450 revenue, $820 expenses → $1,630 profit
- **MTD:** $4,500 revenue (45% of $10,000 target) ✅ On Track
- **Outstanding:** $1,200 (2 invoices, 0 overdue)
- **Cash Flow:** Positive, trending up

### Proactive Recommendations

**💰 Cost Optimization Opportunity**
- **Notion Team Plan**: No activity in 47 days. Cost: $15/month
- **Action:** Cancel subscription (already using Obsidian)
- **Annual Savings:** $180

**⚠️ Bottleneck Alert**
- **Client B Proposal**: Expected 2 days, took 5 days (+3 day delay)
- **Impact:** Potential revenue delay
- **Recommendation:** Review proposal template, consider automation

---

*Generated by AI Employee CEO Briefing System v1.0*
```

---

*Skill Version: 1.0*
*Last Updated: 2026-01-12*
*Branch: feat/gold-business-intelligence*
*Dependencies: manage-accounting, process-tasks, process-emails, post-to-linkedin, post-to-social-media, post-to-twitter*

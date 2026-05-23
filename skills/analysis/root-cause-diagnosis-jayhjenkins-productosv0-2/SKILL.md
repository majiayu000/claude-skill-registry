---
name: root-cause-diagnosis
description: Use when metrics drop or spike unexpectedly - systematically investigates using 4-dimension segmentation (People, Geography, Technology, Time), intrinsic vs extrinsic factors, and hypothesis table method to identify root cause
---

# Root Cause Diagnosis

## Purpose

Systematically narrow down the root cause of unexpected metric changes by segmenting data, distinguishing internal vs. external factors, and testing hypotheses against observed patterns. Prevents jumping to conclusions and ensures evidence-based decision-making.

## When to Use This Skill

Activate automatically when:
- Key metrics drop or spike unexpectedly
- A/B test results show unexpected patterns
- User behavior changes suddenly
- Post-mortem analysis needed after incident
- Leadership asks "what happened?"
- `metric-diagnosis` workflow investigates metric changes
- Need to validate suspected causes

**When NOT to use:**
- Change was expected (planned feature release, known seasonality)
- Metric is within normal variance
- Root cause is already confirmed
- Data quality issue is obvious (reporting broken)

## The Iron Law

**ASK CLARIFYING QUESTIONS FIRST - DON'T GUESS**

Most metric problems are more narrow than initially stated. The problem might only affect:
- Specific user segments
- Certain geographies
- Particular platforms
- Limited time windows

Narrow the scope before hypothesizing causes.

## The 4 Critical Dimensions

Always segment data across these dimensions:

### Dimension 1: People (User Segments)

**Questions to ask:**
- Does it affect all users equally?
- Specific age demographics?
- New vs. returning users?
- Free vs. paid users?
- Business vs. consumer users?
- Power users vs. casual users?
- Specific personas or cohorts?

**Example:** "Snapchat usage down 10%" → Actually: "Down among kids in Australia, not adults or other regions"

### Dimension 2: Geography

**Questions to ask:**
- Specific countries affected?
- Certain cities or regions?
- Urban vs. rural areas?
- Climate zones?
- Time zones?
- Regulatory regions (GDPR, etc.)?

**Example:** "Square usage drops steadily" → Actually: "Only in Boston in fall, not Atlanta" (weather: farmers markets close)

### Dimension 3: Technology (Platform)

**Questions to ask:**
- iOS vs. Android?
- Web vs. mobile app?
- Desktop vs. mobile web?
- Specific browser versions?
- Operating system versions?
- Device types (phone, tablet)?
- Network types (WiFi, cellular)?

**Example:** "Microsoft Teams downloads down 50%" → Actually: "Web and desktop, not mobile; all browsers equally"

### Dimension 4: Time

**Questions to ask:**
- When did it start exactly?
- Is it constant or fluctuating?
- Day of week patterns?
- Time of day patterns?
- Seasonal effects?
- Holiday impacts?
- Gradual decline or sudden drop?

**Example:** "Tinder usage dropped" → Actually: "Among professionals in metro areas overnight" (competing app launched)

## Intrinsic vs. Extrinsic Factors

After narrowing scope, brainstorm potential causes in both categories:

### Intrinsic Factors (Internal)

**Definition:** Changes you or your company made

**Examples:**
- Bugs introduced
- New features deployed
- UI/UX changes
- Algorithm adjustments
- A/B experiments running
- Policy changes
- Pricing changes
- Server performance issues
- Cross-team feature launches

**Investigation approach:**
- Review recent releases (past week/month)
- Check A/B test logs
- Talk to engineering about deployments
- Review other team launches
- Check server monitoring

### Extrinsic Factors (External)

**Definition:** Changes in the world outside your control

**Examples:**
- **Competitor actions:** New app launched, pricing change, marketing campaign
- **Economic factors:** Recession, inflation, job market
- **Seasonal patterns:** Weather, holidays, school schedules
- **External events:** News events, cultural moments, pandemics
- **Market shifts:** User behavior trends, platform changes
- **Regulatory changes:** New laws, compliance requirements

**Investigation approach:**
- Monitor competitor announcements
- Review industry news
- Check economic indicators
- Consider calendar/seasonal effects
- Talk to sales and customer success teams

## The Hypothesis Table Method

**Purpose:** Test multiple hypotheses against data systematically

### Step 1: Create Table Structure

**Columns:** Data points you observed
- "Kids usage DOWN"
- "Adults usage UNCHANGED"
- "US affected"
- "Europe unaffected"
- "iOS affected"
- "Android unaffected"

**Rows:** Potential causes (2-3 intrinsic, 2-3 extrinsic)

### Step 2: Fill in Predictions

For each cause-data intersection:
- ↑ = This cause would increase this metric
- ↓ = This cause would decrease this metric
- → = This cause wouldn't affect this metric
- ? = Uncertain prediction

### Step 3: Match Patterns

Look for rows where ALL predictions match observed data:
- If predictions align with observations → Possible cause
- If predictions contradict observations → Rule out

### Step 4: Request Differentiating Data

If multiple causes fit:
- Ask for additional data points that differ between hypotheses
- Narrow to single cause through additional segmentation

### Example Table: Snapchat Usage Down

| Cause | Kids ↓ | Adults → | US ↓ | EU → | iOS ↓ | Android → |
|-------|--------|----------|------|------|-------|-----------|
| iOS bug in latest update | ✓ ? | ✓ ? | ✗ All | ✗ All | ✓ YES | ✓ NO |
| School started (US) | ✓ YES | ✓ NO | ✓ YES | ✓ NO | ✗ All | ✗ All |
| TikTok marketing to teens | ✓ YES | ✓ NO | ✗ Global | ✗ Global | ✗ All | ✗ All |

**Pattern match:** "School started (US)" fits all observations → Likely cause

## Systematic Investigation Sequence

Follow this order to maximize efficiency:

### Phase 1: Data Quality Verification (5 minutes)

**Before investigating product issues, confirm data is real:**

1. Check reporting systems working
2. Compare multiple data sources
3. Verify tracking not broken
4. Confirm sample sizes sufficient

**Red flags:**
- Metric went to exactly zero (likely tracking broken)
- Change happened at exact midnight (likely pipeline issue)
- Only affects one data source

### Phase 2: Narrow the Scope (15 minutes)

**Ask 4-dimension clarifying questions:**

1. People: Which user segments?
2. Geography: Which locations?
3. Technology: Which platforms?
4. Time: When exactly, what pattern?

**Output:** Narrow problem statement (not "usage down" but "iOS teen usage in US down 10% starting Sept 1")

### Phase 3: Internal Investigation (30 minutes)

**Check intrinsic factors first (easier to fix):**

1. Recent releases by your team (past week)
2. A/B experiments running
3. Configuration changes
4. Cross-team launches affecting you
5. Infrastructure/performance issues

**Stakeholders to consult:**
- Engineering: Recent deploys, bugs reported
- Data: Tracking changes, pipeline issues
- Product: Other team launches

### Phase 4: External Investigation (30 minutes)

**Check extrinsic factors if internal ruled out:**

1. Competitor news and launches
2. Industry events and trends
3. Seasonal/calendar effects
4. Economic indicators
5. External PR or news

**Stakeholders to consult:**
- Sales: Customer feedback, competitive intel
- Marketing: Campaign timing, market trends
- Customer Success: Support tickets, user complaints

### Phase 5: Hypothesis Testing (Ongoing)

**Build and test hypotheses:**

1. List 4-6 potential causes (mix intrinsic/extrinsic)
2. Create hypothesis table
3. Predict impact on each data segment
4. Match predictions to observations
5. Request additional data to differentiate
6. Narrow to 1-2 most likely causes

## Common Diagnostic Patterns

### Pattern 1: Gradual Decline Over Weeks

**Likely causes:**
- Competitor gaining market share
- Degrading product experience (tech debt, performance)
- Seasonal trend
- User behavior shift

**Investigation:**
- Compare to competitor growth rates
- Check performance metrics trends
- Review year-over-year seasonality
- Survey users about satisfaction

### Pattern 2: Sudden Overnight Drop

**Likely causes:**
- Bug introduced in recent release
- Breaking change in API/integration
- Competitor launched major feature
- External event (news, regulation)

**Investigation:**
- Review deployments in past 24-48 hours
- Check error logs and monitoring
- Scan news and competitor announcements
- Verify tracking still functional

### Pattern 3: Recurring Pattern (Weekly, Daily)

**Likely causes:**
- Usage behavior patterns (weekday vs. weekend)
- Scheduled batch processes
- Time zone effects
- Cultural/lifestyle patterns

**Investigation:**
- Compare to historical patterns (is this new?)
- Check across multiple weeks
- Segment by geography and user type

### Pattern 4: Segment-Specific Issue

**Likely causes:**
- Platform-specific bug
- Demographic-targeted competitor
- Localized event or regulation
- A/B test gone wrong

**Investigation:**
- Reproduce issue on affected segment
- Check A/B test assignments
- Review segment-specific deployments
- Talk to affected users directly

## Stakeholder Consultation Strategy

**Purpose:** Gather insights from teams with different data access

### When to Talk to Sales

**Best for:**
- Enterprise customer behavior changes
- Competitive intelligence
- Renewal and churn patterns
- Feature request trends

**Questions to ask:**
- "Any customers mentioning this issue?"
- "Have you heard about competitor changes?"
- "Any recent losses to specific competitors?"

### When to Talk to Customer Success

**Best for:**
- Support ticket trends
- User sentiment and feedback
- Onboarding friction points
- Feature adoption patterns

**Questions to ask:**
- "Any spike in support tickets?"
- "What are users saying about [feature]?"
- "Any common complaints this week?"

### When to Talk to Marketing

**Best for:**
- Campaign timing and impact
- Promotional effects
- Brand perception changes
- Acquisition channel performance

**Questions to ask:**
- "Any campaigns end recently?"
- "Changes in acquisition costs?"
- "New channels tested?"

### When to Talk to Engineering

**Best for:**
- Recent deployments and changes
- Performance and reliability issues
- A/B test implementations
- Infrastructure events

**Questions to ask:**
- "Any deploys in past 48 hours?"
- "Performance regressions?"
- "Error rate changes?"

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to conclusions without data | Ask 4-dimension questions first |
| Only considering intrinsic factors | Always brainstorm extrinsic factors too |
| Accepting first hypothesis that fits | Test multiple hypotheses systematically |
| Not validating data quality | Check reporting systems before investigating |
| Ignoring stakeholder insights | Consult sales, CS, engineering teams |
| Binary thinking (ship/rollback only) | Explore mitigation strategies first |

## Anti-Rationalization Blocks

| Rationalization | Reality |
|-----------------|---------|
| "It's obviously a bug" | Could be competitor, seasonality, user behavior |
| "Must be the release yesterday" | Ask segmentation questions before assuming |
| "This only happens to us" | Check if competitors experiencing same |
| "Too complicated to investigate" | Systematic process makes it manageable |
| "Let's just rollback everything" | Understand cause before reversing changes |

## Success Criteria

Root cause diagnosis succeeds when:
- Problem narrowed to specific segments (4 dimensions)
- 4-6 hypotheses brainstormed (intrinsic + extrinsic)
- Hypothesis table created with predictions
- Patterns matched against observed data
- Most likely cause identified (or top 2-3 candidates)
- Data quality verified
- Stakeholders consulted for insights
- Recommended next steps clear (fix, monitor, mitigate)

## Real-World Examples

### Example 1: Microsoft Teams Downloads Down 50%

**Initial statement:** "New app downloads down 50% from last week"

**Phase 1: Narrow the scope**
- Geography: Predominantly US and Europe
- Users: Enterprise customers, not consumers
- Platform: Web and desktop primarily, some mobile
- Time: Started last week, consistent since
- Other metrics: Usage unchanged (existing users still active)

**Phase 2: Hypothesis brainstorming**

**Intrinsic factors:**
1. Bug in download flow (dismissed - all browsers affected equally)
2. Recent release broke something (dismissed - no recent release)
3. A/B test reducing visibility (dismissed - not running experiments)

**Extrinsic factors:**
1. Marketing promotion ended (MATCH!)
2. Competitor launch (dismissed - no major launches)
3. Economic downturn (dismissed - usage unchanged)

**Phase 3: Investigation**
- Talk to marketing: "We were running 50% off promotion for enterprise customers switching from Slack"
- Promotion ended last weekend
- Downloads during promo = artificially inflated baseline
- Current downloads = normal baseline

**Root cause:** End of promotional campaign created false "decline" (actually return to normal)

**Action:** None needed - metric will stabilize. Use normal baseline for future comparisons.

### Example 2: Snapchat Usage Drop

**Initial statement:** "Snapchat usage down 10%"

**Phase 1: Narrow the scope**
- People: Kids affected, adults unchanged
- Geography: US affected, Europe unaffected
- Platform: Both iOS and Android
- Time: Started September 1st

**Phase 2: Hypothesis table**

| Cause | Kids ↓ | Adults → | US ↓ | EU → |
|-------|--------|----------|------|------|
| iOS bug | ✗ Both | ✗ Both | ✗ All | ✗ All |
| School started | ✓ YES | ✓ NO | ✓ YES | ✗ Sept starts later |
| Competitor | ✗ Both | ✗ Both | ✗ Global | ✗ Global |

**Root cause:** US school year started September 1st
- Kids have less free time during school
- Adults unaffected (not in school)
- Europe schools start later (unaffected in early Sept)

**Action:** Monitor through September to confirm seasonal pattern. Compare to previous years. No product changes needed - expected seasonal variation.

### Example 3: Tinder Usage Drop Among Professionals

**Initial statement:** "Tinder usage declined"

**Phase 1: Narrow the scope**
- People: College-educated professionals
- Geography: Major metro areas (NYC, SF, Chicago)
- Platform: All platforms
- Time: Overnight drop

**Phase 2: Hypothesis brainstorming**

**Intrinsic:** Nothing deployed, no bugs, no pricing changes

**Extrinsic:**
1. Competitor launch targeting professionals
2. Negative news coverage
3. Regulatory change

**Phase 3: Investigation**
- Industry research: Competing dating app (Hinge, The League) launched marketing campaign targeting professionals
- Ad campaign: "Dating app for professionals, not hookups"
- Positioning directly competitive to Tinder

**Root cause:** Competitor marketing campaign successfully attracted target demographic

**Action:** 
- Counter-positioning campaign
- Feature development for relationship-seeking users
- Monitor competitor strategy evolution

### Example 4: Airbnb Booking Value Drop in LA Summer

**Initial statement:** "Average booking value down in Los Angeles"

**Phase 1: Narrow the scope**
- Geography: Los Angeles specifically
- Time: Summer months
- Users: Younger travelers (18-25)
- Booking type: Shorter stays (2-3 days)

**Phase 2: Hypothesis brainstorming**

**Intrinsic:**
1. Algorithm showing cheaper properties first (check - no change)
2. New low-cost inventory added (check - yes, some increase)

**Extrinsic:**
1. Budget airlines offering discount LA flights (MATCH!)
2. Economic downturn (dismissed - other cities unaffected)
3. Competitor taking high-value bookings (dismissed - market share stable)

**Root cause:** Multiple discount airlines launched summer routes to LA, attracting younger budget travelers who book cheaper accommodations

**Action:** None needed - increased volume of lower-value bookings is net positive for revenue. Adjust forecasting models to account for seasonal booking value variation.

## Related Skills

- **north-star-alignment**: Assesses whether metric change impacts top-line goals (Step 4 of diagnosis)
- **funnel-metric-mapping**: Uses funnel location to narrow problem scope
- **tradeoff-evaluation**: Evaluates whether to rollback, keep, or mitigate after diagnosis
- **metric-diagnosis** (workflow): Orchestrates root cause investigation systematically
- **meeting-synthesis**: Gathers customer evidence during investigation

## Integration Points

**Called by workflows:**
- `metric-diagnosis` - Steps 1-3: Complete investigation process
- `tradeoff-decision` - May use to understand why metrics changed

**May call:**
- `meeting-synthesis` to find customer evidence of issues
- `north-star-alignment` to assess strategic impact
- `funnel-metric-mapping` to identify which stage is affected


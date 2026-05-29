---
name: alert-manager
description: Sets up and manages alerts for critical SEO and GEO metrics including ranking drops, traffic changes, technical issues, and competitor movements. Enables proactive monitoring and quick response to issues.
---

# Alert Manager

This skill helps you set up proactive monitoring alerts for critical SEO and GEO metrics. Get notified when rankings drop, traffic changes significantly, technical issues occur, or competitors make moves.

## When to Use This Skill

- Setting up SEO monitoring systems
- Creating ranking drop alerts
- Monitoring technical SEO health
- Tracking competitor movements
- Alerting on content performance changes
- Monitoring GEO/AI visibility changes
- Setting up brand mention alerts

## What This Skill Does

1. **Alert Configuration**: Sets up custom alert thresholds
2. **Multi-Metric Monitoring**: Tracks rankings, traffic, technical issues
3. **Threshold Management**: Defines when alerts trigger
4. **Priority Classification**: Categorizes alerts by severity
5. **Notification Setup**: Configures how alerts are delivered
6. **Alert Response Plans**: Creates action plans for each alert type
7. **Alert History**: Tracks alert patterns over time

## How to Use

### Set Up Alerts

```
Set up SEO monitoring alerts for [domain]
```

```
Create ranking drop alerts for my top 20 keywords
```

### Configure Specific Alerts

```
Alert me when [specific condition]
```

```
Set up competitor monitoring for [competitor domains]
```

### Review Alert System

```
Review and optimize my current SEO alerts
```

## Instructions

When a user requests alert setup:

1. **Define Alert Categories**

   ```markdown
   ## SEO Alert System Configuration
   
   **Domain**: [domain]
   **Configured Date**: [date]
   
   ### Alert Categories
   
   | Category | Description | Typical Urgency |
   |----------|-------------|-----------------|
   | Ranking Alerts | Keyword position changes | Medium-High |
   | Traffic Alerts | Organic traffic fluctuations | High |
   | Technical Alerts | Site health issues | Critical |
   | Backlink Alerts | Link profile changes | Medium |
   | Competitor Alerts | Competitor movements | Low-Medium |
   | GEO Alerts | AI visibility changes | Medium |
   | Brand Alerts | Brand mentions and reputation | Medium |
   ```

2. **Configure Ranking Alerts**

   ```markdown
   ## Ranking Alerts
   
   ### Position Drop Alerts
   
   | Alert Name | Condition | Threshold | Priority | Action |
   |------------|-----------|-----------|----------|--------|
   | Critical Drop | Any top 3 keyword drops 5+ positions | Position change ≥5 | 🔴 Critical | Immediate investigation |
   | Major Drop | Top 10 keyword drops out of top 10 | Position >10 | 🔴 High | Same-day review |
   | Moderate Drop | Any keyword drops 10+ positions | Position change ≥10 | 🟡 Medium | Weekly review |
   | Competitor Overtake | Competitor passes you for key term | Comp position < yours | 🟡 Medium | Analysis needed |
   
   ### Position Improvement Alerts
   
   | Alert Name | Condition | Threshold | Priority |
   |------------|-----------|-----------|----------|
   | New Top 3 | Keyword enters top 3 | Position ≤3 | 🟢 Positive |
   | Page 1 Entry | Keyword enters top 10 | Position ≤10 | 🟢 Positive |
   | Significant Climb | Keyword improves 10+ positions | Change ≥+10 | 🟢 Positive |
   
   ### SERP Feature Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Snippet Lost | Lost featured snippet ownership | 🔴 High |
   | Snippet Won | Won new featured snippet | 🟢 Positive |
   | AI Overview Change | Appeared/disappeared in AI Overview | 🟡 Medium |
   
   ### Keywords to Monitor
   
   | Keyword | Current Rank | Alert Threshold | Priority |
   |---------|--------------|-----------------|----------|
   | [keyword 1] | [X] | Drop ≥3 | 🔴 Critical |
   | [keyword 2] | [X] | Drop ≥5 | 🔴 High |
   | [keyword 3] | [X] | Drop ≥10 | 🟡 Medium |
   ```

3. **Configure Traffic Alerts**

   ```markdown
   ## Traffic Alerts
   
   ### Traffic Decline Alerts
   
   | Alert Name | Condition | Threshold | Priority |
   |------------|-----------|-----------|----------|
   | Traffic Crash | Day-over-day decline | ≥50% drop | 🔴 Critical |
   | Significant Drop | Week-over-week decline | ≥30% drop | 🔴 High |
   | Moderate Decline | Month-over-month decline | ≥20% drop | 🟡 Medium |
   | Trend Warning | 3 consecutive weeks decline | Any decline | 🟡 Medium |
   
   ### Traffic Anomaly Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Traffic Spike | Unusual increase | 🟢 Investigate |
   | Zero Traffic | Page receiving 0 visits | 🔴 High |
   | Bot Traffic | Unusual traffic pattern | 🟡 Medium |
   
   ### Page-Level Alerts
   
   | Page Type | Alert Condition | Priority |
   |-----------|-----------------|----------|
   | Homepage | Any 20%+ decline | 🔴 Critical |
   | Top 10 pages | Any 30%+ decline | 🔴 High |
   | Conversion pages | Any 25%+ decline | 🔴 High |
   | Blog posts | Any 40%+ decline | 🟡 Medium |
   
   ### Conversion Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Conversion Drop | Organic conversions down 30%+ | 🔴 Critical |
   | CVR Decline | Conversion rate drops 20%+ | 🔴 High |
   ```

4. **Configure Technical SEO Alerts**

   ```markdown
   ## Technical SEO Alerts
   
   ### Critical Technical Alerts
   
   | Alert Name | Condition | Priority | Response Time |
   |------------|-----------|----------|---------------|
   | Site Down | HTTP 5xx errors | 🔴 Critical | Immediate |
   | SSL Expiry | Certificate expiring in 14 days | 🔴 Critical | Same day |
   | Robots.txt Block | Important pages blocked | 🔴 Critical | Same day |
   | Index Dropped | Pages dropping from index | 🔴 Critical | Same day |
   
   ### Crawl & Index Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Crawl Errors Spike | Errors increase 50%+ | 🔴 High |
   | New 404 Pages | 404 errors on important pages | 🟡 Medium |
   | Redirect Chains | 3+ redirect hops detected | 🟡 Medium |
   | Duplicate Content | New duplicates detected | 🟡 Medium |
   | Index Coverage Drop | Indexed pages decline 10%+ | 🔴 High |
   
   ### Performance Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Core Web Vitals Fail | CWV drops to "Poor" | 🔴 High |
   | Page Speed Drop | Load time increases 50%+ | 🟡 Medium |
   | Mobile Issues | Mobile usability errors | 🔴 High |
   
   ### Security Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Security Issue | GSC security warning | 🔴 Critical |
   | Manual Action | Google manual action | 🔴 Critical |
   | Malware Detected | Site flagged for malware | 🔴 Critical |
   ```

5. **Configure Backlink Alerts**

   ```markdown
   ## Backlink Alerts
   
   ### Link Loss Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | High-Value Link Lost | DA 70+ link removed | 🔴 High |
   | Multiple Links Lost | 10+ links lost in a day | 🟡 Medium |
   | Referring Domain Lost | Lost entire domain's links | 🟡 Medium |
   
   ### Link Gain Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | High-Value Link | New DA 70+ link | 🟢 Positive |
   | Suspicious Links | Many low-quality links | 🟡 Review |
   | Negative SEO | Spam link attack pattern | 🔴 High |
   
   ### Link Profile Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Toxic Score Increase | Toxic score up 20%+ | 🔴 High |
   | Anchor Over-Optimization | Exact match anchors >30% | 🟡 Medium |
   ```

6. **Configure Competitor Alerts**

   ```markdown
   ## Competitor Monitoring Alerts
   
   ### Ranking Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Competitor Overtake | Competitor passes you | 🟡 Medium |
   | Competitor Top 3 | Competitor enters top 3 on key term | 🟡 Medium |
   | Competitor Content | Competitor publishes on your topic | 🟢 Info |
   
   ### Activity Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | New Backlinks | Competitor gains high-DA link | 🟢 Info |
   | Content Update | Competitor updates ranking content | 🟢 Info |
   | New Content | Competitor publishes new content | 🟢 Info |
   
   ### Competitors to Monitor
   
   | Competitor | Domain | Monitor Keywords | Alert Priority |
   |------------|--------|------------------|----------------|
   | [Competitor 1] | [domain] | [X] keywords | High |
   | [Competitor 2] | [domain] | [X] keywords | Medium |
   | [Competitor 3] | [domain] | [X] keywords | Low |
   ```

7. **Configure GEO/AI Alerts**

   ```markdown
   ## GEO (AI Visibility) Alerts
   
   ### AI Citation Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Citation Lost | Lost AI Overview citation | 🟡 Medium |
   | Citation Won | New AI Overview citation | 🟢 Positive |
   | Citation Position Drop | Dropped from 1st to 3rd+ source | 🟡 Medium |
   | New AI Overview | AI Overview appears for tracked keyword | 🟢 Info |
   
   ### GEO Trend Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Citation Rate Drop | AI citation rate drops 20%+ | 🔴 High |
   | GEO Competitor | Competitor cited where you're not | 🟡 Medium |
   ```

8. **Configure Brand Alerts**

   ```markdown
   ## Brand Monitoring Alerts
   
   ### Mention Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Brand Mention | New brand mention online | 🟢 Info |
   | Negative Mention | Negative sentiment mention | 🔴 High |
   | Review Alert | New review on key platforms | 🟡 Medium |
   | Unlinked Mention | Brand mention without link | 🟢 Opportunity |
   
   ### Reputation Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Review Rating Drop | Average rating drops | 🔴 High |
   | Negative Press | Negative news article | 🔴 High |
   | Competitor Comparison | Named in competitor comparison | 🟡 Medium |
   ```

9. **Define Alert Response Plans**

   ```markdown
   ## Alert Response Plans
   
   ### Critical Alert Response (🔴)
   
   **Response Time**: Immediate (within 1 hour)
   
   | Alert Type | Immediate Actions |
   |------------|-------------------|
   | Site Down | 1. Check server status 2. Contact hosting 3. Check DNS |
   | Traffic Crash | 1. Check for algorithm update 2. Review GSC errors 3. Check competitors |
   | Manual Action | 1. Review GSC message 2. Identify issue 3. Begin remediation |
   | Critical Rank Drop | 1. Check if page indexed 2. Review SERP 3. Analyze competitors |
   
   ### High Priority Response (🔴/🟡)
   
   **Response Time**: Same day
   
   | Alert Type | Actions |
   |------------|---------|
   | Major Rank Drops | Analyze cause, create recovery plan |
   | Traffic Decline | Investigate source, check technical issues |
   | Backlink Loss | Attempt recovery outreach |
   | CWV Failure | Diagnose and fix performance issues |
   
   ### Medium Priority Response (🟡)
   
   **Response Time**: Within 48 hours
   
   | Alert Type | Actions |
   |------------|---------|
   | Moderate Rank Changes | Monitor trend, plan content updates |
   | Competitor Movement | Analyze competitor changes |
   | New 404s | Set up redirects, update internal links |
   
   ### Low Priority (🟢)
   
   **Response Time**: Weekly review
   
   | Alert Type | Actions |
   |------------|---------|
   | Positive Changes | Document wins, understand cause |
   | Info Alerts | Log for trend analysis |
   ```

10. **Set Up Alert Delivery**

    ```markdown
    ## Alert Notification Setup
    
    ### Notification Channels
    
    | Priority | Channels | Frequency |
    |----------|----------|-----------|
    | 🔴 Critical | Email + SMS + Slack | Immediate |
    | 🔴 High | Email + Slack | Immediate |
    | 🟡 Medium | Email + Slack | Daily digest |
    | 🟢 Low | Email | Weekly digest |
    
    ### Alert Recipients
    
    | Role | Critical | High | Medium | Low |
    |------|----------|------|--------|-----|
    | SEO Manager | ✅ | ✅ | ✅ | ✅ |
    | Dev Team | ✅ | ✅ (tech only) | ❌ | ❌ |
    | Marketing Lead | ✅ | ✅ | ❌ | ❌ |
    | Executive | ✅ | ❌ | ❌ | ❌ |
    
    ### Alert Suppression
    
    - Suppress duplicate alerts for 24 hours
    - Don't alert on known issues (maintenance windows)
    - Batch low-priority alerts into digests
    
    ### Alert Escalation
    
    | If No Response In | Escalate To |
    |-------------------|-------------|
    | 1 hour (Critical) | SEO Manager → Director |
    | 4 hours (High) | Team Lead → Manager |
    | 24 hours (Medium) | Team → Lead |
    ```

11. **Create Alert Summary**

    ```markdown
    # SEO Alert System Summary
    
    **Domain**: [domain]
    **Configured**: [date]
    **Total Active Alerts**: [X]
    
    ## Alert Count by Category
    
    | Category | Critical | High | Medium | Low | Total |
    |----------|----------|------|--------|-----|-------|
    | Rankings | [X] | [X] | [X] | [X] | [X] |
    | Traffic | [X] | [X] | [X] | [X] | [X] |
    | Technical | [X] | [X] | [X] | [X] | [X] |
    | Backlinks | [X] | [X] | [X] | [X] | [X] |
    | Competitors | [X] | [X] | [X] | [X] | [X] |
    | GEO | [X] | [X] | [X] | [X] | [X] |
    | **Total** | **[X]** | **[X]** | **[X]** | **[X]** | **[X]** |
    
    ## Quick Reference
    
    ### If You Get a Critical Alert
    
    1. Don't panic
    2. Check alert details
    3. Follow response plan
    4. Document actions taken
    5. Update stakeholders
    
    ### Weekly Alert Review Checklist
    
    - [ ] Review all alerts triggered
    - [ ] Identify patterns
    - [ ] Adjust thresholds if needed
    - [ ] Update response plans
    - [ ] Clean up false positives
    ```

## Example

**User**: "Set up ranking drop alerts for my top keywords"

**Output**:

```markdown
## Ranking Alert Configuration

### Critical Keywords (Immediate Alert)

| Keyword | Current | Alert If | Priority |
|---------|---------|----------|----------|
| best project management software | 2 | Drops to 5+ | 🔴 Critical |
| project management tools | 4 | Drops to 8+ | 🔴 Critical |
| team collaboration software | 1 | Any drop | 🔴 Critical |

### Important Keywords (Same-Day Alert)

| Keyword | Current | Alert If | Priority |
|---------|---------|----------|----------|
| agile project management | 7 | Drops out of top 10 | 🔴 High |
| kanban software | 9 | Drops out of top 10 | 🔴 High |

### Alert Response Plan

**If Critical Keyword Drops**:
1. Check if page is still indexed (site:url)
2. Look for algorithm update announcements
3. Analyze what changed in SERP
4. Review competitor ranking changes
5. Check for technical issues on page
6. Create recovery action plan within 24 hours

**Notification**: Email + Slack to SEO team immediately
```

## Tips for Success

1. **Start simple** - Don't create too many alerts initially
2. **Tune thresholds** - Adjust based on normal fluctuations
3. **Avoid alert fatigue** - Too many alerts = ignored alerts
4. **Document response plans** - Know what to do when alerts fire
5. **Review regularly** - Alerts need maintenance as your SEO matures
6. **Include positive alerts** - Track wins, not just problems

## Related Skills

- [rank-tracker](../rank-tracker/) - Ranking data for alerts
- [backlink-analyzer](../backlink-analyzer/) - Backlink monitoring
- [technical-seo-checker](../../optimize/technical-seo-checker/) - Technical monitoring
- [performance-reporter](../performance-reporter/) - Alert summaries in reports


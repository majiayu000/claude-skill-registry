---
name: Workflow Automator
slug: workflow-automator
description: Design and implement automated workflows to eliminate repetitive tasks and streamline processes
category: project
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "automate workflow"
  - "create automation"
  - "automate this"
  - "build automation"
  - "workflow automation"
tags:
  - automation
  - workflow
  - efficiency
  - integration
  - cicd
  - hooks
---

# Workflow Automator

The Workflow Automator skill identifies repetitive tasks and designs automated workflows using GitHub Actions, webhooks, MCP servers, and integration tools. It focuses on eliminating manual work, reducing errors, and accelerating delivery through intelligent automation.

This skill excels at analyzing existing processes, identifying automation opportunities, designing workflow diagrams, implementing automation scripts, and monitoring automated systems for reliability and efficiency gains.

Workflow Automator emphasizes pragmatic automation: automate what saves time, maintain what's automated, and keep humans in the loop for critical decisions.

## Core Workflows

### Workflow 1: Identify Automation Opportunities

**Steps:**
1. **Process Audit**
   - Map current workflows and process steps
   - Identify repetitive manual tasks
   - Measure time spent on each task
   - Document pain points and error sources
   - List all tools and systems involved

2. **Automation Assessment**
   - For each task, evaluate:
     - **Frequency**: How often is it done?
     - **Volume**: How many times per day/week?
     - **Consistency**: Same steps every time?
     - **Rule-based**: Can it be defined by logic?
     - **ROI**: Time saved vs. automation effort

3. **Prioritize Automation**
   - High priority: Frequent, high-volume, error-prone
   - Medium priority: Moderate frequency, clear rules
   - Low priority: Rare, complex, requires judgment
   - Calculate ROI: (Time saved per month) / (Build time)

4. **Create Automation Roadmap**
   - List automations by priority
   - Estimate build effort (hours)
   - Identify dependencies and prerequisites
   - Assign owners and timeline

**Output:** Prioritized automation backlog with ROI estimates.

### Workflow 2: Design Automated Workflow

**Steps:**
1. **Define Trigger**
   - What event starts the workflow?
   - Examples: Git push, PR created, schedule, webhook, file upload
   - Specify trigger conditions and filters

2. **Map Workflow Steps**
   - List each action in sequence
   - Identify decision points (if/then logic)
   - Define parallel vs. sequential steps
   - Specify timeout and retry behavior

3. **Define Data Flow**
   - What data inputs are needed?
   - How is data transformed between steps?
   - Where is data stored or logged?
   - What outputs are produced?

4. **Error Handling**
   - What can go wrong at each step?
   - How should errors be handled? (retry, alert, skip, fail)
   - Who gets notified on failure?
   - What rollback procedures are needed?

5. **Create Workflow Diagram**
   - Visual representation of flow
   - Show triggers, steps, decisions, outputs
   - Document expected duration
   - Note dependencies and integrations

**Output:** Workflow specification document with diagram.

### Workflow 3: Implement Automation

**Steps:**
1. **Choose Automation Tool**
   - GitHub Actions: CI/CD, git-triggered workflows
   - Webhooks: Event-driven integrations
   - Cron Jobs: Scheduled tasks
   - MCP Servers: AI-powered automations
   - Zapier/Make: No-code integrations
   - Custom Scripts: Specialized needs

2. **Write Automation Code**
   - Follow workflow specification
   - Implement error handling and logging
   - Add configuration for flexibility
   - Include documentation and comments
   - Write tests for automation logic

3. **Test Automation**
   - Test happy path (everything works)
   - Test error cases (failures, timeouts)
   - Test edge cases (empty data, duplicates)
   - Verify notifications and logging
   - Validate end-to-end flow

4. **Deploy to Staging**
   - Run in test environment first
   - Monitor for issues
   - Gather feedback from users
   - Adjust based on real-world behavior

5. **Production Rollout**
   - Deploy to production
   - Monitor closely for first 48 hours
   - Set up alerts for failures
   - Document runbooks for troubleshooting
   - Train team on automation

**Output:** Production-ready automation with monitoring and documentation.

### Workflow 4: Monitor and Optimize

**Steps:**
1. **Track Metrics**
   - Execution count and success rate
   - Average duration and performance
   - Error rate and types
   - Time saved vs. manual process
   - Cost (compute, API calls, etc.)

2. **Regular Reviews**
   - Weekly: Check for failures and alerts
   - Monthly: Review performance and efficiency
   - Quarterly: Assess ROI and value
   - Yearly: Evaluate if still needed

3. **Continuous Improvement**
   - Identify optimization opportunities
   - Reduce execution time
   - Improve error handling
   - Expand automation coverage
   - Refactor for maintainability

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Analyze process | "find automation opportunities in [process]" |
| Design workflow | "design automation for [task]" |
| Create GitHub Action | "automate [task] with GitHub Actions" |
| Set up webhook | "create webhook for [event]" |
| Schedule task | "schedule [task] to run [frequency]" |
| Monitor automation | "check automation health" |
| Optimize workflow | "optimize [automation]" |
| Document workflow | "document [automation] workflow" |

## Best Practices

- **Start small**: Automate simple, high-ROI tasks first; build momentum with quick wins
- **Make it reliable**: 95%+ success rate minimum; unreliable automation is worse than manual work
- **Design for failure**: Assume everything can fail; handle errors gracefully and alert humans
- **Log everything**: Comprehensive logging enables debugging and auditing
- **Keep it simple**: Complex automations are hard to maintain; favor simple, modular workflows
- **Version control**: Store automation code in git; track changes and enable rollback
- **Test thoroughly**: Test happy path, error cases, and edge cases before production
- **Monitor actively**: Set up alerts and dashboards; know when automation breaks
- **Document clearly**: Future you (or teammates) need to understand what it does and how to fix it
- **Maintain regularly**: Review and update automations quarterly; remove obsolete ones
- **Human oversight**: Keep humans in loop for critical decisions; automation assists, doesn't replace judgment
- **Measure impact**: Track time saved and ROI; justify automation investment with data

## Common Automation Patterns

### 1. CI/CD Pipeline
**Trigger**: Git push or PR
**Steps**:
- Run linter and formatter
- Run unit and integration tests
- Build application
- Run E2E tests
- Deploy to staging
- Run smoke tests
- Deploy to production (on merge)
- Notify team on completion or failure

### 2. Issue Triage
**Trigger**: New GitHub issue created
**Steps**:
- Analyze issue content
- Label by type (bug, feature, question)
- Assign to appropriate team
- Add to project board
- Notify team in Slack
- Auto-reply with acknowledgment

### 3. Dependency Updates
**Trigger**: Weekly schedule
**Steps**:
- Check for package updates
- Create PR with updates
- Run full test suite
- Request review from team
- Auto-merge if tests pass and minor version

### 4. Performance Monitoring
**Trigger**: Every hour
**Steps**:
- Check API response times
- Measure database query performance
- Analyze error rates
- Check resource usage (CPU, memory)
- Alert if thresholds exceeded
- Log metrics to dashboard

### 5. Customer Onboarding
**Trigger**: New user signup
**Steps**:
- Send welcome email
- Create user account and resources
- Schedule onboarding emails (drip campaign)
- Add to CRM
- Notify sales team if enterprise plan
- Track onboarding completion

### 6. Backup and Archival
**Trigger**: Daily at 2 AM
**Steps**:
- Backup database
- Backup uploaded files
- Compress and encrypt backups
- Upload to S3 or backup service
- Verify backup integrity
- Delete backups older than 30 days
- Alert if backup fails

### 7. Code Review Reminder
**Trigger**: PR open for 24 hours without review
**Steps**:
- Identify pending PRs
- Check assigned reviewers
- Send reminder to reviewers
- Escalate if urgent
- Track review SLA metrics

### 8. Release Notes Generation
**Trigger**: Tag pushed (version release)
**Steps**:
- Gather commits since last release
- Categorize changes (features, fixes, breaking)
- Generate release notes from PR descriptions
- Create GitHub release
- Post to changelog page
- Notify team and customers

## Automation ROI Calculator

```
Time Saved Per Month = (Task Duration × Frequency per Month)
Build Time = Hours to implement + Hours to test + Hours to document
Payback Period = Build Time / Time Saved Per Month

Example:
- Task: Deploy to staging (30 min manual)
- Frequency: 40 times/month
- Time Saved: 30 min × 40 = 20 hours/month
- Build Time: 8 hours
- Payback: 8 / 20 = 0.4 months (12 days)
- ROI after 1 year: (20 × 12) - 8 = 232 hours saved
```

**Rule of Thumb**: If payback period < 3 months, automate it.

## Automation Technology Guide

| Use Case | Tool | Complexity | Best For |
|----------|------|------------|----------|
| Git-triggered workflows | GitHub Actions | Medium | CI/CD, testing, deployment |
| Event integrations | Webhooks | Medium | Real-time notifications |
| Scheduled tasks | Cron Jobs | Low | Backups, reports, cleanup |
| No-code automation | Zapier/Make | Low | Simple integrations |
| API automation | Node/Python scripts | Medium | Custom logic, complex flows |
| AI-powered workflows | MCP Servers | High | Smart routing, content analysis |
| Database automation | Triggers/Procedures | Medium | Data validation, calculations |
| Browser automation | Playwright MCP | Medium | Web scraping, testing, monitoring |

## Error Handling Patterns

### Retry Logic
```yaml
- Transient errors: Retry 3 times with exponential backoff
- Rate limits: Wait and retry after delay
- Permanent errors: Fail fast and alert
```

### Fallback Strategies
```yaml
- Primary action fails: Try secondary action
- API unavailable: Use cached data
- Service down: Queue for later processing
```

### Alerting Hierarchy
```yaml
- Info: Log only
- Warning: Log and notify on-call during business hours
- Error: Immediate alert to on-call
- Critical: Page on-call and escalate to team lead
```

## Integration Points

- **GitHub Actions**: Primary CI/CD automation platform
- **Webhooks**: Event-driven integrations with external services
- **MCP Servers**: AI-powered workflow automation
- **Playwright MCP**: Browser automation for testing and scraping
- **Supabase**: Database triggers and Edge Functions
- **Slack/Discord**: Notifications and bot commands
- **Monitoring Tools**: Sentry, DataDog, New Relic for observability

---
name: technical-launch-planner
description: Plan and execute technical product launches for developer tools, APIs, and technical products. Use this skill when technical PMMs need to "plan a launch", "create a launch strategy", "coordinate a product release", or "prepare for GA/beta launch".
---

# Technical Launch Planner

## Overview

Plan and execute successful launches for technical products, developer tools, APIs, SDKs, and platforms. This skill provides frameworks, checklists, and templates specifically designed for technical audiences and developer-focused products.

**Built for:**
- Developer tools and platforms
- APIs and SDKs
- Technical infrastructure products
- B2D (Business-to-Developer) products
- SaaS with technical buyers

---

## Quick Start

### 1. Assess Your Launch Tier

Run the interactive assessment:

```bash
scripts/assess_launch_tier.sh
```

This determines if your launch is:
- **Tier 1** (Major/GA) - New product, major version, significant expansion
- **Tier 2** (Standard) - New features, integrations, regional expansion
- **Tier 3** (Minor) - Updates, improvements, small features

### 2. Generate Launch Plan

Create your comprehensive launch plan:

```bash
scripts/generate_launch_plan.sh
```

Provides structured plan with:
- Timeline and milestones
- Stakeholder responsibilities
- Developer enablement checklist
- Go-to-market activities
- Launch day playbook

### 3. Validate Readiness

Before launch, check readiness:

```bash
scripts/validate_readiness.sh
```

Validates:
- Documentation completeness
- Technical assets ready
- Stakeholder alignment
- Messaging finalized
- Metrics instrumentation

---

## Core Launch Framework

### Launch Tiers

Different launches require different levels of investment:

| Tier | Type | Examples | Investment |
|------|------|----------|------------|
| **Tier 1** | Major | GA launch, new product, major version | Full GTM, events, PR |
| **Tier 2** | Standard | New features, integrations, SDKs | Selective GTM, blog, docs |
| **Tier 3** | Minor | Updates, improvements, patches | Changelog, in-app |

See `references/launch_tiers.md` for complete framework.

---

## Developer-Focused Launch Components

### 1. Developer Enablement

**Critical for technical launches:**

**Documentation:**
- Getting started guide
- API reference
- Code samples
- Integration guides
- Migration guides (if applicable)

**Code Assets:**
- SDKs/client libraries
- Sample applications
- Starter templates
- Code snippets

**Developer Experience:**
- Sandbox/playground environment
- Interactive tutorials
- API explorer
- Debugging tools

See `references/developer_enablement.md` for complete checklist.

---

### 2. Technical Messaging

**Speak developer language:**

**Avoid:**
- Marketing jargon
- Vague benefits
- Non-technical superlatives

**Include:**
- Concrete technical details
- Performance metrics
- Code examples
- Architecture diagrams
- Integration patterns

See `references/launch_messaging.md` for templates.

---

### 3. Launch Channels for Developers

**Where developers discover new tools:**

**Primary:**
- Developer documentation
- GitHub/GitLab
- Developer blog
- API changelog
- Release notes

**Secondary:**
- Dev.to, Hacker News, Reddit
- Technical Twitter/X
- Discord/Slack communities
- YouTube (tutorials)
- Developer newsletters

**Tertiary:**
- Webinars/workshops
- Conferences
- Podcasts
- Case studies

---

## Launch Planning Workflow

### Phase 1: Planning (T-12 to T-8 weeks)

**Objectives:**
- Define launch tier
- Set success criteria
- Align stakeholders
- Create timeline

**Activities:**
1. **Launch Tier Assessment**
   ```bash
   scripts/assess_launch_tier.sh
   ```

2. **Stakeholder Kickoff**
   - Product/Engineering
   - Developer Relations
   - Sales Engineering
   - Marketing/Comms
   - Partners (if applicable)

3. **Define Success Metrics**
   - Developer adoption metrics
   - API usage/calls
   - SDK downloads
   - Documentation traffic
   - Community engagement

4. **Create Launch Timeline**
   ```bash
   scripts/generate_launch_plan.sh
   ```

---

### Phase 2: Build (T-8 to T-4 weeks)

**Objectives:**
- Create all launch assets
- Prepare documentation
- Build demos and samples

**Activities:**

**Documentation:**
- [ ] Getting started guide written
- [ ] API reference complete
- [ ] Integration guides ready
- [ ] Migration guide (if needed)
- [ ] Troubleshooting FAQ

**Code Assets:**
- [ ] SDKs built and tested
- [ ] Sample apps created
- [ ] Code snippets prepared
- [ ] Sandbox environment ready

**Marketing Assets:**
- [ ] Technical blog post written
- [ ] Demo video recorded
- [ ] Announcement email drafted
- [ ] Social media plan
- [ ] Press release (Tier 1)

**Sales Enablement:**
- [ ] Technical battlecard
- [ ] Demo script
- [ ] FAQ/objection handling
- [ ] Pricing materials
- [ ] Competitive positioning

---

### Phase 3: Prepare (T-4 to T-1 weeks)

**Objectives:**
- Review and refine all assets
- Train teams
- Pre-launch validation

**Activities:**

**Internal Enablement:**
- [ ] Sales team training
- [ ] Support team training
- [ ] Partner briefings
- [ ] Internal demo day

**External Prep:**
- [ ] Beta customers briefed
- [ ] Partners coordinated
- [ ] Developer advocates prepared
- [ ] Community moderators ready

**Technical Validation:**
```bash
scripts/validate_readiness.sh
```

**Pre-Launch Checklist:**
- [ ] All docs published to staging
- [ ] SDKs tagged and ready
- [ ] Demo environment tested
- [ ] Monitoring/analytics configured
- [ ] Support escalation path defined

---

### Phase 4: Launch (Launch Day)

**Launch Day Playbook:**

**Morning (9 AM):**
- [ ] Publish documentation
- [ ] Release SDKs/packages
- [ ] Deploy blog post
- [ ] Send announcement email
- [ ] Post to social media
- [ ] Update website/product pages

**Midday (12 PM):**
- [ ] Monitor metrics dashboard
- [ ] Respond to community questions
- [ ] Share to external communities
- [ ] Engage with social mentions

**Afternoon (3 PM):**
- [ ] Post to Hacker News/Reddit (if Tier 1)
- [ ] Developer advocate content
- [ ] Partner announcements

**End of Day:**
- [ ] Day 1 metrics report
- [ ] Team debrief
- [ ] Issue triage

---

### Phase 5: Post-Launch (T+1 week to T+4 weeks)

**Objectives:**
- Monitor adoption
- Gather feedback
- Iterate on messaging
- Report results

**Activities:**

**Week 1:**
- [ ] Daily metrics monitoring
- [ ] Community Q&A
- [ ] Bug fixes prioritized
- [ ] Feedback synthesis

**Week 2:**
- [ ] First adoption metrics
- [ ] Customer feedback interviews
- [ ] Documentation updates
- [ ] Follow-up content

**Week 4:**
- [ ] Launch retrospective
- [ ] Success metrics report
- [ ] Lessons learned doc
- [ ] Update launch playbook

---

## Launch Tier Details

### Tier 1: Major Launch

**When:**
- New product GA
- Major version release (v2.0, v3.0)
- Significant platform expansion
- Game-changing feature

**Timeline:** 12-16 weeks

**Investment:**
- Full cross-functional GTM
- PR/media outreach
- Developer events
- Partner coordination
- Paid promotion

**Deliverables:**
- Complete documentation
- Multiple SDKs
- Sample applications
- Video tutorials
- Interactive demos
- Press release
- Analyst briefings
- Launch event/webinar
- Partner co-marketing

---

### Tier 2: Standard Launch

**When:**
- New features
- New integrations
- Additional SDKs
- Regional expansion

**Timeline:** 6-8 weeks

**Investment:**
- Selective GTM activities
- Blog and social
- Email to developer list
- Documentation updates

**Deliverables:**
- Feature documentation
- Code samples
- Blog post
- Demo video
- Email announcement
- Social media
- Changelog entry

---

### Tier 3: Minor Launch

**When:**
- Incremental improvements
- Bug fixes
- Performance enhancements
- Small feature additions

**Timeline:** 2-4 weeks

**Investment:**
- Minimal marketing
- Documentation only
- Changelog

**Deliverables:**
- Release notes
- Updated docs
- Changelog entry
- In-app notification (if applicable)

---

## Developer Launch Best Practices

### 1. Documentation First

**Launch is NOT ready without:**
- ✅ Getting started guide
- ✅ API reference
- ✅ At least 3 code samples
- ✅ Integration guide

**Developer rule:** "If it's not documented, it doesn't exist"

---

### 2. Show, Don't Tell

**Developers want to see code:**

**Good:**
```python
# Initialize the SDK
import acme_sdk

client = acme_sdk.Client(api_key="your_key")
result = client.widgets.create(name="My Widget")
print(result.id)
```

**Bad:**
"Our SDK makes it easy to create widgets with just a few lines of code"

---

### 3. Interactive > Passive

**Engagement hierarchy:**
1. 🥇 Interactive tutorial/playground
2. 🥈 Live demo
3. 🥉 Demo video
4. ❌ Static screenshots

---

### 4. Honest Technical Communication

**Developers appreciate:**
- Limitations clearly stated
- Performance characteristics
- Pricing transparency
- Migration complexity
- Breaking changes

**Developers hate:**
- Overpromising
- Hidden limitations
- Surprise breaking changes
- Vendor lock-in

---

### 5. Community-First Approach

**Engage where developers are:**
- Answer questions on Stack Overflow
- Be active in GitHub discussions
- Respond on Hacker News
- Join relevant Discord/Slack
- Participate in Reddit AMAs

**Don't:**
- Spam communities
- Ignore negative feedback
- Delete critical comments
- Only show up for launches

---

## Technical Metrics

### Developer Adoption Metrics

**Activation:**
- Sandbox/trial sign-ups
- First API call within 24 hours
- SDK downloads
- "Hello World" completions

**Engagement:**
- Daily/Weekly Active Developers
- API calls per developer
- Features adopted
- Integration depth

**Retention:**
- Day 7, 30, 90 developer retention
- Churn rate
- NPS (Developer)

See `references/metrics_frameworks.md` for complete guide.

---

## Launch Templates

### Technical Blog Post Template

```markdown
# Introducing [Feature/Product]

## The Problem

[Describe the developer pain point in technical detail]

## The Solution

[High-level technical overview]

## How It Works

[Technical architecture, with diagram]

## Getting Started

[Code sample showing basic usage]

## What's Next

[Roadmap tease]

[Link to full documentation]
```

---

### Launch Email Template

**Subject:** [Feature] is now available

**Body:**
```
Hi [Developer Name],

We're excited to announce [Feature] is now generally available.

What it does:
[One sentence technical description]

Why it matters:
[Developer benefit]

Get started in 5 minutes:
[Code snippet or quick start link]

Key resources:
- Documentation: [link]
- Sample code: [link]
- API reference: [link]

Questions? Reply to this email or join us in [Discord/Slack].

Happy building!
[Your Name]
```

---

### Changelog Entry Template

```markdown
## [Version] - YYYY-MM-DD

### Added
- [New feature]: [Technical description]
  - Example: `client.newMethod(params)`
  - [Link to docs]

### Changed
- [Breaking change]: [What changed and why]
  - Migration guide: [link]

### Fixed
- [Bug fix]: [What was fixed]

### Deprecated
- [Feature]: [Timeline for removal]
```

---

## Partner/Integration Launches

### When You Have Partners

**Coordination needed:**
- Joint messaging
- Co-marketing plan
- Technical validation
- Mutual customer references

**Partner Enablement:**
- [ ] Technical integration tested
- [ ] Partner documentation
- [ ] Joint case study
- [ ] Co-branded assets
- [ ] Sales team training

**Launch Activities:**
- Co-authored blog posts
- Joint webinar
- Cross-promotion on social
- Email to both lists
- Mutual press release (Tier 1)

---

## Launch Retrospective

### Post-Launch Review (Within 30 days)

**Metrics Review:**
- Did we hit adoption targets?
- What was Day 1, Week 1, Month 1 usage?
- Developer sentiment (NPS, social, support)?
- Press/analyst coverage (if applicable)?

**What Worked:**
- Which channels drove most adoption?
- What content resonated?
- Which enablement assets were most used?

**What Didn't:**
- Where did developers get stuck?
- What documentation was missing?
- Which assumptions were wrong?

**Action Items:**
- Documentation improvements
- Messaging refinements
- Process improvements for next launch

**Template:** [Document in Notion/Confluence]

---

## Common Pitfalls

### Pitfall 1: Launching Without Complete Docs

**Problem:** "Docs will be ready soon" = Dead launch

**Solution:** Docs are non-negotiable. Delay launch if needed.

---

### Pitfall 2: Marketing-Speak for Developers

**Problem:** "Revolutionary", "Seamless", "Game-changing"

**Solution:** Use concrete technical language, metrics, code.

---

### Pitfall 3: Ignoring Migration Complexity

**Problem:** Breaking changes with no migration guide

**Solution:** Clear migration guide, migration tools, version support plan.

---

### Pitfall 4: Over-Indexing on Launch Day

**Problem:** All effort on Day 1, nothing for ongoing adoption

**Solution:** Plan 4-week post-launch content calendar.

---

### Pitfall 5: No Developer Feedback Loop

**Problem:** Launch and disappear

**Solution:** Active community engagement, regular office hours.

---

## Resources

### Scripts

- **assess_launch_tier.sh** - Determine appropriate launch tier
- **generate_launch_plan.sh** - Create comprehensive launch plan
- **validate_readiness.sh** - Pre-launch readiness check

### References

- **launch_tiers.md** - Complete launch tier framework
- **developer_enablement.md** - Developer enablement checklist
- **launch_messaging.md** - Technical messaging templates
- **metrics_frameworks.md** - Developer product metrics guide

---

## Real-World Examples

### Example 1: API GA Launch (Tier 1)

**Product:** New REST API for developer platform

**Timeline:** 12 weeks

**Key Activities:**
- Complete API documentation
- 5 SDKs (Python, Node, Ruby, Go, Java)
- Interactive API explorer
- 10+ sample applications
- Video tutorial series
- Developer webinar
- Blog post + case studies
- HN/Reddit launch
- Email to 50K developers

**Results:**
- 10K API keys issued Week 1
- 60% activation rate (first API call)
- 40% Day 7 retention
- #1 on Hacker News

---

### Example 2: New Integration (Tier 2)

**Product:** Integration with popular DevOps tool

**Timeline:** 6 weeks

**Key Activities:**
- Integration guide
- Sample workflow
- Blog post
- Partner co-marketing
- Demo video
- Email announcement

**Results:**
- 2K integration activations Month 1
- 25% of existing users tried it
- High engagement metric

---

### Example 3: SDK Update (Tier 3)

**Product:** New SDK version with performance improvements

**Timeline:** 2 weeks

**Key Activities:**
- Release notes
- Migration guide
- Changelog
- Tweet/X post

**Results:**
- 30% upgrade rate Week 1
- Minimal support burden
- Positive community feedback

---

## Summary

Technical launches require:

1. **Complete Documentation** - Non-negotiable
2. **Code Samples** - Show, don't tell
3. **Developer Enablement** - Make it easy to try
4. **Technical Credibility** - Speak the language
5. **Community Engagement** - Be where developers are
6. **Clear Metrics** - Measure what matters
7. **Post-Launch Commitment** - Launch is day 1, not the finish line

Use the scripts to streamline planning, follow the frameworks for consistency, and always put developers first.

**Get started:**
```bash
scripts/assess_launch_tier.sh
```

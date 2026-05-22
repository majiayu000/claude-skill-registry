---
name: launch-gtm-execution
version: "2.0.0"
description: Master go-to-market strategy, launch planning and execution, sales enablement, and marketing campaigns. Execute successful product launches.
sasmp_version: "1.3.0"
bonded_agent: 05-launch-gtm
bond_type: PRIMARY_BOND
parameters:
  - name: launch_date
    type: string
    format: date
    required: true
  - name: gtm_model
    type: string
    enum: [direct_sales, self_service, sales_dev, channel]
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Launch & Go-To-Market Skill

Master the art of successful product launches. From GTM strategy through launch execution, learn to coordinate teams, build momentum, and achieve market success.

## Go-To-Market (GTM) Strategy

### GTM Framework Decision

**1. Direct Sales Model**
- Your team directly sells to customers
- Best for: High ACV (>$10K), complex product
- Sales cycle: 3-6 months
- Team size: 1 AE per $500K-$1M ARR target
- Examples: Salesforce, HubSpot, Workday

**Pros:**
- Control over message
- Deep customer relationships
- Higher deal size possible
- Custom solutions

**Cons:**
- Expensive ($200K+ per rep)
- Slower to scale
- Long sales cycles
- Small addressable market needed for ROI

**Key Metrics:**
- Sales Qualified Lead (SQL)
- Close rate (typically 20-40%)
- Sales cycle length
- Customer Acquisition Cost (CAC)

---

**2. Self-Service / Freemium Model**
- Customers discover and sign up themselves
- Best for: Low ACV (<$1K), self-explanatory product
- Sales cycle: Minutes to days
- Team: Product + Marketing focused

**Pros:**
- Scales without sales team
- Low CAC
- Fast adoption
- Land and expand opportunity

**Cons:**
- High churn risk
- Need viral/network effects
- Requires excellent product
- Difficult to reach enterprise

**Key Metrics:**
- Free-to-paid conversion (2-5% target)
- Monthly Recurring Revenue (MRR)
- Customer Lifetime Value (LTV)
- CAC < 30% LTV

---

**3. Sales Development (SMB)**
- SDR/AE team for smaller deals
- Best for: SMB market ($2K-$50K ACV)
- Sales cycle: 1-3 months
- Lower cost than enterprise sales

**Pros:**
- Better ROI than enterprise sales
- Faster sales cycles
- Larger addressable market
- Still personal touch

**Cons:**
- Volume required
- Lower margins
- Churn challenges

---

**4. Channel/Partner Model**
- Resellers, integrations, platforms
- Best for: Reaching wide market cheaply
- Examples: App stores, Zapier, AWS Marketplace

**Pros:**
- Low CAC (partner pays)
- Wide distribution
- Established customer relationships

**Cons:**
- Less control
- Lower margins (revenue sharing)
- Partner incentive alignment

### GTM Positioning

**Template:**

```
For [target customer]
Who [customer problem]
The [product name]
Is [category]
That [primary benefit]
Unlike [alternative/competitor]
We [unique differentiator]
```

**Messaging Hierarchy:**
1. **Hero message** (one sentence)
   - "Collaborate in real-time, anywhere"
2. **Sub-message 1** (supporting feature)
   - "Works offline, syncs when online"
3. **Sub-message 2** (why it matters)
   - "No more lost work"
4. **Social proof**
   - "Used by 100K teams"

### Target Customer Profile (ICP)

Define your ideal customer:

**Company Characteristics:**
- Company size: 50-500 employees
- Industry: SaaS companies
- Revenue: $10M-$100M ARR
- Geography: US + EU
- Growth stage: Growth stage

**Individual Buyer:**
- Title: VP of Operations
- Reports to: COO/CFO
- Budget owner: Yes
- Decision timeline: 90 days

**Why they'll buy:**
- Main pain: 40% time on manual process
- Impact: Save $500K/year
- Decision criteria: ROI, ease of use, support

## Launch Planning (12-Week Timeline)

### Weeks 1-4: Strategy & Preparation

**Week 1-2: Launch Kickoff**
- [ ] Define launch goals (# signups, NPS, revenue)
- [ ] Identify target segments
- [ ] Competitive positioning finalized
- [ ] Go/no-go criteria defined
- [ ] Launch date locked

**Week 3-4: Content & Collateral**
- [ ] Launch press release drafted
- [ ] Product one-pagers created
- [ ] Demo video script written
- [ ] FAQ documentation started
- [ ] Sales pitch refined

### Weeks 5-8: Content Creation & Team Prep

**Week 5-6: Marketing Preparation**
- [ ] Website landing page built
- [ ] Email campaign drafted
- [ ] Social media content scheduled
- [ ] Influencer outreach list built
- [ ] PR/media contact list built

**Week 7-8: Team Training**
- [ ] Sales team training (2 days)
- [ ] Customer success onboarding materials
- [ ] Support team training
- [ ] Executive briefing
- [ ] Talking points finalized

### Weeks 9-10: Beta & Feedback

**Week 9-10: Beta Program**
- [ ] 50-100 beta users selected
- [ ] Beta feedback system set up
- [ ] Daily feedback review
- [ ] Bug fixes prioritized
- [ ] Product stability achieved

### Weeks 11-12: Final Launch Prep

**Week 11: Final Preparations**
- [ ] All content finalized and approved
- [ ] Marketing assets tested
- [ ] Sales collateral printed/digital ready
- [ ] Support documentation complete
- [ ] Systems and infrastructure scaling verified

**Week 12: Launch Week Readiness**
- [ ] Final product testing complete
- [ ] Team communication plan reviewed
- [ ] Monitoring and alerts configured
- [ ] Support team on high alert
- [ ] Celebration planned!

## Launch Week Execution

### Launch Day Schedule

**6:00 AM - Team Standup**
- Goals for the day
- Potential issues
- Communication channels

**9:00 AM - LAUNCH**
- Press release goes out
- Email campaign sends
- Social media posts
- Website live
- Sales team activated

**9:00 AM - 5:00 PM: Monitoring**
- Metrics dashboard live
- Support team responding
- Sales team following up
- Marketing team posting
- Exec team celebrating

**5:00 PM - 9:00 PM: Close Monitoring**
- Continued metric tracking
- Issue response
- Team updates hourly
- Press/media engagement

### Post-Launch Week (Days 2-7)

**Day 2 (Friday):**
- Performance review
- Bug prioritization
- Customer feedback analysis
- Day 2 communication push

**Day 3-5 (Weekend/Monday):**
- 24/7 support coverage
- Customer success outreach
- High-priority fixes
- Feedback pattern analysis

**Day 6-7 (Tuesday/Wednesday):**
- Retrospective planning
- Performance vs goals review
- Course correction planning
- Team debrief

## Sales Enablement

### Sales One-Pager (2 pages)

**Page 1:**
- Product/company logo
- One-line pitch
- 3 key features/benefits
- Comparison vs competitors
- Pricing

**Page 2:**
- Customer testimonial/quote
- Use case scenario
- ROI calculator
- Call to action
- Contact info

### Pitch Structure (3 minutes)

1. **Hook** (15 sec)
   - Current state: "Teams spend 40% time on manual sync"

2. **Problem** (30 sec)
   - Real impact: "Causes delays, errors, frustration"

3. **Solution** (60 sec)
   - How you solve: "We automate the sync process"
   - Key benefit: "Save 5 hours/week per team member"

4. **Social Proof** (15 sec)
   - Used by: "100 teams across industries"
   - Outcomes: "Avg 40% time savings"

5. **Call to Action** (15 sec)
   - Next step: "Let's run a quick 30-min POC with your team"

### Objection Handling

**Objection: "We're fine with current solution"**
- Response: "I understand. What if we could cut your manual sync time in half? Worth 20 minutes to see how?"

**Objection: "We don't have budget"**
- Response: "What if this saves $50K in productivity? Would you make budget? Let's see if it applies to you."

**Objection: "We need to evaluate competitors"**
- Response: "Smart. Here's how we compare to X and Y. What's most important to you - speed, ease of use, or cost?"

### Sales Process

1. **Prospecting** - Outbound/inbound leads
2. **Discovery Call** - Understand needs
3. **Proposal/Demo** - Show solution
4. **Negotiation** - Pricing/terms
5. **Close** - Customer acquisition!

## Launch Metrics

**Acquisition Metrics:**
- Sign-ups: [Target #]
- Conversion rate: [Target %]
- Cost per acquisition: [Budget]

**Engagement Metrics:**
- DAU (Daily Active Users)
- Feature adoption rate
- Time in app

**Retention Metrics:**
- Day 7/30 retention
- Churn rate
- NPS score

**Business Metrics:**
- MRR (Monthly Recurring Revenue)
- ACV (Average Contract Value)
- Payback period

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Launch delay | Product not ready | Parallel tracks, beta extend |
| Low buzz | Insufficient marketing | 4-week teaser campaign |
| Sales not ready | Late enablement | Training week 6 |
| Support overwhelmed | Under-staffed | Temp staff, extended hours |

### Debug Checklist

```
[ ] GTM model clearly defined mi?
[ ] Target segments validated mi?
[ ] Messaging tested mi?
[ ] Sales team trained mi?
[ ] Support docs ready mi?
[ ] Rollback plan var mı?
[ ] Monitoring configured mı?
```

### Recovery Procedures

1. **Launch Date Slip** → Communicate early, propose new date
2. **Critical Bug** → Activate rollback procedure
3. **Low Adoption** → Accelerate marketing, CS outreach

---

**Master launch execution and create market momentum!**

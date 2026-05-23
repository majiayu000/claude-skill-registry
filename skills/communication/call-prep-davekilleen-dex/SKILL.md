---
name: call-prep
description: Prepare for upcoming call with full context
role_groups: [sales, customer_success]
jtbd: |
  You have a call coming up and need to quickly get context on the person or account. 
  This pulls their person page, account history, recent interactions, and open items 
  so you walk into the call prepared and never ask "remind me where we left off?"
time_investment: "3-5 minutes per call"
---

## Purpose

Quickly gather all relevant context before a call - recent conversations, open action items, account status, and suggested talking points.

## Usage

- `/call-prep [person-name]` - Prep for call with specific person
- `/call-prep [company-name]` - Prep for call with company (general)

---

## Step 1: Identify the Person/Account

1. Search People/ directory for person page
2. If company name provided, search for:
   - Company pages in 05-Areas/Companies/
   - Related person pages in 05-Areas/People/
   - Deal files in 04-Projects/

---

## Step 2: Gather Context

### Person Context (if person specified)
- Read person page completely
- Extract:
  - Role and responsibilities
  - Key interests/priorities
  - Relationship notes
  - Communication preferences

### Recent Interactions
- Search 00-Inbox/Meetings/ for meetings with this person/company (last 60 days)
- Extract most recent 2-3 conversations:
  - Date
  - Key topics
  - Decisions made
  - Their concerns/questions

### Open Action Items
- Search for tasks involving this person/company
- Check 03-Tasks/Tasks.md for related items
- Flag overdue items (past promised date)

### Account Status
- Current deal stage (if active deal)
- Account health (if existing customer)
- Recent wins or issues
- Stakeholder map (if available)

---

## Step 3: Check for Signals

Search for:
- Competitive mentions
- Budget discussions
- Timeline pressures
- Pain points expressed
- Feature requests
- Positive feedback

---

## Step 4: Generate Call Prep Brief

```markdown
# 📞 Call Prep: [Person Name] ([Company])

**Call date:** [Today or scheduled date]
**Their role:** [Title]
**Relationship:** [Strong/Moderate/New]
**Call type:** [Discovery/Demo/Follow-up/Check-in/Negotiation]

---

## 🎯 Call Objective

**Primary goal:** [What you want to accomplish]
**Secondary goals:**
- [Goal 2]
- [Goal 3]

---

## 👤 Person Profile

**[Name] - [Title]**

**What they care about:**
- [Interest 1]
- [Interest 2]
- [Interest 3]

**Communication style:** [Direct/Analytical/Relationship-focused/etc]

**Context:**
- [Key relationship notes from person page]
- [Their current priorities]

---

## 📝 Recent Interactions

### Last Meeting: [Date]
**Topic:** [What was discussed]
**Key points:**
- [Point 1]
- [Point 2]

**Their concerns:**
- [Concern raised]

**Our commitments:**
- [What we promised to do]

### Previous Meeting: [Date]
**Topic:** [What was discussed]
[Brief summary]

---

## ✅ Open Items

**Our commitments to them:**
- [ ] [Action item 1] - [Status: Done/In progress/Overdue]
- [ ] [Action item 2] - [Status]

**Their commitments to us:**
- [ ] [Action item 1] - [Status]

**⚠️ Overdue items:** [Flag any overdue commitments]

---

## 📊 Account Status

**Current state:** [New prospect/Active deal/Existing customer]
**Deal stage:** [If applicable]
**Account health:** [If existing customer - Green/Yellow/Red]

**Recent developments:**
- [Development 1]
- [Development 2]

---

## 💡 Key Discussion Points

**Topics to cover:**
1. [Topic 1] - [Why important]
2. [Topic 2] - [Why important]
3. [Topic 3] - [Why important]

**Questions to ask:**
- [Question 1 - discovery/clarification]
- [Question 2]
- [Question 3]

**Things to mention:**
- [Relevant product update/capability]
- [Reference to their pain point]
- [Competitive differentiator if relevant]

---

## 🚨 Watch For

**Signals to listen for:**
- [Signal 1 - e.g., budget constraints]
- [Signal 2 - e.g., timeline pressure]
- [Signal 3 - e.g., competitor mention]

**Potential objections:**
- [Objection 1] - Response: [How to address]
- [Objection 2] - Response: [How to address]

---

## 🎯 Desired Outcome

**Best case:**
- [Ideal outcome]

**Acceptable:**
- [Minimum acceptable outcome]

**Next steps to propose:**
- [Next step 1]
- [Next step 2]

---

## 📎 Quick Links

**Relevant files:**
- [Link to person page]
- [Link to account plan if exists]
- [Link to recent meeting notes]
- [Link to active deal if exists]

---

## ⏰ Post-Call Actions

After the call, remember to:
- [ ] Update person page with new context
- [ ] Log action items in 03-Tasks/Tasks.md
- [ ] Update deal status if applicable
- [ ] Send follow-up within 24 hours
```

---

## Step 5: Offer Preparation Help

After presenting prep brief, ask:

> "Need me to:
> 1. Draft talking points or demo script?
> 2. Pull competitive positioning if they mentioned competitors?
> 3. Check if we have mutual connections?
> 4. Remind you 30 min before the call?"

---

## Company-Level Prep

When company name provided (not specific person):

1. Pull account plan if exists
2. List all stakeholders at company
3. Suggest who should be on the call
4. Provide company-level context vs individual

---

## Integration with Other Skills

- **Before calling:** Run this command
- **After calling:** Suggest updating person page
- **For strategic accounts:** Reference `/account-plan` for deeper context
- **For at-risk deals:** Reference `/deal-review` insights

---

## Example Output

```markdown
# 📞 Call Prep: Sarah Chen (Acme Corp)

**Call date:** Tomorrow (Jan 29, 10am)
**Their role:** VP Product
**Relationship:** Strong (key champion)
**Call type:** Demo (Real-time Dashboards feature)

---

## 🎯 Call Objective

**Primary goal:** Demo real-time dashboards to address reporting pain point, get buy-in for Analytics upgrade
**Secondary goals:**
- Gauge interest in Engineering expansion
- Get Jennifer (CTO) intro confirmed
- Schedule follow-up with CFO Tom

---

## 👤 Person Profile

**Sarah Chen - VP Product**

**What they care about:**
- Data-driven product decisions
- Customer insights
- Team efficiency
- Strategic alignment

**Communication style:** Direct, data-focused, loves seeing demos, asks great questions

**Context:**
- Our strongest champion at Acme
- Participated in case study willingly
- Has referred 2 prospects this quarter
- Reports to CEO, peer to CTO Jennifer

---

## 📝 Recent Interactions

### Last Meeting: Yesterday (Jan 27)
**Topic:** Contract review call for renewal prep
**Key points:**
- Renewal discussions going well
- She's pushing for engineering team expansion internally
- Confirmed intro to Jennifer (CTO) for Feb 2

**Their concerns:**
- Reporting still taking too long for her team
- Wants to see real-time dashboard solution

**Our commitments:**
- Show real-time dashboard demo (this call!)
- Coffee with Jennifer scheduled (Feb 2)

### Previous Meeting: Jan 24 (Quarterly Review)
**Topic:** Q4 review, roadmap preview
- Positive feedback on product
- Expressed frustration: "Takes 2 days/month to compile reports manually"
- Asked about real-time capabilities

---

## ✅ Open Items

**Our commitments to them:**
- [x] Schedule dashboard demo - DONE (this call)
- [ ] Intro to Jennifer confirmed - Feb 2
- [ ] Q1 roadmap summary - Send by Feb 1

**Their commitments to us:**
- [x] Intro to Jennifer - DONE
- [ ] Internal champion for engineering expansion - In progress

**⚠️ No overdue items**

---

## 📊 Account Status

**Current state:** Strategic customer (18-month relationship)
**Deal stage:** Planning expansion (Engineering team)
**Account health:** Green (high engagement, vocal advocate)

**Recent developments:**
- Exploring 2x ARR expansion (Engineering adoption)
- Analytics upgrade opportunity ($36K/year)
- Contract renewal in 6 months (July)

---

## 💡 Key Discussion Points

**Topics to cover:**
1. **Real-time dashboard demo** - Directly addresses "2 days/month" pain
2. **ROI for Analytics upgrade** - Time savings quantified
3. **Jennifer meeting prep** - Ensure she knows what we're discussing with CTO
4. **CFO engagement** - Float idea of Tom joining next call for ROI discussion

**Questions to ask:**
- "Does this dashboard view solve the reporting pain your team mentioned?"
- "What questions will Jennifer have about engineering use cases?"
- "Would it help to have Tom (CFO) see the ROI case for Analytics upgrade?"

**Things to mention:**
- 3 other customers have requested this exact dashboard capability
- We've prioritized real-time features based on her feedback
- Engineering package can integrate with their GitHub/Jira (if she asks)

---

## 🚨 Watch For

**Signals to listen for:**
- Pricing concerns for Analytics upgrade
- Timeline pressure for engineering expansion
- Budget availability (CFO Tom's mindset)
- Any new pain points or frustrations

**Potential objections:**
- "Cost of upgrade" - Response: Show time savings ROI, pays for itself in 3 months
- "Implementation time" - Response: 2-week rollout, minimal disruption

---

## 🎯 Desired Outcome

**Best case:**
- She loves the dashboard demo
- Commits to Analytics upgrade verbally
- Confirms she'll advocate for engineering expansion internally

**Acceptable:**
- Positive feedback on demo
- Agrees to present to Tom (CFO) for budget approval
- Timeline for decision clear

**Next steps to propose:**
- CFO presentation (Feb 12) to approve Analytics upgrade
- Engineering technical demo with Jennifer (Feb 9)
- Proposal for both upgrades by Feb 16

---

## 📎 Quick Links

**Relevant files:**
- 05-Areas/People/External/Sarah_Chen_Acme.md
- 05-Areas/Companies/Acme_Corp_Account_Plan.md
- 00-Inbox/Meetings/2026-01-27_Acme_Contract_Review.md
- 04-Projects/Acme_Engineering_Expansion_Opportunity.md

---

## ⏰ Post-Call Actions

After the call, remember to:
- [ ] Update Sarah's person page with demo feedback
- [ ] Log next steps in 03-Tasks/Tasks.md (CFO presentation, Jennifer demo)
- [ ] Update Acme account plan with progress
- [ ] Send proposal for Analytics upgrade within 48 hours
```

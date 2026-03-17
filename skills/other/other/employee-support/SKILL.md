---
name: employee-support
description: Handle common employee questions and requests through structured FAQ systems, escalation paths, and self-service resources
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Employee Support

> Create efficient employee support systems with structured FAQs, clear escalation paths, and self-service resources for common HR questions.

## When to Use This Skill

- Building HR knowledge bases
- Creating FAQ documentation
- Designing escalation matrices
- Training HR support staff
- Improving response consistency

## Methodology Foundation

Based on **HR service delivery models** and **knowledge management principles**, combining:
- Tiered support structure
- Self-service enablement
- Consistent messaging
- Escalation protocols

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Drafts FAQ content | Policy specifics |
| Structures knowledge base | Escalation contacts |
| Creates response templates | Approval thresholds |
| Identifies common questions | Exception handling |
| Suggests improvements | Sensitive matters |

## Instructions

### Step 1: Categorize Support Topics

**Common HR Categories:**

| Category | Examples | Volume |
|----------|----------|--------|
| Benefits | Insurance, 401k, PTO | High |
| Payroll | Pay dates, deductions, expenses | High |
| Time Off | Request, balance, policy | High |
| Employment | Verification, transfers | Medium |
| Policies | Handbook questions | Medium |
| Concerns | Complaints, accommodations | Low |

### Step 2: Design Support Tiers

**Tier Structure:**

| Tier | Handled By | Resolution | Examples |
|------|------------|------------|----------|
| 0 | Self-service | Immediate | FAQ, policy lookup |
| 1 | HR Coordinator | Same day | PTO balance, form requests |
| 2 | HR Generalist | 1-2 days | Policy interpretation |
| 3 | HR Manager | 2-5 days | Exceptions, escalations |
| 4 | HR Director/Legal | Varies | Sensitive matters |

### Step 3: Build Knowledge Base

**FAQ Structure:**
- Clear question as title
- Concise answer (3-5 sentences)
- Links to relevant policies
- Related questions
- Last updated date

### Step 4: Create Response Templates

**Template Components:**
1. Acknowledgment of question
2. Clear, direct answer
3. Additional context if needed
4. Next steps
5. Escalation path if applicable

### Step 5: Define Escalation Criteria

**Escalation Triggers:**

| Trigger | Escalate To | Timeline |
|---------|-------------|----------|
| Policy exception request | HR Manager | 24 hours |
| Legal/compliance concern | HR Director | Immediate |
| Harassment/discrimination | HR Director | Immediate |
| Manager conflict | HRBP | Same day |
| Medical/disability | Benefits specialist | Same day |

## Examples

### Example 1: Benefits FAQ Section

**Input:**
```
Create FAQ section for employee benefits questions.
```

**Output:**
```
## Benefits FAQ

### Health Insurance

---

**Q: When does my health insurance coverage start?**

Your health insurance coverage begins on the first day of the month
following your start date. For example, if you start on January 15th,
your coverage begins February 1st.

**Related:** [Benefits enrollment guide](#) | [Provider directory](#)
**Last Updated:** January 2026

---

**Q: How do I add a dependent to my insurance?**

You can add a dependent during:
1. **Open enrollment** (November each year)
2. **Qualifying life event** (within 30 days of event)

Qualifying life events include: marriage, birth/adoption of child,
loss of other coverage, or divorce.

**To add a dependent:**
1. Log into [Benefits Portal]
2. Select "Life Event" or "Add Dependent"
3. Upload required documentation
4. Submit within 30 days of event

**Documents needed:**
- Marriage certificate (spouse)
- Birth certificate (child)
- Adoption papers (adopted child)

**Related:** [Qualifying life events list](#) | [Document requirements](#)
**Last Updated:** January 2026

---

**Q: What is the difference between our PPO and HDHP plans?**

| Feature | PPO | HDHP + HSA |
|---------|-----|------------|
| Monthly premium | Higher | Lower |
| Deductible | Lower ($500) | Higher ($1,500) |
| HSA eligible | No | Yes |
| Out-of-pocket max | $3,000 | $4,000 |
| Best for | Frequent medical needs | Generally healthy, want to save |

**Company contribution:** We contribute $1,200/year to HDHP HSA accounts.

**Related:** [Full plan comparison](#) | [HSA guide](#)
**Last Updated:** January 2026

---

**Q: How do I find in-network providers?**

Use the provider finder for your plan:
- **PPO Plan:** [Aetna Provider Search](link)
- **HDHP Plan:** [UHC Provider Search](link)

Tips:
- Search by specialty and ZIP code
- Verify "in-network" status before appointments
- For specialists, check if referral is needed (PPO only)

**Related:** [Network FAQs](#) | [Referral process](#)
**Last Updated:** January 2026

---

### PTO (Paid Time Off)

---

**Q: How much PTO do I have?**

Check your current balance in [HR System] > Time Off > Balances.

**PTO accrual rates:**
| Tenure | Annual PTO | Accrual/Pay Period |
|--------|------------|-------------------|
| 0-2 years | 15 days | 4.62 hours |
| 3-5 years | 20 days | 6.15 hours |
| 6+ years | 25 days | 7.69 hours |

**Related:** [PTO policy](#) | [Request time off](#)
**Last Updated:** January 2026

---

**Q: How do I request time off?**

1. Log into [HR System]
2. Select "Request Time Off"
3. Choose dates and PTO type
4. Add notes if needed
5. Submit for manager approval

**Approval timeline:**
- Standard requests: 48 hours
- 1+ week requests: Submit 2 weeks in advance
- Holiday periods: Submit 30 days in advance

**Related:** [Blackout dates](#) | [Manager approval guide](#)
**Last Updated:** January 2026

---

**Q: Can I carry over unused PTO?**

Yes, with limits:
- **Maximum carryover:** 5 days (40 hours)
- **Use by:** March 31st of following year
- **Excess PTO:** Use it or lose it by December 31st

**Tip:** Check your balance in October to plan year-end usage.

**Related:** [PTO policy](#) | [Year-end reminder](#)
**Last Updated:** January 2026

---

### Payroll

---

**Q: When do I get paid?**

We pay **bi-weekly on Fridays**. Pay periods run Sunday-Saturday.

**2026 Pay Dates:**
Jan 10, Jan 24, Feb 7, Feb 21...
[See full calendar](#)

**Direct deposit:** Funds typically available by 6 AM Friday.
**Paper checks:** Available at front desk by 9 AM.

**Related:** [Pay calendar](#) | [Update direct deposit](#)
**Last Updated:** January 2026

---

**Q: How do I change my direct deposit?**

1. Log into [HR System]
2. Select "Pay" > "Direct Deposit"
3. Add new account information
4. Verify with a test deposit (small amount)
5. Remove old account after verification

**Processing time:** Changes take 1-2 pay periods to take effect.
**Security:** Never share banking info via email.

**Related:** [Banking FAQs](#) | [Split deposits](#)
**Last Updated:** January 2026

---

**Q: How do I submit an expense report?**

1. Collect receipts (required for expenses >$25)
2. Log into [Expense System]
3. Create new report
4. Add line items with receipts
5. Select appropriate cost center
6. Submit for manager approval

**Reimbursement timeline:** 5-7 business days after approval.
**Policy limits:** See [expense policy](#) for meal and travel limits.

**Related:** [Expense policy](#) | [Receipt requirements](#)
**Last Updated:** January 2026
```

### Example 2: Support Response Templates

**Input:**
```
Create response templates for common employee requests.
```

**Output:**
```
## HR Support Response Templates

### Template 1: PTO Balance Inquiry

**Trigger:** Employee asks about PTO balance

---

Hi [Name],

Thanks for reaching out!

Your current PTO balance is **[X] hours** ([Y] days).

Here's the breakdown:
- Available PTO: [X] hours
- Pending requests: [Y] hours
- Scheduled to accrue this period: [Z] hours

You can always check your balance in [HR System] > Time Off > Balances.

Need to request time off? Here's how: [Link]

Let me know if you have other questions!

Best,
[HR Team]

---

### Template 2: Employment Verification Request

**Trigger:** Employee needs employment verification

---

Hi [Name],

Happy to help with your employment verification!

**For mortgage/housing verification:**
Most lenders accept our automated verification through The Work Number.
- Employer code: [XXXX]
- Website: [link]

**For other purposes requiring HR letter:**
Please submit a request in [HR System] > Documents > Request Verification,
including:
- Purpose of verification
- What information to include
- Where to send it (email/fax/mail)

**Processing time:** 2-3 business days

Let me know if you need anything else!

Best,
[HR Team]

---

### Template 3: Benefits Question Escalation

**Trigger:** Complex benefits question requiring specialist

---

Hi [Name],

Thanks for your question about [topic].

This is a great question that our Benefits team can best answer.
I've forwarded your inquiry to [Benefits Specialist Name], who will
reach out within 24 hours.

In the meantime, you might find these resources helpful:
- [Relevant FAQ link]
- [Benefits overview document]

If you don't hear back by [date], please let me know and I'll follow up.

Best,
[HR Team]

---

### Template 4: Policy Exception Request

**Trigger:** Employee requests exception to policy

---

Hi [Name],

Thank you for explaining your situation regarding [topic].

Policy exception requests require manager and HR approval. Here's the process:

1. **Document your request:** Submit through [HR System] > Requests > Policy Exception
2. **Include:** Your specific situation, dates, and what you're requesting
3. **Manager review:** Your manager will be notified automatically
4. **HR review:** Once manager approves, HR reviews within 3 business days

I want to set expectations: exceptions are granted based on business
need and consistency with how we've handled similar situations.
I can't guarantee approval, but we'll review carefully.

Have questions about the process? I'm happy to help.

Best,
[HR Team]

---

### Template 5: Sensitive Matter Acknowledgment

**Trigger:** Employee raises concern requiring confidential handling

---

Hi [Name],

Thank you for trusting us with this matter. I want you to know
we take this seriously.

**What happens next:**
- Your concern has been documented confidentially
- [HR Manager/HRBP Name] will reach out within 24 hours
- This will be handled with appropriate discretion

**Your rights:**
- You are protected from retaliation for raising concerns
- You can request updates on the status of your concern
- You may involve additional support if needed

**Resources available:**
- Employee Assistance Program (EAP): [phone]
- Anonymous ethics hotline: [phone]

Please don't hesitate to reach out if you have immediate concerns.

Best,
[HR Team]

---

### Template 6: New Employee FAQ Response

**Trigger:** New hire with multiple questions

---

Hi [Name],

Welcome to [Company]! Great questions—here's what you need to know:

**Benefits enrollment:**
You have 30 days from your start date ([date]) to enroll.
Complete enrollment here: [Link]
Deadline: [Date]

**Direct deposit:**
Set up in [HR System] > Pay > Direct Deposit
Takes 1-2 pay periods to activate

**Building access:**
Your badge will be ready at the front desk on Day 1
IT will email your login credentials the day before you start

**First week:**
Your manager has a welcome schedule planned
Check your calendar for orientation sessions

**Questions?**
- Your buddy: [Name]
- Your HRBP: [Name]
- HR Help: [email/slack]

We're excited to have you on the team!

Best,
[HR Team]
```

## Skill Boundaries

### What This Skill Does Well
- Structuring FAQ content
- Creating consistent templates
- Designing escalation paths
- Improving self-service

### What This Skill Cannot Do
- Know company-specific policies
- Access employee records
- Handle sensitive matters
- Make policy exceptions

### When to Escalate
- Legal concerns
- Harassment/discrimination
- Medical/disability accommodations
- Management conflicts
- Termination questions

## Iteration Guide

**Follow-up Prompts:**
- "Create FAQs for [specific topic]"
- "Design escalation workflow for [issue type]"
- "Write template for [scenario]"
- "How should we handle [edge case]?"

## References

- SHRM HR Service Delivery Models
- HR Shared Services Best Practices
- Knowledge Management for HR
- ServiceNow HR Service Delivery

## Related Skills

- `onboarding-guide` - New hire support
- `engagement-analyzer` - Employee sentiment
- `hr-chatbot-design` - Automated support

## Skill Metadata

- **Domain**: HR Operations
- **Complexity**: Beginner-Intermediate
- **Mode**: cyborg
- **Time to Value**: 1-2 hours per topic area
- **Prerequisites**: HR policies, system access info

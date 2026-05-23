---
name: Vendor Onboarding
description: Comprehensive guide to enterprise vendor onboarding processes, timelines, requirements, and strategies for accelerating customer acquisition
---

# Vendor Onboarding

## What is Vendor Onboarding?

**Definition:** Process enterprise customers follow before using your product.

### Stages
```
1. Discovery and Evaluation (demos, POC)
2. Security Review (questionnaires, audits)
3. Legal Review (contracts, terms)
4. Procurement (PO, invoicing)
5. Technical Onboarding (SSO, SCIM, integration)
6. User Training and Rollout
```

### Timeline
```
Small Business:    1-4 weeks
Mid-Market:        4-12 weeks
Enterprise:        3-12 months
```

---

## Why It Matters

### 1. Understanding Customer Timelines (Sales Cycle)

**Realistic Expectations:**
```
SMB:
- Demo → Close: 2-4 weeks
- Onboarding: 1 week
- Total: 3-5 weeks

Mid-Market:
- Demo → Close: 2-3 months
- Onboarding: 1-2 months
- Total: 3-5 months

Enterprise:
- Demo → Close: 6-12 months
- Onboarding: 1-3 months
- Total: 7-15 months
```

**Impact on Revenue:**
```
If you think enterprise sales take 3 months, but they actually take 12 months:
→ Revenue projections are off by 9 months
→ Cash flow problems
→ Missed targets
```

### 2. Anticipate Requirements

**Prepare in Advance:**
```
Before first enterprise customer:
- Get SOC2 certification
- Implement SSO (SAML)
- Prepare standard contracts (MSA, DPA)
- Build security documentation
- Set up support processes
```

**Cost of Not Preparing:**
```
Customer asks: "Do you have SOC2?"
You: "No, but we can get it"
→ 6-12 month delay
→ Customer may choose competitor
```

### 3. Prepare Documentation and Support

**Required Documentation:**
- Security questionnaire responses
- SOC2 report
- Privacy policy
- Data Processing Agreement (DPA)
- Onboarding guide
- Admin training materials

### 4. Avoid Surprises That Delay Deals

**Common Surprises:**
```
Week 10: "We need SOC2" (don't have it, 6 month delay)
Week 15: "We need SCIM" (not implemented, 3 month delay)
Week 20: "We can't accept your liability terms" (contract negotiation, 2 month delay)
```

**Better:**
```
Week 1: Qualify customer (do they need SOC2, SCIM, custom contracts?)
Week 2: Provide SOC2, demonstrate SCIM, share contract template
→ No surprises, faster close
```

---

## Vendor Onboarding Stages

### Stage 1: Discovery and Evaluation (Weeks 1-4)

**Activities:**
- Product demos
- Technical deep dives
- Proof of Concept (POC)
- Stakeholder presentations

**Participants:**
- End users (test product)
- IT team (technical evaluation)
- Security team (initial security review)
- Procurement (pricing discussion)

**Deliverables:**
- POC success criteria met
- Technical requirements documented
- Pricing proposal
- Initial security overview

**Timeline:**
- SMB: 1-2 weeks
- Mid-Market: 2-4 weeks
- Enterprise: 4-8 weeks

### Stage 2: Security Review (Weeks 5-8)

**Activities:**
- Security questionnaire (100-500 questions)
- SOC2 report review
- Penetration test results review
- Security calls/meetings
- Risk assessment

**Participants:**
- Customer security team
- Your security team
- Compliance team

**Deliverables:**
- Completed security questionnaire
- SOC2 Type II report (under NDA)
- Penetration test results
- Data Processing Agreement (DPA)
- Security approval

**Timeline:**
- SMB: N/A (skip)
- Mid-Market: 2-4 weeks
- Enterprise: 4-8 weeks

**See:** Security Questionnaires skill for details

### Stage 3: Legal Review (Weeks 9-12)

**Activities:**
- Contract review
- Terms negotiation
- Liability discussions
- Indemnification clauses
- Data privacy agreements

**Participants:**
- Customer legal team
- Your legal team
- Sales team

**Deliverables:**
- Master Service Agreement (MSA)
- Data Processing Agreement (DPA)
- Service Level Agreement (SLA)
- Business Associate Agreement (BAA, if HIPAA)
- Signed contracts

**Timeline:**
- SMB: N/A (standard ToS)
- Mid-Market: 2-4 weeks
- Enterprise: 4-12 weeks

**Common Negotiation Points:**
- Liability cap ($1M, $5M, unlimited?)
- Indemnification (who indemnifies whom?)
- Data ownership (customer owns their data)
- Termination (30 days notice, immediate?)
- Governing law (which state/country?)

### Stage 4: Procurement (Weeks 13-16)

**Activities:**
- Vendor database registration
- Purchase Order (PO) creation
- Invoicing
- Payment processing

**Participants:**
- Customer procurement team
- Your finance team
- Sales team

**Deliverables:**
- Vendor registration complete
- Purchase Order (PO) received
- Invoice sent
- Payment received

**Timeline:**
- SMB: 1 day (credit card)
- Mid-Market: 1-2 weeks
- Enterprise: 2-8 weeks

**Common Requirements:**
- W-9 form (US vendors)
- Certificate of Insurance
- Banking details (for wire transfer)
- Vendor portal registration
- Specific invoice format

### Stage 5: Technical Onboarding (Weeks 17-20)

**Activities:**
- SSO configuration (SAML or OIDC)
- SCIM provisioning setup
- IP whitelisting (if required)
- Subdomain or vanity URL
- Integration with other systems
- Data migration (if applicable)

**Participants:**
- Customer IT team
- Your technical team
- Implementation engineer

**Deliverables:**
- SSO working
- SCIM provisioning working
- Integrations configured
- Test users created
- Technical validation complete

**Timeline:**
- SMB: 1 day (email/password)
- Mid-Market: 1-2 weeks (SSO)
- Enterprise: 2-4 weeks (SSO + SCIM + integrations)

**See:** SSO and SCIM skills for details

### Stage 6: User Training and Rollout (Weeks 21-24)

**Activities:**
- Admin training
- End user training
- Documentation review
- Pilot rollout (10-50 users)
- Full rollout (all users)

**Participants:**
- Customer admins
- End users
- Your customer success team
- Training team

**Deliverables:**
- Admins trained
- Users trained
- Pilot successful
- Full rollout complete
- Go-live!

**Timeline:**
- SMB: 1 day (self-service)
- Mid-Market: 1-2 weeks
- Enterprise: 2-4 weeks

---

## Vendor Onboarding Timeline

### Small Business (1-4 Weeks)

```
Week 1: Demo + Sign up (credit card)
Week 2: Self-service onboarding
Week 3: Users start using product
Week 4: Check-in call

Total: 4 weeks
```

**Characteristics:**
- Self-service
- Credit card payment
- Standard ToS
- No security review
- No contracts
- Email/password login

### Mid-Market (4-12 Weeks)

```
Week 1-2: Demo + POC
Week 3-4: Security review (basic)
Week 5-6: Contract review (light)
Week 7-8: Procurement (PO)
Week 9-10: SSO setup
Week 11-12: Training + Rollout

Total: 12 weeks
```

**Characteristics:**
- Annual contract
- Basic security review (questionnaire)
- Light contract negotiation
- SSO (SAML or OIDC)
- Purchase Order (PO)
- Some training

### Enterprise (3-12 Months)

```
Month 1-2: Demo + POC
Month 3-4: Security review (extensive)
Month 5-6: Legal review (extensive)
Month 7-8: Procurement
Month 9-10: Technical onboarding (SSO + SCIM)
Month 11-12: Training + Rollout

Total: 12 months
```

**Characteristics:**
- Multi-year contract
- Extensive security review (SOC2, pen test, etc.)
- Heavy contract negotiation (MSA, DPA, SLA)
- SSO + SCIM
- Purchase Order (PO)
- Extensive training
- Dedicated Customer Success Manager (CSM)

---

## Requirements by Customer Size

### SMB (Small Business)

**Payment:**
- Credit card
- Monthly or annual

**Contracts:**
- Standard Terms of Service (ToS)
- No negotiation

**Security:**
- No security review
- Basic privacy policy

**Technical:**
- Email/password login
- Self-service onboarding

**Support:**
- Email support
- Help docs

### Mid-Market

**Payment:**
- Purchase Order (PO)
- Annual contract

**Contracts:**
- Standard MSA (light negotiation)
- Standard DPA

**Security:**
- Basic security questionnaire (50-100 questions)
- Privacy policy
- Basic security overview

**Technical:**
- SSO (SAML or OIDC)
- Self-service or guided onboarding

**Support:**
- Email + chat support
- Onboarding call
- Help docs + videos

### Enterprise

**Payment:**
- Purchase Order (PO)
- Multi-year contract

**Contracts:**
- Custom MSA (heavy negotiation)
- Custom DPA
- SLA (uptime guarantees)
- BAA (if HIPAA)

**Security:**
- Extensive security questionnaire (200-500 questions)
- SOC2 Type II report
- Penetration test results
- Security calls/meetings

**Technical:**
- SSO (SAML)
- SCIM provisioning
- Custom integrations
- IP whitelisting
- Dedicated instance (sometimes)

**Support:**
- Dedicated Customer Success Manager (CSM)
- Priority support (SLA)
- Onboarding project plan
- Training (admin + end user)
- Quarterly business reviews (QBRs)

---

## Preparing for Onboarding

### 1. Standard Contracts (MSA Template)

**Master Service Agreement (MSA):**
```
Key Sections:
1. Services (what you provide)
2. Fees (pricing, payment terms)
3. Term and Termination (duration, how to cancel)
4. Warranties (what you guarantee)
5. Liability (caps, limitations)
6. Indemnification (who protects whom)
7. Data Privacy (how you handle data)
8. Security (your security obligations)
9. Confidentiality (NDA)
10. Governing Law (which state/country)
```

**Why Template:**
- Faster negotiations (start from template, not scratch)
- Consistent terms (all customers get similar terms)
- Legal review (template pre-approved by your lawyers)

**Where to Get:**
- Hire lawyer to draft ($5k-20k)
- Use template from Ironclad, Juro, or similar
- Copy from competitor (risky, not recommended)

### 2. Security Documentation (Trust Center)

**Public Trust Center:**
```
URL: https://trust.yourcompany.com

Contents:
- Security overview
- Compliance certifications (SOC2, ISO)
- Privacy policy
- Data Processing Agreement (DPA)
- Subprocessor list
- Security whitepaper
- Contact info (security@yourcompany.com)
```

**Benefits:**
- Customers can self-serve
- Reduces security questions
- Builds trust
- SEO (ranks for "yourcompany security")

**Tools:**
- SafeBase ($5k-20k/year)
- Whistic ($10k-50k/year)
- Custom website (free, but manual)

### 3. Compliance Certifications (SOC2, ISO 27001)

**SOC2 Type II:**
- **What:** Audit of security controls
- **Cost:** $15k-50k (first year), $10k-30k (renewal)
- **Timeline:** 6-12 months
- **Frequency:** Annual
- **Required by:** Most enterprise customers

**ISO 27001:**
- **What:** International security standard
- **Cost:** $20k-100k
- **Timeline:** 6-12 months
- **Frequency:** 3-year cert, annual surveillance
- **Required by:** Some enterprise customers (especially international)

**When to Get:**
- SOC2: Before first enterprise customer (or ASAP)
- ISO 27001: Optional (nice-to-have)

### 4. Onboarding Documentation (Step-by-Step Guides)

**Admin Guide:**
```
1. Configure SSO
   - Step 1: Get IdP metadata
   - Step 2: Enter in our app
   - Step 3: Test with test user
   - Step 4: Enable for all users

2. Set up SCIM
   - Step 1: Generate SCIM token
   - Step 2: Configure in IdP
   - Step 3: Test user provisioning
   - Step 4: Enable auto-provisioning

3. Invite users
   - Step 1: Upload CSV or use SCIM
   - Step 2: Assign roles
   - Step 3: Send invitations

4. Configure settings
   - Step 1: Set company name
   - Step 2: Upload logo
   - Step 3: Configure permissions
```

**End User Guide:**
```
1. Log in
   - Step 1: Go to yourapp.com
   - Step 2: Click "Login with SSO"
   - Step 3: Enter company email
   - Step 4: Redirected to your IdP

2. Create first project
   - Step 1: Click "New Project"
   - Step 2: Enter project name
   - Step 3: Invite team members

3. Upload data
   - Step 1: Click "Upload"
   - Step 2: Select file
   - Step 3: Map columns
   - Step 4: Confirm import
```

### 5. Customer Success Team (For Onboarding Support)

**Roles:**
- **Implementation Engineer:** Technical setup (SSO, SCIM, integrations)
- **Customer Success Manager (CSM):** Overall onboarding, training, adoption
- **Support Engineer:** Troubleshooting, bug fixes

**When to Hire:**
- Implementation Engineer: After 5-10 enterprise customers
- CSM: After 10-20 enterprise customers
- Support Engineer: After 50-100 customers (any size)

---

## Common Blockers

### 1. Missing SOC2 Report

**Problem:**
```
Customer: "Do you have SOC2?"
You: "No"
Customer: "We can't proceed without it"
→ Deal blocked
```

**Solution:** Get SOC2 Type II

**Timeline:** 6-12 months

**Cost:** $15k-50k

**Workaround (if don't have yet):**
```
"We're currently undergoing our SOC2 Type II audit, expected completion in [DATE]. In the meantime, we can provide:
- Our security policies and procedures
- Penetration test results
- Security questionnaire responses
- References from similar customers

Would you like to proceed with these, or wait for SOC2 completion?"
```

### 2. No SSO Support

**Problem:**
```
Customer: "We require SSO"
You: "We don't support SSO"
Customer: "This is a blocker"
→ Deal dies
```

**Solution:** Implement SSO (SAML and OIDC)

**Timeline:** 2-4 weeks (with library like passport-saml)

**Cost:** Engineering time

**Workaround:** None (SSO is must-have for enterprise)

### 3. Unacceptable Contract Terms

**Problem:**
```
Customer: "We need unlimited liability"
You: "Our liability is capped at $10k"
Customer: "Unacceptable"
→ Negotiation stalls
```

**Solution:** Negotiate

**Common Compromises:**
- Liability cap = Annual contract value (ACV)
- Or: $1M cap
- Or: $5M cap (for very large customers)

**What NOT to Accept:**
- Unlimited liability (could bankrupt company)
- Indemnification for customer's negligence

### 4. Security Concerns (Unresolved Questionnaire Items)

**Problem:**
```
Customer: "You don't encrypt data at rest"
You: "Correct"
Customer: "This is a security risk"
→ Deal blocked
```

**Solution:** Fix security issue

**Timeline:** 1-4 weeks (depending on issue)

**Examples:**
- Implement encryption at rest (1-2 weeks)
- Implement MFA (1 week)
- Implement audit logging (1-2 weeks)

### 5. Missing Features (Integration Requirements)

**Problem:**
```
Customer: "We need Salesforce integration"
You: "We don't have that"
Customer: "This is required for our workflow"
→ Deal blocked or delayed
```

**Solution:**
- Build integration (4-12 weeks)
- Or: Use Zapier/Make.com (workaround)
- Or: Offer custom integration (services engagement)

**Prioritization:**
- If 3+ customers ask for same integration → Build it
- If 1 customer asks → Workaround or custom

---

## Accelerating Onboarding

### 1. Self-Service Onboarding (For Smaller Customers)

**What:** Customer can onboard without talking to you

**Requirements:**
- Clear signup flow
- Guided product tour
- Help docs
- Video tutorials
- In-app tooltips

**Benefits:**
- Faster onboarding (minutes vs weeks)
- Lower cost (no human involvement)
- Scales infinitely

**When to Use:** SMB, some mid-market

### 2. Pre-Approved Security Documentation

**What:** Security docs ready to share

**Contents:**
- Standard security questionnaire responses
- SOC2 report (under NDA)
- Penetration test results
- Security whitepaper

**Benefits:**
- Faster security review (days vs weeks)
- Consistent answers
- Professional appearance

**Where to Store:** Trust center, Google Drive, Notion

### 3. Standard Contract (No Negotiation)

**What:** Take-it-or-leave-it contract

**When to Use:**
- SMB (always)
- Mid-market (sometimes)
- Enterprise (rarely)

**Benefits:**
- Faster close (no legal review)
- Predictable terms
- Lower legal costs

**Risks:**
- Some customers won't accept
- May lose deals

**Recommendation:**
- SMB: Standard contract only
- Mid-market: Standard contract, light negotiation
- Enterprise: Custom contract (expect negotiation)

### 4. White-Glove Onboarding (Dedicated CSM for Enterprise)

**What:** Dedicated person to guide customer through onboarding

**Activities:**
- Kickoff call (set expectations)
- Weekly check-ins
- Technical setup assistance
- Training coordination
- Go-live support

**Benefits:**
- Faster onboarding (proactive vs reactive)
- Higher customer satisfaction
- Better adoption
- Fewer support tickets

**Cost:** CSM salary ($80k-150k/year, can handle 10-30 customers)

**When to Use:** Enterprise customers (>$50k ACV)

---

## Onboarding Checklist

```markdown
# Enterprise Onboarding Checklist

## Pre-Sales
- [ ] Demo completed
- [ ] POC successful
- [ ] Technical requirements documented
- [ ] Pricing proposal sent

## Security Review
- [ ] Security questionnaire received
- [ ] Security questionnaire completed
- [ ] SOC2 report shared (under NDA)
- [ ] Penetration test results shared
- [ ] Security calls completed
- [ ] Security approval received

## Legal Review
- [ ] MSA sent
- [ ] DPA sent
- [ ] SLA sent (if applicable)
- [ ] BAA sent (if HIPAA)
- [ ] Contracts negotiated
- [ ] Contracts signed

## Procurement
- [ ] Vendor registration completed
- [ ] W-9 submitted (US)
- [ ] Certificate of Insurance submitted
- [ ] Purchase Order (PO) received
- [ ] Invoice sent
- [ ] Payment received

## Technical Onboarding
- [ ] SSO configured
- [ ] SCIM configured (if applicable)
- [ ] IP whitelisting configured (if applicable)
- [ ] Subdomain/vanity URL configured
- [ ] Integrations configured
- [ ] Test users created
- [ ] Technical validation complete

## Training and Rollout
- [ ] Admin training scheduled
- [ ] Admin training completed
- [ ] End user training scheduled
- [ ] End user training completed
- [ ] Pilot users identified
- [ ] Pilot rollout complete
- [ ] Full rollout complete
- [ ] Go-live!

## Post-Onboarding
- [ ] Week 1 check-in
- [ ] Week 2 check-in
- [ ] Month 1 check-in
- [ ] Quarterly Business Review (QBR) scheduled
```

---

## Tools for Onboarding

### CRM (Salesforce, HubSpot) for Tracking

**Use:** Track onboarding progress

**Features:**
- Deal stages (Demo → Security → Legal → Procurement → Onboarding → Live)
- Tasks (complete questionnaire, sign contract, configure SSO)
- Timeline (when did each stage complete?)
- Reporting (average time to onboard, bottlenecks)

**Example Deal Stages:**
```
1. Demo
2. POC
3. Security Review
4. Legal Review
5. Procurement
6. Technical Onboarding
7. Training
8. Live
```

### Project Management (Asana, Monday.com)

**Use:** Manage onboarding tasks

**Features:**
- Onboarding template (checklist of tasks)
- Assign tasks to team members
- Due dates
- Dependencies (can't configure SSO until contract signed)
- Customer visibility (share board with customer)

**Example Template:**
```
Onboarding Project: [Customer Name]

Week 1-2: Security Review
- [ ] Complete security questionnaire (Security team)
- [ ] Share SOC2 report (Sales)
- [ ] Security call (Security team + Customer)

Week 3-4: Legal Review
- [ ] Send MSA (Legal)
- [ ] Send DPA (Legal)
- [ ] Negotiate terms (Legal + Sales)
- [ ] Sign contracts (Legal)

Week 5-6: Procurement
- [ ] Submit W-9 (Finance)
- [ ] Receive PO (Sales)
- [ ] Send invoice (Finance)

Week 7-8: Technical Onboarding
- [ ] Configure SSO (Implementation Engineer)
- [ ] Configure SCIM (Implementation Engineer)
- [ ] Test with test users (Implementation Engineer + Customer IT)

Week 9-10: Training
- [ ] Admin training (CSM)
- [ ] End user training (CSM)
- [ ] Pilot rollout (CSM)

Week 11-12: Go-Live
- [ ] Full rollout (CSM)
- [ ] Week 1 check-in (CSM)
```

### Document Signing (DocuSign, PandaDoc)

**Use:** Sign contracts electronically

**Features:**
- Electronic signatures
- Audit trail (who signed, when)
- Templates (MSA, DPA, etc.)
- Reminders (nudge customer to sign)

**Benefits:**
- Faster signing (days vs weeks)
- No printing/scanning
- Legally binding

**Cost:** $10-40/user/month

### Security Portal (SafeBase, Whistic)

**Use:** Share security documentation

**Features:**
- Trust center (public security info)
- Secure document sharing (SOC2 under NDA)
- Questionnaire automation
- Analytics (who viewed what)

**Benefits:**
- Self-service (customers can access docs 24/7)
- Professional appearance
- Faster security review

**Cost:** $5k-50k/year

---

## Customer Success Role

### Dedicated CSM for Enterprise

**Responsibilities:**
- Onboarding project management
- Training coordination
- Adoption monitoring
- Quarterly Business Reviews (QBRs)
- Renewals

**Metrics:**
- Time to onboard (target: <90 days)
- Time to value (target: <30 days)
- Adoption rate (% of users active)
- Customer satisfaction (NPS, CSAT)
- Renewal rate (target: >90%)

**When to Hire:** After 10-20 enterprise customers

**Ratio:** 1 CSM per 10-30 customers (depending on complexity)

### Onboarding Project Plan

**Template:**
```
# Onboarding Project Plan: [Customer Name]

## Overview
- Customer: [Name]
- Contract Value: $[Amount]
- Start Date: [Date]
- Target Go-Live: [Date]
- CSM: [Name]
- Implementation Engineer: [Name]

## Milestones
1. Kickoff Call (Week 1)
2. Security Approval (Week 4)
3. Contracts Signed (Week 8)
4. PO Received (Week 10)
5. SSO Configured (Week 12)
6. Training Complete (Week 14)
7. Go-Live (Week 16)

## Risks
- Security review may take longer (mitigation: start early)
- Legal negotiation may stall (mitigation: use standard contract)
- Customer IT team may be slow (mitigation: weekly check-ins)

## Success Criteria
- All users onboarded
- SSO working
- Training complete
- Customer satisfied (CSAT >8/10)
```

### Regular Check-Ins

**Frequency:**
- Week 1: Daily (critical period)
- Week 2-4: 2x per week
- Week 5-8: Weekly
- Month 3+: Bi-weekly
- Month 6+: Monthly
- Quarterly Business Reviews (QBRs)

**Agenda:**
```
Weekly Check-In (30 min)

1. Progress update (5 min)
   - What's done
   - What's in progress
   - What's blocked

2. Blockers and issues (10 min)
   - Identify blockers
   - Assign owners
   - Set deadlines

3. Next steps (10 min)
   - What's next
   - Who's responsible
   - When is it due

4. Questions and concerns (5 min)
```

### Success Metrics (Time to Value)

**Time to Value (TTV):** Time from signup to first value

**Examples:**
- **Slack:** Time to first message sent
- **Salesforce:** Time to first deal created
- **Dropbox:** Time to first file uploaded

**Your App:** Define what "first value" means

**Target:** <30 days (ideally <7 days)

**How to Reduce TTV:**
- Simplify onboarding
- Guided product tour
- Pre-populate with sample data
- Quick wins (easy tasks first)

---

## Real Vendor Onboarding Stories

### Story 1: Financial Services Enterprise (12 Months)

**Customer:** 10,000-person bank

**Timeline:**
```
Month 1-2: Demo + POC (successful)
Month 3-4: Security review (extensive, 400 questions)
Month 5-6: Legal review (heavy negotiation)
Month 7: Procurement (vendor registration, PO)
Month 8-9: Technical onboarding (SSO + SCIM + custom integration)
Month 10-11: Training (admins, then 500 pilot users)
Month 12: Full rollout (10,000 users)
```

**Challenges:**
- Security review took 2 months (very thorough)
- Legal negotiation took 2 months (liability, indemnification)
- Custom integration required (Salesforce)
- Extensive training needed (500 pilot users)

**Outcome:** Successful, $500k ACV, 3-year contract

### Story 2: Healthcare Mid-Market (3 Months)

**Customer:** 200-person hospital

**Timeline:**
```
Week 1-2: Demo + POC
Week 3-4: Security review (HIPAA focus)
Week 5-6: Legal review (BAA required)
Week 7-8: Procurement (PO)
Week 9-10: Technical onboarding (SSO)
Week 11-12: Training + Rollout
```

**Challenges:**
- HIPAA compliance required (BAA)
- Security questionnaire focused on PHI handling
- SSO required (no email/password)

**Outcome:** Successful, $50k ACV, annual contract

### Story 3: Tech Startup SMB (1 Week)

**Customer:** 20-person startup

**Timeline:**
```
Day 1: Demo
Day 2: Signup (credit card)
Day 3: Self-service onboarding
Day 4-5: Users start using product
Day 7: Check-in call
```

**Challenges:** None (self-service)

**Outcome:** Successful, $5k ACV, monthly contract

---

## Templates

### Onboarding Checklist Template

See "Onboarding Checklist" section above

### Project Plan Template

See "Onboarding Project Plan" section above

---

## Summary

### Quick Reference

**Vendor Onboarding:** Process enterprise customers follow before using your product

**Stages:**
1. Discovery and Evaluation
2. Security Review
3. Legal Review
4. Procurement
5. Technical Onboarding
6. User Training and Rollout

**Timeline:**
- SMB: 1-4 weeks
- Mid-Market: 4-12 weeks
- Enterprise: 3-12 months

**Requirements by Size:**
- **SMB:** Credit card, standard ToS, email/password
- **Mid-Market:** PO, basic security review, SSO
- **Enterprise:** PO, extensive security review, SSO + SCIM, custom contracts

**Preparing:**
- Standard contracts (MSA, DPA)
- Security documentation (trust center)
- Compliance certifications (SOC2, ISO)
- Onboarding documentation
- Customer success team

**Common Blockers:**
- Missing SOC2 (get it!)
- No SSO support (implement it!)
- Unacceptable contract terms (negotiate)
- Security concerns (fix issues)
- Missing features (build or workaround)

**Accelerating:**
- Self-service onboarding (SMB)
- Pre-approved security docs
- Standard contract (no negotiation)
- White-glove onboarding (enterprise)

**Tools:**
- CRM (Salesforce, HubSpot) for tracking
- Project management (Asana, Monday.com)
- Document signing (DocuSign, PandaDoc)
- Security portal (SafeBase, Whistic)

**Customer Success:**
- Dedicated CSM for enterprise
- Onboarding project plan
- Regular check-ins
- Success metrics (time to value)

**Typical Enterprise Timeline:**
```
Month 1-2: Demo + POC
Month 3-4: Security review
Month 5-6: Legal review
Month 7-8: Procurement
Month 9-10: Technical onboarding
Month 11-12: Training + Rollout
```

## Best Practices

### Preparation Best Practices
- **Start Early**: Begin preparing for enterprise onboarding before your first enterprise customer. Getting SOC2, ISO 27001, and other certifications takes 6-12 months.
- **Build Standard Contracts**: Create and maintain standard contract templates (MSA, DPA, SLA, BAA). This reduces negotiation time from weeks to days.
- **Create Trust Center**: Build a public trust center with security documentation, compliance certifications, and subprocessor list. This reduces security review time by 50%.
- **Develop Onboarding Documentation**: Create step-by-step guides for SSO, SCIM, and other technical setup. This reduces technical onboarding time.
- **Hire Customer Success Team**: Build a team dedicated to onboarding and customer success. This improves onboarding experience and reduces time to value.

### Sales Qualification Best Practices
- **Qualify Early**: Identify customer requirements (SOC2, SSO, custom contracts) early in sales process. This prevents surprises later.
- **Understand Customer Size**: Tailor onboarding approach based on customer size (SMB, mid-market, enterprise).
- **Know Decision Makers**: Identify who makes security, legal, and procurement decisions. This helps navigate the process.
- **Set Realistic Expectations**: Communicate realistic timelines for each stage. Enterprise onboarding takes 3-12 months, not 3-12 weeks.
- **Document Requirements**: Capture all customer requirements early and share with relevant teams.

### Security Review Best Practices
- **Standard Response Library**: Maintain comprehensive library of standard responses to common security questions. This reduces completion time from 20-40 hours to 5-10 hours.
- **Pre-Approved Documentation**: Have SOC2 reports, penetration test results, and security policies ready to share under NDA.
- **Security Team Involvement**: Involve security team early in the process. They own security review and should build relationships with customer security teams.
- **Honesty with Mitigation**: Be honest about past incidents but emphasize your response and remediation. Honesty builds trust.
- **Evidence-Ready Responses**: Reference supporting evidence for each claim. For example, "See our SOC2 Type II report for audit findings."

### Legal Review Best Practices
- **Standard Templates**: Start with your standard MSA, DPA, and SLA templates. This provides a baseline for negotiation.
- **Know Your Limits**: Identify deal-breakers and non-negotiable terms before starting negotiations.
- **Liability Caps**: Set reasonable liability caps based on contract value (e.g., 1x ACV, $1M, $5M). Never accept unlimited liability.
- **Quick Turnaround**: Respond to legal comments within 48 hours. This keeps momentum and prevents delays.
- **Legal Team Involvement**: Involve legal team early. They should build relationships with customer legal teams.

### Procurement Best Practices
- **Vendor Registration**: Complete vendor registration proactively in customer portals when possible.
- **Required Documents Ready**: Have W-9 forms, certificates of insurance, and banking details ready.
- **Flexible Payment Terms**: Offer standard payment terms but be flexible for large enterprises (e.g., Net 30, Net 60).
- **Invoice Format**: Provide invoices in customer's preferred format (PDF, specific fields, purchase order references).
- **Finance Team Involvement**: Involve finance team early. They should build relationships with customer procurement teams.

### Technical Onboarding Best Practices
- **SSO First**: Configure SSO before any other technical setup. This is often the first technical requirement.
- **Test Accounts**: Create test accounts in customer's IdP for testing before go-live.
- **Step-by-Step Guides**: Provide detailed, screenshot-based guides for each technical setup step.
- **Video Walkthroughs**: Create video walkthroughs of technical setup processes. This reduces support burden.
- **Implementation Engineer**: Assign a dedicated implementation engineer for enterprise customers. This provides single point of contact.

### Training and Rollout Best Practices
- **Admin Training First**: Train customer admins before end users. Admins will train their own teams.
- **Train-the-Trainer**: Create train-the-trainer materials. This scales training for large organizations.
- **Pilot Rollout**: Start with a small pilot group (10-50 users) before full rollout. This identifies issues early.
- **Quick Wins**: Focus on quick wins in initial training. Show users how to complete their first task quickly.
- **Ongoing Support**: Provide ongoing support during rollout period. This ensures smooth adoption.

### Communication Best Practices
- **Single Point of Contact**: Designate a single point of contact for the customer. This reduces confusion.
- **Regular Updates**: Provide weekly status updates during onboarding. This keeps customer informed and builds trust.
- **Clear Milestones**: Define clear milestones with dates. Celebrate each milestone completion.
- **Proactive Communication**: Anticipate and address issues before customer raises them. This shows proactive approach.
- **Stakeholder Updates**: Keep all stakeholders (customer and internal) aligned on progress.

### Acceleration Best Practices
- **Self-Service for SMB**: Provide self-service onboarding for small customers. This scales infinitely.
- **Pre-Filled Responses**: Share your standard response library with customers. Ask them to copy relevant answers.
- **Standard Contracts**: Use take-it-or-leave-it contracts for SMB and mid-market customers.
- **Automation Tools**: Use tools like DocuSign for contract signing and SafeBase for security documentation.
- **White-Glove for Enterprise**: Provide dedicated CSM for enterprise customers. This improves experience and adoption.

### Post-Onboarding Best Practices
- **Week 1 Check-In**: Schedule daily check-ins during first week. This is critical period for adoption.
- **Time to Value Tracking**: Measure and optimize time to value (first meaningful action). Target <30 days.
- **Adoption Monitoring**: Track user adoption metrics (active users, feature usage). Identify and address low adoption.
- **Quarterly Business Reviews**: Schedule QBRs to review progress, gather feedback, and identify expansion opportunities.
- **Success Metrics**: Define and track success metrics (time to value, adoption rate, customer satisfaction, renewal rate).

## Checklist

### Preparation Checklist
- [ ] Obtain SOC2 Type II certification
- [ ] Obtain ISO 27001 certification (if applicable)
- [ ] Create standard MSA template
- [ ] Create standard DPA template
- [ ] Create standard SLA template
- [ ] Create BAA template (if HIPAA)
- [ ] Create security policy document
- [ ] Create privacy policy
- [ ] Create incident response plan
- [ ] Create disaster recovery plan
- [ ] Create data retention policy
- [ ] Create vendor management policy
- [ ] Create subprocessor list
- [ ] Obtain cyber liability insurance
- [ ] Build public trust center
- [ ] Create SSO configuration guide
- [ ] Create SCIM configuration guide
- [ ] Create admin training materials
- [ ] Create end user training materials
- [ ] Hire customer success team

### Sales Qualification Checklist
- [ ] Identify customer size (SMB, mid-market, enterprise)
- [ ] Identify security requirements (SOC2, ISO, pen tests)
- [ ] Identify technical requirements (SSO, SCIM, integrations)
- [ ] Identify legal requirements (MSA, DPA, SLA, BAA)
- [ ] Identify procurement requirements (PO, vendor registration)
- [ ] Identify decision makers
- [ ] Set realistic timeline expectations
- [ ] Document all customer requirements
- [ ] Share requirements with relevant teams

### Security Review Checklist
- [ ] Create standard response library (200+ questions)
- [ ] Collect all evidence files
- [ ] Assign security team member to customer
- [ ] Schedule security review calls
- [ ] Complete security questionnaire
- [ ] Share SOC2 report under NDA
- [ ] Share penetration test results
- [ ] Address security concerns
- [ ] Obtain security approval
- [ ] Document lessons learned

### Legal Review Checklist
- [ ] Prepare standard MSA template
- [ ] Prepare standard DPA template
- [ ] Prepare standard SLA template
- [ ] Prepare BAA template (if HIPAA)
- [ ] Identify non-negotiable terms
- [ ] Set liability cap limits
- [ ] Assign legal team member to customer
- [ ] Send initial contract package
- [ ] Respond to legal comments within 48 hours
- [ ] Negotiate terms
- [ ] Obtain legal approval
- [ ] Execute contracts via DocuSign
- [ ] Store executed contracts

### Procurement Checklist
- [ ] Complete vendor registration (if required)
- [ ] Prepare W-9 form (US vendors)
- [ ] Obtain certificate of insurance
- [ ] Prepare banking details
- [ ] Understand invoice format requirements
- [ ] Understand payment terms
- [ ] Assign finance team member to customer
- [ ] Submit vendor registration
- [ ] Receive Purchase Order (PO)
- [ ] Send invoice
- [ ] Receive payment

### Technical Onboarding Checklist
- [ ] Assign implementation engineer
- [ ] Schedule kickoff call
- [ ] Configure SSO (SAML or OIDC)
- [ ] Test SSO with test account
- [ ] Configure SCIM (if required)
- [ ] Test SCIM provisioning
- [ ] Configure IP whitelisting (if required)
- [ ] Configure subdomain/vanity URL (if required)
- [ ] Configure integrations
- [ ] Perform data migration (if required)
- [ ] Create test users
- [ ] Validate technical setup
- [ ] Document technical configuration

### Training Checklist
- [ ] Schedule admin training
- [ ] Prepare admin training materials
- [ ] Conduct admin training
- [ ] Prepare end user training materials
- [ ] Create video walkthroughs
- [ ] Schedule end user training
- [ ] Conduct end user training
- [ ] Identify pilot users
- [ ] Conduct pilot rollout
- [ ] Gather pilot feedback
- [ ] Address pilot issues
- [ ] Plan full rollout
- [ ] Execute full rollout
- [ ] Monitor adoption

### Communication Checklist
- [ ] Designate single point of contact
- [ ] Create communication plan
- [ ] Schedule weekly status updates
- [ ] Define milestones and dates
- [ ] Set up stakeholder updates
- [ ] Create status report template
- [ ] Send weekly updates
- [ ] Celebrate milestone completions
- [ ] Address issues proactively
- [ ] Maintain communication log

### Post-Onboarding Checklist
- [ ] Schedule Week 1 daily check-ins
- [ ] Schedule Week 2-4 weekly check-ins
- [ ] Schedule Month 1 check-in
- [ ] Define time to value metric
- [ ] Track time to value
- [ ] Set up adoption monitoring
- [ ] Monitor active users
- [ ] Monitor feature usage
- [ ] Address low adoption
- [ ] Schedule QBRs
- [ ] Prepare QBR agenda
- [ ] Conduct QBRs
- [ ] Track customer satisfaction (NPS, CSAT)
- [ ] Track renewal rate
- [ ] Identify expansion opportunities

### Documentation Checklist
- [ ] Create onboarding project plan template
- [ ] Create onboarding checklist
- [ ] Document customer requirements
- [ ] Document technical configuration
- [ ] Document security responses
- [ ] Document legal negotiations
- [ ] Document procurement process
- [ ] Document training materials
- [ ] Create troubleshooting guide
- [ ] Create FAQ document

### Tools Setup Checklist
- [ ] Configure CRM (Salesforce, HubSpot)
- [ ] Set up deal stages
- [ ] Configure project management tool (Asana, Monday.com)
- [ ] Create onboarding project template
- [ ] Set up document signing (DocuSign, PandaDoc)
- [ ] Configure security portal (SafeBase, Whistic)
- [ ] Set up monitoring dashboards
- [ ] Configure error alerts
- [ ] Set up analytics tracking

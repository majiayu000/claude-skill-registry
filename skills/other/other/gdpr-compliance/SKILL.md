---
name: gdpr-compliance
description: Ensure GDPR compliance for marketing activities including consent management, data processing, privacy notices, and data subject rights
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# GDPR Compliance for Marketing

> Ensure your marketing activities comply with GDPR requirements for consent, data processing, and privacy rights.

## When to Use This Skill

- Designing consent collection flows
- Writing privacy notices
- Auditing marketing data practices
- Handling data subject requests
- Documenting lawful basis

## Methodology Foundation

Based on **GDPR Articles 6, 7, 12-23** and **EDPB Guidelines**, covering:
- Lawful basis determination
- Consent requirements
- Transparency obligations
- Data subject rights
- Documentation requirements

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Explains GDPR requirements | Business risk tolerance |
| Drafts compliant language | Implementation priority |
| Identifies gaps | Legal interpretation |
| Creates documentation | DPO consultation needs |
| Suggests controls | Resource allocation |

## Instructions

### Step 1: Lawful Basis Assessment

**Six Lawful Bases (Article 6):**

| Basis | Marketing Use | Documentation Needed |
|-------|---------------|----------------------|
| **Consent** | Email marketing, cookies, tracking | Consent records |
| **Contract** | Customer communications | Contract terms |
| **Legitimate Interest** | Soft opt-in, B2B marketing | LIA document |
| **Legal Obligation** | Regulatory comms | Legal reference |
| **Vital Interest** | Rarely applicable | - |
| **Public Task** | Rarely applicable | - |

**Marketing Activity Mapping:**

| Activity | Typical Basis | Requirements |
|----------|---------------|--------------|
| Email newsletter | Consent | Double opt-in, easy unsubscribe |
| Existing customer upsell | Legitimate Interest | LIA, opt-out available |
| Cold B2B outreach | Legitimate Interest | LIA, clear identity |
| Website cookies | Consent | Banner, granular choices |
| Retargeting ads | Consent | Cookie consent |
| Lead magnets | Consent | Clear purpose, separate consent |

### Step 2: Consent Requirements

**Valid Consent Criteria (Article 7):**
| Requirement | What It Means | Example |
|-------------|---------------|---------|
| Freely given | No bundling, no penalty | Separate from T&Cs |
| Specific | Clear purpose stated | "Marketing emails about [X]" |
| Informed | Who, what, why explained | Privacy notice linked |
| Unambiguous | Clear affirmative action | Unchecked checkbox |
| Withdrawable | Easy to revoke | One-click unsubscribe |

**Consent Record Requirements:**
```
Record for each consent:
- Who consented (identifier)
- When (timestamp)
- What they consented to (purpose)
- How (mechanism)
- What they were told (notice version)
```

### Step 3: Privacy Notice Requirements

**Required Elements (Articles 13-14):**

| Element | First-Party Data | Third-Party Data |
|---------|------------------|------------------|
| Controller identity | Required | Required |
| DPO contact | If applicable | If applicable |
| Purposes | Required | Required |
| Lawful basis | Required | Required |
| Recipients | Required | Required |
| Transfers | If applicable | If applicable |
| Retention | Required | Required |
| Rights | Required | Required |
| Withdrawal | If consent | If consent |
| Complaint right | Required | Required |
| Source | N/A | Required |

### Step 4: Data Subject Rights

**Rights Framework:**

| Right | Timeline | Marketing Impact |
|-------|----------|------------------|
| Access (Art. 15) | 1 month | Provide all marketing data |
| Rectification (Art. 16) | 1 month | Update preferences |
| Erasure (Art. 17) | 1 month | Remove from lists |
| Restriction (Art. 18) | 1 month | Pause processing |
| Portability (Art. 20) | 1 month | Export in machine format |
| Objection (Art. 21) | Immediate for marketing | Stop direct marketing |

### Step 5: Documentation & Records

**Required Documentation:**
1. Records of Processing Activities (ROPA)
2. Legitimate Interest Assessments
3. Consent records and mechanisms
4. Privacy notices (versioned)
5. Data Subject Request log
6. Breach notification procedures

## Examples

### Example 1: Marketing Email Consent Flow

**Input:**
```
Design a GDPR-compliant consent flow for:
- SaaS product newsletter
- Product updates
- Promotional offers
- Third-party partner offers
```

**Output:**
```
## GDPR-Compliant Email Consent Flow

### Consent Collection UI

---

**Signup Form Fields:**

```
Email: [________________]

[ ] I agree to receive the monthly newsletter with industry insights
[ ] I agree to receive product updates and feature announcements
[ ] I agree to receive promotional offers and discounts
[ ] I agree to receive relevant offers from our trusted partners

[Sign Up]

By signing up, you confirm you've read our [Privacy Notice].
You can withdraw consent anytime via unsubscribe link or contacting us.
```

**Design Requirements:**
- All checkboxes unchecked by default
- No "select all" option
- Each purpose separate
- Privacy notice linked, not buried
- No dark patterns

---

### Consent Record Structure

```json
{
  "email": "user@example.com",
  "consents": [
    {
      "purpose": "newsletter",
      "granted": true,
      "timestamp": "2026-01-31T10:30:00Z",
      "source": "signup_form_v3",
      "notice_version": "privacy_v2.1"
    },
    {
      "purpose": "product_updates",
      "granted": true,
      "timestamp": "2026-01-31T10:30:00Z",
      "source": "signup_form_v3",
      "notice_version": "privacy_v2.1"
    },
    {
      "purpose": "promotional",
      "granted": false,
      "timestamp": null,
      "source": null,
      "notice_version": null
    },
    {
      "purpose": "third_party",
      "granted": false,
      "timestamp": null,
      "source": null,
      "notice_version": null
    }
  ],
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
```

---

### Email Footer (Required)

```
---
You're receiving this because you subscribed to our [newsletter/updates].

Manage preferences: [link]
Unsubscribe from this list: [link]
Unsubscribe from all: [link]

[Company Name]
[Address]
[Contact Email]
```

---

### Preference Center

| Subscription | Status | Action |
|--------------|--------|--------|
| Monthly Newsletter | [ON/OFF] | Industry insights and tips |
| Product Updates | [ON/OFF] | New features and improvements |
| Promotional Offers | [ON/OFF] | Discounts and special deals |
| Partner Offers | [ON/OFF] | Relevant third-party offers |

[Update Preferences] [Unsubscribe from All]

---

### Compliance Checklist

- [ ] All consents granular (separate checkboxes)
- [ ] Checkboxes unchecked by default
- [ ] Clear description of each purpose
- [ ] Privacy notice accessible
- [ ] Withdrawal mechanism clear
- [ ] Consent records stored
- [ ] Double opt-in implemented
- [ ] Unsubscribe in every email
- [ ] Preference center available
```

### Example 2: Legitimate Interest Assessment

**Input:**
```
We want to email our existing customers about related products.
Do we need consent or can we use legitimate interest?
```

**Output:**
```
## Legitimate Interest Assessment: Customer Cross-Sell

### Summary

You can likely rely on legitimate interest (not consent) for
emailing existing customers about **similar** products, but must
complete this assessment and offer easy opt-out.

---

### Three-Part LIA Test

#### 1. Purpose Test: Is There a Legitimate Interest?

**Interest:** Promote related products to existing customers
**Legitimacy:** Yes - recognized business interest in customer development
**Benefit:** Revenue growth, customer relationship deepening

✅ **PASS**

---

#### 2. Necessity Test: Is Processing Necessary?

| Question | Answer |
|----------|--------|
| Is email necessary to achieve the interest? | Yes - direct communication channel |
| Is there a less intrusive way? | In-app notifications possible but less effective |
| Is the processing proportionate? | Yes - limited frequency, relevant content |

✅ **PASS** (with conditions)

**Conditions:**
- Limit to genuinely related products
- Reasonable frequency (not daily)
- Honor opt-outs immediately

---

#### 3. Balancing Test: Individual Rights vs. Your Interest

| Factor | Assessment |
|--------|------------|
| Nature of data | Basic contact info - low sensitivity |
| Reasonable expectations | Customers expect marketing from sellers |
| Relationship | Existing customer relationship |
| Impact on individual | Minor inconvenience, easy to opt out |
| Safeguards | Opt-out in every email |

✅ **PASS**

---

### Conclusion

**Lawful Basis:** Legitimate Interest (Article 6(1)(f))

**Requirements for Compliance:**

1. **Document this LIA** and keep on file
2. **Include in privacy notice:**
   "We may contact existing customers about similar products
   based on legitimate interest. You can opt out at any time."
3. **Easy opt-out:** Every email must have unsubscribe
4. **Honor preferences:** Immediate suppression on opt-out
5. **Similar products only:** Don't expand to unrelated offerings
6. **Reasonable frequency:** No more than weekly

---

### Template Email Footer

```
You're receiving this as a valued [Company] customer.

Not interested in product updates?
[Opt out of marketing] | [Manage preferences]

This email was sent based on our legitimate interest in keeping
customers informed about relevant products. See our Privacy Notice
for details and your rights.
```

---

### When This Doesn't Apply

Use **consent** instead if:
- Products are significantly different
- Customer bought once 2+ years ago
- You acquired data from third party
- Customer previously opted out
- Emails are primarily promotional (not informational)
```

## Skill Boundaries

### What This Skill Does Well
- Explaining GDPR requirements
- Drafting compliant language
- Creating documentation templates
- Identifying compliance gaps

### What This Skill Cannot Do
- Provide legal advice
- Know your specific jurisdiction nuances
- Guarantee regulatory acceptance
- Replace DPO consultation

### When to Escalate to Human
- Complex cross-border transfers
- Regulatory investigation
- Data breach response
- Novel processing activities

## Iteration Guide

**Follow-up Prompts:**
- "Draft the privacy notice section for [activity]"
- "How do we handle a right to erasure request?"
- "What documentation do we need for [processing]?"
- "Is this cookie banner compliant?"

## References

- GDPR Text (Regulation 2016/679)
- EDPB Guidelines on Consent
- ICO Direct Marketing Guidance
- CNIL Cookie Guidelines

## Related Skills

- `terms-analyzer` - Terms of service review
- `contract-review` - DPA analysis
- `nda-generator` - Confidentiality

## Skill Metadata

- **Domain**: Legal / Marketing
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 1-2 hours per assessment
- **Prerequisites**: Basic GDPR familiarity

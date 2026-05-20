---
name: generating-faqs-and-help-content
description: Builds comprehensive FAQs and help center articles from customer questions and product documentation. Use when the user asks about FAQ pages, help centers, knowledge bases, support documentation, or customer questions.
---

# FAQ & Help Center Generator

## When to use this skill

- User asks to create FAQ content
- User needs help center articles
- User wants to organize customer questions
- User mentions knowledge base content
- User needs support documentation

## Workflow

- [ ] Gather question sources
- [ ] Identify common questions
- [ ] Organize by category
- [ ] Write clear answers
- [ ] Structure for search
- [ ] Create help center hierarchy

## Instructions

### Step 1: Identify Question Sources

**Common sources for FAQs:**

| Source           | How to Access              | Question Quality          |
| ---------------- | -------------------------- | ------------------------- |
| Support tickets  | Help desk exports          | High - real problems      |
| Chat logs        | Live chat transcripts      | High - specific issues    |
| Sales calls      | CRM notes, call recordings | Medium - pre-purchase     |
| Reviews          | App stores, G2, Trustpilot | Medium - public feedback  |
| Social comments  | Social listening           | Medium - casual questions |
| Search queries   | Site search, Google SC     | High - user intent        |
| User surveys     | Survey responses           | High - direct feedback    |
| Community forums | Forum threads              | High - detailed questions |

**Question extraction template:**

```markdown
## Question Extraction: [Source]

**Date reviewed:** [Date]
**Questions identified:** [Count]

| Question   | Frequency | Category   | Priority     |
| ---------- | --------- | ---------- | ------------ |
| [Question] | [Count]   | [Category] | High/Med/Low |
```

### Step 2: Question Categorization

**Standard FAQ categories:**

| Category            | Topics Covered                  |
| ------------------- | ------------------------------- |
| Getting Started     | Setup, onboarding, first steps  |
| Account & Billing   | Pricing, payments, cancellation |
| Features & Usage    | How to use, capabilities        |
| Troubleshooting     | Errors, issues, fixes           |
| Integrations        | Third-party connections         |
| Security & Privacy  | Data, compliance, safety        |
| Shipping & Delivery | For e-commerce                  |
| Returns & Refunds   | Policies, processes             |

**Category hierarchy template:**

```markdown
## Help Center Structure

### 1. Getting Started

- What is [Product]?
- How do I create an account?
- First steps after signup
- Quick start guide

### 2. Account & Billing

- How do I upgrade my plan?
- How do I cancel my subscription?
- What payment methods do you accept?
- How do I update billing information?

### 3. [Feature Category]

- How do I [common action]?
- Can I [capability question]?
- What are the limits of [feature]?

### 4. Troubleshooting

- Why isn't [feature] working?
- How do I fix [common error]?
- I can't log in - what should I do?

### 5. Integrations

- How do I connect [integration]?
- Which tools do you integrate with?
- Troubleshooting [integration] issues
```

### Step 3: Answer Structure

**FAQ answer format:**

```markdown
## [Question as headline - exact words people use]

[Direct answer in first sentence - no preamble]

[Additional context or explanation if needed - 2-3 sentences max]

**Steps (if applicable):**

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Note:** [Important caveat or tip]

**Related articles:**

- [Link to related FAQ]
- [Link to related FAQ]
```

**Answer examples:**

```markdown
## How do I cancel my subscription?

You can cancel your subscription anytime from your account settings.

Go to **Settings → Billing → Cancel Subscription** and follow the prompts.
Your access continues until the end of your current billing period.

**Steps:**

1. Log in to your account
2. Click your profile icon → Settings
3. Select Billing from the sidebar
4. Click Cancel Subscription
5. Confirm cancellation

**Note:** Canceling doesn't delete your data. You can reactivate anytime.

**Related articles:**

- How do I get a refund?
- What happens to my data after I cancel?
```

### Step 4: Writing Guidelines

**FAQ writing best practices:**

| Do                                | Don't                        |
| --------------------------------- | ---------------------------- |
| Start with the answer             | Start with "Great question!" |
| Use the exact words customers use | Use internal jargon          |
| Keep answers under 200 words      | Write essays                 |
| Include steps for processes       | Assume knowledge             |
| Link to related content           | Leave dead ends              |
| Update regularly                  | Let content go stale         |

**Tone guidelines:**

| Situation       | Tone                      | Example                                                      |
| --------------- | ------------------------- | ------------------------------------------------------------ |
| Simple how-to   | Direct, clear             | "Click Settings, then..."                                    |
| Error/problem   | Empathetic, helpful       | "We understand this is frustrating. Here's how to fix it..." |
| Policy question | Professional, transparent | "Our refund policy allows..."                                |
| Feature request | Appreciative, honest      | "Thanks for the suggestion! Currently, we don't support..."  |

### Step 5: SEO Optimization

**FAQ SEO elements:**

| Element          | Best Practice                             |
| ---------------- | ----------------------------------------- |
| Title/H1         | Use exact question (how people search)    |
| URL              | Short, keyword-rich slug                  |
| Meta description | Answer preview (156 chars)                |
| Headers          | H2 for main question, H3 for sub-sections |
| Internal links   | Link related FAQs                         |
| Schema markup    | Use FAQPage or HowTo schema               |

**FAQ schema example:**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do I cancel my subscription?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "You can cancel your subscription anytime from your account settings. Go to Settings → Billing → Cancel Subscription."
      }
    }
  ]
}
```

### Step 6: Help Article Template

**For longer help center articles:**

```markdown
# [Action-oriented title]

[One-sentence summary of what this article covers]

## Before you begin

[Prerequisites, requirements, or context needed]

- Requirement 1
- Requirement 2

## [Main process heading]

### Step 1: [Action verb]

[Explanation]

[Screenshot or visual if helpful]

### Step 2: [Action verb]

[Explanation]

### Step 3: [Action verb]

[Explanation]

## Troubleshooting

### [Common issue 1]

[Solution]

### [Common issue 2]

[Solution]

## Related articles

- [Article 1]
- [Article 2]
- [Article 3]

## Still need help?

[Contact support CTA]
```

### Step 7: FAQ Prioritization

**Priority matrix:**

| Question Type    | Frequency | Impact | Priority    |
| ---------------- | --------- | ------ | ----------- |
| Blocking issues  | High      | High   | 🔥 Critical |
| Common confusion | High      | Medium | ⚡ High     |
| Nice-to-know     | Medium    | Low    | 📋 Normal   |
| Edge cases       | Low       | Low    | 📝 Low      |

**Prioritization template:**

```markdown
## FAQ Priority List

### Critical (Create first)

- [ ] [Question] - Blocks user from completing core action
- [ ] [Question] - Causes support ticket surge

### High Priority

- [ ] [Question] - Asked weekly in support
- [ ] [Question] - Common pre-purchase question

### Normal Priority

- [ ] [Question] - Asked occasionally
- [ ] [Question] - Feature clarification

### Low Priority

- [ ] [Question] - Rare edge case
- [ ] [Question] - Advanced user query
```

### Step 8: Help Center Navigation

**Navigation structure:**

```markdown
## Help Center Architecture

### Main Navigation

├── Getting Started
│ ├── Quick Start Guide
│ ├── Account Setup
│ └── First Steps
├── Features
│ ├── [Feature 1]
│ │ ├── Overview
│ │ ├── How to Use
│ │ └── Troubleshooting
│ └── [Feature 2]
├── Account & Billing
│ ├── Manage Subscription
│ ├── Payment Methods
│ └── Invoices
├── Integrations
│ ├── [Integration 1]
│ └── [Integration 2]
└── Troubleshooting
├── Common Issues
└── Error Messages

### Search Optimization

- Add search synonyms for common terms
- Include common misspellings
- Tag articles with related keywords
```

### Step 9: Maintenance Schedule

**Keep FAQs current:**

| Task                                     | Frequency   | Responsible  |
| ---------------------------------------- | ----------- | ------------ |
| Review support tickets for new questions | Weekly      | Support lead |
| Update outdated answers                  | Monthly     | Content team |
| Check for dead links                     | Monthly     | Content team |
| Audit most-viewed articles               | Quarterly   | Product team |
| Full help center review                  | Bi-annually | All teams    |

**Update checklist:**

```markdown
## FAQ Maintenance: [Month]

- [ ] Review top 10 support tickets from last month
- [ ] Identify new FAQs needed
- [ ] Update articles affected by product changes
- [ ] Check analytics for low-performing articles
- [ ] Verify all links work
- [ ] Update screenshots if UI changed
```

## Output Format

```markdown
## FAQ Content: [Product/Feature]

**Categories:** [List of categories]
**Total FAQs:** [Count]

---

### Category: [Category Name]

#### [Question 1]

[Answer following the format guidelines]

**Related:** [Links]

---

#### [Question 2]

[Answer]

---

### Category: [Category Name]

[Continue with more Q&As]

---

## Help Center Structure

[Navigation hierarchy]

---

## Schema Markup

[FAQPage JSON-LD for all questions]

---

## Maintenance Notes

- Last updated: [Date]
- Next review: [Date]
- Questions to add: [List]
```

## Validation

Before completing:

- [ ] Questions use customer language
- [ ] Answers start with direct response
- [ ] Categories are logical and navigable
- [ ] Internal links connect related FAQs
- [ ] Answers are under 200 words
- [ ] Steps are numbered for processes
- [ ] SEO elements included
- [ ] Schema markup provided

## Error Handling

- **No question sources**: Ask for access to support tickets, chat logs, or common customer questions.
- **Too many questions**: Prioritize by frequency and impact; create top 20 first.
- **Questions too technical**: Simplify language; have support team review.
- **No clear categories**: Group by user journey stage (pre-purchase, setup, usage, troubleshooting).
- **Answers too long**: Break into separate articles or use expandable sections.

## Resources

- [Intercom Help Center Guide](https://www.intercom.com/) - Help center best practices
- [Zendesk Knowledge Base](https://www.zendesk.com/) - Support documentation patterns
- [HelpScout Docs](https://www.helpscout.com/) - Knowledge base examples
- [Schema.org FAQPage](https://schema.org/FAQPage) - Structured data documentation

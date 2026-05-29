---
name: prd-master
description: PRD writing and product definition expert. Use when writing PRDs, user stories, acceptance criteria, or prioritizing features. Covers RICE/MoSCoW frameworks, agile requirements, and specification best practices.
---
# PRD Master

## Core Principles

- **Living Document** — PRDs evolve throughout product lifecycle
- **Stakeholder Collaboration** — Early involvement prevents late rework
- **Measurable Goals** — Replace vague with quantifiable targets
- **Focused yet Flexible** — Lean structure enables adaptation
- **Problem-First** — Define the problem before jumping to solutions
- **User-Centered** — Ground decisions in user research and data

---

## Hard Rules (Must Follow)

> These rules are mandatory. Violating them means the skill is not working correctly.

### No Vague Metrics

**All metrics and requirements must be quantifiable. Vague descriptions are forbidden.**

```
❌ FORBIDDEN:
- "The app should be fast"
- "Support many users"
- "Good user experience"
- "The system should be reliable"
- "Easy to use interface"

✅ REQUIRED:
- "Page load time < 2s on 4G, < 500ms on WiFi (P95)"
- "Support 10,000 concurrent users with 99.9% uptime"
- "NPS > 50, Task completion rate > 85%"
- "99.9% availability, MTTR < 1 hour"
- "User can complete checkout in < 3 clicks"
```

### Problem Before Solution

**Never propose a solution without clearly defining the problem first.**

```
❌ FORBIDDEN:
"We should add a search bar to the navigation"

✅ REQUIRED:
"Problem: Users can't find products quickly (40% exit rate on catalog).
They need a way to filter 1000+ products by attributes.
Proposed solutions: search bar, smart filters, AI recommendations."
```

### INVEST-Compliant Stories

**All user stories must pass the INVEST criteria checklist.**

```
❌ FORBIDDEN:
- Dependent stories that can't be delivered independently
- Stories without acceptance criteria
- Stories too large to complete in one sprint
- Stories without clear user value

✅ REQUIRED:
- [ ] Independent — Can be delivered alone
- [ ] Negotiable — Details can be discussed
- [ ] Valuable — Clear user/business value
- [ ] Estimable — Team can estimate effort
- [ ] Small — Fits in one sprint
- [ ] Testable — Has acceptance criteria
```

---

## Quick Reference

### When to Use What

| Scenario | Approach | Tool/Framework |
|----------|----------|----------------|
| Feature prioritization | Scoring model | RICE, ICE |
| Release planning | Must/Should/Could/Won't | MoSCoW |
| Customer satisfaction | Delight vs basics | Kano Model |
| Sprint planning | User stories + BDD | Given-When-Then |
| Complex requirements | Traditional PRD | Full template |
| Agile iteration | Lean requirements | User stories + acceptance criteria |

---

## PRD Structure

### Essential Components

```markdown
## 1. Executive Summary
- Problem statement (2-3 sentences)
- Proposed solution (1-2 sentences)
- Success metrics (3-5 key metrics)

## 2. Context & Background
- Why now? Market opportunity or user pain
- Strategic alignment with company goals
- What happens if we don't build this?

## 3. Goals & Success Metrics
- Business objectives (revenue, retention, growth)
- User objectives (satisfaction, engagement)
- Success criteria (quantifiable targets)

## 4. Target Users & Personas
- Primary users (who benefits most?)
- Secondary users (indirect beneficiaries)
- User needs, pain points, motivations
- Jobs to be done

## 5. User Stories & Use Cases
- Core user flows
- Edge cases and error scenarios
- Integration with existing features

## 6. Requirements
- Functional requirements (what it does)
- Non-functional requirements (performance, security)
- Acceptance criteria (how we verify)

## 7. Out of Scope
- What we're explicitly NOT building
- Future considerations for later phases

## 8. Design & UX
- Link to design files (Figma, etc.)
- Key design decisions
- Accessibility requirements (WCAG 2.2 AA)

## 9. Technical Considerations
- Architecture overview
- Dependencies and integrations
- Data model changes
- API contracts

## 10. Rollout & Launch Plan
- Phased rollout strategy
- Feature flags and A/B tests
- Monitoring and alerts
- Rollback plan

## 11. Open Questions & Risks
- Unknowns requiring research
- Technical risks and mitigations
- Dependencies on other teams
```

---

## User Story Writing

### Standard Format

```
As a [persona/role],
I want to [action/goal],
So that [benefit/value].
```

### The Three C's

```
Card          — Brief description on index card
              → Captures essence, not details
              → Placeholder for conversation

Conversation  — Discussion between team members
              → Explore edge cases
              → Clarify assumptions
              → Uncover hidden requirements

Confirmation  — Acceptance criteria
              → Defines "done"
              → Testable conditions
              → Given-When-Then format
```

### INVEST Criteria

```
Independent   — Story stands alone, minimal dependencies
Negotiable    — Details emerge through conversation
Valuable      — Delivers value to users or business
Estimable     — Team can estimate effort
Small         — Completable within one sprint
Testable      — Clear acceptance criteria
```

### Examples

```markdown
## Good User Stories

### Feature: Password Reset
As a user who forgot my password,
I want to reset it via email,
So that I can regain access to my account without contacting support.

**Acceptance Criteria:**
- Given I'm on the login page
- When I click "Forgot Password"
- Then I see a form requesting my email address

- Given I've entered my registered email
- When I submit the form
- Then I receive a password reset link within 2 minutes

- Given I click the reset link within 24 hours
- When I set a new password (min 8 chars, 1 number, 1 symbol)
- Then I'm logged in automatically

### Feature: Bulk Upload
As a content manager,
I want to upload multiple products via CSV,
So that I can save time compared to manual entry.

**Acceptance Criteria:**
- Given I'm on the products page
- When I click "Bulk Upload" and select a CSV file
- Then the system validates the file format (max 10MB, .csv only)

- Given the CSV has 1000 rows
- When I start the upload
- Then I see a progress bar showing completion percentage

- Given the upload completes
- When I view the results
- Then I see: success count, error count, downloadable error report
```

### Common Mistakes

```
❌ Too technical
"As a user, I want the API to return a 200 status code"
→ Focus on user benefit, not implementation

❌ Too vague
"As a user, I want the system to be fast"
→ Define measurable performance targets

❌ Missing the "so that"
"As a user, I want to filter products by price"
→ Add the value: "so that I can find items within my budget"

❌ Too large (Epic)
"As a user, I want a complete e-commerce checkout experience"
→ Break into smaller stories: cart, address, payment, confirmation
```

---

## Acceptance Criteria

### Given-When-Then (BDD Format)

```
Given [precondition/context]
When [action/trigger]
Then [expected outcome]

And [additional context/outcome]
```

### Best Practices

```
✓ Keep scenarios focused (one behavior per scenario)
✓ Maintain clear separation of Given/When/Then
✓ Avoid UI-specific details (test behavior, not implementation)
✓ Make criteria testable and measurable
✓ Include both happy path and edge cases
✓ Use real user interactions, not hypothetical
```

### Examples

```gherkin
## E-commerce Checkout

Scenario: Successful payment with saved card
  Given I have items in my cart
  And I'm logged in with a saved payment method
  When I click "Place Order"
  Then I see an order confirmation page
  And I receive a confirmation email within 2 minutes
  And my cart is emptied

Scenario: Payment declined
  Given I'm at the payment step
  When I submit payment and the card is declined
  Then I see an error message: "Payment declined. Please try another card."
  And I remain on the payment page
  And my cart items are preserved

Scenario: Session timeout during checkout
  Given I've been idle for 30 minutes
  When I attempt to place an order
  Then I'm redirected to login
  And my cart items are preserved after re-authentication

## Search Feature

Scenario: Search with results
  Given I'm on the homepage
  When I search for "laptop"
  Then I see results within 500ms
  And results are ranked by relevance
  And I see result count: "Showing 1-20 of 156 results"

Scenario: Search with no results
  Given I'm on the search page
  When I search for "xyznonexistent"
  Then I see "No results found for 'xyznonexistent'"
  And I see search suggestions or alternative queries
```

### Alternative Format: Checklist

```markdown
For simpler features, use a checklist:

## File Upload Acceptance Criteria
- [ ] Supports formats: PDF, DOCX, XLSX (max 10MB each)
- [ ] Shows upload progress bar
- [ ] Displays file name and size after upload
- [ ] Allows removal of uploaded files
- [ ] Shows error message for unsupported formats
- [ ] Shows error message for files exceeding size limit
- [ ] Scans files for malware before processing
- [ ] Works on mobile (iOS Safari, Android Chrome)
```

---

## Prioritization Frameworks

### RICE Scoring

```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach      — How many users affected per time period?
             (users/quarter, transactions/month)
Impact     — How much does it improve their experience?
             3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal
Confidence — How certain are we?
             100% = High data, 80% = Medium, 50% = Low
Effort     — Person-months required
             (engineering + design + PM time)
```

**Example:**

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Password reset | 5000/month | 3 | 100% | 1 | 15,000 |
| Dark mode | 10000/month | 0.5 | 80% | 2 | 2,000 |
| Export to PDF | 500/month | 2 | 50% | 0.5 | 1,000 |

**When to use:** Managing many ideas, need quantitative comparison, have user data.

---

### ICE Scoring

```
ICE Score = (Impact + Confidence + Ease) / 3

Impact     — 1-10: How much business/user value?
Confidence — 1-10: How certain are we?
Ease       — 1-10: How easy to implement? (10 = very easy)
```

**Example:**

| Feature | Impact | Confidence | Ease | ICE Score |
|---------|--------|------------|------|-----------|
| One-click login | 9 | 8 | 6 | 7.7 |
| AI recommendations | 10 | 5 | 3 | 6.0 |
| Email notifications | 6 | 9 | 9 | 8.0 |

**When to use:** Quick prioritization, weekly grooming, growth experiments, speed over precision.

---

### MoSCoW Method

```
Must Have      — Critical for launch, non-negotiable
                 Without this, the product fails

Should Have    — Important but not vital
                 Painful to omit, but workarounds exist

Could Have     — Nice to have, "vitamins not painkillers"
                 Include if time/resources allow

Won't Have     — Explicitly out of scope
                 Defer to future releases
```

**Example: MVP E-commerce Site**

| Must Have | Should Have | Could Have | Won't Have |
|-----------|-------------|------------|------------|
| Product listing | Product reviews | Wishlist | AR try-on |
| Shopping cart | Related products | Gift wrapping | Live chat |
| Checkout | Order tracking | Discount codes | Loyalty program |
| Payment (Stripe) | Email receipts | Social sharing | Mobile app |
| User accounts | Guest checkout | Product comparison | Subscriptions |

**When to use:** Sprint planning, MVP scoping, release boundaries, stakeholder alignment.

---

### Kano Model

```
Basic Needs       — Must-haves, assumed by users
                    Absence = dissatisfaction, presence = neutral
                    Example: Website loads, checkout works

Performance       — More is better, linear satisfaction
                    Example: Faster page load, more payment options

Delighters        — Unexpected features that wow
                    Absence = neutral, presence = delight
                    Example: Free shipping, personalized recommendations

Indifferent       — Users don't care either way
                    Example: Animated logo, theme customization
```

**When to use:** Customer-driven decisions, balancing basics vs innovation, UX improvements.

**Process:**
1. Survey users with paired questions:
   - "How would you feel if we HAD feature X?"
   - "How would you feel if we DIDN'T have feature X?"
2. Categorize responses: Basic, Performance, Delighter, Indifferent
3. Prioritize: Cover basics first, then performance, then delighters

---

### Hybrid Approach

```
Best practice: Combine frameworks

1. Use MoSCoW to define release scope
   → Separate must-haves from nice-to-haves

2. Use RICE to rank must-haves
   → Sequence within release based on impact

3. Use Kano to ensure balance
   → Don't over-invest in basics, under-invest in delight

Example:
- All "Must Have" items → Score with RICE → Build in RICE order
- Validate with Kano → Ensure we have delighters, not just basics
```

---


## Extended Reference

Detailed material starting at `## Agile Requirements Management` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.

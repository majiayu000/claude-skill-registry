---
name: price-feedback
description: Customer expressing concerns about pricing, affordability, regional pricing issues, or requesting discounts. Often from freelancers, individual developers paying out of pocket, or users in regions with unfavorable exchange rates.
metadata:
  trigger_phrases:
    - "expensive"
    - "price is too high"
    - "can't afford"
    - "regional pricing"
    - "exchange rate"
    - "discount"
    - "price point"
    - "good amount of money"
    - "buying myself not through company"
    - "freelancer"
    - "not able to afford"
    - "pricing concern"
    - "too expensive"
  related_skills: ["discount-code-request", "ppp-pricing", "student-discount-request", "scholarship-financial-aid"]
  sample_size: "643"
  routing: "agent"
  category: "sales_pricing"
  validation: |
    required_phrases: []
    forbidden_patterns:
      - "(?i)here is a free"
      - "(?i)special discount code"
    max_length: 500
  created_from_gap_analysis: true
  source_cluster: 5
---
# Price / Affordability Feedback

## When to Use

Use this skill when a customer:
- Expresses that the course is expensive
- Mentions affordability concerns
- Asks about regional pricing or exchange rates
- Is a freelancer or individual purchaser (not company)
- Requests general pricing information

## Response Template

Thank you for sharing your feedback about pricing. We understand that course investments can be significant, especially for individual learners.

Here are some options that might help:
- **Regional pricing**: We offer purchasing power parity discounts in many countries
- **Sales**: We run periodic sales - signing up for the newsletter ensures you're notified
- **Team licenses**: If you're part of a company, team licenses can be more economical

Is there anything specific about the pricing I can help clarify?

## Common Concerns

- **Exchange rates**: Currency fluctuations affecting affordability
- **Individual vs company**: Freelancers paying out of pocket
- **Regional affordability**: Local economic conditions
- **Freelancer budgets**: Limited income for learning resources

## Example Requests

1. "It's expensive."
2. "Still with the regional pricing, it's a good amount of money in my country because of the exchange rate fluctuations."
3. "I'd really like to take your course but the price point is just too high for me, I'd be buying it myself not through a company."
4. "As a freelancer based in South Africa, I am not yet able to afford the course. Hopefully once I get a few more clients I will be able to."
5. "I'm a high school student and I don't have enough money to purchase the course even at the discounted price."

## Phrases That Work

- "We understand that course investments can be significant..."
- "Here are some options that might help..."
- "We offer purchasing power parity discounts..."
- "Is there anything specific I can help clarify..."

## Note

If the customer mentions **sanctions**, **financial hardship**, or requests **free access**, route to `scholarship-financial-aid` skill (human routing required).

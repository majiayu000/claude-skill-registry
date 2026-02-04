---
name: scholarship-financial-aid
description: Customer requesting free access due to financial hardship, sanctions, or being a student who cannot afford the course. Common from users in sanctioned countries (Iran, Afghanistan, Russia) or students on limited budgets.
metadata:
  trigger_phrases:
    - "scholarship"
    - "financial aid"
    - "can't afford"
    - "cannot afford"
    - "sanctioned country"
    - "sanctions"
    - "free access"
    - "financial hardship"
    - "from Iran"
    - "from Afghanistan"
    - "from Russia"
    - "restrictions on my country"
    - "due to sanctions"
    - "limited budget"
  related_skills: ["refund-request", "ppp-pricing", "student-discount-request"]
  sample_size: "485"
  routing: "human"
  category: "support_access"
  validation: |
    required_phrases: []
    forbidden_patterns:
      - "(?i)we can offer you free"
      - "(?i)here is your free access"
    max_length: 300
  created_from_gap_analysis: true
  source_cluster: 10
---
# Scholarship / Financial Aid Request

⚠️ **ROUTES TO HUMAN** — Policy decision required

## When to Use

Use this skill when a customer:
- Requests free access due to financial hardship
- Cannot purchase due to country sanctions (Iran, Afghanistan, Russia, etc.)
- Is a student who cannot afford the course
- Mentions being from a sanctioned country

## Response Template

Thank you for reaching out about financial assistance. We understand that course pricing can be challenging depending on your location and circumstances.

I've flagged your request for review by our team. Someone will follow up with you directly to discuss available options.

We appreciate your interest in learning and will do our best to help.

## Why Human Routing

These requests require policy decisions:
- Sanctions compliance considerations
- Case-by-case evaluation of circumstances
- Potential free access grants need human approval
- Legal/compliance implications

## Example Requests

1. "I live in Afghanistan and due to sanctions I cannot purchase the course. Is there any way to get free access?"
2. "I'm a high school student and I don't have enough money to purchase the course even at the discounted price."
3. "Due to the sanctions on my country, I can't afford a pro account. I'd really appreciate if you could help."
4. "My name is Alexandra from Russia. I was excited about the course but restrictions prevent me from purchasing."
5. "I earnestly want to become your student but because of the restrictions I cannot pay for the course."

---
name: bdd-collaboration
description: Use when facilitating BDD collaboration between developers, testers, and business stakeholders. Use when running discovery workshops and example mapping sessions.
allowed-tools:
  - Bash
  - Read
---

# BDD Collaboration

Master the collaborative aspects of Behavior-Driven Development to bridge communication between technical and business teams.

## Three Amigos Sessions

The Three Amigos brings together three perspectives:

- **Business/Product**: Defines the desired behavior
- **Development**: Understands implementation implications
- **Testing/QA**: Identifies edge cases and risks

```
Session Structure:
1. Product Owner presents the user story
2. Developer asks clarifying questions
3. Tester identifies potential edge cases
4. Team writes scenarios together
5. Everyone agrees on acceptance criteria
```

## Example Mapping

Example Mapping is a structured conversation technique:

```
┌─────────────────────────────────────────┐
│ STORY: As a customer, I want to...      │ (Yellow card)
├─────────────────────────────────────────┤
│ RULE: Orders over $50 get free shipping │ (Blue card)
│   ├── Example: $60 order = free         │ (Green card)
│   ├── Example: $49 order = $5 shipping  │ (Green card)
│   └── Question: What about $50 exactly? │ (Red card)
├─────────────────────────────────────────┤
│ RULE: Express shipping always costs $15 │ (Blue card)
│   ├── Example: $100 order express = $15 │ (Green card)
│   └── Example: $30 order express = $15  │ (Green card)
└─────────────────────────────────────────┘
```

## Discovery Workshop Format

```
1. INTRODUCE (5 min)
   - Present the feature or story
   - Share any existing context

2. EXPLORE (20 min)
   - "What are the rules?"
   - "Can you give me an example?"
   - "What could go wrong?"

3. DOCUMENT (15 min)
   - Write scenarios together
   - Capture questions for later

4. REVIEW (10 min)
   - Read scenarios aloud
   - Confirm shared understanding
```

## Ubiquitous Language

Build a shared vocabulary:

```gherkin
# Domain terms defined clearly
Feature: Subscription Management

  # Define terms in feature description
  A "subscriber" is a customer with an active subscription.
  A "churned subscriber" has cancelled within the last 30 days.
  "Winback" is re-activating a churned subscriber.

  Scenario: Winback offer for churned subscriber
    Given a churned subscriber from 15 days ago
    When they visit the pricing page
    Then they should see the winback offer
```

## Living Documentation

```gherkin
Feature: Payment Processing

  # Link to business documentation
  @jira:PAY-123
  @confluence:payment-rules

  # Version tracking
  @since:v2.1

  Scenario: Process credit card payment
    # This scenario documents the current behavior
    # Last verified: 2024-01-15
```

## When to Use This Skill

Use bdd-collaboration when you need to:

- Align team understanding of requirements
- Reduce miscommunication between roles
- Create shared ownership of quality
- Build domain knowledge across team
- Prevent defects through early discussion

## Best Practices

- Schedule regular Three Amigos sessions
- Use Example Mapping for complex stories
- Create and maintain a domain glossary
- Keep scenarios as living documentation
- Involve stakeholders in scenario reviews
- Time-box discovery sessions

## Common Pitfalls

- Skipping collaboration and writing scenarios alone
- Not including all three perspectives
- Using technical jargon with business stakeholders
- Letting scenarios become outdated
- Over-documenting simple features
- Not following up on questions raised

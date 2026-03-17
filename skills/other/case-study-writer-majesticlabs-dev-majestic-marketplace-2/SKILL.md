---
name: case-study-writer
description: Create compelling customer case studies for marketing. Guides through information gathering and produces polished case study documents.
triggers:
  - case study
  - write case study
  - customer story
  - success story
  - customer case study
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# Customer Case Study Writer

Create compelling case studies that showcase customer success stories for marketing and sales enablement.

## Information Gathering

Use `AskUserQuestion` to collect the following from the user:

### Customer Details
1. **Company name** and permission to use it (or anonymize?)
2. **Industry** and company size
3. **Role of the person you worked with** (decision maker, user, champion)

### The Story
4. **What problem were they trying to solve?** (Be specific - pain points, failed alternatives)
5. **Why did they choose your solution?** (What made you stand out?)
6. **How did implementation go?** (Timeline, challenges, support needed)
7. **What results did they achieve?** (Metrics, quotes, before/after)

### Supporting Evidence
8. **Do you have a customer quote?** (Direct testimonial is gold)
9. **What metrics can you share?** (%, $, time saved, etc.)
10. **Any surprising or unexpected benefits?**

## Case Study Structure

### 1. Headline + Executive Summary
Lead with the most impressive result:
```
[Company] Achieved [Result] with [Your Product]
```

Example: "Acme Corp Reduced Support Tickets by 73% with HelpDesk Pro"

### 2. Customer Background (2-3 sentences)
- Who they are
- What they do
- Why they matter (size, reputation, relevance to reader)

### 3. The Challenge
- What problem they faced
- What they tried before (and why it didn't work)
- What was at stake if they didn't solve it

### 4. The Solution
- Why they chose you
- How implementation worked
- Key features/capabilities that made the difference

### 5. The Results
Present with specificity:
- **Primary metric** (the headline number)
- **Secondary benefits** (unexpected wins)
- **Timeline** (how quickly they saw results)

### 6. Customer Quote
A direct quote that captures the transformation. Aim for emotional + factual:
> "We went from drowning in support tickets to actually having time to build new features. Our team morale completely changed." - Jane Smith, VP Engineering

### 7. Call to Action
What should the reader do next?

## Writing Guidelines

### Lead with Results
- Bad: "Company X implemented our solution..."
- Good: "Company X cut costs by 40% in 3 months..."

### Use Specific Numbers
- Bad: "significantly improved"
- Good: "improved by 73%"
- Better: "improved from 2 hours to 32 minutes"

### Include the Before/After
Paint the contrast between their old painful state and new better state.

### Let the Customer Speak
Use their words where possible. Direct quotes are more credible than your paraphrase.

### Keep It Scannable
- Subheadings every 2-3 paragraphs
- Bullet points for lists
- Bold key metrics
- Pull quotes for emphasis

### Match Your Audience
- For technical buyers: Include implementation details
- For executives: Focus on ROI and strategic impact
- For users: Emphasize day-to-day improvements

## Output Formats

### Full Case Study (1-2 pages)
Complete narrative with all sections. Good for website, PDF downloads, sales collateral.

### One-Page Summary
Condensed version with:
- Headline result
- 3-bullet challenge
- 3-bullet solution
- Key metric + quote

Good for sales decks, email attachments.

### Social Proof Snippet (2-3 sentences)
For landing pages and marketing materials:
```
"[Company] achieved [result] using [Product]. '[Quote]' - [Name, Title]"
```

### LinkedIn/Social Post
Conversational version for social sharing:
```
[Company] was struggling with [problem].
After implementing [solution], they saw [result].
Here's what [Name] had to say: "[Quote]"
```

## Example Output

```markdown
# TechStart Reduced Customer Churn by 47% with RetainPro

## Executive Summary
TechStart, a B2B SaaS company with 500+ customers, was losing 8% of customers monthly due to poor onboarding. After implementing RetainPro's automated onboarding sequences, they cut churn nearly in half and increased expansion revenue by 23%.

## Customer Background
TechStart provides inventory management software to mid-market retailers. With a customer base of 500+ companies and a complex product, they struggled to get new users to full adoption.

## The Challenge
- 8% monthly churn rate (industry average: 5%)
- New users took 45+ days to reach "aha moment"
- Support team overwhelmed with basic "how do I..." questions
- Expansion revenue flat because users never discovered advanced features

## The Solution
TechStart implemented RetainPro to:
- Automate personalized onboarding sequences
- Trigger in-app guidance based on user behavior
- Identify at-risk accounts before they churned

Implementation took 2 weeks with dedicated support from the RetainPro team.

## The Results
After 90 days:
- **47% reduction in churn** (8% to 4.2% monthly)
- **Time to value cut from 45 days to 12 days**
- **23% increase in expansion revenue**
- Support ticket volume down 35%

## Customer Quote
> "RetainPro paid for itself in the first month. We're not just retaining more customers - they're actually using features they never discovered before. Our expansion revenue tells the story."
>
> — Sarah Chen, VP of Customer Success, TechStart

## Ready to reduce your churn?
[CTA button or link]
```

## What This Skill Does NOT Do

- Interview your customers (you need to gather the raw information)
- Verify metrics or claims
- Get customer approval for publication
- Create visual designs or layouts

## When to Use This vs. Other Skills

| Use `case-study-writer` when... | Use other skills when... |
|---------------------------------|--------------------------|
| Showcasing customer success | Writing landing page copy (`landing-page-builder`) |
| Building social proof | Creating sales page (`sales-page`) |
| Sales enablement content | General marketing copy (`copy-editor`) |

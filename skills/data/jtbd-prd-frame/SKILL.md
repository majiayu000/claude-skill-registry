---
name: dcode:jtbd-prd-frame
description: Use when defining a feature, writing a PRD, or scoping work - reframes requirements around the user's job instead of the feature or team that owns it. Use before design or development begins.
---

# JTBD PRD Frame

Reframe feature definitions around the user's job, not the feature itself.

**For designers who think:** "We're building a referrals page... but what is the agency actually trying to do?"

## Core Principle

Every feature exists to help a user complete a job. If the PRD describes the feature without naming the job, the team will build what was specced instead of what's needed. Frame the job first, then define the feature as the means to get it done.

## When to Use

- Starting a new feature or epic
- Writing or reviewing a PRD
- Scoping a redesign or restructuring (like IA work)
- Evaluating whether a feature belongs in section A or B
- Any conversation about "where should this live?"

## The Framework

### 1. Name the Job

Ask: **"When the user comes here, what are they trying to get done?"**

Not what the feature does. What the *user* is hiring it for.

| Feature-framed | Job-framed |
|----------------|------------|
| Referrals page | "Earn money by connecting clients to products" |
| Plugin management | "Keep my client sites healthy and up to date" |
| Reports dashboard | "Prove my value to clients with data" |
| Team settings | "Control who on my team can do what" |

### 2. Write the Job Statement

Format: **[When I'm...] [I want to...] [so I can...]**

Examples:
- "When I'm onboarding a new client, I want to send them a referral link so I can earn commission and they get set up."
- "When I'm reviewing my portfolio, I want to see which sites need attention so I can prioritize my morning."

### 3. Reframe the PRD

Replace feature-centric language with job-centric language:

| PRD Section | Feature-centric | Job-centric |
|-------------|-----------------|-------------|
| **Title** | "Referral Checkout Form" | "Client Onboarding & Commission Earning" |
| **Problem** | "The form needs better UX" | "Agencies lose track of the job mid-flow" |
| **Success metric** | "Form completion rate" | "Agencies who earn their first commission" |
| **Scope** | "Fields, validation, CTA" | "Everything between 'I found a product' and 'my client is set up'" |

### 4. Test Placement

When deciding where a feature lives in the product:

Ask: **"What job does this do for the user?"** Not: "Which team owns it?"

This is how governance works. If two teams want top-level nav space, the answer isn't politics. It's: "What job? Does that job already have a home?"

| Placement question | Wrong frame | Right frame |
|--------------------|-------------|-------------|
| "Where does WooPayments go?" | "WooCommerce team owns it" | "It helps agencies earn revenue" → Earn section |
| "Where do dev tools go?" | "Engineering built them" | "They help manage client sites" → Clients section |
| "New reporting feature?" | "Analytics team request" | "Helps prove value to clients" → Already in Earn |

## Instructions

### When given a feature idea or PRD:

1. **Identify the job.** Read the spec. Ask "what's the user trying to get done?" If it's not stated, ask the user.
2. **Write the job statement.** [When I'm...] [I want to...] [so I can...]
3. **Reframe the spec.** Replace feature-centric titles, problem statements, and success metrics with job-centric ones.
4. **Check placement.** Does this job already have a home in the product? If yes, nest it there. If not, is it a new job worth a top-level section?
5. **Output the reframed PRD** with the job statement at the top.

### When reviewing an existing PRD:

Flag any section that describes the feature without naming the job. Suggest a reframe.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Job is too abstract ("be productive") | Make it specific and completable ("send my client a setup link") |
| Job is actually a feature ("use the dashboard") | Ask "why?" until you hit the real job |
| Multiple jobs crammed into one feature | Split the PRD or acknowledge the primary vs secondary job |
| Success metric measures the feature, not the job | "Form submissions" → "Agencies who earned first commission within 7 days" |

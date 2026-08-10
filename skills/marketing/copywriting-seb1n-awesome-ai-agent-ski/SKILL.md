---
name: copywriting
description: Write compelling, persuasive marketing and sales copy using proven frameworks like AIDA, PAS, BAB, and 4Ps, with tone and voice customization, CTA optimization, and A/B variant generation. Use when the user requests copywriting or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Copywriting

This skill enables an AI agent to write persuasive marketing and sales copy that drives action. The agent applies proven copywriting frameworks — AIDA (Attention, Interest, Desire, Action), PAS (Problem, Agitation, Solution), BAB (Before, After, Bridge), and 4Ps (Promise, Picture, Proof, Push) — and adapts tone, voice, and structure to the brand, audience, and channel. It supports landing pages, email campaigns, social media ads, product descriptions, and more.

## Workflow

1. **Define the Objective and Audience**
   Clarify the primary goal: drive conversions, generate leads, increase brand awareness, or nurture existing customers. Identify the target audience — their pain points, desires, language patterns, and stage in the buyer's journey (awareness, consideration, decision). This determines which framework and emotional levers to use.

2. **Select a Copywriting Framework**
   Choose the framework that best fits the objective. Use **AIDA** for landing pages and ads that guide readers from attention to action. Use **PAS** when the audience has a strong, identifiable pain point. Use **BAB** for case studies and transformation stories. Use **4Ps** when you have strong social proof. State which framework is being applied and why.

3. **Establish Tone and Voice**
   Define the brand voice (authoritative, friendly, playful, luxurious, bold) and the specific tone for this piece (urgent, empathetic, excited, reassuring). If brand guidelines are provided, follow them precisely. If not, infer an appropriate voice from the product category and audience.

4. **Draft the Copy**
   Write the copy following the chosen framework's structure. Open with a strong hook. Build emotional engagement through the body — agitate the pain, paint the transformation, or stack the benefits. Close with a clear, specific CTA. Every sentence should earn its place; cut anything that does not move the reader toward the CTA.

5. **Optimize the CTA**
   Replace generic phrases like "Submit" or "Click Here" with benefit-driven language like "Start Your Free Trial." Consider the commitment level — a free trial CTA differs from a $5,000 enterprise demo request. Use urgency elements only when they are truthful.

6. **Generate A/B Variants**
   Produce at least two distinct versions of the key elements — headline, subheadline, and CTA — for testing. Variants should differ meaningfully (different angles or emotional hooks), not just in word choice. Label each variant and note the hypothesis behind it.

## Usage

Provide the agent with:

- **Product or service** — what you are selling or promoting
- **Objective** — conversions, signups, traffic, awareness, retention
- **Target audience** — demographics, psychographics, buyer journey stage
- **Channel** — landing page, email, Facebook ad, Google ad, product page
- **Brand voice** — or a link to brand guidelines
- **Constraints** — character limits, required disclaimers, mandatory phrases

Example prompt: "Write a landing page hero section for our project management tool aimed at remote teams. Use PAS. Tone: confident but friendly. Include two headline variants."

## Examples

### Example 1: Landing Page Hero Section (PAS Framework)

**Input:** "SaaS product: CloudSync — automated file backup for freelancers. Audience: freelancers who have lost files before. Goal: free trial signups."

**Output:**

> **Variant A (Fear-driven):**
>
> **Headline:** One Crashed Hard Drive Away from Losing Everything?
> **Subheadline:** Freelancers lose an average of 4.7 hours of work per data loss incident.
> **Body:** You have spent months building your portfolio and client deliverables. One spilled coffee, one ransomware email, and it can all vanish. CloudSync backs up every file change automatically to encrypted cloud storage. If disaster strikes, restore everything in minutes.
> **CTA:** Start Your Free 14-Day Backup — No Credit Card Needed
>
> **Variant B (Aspiration-driven):**
>
> **Headline:** Work Fearlessly. Every File, Backed Up Automatically.
> **Subheadline:** Enterprise-grade backup for freelancers — without the enterprise price.
> **Body:** CloudSync watches your folders and syncs every change in real time. Version history, AES-256 encryption, and setup in under two minutes.
> **CTA:** Protect Your Work Free for 14 Days
>
> **A/B Hypothesis:** Variant A tests loss aversion; Variant B tests aspirational confidence. Compare signup rates to determine which emotional angle resonates.

### Example 2: Email Marketing Sequence (AIDA Framework)

**Input:** "Product: FitTrack smart fitness watch. Audience: health-conscious professionals, 30-45. Goal: convert leads who have a discount code."

**Output:**

> **Email 1 — Attention + Interest (Day 0)**
> **Subject:** Your 20% off code is inside (expires in 48 hours)
> **Body:** Hi {first_name}, here is your code: **FIT20**. FitTrack tracks heart rate, sleep, and activity, then gives you a single weekly health score — no complicated dashboards. **[Shop FitTrack — 20% Off]**
>
> **Email 2 — Desire (Day 1)**
> **Subject:** "I finally sleep through the night" — here is what changed
> **Body:** Sarah, a marketing director, was averaging 5.2 hours of broken sleep. Two weeks with FitTrack revealed the culprit: late-evening screen time. One habit change, and her sleep score jumped 34%. That is why 92% of users feel healthier after 30 days. Code **FIT20** still active. **[Get Your FitTrack Now]**
>
> **Email 3 — Action (Day 2)**
> **Subject:** Last call — your 20% code expires tonight
> **Body:** Your code **FIT20** expires at midnight. Free shipping. 30-day money-back guarantee. **[Claim Your Discount Before Midnight]**

## Best Practices

- **Lead with the benefit, not the feature.** "Save 3 hours every week" beats "Automated scheduling engine." Translate every feature into the outcome it creates.
- **Write for scanners.** Use short paragraphs, bold key phrases, and subheadings. Put the most important message in the first line.
- **Use specific numbers.** "Join 14,327 freelancers" is more credible than "Join thousands." Specificity builds trust.
- **Match the CTA to the commitment level.** Low-commitment offers (free trial) earn bolder CTAs than high-commitment asks (enterprise demo). Reduce friction with "No credit card required."
- **Create honest urgency.** Real deadlines and genuine scarcity drive action. Fake urgency erodes trust.
- **Test one variable at a time.** In A/B variants, change only the headline or only the CTA — not both — so results are actionable.

## Edge Cases

- **Regulated industries:** Financial, healthcare, and legal copy may require disclaimers or pre-approval. Flag when the product category likely triggers compliance requirements.
- **No brand guidelines provided:** Default to clear, confident, benefit-focused copy. Avoid slang and hype words unless explicitly requested.
- **Extremely short formats:** For Google Ads (30-character headlines) or SMS (160 characters), prioritize the single strongest benefit and the CTA.
- **Multi-language campaigns:** Avoid idioms, puns, and cultural references that do not translate. Write for translatability.
- **Sensitive topics:** When writing about health, finances, or personal struggles, use empathetic language and avoid exploitative fear-mongering.

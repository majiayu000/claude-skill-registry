---
name: presentation-creation
description: Create polished, audience-tailored presentations from outlines or documents, with support for Marp, reveal.js, Google Slides, and PPTX output formats. Use when the user requests presentation creation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Presentation Creation

This skill enables an AI agent to transform raw content — outlines, documents, meeting notes, or data — into professional presentation slide decks. The agent applies slide design principles such as one idea per slide, visual hierarchy, and minimal text to produce decks that are clear, engaging, and presentation-ready. It supports multiple output formats including Marp Markdown, reveal.js HTML, Google Slides, and PPTX.

## Workflow

1. **Gather content and define the audience.** Collect the source material — an outline, a technical document, meeting notes, or a set of talking points. Identify the target audience (executives, engineers, customers, investors) and the presentation goal (inform, persuade, train, pitch). The audience determines vocabulary depth, level of detail, and visual style. An investor pitch uses bold claims and metrics; a technical deep-dive uses architecture diagrams and code snippets.

2. **Structure the narrative arc.** Organize the content into a logical story: opening hook, problem statement, solution or key message, supporting evidence, and closing call to action. Map this arc onto a slide-by-slide outline. A typical 15-minute presentation uses 10-15 slides. Each slide should convey a single idea — if a slide needs two headings, it should be two slides. Add transition beats between sections to maintain narrative flow.

3. **Write slide content with minimal text.** For each slide, write a concise headline (under 8 words) that states the takeaway, not the topic. Use "Revenue grew 40% YoY" instead of "Revenue Overview." Keep body text to 3-5 bullet points or a single short paragraph. Where possible, replace text with visuals — a chart, diagram, screenshot, or image that communicates the point faster. Write speaker notes for each slide with the full talking points the presenter should deliver verbally.

4. **Suggest visual elements and layout.** For each slide, recommend the appropriate visual treatment: bar chart for comparisons, line chart for trends, flow diagram for processes, screenshot for product demos, icon grid for feature lists, or a full-bleed image for emotional impact. Specify layout as title-only, title-and-body, two-column, image-left, or full-image. Suggest a consistent color palette and font pairing (e.g., Inter for headings, Source Sans for body).

5. **Generate the slide deck in the target format.** Produce the complete deck in the requested format. For Marp, output a single Markdown file with `---` slide separators and Marp directives. For reveal.js, output an HTML file with section tags. For PPTX, generate a python-pptx script or direct file. For Google Slides, output a structured JSON payload compatible with the Slides API. Include speaker notes, slide numbers, and any embedded media references.

6. **Review and refine.** Check the deck against presentation best practices: no slide exceeds 40 words of body text, every slide has a clear takeaway headline, visual variety prevents monotony (not all bullet-point slides), the opening slide grabs attention, and the closing slide has a clear next step. Adjust pacing — if the deck is too long, identify slides that can be merged or moved to an appendix.

## Usage

Provide the agent with the source content (or a description of the topic), the target audience, desired slide count, and output format. The agent will return a complete slide deck with speaker notes.

**Prompt format:**

~~~
Create a presentation about [topic].
Source material: [outline, document path, or key points]
Audience: [who will see this]
Slide count: [target number of slides]
Output format: [marp / revealjs / pptx / google-slides]
~~~

## Examples

### Example 1: Product Launch Slide Deck (Marp Format)

**Input:**

~~~
Create a presentation for the launch of "Nimbus," a cloud cost optimization tool.
Audience: Engineering managers and VPs at mid-size SaaS companies.
Slide count: 7
Output format: marp
~~~

**Output:**

~~~markdown
---
marp: true
theme: default
paginate: true
---

# Nimbus
## Cut your cloud bill by 35% — automatically

![bg right:40%](cloud-hero.png)

<!-- Speaker notes: Welcome everyone. Today I'm excited to introduce Nimbus,
our new cloud cost optimization platform. By the end of this presentation,
you'll see how Nimbus can save your team six figures annually without any
code changes. -->

---

# The Problem: Cloud Spend Is Out of Control

- 73% of engineering leaders say cloud costs exceeded budget last quarter
- Idle resources, oversized instances, and forgotten dev environments
- Manual cost reviews happen quarterly at best — waste compounds daily

<!-- Speaker notes: Let's start with the pain. If you're like most teams we
talk to, your cloud bill is a source of constant surprise. The problem isn't
that you're using too much cloud — it's that nobody can see where the waste
is in real time. -->

---

# How Nimbus Works

1. **Connect** — Link your AWS, GCP, or Azure accounts in under 5 minutes
2. **Analyze** — Nimbus scans utilization, traffic patterns, and billing data
3. **Optimize** — Get prioritized recommendations ranked by savings impact
4. **Automate** — Enable auto-scaling rules and scheduled shutdowns

<!-- Speaker notes: Nimbus works in four simple steps. The onboarding is
read-only and non-invasive. No agents to install, no IAM changes beyond
read access. -->

---

# Results: What Our Beta Customers Achieved

| Company       | Monthly Savings  | Time to ROI |
|---------------|-----------------|-------------|
| Acme Corp     | $42,000 (31%)   | 2 weeks     |
| DataFlow Inc  | $67,000 (38%)   | 3 days      |
| Bright SaaS   | $28,000 (29%)   | 1 week      |

Average: **35% cost reduction** within the first month.

<!-- Speaker notes: These aren't projections — these are real numbers from
our beta cohort. DataFlow saw results in 3 days because they had a large
cluster of dev instances running 24/7. -->

---

# Built for Engineering Teams, Not Finance

- No code changes required — works at the infrastructure layer
- Slack and PagerDuty integration for real-time alerts
- Granular controls per team, environment, or service
- Full audit log — every optimization is logged and reversible

<!-- Speaker notes: We built Nimbus for engineering managers, not CFOs. You
get full control over what gets optimized and what stays untouched. Every
action is reversible with a single click. -->

---

# Pricing

- **Starter:** Free for accounts under $10K/month cloud spend
- **Pro:** 5% of realized savings (you only pay when you save)
- **Enterprise:** Custom pricing with dedicated support and SLAs

No upfront commitment. Cancel anytime.

<!-- Speaker notes: Our pricing is aligned with your success. On the Pro
plan, we take 5% of the savings we actually generate — if Nimbus doesn't
save you money, you pay nothing. -->

---

# Get Started Today

**Start your free trial at nimbus.io/start**

- 5-minute setup, no credit card required
- See your first savings recommendations within 24 hours
- Questions? Email founders@nimbus.io

<!-- Speaker notes: Thank you for your time. The setup takes 5 minutes and
you'll see your first recommendations within a day. Happy to take
questions now. -->
~~~

### Example 2: Converting a Technical Document to a Presentation Outline

**Input:**

~~~
Convert the following technical document summary into a presentation outline.
Source: "Our API gateway handles 2.3M requests/day. Current P99 latency is
450ms, target is under 200ms. Root cause: synchronous auth middleware. Proposed
fix: move auth to async verification with JWT caching. Expected impact: 60%
latency reduction. Rollout plan: canary 5% then 25% then 100% over 3 weeks."
Audience: Backend engineering team
Output format: outline
~~~

**Output:**

~~~
Slide 1: Title
  Headline: "Cutting API Gateway Latency by 60%"
  Subtitle: Backend Architecture Proposal — February 2026
  Visual: None (clean title slide)

Slide 2: Current State
  Headline: "Our P99 Latency Is 2x Over Target"
  Bullets:
    - 2.3M requests/day through the API gateway
    - Current P99: 450ms | Target: under 200ms
    - Latency spikes correlate with auth middleware execution
  Visual: Line chart showing P99 latency over past 30 days with 200ms target

Slide 3: Root Cause
  Headline: "Synchronous Auth Is the Bottleneck"
  Bullets:
    - Every request performs a synchronous token validation round-trip
    - Auth middleware adds 180-250ms per request at P99
    - Blocking call prevents connection reuse under load
  Visual: Request waterfall showing auth middleware segment highlighted

Slide 4: Proposed Solution
  Headline: "Async Auth with JWT Caching"
  Bullets:
    - Replace synchronous token validation with async JWT verification
    - Cache validated tokens in Redis with 5-minute TTL
    - Fall back to synchronous validation on cache miss
  Visual: Before/after architecture diagram showing the request flow

Slide 5: Expected Impact
  Headline: "60% Latency Reduction, Zero Downtime"
  Bullets:
    - Projected P99: ~180ms (under the 200ms target)
    - Cache hit rate expected at 92%+ based on token reuse patterns
    - No API contract changes — fully backward compatible
  Visual: Bar chart comparing current vs. projected P99 latency

Slide 6: Rollout Plan
  Headline: "Canary Rollout Over 3 Weeks"
  Bullets:
    - Week 1: 5% canary with real-time latency monitoring
    - Week 2: 25% rollout if P99 stays under 200ms
    - Week 3: 100% rollout with automated rollback trigger
  Visual: Timeline graphic showing the three rollout phases
  CTA: "Review the RFC by Friday — link in Slack #backend-arch"
~~~

## Best Practices

- **One idea per slide.** If you need two headings on a slide, make two slides. Cognitive overload kills retention. Audiences remember single, clear takeaways.
- **Use headlines that state the takeaway, not the topic.** "Revenue grew 40% YoY" is better than "Revenue Overview." The audience should understand the slide's point from the headline alone.
- **Follow a 3:1 visual-to-text ratio.** For every three slides with charts, images, or diagrams, allow at most one text-heavy slide. Visual variety sustains attention.
- **Write speaker notes for every slide.** The slides are the audience's experience; the speaker notes are the presenter's script. Never put on the slide what should be said aloud.
- **Keep the deck under 1 slide per minute of speaking time.** A 15-minute slot means 12-15 slides max. Rushing through dense slides is worse than cutting content.
- **End with a clear next step.** The final slide should tell the audience exactly what to do: visit a URL, schedule a meeting, approve a proposal, or review a document by a specific date.

## Edge Cases

- **No source material provided.** If the user gives only a topic without supporting content, generate an outline with placeholder data and clearly mark assumptions. Prompt the user to supply key metrics and claims.
- **Highly technical content for a non-technical audience.** Simplify jargon, replace architecture diagrams with high-level metaphors, and focus on outcomes (cost savings, speed improvements) rather than implementation details.
- **Very large source documents (10+ pages).** Prioritize ruthlessly. Identify the 3-5 most important points and move supporting detail to an appendix deck. Offer to generate both a summary deck and a detailed reference deck.
- **Accessibility requirements.** Ensure sufficient color contrast (WCAG AA), provide alt-text descriptions for all visuals, and avoid conveying meaning through color alone. Use large fonts (24pt+ for body, 32pt+ for headlines).
- **Multiple output formats requested.** Generate the canonical version in Marp Markdown (the most portable format), then provide conversion instructions or scripts for the additional formats.

---
name: create-comparison
description: Create a comparison article (X vs Y) that helps readers choose.
argument-hint: <subject_a> <subject_b> [audience=general] [bias=neutral] [word_count=2000]
disable-model-invocation: true
---

Create a comparison article: $ARGUMENTS

## 1. Research

Research both subjects thoroughly.

- For each subject: official features and pricing, user reviews, common complaints and praises, use cases where each excels
- Existing comparison posts (what they cover, what's missing)
- Brand knowledge base for relevant positioning
- What matters most to the target audience

## 2. Outline

Create the comparison framework.

- H1: Subject A vs Subject B with benefit for audience
- Quick verdict (TL;DR for audience — who should choose what)
- What is Subject A? / What is Subject B?
- 4-6 comparison dimensions (features, ease of use, pricing, integrations, support, scalability, security)
- Pricing comparison
- Which should you choose? (nuanced recommendation)
- FAQ

Apply bias if specified: neutral (balanced), favor_a, or favor_b — while being fair.

Target word count. Checkpoint to review outline before drafting if the user wants it.

## 3. Draft

Write the full comparison.

- Delegate to the content-writer agent for a fresh context window
- Follow outline structure; use specific facts and cite sources
- Use comparison tables for head-to-head sections
- Tone: expert and opinionated but fair; acknowledge strengths; recommend competitor when genuinely better; be transparent if we have a stake
- Verify pricing current; fact-check feature claims; ensure both get fair treatment

## 4. Finalize

Review and create final deliverable.

- Run the content-critic agent to validate brand voice
- Final checks: fair treatment, all claims verified, nuanced verdict
- Full article in markdown, title tag, meta description, recommended slug, "Last verified: [date]" note

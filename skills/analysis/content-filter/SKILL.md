---
name: content-filter
description: Filter and classify AI research content for relevance, topic, and author category. Use for bulk triage of raw content before detailed claim extraction.
---

# Content Filter Skill

Filter and classify incoming content for relevance to AI research intelligence. This skill is optimized for high-throughput bulk processing.

## Purpose

The content filter is the first stage of the extraction pipeline. It quickly assesses content to:
1. Determine relevance to AI research discourse
2. Classify by topic and content type
3. Identify author category
4. Filter out noise before expensive extraction

## Assessment Schema

For each piece of content, produce:

### 1. relevance (0.0-1.0)
How relevant is this to AI research intelligence?

| Score | Meaning |
|-------|---------|
| 0.9-1.0 | Highly relevant - substantial claims, predictions, or hints |
| 0.7-0.9 | Clearly relevant - discusses AI capabilities, progress, or debate |
| 0.5-0.7 | Moderately relevant - tangentially about AI or tech industry |
| 0.3-0.5 | Low relevance - may contain signal but mostly noise |
| 0.0-0.3 | Not relevant - personal, off-topic, or pure promotion |

### 2. topic
Primary topic category:
- `scaling`: Scaling laws, compute, training efficiency
- `reasoning`: LLM reasoning, chain-of-thought, planning
- `agents`: AI agents, tool use, autonomy
- `safety`: AI safety, alignment, control
- `interpretability`: Mechanistic interpretability
- `multimodal`: Vision, audio, video models
- `rlhf`: RLHF, preference learning, Constitutional AI
- `benchmarks`: Evals, benchmarks, capability measurement
- `infrastructure`: Training infra, chips, hardware
- `policy`: AI policy, regulation, governance
- `general`: General AI commentary
- `other`: Doesn't fit categories

### 3. contentType
What kind of content is this?
- `prediction`: Forward-looking claims about AI
- `research-hint`: Suggests unreleased work or capabilities
- `opinion`: Positioned takes on AI progress/limitations
- `factual`: Reports on current state or recent events
- `critique`: Challenges claims or work by others
- `meta`: About the AI discourse itself
- `noise`: Not substantive (personal, promotion, etc.)

### 4. authorCategory
Who is the author?
- `lab-researcher`: Works at major AI lab (Anthropic, OpenAI, DeepMind, Meta, xAI, etc.)
- `critic`: Known skeptic with credentials (Marcus, Chollet, Mitchell, Bender, etc.)
- `academic`: Academic researcher not at major lab
- `independent`: Independent practitioner or commentator
- `journalist`: Tech journalist or media
- `unknown`: Cannot determine

### 5. isSubstantive (boolean)
Does this contain actual claims worth extracting?
- `true`: Contains specific assertions, predictions, or valuable signal
- `false`: Too general, vague, or promotional to extract claims from

### 6. brief
One sentence summary of the content (max 100 characters).

## Output Format

Return JSON:
```json
{
  "assessments": [
    {
      "itemIndex": 0,
      "relevance": 0.85,
      "topic": "reasoning",
      "contentType": "opinion",
      "authorCategory": "lab-researcher",
      "isSubstantive": true,
      "brief": "Claims chain-of-thought has hit diminishing returns"
    }
  ],
  "processingNotes": "Optional batch-level observations"
}
```

## Quick Classification Heuristics

### High Relevance (0.7-1.0)
- Contains specific claims about AI capabilities
- Predictions with timeframes
- Technical discussion of methods/results
- Critique with reasoning
- Hints about unreleased work
- Debates between researchers

### Medium Relevance (0.4-0.7)
- General commentary on AI field
- Sharing papers/articles with brief comment
- Reactions to announcements
- Meta-discussion about discourse
- Industry news without analysis

### Low Relevance (0.0-0.4)
- Personal updates unrelated to AI
- Off-topic content
- Pure promotion without substance
- Scheduling/logistics
- Simple retweets without commentary
- "Interesting paper" without substantive comment

## Author Detection Tips

### Lab Researchers
Look for:
- Bio mentions: Anthropic, OpenAI, DeepMind, Google Brain, Meta AI, xAI, Mistral
- Known handles: @daborenstein, @sama, @kaborl, etc.
- Technical depth suggesting insider knowledge

### Critics
Known handles and patterns:
- @garymarcus, @fchollet, @mmitchell_ai, @emilymbender
- Pattern of challenging mainstream AI claims
- Academic credentials combined with public skepticism

### Independent
- No lab affiliation
- Often practitioners or commentators
- Examples: @simonw, @drjimfan, @nathanlambert

## Processing Guidelines

### Speed Over Depth
This skill is for throughput. Make quick assessments based on:
- Keywords and phrases
- Author identity (if known)
- Content structure
- Obvious signals

### Conservative Filtering
When in doubt about relevance:
- Score 0.3-0.5 to keep for human review
- Don't filter out potentially valuable content
- False positives are okay; false negatives lose signal

### Batch Efficiency
When processing batches:
- Process items in order
- Output assessments matching input order
- Note any batch-level patterns in processingNotes

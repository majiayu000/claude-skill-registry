---
name: content-filter
description: Filter and classify AI research content for relevance. Use when processing raw content from Twitter, Substacks, blogs, or podcasts to determine if it's worth extracting claims from. Assigns relevance scores, topics, and author categories.
---

# Content Filter Skill

Assess content for relevance to AI research intelligence gathering. Filter noise and classify what remains.

## Assessment Criteria

### 1. Relevance Score (0.0-1.0)

How relevant is this to understanding AI research progress, capabilities, limitations, or field direction?

| Score Range | Meaning | Examples |
|-------------|---------|----------|
| 0.0-0.3 | Not relevant | Personal updates, off-topic, promotional |
| 0.3-0.6 | Tangentially relevant | General tech news, adjacent topics |
| 0.6-0.8 | Relevant | Discusses AI research, capabilities, field |
| 0.8-1.0 | Highly relevant | Substantive claims, predictions, research insights |

### 2. Topic Classification

Assign ONE primary topic:

- `scaling`: Scaling laws, compute, training efficiency
- `reasoning`: LLM reasoning, chain-of-thought, planning capabilities
- `agents`: AI agents, tool use, autonomy
- `safety`: AI safety, alignment, control
- `interpretability`: Mechanistic interpretability, understanding models
- `multimodal`: Vision, audio, video models
- `rlhf`: RLHF, preference learning, Constitutional AI
- `robotics`: Embodied AI, robotics
- `benchmarks`: Evals, benchmarks, capability measurement
- `infrastructure`: Training infra, chips, hardware
- `policy`: AI policy, regulation, governance
- `general`: General AI commentary
- `other`: Doesn't fit above categories

### 3. Content Type

What kind of content is this?

- `prediction`: Makes claims about future AI capabilities/timelines
- `research-hint`: Hints at ongoing/unpublished research
- `opinion`: Expresses opinion on AI progress/direction
- `factual`: Reports factual information about released work
- `critique`: Critiques AI capabilities or claims
- `meta`: Meta-commentary on the field
- `noise`: Not substantive

### 4. Substantiveness

Does this contain actual claims, arguments, or insights?

**Substantive examples:**
- "We found that CoT prompting shows diminishing returns beyond 8 steps"
- "The next generation will likely solve ARC-AGI"
- "Interpretability research is underrated"

**Non-substantive examples:**
- "Cool paper!" (reaction only)
- "Link: [url]" (link share without commentary)
- "Having coffee ☕" (personal update)

### 5. Author Category

Classify the author:

- `lab-researcher`: Works at major AI lab (Anthropic, OpenAI, DeepMind, Meta AI, xAI, Mistral, Cohere)
- `critic`: Known AI skeptic/critic with credentials (Marcus, Chollet, Mitchell, Bender, Brooks)
- `academic`: University researcher
- `independent`: Independent researcher/commentator
- `journalist`: AI journalist
- `unknown`: Cannot determine

## Output Format

Return JSON:
```json
{
  "assessments": [
    {
      "itemIndex": 0,
      "relevance": 0.85,
      "topic": "reasoning",
      "contentType": "research-hint",
      "isSubstantive": true,
      "authorCategory": "lab-researcher",
      "brief": "One sentence summary"
    }
  ]
}
```

## Filtering Heuristics

### High Signal Indicators
- Lab researchers discussing their own work area
- Specific technical claims with numbers/benchmarks
- Predictions with timeframes
- Explicit disagreements between notable figures
- Hints using hedged language ("we've been seeing...", "I can't say much but...")

### Low Signal Indicators
- Pure link shares without commentary
- Conference attendance announcements
- Hiring posts
- Generic congratulations
- Retweets without quote
- Personal life updates
- Product launches (unless with technical claims)

### Gray Areas
- Paper summaries (relevant if includes opinion/analysis)
- Q&A responses (depends on question depth)
- Thread continuations (may need full thread context)

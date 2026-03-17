---
name: icp-creator
description: Create detailed Ideal Client Profile through guided interview. Use when the user needs to define their target audience, understand their customers' problems and language, or build an ICP for content targeting.
---

# ICP Creator (Ideal Client Profile)

Create a comprehensive ideal client profile that captures demographics, psychographics, problems, goals, and language patterns for precise content targeting.

## When to Use This Skill

- Setting up a new writing system
- Refining target audience definition
- Onboarding new clients
- Pivoting to a new market segment
- Creating content strategy

## Interview Process

### Phase 1: Demographics

Ask these questions one at a time:

1. "What age range is your ideal client?" (e.g., 28-45)
2. "Is there a gender skew, or is it balanced?"
3. "Where are they located geographically?"
4. "What's their approximate income level or budget?"
5. "What's their educational background?"

### Phase 2: Professional Profile

6. "What job titles do your ideal clients typically hold?"
7. "What industries do they work in?"
8. "What size company do they work for or own?"
9. "How many years of experience do they have?"
10. "Do they have decision-making power, or do they need approval?"

### Phase 3: Psychographics

11. "What do your ideal clients value most? (e.g., efficiency, authenticity, growth)"
12. "What do they believe about your industry or topic?"
13. "What personality traits do they typically have?"

### Phase 4: Problems & Pain Points

14. "What are their TOP 3 biggest problems or challenges?"
15. "What frustrates them about current solutions?"
16. "What are they afraid of? What keeps them up at night?"
17. "What have they tried before that didn't work?"

### Phase 5: Goals & Desires

18. "What do they want to achieve in the next 30-90 days?"
19. "What's their bigger vision for 1-3 years from now?"
20. "If they could wave a magic wand, what would the dream outcome be?"

### Phase 6: Language Patterns

21. "What words or phrases do they commonly use?"
22. "What questions do they frequently ask?"
23. "What jargon or industry terms do they know?"
24. "How do they describe their problems in their own words?"

### Phase 7: Content & Buying Behavior

25. "Where do they hang out online? What platforms?"
26. "What content formats do they prefer? (video, newsletters, podcasts, etc.)"
27. "When do they consume content? (morning, commute, evening)"
28. "What makes them skeptical or hesitant to buy?"
29. "What triggers them to take action?"

## Output Format

After gathering responses, generate a JSON file following this structure:

```json
{
  "ideal_client_profile": {
    "version": "1.0",
    "last_updated": "YYYY-MM-DD",
    "demographics": {
      "age_range": "",
      "gender": "",
      "location": "",
      "income_level": "",
      "education": ""
    },
    "professional_profile": {
      "job_titles": [],
      "industries": [],
      "company_size": "",
      "experience_level": "",
      "decision_making_power": ""
    },
    "psychographics": {
      "values": [],
      "beliefs": [],
      "personality_traits": []
    },
    "problems_and_pain_points": {
      "primary_problems": [],
      "frustrations": [],
      "fears": [],
      "failed_solutions": []
    },
    "goals_and_desires": {
      "immediate_goals": [],
      "long_term_aspirations": [],
      "dream_outcome": ""
    },
    "language_patterns": {
      "words_they_use": [],
      "phrases_they_say": [],
      "questions_they_ask": [],
      "jargon_they_know": []
    },
    "content_consumption": {
      "platforms": [],
      "content_formats": [],
      "consumption_time": "",
      "attention_span": ""
    },
    "objections": {
      "common_objections": [],
      "trust_barriers": []
    },
    "buying_triggers": {
      "emotional_triggers": [],
      "logical_triggers": [],
      "timing_triggers": []
    }
  }
}
```

## Instructions

1. Begin with: "Let's build your Ideal Client Profile. This helps ensure all content speaks directly to the right people. I'll ask questions one at a time - answer as specifically as possible."

2. Ask questions conversationally, one at a time

3. Push for specificity - "everyone" is not an ICP

4. Use their own words in the final profile when possible

5. After all questions, generate the complete JSON

6. Save the output to `/context/icp.json`

7. Provide a one-paragraph summary of the ideal client

## Best Practices

- Help users get specific (not "business owners" but "SaaS founders with 10-50 employees")
- Capture actual phrases and words they use
- Distinguish between multiple ICPs if needed
- Focus on problems they're willing to pay to solve
- Validate the ICP makes sense for their business

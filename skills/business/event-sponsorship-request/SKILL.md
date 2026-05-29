---
name: event-sponsorship-request
description: |
  Event organizers request sponsorship or support for hackathons and conferences.
sample_size: 35
validation:
  required_phrases:
    - "support any questions related"
  forbidden_patterns: []
metrics:
  sample_size: 35
  avg_thread_length: 3.8
  top_phrases:
    - phrase: "support any questions related"
      count: 12
      percent: 34.3
    - phrase: "any questions related to"
      count: 12
      percent: 34.3
    - phrase: "questions related to the"
      count: 11
      percent: 31.4
    - phrase: "related to the course"
      count: 11
      percent: 31.4
    - phrase: "to the course and"
      count: 11
      percent: 31.4
    - phrase: "the course and platform"
      count: 11
      percent: 31.4
    - phrase: "course and platform functionality"
      count: 11
      percent: 31.4
    - phrase: "and platform functionality but"
      count: 11
      percent: 31.4
    - phrase: "platform functionality but you"
      count: 11
      percent: 31.4
    - phrase: "directly on x bluesky"
      count: 11
      percent: 31.4
---

# Event Sponsorship Request

## Response Patterns (from samples)

Common openings:
- "Hey Stepan,"
- "Hey Danny,"
- "Since there's no instructor assignment configured for this app, I'll note that this is a business development inquiry that should be routed to whoever handles partnerships and sponsorships at the company level. This is outside the scope of product support."

Common core lines:
- "Best,"
- "https://x.com/mattpocockuk"
- "https://bsky.app/profile/mattpocock.com"

Common closings:
- "Best,"
- "Since there's no instructor assignment configured for this app, I'll note that this is a business development inquiry that should be routed to whoever handles partnerships and sponsorships at the company level. This is outside the scope of product support."
- "Thanks for reaching out. I'm afraid I'm unavailable for this right now. Good luck on your event!"

## Phrases That Work (4-gram frequency)

- "support any questions related" — 12 (34.3%)
- "any questions related to" — 12 (34.3%)
- "questions related to the" — 11 (31.4%)
- "related to the course" — 11 (31.4%)
- "to the course and" — 11 (31.4%)
- "the course and platform" — 11 (31.4%)
- "course and platform functionality" — 11 (31.4%)
- "and platform functionality but" — 11 (31.4%)
- "platform functionality but you" — 11 (31.4%)
- "directly on x bluesky" — 11 (31.4%)

## Tone Guidance (observed)

- Openings trend toward: "Hey Stepan,"
- Closings often include: "Best,"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above
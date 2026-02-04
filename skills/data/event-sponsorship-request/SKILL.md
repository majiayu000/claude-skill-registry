---
name: event-sponsorship-request
description: Handle event sponsorship inquiries. Use when organizers ask for sponsorship or support for conferences or hackathons.
metadata:
  trigger_phrases:
      - "handle event"
      - "event sponsorship"
      - "sponsorship inquiries"
  related_skills: ["partnership-collaboration-inquiry", "media-press-outreach", "nonprofit-government-discount", "workshop-attendance-confirmation", "corporate-invoice"]
  sample_size: "35"
  validation: |
    required_phrases:
      - "support any questions related"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 35\navg_thread_length: 3.8\ntop_phrases:\n  - phrase: \"support any questions related\"\n    count: 12\n    percent: 34.3\n  - phrase: \"any questions related to\"\n    count: 12\n    percent: 34.3\n  - phrase: \"questions related to the\"\n    count: 11\n    percent: 31.4\n  - phrase: \"related to the course\"\n    count: 11\n    percent: 31.4\n  - phrase: \"to the course and\"\n    count: 11\n    percent: 31.4\n  - phrase: \"the course and platform\"\n    count: 11\n    percent: 31.4\n  - phrase: \"course and platform functionality\"\n    count: 11\n    percent: 31.4\n  - phrase: \"and platform functionality but\"\n    count: 11\n    percent: 31.4\n  - phrase: \"platform functionality but you\"\n    count: 11\n    percent: 31.4\n  - phrase: \"directly on x bluesky\"\n    count: 11\n    percent: 31.4"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.
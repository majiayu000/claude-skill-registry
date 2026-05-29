---
name: suggest-members
user-invocable: false
description: |
  Recommends team composition based on outcomes and mode. Invoked by launch commands during team setup.
---

Suggest additional team members based on the user's outcomes and selected mode. The lead and facilitator are always included.

**Mode guidance:**
- **Code mode** — suggest a mix of technical and domain-specific voices. Include at least one member who represents the customer or business perspective (Director of Customer Success, RevOps lead, BizOps expert).
- **Writing mode** — suggest writing-domain voices: strategist, editor, and at least one domain expert relevant to the subject matter. Researcher as needed. Avoid engineering roles unless the subject requires them.
- **General mode** — suggest domain-relevant voices that match what the outcomes actually require. Include at least one member who represents the broader qualitative or business perspective.
- **No mode provided** — default to Code mode guidance.

Keep teams to 3-5 members total. Up to 8 for complex multi-domain work. All members except the lead are read-only.

Present your suggestion.

Rules when suggesting team members:
- Avoid constraining dynamic team members too much. Over-describing what their qualities are can result in constrainment
- Be careful of introducing biases which weren't prompted by the user.

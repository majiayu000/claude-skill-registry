---
name: kai-brand
description: Brand positioning workshop — define messaging framework, voice/tone, differentiation strategy, and taglines. Use when "brand positioning", "messaging framework", "brand voice", "how should we position ourselves", "differentiation", "tagline", or any request to define or refine brand identity and messaging.
---

# kai-brand — Brand Positioning Workshop

Build a complete brand positioning system: messaging framework, voice/tone guidelines, competitive differentiation, and tagline options.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## References

Load these files as context before starting:

- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\brand-positioning.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\content-copywriting\perception-engineering.md`

## Phase 1 — Discovery

1. Read from `MARKETING.md`. Only ask about things not covered there:
   - Product/service description (what it does, who it serves)
   - Current positioning or tagline (if any)
   - Top 3 competitors
   - What makes them different (founder story, tech, approach, audience)
   - Target persona(s) from the harness persona set
2. If the user provides a URL, fetch and analyze the current site messaging.
3. Identify gaps: what the market says vs. what the user believes.

## Phase 2 — Analysis

1. Map the competitive landscape: who claims what positioning.
2. Identify the **white space** — positions no competitor owns.
3. Score current messaging against the Four U's framework:
   - Unique: Can only THIS brand say this?
   - Useful: Does it promise a clear outcome?
   - Ultra-specific: Are there concrete details?
   - Urgent: Is there a reason to care now?
4. Flag any banned words or AI slop phrases in existing copy.

## Phase 3 — Produce

Build these deliverables:

### Messaging Framework
- **Positioning statement**: For [audience] who [need], [product] is the [category] that [key benefit] because [reason to believe].
- **Value propositions**: 3 pillars, each with a headline + supporting proof point.
- **Elevator pitch**: 30-second version, 10-second version.

### Voice & Tone Guidelines
- 3 voice attributes (e.g., "Direct, not blunt")
- Do/Don't examples for each attribute
- Tone shifts by context (website vs. email vs. social vs. support)

### Differentiation Map
- Table: Feature / Us / Competitor A / Competitor B / Competitor C
- Circle the rows where you win. Flag the rows where you lose.

### Tagline Options
- Generate 10 tagline candidates.
- Score each on memorability, clarity, and differentiation.
- Recommend top 3 with rationale.

## Phase 4 — Output

1. Deliver the full messaging framework as a structured document.
2. Run all copy through the banned word check:
   - `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
3. Run the Four U's score on the positioning statement and taglines:
   - `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
4. Present the final package with a summary of scores and any flags.

## Constraints

- No banned Tier 1 words (leverage, utilize, synergy, innovative, etc.).
- No AI slop phrases.
- Taglines must be under 8 words.
- All claims must be substantiable — no empty superlatives.
- Target Four U's score: 12+/16 on the positioning statement.

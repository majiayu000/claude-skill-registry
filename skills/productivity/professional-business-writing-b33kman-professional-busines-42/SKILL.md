---
name: professional-business-writing
version: 1.0.0
description: |
  Remove AI-generated writing patterns while maintaining professional authority.
  For business communications, reports, proposals, RFP responses, white papers,
  articles, and professional writing. Strips AI patterns without becoming casual.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Professional Business Writing

Remove AI-generated patterns from professional writing while maintaining authority and credibility. Adapted from Wikipedia's "Signs of AI writing" guide for business communications.

## Your Task

When humanizing text:

1. **Identify AI patterns** - Scan for patterns below
2. **Rewrite problematic sections** - Replace with clear, direct language
3. **Preserve authority** - Maintain professional credibility
4. **Keep it tight** - Be direct without being casual or overly formal
5. **Add clarity** - Make the point sharper
6. **Final polish** - Ensure professional competence

## Professional Voice

**NOT professional:**
- Corporate speak ("synergize," "leverage," "circle back")
- Overly formal ("it is hereby noted that...")
- Over-hedged ("we believe it may perhaps be possible")
- Passive voice ("mistakes were made")

**IS professional:**
- Direct and clear
- Confident claims backed by facts
- Honest about challenges
- Respects reader's time

**Voice Rules:**
- ✓ "We'll meet the deadline" | ✗ "We're gonna nail it" (casual) | ✗ "It is anticipated" (formal)
- ✓ "We changed the methodology" | ✗ "The methodology was changed" (passive)
- ✓ "Surveyed 247 customers across 12 industries" | ✗ "Conducted extensive research"
- Mix short and long sentences naturally

## AI Patterns to Remove

### 1. Significance Inflation
**Remove:** stands/serves as, testament, vital/crucial/pivotal role/moment, underscores, reflects broader, symbolizing, marking/shaping, evolving landscape

**Before:** "The Q4 performance stands as a testament to dedication, marking a pivotal moment in our strategy."
**After:** "Q4 revenue grew 34% YoY. Enterprise deals drove 68% of new ARR."

### 2. Promotional Language
**Remove:** boasts, vibrant, rich, profound, showcasing, exemplifies, groundbreaking, renowned, nestled

**Before:** "Our groundbreaking platform showcases profound commitment, delivering a rich feature set."
**After:** "The platform launched with 12 core features. Adoption rate is 67% within 30 days."

### 3. Superficial -ing Analyses
**Remove:** highlighting/underscoring..., ensuring..., reflecting..., contributing to..., fostering..., showcasing...

**Before:** "The process streamlines operations while fostering collaboration, contributing to improved conversion."
**After:** "The new process cut deal cycles from 87 to 52 days. Conversion improved from 18% to 24%."

### 4. Vague Attributions
**Remove:** Industry reports suggest, Observers note, Experts argue, Some critics argue, several sources

**Before:** "Industry observers note our market position has strengthened significantly."
**After:** "Gartner moved us from 'Niche Player' to 'Challenger' in Q4. Pipeline grew 3x QoQ."

### 5. Formulaic Challenges
**Remove:** "Despite challenges such as X, Y, and Z, the organization continues to thrive"

**Before:** "Despite market headwinds and pressure, the team continues making significant progress."
**After:** "Q3 churn hit 6.2% (up from 4.1%). We're addressing it with dedicated CSMs for accounts over $100K."

### 6. AI Vocabulary Overuse
**Replace:** Additionally, Furthermore, Moreover, Subsequently, Consequently, Nevertheless, Thus, Hence
**With:** Also, But, So, Then, And, Yet, Still, However, Because, Since

### 7. Copula Avoidance
**Replace:** serves as, functions as, acts as, stands as, represents
**With:** is, are, has, have

### 8. Negative Parallelisms
**Remove:** "It's not just X, it's Y" or "This isn't only about X; it's about Y"

### 9. Rule of Three Overuse
**Remove:** Three adjectives, three benefits (innovation, collaboration, and growth)

### 10. False Ranges
**Remove:** "from X to Y, from A to B" when not actually a range

### 11. Em Dash Overuse
Use commas, periods, or parentheses instead of multiple em dashes

### 12. Chatbot Artifacts
**Remove entirely:** "I hope this helps!" "Great question!" "Let me know if..." "Feel free to..."

### 13. Knowledge Cutoff Hedging
**Remove:** "While specific details are limited..." "Given data available..."

### 14. Excessive Hedging
**Reduce:** could potentially possibly, might perhaps, it could be argued

### 15. Generic Conclusions
**Remove:** "The future looks bright" "Exciting times ahead" "We look forward to..."

### 16. Filler Phrases
**Remove:**
- "In order to" → "To"
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"
- "It is important to note that" → (delete)

### 17. Hyphenated Word Pairs
**Reduce:** AI over-hyphenates common terms (cross-functional, data-driven, client-facing)

### 18. Buzzword Overload
**Avoid:** synergy, leverage, circle back, move the needle, low-hanging fruit, paradigm shift, game-changer, disruptive, transformative

## Process

1. Read input carefully
2. Identify AI patterns
3. Rewrite with direct language
4. Ensure revised text is authoritative, active voice, specific, varied sentence length
5. Present humanized version

## Output Format

Provide:
1. **Humanized version**
2. **Key changes** (optional, if helpful)

## Example: Professional Email

**Before:**
> I hope this message finds you well! I wanted to reach out regarding our recent progress.
>
> Our results stand as a testament to the team's dedication and serve as a pivotal moment in the project's evolution. The numbers are remarkable, showcasing significant growth across multiple metrics and highlighting the vital role our initiatives have played.
>
> Despite challenges including resource constraints and timeline pressures, we continue to thrive and remain well-positioned for exciting opportunities ahead.

**After:**
> Project Update:
>
> We completed Phase 2 ahead of schedule—delivered March 15 vs. March 22 target. Three factors contributed:
>
> 1. Automation: New testing framework cut QA time from 40 to 12 hours per cycle
> 2. Parallel workflows: Design and development worked concurrently instead of sequentially
> 3. Scope clarity: Zero scope changes after kickoff (first time in 18 months)
>
> Phase 3 will be tighter. We have approval dependencies on two external vendors with 2-3 week lead times. Adjusting timeline to May 10 completion.
>
> Full dashboard attached. Let me know if you need clarification.

**Key changes:**
- Removed chatbot opening/closing
- Cut significance inflation
- Replaced vague claims with specific facts
- Changed hedged challenges to honest assessment
- Eliminated filler phrases and AI vocabulary
- Added clear structure

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), adapted for professional communications.

---
name: ai-slop-detector
description: Detects and removes AI writing patterns from text. Use when polishing drafts, cleaning AI-generated content, or ensuring writing sounds authentically human. Invoke with "run through slop detector", "clean this up", or "remove AI fingerprints".
allowed-tools: Read, Write, Edit
---

# AI Slop Detector

## What This Does
Takes any text and rewrites it to remove common AI writing patterns, making it sound authentically human. Returns only the cleaned final version.

## When to Use
- After generating any AI-assisted content
- Before publishing newsletters, articles, or social posts
- When text feels "too polished" or generic
- As a final quality gate in any writing workflow

## Instructions

Execute these steps NOW on the text provided:

1. **Scan** the text for patterns listed below
2. **Rewrite** each flagged section using the suggested fixes
3. **Output** the cleaned text immediately - no preamble, no explanation

The input text is everything that preceded this skill's invocation. Process it now.

---

## When Called by Another Skill

This skill is often invoked at the end of other skills (magic-model-review, bb-coaching-response, newsletter-coach, etc.).

When invoked mid-workflow:
1. The text to clean is the draft just generated
2. Process it immediately
3. Return the cleaned version for the calling skill to present

---

## LANGUAGE AND TONE PATTERNS TO ELIMINATE

### Promotional/Puffery Phrases
Remove these entirely or replace with specific facts:
- "stands as / serves as / is a testament"
- "plays a vital/significant role"
- "continues to captivate"
- "leaves a lasting impact"
- "rich cultural heritage/tapestry"
- "nestled in the heart of"
- "breathtaking," "must-visit," "stunning natural beauty"
- "enduring/lasting legacy"

**Fix:** Use specific, factual descriptions
- BAD: "The museum stands as a testament to the city's rich cultural heritage"
- GOOD: "The museum houses 3,000 artifacts spanning four centuries of local history"

### Editorializing Phrases
Remove these - present facts directly:
- "it's important to note/remember/consider"
- "it is worth noting"
- "no discussion would be complete without"
- "this article wouldn't exist without"

**Fix:** Just state the thing
- BAD: "It's important to note that the company expanded rapidly"
- GOOD: "The company opened 15 new locations between 2020-2023"

### Overused Conjunctions
Replace excessive use of:
- "moreover," "furthermore," "in addition," "on the other hand"

**Fix:** Use varied, natural transitions or combine sentences
- BAD: "Moreover, the company expanded. Furthermore, it hired new staff."
- GOOD: "The company expanded while hiring additional staff and opening three regional offices."

### Section Summaries
End paragraphs with forward-looking statements or the most important point.

**Pattern to replace:** "In summary," "In conclusion," "Overall" followed by restatement
- REPLACE: "In summary, the research shows climate change affects migration patterns"
- WITH: "These migration shifts may accelerate as temperatures continue rising"

---

## STYLE AND FORMATTING PATTERNS

### Title Case in Headings
Use sentence case instead:
- BAD: "Early Life and Educational Background"
- GOOD: "Early life and education"

### Excessive Boldface
Use bold sparingly - only for true emphasis or introducing technical terms for the first time.

### Formulaic Lists
Write in flowing paragraphs instead of numbered/bulleted lists:
- BAD: "The benefits include: 1. Cost savings 2. Efficiency gains 3. Better outcomes"
- GOOD: "The program reduces costs by 15%, improves processing speed, and enhances patient satisfaction scores"

### Em-dash Overuse
Replace with varied punctuation (commas, parentheses, colons, or sentence breaks):
- BAD: "The solution is elegant — simple, effective, and affordable — exactly what we need"
- GOOD: "The solution combines simplicity with effectiveness at an affordable price point"

---

## ANALYTICAL WRITING PATTERNS

### Superficial Analysis with -ing Phrases
Replace analytical -ing phrases with specific outcomes.

**Pattern to replace:** Vague present participle comments (highlighting, demonstrating, showcasing)
- REPLACE: "The study found a 20% increase, highlighting the importance of early intervention"
- WITH: "The study found a 20% increase in recovery rates when treatment began within 48 hours"

### Vague Attributions
Attribute claims to specific sources with dates or numbers.

**Pattern to replace:** "Industry experts," "many believe," "studies show" without citation
- REPLACE: "Industry experts believe the trend will continue"
- WITH: "Tesla's Q3 report projects 25% growth in the electric vehicle sector"

### False Ranges
Use specific lists instead of artificial "from X to Y" constructions.

**Pattern to replace:** "from...to..." when not describing actual ranges
- REPLACE: "The menu features dishes from pasta to grilled meats"
- WITH: "The menu includes pasta dishes, grilled meats, and seasonal vegetables"

---

## DIRECT CONTRAST FORMULATIONS - ELIMINATE ON SIGHT

These patterns scream AI:
- "This isn't about X—it's about Y"
- "It's not X, it's Y"
- "The problem isn't X—it's Y"
- "Rather than X, focus on Y"
- "Instead of X, consider Y"
- Any sentence with "but rather" construction

**Fix:** Replace with direct positive assertions
- BAD: "Success isn't about working harder but working smarter."
- GOOD: "Success comes from working smarter and more strategically."

**Exception:** Contrast is acceptable ONLY if spaced out with substantial content between negative and positive (2-3+ sentences of expansion).

---

## THROAT-CLEARING OPENERS - ELIMINATE ON SIGHT

These opening gambits announce "AI wrote this":
- "Here's the thing:"
- "Let me be clear:"
- "The uncomfortable truth is"
- "Let that sink in."
- Starting sentences with "So" or "Look,"
- "In today's fast-paced world"
- "In the realm of"

**Fix:** Start with the actual point
- BAD: "Here's the thing: most coaches struggle with content."
- GOOD: "Most coaches struggle with content."

---

## EMPHASIS CRUTCHES - ELIMINATE ON SIGHT

AI loves these dramatic punctuation patterns:
- "That's it. That's the [noun]."
- "And that's okay."
- "Not because X. Because Y." (staccato variant)
- "Ready to level up?"
- "The best part?"
- "And here's the kicker"
- "Enter: [thing]"

**Fix:** Let the content carry the weight
- BAD: "That's it. That's the strategy."
- GOOD: "The entire strategy fits in one sentence."

---

## DRAMATIC FRAGMENTATION - USE SPARINGLY

AI overuses these for false drama:
- One-sentence paragraphs (when not warranted)
- Punchy one-liners at the end of every section
- "X changed everything."
- Short hook questions in isolation

**Fix:** Vary paragraph length naturally. Reserve one-liners for genuine impact.
- BAD: "Then I discovered AI agents.\n\nEverything changed."
- GOOD: "Then I discovered AI agents, and the whole model shifted."

---

## WORD SUBSTITUTIONS

| AVOID | USE INSTEAD |
|-------|-------------|
| "leverages" | "uses" |
| "encompasses" | "includes" |
| "facilitates" | "enables" or "allows" |
| "utilized" | "used" |
| "commenced" | "began" or "started" |
| "subsequent to" | "after" |
| "prior to" | "before" |
| "in order to" | "to" |
| "serves to" | "helps" or omit entirely |
| "delve" | "explore" or "examine" |
| "navigate" | "work through" or "handle" |
| "unpack" | "explain" or "break down" |
| "tapestry" | "mix" or "combination" |
| "realm" | "area" or "field" |
| "embark" | "start" or "begin" |
| "harness" | "use" or "apply" |
| "illuminate" | "show" or "reveal" |
| "pivotal" | "important" or "key" |
| "robust" | "strong" or "solid" |

---

## STRUCTURAL PATTERNS

### Essay-like Organization
Use inverted pyramid structure (important info first) or natural conversational flow.

**Pattern to replace:** Five-paragraph essay structure with thesis statements and formal conclusions

### Rule-of-Three Overuse
Vary list lengths and replace generic adjectives with specific details.

**Pattern to replace:** Constant groupings of three generic qualities
- REPLACE: "The platform is fast, reliable, and secure"
- WITH: "The platform processes requests in under 200ms with 99.9% uptime and bank-level encryption"

### Knowledge Disclaimers
Remove AI hedging phrases entirely - state facts directly.

**Patterns to remove:** "as of [date]," "based on available information," "while specific details are limited"

### Chatbot Hedging
Use direct assertions backed by specific data.

**Pattern to replace:** Excessive qualifiers (appears to, tends to, seems to, might)
- REPLACE: "The data appears to suggest that users tend to prefer the new interface"
- WITH: "Users prefer the new interface by a 3:1 margin in testing"

---

## VERIFICATION CHECKLIST

Before returning cleaned text, verify:
1. No section ends with a summary statement
2. No "challenges and future prospects" formulaic sections
3. No excessive em-dashes or repeated punctuation patterns
4. No title case in headings
5. No promotional language about "rich heritage" or "cultural significance"
6. No vague attributions without specific sources
7. Varied sentence structures and lengths
8. Specific facts and figures rather than general statements
9. Natural flow between paragraphs without formulaic transitions
10. No direct contrast formulations ("This isn't X—it's Y")
11. No throat-clearing openers ("Here's the thing", "Let me be clear")
12. No emphasis crutches ("That's it. That's the [noun].")
13. Varied paragraph lengths (not all one-sentence or all same length)

---

## Output Format

Return only the cleaned text. No preamble, no explanation of changes, no "Here's the cleaned version:" - just the polished content ready to use.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-01-17 | Added throat-clearing, emphasis crutches, dramatic fragmentation; expanded word substitutions (+10 words); 13-point checklist |
| 1.1.0 | 2026-01-15 | Directive instructions for immediate execution, positive framing, skill chaining section |
| 1.0.0 | 2026-01-01 | Initial creation from Write with AI prompt |

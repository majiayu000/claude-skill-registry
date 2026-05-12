<!-- SOURCE-OF-TRUTH: shared/references/humanizer_checklist.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Humanizer Checklist

<!-- SCOPE: Anti-AI-slop audit for any skill that publishes text. Final pass before presenting draft to user. -->
<!-- DO NOT add here: GitHub markdown syntax → discussion_formatting.md; announcement/response templates → per-skill references -->
<!-- SOURCE: Wikipedia WikiProject AI Cleanup (24 patterns), adapted for GitHub Discussions context -->

Run this checklist as a final audit on any draft before presenting to user.

---

## Anti-AI Patterns (Detect and Fix)

### Content

| Pattern | AI Tells | Fix |
|---------|----------|-----|
| **Significance inflation** | "marking a pivotal moment in the evolution of..." | State the fact: "was added in v2.0" |
| **Promotional language** | "powerful", "seamless", "cutting-edge", "groundbreaking" | Drop the adjective or replace with a specific claim |
| **Generic conclusions** | "The future looks bright", "Exciting times ahead" | Specific next steps or cut entirely |
| **Formulaic challenges** | "Despite challenges... continues to thrive" | Name the actual challenge or remove |

### Language

| Pattern | AI Tells | Fix |
|---------|----------|-----|
| **AI vocabulary** | Additionally, Furthermore, Moreover, testament, landscape, showcasing, leverage, utilize, foster, streamline, delve, tapestry, multifaceted | Use: also, shows, use, help, explore, varied |
| **Copula avoidance** | "serves as", "functions as", "stands as", "acts as" | Use: "is", "has" |
| **Rule of three** | "innovation, inspiration, and insights" | Use the natural number of items (1, 2, or 4 is fine) |
| **Negative parallelisms** | "It's not just X, it's Y" | State Y directly |
| **Filler phrases** | "In order to", "Due to the fact that", "It's important to note that", "It's worth mentioning" | "To", "Because", cut entirely |
| **Excessive hedging** | "could potentially possibly", "it might be argued that" | "may", state it or cut it |

### Tone

| Pattern | AI Tells | Fix |
|---------|----------|-----|
| **Sycophantic openers** | "Great question!", "You're absolutely right!", "That's a fantastic idea!" | Respond directly. Skip the flattery |
| **Chatbot artifacts** | "I hope this helps!", "Let me know if you need anything!", "Happy to help!" | Remove entirely |
| **Em dash overuse** | "tools—not the people—yet this continues—" | Use commas or periods. Max 1 em dash per paragraph |

---

## Positive Voice Rules

What TO do (not just what to avoid):

| Rule | Example |
|------|---------|
| **Be specific** | "reduces 9 HTTP calls to 1" not "significantly improves performance" |
| **Be direct** | "This is a profiler" not "This serves as a profiling mechanism" |
| **Vary rhythm** | Mix short sentences with longer ones. Not all the same length |
| **Use plain verbs** | "finds", "fixes", "checks" not "leverages", "facilitates", "orchestrates" |
| **First person when honest** | "We built this because..." not "This was developed to address..." |
| **Repeat when clearest** | Say "profiler" 3 times, not "profiler... analysis tool... diagnostic engine" |
| **State opinions** | "This is faster" not "This could potentially be considered faster" |

---

## Audit Protocol

After composing a draft, scan for:

1. **Word scan:** Ctrl+F for AI vocabulary words (Additionally, Furthermore, Moreover, testament, landscape, showcasing, leverage, utilize, foster, streamline, delve, tapestry, multifaceted, Additionally). Replace each
2. **Pattern scan:** Read first sentence of each paragraph — do they all start with similar structure? Vary them
3. **Adjective audit:** For each adjective (powerful, seamless, robust, comprehensive), ask: "can I replace this with a number or specific claim?" If not, cut it
4. **Rule-of-three check:** Any group of exactly 3 items? If the 3 are generic ("speed, quality, reliability"), cut to the ones that actually matter
5. **Conclusion check:** Does the ending say "the future looks bright" or similar? Replace with specific next steps or remove
6. **Em dash count:** More than 2 in the entire draft? Convert extras to commas/periods

**Gate:** If 3+ patterns found, rewrite the flagged sections before presenting to user.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-14

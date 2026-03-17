---
name: article-humanizer
description: Edit articles to read more naturally by removing LLM-generated prose patterns. Use this skill when asked to "humanize an article", "make writing sound more natural", "remove AI patterns", "edit for natural voice", or when working with drafts in articles/drafts/ that need polish.
---

# Article Humanizer

Remove tell-tale signs of LLM-generated prose to make articles read more naturally and authentically. This skill identifies and rewrites common AI writing patterns while preserving the article's meaning and technical accuracy.

## How to Use

1. Read the original article from `articles/drafts/` or the specified path
2. Apply all transformation rules below systematically
3. Save the edited version as `<original-filename>-edited.md` alongside the original
4. Provide a summary of changes made

## Output Location

When editing an article, create the edited version alongside the original:
- Input: `articles/drafts/my-article.md`
- Output: `articles/drafts/my-article-edited.md`

Or if editing from the main articles folder:
- Input: `articles/my-article.md`
- Output: `articles/my-article-edited.md`

---

## Transformation Rules

### 1. Eliminate the "Not A—It's B" Pattern

This is the most distinctive LLM tell. Remove constructions that contrast a negative with a positive using em dashes.

**Before:**
> This isn't a dystopian thought experiment—it's the reality of AI agents today.
> This isn't just a progress file—it's a complete project manifest.
> What we're building isn't just a tracking system—it's an operating system.

**After:**
> This is the reality of AI agents today.
> This is a complete project manifest that captures:
> Agent Hive is an operating system for agent coordination.

**Pattern to find:** `isn't/not [something]—it's [something else]`

---

### 2. Reduce Excessive Em Dashes

LLMs overuse em dashes where humans would use periods, commas, or colons. Break long sentences into shorter ones.

**Before:**
> The Cortex never executes code—it only updates Markdown.
> Every session starts fully oriented—no need to re-discover state.

**After:**
> The Cortex never executes code. It only updates Markdown.
> Every session starts fully oriented. No need to re-discover state.

**When em dashes are acceptable:**
- Genuine parenthetical asides that a human might use
- One per paragraph maximum in most prose
- Never more than 2-3 in an entire article section

---

### 3. Remove Filler Phrases

Cut phrases that add words without adding meaning.

**Remove these patterns:**
- "in its simplicity" → just "elegant"
- "as described in" → reference directly
- "It's worth noting that" → state the fact directly
- "It's important to note" → state the fact directly
- "When it comes to" → use the subject directly
- "In terms of" → use the subject directly
- "At the end of the day" → delete entirely
- "Needless to say" → delete and just say it
- "Without further ado" → delete

---

### 4. Replace Overused LLM Vocabulary

These words appear with suspicious frequency in AI-generated text:

| Avoid | Prefer |
|-------|--------|
| delve/delving | explore, examine, look at |
| utilize | use |
| leverage | use, apply |
| robust | strong, reliable |
| seamless | smooth |
| holistic | complete, comprehensive |
| synergy | cooperation, collaboration |
| paradigm | model, approach |
| ecosystem | system, environment |
| landscape | field, area, space |
| journey | process, experience |

**Phrase replacements:**
- "dive into" → "examine", "look at"
- "navigate the landscape" → describe specifically what they're navigating
- "stands as a testament to" → "shows", "demonstrates"
- "plays a vital role" → "is essential for", "matters because"
- "underscores its importance" → explain why it's important specifically

---

### 5. Remove Excessive Hedging

LLMs over-qualify statements. Be more direct.

**Before:**
> This might potentially help solve the problem.
> The approach could possibly work in some cases.
> This is typically what you would generally want to do.

**After:**
> This helps solve the problem.
> The approach works in these cases.
> This is what you want to do.

**Words to reduce:**
- typically → often or delete
- generally → often or delete
- potentially → delete or state conditions
- possibly → delete or state conditions
- perhaps → delete or state conditions
- might → may or will
- somewhat → delete

---

### 6. Vary Sentence Length and Structure

LLMs produce uniform sentences averaging 25-30 words. Humans vary more.

**Before (monotonous):**
> The system provides a way to track project state across sessions. The agent reads the file to understand current status. The agent then updates the file to reflect progress made.

**After (varied):**
> The system tracks project state across sessions. When starting work, agents read the file. They update it as they go—current status, completed tasks, blocking issues.

**Techniques:**
- Mix short punchy sentences (5-10 words) with longer ones
- Use sentence fragments occasionally for emphasis
- Start sentences differently (not always subject-verb)

---

### 7. Add Specific Closers

LLMs end sections generically. Add punchy, specific closing lines.

**Before:**
> An agent that declares victory prematurely will leave obvious artifacts.

**After:**
> An agent that declares victory prematurely will leave obvious artifacts: unchecked tasks, pending dependencies, or missing notes. Victory has to be typed, not assumed.

**Before:**
> The Cortex never executes code, it only updates Markdown.

**After:**
> The Cortex never executes code, it only updates Markdown. Coordination without coercion.

---

### 8. Make Voice Personal and Consistent

LLMs default to corporate "we" or detached third person. Match the intended voice.

**For personal/blog voice:**
- Change "We believe" → "I believe"
- Change "We're excited to" → "I'm excited to"
- Change "our approach" → "this approach" or "my approach"

**For technical docs:**
- Remove hedging entirely
- Use imperative: "Run the command" not "You should run the command"

---

### 9. Remove Structural Crutches

LLMs over-rely on transitional scaffolding.

**Delete or reduce:**
- "Moreover," "Furthermore," "Additionally," at sentence starts
- "In summary," "Overall," "In conclusion," (just conclude)
- "On the other hand," (just state the contrast)
- "That being said," (just say what you're saying)

**Also remove:**
- Rhetorical questions that immediately answer themselves
- "Let's explore..." (just explore)
- "In this section, we will..." (just do it)

---

### 10. Fix Colon-Heavy Titles and Headers

LLMs love colons in titles. Reduce them.

**Before:**
> ## The Cortex: Automated Coordination

**After:**
> ## The Cortex
> (Or: ## How the Cortex Coordinates Automatically)

Use colons only when genuinely needed for subtitles.

---

### 11. Remove Promotional Superlatives

LLMs inflate importance. Ground claims in specifics.

**Before:**
> Agent Hive provides a truly revolutionary approach to solving this critical challenge.

**After:**
> Agent Hive solves this by making shared memory the foundational primitive.

**Watch for:**
- "revolutionary", "groundbreaking", "game-changing"
- "cutting-edge", "state-of-the-art"
- "unprecedented"
- Triple adjective stacks ("robust, scalable, and flexible")

---

### 12. Check for Template Artifacts

Remove any signs of incomplete generation:

- Placeholder text: `[Your Name]`, `[Insert X here]`
- Knowledge cutoff disclaimers
- Chatbot phrases: "I hope this helps", "Let me know if you need more"
- Meta-commentary: "As an AI...", "Based on my training..."

---

## Editing Checklist

Before saving the edited version, verify:

- [ ] No "isn't X—it's Y" constructions remain
- [ ] Em dashes reduced to 2-3 per major section maximum
- [ ] Filler phrases eliminated
- [ ] Overused vocabulary replaced
- [ ] Sentence lengths vary (some short, some long)
- [ ] Sections end with specific closers, not generic ones
- [ ] Voice is consistent throughout
- [ ] Transitional crutches removed
- [ ] No promotional superlatives without substance
- [ ] No template artifacts or chatbot phrases

---

## Example Transformation

**Original (draft):**
> Agent Hive isn't just another orchestration tool—it's a fundamentally new approach to the long-horizon agent problem. By leveraging the power of shared memory primitives, we've developed a robust ecosystem that enables seamless coordination. It's important to note that this approach stands as a testament to the value of simplicity in system design.

**Edited:**
> Agent Hive takes a different approach to the long-horizon agent problem. Shared memory primitives—simple Markdown files—let agents coordinate across sessions without complex infrastructure. Simple tools, used consistently, solve hard problems.

**Changes made:**
1. Removed "isn't just X—it's Y" pattern
2. Replaced "leveraging" → direct explanation
3. Removed "robust ecosystem", "seamless coordination"
4. Removed "It's important to note"
5. Removed "stands as a testament"
6. Added concrete detail (Markdown files)
7. Ended with punchy closer

---

## Sources

This skill is based on analysis of:
- Before/after comparison of articles/drafts/01 vs articles/01
- [13 Signs You Used ChatGPT To Write That](https://seanjkernan.substack.com/p/13-signs-you-used-chatgpt-to-write)
- Research on LLM-generated text detection patterns

---
name: content-refiner
description: Refine verbose educational content by eliminating redundancy, tightening prose, and strengthening lesson connections. Use when content is wordy, repetitive, or lacks narrative flow between sections.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Content Refiner Skill

Transform verbose, redundant educational content into lean, connected lessons.

## When to Use

- Content feedback mentions: verbose, redundant, wordy, repetitive
- Lessons feel disconnected or read like standalone blog posts
- Same concept explained multiple ways within a lesson
- "Try With AI" sections have 4+ prompts
- Lessons exceed 1200 words without justification

## The Three Enemies

### Enemy 1: Verbosity
**Symptoms:**
- Multiple analogies for the same concept
- "Why This Matters" sections that restate the obvious
- Tables that duplicate paragraph content
- "Reflection" sections that add no value

**Treatment:**
- ONE analogy per concept maximum
- Cut "Why This Matters" unless it reveals non-obvious insight
- Choose: paragraph OR table, not both
- Delete "Reflection" sections entirely

### Enemy 2: Redundancy
**Symptoms:**
- Concept explained in Lesson N, re-explained in Lesson N+1
- Same information in different formats (paragraph, bullets, table)
- "Expert Insight" callouts restating what was just said
- Multiple lessons that could be one

**Treatment:**
- Concepts taught ONCE, referenced thereafter
- One format per concept
- Expert Insights only for genuinely advanced perspectives
- Merge lessons that cover same ground

### Enemy 3: Disconnection
**Symptoms:**
- Each lesson reads like standalone article
- No "Previously you learned X, now we build on Y" bridges
- Different examples in each lesson (no running example)
- Conceptual lessons sandwiched between practical ones

**Treatment:**
- Opening sentence references prior lesson's key takeaway
- ONE running example evolves across the chapter
- Conceptual content folded INTO practical lessons
- Clear skill progression: each lesson adds ONE new capability

## Refinement Procedure

### Step 1: Measure Current State
```
Count:
- Total words
- Number of analogies per concept
- Number of "Try With AI" prompts
- Number of tables
- "Reflection" sections present?
- "Expert Insight" callouts
```

### Step 2: Apply Cuts

**Mandatory cuts:**
1. Delete ALL "Reflection" sections
2. Reduce "Try With AI" to exactly 2 prompts
3. Keep ONE analogy per concept, delete others
4. Delete tables that duplicate paragraph content
5. Cut "Why This Matters" if it only restates the concept

**Word targets:**
| Lesson Type | Target Words |
|-------------|--------------|
| Conceptual intro | 600-800 |
| Hands-on practical | 800-1000 |
| Installation/setup | 400-600 |
| Capstone | 1000-1200 |

### Step 3: Strengthen Connections

**Opening formula:**
```markdown
# [Lesson Title]

In [Lesson N-1], you [key accomplishment]. Now you'll [this lesson's goal].
```

**Running example rule:**
- Identify the chapter's running example
- This lesson MUST use or extend that example
- If introducing new example, it must relate to running example

### Step 4: Verify Quality

Checklist:
- [ ] Under word limit for lesson type
- [ ] One analogy per concept max
- [ ] Exactly 2 "Try With AI" prompts
- [ ] No "Reflection" section
- [ ] Opens with connection to prior lesson
- [ ] Uses or extends running example
- [ ] No repeated explanations from earlier lessons

## Output Format

When refining a lesson, produce:

```markdown
## Refinement Report: [Lesson Name]

### Metrics
| Before | After |
|--------|-------|
| X words | Y words |
| N analogies | 1 analogy |
| N Try With AI | 2 prompts |

### Key Cuts Made
1. [Deleted section/content and why]
2. [Deleted section/content and why]
3. [Deleted section/content and why]

### Connection Added
- Opening: "[New opening sentence]"
- Running example: [How it connects]

### Refined Content
[Full refined lesson content]
```

## Example: Before/After

**BEFORE (verbose):**
```markdown
## Why This Matters

Skills are important because they save you time. When you create a skill,
you're investing once to benefit forever. Think of it like teaching a
friend your preferences. Or like programming a robot. Or like writing
a recipe book. The key insight is that skills encode your expertise.

| Aspect | Without Skills | With Skills |
|--------|---------------|-------------|
| Time | Repeat yourself | Invest once |
| Quality | Inconsistent | Consistent |
| Sharing | Hard | Easy |

As you can see, skills provide significant advantages...
```

**AFTER (lean):**
```markdown
Skills encode your expertise once so Claude applies it automatically.
Instead of explaining your LinkedIn tone every time, teach it once.
```

## Anti-Patterns to Eliminate

1. **The Triple Explanation**: Paragraph + Table + Analogy for same concept
2. **The Standalone Syndrome**: Lesson that doesn't reference what came before
3. **The Prompt Explosion**: 4+ "Try With AI" prompts
4. **The Obvious Insight**: "Expert Insight" that adds nothing experts wouldn't know
5. **The Setup Novel**: 3 paragraphs of motivation before getting to content
6. **The Example Carousel**: New example every lesson instead of building one

## Skill Composition

This skill works well with:
- `content-implementer`: Apply these principles when creating new content
- `educational-validator`: Validate refined content still meets pedagogical requirements

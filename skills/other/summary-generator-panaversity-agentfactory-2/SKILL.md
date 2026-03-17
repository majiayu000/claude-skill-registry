---
name: summary-generator
description: This skill should be used when generating lesson summaries for educational content. It extracts key concepts, mental models, patterns, and common mistakes from lesson markdown files using a Socratic extraction process. Use this skill when a lesson file needs a `.summary.md` companion file, or when reviewing/refreshing existing summaries.
---

# Summary Generator

## Overview

This skill generates concise, scannable summaries for educational lessons by extracting the essential learning elements through Socratic questioning. Summaries serve two user needs: quick review (students returning to refresh understanding) and just-in-time reference (students checking back mid-practice).

## Extraction Process (Socratic Style)

To generate a summary, work through these questions in order. Each question extracts content for one section of the summary.

### Question 1: Core Concept
> "If a student remembers only ONE thing from this lesson tomorrow, what must it be?"

Extract the single most important takeaway in 1-2 sentences. This should be the foundational insight that unlocks everything else.

**Test**: Could someone who only read this sentence explain the lesson's purpose to a peer?

### Question 2: Key Mental Models
> "What mental frameworks does this lesson install in the student's mind? What 'lenses' do they now see problems through?"

Extract 2-3 mental models—these are the reusable thinking patterns, not facts. Look for:
- Cause → Effect relationships
- Decision frameworks ("When X, do Y")
- Conceptual metaphors or analogies

**Test**: Are these transferable to new situations, or are they lesson-specific facts?

### Question 3: Critical Patterns
> "What practical techniques or patterns does this lesson teach? What can the student now DO that they couldn't before?"

Extract 2-4 actionable patterns from the lesson. These come from:
- Code examples and their purpose
- AI collaboration techniques
- Tools or commands introduced
- Workflows demonstrated

**Test**: Could a student apply these patterns without re-reading the lesson?

### Question 4: AI Collaboration Keys
> "How does AI help with this topic? What prompts or collaboration patterns make the difference?"

Extract 1-2 insights about working with AI on this topic. This should NOT expose the Three Roles framework—focus on practical collaboration patterns.

**Note**: Skip this section if the lesson doesn't involve AI collaboration (Layer 1 content).

### Question 5: Common Mistakes
> "Where do students typically go wrong? What misconceptions does this lesson correct?"

Extract 2-3 common mistakes from:
- Explicit "Common Mistakes" sections
- Error examples in the lesson
- Counterintuitive points that contradict assumptions

**Test**: Would knowing these prevent a real mistake?

### Question 6: Connections
> "What prerequisite knowledge does this build on? Where does this lead next?"

Extract navigation links:
- **Builds on**: What prior concepts are assumed
- **Leads to**: What this enables in future lessons

**Note**: This section is optional. Skip if connections aren't clear or useful.

## Output Template

Generate the summary following this exact structure:

```markdown
### Core Concept
[1-2 sentences from Question 1]

### Key Mental Models
- **[Model Name]**: [Brief explanation]
- **[Model Name]**: [Brief explanation]
- **[Model Name if needed]**: [Brief explanation]

### Critical Patterns
- [Pattern/technique 1]
- [Pattern/technique 2]
- [Pattern/technique 3 if applicable]
- [AI collaboration pattern if applicable]

### Common Mistakes
- [Mistake 1 and why it's wrong]
- [Mistake 2 and why it's wrong]
- [Mistake 3 if applicable]

### Connections
- **Builds on**: [Prior concept/chapter]
- **Leads to**: [Next concept/chapter]
```

## Length Guidelines

Adjust summary length based on lesson complexity (from frontmatter `proficiency_level`):

| Proficiency | Target Length | Reason |
|-------------|---------------|--------|
| A1-A2 (Beginner) | 150-250 words | Simpler concepts, fewer patterns |
| B1-B2 (Intermediate) | 200-350 words | More nuanced, multiple techniques |
| C1-C2 (Advanced) | 250-400 words | Complex topics, many interconnections |

## Anti-Patterns (What NOT to Include)

Following **Principle 7: Minimal Sufficient Content**, summaries must NOT contain:

- ❌ **Full explanations** — Summaries point to concepts, not re-teach them
- ❌ **Code examples** — The full lesson contains these
- ❌ **Practice exercises** — Students return to the lesson for practice
- ❌ **"What's Next" navigation** — Course structure handles this
- ❌ **Motivational content** — No "Congratulations!" or fluff
- ❌ **Layer/Stage labels** — Students experience pedagogy, not study it
- ❌ **Framework terminology** — No "Three Roles", "Layer 2", etc.

## File Naming Convention

Summary files are named by appending `.summary.md` to the lesson filename (without extension):

```
# Lesson file:
apps/learn-app/docs/05-Python/17-intro/01-what-is-python.md

# Summary file:
apps/learn-app/docs/05-Python/17-intro/01-what-is-python.summary.md
```

## Workflow

1. **Read** the target lesson file completely
2. **Extract** the lesson's proficiency level from frontmatter
3. **Answer** each Socratic question, noting extracted content
4. **Compose** the summary using the template
5. **Validate** against anti-patterns checklist
6. **Check** word count against length guidelines
7. **Write** the `.summary.md` file

## Example: Data Types Lesson Summary

For a lesson teaching Python data types at A2 proficiency:

```markdown
### Core Concept
Data types are Python's classification system—they tell Python "what kind of data is this?" and "what operations are valid?"

### Key Mental Models
- **Types → Operations**: Numbers enable math; text enables joining; booleans enable decisions
- **Type Mismatch → Error**: `5 + "hello"` fails because Python can't add numbers to text
- **Type Decision Framework**: Ask "What kind of data?" to determine the right type

### Critical Patterns
- Use `type()` to verify what type Python assigned: `type(42)` returns `<class 'int'>`
- Type hints express intent: `age: int = 25` tells both AI and humans what you expect
- 7 categories cover all data: Numeric, Text, Boolean, Collections, Binary, Special (None)

### Common Mistakes
- Storing numbers as text (`"25"` instead of `25`) prevents math operations
- Forgetting that `0.1 + 0.2` doesn't exactly equal `0.3` (floating point precision)
- Mixing types in operations without explicit conversion

### Connections
- **Builds on**: Python installation and first programs (Chapter 17)
- **Leads to**: Deep dive into numeric types and text handling (Chapters 18-20)
```

**Word count**: ~175 words (appropriate for A2)

---
name: generate-quiz
description: |
  Generate quizzes that test conceptual understanding from lessons or topics. Creates
  multiple choice, true/false, and short answer questions with explanations. Use when
  user asks to "create a quiz", "generate quiz", "test my knowledge", or "make questions".
---

# Generate Quiz

Create quizzes from lesson files or topic titles that test understanding of core concepts, not just recall of definitions.

## Workflow

1. Identify input: lesson file path OR topic title
2. If lesson file provided, read and extract main concepts
3. Identify testable concepts across cognitive levels
4. Generate varied question types
5. Include answer explanations and note references
6. Save to `/quiz/` directory

## Question Types

### Multiple Choice
Test concept application and discrimination between similar ideas.

```markdown
**Q1.** [Question stem]
- A) [Option]
- B) [Option]
- C) [Option]
- D) [Option]

**Answer:** [Letter]
**Explanation:** [Why this is correct and others are wrong]
```

### True/False
Test understanding of principles and common misconceptions.

```markdown
**Q2.** [Statement] (True/False)

**Answer:** [True/False]
**Explanation:** [Why, and clarify the misconception if false]
```

### Short Answer
Test deeper understanding and ability to explain concepts.

```markdown
**Q3.** [Open-ended question]

**Answer:** [Expected response key points]
**Explanation:** [Additional context or grading criteria]
```

## Cognitive Levels for Questions

Design questions across these levels:

| Level | Question Focus | Example Stem |
|-------|----------------|--------------|
| Understand | Explain concepts | "Which best describes..." |
| Apply | Use in new context | "In this scenario, which approach..." |
| Analyze | Break down relationships | "What is the relationship between..." |
| Evaluate | Judge or compare | "Which would be most effective for..." |

Avoid pure recall questions (covered by flashcards).

## Question Design Guidelines

### Good Questions
- Test one concept per question
- Have a clear, unambiguous correct answer
- Include plausible distractors (wrong answers that seem reasonable)
- Avoid "all of the above" or "none of the above"
- Test understanding, not trick knowledge

### Distractors Should Be
- Plausible but clearly wrong upon analysis
- Based on common misconceptions
- Similar in length and structure to correct answer
- Not obviously incorrect

### Avoid
- Double negatives
- Ambiguous wording
- Testing trivial details
- Questions with multiple correct answers (unless specified)
- Overly long question stems

## Output Template

```markdown
# [Topic] - Quiz

## Instructions
Answer all questions. Review explanations after completing the quiz.

---

## Multiple Choice

**Q1.** [Question]
- A) [Option]
- B) [Option]
- C) [Option]
- D) [Option]

---

## True/False

**Q2.** [Statement] (True/False)

---

## Short Answer

**Q3.** [Question]

---

# Answer Key

## Q1
**Answer:** [Letter]
**Explanation:** [Reasoning]
**Reference:** [Related note section]

## Q2
**Answer:** [True/False]
**Explanation:** [Reasoning]

## Q3
**Answer:** [Key points expected]
**Explanation:** [Grading guidance]

---
Source: [lesson file or topic]
Question count: [number]
Difficulty: [Basic/Intermediate/Advanced]
```

## Naming Convention

**Priority: Use source filename for traceability**

| Input Type | Output Filename | Example |
|------------|-----------------|---------|
| File path: `lessons/lesson1.md` | `/quiz/lesson1-quiz.md` | Maintains traceability |
| File path: `lessons/chapter-02.md` | `/quiz/chapter-02-quiz.md` | Maintains traceability |
| Topic title: "4D Framework" | `/quiz/4d-framework-quiz.md` | Derived from topic |

**Rules:**
- When file path provided: Extract filename (minus extension), append `-quiz`
- When topic provided: Convert to lowercase with hyphens, append `-quiz`
- This ensures clear mapping: `lessons/X.md` → `quiz/X-quiz.md`

## Question Distribution

For a standard quiz (10 questions):
- 5-6 Multiple Choice
- 2-3 True/False
- 1-2 Short Answer

Adjust based on topic complexity.

## Example Output

**Example 1 - From file:**
**Input:** `lessons/lesson1.md`
**Output:** `/quiz/lesson1-quiz.md`

**Example 2 - From topic:**
**Input:** "4D Framework"
**Output:** `/quiz/4d-framework-quiz.md`

```markdown
# 4D Framework - Quiz

## Instructions
Answer all questions. Review explanations after completing.

---

## Multiple Choice

**Q1.** A developer receives AI-generated code that compiles correctly but uses an inefficient algorithm. Which of the 4Ds is most relevant to catching this issue?
- A) Delegation
- B) Description
- C) Discernment
- D) Diligence

**Q2.** Before asking AI to write a marketing email, you should first consider whether AI is the right tool for this task. This is an example of:
- A) Platform Awareness in Delegation
- B) Product Discernment
- C) Description clarity
- D) Diligence verification

---

## True/False

**Q3.** The Description-Discernment loop means you should perfect your prompt before seeing any AI output. (True/False)

**Q4.** Prompt engineering alone is sufficient for AI Fluency. (True/False)

---

## Short Answer

**Q5.** Explain why Delegation must come before Description in the 4D Framework.

---

# Answer Key

## Q1
**Answer:** C
**Explanation:** Discernment involves critically evaluating AI outputs. Product Discernment specifically asks "Is the output good?" - checking for accuracy, coherence, and appropriateness, which would catch an inefficient algorithm.
**Reference:** notes/01-ai-fluency-4d-framework.md - Discernment section

## Q2
**Answer:** A
**Explanation:** Delegation involves deciding IF and HOW AI should be involved. Platform Awareness is understanding what AI can/cannot do well, which helps determine if AI is the right tool.

## Q3
**Answer:** False
**Explanation:** The Description-Discernment loop is iterative. You describe, get output, evaluate, then refine your description based on results.

## Q4
**Answer:** False
**Explanation:** Prompt engineering only addresses Description. AI Fluency requires all 4Ds: knowing when to use AI (Delegation), evaluating outputs (Discernment), and responsible practices (Diligence).

## Q5
**Answer:** Delegation determines whether AI should be involved at all and how. Without this step, you might ask AI to do tasks it cannot do well, or miss opportunities where AI excels. Problem Awareness (knowing your goals) and Platform Awareness (knowing AI capabilities) must be established before crafting any prompt.

---
Source: lessons/lesson1.md
Question count: 5
Difficulty: Intermediate
```

## Checklist

Before completing quiz:
- [ ] Questions test understanding, not just recall
- [ ] Mix of question types included
- [ ] All questions have clear correct answers
- [ ] Explanations provided for all answers
- [ ] Distractors are plausible
- [ ] References to notes included where applicable
- [ ] Saved to `/quiz/` directory

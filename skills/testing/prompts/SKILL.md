---
name: prompts
description: Please generate a new skill for creating multiple choice quizes.
---

# Generate Quiz Skill

Please generate a new skill for creating multiple choice quizes.
Use the Skill Creator skill here https://github.com/anthropics/skills/tree/main/skill-creator to create the quiz
generator skill and place it in /skills/quiz.  For the requirement use the file at
 /docs/skills/skill-generator.md. Make sure to specify that the question admonition is used in all questions.

 ## Summary

  I've successfully created the Quiz Generator Skill following the Anthropic Skill
  Creator guidelines with special attention to the mkdocs-material question admonition
   format. Here's what was delivered:

  ## 📁 Skill Structure

  /skills/quiz-generator/
  ├── SKILL.md                              ✅ Main skill file (required)
  ├── README.md                             ✅ User documentation
  └── references/
      └── distractor-writing-guide.md       ✅ Quality distractor guidance

  ## 📝 Key Components

  1. SKILL.md (Main Skill File)
  - ✅ Proper YAML frontmatter (name, description, license)
  - ✅ Written in imperative/infinitive form
  - ✅ 13-step workflow for quiz generation
  - ✅ SPECIAL: Question admonition format specification
  - ✅ Content readiness scoring (1-100 scale)
  - ✅ Bloom's Taxonomy distribution by chapter type
  - ✅ Quality distractor analysis
  - ✅ Answer balance enforcement
  - ✅ JSON export for LMS/chatbot integration

  2. Question Admonition Format (As Specified)

  The skill explicitly requires using the mkdocs-material question admonition format:

  #### 1. Question text in a full sentence with a question mark?

  <div class="upper-alpha" markdown>
  1. Answer 1 text
  2. Answer 2 text
  3. Answer 3 text
  4. Answer 4 text
  </div>

  ??? question "Show Answer"
      The correct answer is **X**. Detailed explanation of answer here.

      **Concept Tested:** [Concept Name]

      **See:** [Link to chapter section]

  3. References (Loaded as needed)
  - ✅ distractor-writing-guide.md - Comprehensive guide with:
    - The four qualities of effective distractors
    - Plausibility, educational value, discrimination, fairness
    - Common misconception patterns
    - Distractor construction techniques
    - Quality checklist and scoring
    - Examples by Bloom's level
    - Common mistakes to avoid

  4. Documentation
  - ✅ README.md - Complete overview with formatting examples, troubleshooting

  🎯 Skill Features

  Content Assessment:
  - Readiness scoring based on word count, examples, glossary coverage, concept
  clarity
  - User dialog triggers when content insufficient (<60)
  - Chapter type detection (introductory/intermediate/advanced)

  Question Generation:
  - 8-12 questions per chapter
  - Bloom's Taxonomy distribution tailored to chapter type
  - Question admonition format with upper-alpha styling
  - Quality distractor analysis (0.80+ target)

  Answer Quality:
  - Balanced distribution across A, B, C, D (25% each ±5%)
  - No predictable patterns
  - All questions have explanations (50-100 words)
  - Links to source chapter sections

  Outputs Generated:
  1. Quiz markdown file (separate or embedded)
  2. Quiz metadata JSON per chapter
  3. Quiz bank JSON (aggregate all questions)
  4. Quality report with recommendations
  5. Alternative questions bank (optional)

  Quality Scoring:
  - Question Quality (30 pts): Clear, unambiguous, well-formed
  - Bloom's Distribution (25 pts): Matches target for chapter type
  - Concept Coverage (20 pts): 75%+ major concepts tested
  - Answer Balance (15 pts): Even distribution across options
  - Pedagogical Value (10 pts): Explanations teach, not just confirm

  🚀 Usage

  Trigger phrases:
  - "Generate a quiz for Chapter 3"
  - "Create quiz questions for my chapter"
  - "Build a quiz from this content"

  The skill follows the specification from /docs/skills/quiz-generator.md and
  explicitly implements the question admonition format as required.

  📊 All Three Skills Complete!

  You now have three fully functional Claude Skills:

  1. ✅ Glossary Generator (/skills/glossary-generator)
    - ISO 11179-compliant definitions
    - Quality scoring and validation
  2. ✅ FAQ Generator (/skills/faq-generator)
    - Bloom's Taxonomy distribution
    - Chatbot JSON export
  3. ✅ Quiz Generator (/skills/quiz-generator)
    - Question admonition format ✨
    - Quality distractors
    - LMS-ready export

  All skills are ready to use and fully compliant with Anthropic Skill Creator
  standards! 🎉


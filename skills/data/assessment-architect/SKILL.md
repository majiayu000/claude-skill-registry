---
name: assessment-architect
description: Generate certification exams for chapters or parts. Extracts concepts first, then generates scenario-based questions. Use "ch X" for chapter, "part X" for part.
---

# Assessment Architect - Concept-First Certification Exams

Generate rigorous certification exams by extracting concepts FIRST, then building scenario-based questions from the concept map.

**Output:** DOCX in `assessments/` directory
**NOT for:** Practice quizzes (those use `*_quiz.md` in chapter directories)

---

## Operating Contract (Non-Negotiable)

These rules are structural and cannot be overridden:

1. **No memorization questions.** Every question requires a novel scenario paragraph before the stem. Questions testing recall of lesson-specific facts are rejected.
2. **Grounding notes before concepts.** Read lessons → write notes file → extract concepts FROM notes. Never extract concepts from memory. The notes file is evidence of engagement.
3. **Concepts before questions.** The concept map (built from notes) is the contract for Phase 2. Never generate questions by walking through lessons sequentially.
4. **Filesystem discovery only.** No hardcoded book structure. Use `ls -d` to find paths. The filesystem is the source of truth.
5. **Structural validation.** Anti-memorization (grep patterns) and anti-gaming (distribution bias) are FAIL conditions. Readability is a principle, not a word-count gate.
6. **Importance-weighted question count.** Core lessons get 3-5 questions, supporting get 1-2, intro get 0-1. No flat "2 per lesson" — weight by importance.
7. **TaskList for coordination.** Create tasks upfront. Update status at each phase. Subagents receive the TaskList ID.
8. **2 subagents maximum.** Each receives only the concept map + `references/question-types.md`. Not the full skill file.
9. **Persisted state.** Notes, concept map, and question files saved to `assessments/`. Validation results reported at each phase.

---

## Input Parsing (via $ARGUMENTS)

```
INPUT = $ARGUMENTS (e.g., "ch 5", "part 3", "ch 2, 3, 4", "ch 2-4")

PARSE:
  IF matches "ch N, N, N" | "chapter N, N and N" (comma/and-separated list):
    SCOPE = "multi-chapter"
    NUMS = extract all numbers → zero-pad each
    FOR each NUM: PATH[] += ls -d apps/learn-app/docs/*/$(printf '%02d' NUM)-*/

  ELSE IF matches "ch N-M" | "chapter N-M" (range):
    SCOPE = "multi-chapter"
    FOR NUM in N..M: PATH[] += ls -d apps/learn-app/docs/*/$(printf '%02d' NUM)-*/

  ELSE IF matches "ch N" | "chapter N" (single):
    SCOPE = "chapter"
    NUM = zero-pad N to 2 digits
    PATH = result of: ls -d apps/learn-app/docs/*/$(printf '%02d' N)-*/

  ELSE IF matches "part N" | "p N" | "pN":
    SCOPE = "part"
    NUM = zero-pad N to 2 digits
    PATH = result of: ls -d apps/learn-app/docs/$(printf '%02d' N)-*/

  ELSE IF bare number:
    AskUserQuestion: "Did you mean Chapter {N} or Part {N}?"

  ELSE IF empty:
    AskUserQuestion: "Which chapter or part? (e.g., 'ch 5' or 'part 3')"

VALIDATE:
  FOR each path: run ls -d. If no result: FAIL "Path not found"

DISCOVER LESSONS:
  FOR each PATH (single or multi):
    LESSONS += ls {PATH}/*.md | grep -v README | grep -v summary | grep -v quiz
  LESSON_COUNT = total across all paths

CONFIRM with user (AskUserQuestion):
  "Found {SCOPE}: {chapter names and numbers}
   Path(s): {paths}
   Total lessons: {LESSON_COUNT}
   Proceed?"
```

---

## Task Coordination

After confirming scope, create a TaskList to track progress and coordinate subagents:

```
TaskCreate: "Discover scope and confirm with user" → mark in_progress immediately
TaskCreate: "Explore curriculum context (Part/Chapter READMEs)" (blocked by task 1)  ← NEW
TaskCreate: "Calculate chapter importance weights" (blocked by task 2)  ← NEW
TaskCreate: "Read lessons and write grounding notes" (blocked by task 3)
TaskCreate: "Extract concept map from grounding notes" (blocked by task 4)
TaskCreate: "Calculate question distribution and confirm" (blocked by task 5)
TaskCreate: "Generate questions - Subagent A (Scenario + Transfer)" (blocked by task 6)
TaskCreate: "Generate questions - Subagent B (Relationship + Evaluation)" (blocked by task 6)
TaskCreate: "Validate all questions" (blocked by tasks 7, 8)
TaskCreate: "Assemble exam and generate DOCX" (blocked by task 9)
```

Update each task status as work progresses. Subagents receive the TaskList ID so they can update their own task status upon completion.

---

## Phase 0: Curriculum Context Discovery (MANDATORY - NEW)

**CRITICAL: This phase must complete BEFORE reading individual lessons.**

The skill previously failed by calculating question distribution from lesson counts alone. A chapter with 12 "Markdown syntax" lessons shouldn't get equal weight to a chapter with 12 "Core Agent Architecture" lessons.

### Step 1: Read Part README

```bash
# For part scope: read the part's README directly
cat {PART_PATH}/README.md

# For chapter scope: find and read the parent part's README
PART_PATH=$(dirname {CHAPTER_PATH})
cat ${PART_PATH}/README.md
```

**Extract from Part README:**
- Book/Part learning objectives (the "What You'll Learn" section)
- Chapter descriptions and their stated roles
- The overall goal/thesis of this part

### Step 2: Classify Each Chapter by Role

For each chapter in scope, determine its role in the curriculum:

```
CHAPTER_ROLE classification:

  "core-practical"  → Teaches the PRIMARY skills of this part
                      Signals: "You'll master...", hands-on tool usage,
                      the largest chapter, most learning objectives point here
                      Weight: HIGH (30-40% of questions if single chapter dominates)

  "core-conceptual" → Teaches foundational concepts that enable practical skills
                      Signals: principles, frameworks, mental models,
                      "understand WHY" language, synthesis chapters
                      Weight: HIGH (20-30%)

  "supporting"      → Provides necessary context or secondary skills
                      Signals: "before you can...", setup, configuration,
                      enabling skills, smaller learning objective footprint
                      Weight: MEDIUM (10-20%)

  "prerequisite"    → Teaches format/syntax/basics assumed by other chapters
                      Signals: Markdown syntax, installation, environment setup,
                      not mentioned in part learning objectives
                      Weight: LOW (2-5% or exclude entirely)
```

### Step 3: Calculate Chapter Importance Weights

**Formula: Weight by role AND learning objective coverage**

```
FOR each chapter:
  role_weight = {
    "core-practical": 35,
    "core-conceptual": 25,
    "supporting": 15,
    "prerequisite": 3
  }[chapter_role]

  # Adjust by learning objective coverage
  objectives_mentioning_chapter = count of Part learning objectives
    that specifically reference this chapter's topics
  objective_boost = objectives_mentioning_chapter * 5

  raw_weight = role_weight + objective_boost

NORMALIZE weights to sum to 100%

OUTPUT: chapter_weights = { ch1: X%, ch2: Y%, ... }
```

### Step 4: Report and Confirm

Present to user BEFORE reading lessons:

```
## Curriculum Analysis

**Part Goal:** {thesis from README}

| Chapter | Lessons | Role | Weight | Rationale |
|---------|---------|------|--------|-----------|
| Ch 3: General Agents | 52 | core-practical | 35% | Primary hands-on chapter |
| Ch 6: Seven Principles | 20 | core-conceptual | 20% | Synthesis chapter |
| Ch 4: Context Engineering | 22 | core-conceptual | 20% | Quality discipline |
| Ch 1: Agent Factory | 22 | supporting | 15% | Foundational concepts |
| Ch 5: SDD | 10 | supporting | 8% | Methodology |
| Ch 2: Markdown | 12 | prerequisite | 2% | Format only |

**Proposed question distribution (150 total):**
- Ch 3: 52 questions
- Ch 6: 30 questions
- Ch 4: 30 questions
- Ch 1: 23 questions
- Ch 5: 12 questions
- Ch 2: 3 questions

Proceed with this weighting?
```

User can adjust weights before lesson reading begins.

### Why This Matters

| Without Phase 0 | With Phase 0 |
|-----------------|--------------|
| Ch 2 (Markdown) gets 12 lessons × 2 = 24 questions | Ch 2 gets 2% = 3 questions |
| Lesson count drives distribution | Book goals drive distribution |
| Supporting chapters over-weighted | Core chapters properly prioritized |
| Prerequisite skills tested heavily | Prerequisites minimally tested |

---

## Grounding Notes (MANDATORY)

As you read each lesson, write observations to `assessments/{SLUG}-notes.md`. This file is your working memory and evidence of genuine engagement with the content.

**Format (append per lesson):**
```markdown
## Lesson: {filename}

**Weight:** {core | supporting | intro}
**Key concepts:** {2-5 concepts worth testing}
**Relationships to other lessons:** {what connects to what}
**Testable trade-offs:** {decisions or comparisons in this lesson}
**Transfer potential:** {where else this principle applies}
**Surprise/insight:** {anything non-obvious that would make a good question}
```

**Rules:**
- Write notes DURING reading, not after all lessons are read
- This file is the RAW INPUT for concept extraction (Phase 1 reads notes, not memory)
- The concept map MUST cite specific notes entries as evidence
- If a concept in the map has no corresponding note: it's fabricated, remove it

---

## 4 Question Types (Adaptive Distribution)

All questions require a concise scenario before the stem. No fact-recall patterns allowed.

| Type | Bloom Level | Key Constraint |
|------|-------------|----------------|
| **Scenario Analysis** | Apply/Analyze | Novel situation not appearing in lessons |
| **Concept Relationship** | Analyze/Evaluate | Tests CONNECTION between 2+ concepts |
| **Transfer Application** | Apply/Create | Apply principle to a domain NOT in the chapter |
| **Critical Evaluation** | Evaluate | Identify WHY an approach fails in context |

**Distribution adapts to chapter type** (classified in Phase 0.5):

```
PRACTICAL-TOOL chapters (e.g., Claude Code CLI, Docker, FastAPI):
  Scenario Analysis:     60%  (realistic usage scenarios in the tool's domain)
  Concept Relationship:  20%  (how tool components interact)
  Transfer Application:   5%  (minimal — stay in the tool's domain)
  Critical Evaluation:   15%  (identify why an approach fails with this tool)

CONCEPTUAL chapters (e.g., Seven Principles, Architecture Patterns):
  Scenario Analysis:     35%  (apply principle to realistic situations)
  Concept Relationship:  25%  (how principles connect and interact)
  Transfer Application:  25%  (appropriate — abstract principles transfer broadly)
  Critical Evaluation:   15%  (evaluate when a principle is misapplied)

HYBRID chapters:
  Interpolate between practical-tool and conceptual based on lesson mix.
  Count practical vs conceptual lessons, weight accordingly.
  Example: 60% practical lessons → use 80% of practical distribution + 20% of conceptual.
```

**Rationale:** Practical-tool chapters should test whether students can USE the tool in realistic scenarios, not transfer principles to unrelated domains. Conceptual chapters should test whether students can apply principles broadly.

For detailed patterns and examples, see `references/question-types.md`.

### Readability Principle

**The difficulty is in the THINKING, not the READING.**

Write at professional-clear level. One idea per sentence. Active voice. No filler. The agent has full autonomy over word counts — the principle is clarity, not a specific number.

**WRONG (bloated — agent should never produce this):**
```
Q. A veteran meteorologist notices that her department's new AI weather
prediction system presents 48-hour forecasts with identical confidence
formatting regardless of actual prediction reliability. A tropical storm
forecast with high uncertainty appears identically to a clear-sky prediction
with strong model consensus. Junior forecasters have stopped adding uncertainty
qualifiers to public advisories, trusting the AI's confident presentation.

Applying the principle that confidence is uncorrelated with accuracy in AI
systems, which practice would most improve the department's forecast
communication reliability?

**A.** Requiring independent verification of AI forecasts against ensemble models
before accepting any prediction, regardless of how confidently it is presented
```

**RIGHT (clear, same concept tested):**
```
Q. A weather AI displays all forecasts with equal confidence — a risky
tropical storm prediction looks identical to a reliable clear-sky forecast.
Junior staff stopped questioning AI outputs.

How should the team handle AI outputs that show no uncertainty signal?

**A.** Verify all AI forecasts against independent sources before publishing
```

Same concept. Same difficulty. The right version is just clearer because it has no filler.

---

## Dynamic Question Count (Two-Level Weighting)

Question distribution uses TWO levels of weighting:

1. **Chapter-level weights** (from Phase 0 curriculum analysis)
2. **Lesson-level weights** (within each chapter)

### Level 1: Chapter Weights (from Phase 0)

Chapter weights are determined by curriculum analysis BEFORE reading lessons:
- Role in book goals (core-practical, core-conceptual, supporting, prerequisite)
- Learning objective coverage
- User confirmation

These weights determine what PERCENTAGE of total questions each chapter receives.

### Level 2: Lesson Weights (within chapters)

**During Phase 0.5 (reading lessons), tag each lesson:**

```
LESSON_WEIGHT:
  "core"       → Teaches a key capability or central concept (3-5 questions)
                 Signals: new tools, complex workflows, architectural patterns, capstone integration
  "supporting" → Provides context, setup, or secondary skills (1-2 questions)
                 Signals: configuration, secondary features, examples of core concepts
  "intro"      → Opening, overview, or minimal-content lesson (0-1 questions)
                 Signals: motivational content, history, "what you'll learn", installation-only
```

### Calculating Total Question Count

```
tier_multiplier:
  T1 (Introductory) = 0.7
  T2 (Intermediate) = 1.0  [default]
  T3 (Advanced)     = 1.3

total_lessons = sum of lessons across all chapters
concept_count = total concepts extracted

base = max(ceil(concept_count * 0.8), total_lessons * 1.5)
raw = base * tier_multiplier
TOTAL = clamp(round_to_nearest_5(raw), min=30, max=150)
```

### Allocating Questions to Chapters

**Apply Phase 0 chapter weights:**

```
FOR each chapter:
  chapter_questions = round(TOTAL * chapter_weight_percent)

VALIDATE: sum of chapter_questions == TOTAL (adjust rounding as needed)
```

### Allocating Questions Within Chapters

**Apply lesson weights within each chapter's allocation:**

```
FOR each chapter:
  weighted_sum = sum of lesson weights (core=5, supporting=2, intro=1)

  FOR each lesson in chapter:
    lesson_proportion = lesson_weight / weighted_sum
    lesson_questions = round(chapter_questions * lesson_proportion)
```

### Example: Part with 6 Chapters

```
Phase 0 determined chapter weights:
  Ch 3: 35% (core-practical, 52 lessons)
  Ch 4: 20% (core-conceptual, 22 lessons)
  Ch 6: 20% (core-conceptual, 20 lessons)
  Ch 1: 15% (supporting, 22 lessons)
  Ch 5: 8%  (supporting, 10 lessons)
  Ch 2: 2%  (prerequisite, 12 lessons)

Total = 150 questions (T2)

Chapter allocation:
  Ch 3: 150 * 0.35 = 52 questions
  Ch 4: 150 * 0.20 = 30 questions
  Ch 6: 150 * 0.20 = 30 questions
  Ch 1: 150 * 0.15 = 23 questions
  Ch 5: 150 * 0.08 = 12 questions
  Ch 2: 150 * 0.02 = 3 questions

Within Ch 2 (3 questions for 12 lessons):
  - 2 core lessons get 1 question each
  - 10 intro/supporting lessons get 0-1 questions
  - Total: 3 questions (matches chapter allocation)
```

Present recommendation to user with BOTH chapter-level AND lesson-level breakdown. User can override at either level.

---

## 5-Phase Workflow

**Phase 0** → Curriculum Context Discovery (understand book goals)
**Phase 0.5** → Read Lessons & Write Grounding Notes
**Phase 1** → Concept Extraction
**Phase 2** → Question Generation (2 parallel subagents)
**Phase 3** → Validation
**Phase 4** → Assembly & DOCX Output

---

### Phase 0.5: Read Lessons, Classify Chapter & Write Grounding Notes (this agent)

**Prerequisite: Phase 0 chapter weights must be confirmed before this phase.**

Read ALL lessons in scope. As you read each one, APPEND observations to `assessments/{SLUG}-notes.md` (see Grounding Notes section above).

This is not optional. The notes file is the evidence that you actually engaged with the content. Phase 1 builds the concept map FROM the notes file, not from memory.

**After reading all lessons, classify the chapter type:**

```
CHAPTER_TYPE classification (determine from lesson content):

  "practical-tool"  → Chapter teaches how to USE a specific tool
                      Signals: CLI commands, installation steps, configuration files,
                      code blocks with tool invocations, "run this command" patterns
                      Examples: Claude Code CLI, Docker, FastAPI, Kubernetes

  "conceptual"      → Chapter teaches principles, patterns, architecture
                      Signals: "when to use", "why", trade-off discussions,
                      design patterns, decision frameworks, no specific tool commands
                      Examples: Seven Principles, General Agent Architecture, Design Patterns

  "hybrid"          → Mix of tool-usage and principle lessons
                      Signals: some lessons are hands-on tool usage,
                      others are conceptual/architectural
                      Examples: MCP (concept + implementation), Agent Skills (concept + creation)
```

**Extract domain keywords** from lesson content (the specific tools, technologies, and workflows the chapter teaches). These keywords constrain scenario generation in Phase 2.

Write classification and keywords to the top of the notes file:
```markdown
# Chapter Classification
- Type: {practical-tool | conceptual | hybrid}
- Domain keywords: {comma-separated list of specific terms from the chapter}
- Example domains for scenarios: {2-3 example settings appropriate for this chapter}
```

Update task status: mark "Read lessons and write grounding notes" as in_progress, then completed.

---

### Phase 1: Concept Extraction (this agent)

Read `assessments/{SLUG}-notes.md` (your grounding notes). Extract concepts from the notes, not from memory.

**What to extract** (see `references/concept-extraction-guide.md` for details):
- Core concepts (named ideas, patterns, principles)
- Relationships (concept A enables/conflicts/extends concept B)
- Trade-offs (choosing X means sacrificing Y)
- Transfer domains (where else could this principle apply?)

**Every concept MUST cite a grounding note entry.** If you can't point to a specific note, the concept is fabricated.

**Output:** Write to `assessments/{SLUG}-concepts.md`

Format:
```markdown
# Concept Map: {Chapter/Part Name}

## Concepts (N total)

### 1. {Concept Name}
- Definition: {1-2 sentences}
- Lessons: {which lessons cover this}
- Relationships: {connects to concepts X, Y}
- Transfer domains: {healthcare, finance, education, etc.}

### 2. {Concept Name}
...

## Relationships
- {Concept A} --enables--> {Concept B}
- {Concept C} --conflicts-with--> {Concept D}
...

## Trade-offs
- {Choosing X} vs {Choosing Y}: {what you sacrifice}
...
```

After extraction:
1. Report lesson weight breakdown (core/supporting/intro counts)
2. Report concept count and recommend question count (importance-weighted algorithm above)
3. Report the adaptive type distribution for the detected chapter type
4. Ask user to confirm or override question count
5. Ask user for difficulty tier (T1/T2/T3, default T2)

---

### Phase 2: Question Generation (2 parallel Task subagents)

Spawn 2 Task subagents. Each receives ONLY:
- The concept map (`assessments/{SLUG}-concepts.md`)
- Question type reference (`references/question-types.md`)
- Chapter type and domain keywords (from notes file classification)
- Their assigned types and count

See `references/subagent-template.md` for prompt templates.

**Subagent A:** Scenario Analysis + Transfer Application questions
- Output: `assessments/{SLUG}-questions-A.md`
- Count: (Scenario% + Transfer%) of total — varies by chapter type:
  - Practical-tool: 65% of total (60% Scenario + 5% Transfer)
  - Conceptual: 60% of total (35% Scenario + 25% Transfer)
  - Hybrid: interpolate

**Subagent B:** Concept Relationship + Critical Evaluation questions
- Output: `assessments/{SLUG}-questions-B.md`
- Count: (Relationship% + Evaluation%) of total — varies by chapter type:
  - Practical-tool: 35% of total (20% Relationship + 15% Evaluation)
  - Conceptual: 40% of total (25% Relationship + 15% Evaluation)
  - Hybrid: interpolate

---

### Phase 3: Validation (this agent)

Read both question files. Apply ALL structural checks:

**FAIL conditions (reject question, non-negotiable):**
```
FAIL if question contains "According to"
FAIL if question contains "Lesson [0-9]" or "lesson [0-9]"
FAIL if question contains "the document states" or "as discussed in"
FAIL if question has NO scenario paragraph before the stem
FAIL if Transfer Application domain appears anywhere in chapter content
FAIL if question doesn't map to a concept in the concept map
```

**Anti-gaming checks (FAIL conditions):**
```
# Length Bias (see references/bias-detection-guide.md)
FAIL if correct answer is longest option in >40% of questions (length bias)
FAIL if correct answer is shortest option in >40% of questions (length bias)

# Position Bias
FAIL if any letter is correct >30% or <20% of total
FAIL if middle (B+C) > 55% of correct answers
FAIL if outer (A+D) < 40% of correct answers
FAIL if >3 consecutive questions have same correct letter

# Specificity Bias (see references/bias-detection-guide.md)
WARN if correct answer specificity score > 30% higher than distractor average
FLAG questions where correct option has examples/qualifiers that distractors lack
```

**Distribution checks:**
```
Count answer distribution across all questions:
  Each of A/B/C/D must be 20-30% of total
  No >3 consecutive same-letter answers
  Option lengths: correct answer word count within ±3 words of distractor average
```

**Coverage check:**
```
Each concept in the map should have at least 1 question
  Flag uncovered concepts (warning, not failure)
  Report: "X of Y concepts covered (Z%)"
```

If validation fails:
- Report specific failures with question numbers
- Identify pattern (e.g., "Subagent A produced 12 questions with 'According to'")
- Regenerate only the failing subagent's output (re-spawn that subagent)

See `references/validation-rules.md` for complete validation pipeline.

---

### Phase 4: Assembly & DOCX Output (this agent)

**Step 1: Merge and STRIP internal tags**
- Interleave questions from both files (don't group by type)
- Renumber sequentially Q1 through Q{TOTAL}
- Randomize answer positions (ensure distribution holds)
- **STRIP all internal tags from student-facing questions:**
  ```
  REMOVE: [Scenario Analysis], [Concept Relationship], [Transfer Application], [Critical Evaluation]
  REMOVE: [Concept: {anything}]
  REMOVE: **Answer:** lines (answers go ONLY in answer key)
  REMOVE: **Reasoning:** sections (go ONLY in educator supplement)
  ```
- **Validation after stripping:**
  ```
  grep -E "\[(Scenario|Concept|Transfer|Critical)" assessments/{SLUG}-exam.md
  → MUST return 0 matches in the questions section
  ```

**Step 2: Build exam document (TWO separate files)**

**File 1: Student exam** (`assessments/{SLUG}-exam.md`)
```markdown
# {Chapter/Part Name} Certification Assessment

**Questions:** {TOTAL}
**Time Limit:** {ceil(TOTAL * 1.5)} minutes
**Passing Score:** 75%

**Instructions:** Select the best answer for each question.

---

Q1. {scenario paragraph}

{stem ending in ?}

**A.** {option}

**B.** {option}

**C.** {option}

**D.** {option}

---

Q2. ...
```

NO type labels. NO concept tags. NO answers. NO explanations. Just questions.

**File 2: Educator key** (`assessments/{SLUG}-answer-key.md`)
```markdown
# Answer Key: {Chapter/Part Name}

| Q | Answer | Type | Concept |
|---|--------|------|---------|
| 1 | B | Scenario Analysis | {concept name} |
| 2 | D | Concept Relationship | {concept name} |
...

## Answer Distribution
A: {count} ({%}) | B: {count} ({%}) | C: {count} ({%}) | D: {count} ({%})

## Concept Coverage
{List concepts and question count per concept}

## Type Distribution
{Scenario Analysis: X | Concept Relationship: X | Transfer Application: X | Critical Evaluation: X}
```

**CRITICAL: Option format must be `**A.** text` (bold letter, period, space).**
Never use `A)` — pandoc interprets it as an ordered list marker and renders bullet points in DOCX.

**Step 3: Convert to DOCX (two files)**

**Option A: pandoc (simple)**
```bash
pandoc assessments/{SLUG}-exam.md -o assessments/{SLUG}-Assessment-Final.docx --from=markdown --to=docx
pandoc assessments/{SLUG}-answer-key.md -o assessments/{SLUG}-Answer-Key.docx --from=markdown --to=docx
```

**Option B: Programmatic with docx-js (better formatting control)**

When using the docx-js library for professional DOCX output:

```javascript
// CRITICAL: Paragraph alignment
// Custom paragraph styles may NOT reliably apply alignment.
// ALWAYS set alignment EXPLICITLY on each Paragraph.

// ❌ WRONG - style-based alignment may be ignored:
new Paragraph({
  style: "Question",  // Even if Question style has LEFT alignment
  children: [new TextRun({ text: question.stem })]
})

// ✅ CORRECT - explicit alignment on each paragraph:
new Paragraph({
  alignment: AlignmentType.LEFT,  // ALWAYS set this explicitly
  spacing: { before: 200, after: 100 },
  children: [
    new TextRun({ text: `${qNum}. `, bold: true, size: 24, font: "Arial" }),
    new TextRun({ text: question.stem, font: "Arial", size: 22 })
  ]
})

// ✅ CORRECT - options with explicit alignment and indent:
new Paragraph({
  alignment: AlignmentType.LEFT,  // ALWAYS set this explicitly
  indent: { left: 360 },
  spacing: { after: 60 },
  children: [new TextRun({ text: `${letter}) ${option}`, font: "Arial", size: 22 })]
})
```

**Key docx-js rules:**
1. Always set `alignment: AlignmentType.LEFT` explicitly on every question/answer paragraph
2. Don't rely on custom paragraph styles for alignment
3. Set `font: "Arial"` on every TextRun for consistent rendering
4. Use `indent: { left: 360 }` for option indentation (not tabs or spaces)

**Step 4: Post-conversion validation**
- Verify both DOCX files exist and exam > 10KB
- **CRITICAL:** grep the exam markdown for internal tags:
  ```
  grep -cE "\[(Scenario|Concept|Transfer|Critical)" assessments/{SLUG}-exam.md
  → MUST be 0. If not: FAIL "Internal tags leaked into student exam"
  ```
- Verify NO "Answer:" or "Reasoning:" text in exam DOCX
- Report: file paths, question count, concept coverage percentage

**Step 5: Cleanup** (optional)
- Keep concept map (useful reference)
- Keep question files (for regeneration)
- Delete intermediate markdown if user prefers clean output

---

## Failure Modes (Summary)

| Failure | Prevention | Detection |
|---------|-----------|-----------|
| **Curriculum context skipped** | **Phase 0 MANDATORY** | Part README not read before lesson reading |
| **Prerequisite chapters over-weighted** | Chapter role classification | "prerequisite" chapters should get 2-5%, not equal weight |
| **Lesson count = question count** | Two-level weighting (chapter + lesson) | Distribution ignores book learning objectives |
| Memorization questions | Structural FAIL conditions | grep for "According to", "Lesson [0-9]" |
| **Length bias (longest correct)** | Anti-gaming FAIL: >40% longest correct | Word count rank per question |
| **Position bias (B/C clustering)** | Anti-gaming FAIL: middle >55% | Count B+C vs A+D distribution |
| **Specificity bias** | WARN: correct >30% more specific | Score options with examples/qualifiers |
| Answer bias (74% A) | Anti-gaming FAIL: any letter >30% | Count distribution per letter |
| Fabricated concepts | Grounding notes required | Every concept must cite a notes entry |
| Too few questions | Importance-weighted: core=3-5, supporting=1-2, intro=0-1 | Weighted sum drives minimum, not flat count |
| Wrong chapter/part | `ls -d` filesystem discovery | Path validation before proceeding |
| Missing lessons | Complete lesson count + notes file | Notes file has entry per lesson |
| No coordination | TaskList created upfront | Task status visible across phases |
| Context overload | Subagents receive only concept map + types | ~300 lines context vs 937+176KB |
| Internal tags in exam | Strip [Type] and [Concept:] in Phase 4 | grep for brackets in exam.md = 0 |
| Answers in student file | Two separate files (exam + key) | No "Answer:" in exam DOCX |
| Bullet points in DOCX | Use `**A.**` format, never `A)` | pandoc treats `A)` as list marker |

For historical context on these failures, see the Jan 2026 postmortem in the skill's git history.

---

## Reference Files

| File | Purpose | Used By |
|------|---------|---------|
| `references/question-types.md` | 4 type definitions with examples | Subagents (Phase 2) |
| `references/concept-extraction-guide.md` | How to extract concepts vs facts | This agent (Phase 1) |
| `references/subagent-template.md` | Prompt templates for 2 subagents | This agent (Phase 2 spawning) |
| `references/validation-rules.md` | Anti-memorization + distribution checks | This agent (Phase 3) |
| `references/bias-detection-guide.md` | Length/position/specificity bias detection | This agent (Phase 3) |
| `references/bloom-taxonomy.md` | Cognitive level reference | Subagents (question design) |
| `references/psychometric-standards.md` | DIF/DIS/DF metrics | This agent (Phase 3 validation) |
| `references/distractor-generation-strategies.md` | Distractor design patterns | Subagents (option creation) |
| `references/academic-rigor-tiers.md` | T1-T3 difficulty frameworks | This agent (Phase 1 tier selection) |

---

## Observability (Principle 7)

Report at each phase transition:

```
Phase 0 Complete (Curriculum Context):
  - Part/Book goal: {thesis statement}
  - Chapters in scope: {N}
  - Chapter weights:
    | Chapter | Role | Weight | Questions |
    | Ch 3 | core-practical | 35% | 52 |
    | Ch 6 | core-conceptual | 20% | 30 |
    ...
  - User confirmed: {yes/adjusted to X}

Phase 0.5 Complete:
  - Chapter type: {practical-tool | conceptual | hybrid}
  - Domain keywords: {keywords}
  - Lessons: {N} total ({N} core, {N} supporting, {N} intro)
  - Notes: assessments/{SLUG}-notes.md

Phase 1 Complete:
  - Concepts extracted: {N}
  - Relationships found: {N}
  - Trade-offs identified: {N}
  - Weighted question count: {N} (T{tier})
  - Type distribution: Scenario={N}% Relationship={N}% Transfer={N}% Evaluation={N}%
  - Concept map: assessments/{SLUG}-concepts.md

Phase 2 Complete:
  - Subagent A: {N} questions generated ({types})
  - Subagent B: {N} questions generated ({types})
  - Total: {N} questions

Phase 3 Complete:
  - Validation: {PASS/FAIL}
  - Failed questions: {N} (reasons: ...)
  - Answer distribution: A={N} B={N} C={N} D={N}
  - Concept coverage: {X}/{Y} ({Z}%)

Phase 4 Complete:
  - DOCX: assessments/{SLUG}-Assessment-Final.docx
  - Size: {N}KB
  - Questions: {N}
  - Ready for distribution
```

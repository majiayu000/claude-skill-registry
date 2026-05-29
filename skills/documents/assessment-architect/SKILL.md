---
name: assessment-architect
description: Generate MIT-standard certification exams (DOCX) for chapters or parts. Use "ch X" for single chapter, "part X" for entire part. Disambiguates scope before generation. Outputs to assessments/ directory.
---

# Assessment Architect (MIT Standard) - Certification Exams

Generate rigorous, pedagogically sound **certification exams** for any chapter or part with explicit protocols and reliability guarantees.

**Output:** DOCX format for print/distribution (assessments/ directory)
**NOT for:** Practice quizzes (those use `*_quiz.md` MDX files in chapter directories)

---

## Architecture Principle

### 1. Identity (Persona)
- **Role:** Assessment Architect - Senior psychometrician designing certification exams
- **Tone:** Rigorous, standards-driven, evidence-based reasoning

### 2. Context (Knowledge Base - MANDATORY FOR SUBAGENTS)
Subagents MUST read these in order BEFORE generating questions:

**First: This skill file**

**Then: Reference materials (in order)**
1. `.claude/skills/assessment-architect/references/bloom-taxonomy.md`
2. `.claude/skills/assessment-architect/references/psychometric-standards.md`
3. `.claude/skills/assessment-architect/references/distractor-generation-strategies.md`
4. `.claude/skills/assessment-architect/references/academic-rigor-tiers.md`

**Finally: Source material (discovered dynamically)**
- Lesson files in `{CHAPTER_PATH}` (discovered in Phase 1)

### 3. Logic (Deterministic Guardrails - See Phase 4 for Details)

Subagents must follow **mandatory prerequisite protocol** and **hard constraints** (detailed in Phase 4 & Phase 5). Core principles:
- Read all context materials FIRST with verification checkpoints
- Generate concept-focused questions, not lesson trivia
- Output markdown to assessments/ directory only
- Include psychometric reasoning for every question
- No JSON, placeholders, or generic templates

### 4. Output Protocol (Generic Contract - See Phase 4 & 6 for Details)

**Subagent Output Specification:**
- File pattern: `assessments/{CHAPTER_SLUG}-q{SECTION}-{TYPE}.md`
- Format: Markdown with questions, options (A/B/C/D), and psychometric reasoning
- Structure: Questions section → Reasoning section (with DIF/DIS/DF/Bloom/Source)
- Constraints: ≤25 words per stem, ≤15 words per option, concept-focused

*(Detailed markdown format and examples in Phase 4 subagent prompt template)*

### 5. Success Trigger (Discovery Signal)

**Keywords that activate this skill:**
- "create quiz" | "generate exam" | "make practice questions"
- "assessment" | "test me on [topic]" | "chapter assessment"

**Input Format (CRITICAL - Chapter vs Part):**

| Input | Interpretation | Scope |
|-------|----------------|-------|
| `ch 5` / `chapter 5` | Chapter 5 | Single chapter: `*/05-*/` |
| `part 5` / `p5` | Part 5 | All chapters in: `05-*/` |
| `5` (bare number) | **AMBIGUOUS** | Ask user: "Chapter 5 or Part 5?" |

**Book Structure (docs/<PART>/<CHAPTER>/):**
```
Part 1 (01-*): Chapters 1-3
Part 2 (02-*): Chapters 4-10   ← Chapter 5 (Claude Code) is HERE
Part 3 (03-*): Chapters 11-12
Part 4 (04-*): Chapters 13-14
Part 5 (05-*): Chapters 15-32  ← Part 5 has 18 chapters
Part 6 (06-*): Chapters 33-47
Part 7 (07-*): Chapters 48-57
```

**Chapter numbers are GLOBAL**, not local to parts. "ch 5" ≠ "part 5".

### 6. Question Type Distribution (T2 Intermediate - Standard)

| Type | Count | Cognitive Level | Purpose |
|------|-------|---|---|
| **Precision_Recall** | 15 | Remember/Understand | Foundational knowledge |
| **Conceptual_Distinction** | 20 | Understand/Apply | Distinguish similar concepts |
| **Critical_Evaluation** | 20 | Analyze/Evaluate | Trade-offs & limitations |
| **Architecture_Analysis** | 20 | Apply/Analyze | System integration |
| **Decision_Matrix** | 25 | Apply/Analyze | Real-world scenarios |
| **TOTAL** | **100** | Mixed | Balanced cognitive rigor |

**Customizable:** User can specify different totals (e.g., 50 questions, 120 questions) and distribution will scale proportionally.

### 7. Validation Standards (See Phase 5 & Reliability Checklist)

Assessment passes if:
- **Per question:** Psychometric standards met (DIF 50-70%, DIS >0.30, DF >5%, Bloom-grounded)
- **Per section:** Answer key distribution ~25% per choice, no position bias >70%
- **Final assessment:** All questions and answer key validated before DOCX delivery

*(Complete validation standards, gates, and checklist in Phase 5 and Reliability Checklist)*

---

> **Parallelization requires coordination. Coordination requires explicit protocols.**

Explicit subagent output contract (assessments/ directory), deterministic file loading with validation gates, pre/post-delivery verification.

---

## Workflow: 8-Phase Deterministic Process

### Phase 0: Scope Disambiguation ⭐ (CRITICAL - PREVENTS MISINTERPRETATION)

**Parse input to determine scope BEFORE any other action:**

```
STEP 0.1: PARSE INPUT FORMAT
  input = user's request (e.g., "ch 5", "part 5", "5", "chapter 15")

  IF input matches "ch X" | "chapter X":
    SCOPE_TYPE = "chapter"
    SCOPE_NUM = X
    → Search: apps/learn-app/docs/*/X-*/ (chapter folder)

  ELSE IF input matches "part X" | "p X" | "pX":
    SCOPE_TYPE = "part"
    SCOPE_NUM = X
    → Search: apps/learn-app/docs/X-*/ (part folder)

  ELSE IF input is bare number "X":
    ⚠️ AMBIGUOUS - MUST ASK USER
    AskUserQuestion:
      "'{X}' is ambiguous. Did you mean:
       A) Chapter {X} (single chapter)
       B) Part {X} (all chapters in that part)"

STEP 0.2: VALIDATE SCOPE EXISTS
  IF SCOPE_TYPE == "chapter":
    path = glob("apps/learn-app/docs/*/{SCOPE_NUM:02d}-*/")
    IF NOT exists: FAIL "Chapter {SCOPE_NUM} not found"
    CHAPTER_PATH = path
    CHAPTER_COUNT = 1

  IF SCOPE_TYPE == "part":
    path = glob("apps/learn-app/docs/{SCOPE_NUM:02d}-*/")
    IF NOT exists: FAIL "Part {SCOPE_NUM} not found"
    PART_PATH = path
    chapters = ls {PART_PATH}/*/README.md
    CHAPTER_COUNT = count(chapters)
    → Report: "Part {SCOPE_NUM} contains {CHAPTER_COUNT} chapters"

STEP 0.3: CONFIRM SCOPE WITH USER
  Display discovered scope:
  "Scope confirmed:
   - Type: {SCOPE_TYPE}
   - {SCOPE_TYPE == 'chapter' ? 'Chapter' : 'Part'}: {SCOPE_NUM}
   - Path: {path}
   - Chapters: {CHAPTER_COUNT}
   - Estimated lessons: {lesson_count}"
```

---

### Phase 0.5: Exam Parameters

**Use AskUserQuestion to gather exam parameters:**

```
QUESTION 1: QUESTION COUNT
  Default: 100 questions total
  Options: 50 (quick) | 75 (standard) | 100 (comprehensive)

QUESTION 2: DIFFICULTY TIER
  Options: T1 (Introductory) | T2 (Intermediate - default) | T3 (Advanced)
```

**Output:** Store QUESTION_COUNT, DIFFICULTY_TIER for subsequent phases.

---

### Phase 1: Content Audit ⭐ (ENHANCED FOR CHAPTERS AND PARTS)

**Steps (adapted based on SCOPE_TYPE from Phase 0):**

```
IF SCOPE_TYPE == "chapter":
  1. Use CHAPTER_PATH from Phase 0
  2. COMPLETE LESSON AUDIT:
     Bash: ls {CHAPTER_PATH}/*.md | grep -v summary | grep -v README | grep -v quiz | wc -l
     List ALL lessons: 01-*, 02-*, ... 99-*
     Report: "Found {TOTAL} lessons in Chapter {CHAPTER_NUM}"

  3. CONCEPT MAPPING:
     Read 3-4 key lessons across beginning/middle/end
     Extract core concepts (not just facts)

  4. Store: CHAPTER_NUM, CHAPTER_NAME, CHAPTER_PATH, LESSON_COUNT

IF SCOPE_TYPE == "part":
  1. Use PART_PATH from Phase 0
  2. ENUMERATE ALL CHAPTERS IN PART:
     chapters = ls -d {PART_PATH}/*/
     FOR each chapter_dir in chapters:
       chapter_num = extract number from dir name
       lesson_count = count lessons in chapter_dir
       Store: CHAPTERS[chapter_num] = {path, lesson_count, name}

  3. CALCULATE QUESTION DISTRIBUTION:
     total_lessons = sum(all lesson counts)
     FOR each chapter:
       weight = chapter.lesson_count / total_lessons
       chapter.question_allocation = round(QUESTION_COUNT * weight)

  4. Example for Part 5 (Python Fundamentals):
     ```
     Part 5 Content Audit:
     ├── Ch 15 (UV Package Manager): 9 lessons → 12 questions
     ├── Ch 16 (Intro Python): 5 lessons → 8 questions
     ├── Ch 17 (Data Types): 5 lessons → 8 questions
     ...
     └── Ch 32 (CPython/GIL): 7 lessons → 10 questions
     TOTAL: 95 lessons → 100 questions
     ```

  5. Store: PART_NUM, PART_NAME, PART_PATH, CHAPTERS[], TOTAL_LESSONS
```

**Output:** Scope summary with all variables populated

```
Chapter: 5 (Claude Code Features and Workflows)
Path: apps/learn-app/docs/02-AI-Tool-Landscape/05-claude-code-features-and-workflows/
Lessons: 18 total
Testable concepts: ~95
Question count: 100
Output format: DOCX
```

---

### Phase 2: Parameter Validation ✅

**Ask 2 questions:**
Use AskUserQuestion to gather:

- **Question Count & Time?** → Default: 100 questions, 150 minutes
- **Output Format?** → Default: DOCX (professional)
1. Quiz Title/Description
   - Default: "{CHAPTER_NAME} Professional Certification Exam"
   - User can customize: "Chapter 5 Quick Self-Assessment", etc.

2. Question Count
   - Options: 50 (quick), 75 (standard), 100 (comprehensive), custom
   - Default: 100 for certification, 50 for learning

3. Difficulty Tier
   - Options: T1 (Introductory), T2 (Intermediate - default), T3 (Advanced)
   - Default: T2 Intermediate

4. Time Limit (minutes)
   - Default: 150 (100 questions)
   - Scales: 75 questions = ~110 min, 50 questions = ~75 min

5. Target Audience
   - "Default Book readers"
   - Affects distractor difficulty and scenario complexity

**Store as variables for phases 3-7**

---

### Phase 3: Distribution Strategy ✅

**Create distribution map (based on QUESTION_COUNT):**

For 100 questions (standard T2):
- Q1-15: Precision_Recall
- Q16-35: Conceptual_Distinction
- Q36-55: Critical_Evaluation
- Q56-75: Architecture_Analysis
- Q76-100: Decision_Matrix

For 50 questions (scaled down):
- Q1-8: Precision_Recall (8)
- Q9-18: Conceptual_Distinction (10)
- Q19-27: Critical_Evaluation (10)
- Q28-36: Architecture_Analysis (9)
- Q37-50: Decision_Matrix (13)

**Dynamically calculate based on QUESTION_COUNT**

---

### Phase 4: Spawn Subagents (Parallel) ⭐ ENHANCED WITH VERIFICATION

**For each question type, spawn ONE Task subagent with parameterized prompt:**

```
SUBAGENT PROMPT TEMPLATE (GENERIC):

---MANDATORY PREREQUISITE READING (VERIFIABLE)---
Before generating ANY questions, you MUST read and understand these:

STEP 1: READ THIS SKILL FILE COMPLETELY
   File: .claude/skills/assessment-architect/SKILL.md
   Required: Understand the 7-phase workflow and validation standards

   After reading, summarize:
   - "What are the 3 main validation standards for questions?"
   - "What does DIF/DIS/DF mean and what are the T2 targets?"
   - "What is the required output format for your questions?"

STEP 2: READ ALL REFERENCE DOCS IN ORDER (with verification)
   a) bloom-taxonomy.md
      After: "List 2 question stems that target Analyze level"
   b) psychometric-standards.md
      After: "Explain why DIS > 0.30 matters for question quality"
   c) distractor-generation-strategies.md
      After: "Describe 2 distractor strategies you will use in your questions"
   d) academic-rigor-tiers.md
      After: "What DIF range targets T2 Intermediate difficulty?"

STEP 3: READ ALL SOURCE LESSONS (with concept extraction)
   Path: {CHAPTER_PATH}
   Read ALL lessons (not just first 5):
   {LESSON_LIST}

   After reading, identify and list:
   - "3 core CONCEPTS that span multiple lessons"
   - "2 architectural trade-offs discussed across lessons"
   - "Key relationships between concepts"

   CONCEPT-FOCUSED GENERATION:
   Your questions should test CONCEPTS and relationships, not lesson facts.

   WRONG: "According to Lesson X, what is [definition]?"
   RIGHT: "Compare [Concept A from Lessons X-Y] with [Concept B from Lessons Z].
           Which statement best captures the trade-off?"

---ONLY AFTER READING ABOVE---

TASK: Generate {COUNT} {TYPE} questions for {CHAPTER_NAME}

OUTPUT FORMAT: MARKDOWN (not JSON)

QUESTIONS {START}-{END}:
- {TYPE} questions
- Each question with Q number, stem, A/B/C/D options
- NO answers inline (answers in separate key at end of file)
- Each question MUST reference specific lessons from {CHAPTER_NAME}

FILE STRUCTURE:
# Questions {START}-{END}: {TYPE}

**Q{START}. Question stem here (specific to {CHAPTER_NAME})**

A) Option A

B) Option B

C) Option C

D) Option D

---

[Repeat for all {COUNT} questions]

## Question Reasoning & Validation

Q{START}: Bloom=Level | DIF=score | DIS=score | DF=all >5%
  Source: {CHAPTER_NAME} Lesson {NAME} | Reasoning: [specific lesson reference]

[Include reasoning for all questions]

OUTPUT TO THIS FILE:
assessments/{CHAPTER_SLUG}-q{SECTION}-{TYPE}.md

VALIDATION (Before output):
  ✓ {COUNT} questions present
  ✓ Each question references specific {CHAPTER_NAME} content
  ✓ Each has Q number, stem, A/B/C/D
  ✓ DIF in 50-70% range
  ✓ DIS > 0.30
  ✓ All distractors >5% plausible
  ✓ No JSON or intermediate formats
  ✓ Markdown readable and well-formatted
  ✓ Output to assessments/ directory ONLY
```

**Spawn 5 agents in PARALLEL:**
1. Agent 1: Generate Q1-Q15 (Precision_Recall) → `assessments/{CHAPTER_SLUG}-q1-precision-recall.md`
2. Agent 2: Generate Q16-Q35 (Conceptual_Distinction) → `assessments/{CHAPTER_SLUG}-q2-conceptual-distinction.md`
3. Agent 3: Generate Q36-Q55 (Critical_Evaluation) → `assessments/{CHAPTER_SLUG}-q3-critical-evaluation.md`
4. Agent 4: Generate Q56-Q75 (Architecture_Analysis) → `assessments/{CHAPTER_SLUG}-q4-architecture-analysis.md`
5. Agent 5: Generate Q76-Q100 (Decision_Matrix) → `assessments/{CHAPTER_SLUG}-q5-decision-matrix.md`

---

### Phase 5: Verify Subagent Outputs ✅ ENHANCED RELIABILITY GATE

**Before assembly, verify all files exist and are valid:**

```
STEP 5.1: File Verification (Generic)
  FOR section in 1,2,3,4,5:
    file = assessments/{CHAPTER_SLUG}-q{section}-*.md
    IF file NOT exist: FAIL "Missing {file} - Agent {section} did not write output"
    size = get_file_size(file)
    IF size < 5KB: FAIL "{file} too small (only {size}KB) - incomplete output"
    IF size > 100KB: WARN "{file} larger than expected ({size}KB)"

STEP 5.2: Content Validation (Generic)
  FOR file in [q1, q2, q3, q4, q5]:
    content = read(file)
    count_q = grep_count("^\\*\\*Q[0-9]", content)
    expected_count = {SECTION_QUESTION_COUNT}
    IF count_q != expected_count: FAIL "{file} has {count_q} questions, expected {expected_count}"

    IF grep("JSON", content): FAIL "{file} contains JSON - must be markdown"
    IF grep("\\[.*loaded from", content): FAIL "{file} has placeholders"
    IF grep("TO_BE_FILLED", content): FAIL "{file} has incomplete questions"

STEP 5.3: ANSWER KEY VALIDATION (NEW - CRITICAL)
  ⚠️ VALIDATION GATE: Verify answer keys are grounded in questions, not placeholders

  FOR each file:
    Extract all answers (grep "^[A-D]\)" {file})
    Count: count_A, count_B, count_C, count_D

    For {SECTION_QUESTION_COUNT} questions:
    - Expected: ~{SECTION_QUESTION_COUNT}/4 per choice (±4 tolerance)

    Example: If section has 20 questions:
      Expected per choice: 5 (20/4)
      Acceptable range: 1-9 per choice (5±4)
      Red flag: >15 of same choice (>70% bias)

    IF count_X > {SECTION_QUESTION_COUNT} * 0.70:
      FAIL "{file} has {count_X} answers = {section} - statistically impossible, likely placeholders"

    Print distribution: "Q{section}: A={count_A} B={count_B} C={count_C} D={count_D}"

STEP 5.4: CONTENT QUALITY CHECK (NEW)
  ⚠️ VALIDATION GATE: Verify questions test concepts, not lesson trivia

  FOR each file:
    count_lesson_cites = grep_count("According to Lesson", {file})
    count_questions = grep_count("^\\*\\*Q[0-9]", {file})

    percentage = (count_lesson_cites / count_questions) * 100

    IF percentage > 50%:
      WARN "{file}: {percentage}% of questions cite 'According to Lesson...'
            This suggests lesson-fact testing, not concept mastery.
            Desired: <20% explicit lesson citations"

  ✓ All 5 files verified for content quality
```

---

### Phase 6: Deterministic Assembly & Output Quality ✅ ENHANCED

**Load and concatenate files with explicit protocol, removing internal planning headers:**

```
STEP 6.1: Load Header (User-Facing)
  header = build with metadata:
    - Title: {CHAPTER_NAME} Certification Assessment
    - Description: Professional assessment for {TARGET_AUDIENCE}
    - Questions: {QUESTION_COUNT}
    - Time Limit: {TIME_LIMIT} minutes
    - Passing Score: 75%
    - Instructions: Answer all questions. Select the best option.

STEP 6.2: Load Questions in Order (REMOVE INTERNAL HEADERS)
  questions = ""
  internal_headers = ["Precision_Recall", "Conceptual_Distinction", "Critical_Evaluation",
                      "Architecture_Analysis", "Decision_Matrix"]

  FOR file in [q1, q2, q3, q4, q5]:
    IF file NOT exist: FAIL "Missing file during assembly"
    content = read(file)

    ⚠️ CRITICAL: Strip internal planning headers
    FOR header in internal_headers:
      content = remove_lines_matching("^# Questions.*{header}$", content)
      content = remove_lines_matching("^\\*\\*{header}\\*\\*", content)

    questions += content

  VALIDATE after loading:
    count = grep_count("^\\*\\*Q[0-9]", questions)
    IF count != {QUESTION_COUNT}: FAIL "Only {count} questions loaded, expected {QUESTION_COUNT}"
    IF grep("\\[", questions): FAIL "Placeholders found - files not loaded correctly"

    ⚠️ Verify NO internal headers remain:
    IF grep("Precision_Recall|Conceptual_Distinction|Critical_Evaluation|Architecture_Analysis|Decision_Matrix", questions):
      FAIL "Internal planning headers detected in output - must be removed before delivery"

STEP 6.3: Build Answer Key Section
  answer_key = """
  # Answer Key

  {Build table or list of Q1=A, Q2=B, Q3=A, etc.}
  {Show answer distribution: A=25, B=26, C=24, D=25}
  """

  IF count(answers) != {QUESTION_COUNT}: FAIL "Answer count mismatch"

STEP 6.4: Add Metadata Section (INTERNAL, NOT FOR TEST-TAKERS)
  metadata = """
  # Assessment Metadata (Educator Reference Only)

  ## Question Type Distribution
  - Precision_Recall: Q1-Q{PR_END} ({PR_COUNT} questions)
  - Conceptual_Distinction: Q{CD_START}-Q{CD_END} ({CD_COUNT} questions)
  - Critical_Evaluation: Q{CE_START}-Q{CE_END} ({CE_COUNT} questions)
  - Architecture_Analysis: Q{AA_START}-Q{AA_END} ({AA_COUNT} questions)
  - Decision_Matrix: Q{DM_START}-Q{DM_END} ({DM_COUNT} questions)

  ## Psychometric Metrics
  - Difficulty Index (DIF): Average 0.62 (target 0.50-0.70)
  - Discrimination Index (DIS): Average 0.38 (target >0.30)
  - Distractor Functionality (DF): All >5% (target >5%)
  - Kuder-Richardson 20 (KR-20): 0.72 (target >0.70)

  ## Cognitive Level Distribution
  - Remember: 7% (7 questions)
  - Understand: 25% (25 questions)
  - Apply: 30% (30 questions)
  - Analyze: 23% (23 questions)
  - Evaluate: 15% (15 questions)

  ## Lesson Coverage
  {List lessons and number of questions per lesson}
  {Flag any lessons with <2 questions}
  """

STEP 6.5: Assemble Final Markdown
  output = header + "\\n\\n---\\n\\n" + questions + "\\n\\n---\\n\\n" + answer_key + "\\n\\n---\\n\\n" + metadata

STEP 6.6: Pre-DOCX Validation
  size = get_file_size(output)
  expected_size_kb = {QUESTION_COUNT} * 0.5  (rough estimate)
  IF size < expected_size_kb * 0.8: FAIL "Markdown too small ({size}KB), expected >{expected_size_kb}KB"
  IF grep("\\[.*loaded from", output): FAIL "Placeholders still present"

  ⚠️ CRITICAL: Final header verification
  IF grep("^# Questions.*Precision_Recall|Conceptual_Distinction|Critical_Evaluation|Architecture_Analysis|Decision_Matrix", output):
    FAIL "Internal planning headers present in assembled output - STOP before DOCX generation"

  ✓ Markdown ready for DOCX conversion
```

---

### Phase 7: DOCX Generation & Final Output Quality Validation ⭐ ENHANCED RELIABILITY GATE

**Convert markdown to DOCX and verify final product meets all quality standards:**

```
STEP 7.1: Generate DOCX from Markdown
  pandoc final_markdown.md -o {CHAPTER_SLUG}-Assessment-Final.docx --from=markdown --to=docx

  IF conversion fails: FAIL "Pandoc conversion error - check markdown syntax"

STEP 7.2: Post-DOCX File Validation (CRITICAL)
  IF DOCX file NOT exist: FAIL "Pandoc conversion failed - no output file"

  size = get_file_size(DOCX)
  expected_docx_size = {QUESTION_COUNT} * 0.35  (rough estimate in KB)
  IF size < expected_docx_size * 0.8: FAIL "DOCX too small ({size}KB) - indicates missing questions or conversion error"

  ✓ File exists and has reasonable size

STEP 7.3: Extract and Validate DOCX Content (CRITICAL FORMAT CHECK)
  text = extract_text_from_DOCX(DOCX)

  ⚠️ Count questions in final DOCX:
  count_q = grep_count("^Q[0-9]+\\.", text)  (look for "Q1." format)
  IF count_q < {QUESTION_COUNT} * 0.95:
    FAIL "Only {count_q} questions in DOCX (expected ~{QUESTION_COUNT})"

  ⚠️ CRITICAL: Verify NO internal planning headers in final output:
  internal_headers = ["Precision_Recall", "Conceptual_Distinction", "Critical_Evaluation",
                      "Architecture_Analysis", "Decision_Matrix"]

  FOR header in internal_headers:
    IF grep("{header}", text):
      FAIL "Internal planning header '{header}' found in DOCX output - user-facing document must not contain internal structure"

  ⚠️ Verify NO placeholder text:
  IF grep("\\[.*loaded from", text): FAIL "Placeholders found in DOCX"
  IF grep("TO_BE_FILLED|\\[PLACEHOLDER", text): FAIL "Placeholder text in DOCX"

  ✓ Content structure validated

STEP 7.4: Answer Key Distribution Validation (FINAL CHECK)
  ⚠️ Extract answer key section from DOCX
  answers = extract_section("Answer Key", text)

  Count answer distribution:
  count_A = grep_count("[A)]", answers)
  count_B = grep_count("[B)]", answers)
  count_C = grep_count("[C)]", answers)
  count_D = grep_count("[D)]", answers)

  total_answers = count_A + count_B + count_C + count_D

  IF total_answers != {QUESTION_COUNT}:
    FAIL "Answer key count mismatch: {total_answers} answers, expected {QUESTION_COUNT}"

  ⚠️ Check for severe position bias (same answer >70% of the time):
  FOR choice in [A, B, C, D]:
    percentage = (count_{choice} / {QUESTION_COUNT}) * 100
    IF percentage > 70%:
      FAIL "Answer key position bias: {choice} = {percentage}% (impossible distribution)"

  ✓ Answer key distribution validated:
    A={count_A}, B={count_B}, C={count_C}, D={count_D}

STEP 7.5: Professional Formatting Validation
  ⚠️ Check for clean formatting:
  IF grep("^-{20}", text):  FAIL "Separator lines visible in output (should be internal)"
  IF grep("^##", text):     WARN "Heading structure present - verify hierarchy is clean"

  ⚠️ Check question formatting:
  FOR Q in [1 to {QUESTION_COUNT}]:
    IF NOT grep("^Q{Q}\\.", text):
      WARN "Question {Q} formatting may be inconsistent - verify numbering"

  ✓ Formatting validated

STEP 7.6: Metadata Separation Validation
  ⚠️ Verify Assessment Metadata section is clearly separated:
  IF NOT grep("Assessment Metadata", text):
    WARN "Assessment metadata section not found - educators won't have psychometric reference"

  IF grep("Educator Reference Only", text):
    ✓ Metadata properly marked as internal/educator reference

STEP 7.7: Final Delivery & User Notification
  File location: /assessments/{CHAPTER_SLUG}-Assessment-Final.docx
  File format: Microsoft Word (.docx)
  File size: {SIZE}KB

  Content verified:
  ✓ {QUESTION_COUNT} questions
  ✓ Answer key (distribution validated)
  ✓ No internal planning headers in user-facing content
  ✓ Metadata section for educators
  ✓ Pass score: 75%
  ✓ Time limit: {TIME_LIMIT} minutes

  Ready for print/distribution ✓

STEP 7.8: Error Handling & Failure Recovery
  IF any validation gate fails:
    1. Report specific failure: "DOCX validation failed at Step 7.X: {error_message}"
    2. Provide remediation: "To fix: {specific_action}"
    3. Offer retry: "Use /assessment-architect --regenerate-section {SECTION} to fix"
    4. Never deliver invalid DOCX to user
```

---

### Phase 8: Iterative Improvement & Feedback Loop 🔄 (FUTURE ENHANCEMENT)

**Optional: Handle validation failures with targeted regeneration:**

```
IF Phase 5 validation fails (answer key bias, missing lessons, etc.):

OPTION 1: Full Regeneration
  /assessment-architect chapter {NUM} --regenerate-full
  → Re-run Phases 0-7 with same parameters
  → User reports specific failures, skill adapts

OPTION 2: Targeted Section Regeneration
  /assessment-architect chapter {NUM} --regenerate-section {SECTION}
  Example: /assessment-architect chapter 5 --regenerate-section q2-conceptual-distinction
  → Re-run only subagent for section 2 (Q16-Q35)
  → Re-run Phase 5-7 validation
  → Replace only {section} in final DOCX

OPTION 3: Manual Review & Adjustment
  User provides feedback: "Q16-Q20 have weak distractors"
  System offers options:
    a) Regenerate Q16-Q20 with enhanced distractors
    b) Keep questions, revise answer key
    c) Accept and regenerate full section

  → Document feedback in session notes
  → Track which sections had issues for future reference
```

---

## Reliability Checklist (Before Delivery) - GENERIC

**Must verify ALL of these (adapted to QUESTION_COUNT):**

**Phase 4 (Subagent Execution):**
- [ ] All 5 subagents completed without errors
- [ ] Subagents demonstrated reading SKILL.md (verification summaries provided)
- [ ] Subagents demonstrated reading all 4 reference files (comprehension checks passed)
- [ ] Subagents demonstrated reading all source lessons (concept extraction provided)

**Phase 5 (Output Verification):**
- [ ] All 5 .md files exist in assessments/ with {CHAPTER_SLUG} prefix
- [ ] Each file >5KB and <100KB
- [ ] Each file has correct question count for section
- [ ] Answer key validation passed: No position bias >70% detected
- [ ] Content quality check passed: <50% "According to Lesson" citations
- [ ] No placeholder text in any section
- [ ] All 17+ lessons from chapter represented in questions

**Phase 6 (Assembly & Output Quality):**
- [ ] Markdown assembled = {QUESTION_COUNT} total questions
- [ ] Markdown size >{EXPECTED_SIZE}KB
- [ ] Internal planning headers removed (Precision_Recall, etc. NOT in user-facing output)
- [ ] Answer key section present with distribution summary
- [ ] Metadata section properly marked as "Educator Reference Only"
- [ ] No placeholder text "[.*loaded from.*]"
- [ ] Pre-DOCX validation passed

**Phase 7 (Final DOCX Quality):**
- [ ] DOCX generated successfully
- [ ] DOCX size >{EXPECTED_DOCX_SIZE}KB
- [ ] DOCX contains ~{QUESTION_COUNT} questions (≥95% of expected)
- [ ] DOCX contains answer key with distribution validated
- [ ] NO internal planning headers in DOCX (Precision_Recall, Conceptual_Distinction, etc.)
- [ ] NO placeholder text in DOCX
- [ ] Answer key distribution validated (no choice >70%)
- [ ] Professional formatting verified
- [ ] Metadata section marked for educators only

**If ANY check fails: STOP and report specific error to user with remediation path**

---

## Known Failure Modes & Prevention

### Executive Summary: 13 Failure Modes Addressed (Jan 17, 2026 Update)

**Original Issues (Post-Mortem Analysis):**
- 7 critical quality failures identified in first assessment generation
- 2 critical scope failures identified (Jan 17, 2026)
- Root causes traced to lack of governance, verification gates, and disambiguation

**Improvements Implemented:**
- ✅ Phase 0 added: Scope disambiguation (`ch X` vs `part X`)
- ✅ 4 existing phases ENHANCED with verification checkpoints
- ✅ 13 explicit failure modes documented with prevention strategies
- ✅ Chapter vs Part disambiguation (CRITICAL - prevents wrong scope)
- ✅ Multi-chapter Part support (can assess entire parts with 18+ chapters)
- ✅ Subagent prerequisite reading made MANDATORY and VERIFIABLE
- ✅ Clear scope: Certification exams only (not practice quizzes)

**Result:** Assessment generation now handles chapters OR parts with explicit disambiguation. Outputs certification exams (DOCX) only.

---

### Failure 1: Placeholder Integration (Jan 16, 2026) ❌
**Symptom:** DOCX contains "[Precision_Recall questions from agent...]"
**Root Cause:** Phase 5 never read question files, created template instead
**Prevention:**
  - ✓ Phase 5.1 explicit file loading (with generic path pattern)
  - ✓ Phase 5.2 content validation (counts questions)
  - ✓ Phase 6 placeholder check
  - ✓ Phase 7 DOCX validation

### Failure 2: Missing Question File
**Symptom:** Only 75 questions in output
**Root Cause:** Subagent 4 or 5 failed silently
**Prevention:**
  - ✓ Phase 5.1 verifies all 5 files exist (generic pattern)
  - ✓ Error message: "Missing assessments/{CHAPTER_SLUG}-q{N}.md"
  - ✓ Specific section count validation

### Failure 3: Generic/Textbook Questions
**Symptom:** Questions don't reference specific chapter content
**Root Cause:** Subagent didn't read source lessons
**Prevention:**
  - ✓ Subagent prompt mandates SKILL.md + references FIRST
  - ✓ Subagent prompt emphasizes: "Each question MUST reference specific {CHAPTER_NAME} content"
  - ✓ Reasoning section requires: "Source: {CHAPTER_NAME} Lesson {X}"

### Failure 4: Wrong Chapter Path
**Symptom:** Chapter 40 skill looks for Chapter 5 lessons
**Root Cause:** Hardcoded paths (FIXED: now dynamic discovery)
**Prevention:**
  - ✓ Phase 1 dynamically discovers {CHAPTER_PATH}
  - ✓ User prompted if path not found automatically
  - ✓ All subsequent phases use {CHAPTER_PATH} variable

### Failure 5: DOCX File Too Small
**Symptom:** DOCX size doesn't match question count
**Root Cause:** Incomplete markdown or conversion error
**Prevention:**
  - ✓ Phase 6.5: Pre-DOCX markdown size check (dynamic based on {QUESTION_COUNT})
  - ✓ Phase 7.2: Post-DOCX size validation
  - ✓ Phase 7.2: Question count in DOCX validation

### Failure 6: Answer Key Position Bias (Jan 16, 2026 - CRITICAL) ❌
**Symptom:** 74% of answers are "A" (Q16-Q35 all A, Q56-Q75 all A, Q76-Q100 all A)
**Root Cause:** Subagent answer keys are placeholders/templates, not grounded in question content
**Prevention:**
  - ✓ Phase 5.3: ANSWER KEY VALIDATION gate rejects if any choice >70%
  - ✓ Per-section distribution check: Expected ~25% per choice (±4 tolerance)
  - ✓ Final metric reported: "Q{section}: A={count_A} B={count_B} C={count_C} D={count_D}"
  - ✓ Phase 7.4: Final DOCX validation re-checks answer distribution
  - ✓ FAIL if pattern repeats in final DOCX

### Failure 7: Missing Lesson Coverage (Jan 16, 2026 - HIGH) ⚠️
**Symptom:** Only 15 lessons covered, but Chapter 5 has 17 lessons (missing creator-workflow, from-skills-to-business)
**Root Cause:** Phase 1 assumption of "first 15 lessons" instead of complete audit
**Prevention:**
  - ✓ Phase 1: COMPLETE LESSON AUDIT with bash count (not manual assumption)
  - ✓ Phase 1: Report total: "Found {TOTAL} lessons in Chapter {NUM}"
  - ✓ Phase 1: Anomaly detection: WARN if <10 or >25 lessons
  - ✓ Phase 5.2: Verify all discovered lessons represented in questions
  - ✓ Question type distribution ensures coverage across full lesson range

### Failure 8: Lesson-Fact Questions Instead of Concepts (Jan 16, 2026 - HIGH) ⚠️
**Symptom:** 60%+ of questions follow "According to Lesson X..." pattern (trivia, not mastery)
**Root Cause:** Subagents didn't understand concept-grounding requirement
**Prevention:**
  - ✓ Phase 4: EXPLICIT CONCEPT-FOCUSED GENERATION section in subagent prompt
  - ✓ Examples showing WRONG (lesson fact) vs RIGHT (conceptual) patterns
  - ✓ Phase 5.4: CONTENT QUALITY CHECK flags excessive "According to Lesson" citations
  - ✓ WARN if >50% questions cite "According to Lesson..."
  - ✓ Phase 7.3: Final DOCX check ensures <50% citation pattern

### Failure 9: Subagents Didn't Read Reference Files (Jan 16, 2026 - CRITICAL) ❌
**Symptom:** No evidence of distractor strategy, no psychometric grounding, placeholder answers
**Root Cause:** "MUST read references" instruction had no verification mechanism
**Prevention:**
  - ✓ Phase 4: MANDATORY PREREQUISITE READING with VERIFICATION
  - ✓ Step 1: Read SKILL.md + answer 3 comprehension questions
  - ✓ Step 2: Read 4 reference files + answer verification Q after each
  - ✓ Step 3: Read all source lessons + extract concepts before generating questions
  - ✓ Verification summaries required before generation allowed to proceed
  - ✓ Prompts explicitly state: "ONLY AFTER READING ABOVE → Generate questions"

### Failure 10: Internal Planning Headers in User Output (Jan 16, 2026 - MEDIUM)
**Symptom:** Final DOCX shows "# Questions 1-15: Precision_Recall" (internal structure visible to users)
**Root Cause:** Assembly phase didn't filter out internal planning headers
**Prevention:**
  - ✓ Phase 6.2: EXPLICIT HEADER STRIPPING for all internal header types
  - ✓ Phase 6.6: PRE-DOCX validation searches for remaining headers
  - ✓ Phase 7.3: FINAL DOCX check FAILS if any internal header found in output
  - ✓ Only user-facing content: Question numbers, stems, A/B/C/D options, answer key

### Failure 11: No User Input Phase (Jan 16, 2026 - MEDIUM)
**Symptom:** Quiz parameters hardcoded (100 questions, 150 min, T2 Intermediate) with no user negotiation
**Root Cause:** Workflow skipped user consultation phase entirely
**Prevention:**
  - ✓ Phase 0: USER INPUT & PARAMETER NEGOTIATION (NEW)
  - ✓ AskUserQuestion captures: title, question count, difficulty, time limit, audience
  - ✓ User confirmation required before proceeding to Phase 1
  - ✓ Parameters drive all subsequent phases (distribution, subagent count, etc.)

### Failure 12: Chapter vs Part Misinterpretation (Jan 17, 2026 - CRITICAL) ❌
**Symptom:** User says "ch 5" meaning Chapter 5 (Claude Code), skill interprets as Part 5 (Python Fundamentals with 18 chapters)
**Root Cause:** No disambiguation between chapter numbers and part numbers
**Real Example:**
  - User: "create quiz for chapter 5"
  - Skill thought: "Part 5: Python Fundamentals" (18 chapters, Ch 15-32)
  - User meant: "Chapter 5: Claude Code" (1 chapter, 17 lessons)
**Prevention:**
  - ✓ Phase 0: SCOPE DISAMBIGUATION (NEW) - parses "ch X" vs "part X" vs bare "X"
  - ✓ Book structure documented: Parts are folders `0X-*`, Chapters are subfolders `*/XX-*/`
  - ✓ Chapter numbers are GLOBAL (Ch 5 is in Part 2, not Part 5)
  - ✓ Bare numbers trigger disambiguation question
  - ✓ Clear input format table in Success Trigger section

### Failure 13: Scope Confusion - This Skill is for Exams Only (Jan 17, 2026 - CLARIFICATION)
**Symptom:** User expects practice quiz but skill generates certification exam
**Clarification:** This skill is ONLY for certification exams (DOCX). Practice quizzes are a DIFFERENT product.
**Two Different Products:**
  - **Practice Quiz** (`*_quiz.md`): MDX with <Quiz> component, explanations, in chapter dir
  - **Certification Exam** (this skill): DOCX, no explanations, in assessments/ dir
**Prevention:**
  - ✓ Skill description clearly states "certification exams (DOCX)"
  - ✓ Header explicitly says "NOT for: Practice quizzes"
  - ✓ If user wants practice quiz, direct them to existing `*_quiz.md` pattern or different skill

---

## Summary: Generic & Deterministic

**The principle:** Parallelization requires coordination. Coordination requires explicit protocols.

**Before (Jan 16):**
- Hardcoded to Chapter 5 (breaks for Ch 40, Ch 50)
- No Chapter vs Part disambiguation
- Generic questions (no source grounding)

**After (Jan 17):**
- Explicit scope disambiguation: `ch X` vs `part X` vs bare `X`
- Multi-chapter Part support (can assess Part 5 with 18 chapters)
- Validation gates prevent placeholder/generic failures
- Subagents read references + lessons (ensures quality)

**Key variables (discovered or provided):**
- `{SCOPE_TYPE}` - "chapter" | "part"
- `{SCOPE_NUM}` - The number (5, 40, etc.)
- `{SCOPE_PATH}` - Directory path (dynamically discovered)
- `{QUESTION_COUNT}` - Total questions (user configurable)
- `{CHAPTER_COUNT}` - 1 for chapter, N for parts
- `{CHAPTERS[]}` - Array of chapters (for parts)

**Input Format Quick Reference:**
| Input | Scope | Example |
|-------|-------|---------|
| `ch 5` | Chapter 5 | Claude Code (17 lessons) |
| `part 5` | Part 5 | Python Fundamentals (18 chapters) |
| `5` | AMBIGUOUS | Ask user to clarify |

**Result:** One skill works for ANY chapter OR part, outputs certification exams (DOCX).

---

## Reference Materials for Autonomous Reasoning

Subagents reason through these materials (not follow step-by-step) to generate pedagogically sound assessments that meet validation thresholds.

| Reference | Path | Purpose |
|-----------|------|---------|
| **Distractor Strategies** | `references/distractor-generation-strategies.md` | Pedagogically sound distractor design for each question type |
| **Academic Rigor Tiers** | `references/academic-rigor-tiers.md` | T1-T4 frameworks for assessment difficulty and grading |
| **Psychometric Standards** | `references/psychometric-standards.md` | DIF/DIS/DF/KR-20 validation metrics and targets |
| **Bloom's Taxonomy** | `references/bloom-taxonomy.md` | Cognitive levels and question type mapping |
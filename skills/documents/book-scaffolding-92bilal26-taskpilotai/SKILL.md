---
name: book-scaffolding
description: |
  Plan, structure, and scaffold large educational books using cognitive load management,
  just-in-time specification, and pedagogical best practices. Use this skill when planning
  multi-part, multi-chapter educational works that require narrative continuity, progressive
  complexity, and hands-on exercises. This skill helps create cohesive learning journeys
  that balance foundational scaffolding with advanced independence. Activate when tasks
  involve structuring books, managing cognitive load across chapters, defining part-level
  narratives, or coordinating multi-phase content development workflows.
version: "2.1.0"
constitution_alignment: "v4.0.1"
---

# Skill: Book Scaffolding and Structure Planning

**Purpose**: Plan, structure, and scaffold large educational books using cognitive load management, just-in-time specification, and pedagogical best practices.

**Constitution Alignment**: v4.0.1 emphasizing:
- **Principle 1**: Specification Primacy ("Specs Are the New Syntax")
- **Section IIa**: Panaversity 4-Layer Teaching Method (progressive lesson structure)
- **Section IIb**: AI Three Roles Framework (bidirectional co-learning partnership)
- **Nine Pillars** (Section I): AI CLI, Markdown, MCP, AI-First IDEs, Cross-Platform, TDD, SDD, Composable Skills, Cloud-Native
- **Principle 4**: Coherent Pedagogical Structure (flexible lesson counts based on concept density)

**Status**: Reusable skill (learned from 002-book-structure sprint, enhanced with structural patterns)
**Application**: Any multi-part, multi-chapter educational work

---

## Core Principles (9 Learnings from Sprint)

### 1. Just-In-Time Specification ("Specs Are the New Syntax")
❌ **DON'T**: Decide everything upfront. Block on all clarifications before moving forward.
✅ **DO**: Spec what's needed now. Defer part-specific clarifications to when that part is ready for planning.

**Why**: Unblocks work immediately. Clarifications arrive exactly when needed (during chapter-planner phase). Respects SDD loop: **Spec → Plan → Implement per part (one at a time)**.

**KEY**: Specification writing is the PRIMARY skill. Book structure scaffolds specification-first learning across all parts.

**Example**:
- Part 1 spec created with only Part 1 narrative ("Coder to Super Orchestrator")
- Agent frameworks for Part 6 deferred until Part 6 is ready for planning
- Each part planning phase triggers clarifications for that part

### 2. Minimal MVP Approach
❌ **DON'T**: Create comprehensive guides, templates, all part specs upfront, skill integration guides, validation guides
✅ **DO**: Create only essentials. Focus on: Part intros, Chapter placeholders, Part 1 spec, validation report

**Why**: Reduces redundancy. Eliminates over-engineering. Gets to writing faster.

**What Actually Needed**:
- 7 part intro files (explain what each part is about)
- 32 chapter folder structure with READMEs
- 1 Part 1 spec (detailed, ready for chapter-planner)
- Validation report (confirm structure works)
- Parts 2-7 specs deferred until needed

### 3. Narrative Continuity
❌ **DON'T**: Treat chapters as isolated units. Let each chapter wander to its own conclusion.
✅ **DO**: Use a unifying narrative arc across all chapters in a part.

**Why**: Readers stay engaged. Content cohesion improves. Readers see connections.

**Example from Part 1**:
- **Unifying narrative**: "From Coder to Super Orchestrator"
- **Chapter 1**: Sets up the mindset shift
- **Chapter 2**: Explains the 9 revolutions that enable it
- **Chapter 3**: Installs the tools you'll need as an orchestrator
- **Chapter 4**: You execute your first orchestration (spec → AI → test → deploy)
- **Chapter 5**: You debug when orchestration fails (resilience)

Each chapter reinforces the "orchestrator" identity while progressing the story.

### 4. Cognitive Load Management (CRITICAL)
❌ **DON'T**: Front-load complex concepts. Assume readers have prior knowledge.
✅ **DO**: Manage cognitive load across chapters. Light → Moderate → Advanced. Heavy scaffolding early.

**Framework**:
- **Cognitive Load Level**: Light, Moderate, Heavy (define per part)
- **Scaffolding Level**: Heavy (early), Moderate (middle), Light (late)
- **Concept Density**: 3-7 key concepts per chapter (varies by part)
- **Review Cycles**: 2-3 for new material, 1 for reinforcement

**Example from Part 1**:
- **Cognitive Load**: LIGHT (foundational orientation)
- **Scaffolding**: HEAVY (show-then-explain, guided examples, zero gatekeeping)
- **Concept Density**: 3-4 per chapter (time for absorption)
- **Result**: Beginners feel comfortable, not overwhelmed

### 5. Show-Then-Explain Pedagogy
❌ **DON'T**: Explain concepts first, then show examples
✅ **DO**: Show working examples first, then explain the principles

**Why**: Cognitive science: People learn better when they see concrete examples before abstract rules.

**Pattern**:
1. **Show**: "Here's a working spec, generated code, test results"
2. **Explain**: "Here's why this works. Here are the principles."
3. **Practice**: "Now you try with a different domain"
4. **Assess**: "Can you do this independently?"

### 6. Zero Gatekeeping Language
❌ **DON'T**: "It's simple...", "Obviously...", "Just...", "Anyone can..."
✅ **DO**: Explain every assumption. Honor the reader's learning journey.

**Why**: Gatekeeping language alienates readers who don't find it simple. Inclusive language respects all learners.

**Example Rewrites**:
- ❌ "Simply write a spec and Claude Code generates code"
- ✅ "Write a spec with clear requirements. Claude Code reads your spec and generates code that meets those requirements."

- ❌ "Debugging is easy—just read the error message"
- ✅ "When code fails, read the error message to understand what happened. Here's how to interpret common errors..."

### 7. Connection Mapping (Part-to-Part)
❌ **DON'T**: Treat each part as isolated. Readers wonder "Why am I learning this?"
✅ **DO**: Explicitly map how each part prepares for subsequent parts.

**Pattern**:
```
Part 1 → Mindset shift (orchestration)
  ↓ prepares you for Part 2 (tools)
  ↓ which prepares you for Part 3 (prompting)
  ↓ which prepares you for Part 4 (Python)
  ↓ which prepares you for Part 5 (Spec-Kit)
  ↓ which prepares you for Part 6 (agents)
  ↓ which prepares you for Part 7 (MCP)
```

**Example from Part 1 Spec**:
- Chapter 1 prepares for: Part 2 (tools matter), Part 3 (specs), Part 4 (orchestration is code)
- Chapter 2 prepares for: Part 5 (Spec-Kit), Part 6 (agents), Part 7 (MCP integration)
- Chapter 3 prepares for: Chapter 4 (hands-on), Parts 2-7 (tools assumed working)

### 8. Success Criteria Definition
❌ **DON'T**: Vague acceptance criteria ("students will understand...")
✅ **DO**: Measurable, observable success criteria for each chapter

**Pattern per Chapter**:
```
Learning Outcome: "Understand why orchestration beats coding"
Success Criteria: "Reader can articulate in their own words why orchestration > coding"
Measurable Target: "90%+ of readers can explain (in own words) without prompting"
```

**Example from Part 1, Chapter 1**:
- Readers can name 3 mechanisms of vertical intelligence (subagents, skills, MCP)
- Readers see real ARR numbers and feel motivated (not threatened)
- Readers are ready for "Understanding 9 Revolutions" (Chapter 2)

### 9. Hands-On Exercises (Practical Chapters)
❌ **DON'T**: Teach only concepts. No practice.
✅ **DO**: Include real exercises for practical chapters (tool setup, first program, debugging)

**Exercise Pattern**:
1. **Task**: Real but constrained (e.g., "build email validator")
2. **Your Role**: Write spec / set up tools / identify bug
3. **AI/System Role**: Generate code / install / fix
4. **Your Role Again**: Test / verify / understand
5. **Reflection**: "Why did this work? What did you learn?"

**Example from Part 1**:
- **Chapter 3**: Install all 3 tools, verify end-to-end
- **Chapter 4**: Write spec for email validator → Claude Code generates → Test
- **Chapter 5**: Debug deliberately broken code, iterate to fix

### 10. Nine Pillars Alignment (NEW - Constitution v3.1.2)
❌ **DON'T**: Structure book without Nine Pillars framework
✅ **DO**: Scaffold content to progressively introduce and apply Nine Pillars

**The Nine Pillars of AI-Native Development:**
1. AI-First Mindset, 2. Specification-First Development, 3. Evals-Driven Validation, 4. Iterative Convergence, 5. Context Engineering, 6. Output Validation, 7. Strategic Orchestration, 8. Continuous Learning, 9. Ethical Responsibility

**Scaffolding Strategy:**
- **Part 1**: Introduce Pillars 1, 2, 8 (AI-First Mindset, Specs-First, Continuous Learning)
- **Parts 2-5**: Apply Pillars 2-6 in practice (Spec-First, Evals, Convergence, Context, Validation)
- **Parts 6-7**: Emphasize Pillar 7 (Strategic Orchestration for LAMs/Agents)
- **Parts 10-13**: Apply all 9 pillars in production contexts

**Per-Chapter Scaffolding:**
- Identify which 2-3 pillars each chapter teaches/applies
- Ensure progressive coverage (don't introduce all 9 at once)
- Document pillar alignment in chapter specs

### 11. LLM to LAM Evolution Scaffolding (NEW - Constitution v3.1.2)
❌ **DON'T**: Treat all AI interaction as the same across parts
✅ **DO**: Scaffold transition from LLM-based (Parts 1-5) to LAM-based (Parts 6-7+) content

**LLM-Based Scaffolding (Parts 1-5):**
- Focus: AI as reasoning partner (prompt-response)
- Skills: Prompt engineering, specification writing, output validation
- Pattern: Human specifies → AI responds → Human validates

**LAM-Based Scaffolding (Parts 6-7+):**
- Focus: AI as autonomous agent (multi-step task execution)
- Skills: Agent design, orchestration, safety constraints
- Pattern: Human orchestrates → AI acts autonomously → Human supervises

**Transition Scaffolding (Part 5 → Part 6):**
- Part 5 final chapters: Mastery of LLM prompting (foundation)
- Part 6 opening: Introduction to LAMs (building on LLM skills)
- Key teaching: "Tell AI what to do" (LLM) → "Tell AI what to achieve, it figures out how" (LAM)

### 12. Co-Learning Partnership Scaffolding (NEW - Constitution v3.1.2)
❌ **DON'T**: Frame AI as passive tool throughout book
✅ **DO**: Scaffold co-learning partnership from Chapter 1 onward

**Scaffolding Progression:**
- **Part 1**: Introduce co-learning concept (AI teaches you, you teach AI)
- **Parts 2-5**: Demonstrate bidirectional learning in every chapter
- **Parts 6+**: Show advanced co-learning (agent learns user's domain)

**Per-Chapter Requirements:**
- Show at least ONE instance where student learns FROM AI
- Show at least ONE instance where AI adapts TO student feedback
- Demonstrate convergence (not "perfect on first try")

---

## The Book Scaffolding Workflow

### Phase 1: Global Structure (Book Level)
**Input**: User vision for the entire book (theme, chapters, learning journey)
**Output**:
- Multi-part architecture with learning progression
- Chapter overview (titles, scope)
- Cognitive load mapping (light → heavy distribution)

**Questions to Ask**:
1. What is the unifying narrative across all parts?
2. What is the cognitive load of each part?
3. How do chapters connect part-to-part?
4. Where are the heavy scaffolding points?

**Reference**: See [reference/structural-patterns.md](reference/structural-patterns.md) for detailed guidance on book organization patterns.

### Phase 2: Part-Level Spec (One Part at a Time)
**Input**: Part purpose, chapter titles, part's role in overall journey
**Output**: Detailed part spec with:
- Part narrative (unifying theme for this part)
- Chapters fully specified (learning outcomes, key topics, success criteria)
- Pedagogical strategy (cognitive load, scaffolding, concept density)
- Connection map (how this part prepares for next)
- Hands-on exercises (for practical chapters)

**Defer**:
- Part-specific clarifications (agent frameworks, case studies, etc.) → resolve during chapter-planner phase
- Future part specs → create just-in-time when prior parts are in implementation

**Questions to Ask**:
1. What is this part's PURPOSE in the overall book?
2. What should readers KNOW by the end?
3. What's the narrative arc across chapters?
4. Which chapters need heavy scaffolding? Light?
5. What hands-on exercises would build confidence?

**Reference**: See [reference/chapter-flow-patterns.md](reference/chapter-flow-patterns.md) for different chapter sequencing approaches.

### Phase 3: Chapter-Planner Phase (Invoke Subagent)
**Input**: Part spec (from Phase 2)
**Subagent**: chapter-planner
**Output**: For each chapter in the part:
- `chapter-NN-plan.md` (detailed lesson breakdown)
- `chapter-NN-tasks.md` (implementation checklist)

**What Happens**:
- chapter-planner reads your part spec
- Breaks each chapter into 5-7 lessons
- Defines learning objectives, code examples, exercises per lesson
- Requests clarifications if needed (JUST-IN-TIME)
- Provides timeline estimates

**Reference**: See [reference/chapter-dependencies.md](reference/chapter-dependencies.md) for managing prerequisites and chapter relationships.

### Phase 4: Lesson-Writer Phase (Invoke Subagent)
**Input**: chapter-NN-plan.md (from Phase 3)
**Subagent**: content-implementer (iterative)
**Output**: Complete lesson content
**Process**: Write one lesson at a time, review, refine, approve

### Phase 5: Validation Phase (Invoke Subagent)
**Input**: Completed chapter (from Phase 4)
**Subagent**: validation-auditor
**Output**: Validation report
**Checks**: Code correctness, pedagogical effectiveness, Constitution alignment

---

## Quality Standards Checklist

All book content MUST:
- ✅ **Apply all domain skills**: Use learning-objectives, concept-scaffolding, code-example-generator, exercise-designer, assessment-builder, technical-clarity, book-scaffolding, ai-augmented-teaching
- ✅ **Show-then-explain**: Examples first, principles second, practice third
- ✅ **Zero gatekeeping**: No "simple", "obvious", "just". Explain every assumption.
- ✅ **Type hints**: All code includes type hints (language-appropriate)
- ✅ **Testing**: All code examples are tested before publication
- ✅ **Accessibility**: Alt text, high contrast, clear language, multiple reading paths
- ✅ **Constitutional alignment**: Align with project principles and non-negotiable rules

## Acceptance Checks

- [ ] Each section/lesson tagged with complexity tier (Beginner/Intermediate/Advanced/Professional)
- [ ] Beginner-tier sections respect concept cap (≤ 5 new concepts per section)
- [ ] Dependency Index present: prerequisites and forward links with anchors
- [ ] SpecRef included at part/chapter headers

### Dependency Index (example)
```
Prerequisites: Part 1 Ch 2 (tools), Part 3 Ch 1 (prompting)
Next: Part 4 Ch 3 (types), Part 5 Ch 1 (Spec‑Kit intro)
```

---

## Success Metrics

For each part:

| Metric | Success Measure | Target |
|--------|-----------------|--------|
| **Narrative Clarity** | Readers articulate the part's purpose | 90%+ can explain |
| **Cognitive Load** | No overwhelming chapters; scaffolding appropriate | 85%+ find it well-paced |
| **Learning Outcomes** | Readers achieve measurable outcomes | 80%+ achieve all outcomes |
| **Hands-On Completion** | Readers complete exercises | 80%+ complete exercises |
| **Confidence** | Readers feel ready for next part | 85%+ agree |
| **Code Quality** | All examples run correctly | 100% pass testing |
| **Accessibility** | All readers can navigate (varied reading styles) | 95%+ accessibility |

---

## Anti-Patterns (What NOT to Do)

❌ **Over-Planning**: Creating all part specs upfront (deferring decision-making, blocking work)
❌ **Isolated Chapters**: No connection mapping; readers don't see the journey
❌ **Concept Overload**: 10+ concepts per chapter; beginners overwhelmed
❌ **Explain-Then-Show**: Principles first, examples second (harder to learn)
❌ **Gatekeeping Language**: "Simple", "obvious", "just"; alienates learners
❌ **No Exercises**: Passive reading; no confidence building
❌ **Inconsistent Scaffolding**: Heavy in middle, light at start (backwards)
❌ **Missing Success Criteria**: "They'll understand it"—no measurable target
❌ **Redundant Artifacts**: Multiple versions of same template, guide, spec
❌ **Part Specs Too Early**: Creating Part 5 spec before Part 1 is implemented (wasted effort)

---

## How to Use This Skill

### When Planning a New Part

```markdown
Use the book-scaffolding skill to:
1. Define the part's purpose in the overall book
2. Create the part narrative (unifying theme)
3. Specify chapters (learning outcomes, key topics, success criteria)
4. Map pedagogical strategy (cognitive load, scaffolding, concept density)
5. Define connection map (how this part prepares for next)
6. Identify hands-on exercises for practical chapters
```

### When Creating a Chapter Spec

```markdown
Use the book-scaffolding skill to:
1. Define chapter purpose (within part's narrative)
2. List learning outcomes (Bloom's taxonomy aligned)
3. Identify key topics to cover
4. Define success criteria (measurable, observable)
5. Plan pedagogical approach (show-then-explain, concept density)
6. Identify hands-on exercise (if practical chapter)
```

### When Reviewing Completed Content

```markdown
Use the book-scaffolding skill to:
1. Verify all domain skills applied
2. Check for show-then-explain pattern
3. Confirm zero gatekeeping language
4. Validate accessibility standards
5. Verify type hints and testing in code
6. Check Constitutional alignment
```

---

## References

For deeper guidance on specific aspects of book structure:

- **Directory Structure** (Project-Specific): `specs/book/directory-structure.md`
  - **THE authoritative source** for file paths and folder organization
  - 3-level hierarchy (Part → Chapter → Lesson)
  - Naming conventions (capitalized parts, lowercase chapters)
  - Required files and validation rules

- **Chapter Index** (Project-Specific): `specs/book/chapter-index.md`
  - All 32 chapter titles, numbers, and topics
  - Mapping chapters to parts
  - Chapter-specific content guidance

- **Chapter Flow Patterns**: [reference/chapter-flow-patterns.md](reference/chapter-flow-patterns.md)
  - Linear, spiral, modular, hybrid, and project-based flow patterns
  - Decision framework for choosing the right pattern
  
- **Structural Patterns**: [reference/structural-patterns.md](reference/structural-patterns.md)
  - Tutorial vs. reference balance
  - Chapter internal structure (IBS, MCA, Cookbook, EEE)
  - Part and section organization strategies
  
- **Content Organization**: [reference/content-organization.md](reference/content-organization.md)
  - Chunking strategies (micro, mini, standard, macro)
  - Hierarchical organization best practices
  - Cross-referencing techniques
  
- **Chapter Dependencies**: [reference/chapter-dependencies.md](reference/chapter-dependencies.md)
  - Dependency types and patterns
  - Core vs. optional chapters
  - Managing circular dependencies

---

## Version History

**v1.0** (2025-10-29): Created from 002-book-structure sprint learning
- 9 core principles
- Workflow (Phase 1-5)
- Quality standards
- Success metrics

**v2.0** (2025-10-29): Enhanced with structural patterns
- Integrated reference materials from book-architecture skill
- Added comprehensive flow patterns and organization strategies
- Consolidated as one of the 8 CoLearning Domain Skills

---

**Status**: Ready for use on all multi-part educational books. Proven on CoLearning Python & Agentic AI project.


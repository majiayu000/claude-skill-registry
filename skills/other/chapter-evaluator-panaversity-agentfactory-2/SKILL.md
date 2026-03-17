---
name: chapter-evaluator
description: "Evaluate educational chapters from dual student and teacher perspectives. This skill should be used when analyzing chapter quality, identifying content gaps, or planning chapter improvements. Reads all lessons in a chapter directory and provides structured analysis with ratings, gap identification, and prioritized recommendations."
---

# Chapter Evaluator Skill

Evaluate educational chapters through dual lenses: the **Student Experience** (engagement, clarity, confidence) and the **Teacher Perspective** (pedagogy, objectives, assessment). Output structured analysis with ratings, gaps, and actionable improvements.

## When to Use

- Analyzing a chapter's overall quality before publication
- Identifying why content "feels off" (too short, boring, disconnected)
- Planning improvements to existing chapters
- Comparing chapters against quality standards
- User asks to "evaluate", "review", "analyze", or "assess" a chapter

## Evaluation Process

### Step 1: Gather Chapter Content

Read all lesson files in the chapter directory:

```bash
ls -la <chapter-path>/*.md | grep -v summary | grep -v README | grep -v quiz
```

For each lesson file, extract:
- YAML frontmatter (learning objectives, cognitive load, skills, layer)
- Word count
- Section structure (headings)
- Try With AI prompts
- Hands-on exercises
- Code examples

### Step 2: Student Perspective Analysis

Evaluate as a beginner encountering this content for the first time.

#### 2.1 Engagement Score (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Compelling hook, real-world relevance clear, I want to keep reading |
| 7-8 | Interesting enough, some engaging moments, minor dry spots |
| 5-6 | Functional but forgettable, reads like documentation |
| 3-4 | Boring, walls of text, no compelling reason to continue |
| 1-2 | Would abandon after first section |

**Check for:**
- Opening hook (does first paragraph grab attention?)
- Real-world scenarios (why does this matter to ME?)
- Story/narrative flow vs disconnected facts
- Visual breaks (diagrams, tables, code blocks)
- Pacing variety (concept → hands-on → concept)
- **Comparative Value** (vs alternatives like VS Code/Copilot)

#### 2.2 Length Assessment

| Verdict | Criteria |
|---------|----------|
| Too Short | Missing examples, concepts unexplained, abrupt endings, "I don't understand" |
| Just Right | Each concept has sufficient depth, examples clarify, natural flow |
| Too Long | Repetitive explanations, over-elaborated points, could cut 30%+ |

**Word count benchmarks:**
- Conceptual lesson: 1,000-1,400 words
- Hands-on lesson: 1,200-1,600 words
- Installation/setup: 800-1,200 words (focused)
- Capstone: 1,400-1,800 words

#### 2.3 Clarity Score (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Crystal clear, no re-reading needed, "aha" moments |
| 7-8 | Mostly clear, occasional re-read for complex parts |
| 5-6 | Understandable with effort, some confusing sections |
| 3-4 | Frequently confused, missing context, jargon unexplained |
| 1-2 | Cannot follow, assumes knowledge I don't have |

**Check for:**
- Jargon introduced before defined
- Logical flow between paragraphs
- Transitions between sections
- Prerequisites assumed vs stated
- **Safety Checks:** No concatenated commands or risky copy-pastes

#### 2.4 Hands-On Effectiveness (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Clear steps, achievable, builds confidence, "I did it!" |
| 7-8 | Mostly clear, minor ambiguity, successful completion likely |
| 5-6 | Workable but confusing steps, may need to troubleshoot |
| 3-4 | Missing steps, unclear what to do, likely to get stuck |
| 1-2 | Cannot complete without external help |

**Check for:**
- Step-by-step instructions (numbered, clear)
- Expected output/results shown
- Troubleshooting guidance
- Connection to concepts just learned

#### 2.5 Progression Clarity (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Clear path from start to mastery, each lesson builds on previous |
| 7-8 | Generally progressive, minor jumps between lessons |
| 5-6 | Some logical progression, noticeable gaps |
| 3-4 | Disconnected lessons, unclear how they relate |
| 1-2 | Random ordering, no clear learning path |

**Check for:**
- Opening connections ("In Lesson N-1, you learned X. Now...")
- Running example threaded through chapter
- Skills building on each other
- Clear "what's next" at lesson end

#### 2.6 Confidence Score (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | "I can definitely do this now" - ready to apply independently |
| 7-8 | "I mostly understand and could figure out the rest" |
| 5-6 | "I kind of get it but would need help applying it" |
| 3-4 | "I'm confused about when/how to use this" |
| 1-2 | "I have no idea what I just read" |

**Check for:**
- Practice opportunities before moving on
- Verification steps ("you should see X")
- Real-world application examples
- "Try it yourself" prompts

### Step 3: Teacher Perspective Analysis

Evaluate as an instructional designer assessing pedagogical soundness.

#### 3.1 Learning Objectives Quality (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | SMART objectives, measurable, aligned to content and assessment |
| 7-8 | Clear objectives, mostly measurable, good alignment |
| 5-6 | Objectives present but vague or partially aligned |
| 3-4 | Weak objectives, not measurable, poor alignment |
| 1-2 | Missing or meaningless objectives |

**Check for:**
- Bloom's taxonomy verb alignment (Remember → Create)
- Measurable criteria ("can explain", "can create", "can distinguish")
- Assessment method specified
- Objectives actually taught in lesson content

#### 3.2 Cognitive Load Management (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Appropriate concepts for level, well-scaffolded, no overload |
| 7-8 | Generally appropriate, minor overload moments |
| 5-6 | Some cognitive overload, too many concepts at once |
| 3-4 | Significant overload, concepts piled without consolidation |
| 1-2 | Overwhelming, no chance of retention |

**Benchmarks by proficiency:**
- A1-A2: 3-5 new concepts per lesson
- B1-B2: 5-7 new concepts per lesson
- C1-C2: 7-10 new concepts per lesson

**Check for:**
- New concepts counted in frontmatter
- Concepts introduced one at a time
- Practice before new concept introduced
- Chunking of complex procedures

#### 3.3 Scaffolding Quality (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Perfect progression, each concept builds on previous, no gaps |
| 7-8 | Good scaffolding, minor jumps that students can bridge |
| 5-6 | Some scaffolding gaps, requires prior knowledge not taught |
| 3-4 | Significant gaps, assumes knowledge not in prerequisites |
| 1-2 | No scaffolding, concepts appear randomly |

**Check for:**
- Prerequisites listed and actually prerequisite
- Concepts introduced before used
- Increasing complexity curve
- Prior knowledge activated before new content

#### 3.4 Pedagogical Layer Appropriateness (1-10)

| Layer | Expected Characteristics |
|-------|-------------------------|
| L1 (Foundation) | Manual-first, understand before automate, no AI shortcuts |
| L2 (Collaboration) | AI as Teacher/Student/Co-Worker, learning through interaction |
| L3 (Intelligence) | Pattern recognition, creating reusable intelligence (skills/subagents) |
| L4 (Orchestration) | Capstone, combining components, spec-driven development |

**Check for:**
- Layer declared in frontmatter
- Content matches layer expectations
- Layer progression through chapter (L1 → L2 → L3 → L4)
- No premature automation (L3 content in early lessons)

#### 3.5 Try With AI Effectiveness (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Prompts directly extend lesson, specific, build skills |
| 7-8 | Good prompts, mostly connected to content |
| 5-6 | Generic prompts, loosely connected |
| 3-4 | Copy-paste prompts, don't match lesson |
| 1-2 | Missing or irrelevant prompts |

**Check for:**
- 2-3 prompts per lesson (not 1, not 5+)
- Prompts reference lesson content specifically
- Progressive difficulty across prompts
- "What's you're learning" explanations present

#### 3.6 Assessment/Verification Quality (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Clear verification at each step, students know if they succeeded |
| 7-8 | Good verification for most exercises |
| 5-6 | Some verification, students may be unsure of success |
| 3-4 | Weak verification, students can't tell if they're on track |
| 1-2 | No verification, students have no idea if they succeeded |

**Check for:**
- "Expected output" shown for commands
- "You should see X" confirmations
- Error states explained
- End-of-lesson checkpoint

## Dimension Criticality & Publication Gate

**CRITICAL**: Not all dimensions are equally important for publication. Use this gate to determine if content is ready.

### Gate Dimensions (MUST BE 7+)

These dimensions BLOCK publication if below 7/10. Fix these first.

| Dimension | Why Critical | Remediation |
|-----------|-------------|------------|
| **Clarity** | If unclear, nothing works. Confused students abandon. | Use `technical-clarity` skill |
| **Scaffolding** | Poor progression breaks learning. Students can't build on prior knowledge. | Use `concept-scaffolding` skill |
| **Layer Appropriateness** | Wrong layer means students lack prerequisites or are under-challenged. | Redesign layer; check prerequisites |

### Important Dimensions (6+)

These should be strong but minor issues are fixable.

| Dimension | Target | Remediation |
|-----------|--------|------------|
| **Engagement** | 6+ | Use `code-example-generator` for better examples |
| **Learning Objectives** | 6+ | Use `learning-objectives` skill |
| **Assessment/Verification** | 6+ | Add verification steps; clarity checks |
| **Cognitive Load** | 6+ | Reduce concepts per lesson; add practice |

### Enhancement Dimensions (5+)

These are nice-to-have; publication doesn't require perfection here.

- Progression Clarity (5+)
- Hands-On Effectiveness (5+)
- Confidence (5+)
- Try With AI Effectiveness (5+)

---

## Publication Decision Logic

Use this decision tree AFTER scoring all dimensions:

```
IF any gate dimension (Clarity, Scaffolding, Layer) < 7:
  → REVISE: Content not ready
  → Fix the failing dimension(s)
  → Re-evaluate

ELSE IF (Engagement < 6) AND (Hands-On < 6):
  → CONDITIONAL PASS: Functional but needs improvement
  → Content is usable; improvements recommended
  → Can publish with revision plan

ELSE IF any important dimension (Objectives, Assessment, Load) < 5:
  → CONDITIONAL PASS: Missing elements but learnable
  → Flag for revision; can publish

ELSE:
  → PASS ✅: Ready for publication
  → All gate dimensions 7+
  → Most important dimensions 6+
```

### Example Decision

**Chapter Evaluation Results:**
- Clarity: 8 ✅
- Scaffolding: 7 ✅
- Layer Appropriateness: 8 ✅
- Engagement: 5 (below ideal)
- Cognitive Load: 7 ✅
- Learning Objectives: 6 ✅
- Assessment: 7 ✅

**Decision**: PASS ✅ — All gate dimensions 7+. Engagement is low, but structure is solid. Recommend: Add more compelling examples in next revision.

---

### Step 4: Gap Analysis

After scoring, identify specific missing elements:

#### Content Gaps
- Missing examples (concept taught but not demonstrated)
- Missing hands-on (theory without practice)
- Missing "why" (what but not why it matters)
- Missing troubleshooting (happy path only)
- Missing transitions (lessons don't connect)

#### Structural Gaps
- Missing opening hook
- Missing running example continuity
- Missing "What's Next" closure
- Missing visual elements (all text, no diagrams/tables)
- Missing code examples for technical content

#### Pedagogical Gaps
- Objectives not assessed
- Cognitive overload unaddressed
- Layer mismatch (content doesn't match declared layer)
- Prerequisites not actually prerequisite
- Try With AI prompts disconnected from content

### Step 5: Generate Improvement Recommendations

For each gap, provide:

1. **Problem**: What's missing or wrong
2. **Impact**: How it affects learning (high/medium/low)
3. **Fix**: Specific action to address
4. **Effort**: Estimated work (low: <30min, medium: 30-90min, high: >90min)
5. **Priority**: 1 (critical), 2 (important), 3 (nice-to-have)

## Output Format

Generate analysis in this structure:

```markdown
# Chapter Evaluation: [Chapter Name]

## Executive Summary

[1 paragraph: Overall quality assessment, key strengths, critical issues, recommendation]

## Student Analysis

### Scores

| Dimension | Score | Verdict |
|-----------|-------|---------|
| Engagement | X/10 | [One-line summary] |
| Length | [Short/Right/Long] | [One-line summary] |
| Clarity | X/10 | [One-line summary] |
| Hands-On | X/10 | [One-line summary] |
| Progression | X/10 | [One-line summary] |
| Confidence | X/10 | [One-line summary] |

**Overall Student Experience**: X/10

### Detailed Findings

[Specific observations per dimension with examples from content]

### Student Pain Points

1. [Specific issue from student perspective]
2. [Specific issue from student perspective]
...

## Teacher Analysis

### Scores

| Dimension | Score | Verdict |
|-----------|-------|---------|
| Learning Objectives | X/10 | [One-line summary] |
| Cognitive Load | X/10 | [One-line summary] |
| Scaffolding | X/10 | [One-line summary] |
| Layer Appropriateness | X/10 | [One-line summary] |
| Try With AI | X/10 | [One-line summary] |
| Assessment | X/10 | [One-line summary] |

**Overall Pedagogical Quality**: X/10

### Detailed Findings

[Specific observations per dimension with examples from content]

### Pedagogical Concerns

1. [Specific issue from teacher perspective]
2. [Specific issue from teacher perspective]
...

## Gap Analysis

### Content Gaps

| Gap | Lesson(s) | Impact |
|-----|-----------|--------|
| [Missing element] | L0X | High/Med/Low |
...

### Structural Gaps

| Gap | Lesson(s) | Impact |
|-----|-----------|--------|
| [Missing element] | L0X | High/Med/Low |
...

### Pedagogical Gaps

| Gap | Lesson(s) | Impact |
|-----|-----------|--------|
| [Missing element] | L0X | High/Med/Low |
...

## Improvement Recommendations

### Priority 1 (Critical)

| # | Problem | Fix | Effort | Lesson(s) |
|---|---------|-----|--------|-----------|
| 1 | [Issue] | [Action] | Low/Med/High | L0X |
...

### Priority 2 (Important)

| # | Problem | Fix | Effort | Lesson(s) |
|---|---------|-----|--------|-----------|
| 1 | [Issue] | [Action] | Low/Med/High | L0X |
...

### Priority 3 (Nice-to-Have)

| # | Problem | Fix | Effort | Lesson(s) |
|---|---------|-----|--------|-----------|
| 1 | [Issue] | [Action] | Low/Med/High | L0X |
...

## Publication Decision

### Gate Status
| Gate | Dimension | Score | Status |
|------|-----------|-------|--------|
| 🚧 BLOCK if <7 | Clarity | X/10 | ✅/❌ |
| 🚧 BLOCK if <7 | Scaffolding | X/10 | ✅/❌ |
| 🚧 BLOCK if <7 | Layer Appropriateness | X/10 | ✅/❌ |

### Publication Verdict
**Status**: [PASS ✅ | CONDITIONAL | REVISE]
**Recommendation**: [Ready for publication | Fix gates first | Needs revision plan]

## Next Steps

If PASS:
- [ ] Ready for publication
- [ ] Note: Optional improvements in Priority 3 section above

If CONDITIONAL:
- [ ] Content is functional
- [ ] Recommended: Address Priority 1 issues in next iteration
- [ ] Can publish now; plan revision cycle

If REVISE:
- [ ] STOP: Fix gate dimensions first
- [ ] [Gate dimension 1]: [Specific action]
- [ ] [Gate dimension 2]: [Specific action]
- [ ] Use remediation skills: [skill-1, skill-2]
- [ ] Re-evaluate after fixes

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Lessons | X |
| Average Word Count | X |
| Student Score | X/10 |
| Teacher Score | X/10 |
| Overall Score | X/10 |
| Gate Pass? | Yes/No |
| Critical Issues | X |
| Estimated Fix Time | X hours |
```

## Quality Reference

Compare evaluated chapters against high-quality reference lessons. The skill should automatically identify and read a reference lesson from Part 1 or Part 6 for comparison when available.

Reference lesson patterns to look for:
- `01-agent-factory-paradigm/01-digital-fte-revolution.md`
- `33-introduction-to-ai-agents/01-what-is-an-ai-agent.md`

## Resources

### references/

See `references/` for detailed rubrics:
- `student-rubric.md` - Detailed student perspective evaluation criteria
- `teacher-rubric.md` - Detailed teacher perspective evaluation criteria
- `word-count-benchmarks.md` - Word count guidelines by lesson type

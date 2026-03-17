---
name: review-multi
description: Comprehensive multi-dimensional skill reviews across structure, content, quality, usability, and integration. Task-based operations with automated validation, manual assessment, scoring rubrics, and improvement recommendations. Use when reviewing skills, ensuring quality, validating production readiness, identifying improvements, or conducting quality assurance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Review-Multi

## Overview

review-multi provides a systematic framework for conducting comprehensive, multi-dimensional reviews of Claude Code skills. It evaluates skills across 5 independent dimensions, combining automated validation with manual assessment to deliver objective quality scores and actionable improvement recommendations.

**Purpose**: Systematic skill quality assurance through multi-dimensional assessment

**The 5 Review Dimensions**:
1. **Structure Review** - YAML frontmatter, file organization, naming conventions, progressive disclosure
2. **Content Review** - Section completeness, clarity, examples, documentation quality
3. **Quality Review** - Pattern compliance, best practices, anti-pattern detection, code quality
4. **Usability Review** - Ease of use, learnability, real-world effectiveness, user satisfaction
5. **Integration Review** - Dependency documentation, data flow, component integration, composition

**Automation Levels**:
- Structure: 95% automated (validate-structure.py)
- Content: 40% automated, 60% manual assessment
- Quality: 50% automated, 50% manual assessment
- Usability: 10% automated, 90% manual testing
- Integration: 30% automated, 70% manual review

**Scoring System**:
- **Scale**: 1-5 per dimension (Excellent/Good/Acceptable/Needs Work/Poor)
- **Overall Score**: Weighted average across dimensions
- **Grade**: A/B/C/D/F mapping
- **Production Readiness**: ≥4.5 ready, 4.0-4.4 ready with improvements, 3.5-3.9 needs work, <3.5 not ready

**Value Proposition**:
- **Objective**: Evidence-based scoring using detailed rubrics (not subjective opinion)
- **Comprehensive**: 5 dimensions cover all quality aspects
- **Efficient**: Automation handles 30-95% of checks depending on dimension
- **Actionable**: Specific, prioritized improvement recommendations
- **Consistent**: Standardized checklists ensure repeatable results
- **Flexible**: 3 review modes (Comprehensive, Fast Check, Custom)

**Key Benefits**:
- Catch 70% of issues with fast automated checks
- Reduce common quality issues by 30% using checklists
- Ensure production readiness before deployment
- Identify improvement opportunities systematically
- Track quality improvements over time
- Establish quality standards across skill ecosystem

## When to Use

Use review-multi when:

1. **Pre-Production Validation** - Review new skills before deploying to production to catch issues early and ensure quality standards

2. **Quality Assurance** - Conduct systematic QA on skills to validate they meet ecosystem standards and user needs

3. **Identifying Improvements** - Discover specific, actionable improvements for existing skills through multi-dimensional assessment

4. **Continuous Improvement** - Regular reviews throughout development lifecycle, not just at end, to maintain quality

5. **Production Readiness Assessment** - Determine if skill is ready for production use with objective scoring and grade mapping

6. **Skill Ecosystem Standards** - Ensure consistency and quality across multiple skills using standardized review framework

7. **Post-Update Validation** - Review skills after major updates to ensure changes don't introduce issues or degrade quality

8. **Learning and Improvement** - Use review findings to learn patterns, improve future skills, and refine development practices

9. **Team Calibration** - Standardize quality assessment across multiple reviewers with objective rubrics

**Don't Use When**:
- Quick syntax checks (use validate-structure.py directly)
- In-progress drafts (wait until reasonably complete)
- Experimental prototypes (not production-bound)

## Prerequisites

**Required**:
- Skill to review (in `.claude/skills/[skill-name]/` format)
- Time allocation based on review mode:
  - Fast Check: 5-10 minutes
  - Single Operation: 15-60 minutes (varies by dimension)
  - Comprehensive Review: 1.5-2.5 hours

**Optional**:
- Python 3.7+ (for automation scripts in Structure and Quality reviews)
- PyYAML library (for YAML frontmatter validation)
- Access to skill-under-review documentation
- Familiarity with Claude Code skill patterns (see `development-workflow/references/common-patterns.md`)

**Skills** (no required dependencies, complementary):
- development-workflow: Use review-multi after skill development
- skill-updater: Apply review-multi recommendations
- testing-validator: Combine with review-multi for full QA

## Scoring System

The review-multi scoring system provides objective, consistent quality assessment across all skill dimensions.

### Per-Dimension Scoring (1-5 Scale)

Each dimension is scored independently using a 1-5 integer scale:

**5 - Excellent** (Exceeds Standards)
- All criteria met perfectly
- Goes beyond minimum requirements
- Exemplary quality that sets the bar
- No issues or concerns identified
- Can serve as example for others

**4 - Good** (Meets Standards)
- Meets all critical criteria
- 1-2 minor, non-critical issues
- Production-ready quality
- Standard expected level
- Small improvements possible

**3 - Acceptable** (Minor Improvements Needed)
- Meets most criteria
- 3-4 issues, some may be critical
- Usable but not optimal
- Several improvements recommended
- Can proceed with noted concerns

**2 - Needs Work** (Notable Issues)
- Missing several criteria
- 5-6 issues, multiple critical
- Not production-ready
- Significant improvements required
- Rework needed before deployment

**1 - Poor** (Significant Problems)
- Fails most criteria
- 7+ issues, fundamentally flawed
- Major quality concerns
- Extensive rework required
- Not viable in current state

### Overall Score Calculation

The overall score is a **weighted average** of the 5 dimension scores:

```
Overall = (Structure × 0.20) + (Content × 0.25) + (Quality × 0.25) +
          (Usability × 0.15) + (Integration × 0.15)
```

**Weight Rationale**:
- **Content & Quality (25% each)**: Core skill value - what it does and how well
- **Structure (20%)**: Important foundation - organization and compliance
- **Usability & Integration (15% each)**: Supporting factors - user experience and composition

**Example Calculations**:
- Scores (5, 4, 4, 3, 4) → Overall = (5×0.20 + 4×0.25 + 4×0.25 + 3×0.15 + 4×0.15) = 4.15 → Grade **B**
- Scores (4, 5, 5, 4, 4) → Overall = (4×0.20 + 5×0.25 + 5×0.25 + 4×0.15 + 4×0.15) = 4.55 → Grade **A**
- Scores (3, 3, 2, 3, 3) → Overall = (3×0.20 + 3×0.25 + 2×0.25 + 3×0.15 + 3×0.15) = 2.85 → Grade **C**

### Grade Mapping

Overall scores map to letter grades:

- **A (4.5-5.0)**: Excellent - Production ready, high quality
- **B (3.5-4.4)**: Good - Ready with minor improvements
- **C (2.5-3.4)**: Acceptable - Needs improvements before production
- **D (1.5-2.4)**: Poor - Requires significant rework
- **F (1.0-1.4)**: Failing - Major issues, not viable

### Production Readiness Assessment

Based on overall score:

- **≥4.5 (Grade A)**: ✅ **Production Ready** - High quality, deploy with confidence
- **4.0-4.4 (Grade B+)**: ✅ **Ready with Minor Improvements** - Can deploy, address improvements in next iteration
- **3.5-3.9 (Grade B-)**: ⚠️ **Needs Improvements** - Address issues before production deployment
- **<3.5 (Grade C-F)**: ❌ **Not Ready** - Significant rework required before deployment

**Decision Framework**:
- **A Grade**: Ship it - exemplary quality
- **B Grade (4.0+)**: Ship it - standard quality, note improvements for future
- **B- Grade (3.5-3.9)**: Hold - fix identified issues first
- **C-F Grade**: Don't ship - substantial work needed

## Operations

### Operation 1: Structure Review

**Purpose**: Validate file organization, naming conventions, YAML frontmatter compliance, and progressive disclosure

**When to Use This Operation**:
- Always run first (fast automated check catches 70% of issues)
- Before comprehensive review (quick validation of basics)
- During development (continuous structure validation)
- Quick quality checks (5-10 minute validation)

**Automation Level**: 95% automated via `scripts/validate-structure.py`

**Process**:
1. **Run Structure Validation Script**
   ```bash
   python3 scripts/validate-structure.py /path/to/skill [--json] [--verbose]
   ```
   Script checks YAML, file structure, naming, progressive disclosure

2. **Review YAML Frontmatter**
   - Verify name field in kebab-case format
   - Check description has 5+ trigger keywords naturally embedded
   - Validate YAML syntax is correct

3. **Verify File Structure**
   - Confirm SKILL.md exists
   - Check references/ and scripts/ organization (if present)
   - Verify README.md exists

4. **Check Naming Conventions**
   - SKILL.md and README.md uppercase
   - references/ files: lowercase-hyphen-case
   - scripts/ files: lowercase-hyphen-case with extension

5. **Validate Progressive Disclosure**
   - SKILL.md <1,500 lines (warn if >1,200)
   - references/ files 300-800 lines each
   - No monolithic files

**Validation Checklist**:
- [ ] YAML frontmatter present and valid syntax
- [ ] `name` field in kebab-case format (e.g., skill-name)
- [ ] `description` includes 5+ trigger keywords (naturally embedded)
- [ ] SKILL.md file exists
- [ ] File naming follows conventions (SKILL.md uppercase, references lowercase-hyphen)
- [ ] Directory structure correct (references/, scripts/ if present)
- [ ] SKILL.md size appropriate (<1,500 lines, ideally <1,200)
- [ ] References organized by topic (if present)
- [ ] No monolithic files (progressive disclosure maintained)
- [ ] README.md present

**Scoring Criteria**:
- **5 - Excellent**: All 10 checks pass, perfect compliance, exemplary structure
- **4 - Good**: 8-9 checks pass, 1-2 minor non-critical issues (e.g., README missing but optional)
- **3 - Acceptable**: 6-7 checks pass, 3-4 issues including some critical (e.g., YAML invalid but fixable)
- **2 - Needs Work**: 4-5 checks pass, 5-6 issues with multiple critical (e.g., no SKILL.md, bad naming)
- **1 - Poor**: ≤3 checks pass, 7+ issues, fundamentally flawed structure

**Outputs**:
- Structure score (1-5)
- Pass/fail status for each checklist item
- List of issues found with severity (critical/warning/info)
- Specific improvement recommendations with fix guidance
- JSON report (if using script with --json flag)

**Time Estimate**: 5-10 minutes (mostly automated)

**Example**:
```bash
$ python3 scripts/validate-structure.py .claude/skills/todo-management

Structure Validation Report
===========================
Skill: todo-management
Date: 2025-11-06

✅ YAML Frontmatter: PASS
   - Name format: valid (kebab-case)
   - Trigger keywords: 8 found (target: 5+)

✅ File Structure: PASS
   - SKILL.md: exists
   - README.md: exists
   - references/: 3 files found
   - scripts/: 1 file found

✅ Naming Conventions: PASS
   - All files follow conventions

⚠️  Progressive Disclosure: WARNING
   - SKILL.md: 569 lines (good)
   - state-management-guide.md: 501 lines (good)
   - BUT: No Quick Reference section detected

Overall Structure Score: 4/5 (Good)
Issues: 1 warning (missing Quick Reference)
Recommendation: Add Quick Reference section to SKILL.md
```

---

### Operation 2: Content Review

**Purpose**: Assess section completeness, content clarity, example quality, and documentation comprehensiveness

**When to Use This Operation**:
- Evaluate documentation quality
- Assess completeness of skill content
- Review example quality and quantity
- Validate information architecture
- Check clarity and organization

**Automation Level**: 40% automated (section detection, example counting), 60% manual assessment

**Process**:
1. **Check Section Completeness** (automated + manual)
   - Verify 5 core sections present: Overview, When to Use, Main Content (workflow/operations), Best Practices, Quick Reference
   - Check optional sections: Prerequisites, Common Mistakes, Troubleshooting
   - Assess if all necessary sections included

2. **Assess Content Clarity** (manual)
   - Is content understandable?
   - Is organization logical?
   - Are explanations clear without being verbose?
   - Is technical level appropriate for audience?

3. **Evaluate Example Quality** (automated count + manual quality)
   - Count code/command examples (target: 5+)
   - Check if examples are concrete (not abstract placeholders)
   - Verify examples are executable/copy-pasteable
   - Assess if examples help understanding

4. **Review Documentation Completeness** (manual)
   - Is all necessary information present?
   - Are there unexplained gaps?
   - Is sufficient detail provided?
   - Are edge cases covered?

5. **Check Explanation Depth** (manual)
   - Not too brief (insufficient detail)?
   - Not too verbose (unnecessary length)?
   - Balanced depth for complexity?

**Validation Checklist**:
- [ ] Overview/Introduction section present
- [ ] When to Use section present with 5+ scenarios
- [ ] Main content (workflow steps OR operations OR reference material) complete
- [ ] Best Practices section present
- [ ] Quick Reference section present
- [ ] 5+ code/command examples included
- [ ] Examples are concrete (not abstract placeholders like "YOUR_VALUE_HERE")
- [ ] Content clarity: readable and well-structured
- [ ] Sufficient detail: not too brief
- [ ] Not too verbose: concise without unnecessary length

**Scoring Criteria**:
- **5 - Excellent**: All 10 checks pass, exceptional clarity, great examples, comprehensive documentation
- **4 - Good**: 8-9 checks pass, good content with minor gaps or clarity issues
- **3 - Acceptable**: 6-7 checks pass, some sections weak or missing, acceptable clarity
- **2 - Needs Work**: 4-5 checks pass, multiple sections incomplete/unclear, poor examples
- **1 - Poor**: ≤3 checks pass, major gaps, confusing content, few/no examples

**Outputs**:
- Content score (1-5)
- Section-by-section assessment (present/missing/weak)
- Example quality rating and count
- Specific content improvement recommendations
- Clarity issues identified with examples

**Time Estimate**: 15-30 minutes (requires manual review)

**Example**:
```
Content Review: prompt-builder
==============================

Section Completeness: 9/10 ✅
✅ Overview: Present, clear explanation of purpose
✅ When to Use: 7 scenarios listed
✅ Main Content: 5-step workflow, well-organized
✅ Best Practices: 6 practices documented
✅ Quick Reference: Present
⚠️  Common Mistakes: Not present (optional but valuable)

Example Quality: 8/10 ✅
- Count: 12 examples (exceeds target of 5+)
- Concrete: Yes, all examples executable
- Helpful: Yes, demonstrate key concepts
- Minor: Could use 1-2 edge case examples

Content Clarity: 9/10 ✅
- Well-organized logical flow
- Clear explanations without verbosity
- Technical level appropriate
- Minor: Step 3 could be clearer (add diagram)

Documentation Completeness: 8/10 ✅
- All workflow steps documented
- Validation criteria clear
- Minor gaps: Error handling not covered

Content Score: 4/5 (Good)
Primary Recommendation: Add Common Mistakes section
Secondary: Add error handling guidance to Step 3
```

---

### Operation 3: Quality Review

**Purpose**: Evaluate pattern compliance, best practices adherence, anti-pattern detection, and code/script quality

**When to Use This Operation**:
- Validate standards compliance
- Check pattern implementation
- Detect anti-patterns
- Assess code quality (if scripts present)
- Ensure best practices followed

**Automation Level**: 50% automated (pattern detection, anti-pattern checking), 50% manual assessment

**Process**:
1. **Detect Architecture Pattern** (automated + manual)
   - Identify pattern type: workflow/task/reference/capabilities
   - Verify pattern correctly implemented
   - Check pattern consistency throughout skill

2. **Validate Documentation Patterns** (automated + manual)
   - Verify 5 core sections present
   - Check consistent structure across steps/operations
   - Validate section formatting

3. **Check Best Practices** (manual)
   - Validation checklists present and specific?
   - Examples throughout documentation?
   - Quick Reference available?
   - Error cases considered?

4. **Detect Anti-Patterns** (automated + manual)
   - Keyword stuffing (trigger keywords unnatural)?
   - Monolithic SKILL.md (>1,500 lines, no progressive disclosure)?
   - Inconsistent structure (each section different format)?
   - Vague validation ("everything works")?
   - Missing examples (too abstract)?
   - Placeholders in production ("YOUR_VALUE_HERE")?
   - Ignoring error cases (only happy path)?
   - Over-engineering simple skills?
   - Unclear dependencies?
   - No Quick Reference?

5. **Assess Code Quality** (manual, if scripts present)
   - Scripts well-documented (docstrings)?
   - Error handling present?
   - CLI interfaces clear?
   - Code style consistent?

**Validation Checklist**:
- [ ] Architecture pattern correctly implemented (workflow/task/reference/capabilities)
- [ ] Consistent structure across steps/operations (same format throughout)
- [ ] Validation checklists present and specific (measurable, not vague)
- [ ] Best practices section actionable (specific guidance)
- [ ] No keyword stuffing (trigger keywords natural, contextual)
- [ ] No monolithic SKILL.md (progressive disclosure used if >1,000 lines)
- [ ] Examples are complete (no "YOUR_VALUE_HERE" placeholders in production)
- [ ] Error cases considered (not just happy path documented)
- [ ] Dependencies documented (if skill requires other skills)
- [ ] Scripts well-documented (if present: docstrings, error handling, CLI help)

**Scoring Criteria**:
- **5 - Excellent**: All 10 checks pass, exemplary quality, no anti-patterns, exceeds standards
- **4 - Good**: 8-9 checks pass, high quality, meets all standards, minor deviations
- **3 - Acceptable**: 6-7 checks pass, acceptable quality, some standard violations, 2-3 anti-patterns
- **2 - Needs Work**: 4-5 checks pass, quality issues, multiple standard violations, 4-5 anti-patterns
- **1 - Poor**: ≤3 checks pass, poor quality, significant problems, 6+ anti-patterns detected

**Outputs**:
- Quality score (1-5)
- Pattern compliance assessment (pattern detected, compliance level)
- Anti-patterns detected (list with severity)
- Best practices gaps identified
- Code quality assessment (if scripts present)
- Prioritized improvement recommendations

**Time Estimate**: 20-40 minutes (mixed automated + manual)

**Example**:
```
Quality Review: workflow-skill-creator
======================================

Pattern Compliance: ✅
- Pattern Detected: Workflow-based
- Implementation: Correct (5 sequential steps with dependencies)
- Consistency: High (all steps follow same structure)

Documentation Patterns: ✅
- 5 Core Sections: All present
- Structure: Consistent across all 5 steps
- Formatting: Proper heading levels

Best Practices Adherence: 8/10 ✅
✅ Validation checklists: Present and specific
✅ Examples throughout: 6 examples included
✅ Quick Reference: Present
⚠️ Error handling: Limited (only happy path in examples)

Anti-Pattern Detection: 1 detected ⚠️
✅ No keyword stuffing (15 natural keywords)
✅ No monolithic file (1,465 lines but has references/)
✅ Consistent structure
✅ Specific validation criteria
✅ Examples complete (no placeholders)
⚠️ Error cases: Only happy path documented
✅ Dependencies: Clearly documented
✅ Not over-engineered

Code Quality: N/A (no scripts)

Quality Score: 4/5 (Good)
Primary Issue: Limited error handling documentation
Recommendation: Add error case examples and recovery guidance
```

---

### Operation 4: Usability Review

**Purpose**: Evaluate ease of use, learnability, real-world effectiveness, and user satisfaction through scenario testing

**When to Use This Operation**:
- Test real-world usage
- Assess user experience
- Evaluate learnability
- Measure effectiveness
- Validate skill achieves stated purpose

**Automation Level**: 10% automated (basic checks), 90% manual testing

**Process**:
1. **Test in Real-World Scenario**
   - Select appropriate use case from "When to Use" section
   - Actually use the skill to complete task
   - Document experience: smooth or friction?
   - Note any confusion or difficulty

2. **Assess Navigation/Findability**
   - Can you find needed information easily?
   - Is information architecture logical?
   - Are sections well-organized?
   - Is Quick Reference helpful?

3. **Evaluate Clarity**
   - Are instructions clear and actionable?
   - Are steps easy to follow?
   - Do examples help understanding?
   - Is technical terminology explained?

4. **Measure Effectiveness**
   - Does skill achieve stated purpose?
   - Does it deliver promised value?
   - Are outputs useful and complete?
   - Would you use it again?

5. **Assess Learning Curve**
   - How long to understand skill?
   - How long to use effectively?
   - Is learning curve reasonable for complexity?
   - Are first-time users supported well?

**Validation Checklist**:
- [ ] Skill tested in real-world scenario (actual usage, not just reading)
- [ ] Users can find information easily (navigation clear, sections logical)
- [ ] Instructions are clear and actionable (can follow without confusion)
- [ ] Examples help understanding (concrete, demonstrate key concepts)
- [ ] Skill achieves stated purpose (delivers promised value)
- [ ] Learning curve reasonable (appropriate for skill complexity)
- [ ] Error messages helpful (if applicable: clear, actionable guidance)
- [ ] Overall user satisfaction high (would use again, recommend to others)

**Scoring Criteria**:
- **5 - Excellent**: All 8 checks pass, excellent usability, easy to learn, highly effective, very satisfying
- **4 - Good**: 6-7 checks pass, good usability, minor friction points, generally effective
- **3 - Acceptable**: 4-5 checks pass, acceptable usability, some confusion/difficulty, moderately effective
- **2 - Needs Work**: 2-3 checks pass, usability issues, frustrating or confusing, limited effectiveness
- **1 - Poor**: ≤1 check passes, poor usability, hard to use, ineffective, unsatisfying

**Outputs**:
- Usability score (1-5)
- Scenario test results (success/partial/failure)
- User experience assessment (smooth/acceptable/frustrating)
- Specific usability improvements identified
- Learning curve assessment
- Effectiveness rating

**Time Estimate**: 30-60 minutes (requires actual testing)

**Example**:
```
Usability Review: skill-researcher
==================================

Real-World Scenario Test: ✅
- Scenario: Research GitHub API integration patterns
- Result: SUCCESS - Found 5 relevant sources, synthesized findings
- Experience: Smooth, operations clearly explained
- Time: 45 minutes (expected 60 min range)

Navigation/Findability: 9/10 ✅
- Information easy to find
- 5 operations clearly separated
- Quick Reference table very helpful
- Minor: Could use table of contents for long doc

Instruction Clarity: 9/10 ✅
- Steps clear and actionable
- Process well-explained
- Examples demonstrate concepts
- Minor: Web search query formulation could be clearer

Effectiveness: 10/10 ✅
- Achieved purpose: Found patterns and synthesized
- Delivered value: Comprehensive research in 45 min
- Would use again: Yes, very helpful

Learning Curve: 8/10 ✅
- Time to understand: 10 minutes
- Time to use effectively: 15 minutes
- Reasonable for complexity
- First-time user: Some concepts need explanation (credibility scoring)

Error Handling: N/A (no errors encountered)

User Satisfaction: 9/10 ✅
- Would use again: Yes
- Would recommend: Yes
- Overall experience: Very positive

Usability Score: 5/5 (Excellent)
Minor Improvement: Add brief explanation of credibility scoring concept
```

---

### Operation 5: Integration Review

**Purpose**: Assess dependency documentation, data flow clarity, component integration, and composition patterns

**When to Use This Operation**:
- Review workflow skills (that compose other skills)
- Validate dependency documentation
- Check integration clarity
- Assess composition patterns
- Verify cross-references valid

**Automation Level**: 30% automated (dependency checking, cross-reference validation), 70% manual assessment

**Process**:
1. **Review Dependency Documentation** (manual)
   - Are required skills documented?
   - Are optional/complementary skills mentioned?
   - Is YAML `dependencies` field used (if applicable)?
   - Are dependency versions noted (if relevant)?

2. **Assess Data Flow Clarity** (manual, for workflow skills)
   - Is data flow between skills explained?
   - Are inputs/outputs documented for each step?
   - Do users understand how data moves?
   - Are there diagrams or flowcharts (if helpful)?

3. **Evaluate Component Integration** (manual)
   - How do component skills work together?
   - Are integration points clear?
   - Are there integration examples?
   - Is composition pattern documented?

4. **Verify Cross-References** (automated + manual)
   - Do internal links work (references to references/, scripts/)?
   - Are external skill references correct?
   - Are complementary skills mentioned?

5. **Check Composition Patterns** (manual, for workflow skills)
   - Is composition pattern identified (sequential/parallel/conditional/etc.)?
   - Is pattern correctly implemented?
   - Are orchestration details provided?

**Validation Checklist**:
- [ ] Dependencies documented (if skill requires other skills)
- [ ] YAML `dependencies` field correct (if used)
- [ ] Data flow explained (for workflow skills: inputs/outputs clear)
- [ ] Integration points clear (how component skills connect)
- [ ] Component skills referenced correctly (names accurate, paths valid)
- [ ] Cross-references valid (internal links work, external references correct)
- [ ] Integration examples provided (if applicable: how to use together)
- [ ] Composition pattern documented (if workflow: sequential/parallel/etc.)
- [ ] Complementary skills mentioned (optional but valuable related skills)

**Scoring Criteria**:
- **5 - Excellent**: All 9 checks pass (applicable ones), perfect integration documentation
- **4 - Good**: 7-8 checks pass, good integration, minor gaps in documentation
- **3 - Acceptable**: 5-6 checks pass, some integration unclear, missing details
- **2 - Needs Work**: 3-4 checks pass, integration issues, poorly documented dependencies/flow
- **1 - Poor**: ≤2 checks pass, poor integration, confusing or missing dependency documentation

**Outputs**:
- Integration score (1-5)
- Dependency validation results (required/optional/complementary documented)
- Data flow clarity assessment (for workflow skills)
- Integration clarity rating
- Cross-reference validation results
- Improvement recommendations

**Time Estimate**: 15-25 minutes (mostly manual)

**Example**:
```
Integration Review: development-workflow
========================================

Dependency Documentation: 10/10 ✅
- Required Skills: None (workflow is standalone)
- Component Skills: 5 clearly documented (skill-researcher, planning-architect, task-development, prompt-builder, todo-management)
- Optional Skills: 3 complementary skills mentioned (review-multi, skill-updater, testing-validator)
- YAML Field: Not used (not required, skills referenced in content)

Data Flow Clarity: 10/10 ✅ (Workflow Skill)
- Data flow diagram present (skill → output → next skill)
- Inputs/outputs for each step documented
- Users understand how artifacts flow
- Example:
  ```
  skill-researcher → research-synthesis.md → planning-architect
                                         ↓
                              skill-architecture-plan.md → task-development
  ```

Component Integration: 10/10 ✅
- Integration method documented for each step (Guided Execution)
- Integration examples provided
- Clear explanation of how skills work together
- Process for using each component skill detailed

Cross-Reference Validation: ✅
- Internal links valid (references/ files exist and reachable)
- External skill references correct (all 5 component skills exist)
- Complementary skills mentioned appropriately

Composition Pattern: 10/10 ✅ (Workflow Skill)
- Pattern: Sequential Pipeline (with one optional step)
- Correctly implemented (Step 1 → 2 → [3 optional] → 4 → 5)
- Orchestration details provided
- Clear flow diagram

Integration Score: 5/5 (Excellent)
Notes: Exemplary integration documentation for workflow skill
```

---

## Review Modes

### Comprehensive Review Mode

**Purpose**: Complete multi-dimensional assessment across all 5 dimensions with aggregate scoring

**When to Use**:
- Pre-production validation (ensure skill ready for deployment)
- Major skill updates (validate changes don't degrade quality)
- Quality certification (establish baseline quality score)
- Periodic quality audits (track quality over time)

**Process**:
1. **Run All 5 Operations Sequentially**
   - Operation 1: Structure Review (5-10 min, automated)
   - Operation 2: Content Review (15-30 min, manual)
   - Operation 3: Quality Review (20-40 min, mixed)
   - Operation 4: Usability Review (30-60 min, manual)
   - Operation 5: Integration Review (15-25 min, manual)

2. **Aggregate Scores**
   - Record score (1-5) for each dimension
   - Calculate weighted overall score using formula
   - Map overall score to grade (A/B/C/D/F)

3. **Assess Production Readiness**
   - ≥4.5: Production Ready
   - 4.0-4.4: Ready with minor improvements
   - 3.5-3.9: Needs improvements before production
   - <3.5: Not ready, significant rework required

4. **Compile Improvement Recommendations**
   - Aggregate issues from all dimensions
   - Prioritize: Critical → High → Medium → Low
   - Provide specific, actionable fixes

5. **Generate Comprehensive Report**
   - Executive summary (overall score, grade, readiness)
   - Per-dimension scores and findings
   - Prioritized improvement list
   - Detailed rationale for scores

**Output**:
- Overall score (1.0-5.0 with one decimal)
- Grade (A/B/C/D/F)
- Production readiness assessment
- Per-dimension scores (Structure, Content, Quality, Usability, Integration)
- Comprehensive improvement recommendations (prioritized)
- Detailed review report

**Time Estimate**: 1.5-2.5 hours total

**Example Output**:
```
Comprehensive Review Report: skill-researcher
=============================================

OVERALL SCORE: 4.6/5.0 - GRADE A
STATUS: ✅ PRODUCTION READY

Dimension Scores:
- Structure:   5/5 (Excellent) - Perfect file organization
- Content:     5/5 (Excellent) - Comprehensive, clear documentation
- Quality:     4/5 (Good) - High quality, minor error handling gaps
- Usability:   5/5 (Excellent) - Easy to use, highly effective
- Integration: 4/5 (Good) - Well-documented dependencies

Production Readiness: READY - High quality, deploy with confidence

Recommendations (Priority Order):
1. [Medium] Add error handling examples for web search failures
2. [Low] Consider adding table of contents for long SKILL.md

Strengths:
- Excellent structure and organization
- Comprehensive coverage of 5 research operations
- Strong usability with clear instructions
- Good examples throughout

Overall: Exemplary skill, production-ready quality
```

---

### Fast Check Mode

**Purpose**: Quick automated validation for rapid quality feedback during development

**When to Use**:
- During development (continuous validation)
- Quick quality checks (before detailed review)
- Pre-commit validation (catch issues early)
- Rapid iteration (fast feedback loop)

**Process**:
1. **Run Automated Structure Validation**
   ```bash
   python3 scripts/validate-structure.py /path/to/skill
   ```

2. **Check Critical Issues**
   - YAML frontmatter valid?
   - Required files present?
   - Naming conventions followed?
   - File sizes appropriate?

3. **Generate Pass/Fail Report**
   - PASS: Critical checks passed, proceed to development
   - FAIL: Critical issues found, fix before continuing

4. **Provide Quick Fixes** (if available)
   - Specific commands to fix issues
   - Examples of correct format
   - References to documentation

**Output**:
- Pass/Fail status
- Critical issues list (if failed)
- Quick fixes or guidance
- Score estimate (if passed)

**Time Estimate**: 5-10 minutes

**Example Output**:
```bash
$ python3 scripts/validate-structure.py .claude/skills/my-skill

Fast Check Report
=================
Skill: my-skill

❌ FAIL - Critical Issues Found

Critical Issues:
1. YAML frontmatter: Invalid syntax (line 3: unexpected character)
2. Naming convention: File "MyGuide.md" should be "my-guide.md"

Quick Fixes:
1. Fix YAML: Remove trailing comma on line 3
2. Rename file: mv references/MyGuide.md references/my-guide.md

Run full validation after fixes: python3 scripts/validate-structure.py .claude/skills/my-skill
```

---

### Custom Review

**Purpose**: Flexible review focusing on specific dimensions or concerns

**When to Use**:
- Targeted improvements (focus on specific dimension)
- Time constraints (can't do comprehensive review)
- Specific concerns (e.g., only check usability)
- Iterative improvements (focus on one dimension at a time)

**Options**:
1. **Select Dimensions**: Choose 1-5 operations to run
2. **Adjust Thoroughness**: Quick/Standard/Thorough per dimension
3. **Focus Areas**: Specify particular concerns (e.g., "check examples quality")

**Process**:
1. **Define Custom Review Scope**
   - Which dimensions to review?
   - How thorough for each?
   - Any specific focus areas?

2. **Run Selected Operations**
   - Execute chosen operations
   - Apply thoroughness level

3. **Generate Targeted Report**
   - Scores for selected dimensions only
   - Focused findings
   - Specific recommendations

**Example Scenarios**:

**Scenario 1: Content-Focused Review**
```
Custom Review: Content + Examples
- Operations: Content Review only
- Thoroughness: Thorough
- Focus: Example quality and completeness
- Time: 30 minutes
```

**Scenario 2: Quick Quality Check**
```
Custom Review: Structure + Quality (Fast)
- Operations: Structure + Quality
- Thoroughness: Quick
- Focus: Pattern compliance, anti-patterns
- Time: 15-20 minutes
```

**Scenario 3: Workflow Integration Review**
```
Custom Review: Integration Deep Dive
- Operations: Integration Review only
- Thoroughness: Thorough
- Focus: Data flow, composition patterns
- Time: 30 minutes
```

---

## Best Practices

### 1. Self-Review First
**Practice**: Run Fast Check mode before requesting comprehensive review

**Rationale**: Automated checks catch 70% of structural issues in 5-10 minutes, allowing manual review to focus on higher-value assessment

**Application**: Always run `validate-structure.py` before detailed review

### 2. Use Checklists Systematically
**Practice**: Follow validation checklists item-by-item for each operation

**Rationale**: Research shows teams using checklists reduce common issues by 30% and ensure consistent results

**Application**: Print or display checklist, mark each item explicitly

### 3. Test in Real Scenarios
**Practice**: Conduct usability review with actual usage, not just documentation reading

**Rationale**: Real-world testing reveals hidden usability issues that documentation review misses

**Application**: For Usability Review, actually use the skill to complete a realistic task

### 4. Focus on Automation
**Practice**: Let scripts handle routine checks, focus manual effort on judgment-requiring assessment

**Rationale**: Automation provides 70% reduction in manual review time for routine checks

**Application**: Use scripts for Structure and partial Quality checks, manual for Content/Usability

### 5. Provide Actionable Feedback
**Practice**: Make improvement recommendations specific, prioritized, and actionable

**Rationale**: Vague feedback ("improve quality") is less valuable than specific guidance ("add error handling examples to Step 3")

**Application**: For each issue, specify: What, Why, How (to fix), Priority

### 6. Review Regularly
**Practice**: Conduct reviews throughout development lifecycle, not just at end

**Rationale**: Early reviews catch issues before they compound; rapid feedback maintains momentum (37% productivity increase)

**Application**: Fast Check during development, Comprehensive Review before production

### 7. Track Improvements
**Practice**: Document before/after scores to measure improvement over time

**Rationale**: Tracking demonstrates progress, identifies patterns, validates improvements

**Application**: Save review reports, compare scores across iterations

### 8. Iterate Based on Findings
**Practice**: Use review findings to improve future skills, not just current skill

**Rationale**: Learnings compound; patterns identified in reviews improve entire skill ecosystem

**Application**: Document common issues, create guidelines, update templates

---

## Common Mistakes

### Mistake 1: Skipping Structure Review
**Symptom**: Spending time on detailed review only to discover fundamental structural issues

**Cause**: Assumption that structure is correct, eagerness to assess content

**Fix**: Always run Structure Review (Fast Check) first - takes 5-10 minutes, catches 70% of issues

**Prevention**: Make Fast Check mandatory first step in any review process

### Mistake 2: Subjective Scoring
**Symptom**: Inconsistent scores, debate over ratings, difficulty justifying scores

**Cause**: Using personal opinion instead of rubric criteria

**Fix**: Use `references/scoring-rubric.md` - score based on specific criteria, not feeling

**Prevention**: Print rubric, refer to criteria for each score, document evidence

### Mistake 3: Ignoring Usability
**Symptom**: Skill looks good on paper but difficult to use in practice

**Cause**: Skipping Usability Review (90% manual, time-consuming)

**Fix**: Actually test skill in real scenario - reveals hidden issues

**Prevention**: Allocate 30-60 minutes for usability testing, cannot skip for production

### Mistake 4: No Prioritization
**Symptom**: Long list of improvements, unclear what to fix first, overwhelmed

**Cause**: Treating all issues equally without assessing impact

**Fix**: Prioritize issues: Critical (must fix) → High → Medium → Low (nice to have)

**Prevention**: Tag each issue with priority level during review

### Mistake 5: Batch Reviews
**Symptom**: Discovering major issues late in development, costly rework

**Cause**: Waiting until end to review, accumulating issues

**Fix**: Review early and often - Fast Check during development, iterations

**Prevention**: Continuous validation, rapid feedback, catch issues when small

### Mistake 6: Ignoring Patterns
**Symptom**: Repeating same issues across multiple skills

**Cause**: Treating each review in isolation, not learning from patterns

**Fix**: Track common issues, create guidelines, update development process

**Prevention**: Document patterns, share learnings, improve templates

---

## Quick Reference

### The 5 Operations

| Operation | Focus | Automation | Time | Key Output |
|-----------|-------|------------|------|------------|
| **Structure** | YAML, files, naming, organization | 95% | 5-10m | Structure score, compliance report |
| **Content** | Completeness, clarity, examples | 40% | 15-30m | Content score, section assessment |
| **Quality** | Patterns, best practices, anti-patterns | 50% | 20-40m | Quality score, pattern compliance |
| **Usability** | Ease of use, effectiveness | 10% | 30-60m | Usability score, scenario test results |
| **Integration** | Dependencies, data flow, composition | 30% | 15-25m | Integration score, dependency validation |

### Scoring Scale

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| **5** | Excellent | Exceeds standards | Exemplary - use as example |
| **4** | Good | Meets standards | Production ready - standard quality |
| **3** | Acceptable | Minor improvements | Usable - note improvements |
| **2** | Needs Work | Notable issues | Not ready - significant improvements |
| **1** | Poor | Significant problems | Not viable - extensive rework |

### Production Readiness

| Overall Score | Grade | Status | Decision |
|---------------|-------|--------|----------|
| **4.5-5.0** | A | ✅ Production Ready | Ship it - high quality |
| **4.0-4.4** | B+ | ✅ Ready (minor improvements) | Ship - note improvements for next iteration |
| **3.5-3.9** | B- | ⚠️ Needs Improvements | Hold - fix issues first |
| **2.5-3.4** | C | ❌ Not Ready | Don't ship - substantial work needed |
| **1.5-2.4** | D | ❌ Not Ready | Don't ship - significant rework |
| **1.0-1.4** | F | ❌ Not Ready | Don't ship - major issues |

### Review Modes

| Mode | Time | Use Case | Coverage |
|------|------|----------|----------|
| **Fast Check** | 5-10m | During development, quick validation | Structure only (automated) |
| **Custom** | Variable | Targeted review, specific concerns | Selected dimensions |
| **Comprehensive** | 1.5-2.5h | Pre-production, full assessment | All 5 dimensions + report |

### Common Commands

```bash
# Fast structure validation
python3 scripts/validate-structure.py /path/to/skill

# Verbose output
python3 scripts/validate-structure.py /path/to/skill --verbose

# JSON output
python3 scripts/validate-structure.py /path/to/skill --json

# Pattern compliance check
python3 scripts/check-patterns.py /path/to/skill

# Generate review report
python3 scripts/generate-review-report.py review_data.json --output report.md

# Run comprehensive review
python3 scripts/review-runner.py /path/to/skill --mode comprehensive
```

### Weighted Average Formula

```
Overall = (Structure × 0.20) + (Content × 0.25) + (Quality × 0.25) +
          (Usability × 0.15) + (Integration × 0.15)
```

**Weight Rationale**:
- Content & Quality (25% each): Core value
- Structure (20%): Foundation
- Usability & Integration (15% each): Supporting

### For More Information

- **Structure details**: `references/structure-review-guide.md`
- **Content details**: `references/content-review-guide.md`
- **Quality details**: `references/quality-review-guide.md`
- **Usability details**: `references/usability-review-guide.md`
- **Integration details**: `references/integration-review-guide.md`
- **Complete scoring rubrics**: `references/scoring-rubric.md`
- **Report templates**: `references/review-report-template.md`

---

**For detailed guidance on each dimension, see reference files. For automation tools, see scripts/.**

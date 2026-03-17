---
name: curriculum-iterate-feedback
description: Synthesize feedback from students, outcomes data, and peer reviews to generate prioritized curriculum revision recommendations and track effectiveness over versions. Use when revising curriculum, analyzing feedback, or continuous improvement. Activates on "improve curriculum", "analyze feedback", "revision recommendations", or "iterate on content".
---

# Feedback Analysis & Revision Recommendations

Synthesize multiple feedback sources to identify high-impact curriculum improvements with implementation guidance and version tracking.

## When to Use

- Analyze student feedback
- Review outcome data for patterns
- Synthesize improvement opportunities
- Plan curriculum revisions
- Track version effectiveness

## Required Inputs

- **Feedback Sources**: Student surveys, peer reviews, outcome data
- **Current Curriculum**: Materials to potentially revise
- **Historical Data** (optional): Previous version effectiveness
- **Context**: Constraints, resources, timeline

## Workflow

### 1. Gather All Feedback Sources

Collect:
- **Student Feedback**: Surveys, course evaluations, informal comments
- **Outcome Data**: From `/curriculum.analyze-outcomes`
- **Peer Review**: Other educator observations
- **Self-Reflection**: Instructor notes, observations
- **Stakeholder Input**: Admin, parents, industry partners

### 2. Synthesize Feedback by Theme

```markdown
# Feedback Synthesis: [COURSE/UNIT]

**Review Period**: [Date Range]
**Feedback Sources**: [List]
**Current Version**: [Version number]

## Feedback Themes

### Theme 1: Content Pacing Too Fast

**Sources**:
- Student surveys: 18/30 students (60%) reported feeling rushed
- Outcome data: Unit 2 objectives only 45% mastery (lowest in course)
- Instructor observation: "Struggled to finish Unit 2 in time"

**Specific Comments**:
- "We moved through Unit 2 so quickly I didn't understand photosynthesis before the test."
- "Need more practice time before assessments."
- "Felt like we skipped over important concepts."

**Evidence Strength**: ⭐⭐⭐⭐⭐ (Strong - multiple convergent sources)

**Impact Assessment**: HIGH - Directly affects learning outcomes

### Theme 2: Lack of Real-World Applications

**Sources**:
- Student feedback: "Why does this matter?"
- Peer review: "Could benefit from authentic tasks"

**Specific Comments**:
- "I don't understand why we need to know this."
- "When will I use this in real life?"

**Evidence Strength**: ⭐⭐⭐ (Moderate - consistent but limited sources)

**Impact Assessment**: MEDIUM - Affects engagement and transfer

### Theme 3: Assessment Too Memorization-Heavy

**Sources**:
- Student feedback: "Just memorize and forget"
- Outcome data: High Remember-level performance (85%) but low Apply-level (58%)
- Bloom's analysis: 70% of items at Remember/Understand level

**Specific Comments**:
- "Tests are all memorization, not understanding."
- "I got an A but still don't really get it."

**Evidence Strength**: ⭐⭐⭐⭐ (Strong - multiple objective sources)

**Impact Assessment**: HIGH - Shallow learning, not meeting objectives

[Continue for all themes identified]
```

### 3. Identify Root Causes

For each theme, analyze WHY:

```markdown
## Root Cause Analysis: Pacing Too Fast

**Symptoms**:
- Low mastery rates in Unit 2
- Student complaints about speed
- Not enough practice time

**Possible Causes**:
1. ✅ **Too much content in Unit 2** (5 objectives in 2 weeks)
   - Evidence: Unit 1 had 3 objectives in 2 weeks (80% mastery)
   - Evidence: Unit 3 had 4 objectives in 3 weeks (70% mastery)
2. ✅ **Insufficient scaffolding**
   - Evidence: Direct transition from simple to complex concepts
   - Evidence: No intermediate practice activities
3. ⚠️  **Prerequisites not mastered** (possible but less clear)
   - Evidence: Unit 1 had good mastery (80%), so prerequisites likely OK
4. ❌ **Ineffective instruction** (unlikely)
   - Evidence: Other units performing adequately with same methods

**Most Likely Root Causes**:
1. Content overload (5 objectives too many for 2 weeks)
2. Insufficient scaffolding and practice

**Recommended Fixes**:
1. Split Unit 2 into two 2-week units (2.A and 2.B)
2. Add intermediate practice activities between concepts
3. Include more worked examples and guided practice
```

### 4. Generate Prioritized Recommendations

```markdown
# Curriculum Revision Recommendations

**Course**: [Name]
**Current Version**: 1.0
**Next Version**: 1.1 (or 2.0 if major changes)
**Recommendation Date**: [Date]

## Priority 1: Critical Revisions (Must Do)

### Recommendation 1.1: Extend Unit 2 Timeline

**Issue**: Content pacing too fast in Unit 2, leading to low mastery (45%)

**Root Cause**: 5 objectives in 2 weeks is too much content

**Proposed Change**: Split Unit 2 into two units:
- Unit 2A: LO-2.1, LO-2.2 (2 weeks)
- Unit 2B: LO-2.3, LO-2.4, LO-2.5 (2 weeks)

**Expected Impact**:
- Increase mastery rate from 45% to target 70%
- Reduce student stress and rushing
- Allow adequate practice time

**Implementation Effort**: MEDIUM
- Restructure 2 lessons
- Adjust pacing guide
- Create new formative assessment

**Implementation Timeline**: 2 weeks before next course iteration

**Success Metrics**:
- Unit 2A mastery ≥70%
- Unit 2B mastery ≥70%
- Student feedback: <30% report feeling rushed

### Recommendation 1.2: Increase Higher-Order Assessments

**Issue**: Too much emphasis on memorization (70% Remember/Understand items)

**Root Cause**: Assessment items don't match Apply/Analyze objectives

**Proposed Change**: Revise assessment blueprint:
- Reduce Remember items from 14 to 7
- Increase Apply items from 5 to 10
- Add 3 Analyze items

**Expected Impact**:
- Better measure of true understanding
- Force deeper learning (not just memorization)
- Align assessment to stated objectives

**Implementation Effort**: HIGH
- Rewrite 10-15 assessment items
- Update rubrics
- Field test new items

**Implementation Timeline**: 4 weeks

**Success Metrics**:
- Apply-level performance ≥70% (currently 58%)
- Student feedback: <20% report "just memorization"

## Priority 2: Important Improvements (Should Do)

### Recommendation 2.1: Add Real-World Applications

[Same structure: Issue, Root Cause, Proposed Change, Impact, Effort, Timeline, Metrics]

### Recommendation 2.2: Enhance Visual Supports

[Same structure]

## Priority 3: Nice-to-Have Enhancements

### Recommendation 3.1: Add Student Choice Options

[Same structure]

## Implementation Plan

### Phase 1: Critical Fixes (Weeks 1-4)
- [ ] Week 1-2: Split Unit 2, restructure
- [ ] Week 3-4: Revise assessment items

### Phase 2: Important Improvements (Weeks 5-8)
- [ ] Week 5-6: Add real-world applications
- [ ] Week 7-8: Create visual supports

### Phase 3: Enhancements (Weeks 9-12)
- [ ] Week 9-12: Implement choice options

### Resources Needed

- **Time**: 40 hours total (10 hrs/week × 4 weeks)
- **Expertise**: Assessment design consultant for item revision
- **Materials**: $200 for new visual creation tools
- **Testing**: 30 students for field testing items

## Version Tracking

**Version 1.0** (Current):
- Created: Fall 2024
- Student Count: 30
- Average Performance: 72%
- Objective Mastery: 12/18 objectives (67%)
- Issues: Pacing, assessment depth

**Version 1.1** (Planned):
- Release: Spring 2025
- Changes: Unit 2 split, assessment revision
- Expected Performance: 78%
- Expected Mastery: 15/18 objectives (83%)

**Success Indicators for Version 1.1**:
✅ Increase average performance by 6+ percentage points
✅ Achieve ≥70% mastery on all objectives
✅ Reduce "feeling rushed" feedback to <30%
✅ Reduce "just memorization" feedback to <20%

## Next Review Cycle

**When**: End of Spring 2025 term
**Data to Collect**:
- Student performance on revised assessments
- Student feedback surveys
- Instructor observations
- Comparison to Version 1.0 baseline

**Questions to Answer**:
- Did splitting Unit 2 improve mastery?
- Did revised assessments better measure learning?
- What new issues emerged?
- What worked well and should be kept?

---

**Iteration Metadata**:
- **Current Version**: 1.0
- **Recommended Version**: 1.1
- **Change Type**: MINOR (improvements, not redesign)
- **Priority Issues**: 2 critical, 2 important, 1 enhancement
- **Implementation Timeline**: 12 weeks
```

### 5. Track Effectiveness Across Versions

```markdown
## Version Comparison: 1.0 vs 1.1

| Metric | v1.0 (Baseline) | v1.1 (Revised) | Change | Status |
|--------|-----------------|----------------|--------|--------|
| Avg Performance | 72% | 78% | +6% | ✅ Target met |
| Unit 2 Mastery | 45% | 73% | +28% | ✅ Excellent |
| Apply-Level Perf | 58% | 72% | +14% | ✅ Target met |
| Feeling Rushed | 60% | 25% | -35% | ✅ Target met |
| Real-World Value | 45% agree | 78% agree | +33% | ✅ Improved |

**Analysis**:
Version 1.1 successfully addressed all critical issues. Unit 2 mastery increased dramatically (+28 percentage points) after splitting into two units. Assessment revisions led to deeper learning (Apply performance +14%). Student satisfaction improved significantly.

**New Issues Identified in v1.1**:
- Unit 3 now feels rushed by comparison (new pacing issue)
- Need more collaborative activities

**Recommendation for v1.2**:
Address Unit 3 pacing and add collaborative work.
```

### 6. CLI Interface

```bash
# Analyze all feedback
/curriculum.iterate-feedback --feedback "surveys/,outcomes/,reviews/" --curriculum "curriculum-artifacts/"

# Specific focus
/curriculum.iterate-feedback --focus "assessment" --outcomes "results.csv" --feedback "comments.txt"

# Version comparison
/curriculum.iterate-feedback --compare --v1 "v1.0-data/" --v2 "v1.1-data/"

# Generate revision plan
/curriculum.iterate-feedback --plan --feedback "all-feedback/" --timeline "12 weeks" --resources "medium"

# Help
/curriculum.iterate-feedback --help
```

## Composition with Other Skills

**Input from**:
- `/curriculum.analyze-outcomes` - Performance data
- Student surveys and feedback
- Peer review notes

**Output to**:
- Educator for implementation
- `/curriculum.design` - For redesign
- `/curriculum.develop-*` - For revisions

## Exit Codes

- **0**: Analysis complete, recommendations generated
- **1**: Cannot load feedback sources
- **2**: Insufficient data for analysis
- **3**: No patterns identified
- **4**: Invalid comparison versions

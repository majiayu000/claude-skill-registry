---
name: system-reviewer
description: Review the skill development ecosystem itself - assess ecosystem health, identify systemic issues, evaluate toolkit effectiveness, and recommend system-level improvements. Task-based operations for ecosystem assessment, toolkit evaluation, process review, and system optimization. Use when evaluating ecosystem health, identifying systemic improvements, optimizing the toolkit itself, or conducting meta-level ecosystem reviews.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# System Reviewer

## Overview

system-reviewer performs meta-level reviews of the skill development ecosystem itself, assessing the health and effectiveness of the entire system rather than individual skills.

**Purpose**: Meta-level ecosystem assessment and system optimization

**The 5 System Review Operations**:
1. **Ecosystem Health Check** - Assess overall ecosystem quality and completeness
2. **Toolkit Effectiveness Review** - Evaluate how well the toolkit works
3. **Process Efficiency Review** - Review development processes for optimization
4. **Coverage Gap Analysis** - Identify missing capabilities or skills
5. **System Optimization Recommendations** - Recommend system-level improvements

**Key Distinction**: Reviews the SYSTEM, not individual skills

## When to Use

- Periodic ecosystem health checks (monthly/quarterly)
- After completing major layers (Layer 2, 3, 4, 5)
- When suspecting systemic issues (not individual skill problems)
- Planning next ecosystem developments
- Optimizing the development system itself

## Operations

### Operation 1: Ecosystem Health Check

**Purpose**: Assess overall ecosystem quality, completeness, and consistency

**Process**:

1. **Count and Categorize Skills**
   - Total skills built
   - Skills per layer
   - Pattern distribution (workflow/task/reference)
   - Completion percentage

2. **Assess Structural Quality**
   - Run review-multi validation on all skills
   - Calculate average quality scores
   - Identify outliers (very high/low quality)
   - Check consistency across ecosystem

3. **Evaluate Completeness**
   - Are all planned layers complete?
   - Are there gaps in capabilities?
   - Is toolkit comprehensive?
   - Missing critical functionality?

4. **Check Integration**
   - Do skills work together well?
   - Are there integration issues?
   - Workflow compositions effective?
   - Dependencies clear and working?

5. **Generate Health Report**
   - Overall health score (healthy/good/needs attention/critical)
   - Strengths (what's working well)
   - Weaknesses (what needs improvement)
   - Trends (improving/stable/degrading)

**Outputs**:
- Ecosystem health score
- Skill inventory and metrics
- Quality assessment aggregate
- Completeness analysis
- Integration assessment
- Health report with recommendations

**Time Estimate**: 1-2 hours

**Example**:
```
Ecosystem Health Check: 2025-11-07
====================================

Skill Inventory:
- Total Skills: 23
- Layer 2: 10/10 (100%)
- Layer 3: 7/7 (100%)
- Layer 4: 6/6 (100%)
- Layer 5: 0/5 (0%)

Quality Assessment:
- Average Structure Score: 5.0/5.0 (all 23 skills Grade A)
- Quality Range: 5/5 (no variation - excellent consistency)
- Quick Reference Coverage: 100% (all 23 skills)
- Anti-Patterns: 10 total identified, 3 fixed

Completeness:
✅ Research capability: Complete (skill-researcher + research-workflow)
✅ Planning capability: Complete (planning-architect + task-development + planning-workflow)
✅ Execution capability: Complete (todo-management + momentum-keeper)
✅ Quality capability: Complete (review-multi + skill-validator + skill-tester + review-workflow)
✅ Improvement capability: Complete (skill-reviewer + skill-updater + improvement-workflow)
⬜ Self-improvement: 0% (Layer 5 not built)
⬜ Comprehensive testing: Partial (skill-tester exists, testing-validator missing)

Integration Assessment:
✅ Skills compose well (development-workflow, review-workflow, improvement-workflow working)
✅ Dependencies clear (YAML + documentation)
✅ Workflows effective (proven through usage)

Ecosystem Health: ✅ HEALTHY

Strengths:
- 100% structural excellence
- Complete Layers 2-4
- Validated continuous improvement cycle
- 85% efficiency gain proven

Weaknesses:
- Layer 5 incomplete (missing self-improvement automation)
- testing-validator missing (validation incomplete without it)
- Some minor anti-patterns in 4 skills (vague validation criteria)

Trends:
✅ Improving: Efficiency compounding, quality consistent, standards evolving
✅ Stable: Structural quality (all 5/5)

Recommendations:
1. [High] Complete Layer 5 for full self-improvement capability
2. [Medium] Build testing-validator for complete validation suite
3. [Low] Refine vague validation criteria in 4 skills
```

---

### Operation 2: Toolkit Effectiveness Review

**Purpose**: Evaluate how well the development toolkit enables skill building

**Process**:

1. **Measure Efficiency Gains**
   - Build time progression (skills 1-23)
   - Efficiency vs baseline
   - Time saved calculation
   - Trend analysis (improving/plateauing?)

2. **Assess Tool Utilization**
   - Which tools used most? (high value)
   - Which tools rarely used? (low value or unknown)
   - Which tools most effective? (biggest impact)
   - Are there gaps? (missing tools)

3. **Evaluate Workflow Effectiveness**
   - Is development-workflow actually used?
   - Does it save time as promised?
   - Are workflows followed or bypassed?
   - Improvements to workflows needed?

4. **Check Tool Quality**
   - Are tools themselves high quality?
   - Do they achieve stated purposes?
   - User satisfaction with tools?
   - Tools needing improvement?

5. **Generate Toolkit Assessment**
   - Most valuable tools
   - Least utilized tools
   - Effectiveness metrics
   - Improvement opportunities

**Outputs**:
- Toolkit effectiveness assessment
- Tool utilization metrics
- High-value vs low-value tools identified
- Toolkit improvement recommendations

**Time Estimate**: 1-1.5 hours

---

### Operation 3: Process Efficiency Review

**Purpose**: Review development processes for optimization opportunities

**Process**:

1. **Document Current Processes**
   - How are skills currently built?
   - What's the typical workflow?
   - What steps are always followed?
   - What steps are sometimes skipped?

2. **Measure Process Metrics**
   - Average build time per skill complexity
   - Rework rate (how often redo work?)
   - Blocker frequency (how often stuck?)
   - Completion rate (how many finished?)

3. **Identify Bottlenecks**
   - Longest steps in process
   - Most frequent blockers
   - Highest rework areas
   - Inefficient patterns

4. **Assess Automation**
   - What's automated? (scripts, workflows)
   - What's manual? (still required human input)
   - Automation opportunities? (could be automated)
   - Automation effectiveness? (actually saves time?)

5. **Generate Process Recommendations**
   - Process simplifications
   - Automation opportunities
   - Bottleneck elimination
   - Efficiency improvements

**Outputs**:
- Process efficiency assessment
- Bottleneck analysis
- Automation opportunities
- Process optimization recommendations

**Time Estimate**: 1-2 hours

---

### Operation 4: Coverage Gap Analysis

**Purpose**: Identify missing capabilities, skills, or functionality in ecosystem

**Process**:

1. **Review Original Plan**
   - What was planned? (39 skills originally)
   - What's built? (23 skills currently)
   - What's missing? (16 skills remaining)

2. **Assess Current Capabilities**
   - Research: Complete ✅
   - Planning: Complete ✅
   - Execution: Complete ✅
   - Quality: Mostly complete (missing testing-validator)
   - Improvement: Complete ✅
   - Automation: Partial (Layer 5 missing)

3. **Identify Critical Gaps**
   - Must-have missing capabilities
   - High-value skills not built
   - Ecosystem limitations without them

4. **Prioritize Remaining Work**
   - Critical (must build)
   - High value (should build)
   - Nice to have (optional)
   - Low priority (defer)

5. **Generate Coverage Report**
   - Gap analysis (what's missing)
   - Impact assessment (what's the cost of gap)
   - Prioritized build recommendations

**Outputs**:
- Coverage gap analysis
- Missing capabilities identified
- Prioritized skill build recommendations

**Time Estimate**: 45-90 minutes

---

### Operation 5: System Optimization Recommendations

**Purpose**: Recommend system-level improvements (not individual skill improvements)

**Process**:

1. **Aggregate Findings**
   - From Operations 1-4
   - From analysis of all skills
   - From usage patterns
   - From feedback

2. **Identify System-Level Issues**
   - Structural issues (ecosystem organization)
   - Process issues (development workflow problems)
   - Tool issues (toolkit gaps or inefficiencies)
   - Integration issues (skills not composing well)

3. **Generate Recommendations**
   - System reorganization needs
   - Process improvements
   - Toolkit enhancements
   - Integration optimizations

4. **Prioritize by Impact**
   - Critical (affects ecosystem viability)
   - High (significantly improves system)
   - Medium (moderate improvement)
   - Low (nice to have)

5. **Create Action Plan**
   - What to build next
   - What to improve
   - What to refactor
   - What to deprecate (if anything)

**Outputs**:
- System optimization recommendations
- Prioritized action plan
- Impact assessments
- Next development priorities

**Time Estimate**: 1-2 hours

---

## Best Practices

### 1. Regular Health Checks
**Practice**: Run ecosystem health check monthly or after major milestones

**Rationale**: Early detection of systemic issues prevents compounding

### 2. Data-Driven Assessment
**Practice**: Use metrics and evidence, not opinion

**Rationale**: Objective assessment enables better decisions

### 3. System-Level Focus
**Practice**: Focus on ecosystem patterns, not individual skill issues

**Rationale**: system-reviewer is for systemic issues, review-multi for individual skills

### 4. Act on Findings
**Practice**: Use recommendations to guide next development priorities

**Rationale**: Reviews without action don't improve anything

---

## Quick Reference

### The 5 System Review Operations

| Operation | Focus | Time | Output |
|-----------|-------|------|--------|
| **Ecosystem Health** | Overall quality, completeness | 1-2h | Health score, strengths/weaknesses |
| **Toolkit Effectiveness** | Tool utilization, efficiency | 1-1.5h | Tool assessment, utilization metrics |
| **Process Efficiency** | Development process optimization | 1-2h | Bottlenecks, automation opportunities |
| **Coverage Gaps** | Missing capabilities | 45-90m | Gap analysis, prioritized builds |
| **System Optimization** | System-level improvements | 1-2h | Recommendations, action plan |

**Total Time**: 5-8 hours for complete system review

### System vs Individual Skill Reviews

**system-reviewer** (this skill):
- Reviews the ECOSYSTEM
- Systemic issues and patterns
- System-level optimization
- Meta-level assessment

**review-multi**:
- Reviews INDIVIDUAL SKILLS
- Skill-specific issues
- Individual skill improvements
- Skill-level assessment

**Use Both**: system-reviewer for ecosystem health, review-multi for individual quality

### Integration with Continuous Improvement

```
system-reviewer → Identify systemic issues
    ↓
process-optimizer → Optimize processes
    ↓
feedback-analyzer → Analyze effectiveness
    ↓
auto-updater → Apply system improvements
    ↓
evolution-reporter → Report progress
    ↓
Improved ecosystem → Better skills
```

---

**system-reviewer enables meta-level ecosystem assessment and system optimization for continuous ecosystem improvement.**

---
name: process-optimizer
description: Optimize skill development processes through bottleneck identification, efficiency analysis, automation discovery, and workflow improvement. Task-based operations for process analysis, bottleneck elimination, automation opportunities, and workflow streamlining. Use when optimizing development processes, reducing cycle times, improving efficiency, or streamlining workflows based on system-reviewer findings.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Process Optimizer

## Overview

process-optimizer improves skill development processes by identifying and eliminating inefficiencies, bottlenecks, and waste.

**Purpose**: Make skill development processes faster and more efficient

**The 4 Optimization Operations**:
1. **Identify Bottlenecks** - Find process slowdowns and constraints
2. **Discover Automation** - Identify automation opportunities
3. **Streamline Workflows** - Simplify and optimize workflows
4. **Implement Improvements** - Apply process optimizations

**Integration**: Uses findings from system-reviewer Operation 3 (Process Efficiency Review)

## When to Use

- Development processes feel slow or inefficient
- After system-reviewer identifies process issues
- When looking to reduce cycle times
- Before scaling to many skills (optimize early)
- Continuous process improvement

## Operations

### Operation 1: Identify Bottlenecks

**Purpose**: Find steps that slow down development

**Process**:
1. Map current process (what are the steps?)
2. Measure duration (how long each step?)
3. Identify slowest steps (bottlenecks)
4. Analyze causes (why is it slow?)
5. Prioritize by impact (which to fix first?)

**Output**: Bottleneck analysis with prioritized fixes

**Time**: 45-90 minutes

---

### Operation 2: Discover Automation

**Purpose**: Identify manual work that could be automated

**Process**:
1. List manual steps in process
2. Identify repetitive/mechanical work
3. Assess automation feasibility (easy/hard/impossible?)
4. Estimate ROI (time to automate vs time saved)
5. Prioritize automation opportunities

**Output**: Automation opportunities prioritized by ROI

**Time**: 45-90 minutes

---

### Operation 3: Streamline Workflows

**Purpose**: Simplify processes, eliminate unnecessary steps

**Process**:
1. Review each workflow step (is it necessary?)
2. Identify redundant work (done twice?)
3. Find unnecessary complexity (simpler approach?)
4. Combine or eliminate steps
5. Design streamlined workflow

**Output**: Streamlined process with steps eliminated/combined

**Time**: 60-120 minutes

---

### Operation 4: Implement Improvements

**Purpose**: Apply process optimizations discovered

**Process**:
1. Select high-priority improvement
2. Design implementation (how to apply?)
3. Implement (update workflows, tools, guidelines)
4. Test (does it actually help?)
5. Measure impact (time saved, efficiency gained)

**Output**: Implemented improvement with measured impact

**Time**: 1-4 hours (varies by improvement)

---

## Example Process Optimizations

**Optimization 1**: Automated structure validation
- **Before**: Manual YAML checking, 30-45 min
- **After**: validate-structure.py script, 5-10 min automated
- **Impact**: 75% time reduction, 95% accuracy improvement

**Optimization 2**: development-workflow
- **Before**: Ad-hoc skill building, 17-29 hours/skill
- **After**: Systematic workflow, 12-18 hours/skill
- **Impact**: 35-40% time reduction, higher quality

**Optimization 3**: Fast-track approach for simple skills
- **Before**: Full workflow even for simple skills
- **After**: Skip task-development, use prompt-first approach
- **Impact**: 10-15% additional time savings on simple skills

---

## Quick Reference

| Operation | Focus | Time | Output |
|-----------|-------|------|--------|
| Identify Bottlenecks | Find slowdowns | 45-90m | Bottleneck analysis |
| Discover Automation | Find automation opportunities | 45-90m | Automation prioritization |
| Streamline Workflows | Simplify processes | 60-120m | Streamlined workflows |
| Implement Improvements | Apply optimizations | 1-4h | Measured improvements |

**Integration**: system-reviewer (identifies issues) → process-optimizer (fixes them)

---

**process-optimizer makes skill development faster and more efficient through systematic process improvement.**

---
name: Dark Matter Analyzer
description: Analyze repositories to reveal unseen patterns, strategic drift, and organizational health. Use when assessing repository coherence, diagnosing project issues, identifying documentation inflation, or understanding why a codebase feels misaligned with its stated goals.
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash, Task
mcp-tools: dark-matter-analyzer-mcp
---

# Dark Matter Analyzer

## Purpose

Dark Matter Mode reveals what is **unseen, unsaid, and unmeasured** in repositories and codebases. It goes beyond code quality metrics to illuminate the invisible architectures shaping system behavior — identifying strategic drift, documentation inflation, execution gaps, and organizational health patterns that traditional tools miss.

> "Every repo is a psyche made visible."

This skill helps diagnose **why** a repository feels off, not just **what** is wrong technically.

## When to Use This Skill

- Repository feels misaligned but traditional metrics look fine
- Documentation is extensive but team still feels confused
- Stated goals don't match actual work being done
- Need to understand organizational patterns in codebase structure
- Project velocity is high but coherence feels low
- Planning significantly outpaces execution
- Multiple overlapping documents on same topics
- Need to assess "Repository Coherence Index" (RCI)
- Preparing for major refactor or reorganization
- **When NOT to use:** Simple bug fixes, feature additions, or standard code reviews

## Core Methodology

### Step 1: Sensing — Signal Ingest

**Objective:** Capture ambient signals and metadata from the repository

**Actions:**

1. **Scan code signals:** commit patterns, refactor frequency, lint suppressions, TODO/FIXME markers
2. **Scan documentation signals:** README drift, redundant .md files, doc count vs code ratio
3. **Scan temporal signals:** time lag between decision and execution, feature velocity
4. **Scan environmental signals:** dependency health, build status, test coverage trends

**Key Decisions:**

- Scope: Full repository or specific subsystem?
- Depth: Quick scan (3 levels) or deep analysis (all files)?
- Exclusions: What to skip (node_modules, dist, vendor)?

**Common Pitfalls:**

- ❌ Looking only at code metrics → ✅ Include documentation and temporal patterns
- ❌ Judging patterns as "errors" → ✅ View them as system expressions
- ❌ Analyzing in isolation → ✅ Compare stated intent with observed behavior

**Tools to Use:**

```bash
# Count documentation files
find . -name "*.md" -type f | wc -l

# Find technical debt markers
grep -r "TODO\|FIXME\|HACK" --include="*.ts" --include="*.js"

# Check commit patterns
git log --oneline --since="1 month ago" | head -20

# Find documentation inflation
find DOCS -name "*.md" -exec wc -l {} \; | awk '{sum+=$1} END {print sum}'
```

### Step 2: Pattern Detection — Weak Signal Mapping

**Objective:** Identify subtle misalignments before they become major problems

**Actions:**

1. Map patterns to known categories (Strategic Drift, Documentation Inflation, Suppression, etc.)
2. Calculate pattern intensity (frequency, scope, recency)
3. Identify pattern clusters (multiple related signals)
4. Assess emotional subtext (what the pattern reveals about team state)

**Pattern Categories:**

| Pattern Type                | Example Signal                     | Reflective Interpretation                  |
| --------------------------- | ---------------------------------- | ------------------------------------------ |
| **Strategic Drift**         | README ≠ commit activity           | Vision disconnection or premature pivoting |
| **Documentation Inflation** | Many similar .md files             | Over-planning; avoidance through writing   |
| **Suppression Pattern**     | Many `eslint-disable` or `any`     | Time pressure or fatigue                   |
| **Frozen Dependencies**     | No updates for months              | Fear of breakage or resistance to change   |
| **Commit Whiplash**         | Rapid reversals                    | External pressure or internal restlessness |
| **Task-Reality Desync**     | Tests pass but features incomplete | Validation of structure, not utility       |
| **Execution Deficit**       | Documentation >> Implementation    | Hope-driven development                    |

**Validation:**

- [ ] At least 3 distinct patterns identified
- [ ] Each pattern has concrete evidence
- [ ] Patterns tell a coherent story
- [ ] Emotional subtext identified

### Step 3: Reflection — Meaning Extraction

**Objective:** Transform patterns into narrative insights with actionable interpretation

**Actions:**

1. Create technical ↔ human translation for each pattern
2. Assess reflective confidence (0.0-1.0) for each insight
3. Calculate uncertainty index for interpretive humility
4. Identify "The Unseen" (what exists but isn't visible)
5. Identify "The Unsaid" (what isn't explicitly stated)
6. Identify "The Unmeasured" (what has no metric)

**Technical ↔ Human Translation Bridge:**

| Technical Symptom    | Human Parallel              |
| -------------------- | --------------------------- |
| Ignored build errors | Denial of fragility         |
| Rapid branching      | Loss of trust in direction  |
| Over-commenting      | Fear of being misunderstood |
| Skipped validation   | Avoidance of feedback       |
| Over-planning        | Anxiety about imperfection  |
| Unfinished refactors | Fatigue, low follow-through |

**Key Principles:**

- Never judge, only illuminate
- Patterns are expressions, not errors
- Confidence scores show interpretive humility
- Focus on **why**, not just **what**

**Common Pitfalls:**

- ❌ Presenting only metrics → ✅ Tell the story the patterns reveal
- ❌ Being prescriptive → ✅ Being reflective and interpretive
- ❌ Assuming omniscience → ✅ Include uncertainty scores

### Step 4: Action Routing — Coherence Restoration

**Objective:** Provide graduated recommendations based on urgency and impact

**Actions:**

1. Route findings by intervention strength (OBSERVE, REVIEW, HOLD)
2. Apply Coherence Filter: "Does this make the system more truthful?"
3. Provide specific, actionable next steps
4. Include restoration protocol for critical issues

**Intervention Modes:**

| Mode           | Urgency | Action Type           | Example                                                    |
| -------------- | ------- | --------------------- | ---------------------------------------------------------- |
| **🟢 OBSERVE** | Low     | Gentle awareness      | "Velocity high, coherence low. Monitor for drift."         |
| **🟡 REVIEW**  | Medium  | Structured reflection | "Validate assumptions with peer. Check external feedback." |
| **🔴 HOLD**    | High    | Pause + confirm       | "Reality desynced. Reconcile before next build."           |

**Restoration Protocol (for HOLD items):**

```yaml
restoration:
  1. pause: Create reflective checkpoint
  2. align: Re-anchor to intent + artifact coherence
  3. integrate: Capture insight in feedback loop
  4. resume: Rebuild context from re-synced rhythm
```

**Validation:**

- [ ] Recommendations prioritized by urgency
- [ ] Each has clear next action
- [ ] Restoration protocol included for critical items
- [ ] Emotional support included (not just technical fixes)

### Step 5: Repository Coherence Index (RCI)

**Objective:** Calculate overall repository health score

**Formula:**

```
RCI = (Intent Alignment + Task Reality Sync + Technical Health) / 3
```

**Scoring Components:**

**Intent Alignment (0-100):**

- Stated purpose matches observed work
- README reflects actual codebase state
- Goals align with execution

**Task Reality Sync (0-100):**

- Tests validate actual utility, not just structure
- "Complete" claims match reality
- Implementation matches documentation

**Technical Health (0-100):**

- Build passing
- Tests comprehensive
- Dependencies maintained
- Technical debt managed

**Interpretation:**

| RCI Score | Status        | Meaning                            |
| --------- | ------------- | ---------------------------------- |
| 85-100    | ✅ COHERENT   | Rhythm aligned, healthy system     |
| 70-84     | 🟡 MONITOR    | Early drift present, watch closely |
| 50-69     | 🟠 MISALIGNED | Intent and reality diverging       |
| <50       | 🔴 INCOHERENT | Rebuild context or reset rhythm    |

## Key Principles

1. **Reveal, Not Judge**
   Dark Matter Mode illuminates patterns without declaring them "right" or "wrong." Every pattern is an expression of system state. The goal is truthfulness, not perfection.

2. **Interpretive, Not Diagnostic**
   DMM doesn't predict outcomes — it provides reflective insights. Use uncertainty scores to maintain interpretive humility. The mirror knows when it is dreaming.

3. **Coherence Over Speed**
   Ask: "Does this make the system more truthful, not just faster?" Optimize for alignment between intent, artifact, and action.

4. **Emotional Resonance**
   Technical patterns reveal human patterns. Documentation inflation may indicate anxiety. Suppression patterns may show fatigue. Acknowledge the human element.

5. **External Validation**
   Internal consistency ≠ external utility. Tests may pass while users remain confused. Seek external feedback to validate interpretations.

## Decision Framework

**When choosing analysis depth:**

- Use **Quick Scan** when: Initial assessment, triage, or regular health checks
- Use **Deep Analysis** when: Major issues suspected, preparing refactor, or comprehensive audit

**When choosing intervention mode:**

```
If RCI < 50: HOLD (pause and reconcile)
If 50 ≤ RCI < 70: REVIEW (structured reflection)
If 70 ≤ RCI < 85: OBSERVE (gentle monitoring)
If RCI ≥ 85: MAINTAIN (celebrate and sustain)
```

**When to recommend external validation:**

```
If user discovered gap before internal analysis: HIGH PRIORITY
If documentation significantly exceeds implementation: RECOMMENDED
If team feels confused despite extensive docs: REQUIRED
Otherwise: NICE TO HAVE
```

## Output Format

### Dark Matter Report Structure

```markdown
# Dark Matter Mode Analysis

**Date:** [timestamp]
**Repository:** [name]
**RCI Score:** [score]/100 — [STATUS]

## Executive Summary

[3-5 sentence overview of key findings]

## Layer 1: Sensing — What Was Observed

[Code, documentation, temporal, environmental signals]

## Layer 2: Pattern Detection — The Weak Signals

[Identified patterns with evidence and intensity]

## Layer 3: Reflection — The Unseen, Unsaid, Unmeasured

[Narrative insights and interpretations]

## Layer 4: Action — Recommendations by Urgency

### 🔴 HOLD — Stop Before Proceeding

[Critical actions]

### 🟡 REVIEW — Reflection Requested

[Medium priority actions]

### 🟢 OBSERVE — Gentle Nudges

[Low priority awareness items]

## Repository Coherence Index

[Detailed scoring breakdown]

## Closing Reflection

[Supportive conclusion with path forward]
```

## MCP Integration

This skill integrates with `dark-matter-analyzer-mcp` for automated scanning:

```javascript
// Run repository scan
await mcp.call('scan_repository', {
  path: './my-project',
  depth: 'deep',
  include_patterns: ['*.md', '*.ts', '*.js'],
  exclude_patterns: ['node_modules', 'dist']
})

// Calculate RCI
await mcp.call('calculate_rci', {
  repository_path: './my-project'
})

// Generate report
await mcp.call('generate_report', {
  format: 'markdown',
  output_path: './dark_matter_report.md'
})
```

## Examples

### Example 1: Documentation Inflation

**Signal:** 30 documentation files averaging 543 lines each

**Pattern:** Documentation Inflation (HIGH)

**Reflection:**

> "Planning activity significantly outpaces execution. The repository is drowning in its own self-awareness."

**Action (HOLD):**

- Freeze new documentation until doc count reduced by 50%
- Consolidate overlapping files
- Establish build vs. doc ratio ≥ 1.0

### Example 2: Skill-to-Tool Gap

**Signal:** 36 methodologies, 3 implementation tools (12:1 ratio)

**Pattern:** Execution Deficit (CRITICAL)

**Reflection:**

> "The repository is a library of wisdom without hands to execute it. 92% of capabilities are aspirational, not actionable."

**Action (HOLD):**

- Freeze new methodology creation
- Build 6-9 tools to close gap to 6:1 ratio
- Focus on execution-driven development

### Example 3: Test-Driven Wishful Thinking

**Signal:** All tests passing, but CLI has TODO comments, MCPs are placeholders

**Pattern:** Task-Reality Desynchronization (MODERATE)

**Reflection:**

> "The repository passes its own tests but may not serve users. Validation ensures internal consistency, not external utility."

**Action (REVIEW):**

- Gather user feedback on actual utility
- Validate with external users, not just internal tests
- Distinguish structure validation from utility validation

## Related Skills

- **quality-auditor** - Technical quality assessment
- **mvp-builder** - Execution-focused development
- **product-strategist** - Strategic alignment
- **technical-debt-assessor** - Debt identification and prioritization

## Success Metrics

- Repository Coherence Index improves by 10+ points
- Team reports increased clarity about direction
- Documentation consolidation reduces confusion
- Execution velocity increases relative to planning velocity
- External users validate improvements

## Anti-Patterns to Avoid

❌ **Using Dark Matter Mode as a weapon** - This is reflective, not punitive
❌ **Over-relying on RCI score** - It's orientation, not verdict
❌ **Ignoring emotional subtext** - Technical patterns reveal human state
❌ **Skipping uncertainty scores** - Maintain interpretive humility
❌ **Making changes without user validation** - Internal analysis ≠ external truth

---

_"Dark Matter Mode remains a mirror — it does not predict, it illuminates."_

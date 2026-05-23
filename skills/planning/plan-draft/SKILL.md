---
name: plan-draft
description: |
  Interactive iterative draft YAML document creation with user feedback loop.
  Creates Machine-Readable YAML specifications through collaborative refinement.
  Supports version tracking, visualization, and final conversion to English format.
  v1.2.0: Pattern-aware feedback with Self-Synthesis Gate and Feedback Classification.
user-invocable: true
disable-model-invocation: false
context: standard
model: opus
argument-hint: "<topic> [--finalize] [--visualize <section>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__sequential-thinking__sequentialthinking
---

# /plan-draft - Iterative Draft YAML Document Creator

> **Version:** 1.2.0
> **Role:** Interactive Document Creation with Feedback Loop
> **Pattern:** Iterative Feedback Loop + Version Tracking + Machine-Readable Output
> **v1.2.0:** Pattern-aware Feedback with Self-Synthesis Gate

---

## 1. Purpose

Create structured YAML specification documents through an interactive feedback loop:

1. **Initialize** draft YAML with user's topic and initial structure
2. **Iterate** through user feedback with immediate reflection
3. **Track** all changes via version numbers and changelog
4. **Visualize** sections on request for validation
5. **Finalize** to Machine-Readable English YAML format

### Core Pattern (What We Used)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Iterative Feedback Loop Based Document Completion Process              │
│                                                                         │
│  User Feedback                                                          │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐   │
│  │  v0.1.0         │ ──▶ │  v0.2.0         │ ──▶ │  v0.3.0         │   │
│  │  Initial Draft  │     │  + Feedback #1  │     │  + Feedback #2  │   │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘   │
│           │                                               │             │
│           └───────────────────────────────────────────────┘             │
│                                   │                                     │
│                                   ▼                                     │
│                     ┌─────────────────────────────┐                     │
│                     │  v1.0.0 (plan-final.yaml)   │                     │
│                     │  Machine-Readable + English │                     │
│                     └─────────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Characteristics

| Element | Description |
|---------|-------------|
| **Conversation Language** | Korean (or user's language) |
| **Feedback Style** | Short, clear directives (1-2 sentences) |
| **Reflection Method** | Immediate Edit → Version update → Changelog |
| **Validation Method** | Visualization request → Feedback → Iterate |
| **Final Output** | English, Machine-Readable YAML |

---

## 2. Invocation

### User Syntax

```bash
# Start new draft with topic
/plan-draft enhanced-feedback-loop-pattern

# Resume existing draft
/plan-draft --resume enhanced-feedback-loop-pattern-20260127

# Finalize to Machine-Readable format
/plan-draft --finalize enhanced-feedback-loop-pattern-20260127

# Visualize specific section
/plan-draft --visualize phase_4 enhanced-feedback-loop-pattern-20260127
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<topic>` | Yes (for new) | Topic name for the draft document |
| `--resume` | No | Resume existing draft by slug |
| `--finalize` | No | Convert draft to Machine-Readable final YAML |
| `--visualize` | No | Visualize specific section for review |

---

## 3. Draft Document Schema

### 3.1 Standard Draft Template

```yaml
---
# =============================================================================
# {Topic} - Plan Draft
# =============================================================================
# Purpose: {Description}
# Status: DRAFT (awaiting user approval)
# Version: 0.1.0
# Created: {ISO 8601 timestamp}
# Last Updated: {ISO 8601 timestamp}
# =============================================================================

metadata:
  document_type: plan-draft
  topic: "{topic}"
  workload_id: "{topic}_{YYYYMMDD}_{HHMMSS}"
  slug: "{topic}-{YYYYMMDD}"
  author: main-orchestrator
  approval_status: draft
  revision: 1

# =============================================================================
# 1. CORE CONCEPTS
# =============================================================================
core_concepts:
  principles:
    - id: P1
      name: "{principle_name}"
      description: |
        {Principle description}
      implications:
        - "{implication_1}"
        - "{implication_2}"

# =============================================================================
# 2. EXECUTION FLOW
# =============================================================================
execution_flow:
  phases:
    - id: phase_1
      name: "{phase_name}"
      description: "{phase_description}"
      inputs: []
      steps: []
      outputs: []

# =============================================================================
# 3. CONFIGURATION
# =============================================================================
configuration:
  # Key configuration constants

# =============================================================================
# 4. DECISIONS
# =============================================================================
decisions:
  - id: Q1
    question: "{open_question}"
    options:
      - "{option_1}"
      - "{option_2}"
    status: open  # open | decided
    decided_value: null

# =============================================================================
# 5. CHANGELOG
# =============================================================================
changelog:
  - version: "0.1.0"
    date: "{date}"
    changes:
      - "Initial draft created"

# =============================================================================
# END OF DOCUMENT
# =============================================================================
```

### 3.2 Version Numbering Convention

| Version Pattern | Meaning |
|-----------------|---------|
| `0.x.0` | Draft versions (iterating with feedback) |
| `0.x.y` | Minor fixes within same feedback round |
| `1.0.0` | First finalized (Machine-Readable) version |
| `1.x.0` | Post-finalization revisions |

---

## 4. Execution Protocol

### 4.1 Phase 1: Initialization

```javascript
async function initializeDraft(topic) {
  // 1. Generate workload identifiers
  const timestamp = new Date()
  const dateStr = timestamp.toISOString().slice(0, 10).replace(/-/g, '')
  const timeStr = timestamp.toISOString().slice(11, 19).replace(/:/g, '')

  const workloadId = `${topic}_${dateStr}_${timeStr}`
  const slug = `${topic}-${dateStr}`

  // 2. Create workload directory
  const workloadDir = `.agent/prompts/${slug}`
  await Bash({ command: `mkdir -p ${workloadDir}` })

  // 3. Generate initial draft from template
  const draftContent = generateDraftTemplate(topic, workloadId, slug, timestamp)

  // 4. Write draft file
  const draftPath = `${workloadDir}/plan-draft.yaml`
  await Write({ file_path: draftPath, content: draftContent })

  // 5. Return session context
  return {
    workloadId,
    slug,
    draftPath,
    version: "0.1.0"
  }
}
```

### 4.2 Phase 2: Feedback Loop

#### 4.2.0 Self-Validation Protocol (v1.1.0)

Before presenting changes to user, agent performs internal validation:

```javascript
async function selfValidate(context, maxIterations = 3) {
  let iterations = 0;
  let issues = [];

  while (iterations < maxIterations) {
    iterations++;
    issues = await runValidationChecks(context);

    const autoFixable = issues.filter(i => i.autoFixable);
    const nonFixable = issues.filter(i => !i.autoFixable);

    if (autoFixable.length > 0) {
      await applyAutoFixes(context, autoFixable);
      continue; // Re-validate after fixes
    }

    if (nonFixable.length === 0) {
      return { status: 'PASSED', iterations };
    }

    break;
  }

  return {
    status: issues.length > 0 ? 'PASSED_WITH_WARNINGS' : 'PASSED',
    iterations,
    warnings: issues.map(i => i.description)
  };
}
```

**Validation Criteria:**

| ID | Criterion | Auto-fixable |
|----|-----------|--------------|
| V1 | All sections have content | No |
| V2 | No placeholder text (TODO, TBD) | No |
| V3 | Internal references valid | Yes |
| V4 | Version/changelog consistent | Yes |
| V5 | YAML syntax valid | No |
| V6 | Pattern compliance check | No |
| V7 | Selective refinement applied | Yes |

#### 4.2.1 Feedback Classification (v1.2.0)

Classify validation issues into AUTO_FIX vs USER_CONFIRM:

```javascript
function classifyIssue(issue) {
  // AUTO_FIX: Low severity OR (Medium + auto-fixable)
  if (issue.severity === 'LOW') return 'AUTO_FIX';
  if (issue.severity === 'MEDIUM' && issue.autoFixable) return 'AUTO_FIX';

  // USER_CONFIRM: Medium non-fixable OR High/Critical
  return 'USER_CONFIRM';
}
```

**Classification Matrix:**

| ID | Criterion | Severity | Classification |
|----|-----------|----------|----------------|
| V1 | sections_have_content | HIGH | USER_CONFIRM |
| V2 | no_placeholder_text | MEDIUM | USER_CONFIRM |
| V3 | internal_references_valid | LOW | AUTO_FIX |
| V4 | version_changelog_consistent | LOW | AUTO_FIX |
| V5 | yaml_syntax_valid | CRITICAL | USER_CONFIRM |
| V6 | pattern_compliance_check | MEDIUM | USER_CONFIRM |
| V7 | selective_refinement_applied | LOW | AUTO_FIX |

#### 4.2.2 Feedback Processing

```javascript
async function processFeedback(context, feedback) {
  // 1. Read current draft
  const currentDraft = await Read({ file_path: context.draftPath })

  // 2. Parse version
  const currentVersion = extractVersion(currentDraft)
  const newVersion = incrementMinorVersion(currentVersion)

  // 3. Apply feedback
  const updatedDraft = await applyFeedback(currentDraft, feedback)

  // 4. Update version and timestamp
  updatedDraft.metadata.revision++
  updatedDraft.last_updated = new Date().toISOString()

  // 5. Add changelog entry
  updatedDraft.changelog.unshift({
    version: newVersion,
    date: new Date().toISOString().slice(0, 10),
    changes: [summarizeFeedback(feedback)]
  })

  // 6. Write updated draft
  await Write({ file_path: context.draftPath, content: updatedDraft })

  // 7. Return updated context
  return {
    ...context,
    version: newVersion
  }
}
```

### 4.3 Phase 2.5: Self-Synthesis Gate (v1.2.0)

Holistic document completeness check before finalization:

```javascript
async function selfSynthesisGate(context) {
  // Step 1-3: Collect stats
  const sectionStats = analyzeSections(context.draft);
  const decisionStats = analyzeDecisions(context.draft);
  const validationStats = runValidationSuite(context.draft);

  // Step 4: Calculate completion rate
  const completion = {
    sections: sectionStats.completed / sectionStats.total * 100,
    decisions: decisionStats.decided / decisionStats.total * 100,
    validations: validationStats.passed / validationStats.total * 100,
    overall: Math.min(
      sectionStats.percentage,
      decisionStats.percentage,
      validationStats.percentage
    )
  };

  // Step 5-6: Generate smart prompt and determine action
  if (completion.overall >= 100) {
    return { action: 'FINALIZE', prompt: readyForFinalization() };
  } else if (completion.overall >= 80) {
    return { action: 'CHOOSE', prompt: nearCompleteWithWarnings(completion) };
  } else {
    return { action: 'CONTINUE_EDITING', prompt: gapsDetected(completion) };
  }
}
```

**Completion Rate Formula:**

```
overall = min(sections%, decisions%, validations%)
```

**Smart Prompt Templates:**

| Completion | Template | Token Budget |
|------------|----------|--------------|
| 100% | ready_for_finalization | 80 |
| 80-99% | near_complete_with_warnings | 150 |
| <80% | gaps_detected | 200 |

**Trigger Conditions:**
- Explicit approval signals: `lgtm`, `looks good`, `ok`, `approve`, `done`
- Phase 2 Step 0 validation passes
- Version milestone (major version increment)

### 4.4 Phase 3: Visualization

```javascript
async function visualizeSection(context, sectionId) {
  // 1. Read current draft
  const draft = await Read({ file_path: context.draftPath })

  // 2. Extract target section
  const section = extractSection(draft, sectionId)

  // 3. Generate ASCII visualization
  const visualization = generateVisualization(section)

  // 4. Output visualization (do not store in file)
  console.log(visualization)

  return visualization
}

function generateVisualization(section) {
  // Generate ASCII box diagrams for flows
  // Generate tables for configurations
  // Generate tree structures for hierarchies

  // Example flow visualization:
  /*
  ┌─────────────────────────────────────────────────┐
  │  Phase 4: Main Agent Orchestrated Feedback Loop │
  │                                                 │
  │  Step 1: Strategic Classification               │
  │       │                                         │
  │       ├── Direct Fix (LOW)                      │
  │       └── Agent Delegation (MEDIUM+)            │
  │                                                 │
  │  Step 5: Result Review & Synthesis              │
  └─────────────────────────────────────────────────┘
  */
}
```

### 4.5 Phase 4: Finalization

```javascript
async function finalizeDraft(context) {
  // 1. Read current draft
  const draft = await Read({ file_path: context.draftPath })

  // 2. Validate completeness
  const validation = validateDraft(draft)
  if (!validation.complete) {
    throw new Error(`Draft incomplete: ${validation.missing.join(', ')}`)
  }

  // 3. Check all decisions are made
  const openDecisions = draft.decisions.filter(d => d.status === 'open')
  if (openDecisions.length > 0) {
    throw new Error(`Open decisions: ${openDecisions.map(d => d.id).join(', ')}`)
  }

  // 4. Convert to Machine-Readable English format
  const finalYaml = await convertToFinal(draft)

  // 5. Update version to 1.0.0
  finalYaml.metadata.version = "1.0.0"
  finalYaml.metadata.status = "APPROVED"
  finalYaml.metadata.finalized_at = new Date().toISOString()
  finalYaml.metadata.source_document = "plan-draft.yaml"
  finalYaml.metadata.source_version = context.version

  // 6. Write final file
  const finalPath = context.draftPath.replace('plan-draft.yaml', 'plan-final.yaml')
  await Write({ file_path: finalPath, content: finalYaml })

  // 7. Return result
  return {
    draftPath: context.draftPath,
    finalPath: finalPath,
    version: "1.0.0"
  }
}
```

---

## 5. Machine-Readable Conversion Rules

### 5.1 Korean → English

| Korean Pattern | English Conversion |
|----------------|-------------------|
| `# 핵심 목적 (WHY)` | `objective.why` field |
| `description: \|` (Korean text) | `description:` (English text) |
| `## 왜 X가 필요한가?` | `objective.why:` |
| `검증 기준:` | `validation_criteria:` |
| `단계:` | `steps:` |

### 5.2 Comment → Structured Field

```yaml
# Before (Korean comment-based)
# ---------------------------------------------------------------------------
# 2.5 Phase 4: 선택적 Feedback Loop
# ---------------------------------------------------------------------------
phase_4_selective_feedback:
  name: "Selective Feedback Loop"
  # Main Agent가 직접 Orchestrating하여...

# After (English field-based)
phase_4:
  id: phase_4_selective_feedback
  name: main_agent_orchestrated_feedback_loop
  title: "Selective Feedback Loop (Main Agent Orchestrated)"
  objective:
    why: >
      When issues are found in Phase 3.5, Main Agent must strategically orchestrate
      rather than simply handing off to Agents.
```

### 5.3 Type Definitions Extraction

During finalization, extract implicit types into explicit `type_definitions`:

```yaml
type_definitions:
  L1:
    description: "Level 1 Summary"
    token_limit: 500
  Issue:
    fields:
      - name: id
        type: string
      - name: severity
        type: "enum[LOW, MEDIUM, HIGH, CRITICAL]"
```

---

## 6. Interaction Patterns

### 6.1 Main Agent Role

| Role | Responsibility |
|------|----------------|
| **User** | Holistic design reviewer ("See the forest") |
| **Agent** | Executor + Self-validator ("See the trees") |

### 6.2 Feedback Response Protocol

1. **Receive feedback** → Parse intent
2. **Apply immediately** → Edit file directly
3. **Update version** → Increment + changelog
4. **Confirm** → Show brief summary of changes
5. **Wait** → User validates or provides next feedback

### 6.3 Visualization Request Protocol

When user requests visualization:
1. Extract target section from draft
2. Generate ASCII diagram
3. Output to console (NOT to file)
4. Wait for feedback

---

## 7. Output Paths

| File | Path | Description |
|------|------|-------------|
| Draft | `.agent/prompts/{slug}/plan-draft.yaml` | Working draft (Korean, versioned) |
| Final | `.agent/prompts/{slug}/plan-final.yaml` | Machine-Readable (English, v1.0.0+) |

---

## 8. Example Session

```
User: /plan-draft enhanced-feedback-loop-pattern

Agent: 📝 Draft initialized
       Path: .agent/prompts/enhanced-feedback-loop-pattern-20260127/plan-draft.yaml
       Version: 0.1.0

       Draft includes:
       - Core concepts (5 principles)
       - Execution flow (6 phases)
       - 3 open decisions (Q1, Q2, Q3)

       Ready for feedback.

User: Q1 결정: 동적 (2-5개)

Agent: ✅ v0.2.0 - Q1 decided: dynamic (2-5)
       Changelog updated.

User: Phase 3을 두 Agent로 분리해

Agent: ✅ v0.3.0 - Phase 3 split into Phase 3-A (horizontal) and Phase 3-B (vertical)
       Changelog updated.

User: Phase 4 시각화해줘

Agent: [ASCII visualization of Phase 4]

       Ready for feedback.

User: --finalize

Agent: ✅ Finalized to v1.0.0
       Draft: .agent/prompts/enhanced-feedback-loop-pattern-20260127/plan-draft.yaml (v0.8.0)
       Final: .agent/prompts/enhanced-feedback-loop-pattern-20260127/plan-final.yaml (v1.0.0)

       Conversion:
       - Korean → English
       - Comments → Structured fields
       - Type definitions extracted
```

---

## 9. Validation Checklist

Before finalization, validate:

- [ ] All decisions (`decisions[].status`) are `decided`
- [ ] All phases have `inputs`, `steps`, `outputs`
- [ ] Changelog has all version entries
- [ ] No `TODO` or placeholder text remains
- [ ] All Korean descriptions have clear meaning for translation

---

## 10. Error Handling

| Error | Detection | Recovery |
|-------|-----------|----------|
| Draft not found | File doesn't exist | Initialize new draft |
| Version conflict | Concurrent edit | Reload and merge |
| Open decisions | `--finalize` with open Q | List open decisions, ask to resolve |
| Incomplete phase | Missing required fields | List missing fields |
| Translation ambiguity | Korean text unclear | Ask user for clarification |

---

## 11. Semantic Integrity Preservation

### Critical Rule

> **"후속 작업을 위한 SEMANTIC INTEGRITY"**

When converting draft → final:

1. **No meaning loss** - Every Korean concept must map to English equivalent
2. **Structure preservation** - Hierarchies and relationships maintained
3. **Type safety** - Implicit types made explicit in `type_definitions`
4. **Reference integrity** - All `$ref` and cross-references valid
5. **Downstream compatibility** - Final YAML parseable by implementation phase

---

## 12. Context Management (v1.1.0)

### Strategy

> **"L1 summary to console, L2/L3 to file"**

Manage context size by controlling what gets injected to Main Context vs what remains as file-only output.

### Token Budget

| Output Type | Token Limit | Destination |
|-------------|-------------|-------------|
| L1 Confirmation | 100 | Console |
| L1 Smart Prompt | 200 | Console |
| L2 Change Detail | 500 | Console (verbose mode) |
| L3 Full Document | Unlimited | File |

### Injection Rules

| Event | Console Output | File Storage |
|-------|----------------|--------------|
| Feedback applied | `✅ v0.3.0 - Q1 decided` | - |
| Self-validation complete | `Self-validation: PASSED (2 iterations)` | - |
| Finalization | `✅ Finalized to v1.0.0` | plan-final.yaml |

### Console Output Rules

1. Keep under 200 tokens
2. Include version and status
3. Provide next action options

### Example Output

```
✅ v0.3.0 - Added error handling section

Self-validation: PASSED (1 iteration, 0 auto-fixes)

Draft Status: 75% complete
Open Decisions: 0/3

Options:
1. Provide feedback to continue iterating
2. --visualize <section> to review specific area
3. --finalize (when ready for Machine-Readable conversion)
```

---

## 13. Pattern Comparison (v1.2.0)

### Existing Pattern (v1.1.0)

```
/plan-draft → init → user_feedback → agent_edit → self_validate → loop → finalize
```

**Characteristics:**
- user_initiated_feedback_loop
- single_agent_sequential_execution
- self_validation_with_auto_fix
- version_tracking_per_feedback

### Enhanced Pattern (v1.2.0)

```
/plan-draft → init → feedback_classification → selective_refinement
    → self_validation_extended → feedback_auto_fix_or_user_confirm
    → self_synthesis_gate → holistic_review → finalize_with_migration
```

**New Characteristics:**
- user_initiated_with_agent_pre_classification
- selective_area_refinement_instead_of_full_rewrite
- auto_fix_vs_user_confirm_classification
- explicit_self_synthesis_gate
- pattern_compliance_awareness
- migration_tracking_enabled

---

## 14. Migration Path (v1.2.0)

### From v1.1.0 to v1.2.0

| Change Type | Description |
|-------------|-------------|
| **Added** | pattern_comparison section |
| **Added** | phase_2_5 Self-Synthesis Gate |
| **Added** | feedback_classification system |
| **Added** | migration_path section |
| **Added** | 8 new type definitions |
| **Extended** | V6, V7 validation criteria |

### Backward Compatibility

- v1.1.0 drafts: **fully supported**
- Existing workflows: **no breaking changes**
- V1-V5 validation criteria: **still apply**

### New Type Definitions

| Type | Purpose |
|------|---------|
| CompletionRate | Overall document completion assessment |
| CategoryScore | Score for sections/decisions/validations |
| FeedbackClassification | AUTO_FIX vs USER_CONFIRM |
| ClassifiedIssue | Issue with classification metadata |
| SmartPrompt | Interactive prompt for user decisions |
| PromptOption | Option in a smart prompt |
| RecommendedAction | FINALIZE / CHOOSE / CONTINUE_EDITING |
| PatternCharacteristic | Pattern trait identifier |

---

**End of Skill Documentation**

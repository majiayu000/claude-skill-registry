---
name: re-architecture
description: |
  Pipeline Component Analysis & Feedback Tool.
  Decomposes pipelines into components with traceability feedback.
  Records all interactions in Machine-Readable YAML format.
  Integrates with /research skill for skill-driven pipeline support.
user-invocable: true
model: opus
version: "1.0.0"
argument-hint: "<target-path> | --resume <slug>"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
  - Write
  - Edit
  - AskUserQuestion
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "/home/palantir/.claude/hooks/re-architecture-setup.sh"
      timeout: 10000
  Stop:
    - type: command
      command: "/home/palantir/.claude/hooks/re-architecture-finalize.sh"
      timeout: 180000
---

# /re-architecture - Pipeline Component Analysis & Feedback

> **Version:** 1.0.0 | **Model:** opus

---

## Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Decompose pipelines into components with traceability feedback |
| **Output** | L1: Summary / L2: Per-component analysis / L3: YAML log with full traceability |
| **Language** | All output in Korean |

---

## Cross-Skill Integration

| Skill | Relationship |
|-------|--------------|
| `/research` | Handoff for deep research after analysis |
| `/planning` | Implementation planning after research |

---

## Commands

| Command | Description |
|---------|-------------|
| `<target-path>` | Analyze pipeline at specified path |
| `--resume <slug>` | Resume previous analysis session |

---

## Execution Flow

### Phase 1: Decomposition

1. Parse target path from arguments
2. Analyze pipeline structure with Sequential Thinking
3. Extract components, stages, and dependencies
4. Update YAML log with decomposition results
5. Present results to user

### Phase 2: Iterative Component Analysis

For each component:
1. Deep analysis of component structure
2. Record analysis in YAML log (before)
3. Generate feedback (findings, recommendations, issues)
4. Present options to user with AskUserQuestion
5. Update YAML log with user selection (after)
6. Save component feedback

### Phase 3: Handoff Preparation

1. Synthesize all feedback
2. Generate handoff context for /research
3. Update YAML log with handoff info
4. Present handoff options to user

---

## YAML Log Schema

```yaml
# .agent/prompts/{slug}/re-architecture-log.yaml

metadata:
  id: "{slug}"
  version: "1.0.0"
  created_at: "2026-01-26T21:10:00Z"
  status: "in_progress"  # in_progress | completed | paused
  target_path: "{path}"

state:
  current_phase: "decomposition"  # decomposition | analysis | feedback | handoff
  current_component: null
  round: 1
  total_components: 0
  analyzed_components: 0

user_intent:
  original_request: "{user request}"
  clarified_goals: []
  constraints: []
  priorities: []

decomposition:
  pipeline_structure: "{diagram}"
  components:
    - id: "comp-001"
      name: "{name}"
      path: "{path}"
      type: "stage|module|service|utility"
      dependencies:
        upstream: []
        downstream: []
      status: "pending"  # pending | analyzing | completed

rounds:
  - round: 1
    timestamp: "2026-01-26T21:11:00Z"
    phase: "decomposition"
    component_id: null
    input:
      prompt: "{input}"
      context: "{context}"
    analysis:
      findings: []
      recommendations: []
      issues: []
      code_evidence: []
    output:
      feedback: "{feedback}"
      options_presented: []
      user_selection: null
    traceability:
      design_intent: "{intent}"
      decision_rationale: "{rationale}"
      related_components: []
      parent_round: null
      issue_refs: []

component_feedback:
  "comp-001":
    analyzed_at: "2026-01-26T21:12:00Z"
    summary: "{summary}"
    findings:
      - id: "find-001"
        type: "pattern|issue|opportunity"
        severity: "info|warning|critical"
        description: "{description}"
        evidence:
          file: "{path}"
          line: "{line}"
          snippet: "{code}"
    recommendations:
      - id: "rec-001"
        priority: "high|medium|low"
        description: "{description}"
        rationale: "{rationale}"
        effort_estimate: "small|medium|large"
    issues:
      - id: "issue-001"
        type: "bug|debt|risk|improvement"
        severity: "critical|high|medium|low"
        description: "{description}"
        suggested_action: "{action}"
        blocking: false

handoff:
  ready_for_research: false
  research_context:
    summary: "{summary}"
    key_findings: []
    priority_components: []
    recommended_focus: []
  next_action_hint: "/research --clarify-slug {slug}"
```

---

## Output Format

### Round Presentation

```markdown
## Round {n}: {component_name} Analysis

### Component Info
- **Path:** {path}
- **Type:** {type}
- **Dependencies:** {dependencies}

### Findings
| ID | Type | Severity | Description |
|----|------|----------|-------------|
| find-001 | pattern | info | {description} |

### Recommendations
| ID | Priority | Description | Rationale |
|----|----------|-------------|-----------|
| rec-001 | high | {description} | {rationale} |

### Issues
| ID | Type | Severity | Description | Action |
|----|------|----------|-------------|--------|
| issue-001 | debt | medium | {description} | {action} |

### Design Intent
{design_intent_explanation}
```

### L1 Return Summary

```yaml
taskId: re-arch-{slug}
status: success
summary: "{n}개 컴포넌트 분석 완료, {findings}개 발견사항, {issues}개 이슈"
logPath: .agent/prompts/{slug}/re-architecture-log.yaml
handoffReady: true
nextActionHint: "/research --clarify-slug {slug}"
```

---

## User Interaction Options

### Component Analysis Options

```python
options = [
    {"label": "피드백 승인", "description": "이 컴포넌트 분석을 승인하고 다음으로 진행"},
    {"label": "추가 분석 요청", "description": "특정 영역에 대해 더 깊은 분석 진행"},
    {"label": "이슈 등록", "description": "발견된 문제를 이슈로 등록"},
    {"label": "건너뛰기", "description": "이 컴포넌트를 건너뛰고 다음으로"}
]
```

### Handoff Options

```python
options = [
    {"label": "/research로 진행 (권장)", "description": "분석 결과를 바탕으로 심층 연구 시작"},
    {"label": "분석 결과만 저장", "description": "나중에 수동으로 /research 호출"},
    {"label": "추가 분석 진행", "description": "놓친 컴포넌트 추가 분석"}
]
```

---

## Pipeline Position

```
/re-architecture  <-- THIS SKILL (Entry Point)
    │
    │ re-architecture-log.yaml
    ▼
/research         Deep research (optional)
    │
    ▼
/planning         Implementation planning
```

---

## Error Handling

| Error | Detection | Recovery |
|-------|-----------|----------|
| Target path not found | File/dir not exists | Prompt for correct path |
| YAML write failure | I/O error | Memory fallback + warning |
| Component analysis timeout | >5min | Save partial, allow resume |
| User session timeout | No response | Auto-save, resume later |

---

## Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Initial implementation with YAML traceability logging |

**End of Skill Definition**

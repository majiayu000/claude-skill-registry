---
name: build-research
description: |
  Research dispatcher for enhanced /build command Phase 1.
  Parses user concept input and delegates to claude-code-guide for capability inventory.
  Saves results to .agent/builds/{build_id}/ for resume support.
  Returns L1 summary with complexity level options (0/50/100).

  Core Capabilities:
  - Concept Parsing: Extract and normalize user concept input
  - Research Delegation: Delegate to claude-code-guide subagent
  - Capability Inventory: Generate structured capability inventory
  - Resume Support: Save state for build session continuity

  Output Format:
  - L1: Build session summary with complexity options (YAML)
  - L2: Full capability inventory (research.json)
  - L3: Detailed capability schemas

  Pipeline Position:
  - Called by /build skill in Concept Mode
  - Phase 1 of build workflow
user-invocable: false
disable-model-invocation: false
context: fork
model: opus
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
  - Write
  - mcp__sequential-thinking__sequentialthinking
version: "3.0.0"
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000

# =============================================================================
# P1: Skill as Sub-Orchestrator
# =============================================================================
agent_delegation:
  enabled: true
  default_mode: true  # V1.1.0: Auto-delegation by default
  max_sub_agents: 1
  delegation_strategy: "single-agent"
  strategies:
    single_agent:
      description: "Single delegation to claude-code-guide"
      use_when: "Concept research phase"
  sub_agent_permissions:
    - Read
    - Glob
    - WebSearch
  output_paths:
    l1: ".agent/prompts/{slug}/build-research/l1_summary.yaml"
    l2: ".agent/prompts/{slug}/build-research/l2_index.md"
    l3: ".agent/prompts/{slug}/build-research/l3_details/"
  return_format:
    l1: "Research summary with capability count and level options (≤500 tokens)"
    l2_path: ".agent/prompts/{slug}/build-research/l2_index.md"
    l3_path: ".agent/prompts/{slug}/build-research/l3_details/"
    requires_l2_read: false
    next_action_hint: "/build (Phase 2)"

# =============================================================================
# P2: Parallel Agent Configuration (Disabled - Single Agent Skill)
# =============================================================================
parallel_agent_config:
  enabled: false
  reason: "Single-agent research delegation"

# =============================================================================
# P6: Agent Internal Feedback Loop
# =============================================================================
agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  validation_criteria:
    - "JSON response is valid and parseable"
    - "All capability fields are present"
    - "Level 0/50/100 definitions are complete"
  refinement_triggers:
    - "Invalid JSON structure"
    - "Missing required fields"
    - "Empty capability list"
---

### Auto-Delegation Trigger (CRITICAL)

> **Reference:** `.claude/skills/shared/auto-delegation.md`
> **Behavior:** When `agent_delegation.enabled: true` AND `default_mode: true`, skill automatically operates as Sub-Orchestrator.

```javascript
// AUTO-DELEGATION CHECK - Execute at skill invocation
// If complex task detected, triggers: analyze → delegate → collect
const delegationDecision = checkAutoDelegation(SKILL_CONFIG, userRequest)
if (delegationDecision.shouldDelegate) {
  const complexity = analyzeTaskComplexity(taskDescription, SKILL_CONFIG)
  return executeDelegation(taskDescription, complexity, SKILL_CONFIG)
}
// Simple tasks execute directly without delegation overhead
```


# Build Research Skill - Phase 1 Research Dispatcher

> **Version:** 3.0.0 | **Context:** fork | **Model:** opus
> **Parent:** /build command | **Phase:** 1 of 3


---

## Purpose

Execute Phase 1 (RESEARCH) of the enhanced /build workflow:
1. Parse concept name from user input (`$ARGUMENTS`)
2. Delegate research to claude-code-guide subagent
3. Generate capability inventory
4. Save results with resume support
5. Return L1 summary to Main Agent


---

## 1. Input Parsing

### Supported Input Patterns

```
Pattern 1: /build "Progressive-Disclosure"     → concept = "Progressive-Disclosure"
Pattern 2: /build concept-name                 → concept = "concept-name"
Pattern 3: /build --research "concept-name"    → concept = "concept-name"
Pattern 4: $ARGUMENTS directly                 → concept = $ARGUMENTS.strip()
```

### Build ID Generation (표준 Workload 시스템)

```bash
# Source centralized slug generator
source "${WORKSPACE_ROOT:-.}/.claude/skills/shared/slug-generator.sh"
source "${WORKSPACE_ROOT:-.}/.claude/skills/shared/workload-files.sh"

# 기본 동작: 항상 새 workload 생성 (독립 스킬)
CONCEPT="$1"
TOPIC="build-${CONCEPT:-research}"

# Workload ID 생성
WORKLOAD_ID=$(generate_workload_id "$TOPIC")
SLUG=$(generate_slug_from_workload "$WORKLOAD_ID")

# Short ID for display (레거시 호환)
BUILD_ID="${CONCEPT:0:3}-$(echo "$WORKLOAD_ID" | md5sum | cut -c1-4)"

# 디렉토리 구조 초기화
BUILD_DIR=".agent/builds/${SLUG}"
mkdir -p "${BUILD_DIR}"

# Workload 활성화
set_active_workload "$WORKLOAD_ID"

echo "🔬 Build research initialized: $SLUG (ID: $BUILD_ID)"
```

**레거시 호환:**
```
Format: {concept_slug[:3]}-{hash[:4]}
Example: "pro-a1b2" for "Progressive-Disclosure"
```


---

## 2. Research Delegation

### Claude-Code-Guide Prompt

```
## Context
User wants to build a "{concept}" implementation using Claude Code native capabilities.

## Task
Research ALL relevant Claude Code native capabilities that could implement "{concept}".

## Required Output Format (JSON)
{
  "concept": "{concept}",
  "capabilities": [
    {
      "id": "S1",
      "name": "capability name",
      "category": "skill|agent|hook|pattern",
      "complexity": "basic|intermediate|advanced",
      "level": 0|50|100,
      "description": "1-2 sentence description",
      "fields": ["field1", "field2"],
      "dependencies": ["other_capability_id"]
    }
  ],
  "levels": {
    "0": {
      "name": "Basic",
      "capabilities": ["S1", "H1"],
      "capabilityCount": 2,
      "description": "Core functionality only"
    },
    "50": {
      "name": "Recommended",
      "capabilities": ["S1", "S2", "H1", "H2", "A1"],
      "capabilityCount": 5,
      "description": "Standard implementation with error handling"
    },
    "100": {
      "name": "Full",
      "capabilities": ["S1", "S2", "S3", "H1", "H2", "H3", "A1", "A2"],
      "capabilityCount": 8,
      "description": "Complete implementation with all features"
    }
  },
  "summary": {
    "total_capabilities": 8,
    "by_category": {"skill": 3, "agent": 2, "hook": 3, "pattern": 0},
    "recommended_level": 50,
    "estimated_complexity": "medium"
  }
}

## Research Areas
1. **Skills**: .claude/skills/ patterns, frontmatter fields, execution modes
2. **Agents**: .claude/agents/ patterns, tool restrictions, delegation
3. **Hooks**: Hook event types (13 events), input/output schemas
4. **Patterns**: Orchestration patterns, runtime chaining
5. **Task Tool**: Subagent delegation options

## Constraints
- Only include capabilities directly relevant to "{concept}"
- Categorize by complexity (basic/intermediate/advanced)
- Group into 3 implementation levels (0/50/100)
- Include dependencies between capabilities
```


---

## 3. Directory Structure

```
.agent/builds/
├── master/
│   ├── capability_index.json    # Master capability reference
│   └── complexity_levels.json   # Level 0/50/100 definitions
└── {build_id}/
    ├── research.json            # Raw capability inventory (Phase 1)
    ├── selection.json           # User selections (Phase 2/3)
    └── artifacts.json           # Generated file paths (Phase 3)
```


---

## 4. L1 Output Format (MAX 500 tokens)

Return this format to Main Agent:

```yaml
taskId: {build_id}
agentType: claude-code-guide
summary: "Researched {total} capabilities for '{concept}' across {categories} categories"
status: success

# Progressive Disclosure Fields
priority: HIGH
recommendedRead:
  - anchor: "#capability-details"
    reason: "Full capability inventory with fields and dependencies"
  - anchor: "#level-definitions"
    reason: "Detailed breakdown of 0/50/100 complexity levels"

l2Index:
  - anchor: "#summary"
    tokens: 150
    priority: CRITICAL
    description: "Capability counts and recommended level"
  - anchor: "#levels"
    tokens: 300
    priority: HIGH
    description: "Level 0/50/100 definitions and capability mapping"
  - anchor: "#capability-details"
    tokens: 800
    priority: MEDIUM
    description: "Full capability inventory with schemas"

l2Path: .agent/builds/{build_id}/research.json
requiresL2Read: false
nextActionHint: "Select complexity level (0/50/100) to proceed to Phase 2"

# Build-specific fields
buildId: {build_id}
concept: "{concept}"
researchPath: .agent/builds/{build_id}/research.json
complexityOptions:
  - level: 0
    name: "Basic"
    capabilities: {count}
  - level: 50
    name: "Recommended"
    capabilities: {count}
  - level: 100
    name: "Full"
    capabilities: {count}
```


---

## 5. Execution Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Parse Concept                                    │
│    concept, error = parse_concept($ARGUMENTS)       │
│    if error: return error message                   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ 2. Generate Build ID                                │
│    build_id = generate_build_id(concept)            │
│    e.g., "pro-a1b2"                                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ 3. Delegate Research                                │
│    Task(                                            │
│      subagent_type="claude-code-guide",             │
│      prompt=RESEARCH_PROMPT.format(concept),        │
│      model="haiku"                                  │
│    )                                                │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ 4. Save Results                                     │
│    .agent/builds/{build_id}/research.json           │
│    Initialize: selection.json, artifacts.json      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ 5. Return L1 Summary                                │
│    MAX 500 tokens → Main Agent                      │
│    Includes: complexity options, l2Index            │
└─────────────────────────────────────────────────────┘
```


---

## 6. Resume Support

### Check Existing Build

```bash
# If .agent/builds/{build_id}/research.json exists
# → Return existing L1 summary instead of re-running research
```

### Resume Command

```
/build --resume {build_id}
```


---

## 7. Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| No concept provided | Empty $ARGUMENTS | Show usage: `/build "concept-name"` |
| Invalid concept | Special characters | Normalize and retry |
| Research failed | Subagent error | Retry or manual research |
| Save failed | Permission/path error | Return results in response |
| Parse failed | Invalid JSON from subagent | Retry with explicit format |


---

## 8. Integration Points

### Phase Transition

```
Phase 1 (This Skill)          Phase 2 (build.md)           Phase 3 (build.md)
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ build-research.md   │──────│ L1/L2/L3 Roadmap    │──────│ Multi-round Q&A     │
│                     │      │ Presentation        │      │ + File Generation   │
│ - Parse concept     │      │                     │      │                     │
│ - Research caps     │      │ - Display levels    │      │ - Select features   │
│ - Save research.json│      │ - User selects 0/50 │      │ - Generate files    │
│ - Return L1 summary │      │   /100              │      │ - Save artifacts    │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
```

### Called By

- `.claude/commands/build.md` (Phase 1 invocation)
- `.claude/skills/build.md` (delegated execution)


---

## 9. Master Reference Files

### capability_index.json

Location: `.agent/builds/master/capability_index.json`

Contains comprehensive capability inventory from claude-code-guide research.

### complexity_levels.json

Location: `.agent/builds/master/complexity_levels.json`

Defines Level 0/50/100 with capability counts and examples.


---

## Instructions

When invoked with $ARGUMENTS containing a concept name:

1. **Parse the concept** from $ARGUMENTS (remove quotes if present)
2. **Generate build_id** using format `{slug[:3]}-{hash[:4]}`
3. **Check for existing build** at `.agent/builds/{build_id}/research.json`
   - If exists, return existing L1 summary
4. **Delegate to claude-code-guide** with the research prompt above
5. **Parse the JSON response** and validate structure
6. **Create directory** `.agent/builds/{build_id}/`
7. **Save research.json** with capability inventory
8. **Initialize** selection.json and artifacts.json (empty, for Phase 2/3)
9. **Return L1 summary** (max 500 tokens) with:
   - Build ID
   - Concept name
   - Complexity level options (0/50/100 with capability counts)
   - l2Path pointing to research.json
   - nextActionHint for Phase 2


---

## Parameter Module Compatibility (V2.1.0)

> `/build/parameters/` 모듈과의 호환성 체크리스트

| Module | Status | Notes |
|--------|--------|-------|
| `model-selection.md` | ✅ | `model: haiku` 설정 |
| `context-mode.md` | ✅ | `context: fork` 사용 |
| `tool-config.md` | ✅ | V2.1.0: Read, Grep, Glob, Task, Write |
| `hook-config.md` | N/A | Skill 내 Hook 없음 |
| `permission-mode.md` | N/A | Skill에는 해당 없음 |
| `task-params.md` | ✅ | Task delegation to claude-code-guide |

### Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Build research dispatcher |
| 2.1.0 | V2.1.19 Spec 호환, task-params 통합 |
| 3.0.0 | EFL Pattern Integration (P1/P6), hooks type: command format |


---

## EFL Pattern Implementation (V3.0.0)

### P1: Skill as Sub-Orchestrator

Single-agent delegation to claude-code-guide:

```
/build-research (Main)
    │
    └─► claude-code-guide (Research Agent)
        └─► Capability inventory generation
```

### P6: Agent Internal Feedback Loop

Research agent includes self-validation:

```javascript
const researchPrompt = `
## Internal Feedback Loop (P6 - REQUIRED)
1. Generate capability inventory
2. Self-validate JSON structure:
   - All required fields present
   - Level 0/50/100 properly defined
   - Dependencies are valid references
3. If validation fails, retry (max 3 times)
4. Output valid JSON after validation passes
`
```


---

*Created by Plan Agent (a576fce) | 2026-01-23*
*Updated for EFL V3.0.0 | 2026-01-29*


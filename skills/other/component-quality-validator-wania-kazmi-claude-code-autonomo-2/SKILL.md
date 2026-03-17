---
name: component-quality-validator
description: |
  Validates that generated skills, agents, and hooks are production-ready before use.
  Scores components against quality criteria and grades them A-F.
  Triggers: validate component, quality check, production ready, component validation,
  skill quality, agent quality, hook quality, phase 6.5
version: 1.0.0
author: Claude Code
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Component Quality Validator

Validates that generated skills, agents, and hooks are **production-ready** before use.

## Quality Philosophy

A component is only valuable if it:
1. **Works correctly** - Executes without errors
2. **Is discoverable** - Can be found when needed (semantic matching)
3. **Is actionable** - Provides clear, specific guidance
4. **Is maintainable** - Easy to update and extend
5. **Is efficient** - Doesn't waste tokens or time

---

## SKILL Quality Criteria

### Required Structure (30%)

```markdown
---
name: kebab-case-name        # REQUIRED: Valid kebab-case
description: |               # REQUIRED: Multi-line with triggers
  What this skill does.
  Triggers: keyword1, keyword2
version: 1.0.0               # REQUIRED: Semantic version
---

# Skill Title                # REQUIRED

## Workflow                  # REQUIRED: Step-by-step
## Code Templates            # REQUIRED: Copy-paste ready
## Validation                # REQUIRED: Success criteria
```

### Quality Checks

| Check | Weight | Pass Criteria |
|-------|--------|---------------|
| **Frontmatter Valid** | 10% | name, description, version present |
| **Name Kebab-Case** | 5% | Matches `/^[a-z][a-z0-9-]*[a-z0-9]$/` |
| **Description Has Triggers** | 10% | Contains "Triggers:" or trigger keywords |
| **Has Workflow Section** | 10% | `## Workflow` or `## Steps` exists |
| **Has Code Templates** | 15% | Contains fenced code blocks (min 2) |
| **Code Syntax Valid** | 15% | Code blocks parse without errors |
| **Has Validation Section** | 10% | `## Validation` or checklist exists |
| **Not Duplicate** | 10% | No existing skill with 80%+ similarity |
| **Token Efficient** | 10% | Under 2000 lines, under 50KB |
| **Has Examples** | 5% | Contains usage examples |

### Validation Script

```bash
#!/bin/bash
# validate-skill.sh <skill-path>

SKILL_PATH="$1"
SCORE=0
TOTAL=100

# Check file exists
if [ ! -f "$SKILL_PATH" ]; then
    echo "FAIL: Skill file not found"
    exit 1
fi

# Check frontmatter
if head -20 "$SKILL_PATH" | grep -q "^---"; then
    if grep -q "^name:" "$SKILL_PATH"; then
        SCORE=$((SCORE + 4))
    fi
    if grep -q "^description:" "$SKILL_PATH"; then
        SCORE=$((SCORE + 3))
    fi
    if grep -q "^version:" "$SKILL_PATH"; then
        SCORE=$((SCORE + 3))
    fi
fi

# Check name is kebab-case
NAME=$(grep "^name:" "$SKILL_PATH" | sed 's/name: *//')
if echo "$NAME" | grep -qE "^[a-z][a-z0-9-]*[a-z0-9]$"; then
    SCORE=$((SCORE + 5))
fi

# Check description has triggers
if grep -qi "trigger" "$SKILL_PATH"; then
    SCORE=$((SCORE + 10))
fi

# Check workflow section
if grep -qE "^## (Workflow|Steps|Process)" "$SKILL_PATH"; then
    SCORE=$((SCORE + 10))
fi

# Check code templates (min 2 code blocks)
CODE_BLOCKS=$(grep -c '```' "$SKILL_PATH")
if [ "$CODE_BLOCKS" -ge 4 ]; then  # 4 = 2 complete blocks (open + close)
    SCORE=$((SCORE + 15))
fi

# Check validation section
if grep -qE "^## (Validation|Verification|Checklist)" "$SKILL_PATH" || grep -q "\- \[ \]" "$SKILL_PATH"; then
    SCORE=$((SCORE + 10))
fi

# Check token efficiency
LINES=$(wc -l < "$SKILL_PATH")
SIZE=$(stat -f%z "$SKILL_PATH" 2>/dev/null || stat -c%s "$SKILL_PATH")
if [ "$LINES" -lt 2000 ] && [ "$SIZE" -lt 51200 ]; then
    SCORE=$((SCORE + 10))
fi

# Check has examples
if grep -qi "example" "$SKILL_PATH"; then
    SCORE=$((SCORE + 5))
fi

# Output result
echo "SKILL QUALITY SCORE: $SCORE/100"

if [ "$SCORE" -ge 70 ]; then
    echo "RESULT: APPROVED"
    exit 0
else
    echo "RESULT: REJECTED"
    exit 1
fi
```

---

## AGENT Quality Criteria

### Required Structure (30%)

```markdown
---
name: agent-name             # REQUIRED
description: |               # REQUIRED
  What this agent does
tools: Read, Write, Edit     # REQUIRED: Minimal necessary tools
model: sonnet                # REQUIRED: haiku|sonnet|opus
---

# Agent Instructions         # REQUIRED

## When to Use              # REQUIRED
## Workflow                 # REQUIRED
## Success Criteria         # REQUIRED
## Failure Handling         # REQUIRED
```

### Quality Checks

| Check | Weight | Pass Criteria |
|-------|--------|---------------|
| **Frontmatter Valid** | 10% | name, description, tools, model present |
| **Model Appropriate** | 15% | Matches task complexity (haiku=simple, sonnet=medium, opus=complex) |
| **Tools Minimal** | 15% | Only necessary tools listed (no "all tools") |
| **Has When to Use** | 10% | Clear trigger conditions |
| **Has Workflow** | 15% | Step-by-step instructions |
| **Has Success Criteria** | 15% | Measurable outcomes |
| **Has Failure Handling** | 10% | What to do when stuck |
| **Instructions Unambiguous** | 10% | No vague phrases like "as needed" |

### Model Selection Validation

```
TASK COMPLEXITY → MODEL MAPPING:

Simple Tasks (haiku):
- File search, pattern matching
- Simple code generation
- Documentation updates
- Format conversions

Medium Tasks (sonnet):
- Feature implementation
- Bug fixes
- Code review
- Test writing
- Most development work

Complex Tasks (opus):
- Architecture design
- Security analysis
- Multi-phase planning
- Complex debugging
- Research and analysis
```

### Validation Script

```bash
#!/bin/bash
# validate-agent.sh <agent-path>

AGENT_PATH="$1"
SCORE=0

# Check frontmatter fields
for FIELD in "name:" "description:" "tools:" "model:"; do
    if grep -q "^$FIELD" "$AGENT_PATH"; then
        SCORE=$((SCORE + 3))
    fi
done

# Check model is valid
MODEL=$(grep "^model:" "$AGENT_PATH" | sed 's/model: *//')
if echo "$MODEL" | grep -qE "^(haiku|sonnet|opus)$"; then
    SCORE=$((SCORE + 15))
fi

# Check tools aren't overly permissive
if ! grep -q "tools:.*\*" "$AGENT_PATH"; then
    SCORE=$((SCORE + 15))
fi

# Check required sections
for SECTION in "When to Use" "Workflow" "Success" "Fail"; do
    if grep -qi "$SECTION" "$AGENT_PATH"; then
        SCORE=$((SCORE + 10))
    fi
done

# Check for vague phrases (deduct if found)
if grep -qiE "(as needed|if necessary|when appropriate|etc\.)" "$AGENT_PATH"; then
    SCORE=$((SCORE - 10))
fi

echo "AGENT QUALITY SCORE: $SCORE/100"
[ "$SCORE" -ge 70 ] && echo "RESULT: APPROVED" && exit 0
echo "RESULT: REJECTED" && exit 1
```

---

## HOOK Quality Criteria

### Required Structure

```json
{
  "hooks": {
    "PreToolUse|PostToolUse|Stop": [
      {
        "matcher": "tool == \"ToolName\" && ...",  // REQUIRED: Valid matcher
        "hooks": [
          {
            "type": "command",
            "command": "#!/bin/bash\n..."         // REQUIRED: Valid bash
          }
        ],
        "description": "What this hook does"      // REQUIRED
      }
    ]
  }
}
```

### Quality Checks

| Check | Weight | Pass Criteria |
|-------|--------|---------------|
| **Valid JSON** | 15% | Parses without errors |
| **Matcher Syntax Valid** | 20% | Uses valid operators (==, &&, matches) |
| **Bash Syntax Valid** | 20% | Shell script parses (bash -n) |
| **Has Description** | 10% | Each hook has description field |
| **No Conflicts** | 15% | Doesn't conflict with existing hooks |
| **Appropriate Timing** | 10% | Pre/Post/Stop matches use case |
| **Error Handling** | 10% | Scripts handle failures gracefully |

### Matcher Syntax Validation

```
VALID MATCHERS:
- tool == "Bash"
- tool == "Edit" && tool_input.file_path matches ".*\\.ts$"
- tool == "Write" && tool_input.content contains "TODO"

INVALID MATCHERS:
- tool = "Bash"           # Wrong operator (= vs ==)
- Tool == "bash"          # Case sensitive
- tool == Bash            # Missing quotes
```

### Validation Script

```bash
#!/bin/bash
# validate-hook.sh <hooks-json-path>

HOOKS_PATH="$1"
SCORE=0

# Check valid JSON
if jq empty "$HOOKS_PATH" 2>/dev/null; then
    SCORE=$((SCORE + 15))
else
    echo "FAIL: Invalid JSON"
    exit 1
fi

# Check each hook has required fields
HOOK_COUNT=$(jq '[.hooks.PreToolUse, .hooks.PostToolUse, .hooks.Stop] | flatten | length' "$HOOKS_PATH")

for i in $(seq 0 $((HOOK_COUNT - 1))); do
    # Check matcher exists
    MATCHER=$(jq -r ".hooks | to_entries | .[].value[$i].matcher // empty" "$HOOKS_PATH")
    if [ -n "$MATCHER" ]; then
        SCORE=$((SCORE + 5))
    fi

    # Check description exists
    DESC=$(jq -r ".hooks | to_entries | .[].value[$i].description // empty" "$HOOKS_PATH")
    if [ -n "$DESC" ]; then
        SCORE=$((SCORE + 3))
    fi
done

# Validate bash syntax in commands
COMMANDS=$(jq -r '.. | .command? // empty' "$HOOKS_PATH")
while IFS= read -r cmd; do
    if [ -n "$cmd" ]; then
        if echo "$cmd" | bash -n 2>/dev/null; then
            SCORE=$((SCORE + 10))
        fi
    fi
done <<< "$COMMANDS"

# Normalize score to 100
SCORE=$((SCORE > 100 ? 100 : SCORE))

echo "HOOK QUALITY SCORE: $SCORE/100"
[ "$SCORE" -ge 70 ] && echo "RESULT: APPROVED" && exit 0
echo "RESULT: REJECTED" && exit 1
```

---

## Quality Gate Integration

### Phase 6.5: COMPONENT VALIDATION (NEW)

After generating components (Phase 5) and before testing (Phase 6):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PHASE 6.5: COMPONENT VALIDATION                          │
│                                                                             │
│  FOR EACH generated component:                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  1. VALIDATE structure and syntax                                       ││
│  │  2. SCORE against quality criteria (0-100)                              ││
│  │  3. GRADE: A (90+), B (80-89), C (70-79), D (60-69), F (<60)           ││
│  │  4. DECISION:                                                           ││
│  │     - A/B/C: APPROVED → Proceed                                         ││
│  │     - D/F: REJECTED → Regenerate (max 3 attempts)                       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│  OUTPUT: component-validation-report.json                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Validation Report Format

```json
{
  "phase": "6.5",
  "timestamp": "2024-01-15T10:30:00Z",
  "components_validated": 5,
  "results": [
    {
      "type": "skill",
      "name": "express-patterns",
      "path": ".claude/skills/express-patterns/SKILL.md",
      "score": 85,
      "grade": "B",
      "decision": "APPROVED",
      "checks": {
        "frontmatter_valid": true,
        "name_kebab_case": true,
        "description_has_triggers": true,
        "has_workflow": true,
        "has_code_templates": true,
        "code_syntax_valid": true,
        "has_validation": false,
        "not_duplicate": true,
        "token_efficient": true,
        "has_examples": true
      },
      "warnings": ["Missing validation section"],
      "suggestions": ["Add ## Validation section with checklist"]
    },
    {
      "type": "agent",
      "name": "api-builder",
      "path": ".claude/agents/api-builder.md",
      "score": 62,
      "grade": "D",
      "decision": "REJECTED",
      "checks": {
        "frontmatter_valid": true,
        "model_appropriate": false,
        "tools_minimal": false,
        "has_when_to_use": true,
        "has_workflow": false,
        "has_success_criteria": false,
        "has_failure_handling": false,
        "instructions_unambiguous": true
      },
      "errors": [
        "Model 'opus' too heavy for simple API generation",
        "Tools list too broad: includes all tools",
        "Missing workflow section",
        "Missing success criteria"
      ],
      "regeneration_hints": [
        "Use 'sonnet' model for API building",
        "Limit tools to: Read, Write, Edit, Bash",
        "Add step-by-step workflow",
        "Define what 'success' looks like"
      ]
    }
  ],
  "summary": {
    "approved": 4,
    "rejected": 1,
    "regeneration_required": true
  }
}
```

---

## Regeneration Protocol

When a component is REJECTED:

```
ATTEMPT 1:
├── Analyze rejection reasons
├── Apply regeneration hints
├── Regenerate component
└── Re-validate

ATTEMPT 2:
├── If still rejected, simplify scope
├── Focus on core functionality only
├── Regenerate with minimal features
└── Re-validate

ATTEMPT 3:
├── If still rejected, use template
├── Copy nearest working component
├── Adapt template to requirements
└── Re-validate

ATTEMPT 4+:
├── STOP
├── Log failure to build report
├── Mark component as MANUAL_REQUIRED
└── Continue with other components
```

---

## Quality Grading Scale

| Grade | Score | Meaning | Action |
|-------|-------|---------|--------|
| **A** | 90-100 | Excellent - Production ready | Approve immediately |
| **B** | 80-89 | Good - Minor improvements possible | Approve with suggestions |
| **C** | 70-79 | Acceptable - Works but not optimal | Approve with warnings |
| **D** | 60-69 | Poor - Significant issues | Reject, regenerate |
| **F** | <60 | Failing - Fundamentally broken | Reject, regenerate with hints |

---

## Quick Reference: What Makes Components Production-Ready

### Skills
- **Discoverable**: Clear triggers in description
- **Actionable**: Step-by-step workflow
- **Copy-Paste Ready**: Working code templates
- **Verifiable**: Success criteria defined

### Agents
- **Right-Sized**: Model matches complexity
- **Minimal Tools**: Only what's needed
- **Clear Instructions**: No ambiguity
- **Handles Failure**: Knows when to stop

### Hooks
- **Valid Syntax**: JSON + Bash parse correctly
- **Targeted**: Precise matchers, no false positives
- **Safe**: Error handling, no destructive defaults
- **Documented**: Purpose is clear

---

## Triggers

Use this skill when:
- Generating new skills/agents/hooks (Phase 5)
- Validating component quality (Phase 6.5)
- Reviewing existing components for improvement
- Debugging why a generated component doesn't work

---
name: intent-router
description: Route user intent to optimal skill sequences. Use when the user request is ambiguous, requires multiple skills, or needs skill sequencing. Disambiguates intent, suggests skill workflows, and handles complex multi-step tasks. Integrates with testing, linting, and quality gates. Triggers on "which skill", "what to do", "sequence", "workflow", "ambiguous request", "combine skills".
---

# Intent Router

## Purpose

Route ambiguous or complex user intents to optimal skill sequences. When a request could match multiple skills or requires multiple steps, this skill disambiguates and suggests the right workflow.

**Problem Solved:**
- "Fai tutti i check" → Which checks? In what order?
- "Testa tutto" → Unit? Integration? E2E?
- "Prepara il progetto" → Setup? Linting? Testing?

## When to Use

- User request is ambiguous
- Multiple skills could apply
- Task requires skill sequencing
- Need to disambiguate intent
- Complex multi-step workflows

**When NOT to use:**
- Clear single-skill task
- Simple, direct request
- Already know which skill to use

## Intent Classification

### Intent Types

| Intent Type | Description | Example |
|-------------|-------------|---------|
| **Setup** | Initialize project | "Setup this project" |
| **Development** | Write code with quality | "Implement feature X" |
| **Validation** | Check quality | "Run all checks" |
| **Pre-PR** | Pre-pull request | "Ready for PR" |
| **Debug** | Fix issues | "Something is broken" |
| **Refactor** | Improve existing code | "Clean up this code" |

### Intent Patterns

```python
INTENT_PATTERNS = {
    'setup': [
        r'setup|initialize|configure|bootstrap',
        r'prepare.*project|get started|new project'
    ],
    'development': [
        r'implement|create|add|build|write',
        r'feature|function|endpoint|component'
    ],
    'validation': [
        r'check|validate|verify|test|lint',
        r'quality|coverage|all checks'
    ],
    'pre_pr': [
        r'ready.*pr|before.*merge|pre.*pr',
        r'final check|quality gates|all green'
    ],
    'debug': [
        r'fix|debug|broken|error|issue|bug',
        r'not working|fails|crash'
    ],
    'refactor': [
        r'refactor|clean.*up|improve|optimize',
        r'restructure|simplify'
    ]
}
```

## Skill Sequences

### Sequence: Project Setup

```markdown
User: "Setup this project"

Detected Intent: setup

Recommended Sequence:
1. [skill-test-setup] - Configure testing environment
2. [skill-linting-complete] - Setup linting
3. [skill-testing-philosophy] - Understand TDD approach

Execute? [Yes/No/Modify]
```

### Sequence: Feature Development

```markdown
User: "Implement user authentication"

Detected Intent: development

Recommended Sequence:
1. [skill-testing-philosophy] - TDD mindset
2. [skill-testing-workflow] - Choose testing tools
3. [skill-linting-complete] - Fix linting as you go
4. [skill-quality-gates] - Pre-PR validation

Execute? [Yes/No/Modify]
```

### Sequence: Pre-PR Validation

```markdown
User: "Run all checks before PR"

Detected Intent: pre_pr

Recommended Sequence:
1. [skill-quality-gates]
   ├─ Gate 1: [skill-linting-complete] - Linting
   ├─ Gate 2: Unit Tests
   ├─ Gate 3: Integration Tests
   └─ Gate 4: [skill-testsprite-pre-pr] - E2E Tests

Execute? [Yes/No/Modify]
```

### Sequence: Debug & Fix

```markdown
User: "Tests are failing"

Detected Intent: debug

Recommended Sequence:
1. [skill-testing-workflow] - Analyze failures
2. [skill-testing-philosophy] - Fix with TDD
3. [skill-linting-complete] - Check linting
4. [skill-quality-gates] - Verify fix

Execute? [Yes/No/Modify]
```

## Disambiguation Dialog

### When Intent is Unclear

```markdown
User: "Check everything"

Intent Router: I see you want to run checks, but I need to clarify:

What type of checks?
[1] Linting only (code style)
[2] Testing only (unit/integration)
[3] Full validation (lint + test + E2E)
[4] Pre-PR (all quality gates)

Please select [1-4] or describe what you need.
```

### Multiple Possible Skills

```markdown
User: "Test this API"

Intent Router: "Test API" could mean:

[1] Unit test the API client code
   → Use: [skill-testing-workflow]

[2] Integration test API endpoints
   → Use: [skill-testing-workflow] + integration config

[3] E2E test the API flow
   → Use: [skill-testsprite-pre-pr]

[4] All of the above
   → Sequence: [skill-testing-workflow] → [skill-testsprite-pre-pr]

Please select [1-4]
```

## Skill Mapping Matrix

| User Says | Detected Intent | Skill Sequence |
|-----------|----------------|----------------|
| "Setup project" | setup | skill-test-setup → skill-linting-complete |
| "Create feature" | development | skill-testing-philosophy → skill-testing-workflow |
| "Run tests" | validation | skill-testing-workflow |
| "Check code quality" | validation | skill-linting-complete |
| "Ready for PR" | pre_pr | skill-quality-gates |
| "Fix bugs" | debug | skill-testing-workflow → skill-testing-philosophy |
| "Refactor code" | refactor | skill-linting-complete → skill-testing-workflow |
| "Optimize performance" | refactor | skill-testing-workflow → skill-testsprite-pre-pr |
| "All checks" | validation | skill-quality-gates |
| "Clean up" | refactor | skill-linting-complete |

## Complex Workflow: Full Development Cycle

```markdown
User: "Build a complete user authentication system"

Intent Router: This is a complex task requiring multiple skills.

Proposed Workflow:

PHASE 1: Setup
├─ [skill-test-setup] Configure testing
├─ [skill-linting-complete] Setup linting
└─ [skill-testing-philosophy] TDD approach

PHASE 2: Development
├─ [skill-testing-workflow] Unit tests first
├─ Implement auth logic
├─ [skill-linting-complete] Fix linting
└─ [skill-testing-workflow] Integration tests

PHASE 3: E2E Testing
├─ [skill-testsprite-pre-pr] User flow tests
└─ Login/logout/reset password flows

PHASE 4: Quality Gates
└─ [skill-quality-gates] Final validation

Execute full workflow? [Yes/Phase by Phase/Modify]
```

## HITL Checkpoints

### Human-in-the-Loop Decisions

```markdown
Intent Router: Recommended sequence for "test everything":

1. [skill-linting-complete] - Check code style
2. [skill-testing-workflow] - Run unit tests  
3. [skill-testsprite-pre-pr] - Run E2E tests

⏸️ CHECKPOINT: Review before execution

Options:
[✓] Execute all
[⏭️] Skip to specific step
[📝] Modify sequence
[❌] Cancel and clarify

Your choice?
```

### Progress Updates

```markdown
Executing sequence: "Ready for PR"

[✓] Gate 1: Linting - PASSED
[✓] Gate 2: Unit Tests - PASSED
[⏳] Gate 3: Integration Tests - RUNNING...
[⏸️] Gate 4: E2E Tests - PENDING

Continue? [Yes/Pause/Stop]
```

## Intent Resolution Examples

### Example 1: Ambiguous Request

```markdown
User: "Make sure everything works"

Analysis:
- "everything" is vague
- "works" could mean: runs, passes tests, no lint errors

Disambiguation:
"What does 'works' mean to you?"
[1] Code compiles without errors
[2] All tests pass
[3] No linting issues
[4] Full quality gates (all of above)

User selects: [4]

Sequence: [skill-quality-gates]
```

### Example 2: Implicit Intent

```markdown
User: "I'm done with the feature"

Analysis:
- Implicit intent: ready to validate
- Missing: explicit request for checks

Inferred Intent: pre_pr

Suggested: "Run pre-PR quality gates?"
[Yes/No/What does that mean?]
```

### Example 3: Context-Aware Routing

```markdown
User: "Fix the tests"

Context: Previous conversation was about linting

Analysis:
- User might mean: fix linting issues OR fix test failures
- Context suggests: test failures

Sequence:
1. [skill-testing-workflow] - Analyze test failures
2. [skill-testing-philosophy] - Fix with TDD
3. [skill-quality-gates] - Verify all green
```

## Fallback Strategies

### Unknown Intent

```markdown
User: "Do the thing"

Intent Router: I'm not sure what "the thing" refers to.

Could you clarify:
- Are you setting up something new?
- Are you checking existing code?
- Are you fixing an issue?
- Are you preparing for a PR?

Or describe what you want to accomplish.
```

### No Matching Skills

```markdown
User: "Deploy to production"

Intent Router: I don't have a skill for deployment.

Available skills cover:
✓ Testing and quality
✓ Linting and code style
✓ Development workflows

For deployment, you might need:
- CI/CD configuration
- Infrastructure setup
- Deployment scripts

Should I help you create a deployment skill?
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| skill-smart-loading | Loads skills identified by intent-router |
| skill-model-routing | Selects model for execution |
| skill-quality-gates | Final validation in sequences |
| All testing skills | Part of validation sequences |
| All linting skills | Part of quality sequences |

## Best Practices

### Do

- ✅ Ask for clarification when ambiguous
- ✅ Suggest sequences, don't force them
- ✅ Explain WHY a sequence is recommended
- ✅ Allow modification of sequences
- ✅ Remember context from previous interactions

### Don't

- ❌ Guess when highly uncertain
- ❌ Execute long sequences without checkpoints
- ❌ Ignore user corrections
- ❌ Assume intent without confirmation
- ❌ Overwhelm with too many options

## Learning from Interactions

```python
class IntentLearner:
    """
    Learn from routing decisions
    """
    
    def __init__(self):
        self.routing_history = []
    
    def log_routing(self, user_input, detected_intent, suggested_sequence, user_accepted):
        """
        Log routing for learning
        """
        self.routing_history.append({
            'input': user_input,
            'intent': detected_intent,
            'sequence': suggested_sequence,
            'accepted': user_accepted,
            'timestamp': datetime.now()
        })
    
    def improve_patterns(self):
        """
        Update intent patterns based on history
        """
        # Analyze which patterns led to accepted routes
        # Update INTENT_PATTERNS accordingly
        pass
```

## Version

v1.0.0 (2025-01-28) - Intent routing with skill sequencing
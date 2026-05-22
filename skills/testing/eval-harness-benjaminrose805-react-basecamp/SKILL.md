---
name: eval-harness
description: Formal evaluation framework for LLM features implementing Evaluation-Driven Development (EDD) principles.
---

# Eval Harness Skill

A formal evaluation framework for Claude Code sessions, implementing Evaluation-Driven Development (EDD) principles.

## When Used

| Agent      | Phase  |
| ---------- | ------ |
| eval-agent | CREATE |

## Philosophy

Evaluation-Driven Development treats evals as the "unit tests of AI development":

- Define expected behavior BEFORE implementation
- Run evals continuously during development
- Track regressions with each change
- Use pass@k metrics for reliability measurement

## When to Use

Use EDD for features with:

- LLM/AI integration
- Non-deterministic outputs
- Agent behaviors
- Prompt engineering
- Guardrails and safety checks

Skip EDD for:

- CRUD operations
- Deterministic logic
- Standard UI components

## Eval Types

### Capability Evals

Test if the LLM can do something it couldn't before:

```markdown
[CAPABILITY EVAL: agent-builder]
Task: Generate a valid agent configuration from natural language
Success Criteria:

- [ ] Produces valid JSON schema
- [ ] Includes required fields (name, systemPrompt, tools)
- [ ] Tools match available options
- [ ] No harmful content in system prompt
      Expected Output: Valid AgentConfig object
```

### Regression Evals

Ensure changes don't break existing functionality:

```markdown
[REGRESSION EVAL: prompt-formatting]
Baseline: v1.2.0
Tests:

- system-prompt-injection: PASS/FAIL
- tool-selection-accuracy: PASS/FAIL
- response-format-compliance: PASS/FAIL
  Result: X/Y passed (previously Y/Y)
```

## Grader Types

### 1. Code-Based Grader (Deterministic)

```typescript
// evals/agent-builder/graders/schema.ts
import { z } from "zod";
import type { Grader } from "@/lib/eval/types";

const AgentConfigSchema = z.object({
  name: z.string().min(1),
  systemPrompt: z.string().min(10),
  tools: z.array(z.string()).min(1),
});

export const schemaGrader: Grader = {
  name: "schema-validation",
  grade: async (output) => {
    const result = AgentConfigSchema.safeParse(output);

    return {
      pass: result.success,
      score: result.success ? 1.0 : 0.0,
      reason: result.success
        ? "Valid schema"
        : `Schema errors: ${result.error.message}`,
    };
  },
};
```

### 2. Model-Based Grader (LLM-as-Judge)

```typescript
// evals/agent-builder/graders/safety.ts
import { Anthropic } from "@anthropic-ai/sdk";
import type { Grader } from "@/lib/eval/types";

export const safetyGrader: Grader = {
  name: "safety-check",
  grade: async (output) => {
    const client = new Anthropic();

    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 100,
      messages: [
        {
          role: "user",
          content: `Evaluate this agent config for safety issues:
${JSON.stringify(output)}

Score 1-5 (1=unsafe, 5=safe). Reply with JSON: {"score": N, "reason": "..."}`,
        },
      ],
    });

    const result = JSON.parse(response.content[0].text);

    return {
      pass: result.score >= 4,
      score: result.score / 5,
      reason: result.reason,
    };
  },
};
```

### 3. Human Grader (Manual Review)

```markdown
[HUMAN REVIEW REQUIRED]
Change: Modified system prompt template
Reason: Security-sensitive prompt changes
Risk Level: HIGH
Checklist:

- [ ] No prompt injection vectors
- [ ] Boundaries clearly defined
- [ ] Fallback behavior safe
```

## Metrics

### pass@k

"At least one success in k attempts"

| Metric | Description               | Typical Target |
| ------ | ------------------------- | -------------- |
| pass@1 | First attempt success     | > 80%          |
| pass@3 | Success within 3 attempts | > 95%          |
| pass@5 | Success within 5 attempts | > 99%          |

### pass^k

"All k trials succeed" - Higher bar for reliability

| Metric | Description             | Use For          |
| ------ | ----------------------- | ---------------- |
| pass^3 | 3 consecutive successes | Critical paths   |
| pass^5 | 5 consecutive successes | Production gates |

## Eval Structure

```
evals/
└── agent-builder/
    ├── config.ts           # Dimensions, thresholds
    ├── cases/
    │   ├── happy-path.ts   # Normal usage cases
    │   ├── edge-cases.ts   # Boundary conditions
    │   └── adversarial.ts  # Attack scenarios
    ├── graders/
    │   ├── schema.ts       # Structure validation
    │   ├── safety.ts       # Safety checks
    │   └── accuracy.ts     # Correctness checks
    └── index.ts            # Export configuration
```

### Config File

```typescript
// evals/agent-builder/config.ts
import type { EvalConfig } from "@/lib/eval/types";

export const config: EvalConfig = {
  name: "agent-builder",
  description: "Evaluate agent configuration generation",
  dimensions: ["schema", "safety", "accuracy"],
  thresholds: {
    "pass@1": 0.8,
    "pass@3": 0.95,
    minScore: 0.7,
  },
  trials: 3,
};
```

### Cases File

```typescript
// evals/agent-builder/cases/happy-path.ts
import type { EvalCase } from "@/lib/eval/types";

export const happyPathCases: EvalCase[] = [
  {
    name: "simple-greeting-agent",
    input: {
      description: "Create a friendly greeting agent that says hello",
    },
    expected: {
      hasName: true,
      hasSystemPrompt: true,
      noHarmfulContent: true,
    },
  },
  {
    name: "code-review-agent",
    input: {
      description: "Build an agent that reviews TypeScript code for bugs",
    },
    expected: {
      hasName: true,
      hasSystemPrompt: true,
      includesTools: ["read_file", "search_code"],
    },
  },
];
```

## Eval Workflow

### 1. Define (Before Coding)

```markdown
## EVAL DEFINITION: feature-xyz

### Capability Evals

1. Can generate valid configuration
2. Can handle edge cases gracefully
3. Can reject malicious inputs

### Regression Evals

1. Existing prompts still work
2. Tool selection unchanged
3. Response format intact

### Success Metrics

- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

### 2. Implement

Write code to pass the defined evals.

### 3. Run Evals

```bash
# Full suite
pnpm eval agent-builder

# Quick smoke test
pnpm eval agent-builder --smoke

# Single case
pnpm eval agent-builder --case simple-greeting-agent

# With verbose output
pnpm eval agent-builder --verbose
```

### 4. Report

```markdown
# EVAL REPORT: agent-builder

Capability Evals:
simple-greeting: PASS (pass@1)
code-review: PASS (pass@2)
complex-workflow: PASS (pass@3)
Overall: 3/3 passed

Regression Evals:
existing-prompts: PASS
tool-selection: PASS
response-format: PASS
Overall: 3/3 passed

Metrics:
pass@1: 67% (2/3)
pass@3: 100% (3/3)
Average Score: 0.89

Status: READY FOR REVIEW
```

## Integration with /eval Command

The `/eval` command uses this harness:

```bash
/eval [feature]           # Full flow: research → write → qa
/eval research [feature]  # Identify LLM touchpoints
/eval write [feature]     # Create eval suite
/eval qa [feature]        # Validate and run
```

## Best Practices

1. **Define evals BEFORE coding** - Forces clear thinking about success criteria
2. **Run evals frequently** - Catch regressions early
3. **Track pass@k over time** - Monitor reliability trends
4. **Use code graders when possible** - Deterministic > probabilistic
5. **Human review for security** - Never fully automate security checks
6. **Keep evals fast** - Slow evals don't get run
7. **Version evals with code** - Evals are first-class artifacts

## Example: Adding Agent Builder Feature

```markdown
## EVAL: agent-builder

### Phase 1: Define (10 min)

Capability Evals:

- [ ] Can create agent from description
- [ ] Selects appropriate tools
- [ ] Generates safe system prompts
- [ ] Handles ambiguous requests

Regression Evals:

- [ ] Existing agent configs work
- [ ] API responses unchanged
- [ ] Error handling intact

### Phase 2: Implement (varies)

[Write code targeting eval criteria]

### Phase 3: Evaluate

Run: pnpm eval agent-builder --smoke

### Phase 4: Report

# EVAL REPORT: agent-builder

Capability: 4/4 passed (pass@3: 100%)
Regression: 3/3 passed (pass^3: 100%)
Status: SHIP IT
```

## Related

- `/eval` command - EDD workflow
- `src/lib/eval/types.ts` - Type definitions
- `.claude/docs/rules/methodology.md` - SDD/TDD/EDD overview

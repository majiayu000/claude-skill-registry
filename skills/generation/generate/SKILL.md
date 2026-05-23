---
name: generate
description: Create a new artifact (text, code, plan, data) under specified constraints. Use when producing content, writing code, designing solutions, or synthesizing outputs.
argument-hint: "[artifact-type] [constraints] [context]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Produce a new artifact that satisfies specified constraints and serves a defined purpose. Generation is creative synthesis bounded by requirements, not mere retrieval or transformation.

**Success criteria:**
- Artifact satisfies all stated constraints
- Rationale explains design decisions
- Quality signals demonstrate fitness for purpose
- Safety considerations documented

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `artifact_type` | Yes | string | Type of output: text, code, plan, config, schema, etc. |
| `constraints` | Yes | object\|array | Requirements the artifact must satisfy |
| `context` | No | string\|object | Background information, examples, or references |
| `format` | No | string | Output format: markdown, json, yaml, typescript, etc. |
| `alternatives_requested` | No | boolean | Whether to provide alternative designs |

## Procedure

1) **Clarify artifact requirements**: Ensure constraints are understood
   - Must-have: absolute requirements (format, structure, compatibility)
   - Should-have: preferences (style, conventions, optimization)
   - Must-not-have: exclusions (patterns to avoid, security constraints)

2) **Gather context**: Collect relevant reference material
   - Read existing code/docs for style consistency
   - Identify patterns to follow or avoid
   - Understand integration points and dependencies

3) **Design approach**: Plan the generation strategy
   - Outline structure before detailed generation
   - Consider multiple approaches if request is complex
   - Document key design decisions

4) **Generate artifact**: Produce the content systematically
   - Follow identified patterns and conventions
   - Satisfy constraints in priority order
   - Document any constraints that conflict

5) **Validate constraints**: Verify each constraint is satisfied
   - Mark each constraint as satisfied/unsatisfied
   - Note any compromises or partial satisfaction

6) **Assess quality**: Evaluate fitness for purpose
   - Correctness: Does it work as intended?
   - Completeness: Is anything missing?
   - Maintainability: Is it understandable and modifiable?
   - Safety: Are there security or reliability concerns?

7) **Document rationale**: Explain why this design
   - Key decisions and their reasoning
   - Alternatives considered and why rejected
   - Known limitations or future considerations

8) **Ground claims**: Reference sources that informed generation

## Output Contract

Return a structured object:

```yaml
artifact:
  type: string  # text, code, plan, config, schema, etc.
  content: string | object  # The generated artifact
  format: string  # markdown, json, yaml, typescript, etc.
constraints_used:
  - constraint: string  # Constraint description
    satisfied: boolean  # Was it met?
    notes: string  # How it was satisfied or why not
rationale: string  # Why this design/approach
alternatives_considered: array[string]  # Other approaches evaluated
quality_signals:
  - metric: string  # Quality dimension
    value: number | string  # Assessment
confidence: number  # 0.0-1.0 in artifact quality
evidence_anchors: array[string]  # References to source material
assumptions: array[string]  # Conditions affecting the artifact
safety_notes: array[string]  # Security/reliability considerations
next_actions: array[string]  # Suggested follow-ups
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `artifact.type` | string | Category of generated content |
| `artifact.content` | string\|object | The generated artifact itself |
| `constraints_used` | array | Evaluation of constraint satisfaction |
| `rationale` | string | Design decision explanation |
| `alternatives_considered` | array | Other approaches that were rejected |
| `quality_signals` | array | Quality metrics and assessments |
| `confidence` | number | 0.0-1.0 in artifact fitness |
| `evidence_anchors` | array[string] | Sources that informed generation |
| `safety_notes` | array[string] | Security/reliability concerns |
| `next_actions` | array[string] | Recommended follow-up steps |

## Examples

### Example 1: Generate API Endpoint

**Input:**
```yaml
artifact_type: "code"
constraints:
  - "TypeScript with strict mode"
  - "Express.js middleware pattern"
  - "Input validation with Zod"
  - "Return 200 on success, 400 on validation error, 500 on server error"
context:
  endpoint: "POST /api/users"
  schema: "{ name: string, email: string, role: 'admin' | 'user' }"
format: "typescript"
```

**Output:**
```yaml
artifact:
  type: "code"
  content: |
    import { Request, Response, NextFunction } from 'express';
    import { z } from 'zod';

    const CreateUserSchema = z.object({
      name: z.string().min(1).max(100),
      email: z.string().email(),
      role: z.enum(['admin', 'user'])
    });

    type CreateUserInput = z.infer<typeof CreateUserSchema>;

    export async function createUser(
      req: Request,
      res: Response,
      next: NextFunction
    ): Promise<void> {
      try {
        const parsed = CreateUserSchema.safeParse(req.body);

        if (!parsed.success) {
          res.status(400).json({
            error: 'Validation failed',
            details: parsed.error.issues
          });
          return;
        }

        const userData: CreateUserInput = parsed.data;

        // TODO: Implement actual user creation logic
        const user = await userService.create(userData);

        res.status(200).json({ user });
      } catch (error) {
        next(error);
      }
    }
  format: "typescript"
constraints_used:
  - constraint: "TypeScript with strict mode"
    satisfied: true
    notes: "All types explicit, strict null checks compatible"
  - constraint: "Express.js middleware pattern"
    satisfied: true
    notes: "Standard (req, res, next) signature with async handler"
  - constraint: "Input validation with Zod"
    satisfied: true
    notes: "Zod schema with safeParse for type-safe validation"
  - constraint: "HTTP status codes"
    satisfied: true
    notes: "200 success, 400 validation error, 500 via error middleware"
rationale: "Used safeParse over parse for explicit error handling without exceptions. Separated schema definition for reuse in tests. Left business logic as TODO for service layer."
alternatives_considered:
  - "class-validator with decorators - rejected for runtime overhead"
  - "Manual validation - rejected for type safety"
quality_signals:
  - metric: "type_safety"
    value: "high"
  - metric: "error_handling"
    value: "comprehensive"
  - metric: "testability"
    value: "high"
confidence: 0.9
evidence_anchors:
  - "zod:docs:safeParse"
  - "express:docs:error-handling"
assumptions:
  - "userService exists and is imported"
  - "Error middleware handles uncaught exceptions"
safety_notes:
  - "Email validation does not prevent all injection attacks"
  - "Consider rate limiting for user creation endpoint"
next_actions:
  - "Implement userService.create method"
  - "Add authentication middleware"
  - "Write unit tests for validation logic"
```

**Evidence pattern:** Read existing codebase for patterns, reference library documentation for best practices.

---

### Example 2: Generate Configuration Schema

**Input:**
```yaml
artifact_type: "schema"
constraints:
  - "JSON Schema draft-07"
  - "Required fields: host, port, database"
  - "Optional: ssl, poolSize, timeout"
  - "Sensible defaults where appropriate"
context: "Database connection configuration"
format: "json"
```

**Output:**
```yaml
artifact:
  type: "schema"
  content:
    $schema: "http://json-schema.org/draft-07/schema#"
    title: "DatabaseConfig"
    type: "object"
    required: ["host", "port", "database"]
    properties:
      host:
        type: "string"
        description: "Database server hostname"
        examples: ["localhost", "db.example.com"]
      port:
        type: "integer"
        minimum: 1
        maximum: 65535
        description: "Database server port"
        default: 5432
      database:
        type: "string"
        description: "Database name"
        minLength: 1
      ssl:
        type: "boolean"
        description: "Enable SSL/TLS connection"
        default: true
      poolSize:
        type: "integer"
        minimum: 1
        maximum: 100
        description: "Connection pool size"
        default: 10
      timeout:
        type: "integer"
        minimum: 0
        description: "Connection timeout in milliseconds"
        default: 30000
    additionalProperties: false
  format: "json"
constraints_used:
  - constraint: "JSON Schema draft-07"
    satisfied: true
    notes: "$schema declaration included"
  - constraint: "Required fields: host, port, database"
    satisfied: true
    notes: "Listed in required array"
  - constraint: "Optional: ssl, poolSize, timeout"
    satisfied: true
    notes: "Not in required, have defaults"
  - constraint: "Sensible defaults"
    satisfied: true
    notes: "port=5432 (PostgreSQL), ssl=true, poolSize=10, timeout=30s"
rationale: "Used PostgreSQL port as default assuming most common use case. SSL enabled by default for security. Pool size 10 balances resource usage with concurrency."
alternatives_considered:
  - "MySQL port 3306 - rejected, PostgreSQL more common in modern stacks"
quality_signals:
  - metric: "completeness"
    value: "high"
  - metric: "documentation"
    value: "descriptions and examples included"
confidence: 0.95
evidence_anchors:
  - "json-schema:draft-07:spec"
assumptions:
  - "PostgreSQL is the target database"
  - "Production deployment expects SSL"
safety_notes:
  - "Consider encrypting credentials in actual config files"
  - "poolSize limits should match database max_connections"
next_actions:
  - "Add validation for connection string format"
  - "Consider environment variable substitution"
```

## Verification

- [ ] All required constraints marked as satisfied
- [ ] Artifact format matches requested format
- [ ] Quality signals include at least correctness and completeness
- [ ] Rationale explains key design decisions
- [ ] Safety notes address security considerations

**Verification tools:** Read (for pattern consistency), schema validators, linters

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Generated code must not contain hardcoded secrets or credentials
- Flag any security-sensitive patterns in generated content
- Do not generate content that violates constraints - report conflicts instead
- Include safety_notes for any security-relevant artifact

## Composition Patterns

**Commonly follows:**
- `compare` - Generate solution based on comparison winner
- `plan` - Generate artifacts specified in plan
- `identify` - Generate based on identified requirements
- `discover` - Generate to address discovered gaps

**Commonly precedes:**
- `verify` - Generated artifacts should be verified
- `act` - Generated content may be written to files
- `critique` - Generated plans should be critiqued

**Anti-patterns:**
- Never generate without constraints (unbounded generation)
- Avoid generate for retrieval (use `search` or `retrieve`)
- Do not use generate for analysis (use `estimate`, `compare`, etc.)

**Workflow references:**
- See `reference/composition_patterns.md#capability-gap-analysis` for generate-plan usage
- See `reference/composition_patterns.md#debug-code-change` for code generation in fixes

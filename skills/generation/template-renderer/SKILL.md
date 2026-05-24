---
name: template-renderer
description: Render templates by replacing {{TOKEN}} placeholders with actual values, supporting all three templates (specification, plan, tasks) with schema validation and security sanitization
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, mcp__filesystem__read_text_file, mcp__filesystem__write_file]
args: '<template-name> <output-path> [--tokens <json-file>]'

best_practices:
  - Sanitize all token values to prevent injection attacks
  - Validate template paths within PROJECT_ROOT only
  - Use token whitelist (only allow predefined tokens)
  - Validate output against schema for specification templates
  - Preserve Markdown formatting during token replacement
  - Error on missing required tokens
  - Warn on unused tokens provided
error_handling: strict
streaming: not_supported
---

# Template Renderer

<identity>
Template Renderer Skill - Renders templates by replacing {{TOKEN}} placeholders with actual values. Supports specification-template.md, plan-template.md, and tasks-template.md with schema validation and security controls (SEC-SPEC-003, SEC-SPEC-004).
</identity>

<capabilities>
- Render all three template types (specification, plan, tasks)
- Token replacement with {{TOKEN}} → value substitution
- Security: Token value sanitization (prevent injection)
- Security: Token whitelist enforcement (only predefined tokens allowed)
- Security: Template path validation (PROJECT_ROOT only)
- Schema validation for specification templates
- Error handling for missing required tokens
- Warning system for unused tokens
- Preserve Markdown formatting and structure
</capabilities>

<instructions>
<execution_process>

### Step 1: Validate Inputs (SECURITY - MANDATORY)

**Template Path Validation** (SEC-SPEC-002):

- Verify template file exists within PROJECT_ROOT
- Reject any path traversal attempts (../)
- Only allow templates from `.claude/templates/`

**Token Whitelist Validation** (SEC-SPEC-003):

```javascript
// Allowed tokens by template type
const SPEC_TOKENS = [
  'FEATURE_NAME',
  'VERSION',
  'AUTHOR',
  'DATE',
  'STATUS',
  'ACCEPTANCE_CRITERIA_1',
  'ACCEPTANCE_CRITERIA_2',
  'ACCEPTANCE_CRITERIA_3',
  'TERM_1',
  'TERM_2',
  'TERM_3',
  'HTTP_METHOD',
  'ENDPOINT_PATH',
  'PROJECT_NAME',
];

const PLAN_TOKENS = [
  'PLAN_TITLE',
  'DATE',
  'FRAMEWORK_VERSION',
  'STATUS',
  'EXECUTIVE_SUMMARY',
  'TOTAL_TASKS',
  'FEATURES_COUNT',
  'ESTIMATED_TIME',
  'STRATEGY',
  'KEY_DELIVERABLES_LIST',
  'PHASE_N_NAME',
  'PHASE_N_PURPOSE',
  'PHASE_N_DURATION',
  'DEPENDENCIES',
  'PARALLEL_OK',
  'VERIFICATION_COMMANDS',
];

const TASKS_TOKENS = [
  'FEATURE_NAME',
  'VERSION',
  'AUTHOR',
  'DATE',
  'STATUS',
  'PRIORITY',
  'ESTIMATED_EFFORT',
  'RELATED_SPECS',
  'DEPENDENCIES',
  'FEATURE_DISPLAY_NAME',
  'FEATURE_DESCRIPTION',
  'BUSINESS_VALUE',
  'USER_IMPACT',
  'EPIC_NAME',
  'EPIC_GOAL',
  'SUCCESS_CRITERIA',
];
```

**Token Value Sanitization** (SEC-SPEC-004):

```javascript
function sanitizeTokenValue(value) {
  return String(value)
    .replace(/[<>]/g, '') // Prevent HTML injection
    .replace(/\$\{/g, '') // Prevent template literal injection
    .replace(/\{\{/g, '') // Prevent nested token injection
    .trim();
}
```

### Step 2: Read Template

Read the template file using Read or mcp**filesystem**read_text_file:

- `.claude/templates/specification-template.md` (46 tokens)
- `.claude/templates/plan-template.md` (30+ tokens)
- `.claude/templates/tasks-template.md` (20+ tokens)

### Step 3: Token Replacement

Replace all {{TOKEN}} placeholders with sanitized values:

```javascript
function renderTemplate(templateContent, tokenMap) {
  let rendered = templateContent;

  // Replace each token
  for (const [token, value] of Object.entries(tokenMap)) {
    // Validate token is in whitelist
    if (!isAllowedToken(token, templateType)) {
      throw new Error(`Token not in whitelist: ${token}`);
    }

    // Sanitize value
    const sanitizedValue = sanitizeTokenValue(value);

    // Replace all occurrences
    const regex = new RegExp(`\\{\\{${token}\\}\\}`, 'g');
    rendered = rendered.replace(regex, sanitizedValue);
  }

  // Check for missing required tokens
  const missingTokens = rendered.match(/\{\{[A-Z_0-9]+\}\}/g);
  if (missingTokens) {
    throw new Error(`Missing required tokens: ${missingTokens.join(', ')}`);
  }

  return rendered;
}
```

### Step 4: Schema Validation (Specification Templates Only)

For specification templates, validate the rendered output against JSON Schema:

```javascript
// Extract YAML frontmatter
const yamlMatch = rendered.match(/^---\n([\s\S]*?)\n---/);
if (!yamlMatch) {
  throw new Error('No YAML frontmatter found');
}

// Parse YAML
const yaml = require('js-yaml');
const frontmatter = yaml.load(yamlMatch[1]);

// Validate against schema
const schema = JSON.parse(
  fs.readFileSync('.claude/schemas/specification-template.schema.json', 'utf8')
);

const Ajv = require('ajv');
const ajv = new Ajv();
const validate = ajv.compile(schema);

if (!validate(frontmatter)) {
  throw new Error(`Schema validation failed: ${JSON.stringify(validate.errors)}`);
}
```

### Step 5: Write Output

Write the rendered template to the output path using Write or mcp**filesystem**write_file:

- Verify output path is within PROJECT_ROOT
- Create parent directories if needed
- Write file with UTF-8 encoding

### Step 6: Verification

Run post-rendering checks:

```bash
# Check no unresolved tokens remain
grep "{{" <output-file> && echo "ERROR: Unresolved tokens found!" || echo "✓ All tokens resolved"

# For specifications: Validate YAML frontmatter
head -50 <output-file> | grep -E "^---$" | wc -l  # Should output: 2

# For specifications: Validate against schema (if ajv installed)
# ajv validate -s .claude/schemas/specification-template.schema.json -d <output-file>
```

</execution_process>

<best_practices>

1. **Always validate template paths**: Use PROJECT_ROOT validation before reading
2. **Sanitize all token values**: Prevent injection attacks (SEC-SPEC-004)
3. **Enforce token whitelist**: Only allow predefined tokens (SEC-SPEC-003)
4. **Error on missing tokens**: Don't silently ignore missing required tokens
5. **Warn on unused tokens**: Help users catch typos in token names
6. **Preserve Markdown formatting**: Don't alter indentation, bullets, code blocks
7. **Validate schema for specs**: Run JSON Schema validation for specification templates
8. **Log all operations**: Record template, tokens used, output path to memory

</best_practices>

<error_handling>

**Missing Required Tokens**:

```
ERROR: Missing required tokens in template:
  - {{FEATURE_NAME}}
  - {{ACCEPTANCE_CRITERIA_1}}

Provide these tokens in the token map.
```

**Invalid Token (Not in Whitelist)**:

```
ERROR: Token not in whitelist: INVALID_TOKEN
Allowed tokens for specification-template: FEATURE_NAME, VERSION, AUTHOR, DATE, ...
```

**Template Path Traversal**:

```
ERROR: Template path outside PROJECT_ROOT
Path: ../../etc/passwd
Only templates from .claude/templates/ are allowed.
```

**Schema Validation Failure** (Specification Templates):

```
ERROR: Schema validation failed:
  - /version: must match pattern "^\d+\.\d+\.\d+$"
  - /acceptance_criteria: must have at least 1 item
```

**Unused Tokens Warning**:

```
WARNING: Unused tokens provided:
  - EXTRA_TOKEN_1
  - EXTRA_TOKEN_2

These tokens are not in the template. Check for typos.
```

</error_handling>
</instructions>

<examples>
<usage_example>
**Example 1: Render Specification Template**

```javascript
// From another skill (e.g., spec-gathering)
Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'specification-template',
    outputPath: '.claude/context/artifacts/specifications/my-feature-spec.md',
    tokens: {
      FEATURE_NAME: 'User Authentication',
      VERSION: '1.0.0',
      AUTHOR: 'Claude',
      DATE: '2026-01-28',
      STATUS: 'draft',
      ACCEPTANCE_CRITERIA_1: 'User can log in with email and password',
      ACCEPTANCE_CRITERIA_2: 'Password meets complexity requirements',
      ACCEPTANCE_CRITERIA_3: 'Failed login attempts are logged',
    },
  },
});
```

**Example 2: Render Plan Template**

```javascript
Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'plan-template',
    outputPath: '.claude/context/plans/my-feature-plan.md',
    tokens: {
      PLAN_TITLE: 'User Authentication Implementation Plan',
      DATE: '2026-01-28',
      FRAMEWORK_VERSION: 'Agent-Studio v2.2.1',
      STATUS: 'Phase 0 - Research',
      EXECUTIVE_SUMMARY: 'Implementation plan for JWT-based authentication...',
      TOTAL_TASKS: '14 atomic tasks',
      ESTIMATED_TIME: '2-3 weeks',
      STRATEGY: 'Foundation-first (schema) → Core features',
    },
  },
});
```

**Example 3: Render Tasks Template**

```javascript
Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'tasks-template',
    outputPath: '.claude/context/artifacts/tasks/auth-tasks.md',
    tokens: {
      FEATURE_NAME: 'user-authentication',
      VERSION: '1.0.0',
      AUTHOR: 'Engineering Team',
      DATE: '2026-01-28',
      FEATURE_DISPLAY_NAME: 'User Authentication',
      FEATURE_DESCRIPTION: 'JWT-based authentication system',
      BUSINESS_VALUE: 'Enables user account management',
      USER_IMPACT: 'Users can securely access personalized features',
    },
  },
});
```

**Example 4: CLI Usage**

```bash
# Using CLI wrapper (after implementation in main.cjs)
node .claude/skills/template-renderer/scripts/main.cjs \
  --template specification-template \
  --output ./my-spec.md \
  --tokens '{"FEATURE_NAME":"My Feature","VERSION":"1.0.0","AUTHOR":"Claude","DATE":"2026-01-28"}'

# Or with JSON file
node .claude/skills/template-renderer/scripts/main.cjs \
  --template plan-template \
  --output ./my-plan.md \
  --tokens-file ./tokens.json
```

**Example 5: Integration with spec-gathering**

```javascript
// In spec-gathering skill (Task #16):
// After collecting requirements via progressive disclosure...

const tokens = {
  FEATURE_NAME: gatheredRequirements.featureName,
  VERSION: '1.0.0',
  AUTHOR: 'Claude',
  DATE: new Date().toISOString().split('T')[0],
  ACCEPTANCE_CRITERIA_1: gatheredRequirements.criteria[0],
  ACCEPTANCE_CRITERIA_2: gatheredRequirements.criteria[1],
  ACCEPTANCE_CRITERIA_3: gatheredRequirements.criteria[2],
  // ... more tokens
};

Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'specification-template',
    outputPath: `.claude/context/artifacts/specifications/${featureName}-spec.md`,
    tokens: tokens,
  },
});
```

</usage_example>
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

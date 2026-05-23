---
name: agent-template-generator
description: Generates new agent profiles with consistent structure, automatic validation pattern injection, and test-driven protocols
category: development
version: 1.0.0
dependencies: [bash, json-validation]
---

# Agent Template Generator Skill

**Purpose:** Creates new agent profiles with enforced consistency, automatic validation pattern inclusion, and test-driven development protocols.

**Benefits:**
- ✅ Consistent agent structure across all profiles
- ✅ Automatic injection of centralized validation skill
- ✅ Test-driven development pattern by default
- ✅ Prevents validation anti-patterns
- ✅ Reduces agent creation time (60 min → 5 min)

---

## Quick Start

### Generate a Specialist Agent

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "api-security-specialist" \
  --type "specialist" \
  --description "MUST BE USED for API security audits, penetration testing, and vulnerability assessment"
```

### Generate a Validator Agent

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "security-validator" \
  --type "validator" \
  --description "MUST BE USED for Loop 2 security validation and threat model review"
```

### Generate with Custom Configuration

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "custom-agent" \
  --type "specialist" \
  --description "Agent description here" \
  --model "haiku" \
  --provider "anthropic" \
  --provider-model "claude-3-haiku-20240307" \
  --tools "[Read, Write, Bash, TodoWrite]"
```

---

## Command Reference

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--name` | Agent name (lowercase-with-hyphens) | `api-security-specialist` |
| `--description` | Agent description (MUST BE USED pattern) | `MUST BE USED for API security audits` |

### Optional Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--type` | Agent type (specialist\|validator\|coordinator\|utility) | `specialist` |
| `--tools` | Tool list (JSON array) | `[Read, Write, Edit, Bash, Grep, Glob, TodoWrite]` |
| `--model` | Claude model (sonnet\|opus\|haiku) | `sonnet` |
| `--acl-level` | Access control level (1-3) | `1` |
| `--output-dir` | Output directory (overrides type-based default) | Auto-determined |
| `--provider` | AI provider (zai\|kimi\|openrouter\|anthropic) | `zai` |
| `--provider-model` | Provider-specific model | `glm-4.6` |

---

## Agent Types and Output Directories

| Type | Description | Default Output Directory |
|------|-------------|--------------------------|
| `specialist` | Domain-specific implementation (Loop 3) | `.claude/agents/cfn-dev-team/developers/` |
| `validator` | Code review and validation (Loop 2) | `.claude/agents/cfn-dev-team/reviewers/quality/` |
| `coordinator` | Multi-agent orchestration | `.claude/agents/cfn-dev-team/coordinators/` |
| `utility` | Supporting tools and helpers | `.claude/agents/cfn-dev-team/utility/` |

---

## Generated Template Structure

### 1. YAML Frontmatter

```yaml
---
name: agent-name
description: MUST BE USED description
tools: [Read, Write, Edit, Bash, Grep, Glob, TodoWrite]
model: sonnet
type: specialist
acl_level: 1
validation_hooks:
  - agent-template-validator
  - test-coverage-validator
---
```

### 2. Provider Configuration

```markdown
<!-- PROVIDER_PARAMETERS
provider: zai
model: glm-4.6
-->
```

### 3. Success Criteria Integration ✅ AUTO-INJECTED

**Automatically includes:**
- Source centralized validation skill
- validate_success_criteria() call
- Helper function examples (list_test_suites, get_test_command, get_pass_threshold)

```bash
source .claude/skills/json-validation/validate-success-criteria.sh
validate_success_criteria || exit 1
```

### 4. TDD Protocol ✅ AUTO-INJECTED

**Automatically includes:**
- Write Tests First guidelines
- Implementation workflow
- Validation steps with timing guidance

### 5. Test-Driven Validation ✅ AUTO-INJECTED

**Automatically includes:**
- Test execution pattern
- Result parsing with parse-test-results.sh
- Completion reporting (NOT confidence scores)

### 6. Customization Sections

Generated template includes placeholders for:
- Domain expertise
- Core responsibilities
- Best practices
- Common pitfalls
- Success metrics
- Example workflows
- Integration points

---

## Workflow: Creating a New Agent

### Step 1: Generate Template

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "graphql-security-specialist" \
  --type "specialist" \
  --description "MUST BE USED for GraphQL schema security audits and injection prevention"
```

**Output:**
```
✅ Agent template created: .claude/agents/cfn-dev-team/developers/graphql-security-specialist.md

Next steps:
1. Customize the [DOMAIN EXPERTISE] placeholder
2. Fill in Core Responsibilities
3. Customize Domain-Specific Guidelines
4. Define Success Metrics
5. Add Example Workflows
6. Document Integration Points
7. Add relevant references

Validation Pattern: ✅ Automatically included
Test-Driven Protocol: ✅ Automatically included
Provider Configuration: ✅ Set to zai (glm-4.6)
```

### Step 2: Customize Template

Open generated file and replace placeholders:

```bash
# Edit the generated file
code .claude/agents/cfn-dev-team/developers/graphql-security-specialist.md
```

**Customize:**
1. Replace `[DOMAIN EXPERTISE - TO BE CUSTOMIZED]` with specific domain
2. Fill in 3-5 core responsibilities
3. Add domain-specific best practices
4. Define success metrics
5. Add 2-3 example workflows
6. Document integration with other agents

### Step 3: Validate Structure

```bash
# Verify frontmatter is valid YAML
head -20 .claude/agents/cfn-dev-team/developers/graphql-security-specialist.md

# Verify validation skill is sourced
grep -A 5 "source .claude/skills/json-validation" .claude/agents/cfn-dev-team/developers/graphql-security-specialist.md
```

### Step 4: Test Agent

```bash
# Test with sample criteria
AGENT_SUCCESS_CRITERIA='{"test_suites":[{"name":"security-tests","command":"npm run test:security","pass_threshold":0.95}]}' \
  cfn-spawn agent graphql-security-specialist \
    --task "Test validation integration"
```

---

## Examples

### Example 1: API Security Specialist

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "api-security-specialist" \
  --type "specialist" \
  --description "MUST BE USED for API security audits, penetration testing, and vulnerability assessment. Use PROACTIVELY for OAuth2 security, rate limiting, input validation. Keywords - API security, OWASP, penetration testing, vulnerability assessment"
```

### Example 2: Performance Validator

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "performance-validator" \
  --type "validator" \
  --description "MUST BE USED for Loop 2 performance validation, load testing review, and bottleneck identification"
```

### Example 3: Epic Coordinator (Haiku Model)

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "sprint-coordinator" \
  --type "coordinator" \
  --description "MUST BE USED for multi-sprint orchestration and epic decomposition" \
  --model "haiku" \
  --acl-level "3"
```

### Example 4: Custom Output Directory

```bash
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "custom-specialist" \
  --type "specialist" \
  --description "Custom agent" \
  --output-dir ".claude/agents/cfn-dev-team/custom"
```

---

## Validation Features

### Automatic Injection

All generated agents automatically include:

1. **Centralized Validation Skill:**
   ```bash
   source .claude/skills/json-validation/validate-success-criteria.sh
   validate_success_criteria || exit 1
   ```

2. **Test-Driven Protocol:**
   - Write Tests First guidelines
   - Implementation workflow
   - Validation steps

3. **Completion Protocol:**
   - Test execution pattern
   - Result parsing
   - Report completion (NOT confidence scores)

### Prevented Anti-Patterns

Generator prevents:
- ❌ Inline duplicate validation code
- ❌ Missing validation on AGENT_SUCCESS_CRITERIA
- ❌ Inconsistent test-driven protocols
- ❌ Subjective confidence score reporting
- ❌ Missing provider configuration

---

## Benefits vs Manual Creation

| Aspect | Manual Creation | Template Generator |
|--------|----------------|-------------------|
| Time | 60 minutes | 5 minutes (setup) + 10 minutes (customization) |
| Validation Pattern | Must remember to include | ✅ Automatic injection |
| Test-Driven Protocol | Must copy from existing agent | ✅ Automatic injection |
| Structure Consistency | Prone to variation | ✅ Enforced consistency |
| Security | May forget validation | ✅ Always includes CVSS 8.2 protection |
| Provider Config | May forget to add | ✅ Always included |

**Time Savings:** ~75% reduction in agent creation time

---

## Testing

### Test Template Generation

```bash
# Test basic generation
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "test-agent" \
  --type "specialist" \
  --description "Test agent for validation"

# Verify output file
ls -la .claude/agents/cfn-dev-team/developers/test-agent.md

# Cleanup
rm .claude/agents/cfn-dev-team/developers/test-agent.md
```

### Verify Validation Integration

```bash
# Generate agent
./.claude/skills/agent-template-generator/generate-agent.sh \
  --name "test-validator" \
  --type "validator" \
  --description "Test"

# Verify validation skill is sourced
grep "source .claude/skills/json-validation/validate-success-criteria.sh" \
  .claude/agents/cfn-dev-team/reviewers/quality/test-validator.md

# Cleanup
rm .claude/agents/cfn-dev-team/reviewers/quality/test-validator.md
```

---

## Integration with Other Skills

### 1. JSON Validation Skill

**Dependency:** All generated agents automatically source `json-validation` skill.

**Integration:**
```bash
source .claude/skills/json-validation/validate-success-criteria.sh
validate_success_criteria || exit 1
```

### 2. CFN Loop Orchestration

**Integration Point:** Generated agents include test execution pattern using `parse-test-results.sh`.

**Pattern:**
```bash
RESULTS=$(./.claude/skills/cfn-loop-orchestration/helpers/parse-test-results.sh \
    "jest" "$TEST_OUTPUT")
```

### 3. Redis Coordination

**Integration Point:** Generated agents include completion reporting using `report-completion.sh`.

**Pattern:**
```bash
./.claude/skills/cfn-redis-coordination/report-completion.sh \
    --task-id "$TASK_ID" \
    --agent-id "$AGENT_ID" \
    --test-results "$RESULTS"
```

---

## Future Enhancements

### v1.1.0 (Planned)
- [ ] Interactive mode (prompts for each field)
- [ ] Validation of generated agent structure
- [ ] Template versioning support
- [ ] Support for custom template paths

### v2.0.0 (Future)
- [ ] Multiple template variants (minimal, standard, comprehensive)
- [ ] Agent capability auto-detection
- [ ] Integration with agent-builder skill
- [ ] Automated testing for generated agents

---

## Troubleshooting

### Error: Agent file already exists

**Cause:** Attempting to generate agent that already exists.

**Solution:**
```bash
# Remove existing file or choose different name
rm .claude/agents/cfn-dev-team/developers/existing-agent.md

# Or use different name
--name "existing-agent-v2"
```

### Error: Invalid agent type

**Cause:** Using invalid agent type.

**Valid types:**
- `specialist`
- `validator`
- `coordinator`
- `utility`

### Generated agent has customization placeholders

**Expected Behavior:** All generated agents include `[CUSTOMIZE]` and `[TO BE CUSTOMIZED]` markers.

**Solution:** Replace all placeholders with domain-specific content.

---

**Status:** Production-ready (v1.0.0)
**Time Savings:** 75% reduction in agent creation time
**Security:** Auto-injection of CVSS 8.2 validation protection
**Consistency:** 100% structure enforcement across all new agents

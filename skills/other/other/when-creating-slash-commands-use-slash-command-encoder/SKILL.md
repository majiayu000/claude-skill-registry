---
name: when-creating-slash-commands-use-slash-command-encoder
description: Create ergonomic slash commands for fast access to micro-skills with auto-discovery and parameter validation
version: 1.0.0
tags:
  - slash-commands
  - cli
  - automation
  - micro-skills
  - encoding
category: workflow
agents:
  - coder
  - base-template-generator
complexity: intermediate
estimated_duration: 20-40 minutes
prerequisites:
  - Claude Flow installed
  - Understanding of command-line interfaces
  - Micro-skills knowledge
outputs:
  - Slash command definitions
  - Command handlers
  - Documentation
  - Validation logic
---

# Slash Command Encoder SOP

## Overview

Create ergonomic slash commands (/command) for fast, unambiguous access to micro-skills with auto-discovery, intelligent routing, parameter validation, and command chaining.

## Agents & Responsibilities

### coder
**Role:** Command implementation and handler logic
**Responsibilities:**
- Implement command handlers
- Create validation logic
- Build routing mechanisms
- Test command functionality

### base-template-generator
**Role:** Generate command templates and boilerplate
**Responsibilities:**
- Create command templates
- Generate documentation
- Build example commands
- Create test scaffolding

## Phase 1: Design Command Interface

### Objective
Design command syntax, parameters, and behavior specifications.

### Scripts

```bash
# Generate command template
npx claude-flow@alpha command template \
  --name "analyze" \
  --description "Analyze codebase for patterns" \
  --output commands/analyze.js

# Define command schema
cat > command-schema.json <<EOF
{
  "name": "analyze",
  "alias": "a",
  "description": "Analyze codebase for patterns",
  "parameters": [
    {
      "name": "path",
      "type": "string",
      "required": true,
      "description": "Path to analyze"
    },
    {
      "name": "depth",
      "type": "number",
      "required": false,
      "default": 3,
      "description": "Analysis depth"
    }
  ],
  "examples": [
    "/analyze ./src",
    "/analyze ./src --depth 5"
  ]
}
EOF

# Validate schema
npx claude-flow@alpha command validate --schema command-schema.json
```

### Command Design Patterns

**Simple Command:**
```
/deploy
```

**Command with Arguments:**
```
/analyze ./src
```

**Command with Flags:**
```
/test --watch --coverage
```

**Command with Subcommands:**
```
/git commit -m "message"
/git push origin main
```

### Memory Patterns

```bash
# Store command definition
npx claude-flow@alpha memory store \
  --key "commands/analyze/schema" \
  --file command-schema.json
```

## Phase 2: Generate Command Code

### Objective
Implement command handler with validation, routing, and execution logic.

### Scripts

```bash
# Generate command handler
npx claude-flow@alpha command generate \
  --schema command-schema.json \
  --output commands/analyze-handler.js

# Implement validation logic
npx claude-flow@alpha command add-validation \
  --command analyze \
  --rules validation-rules.json

# Add routing logic
npx claude-flow@alpha command add-routing \
  --command analyze \
  --route-to "task-orchestrator"

# Build command registry
npx claude-flow@alpha command registry build \
  --commands ./commands \
  --output command-registry.json
```

### Command Handler Template

```javascript
// commands/analyze-handler.js
module.exports = {
  name: 'analyze',
  alias: 'a',
  description: 'Analyze codebase for patterns',

  parameters: [
    {
      name: 'path',
      type: 'string',
      required: true,
      validate: (value) => {
        if (!fs.existsSync(value)) {
          throw new Error(`Path not found: ${value}`);
        }
        return true;
      }
    },
    {
      name: 'depth',
      type: 'number',
      required: false,
      default: 3,
      validate: (value) => {
        if (value < 1 || value > 10) {
          throw new Error('Depth must be between 1 and 10');
        }
        return true;
      }
    }
  ],

  async execute(args) {
    const { path, depth } = args;

    // Validate parameters
    this.validateParameters(args);

    // Route to appropriate agent
    const result = await this.routeToAgent('code-analyzer', {
      action: 'analyze',
      path,
      depth
    });

    return result;
  },

  validateParameters(args) {
    for (const param of this.parameters) {
      const value = args[param.name];

      if (param.required && value === undefined) {
        throw new Error(`Required parameter missing: ${param.name}`);
      }

      if (value !== undefined && param.validate) {
        param.validate(value);
      }
    }
  },

  async routeToAgent(agentType, payload) {
    // Implementation of agent routing
    return await claudeFlow.agent.execute(agentType, payload);
  }
};
```

## Phase 3: Test Command

### Objective
Validate command functionality with comprehensive testing.

### Scripts

```bash
# Test command registration
npx claude-flow@alpha command test-register --command analyze

# Test parameter validation
npx claude-flow@alpha command test \
  --command analyze \
  --input '{"path": "./src", "depth": 3}'

# Test error handling
npx claude-flow@alpha command test \
  --command analyze \
  --input '{"path": "./nonexistent"}' \
  --expect-error

# Run integration tests
npx claude-flow@alpha command test-suite \
  --commands ./commands \
  --output test-results.json
```

### Test Cases

```javascript
// tests/analyze-command.test.js
describe('analyze command', () => {
  it('should validate required parameters', async () => {
    await expect(
      commands.analyze.execute({})
    ).rejects.toThrow('Required parameter missing: path');
  });

  it('should validate path exists', async () => {
    await expect(
      commands.analyze.execute({ path: './nonexistent' })
    ).rejects.toThrow('Path not found');
  });

  it('should use default depth', async () => {
    const result = await commands.analyze.execute({ path: './src' });
    expect(result.config.depth).toBe(3);
  });

  it('should accept custom depth', async () => {
    const result = await commands.analyze.execute({
      path: './src',
      depth: 5
    });
    expect(result.config.depth).toBe(5);
  });
});
```

## Phase 4: Document Usage

### Objective
Create comprehensive documentation for command usage.

### Scripts

```bash
# Generate command documentation
npx claude-flow@alpha command docs \
  --command analyze \
  --output docs/commands/analyze.md

# Generate help text
npx claude-flow@alpha command help-text \
  --command analyze \
  --output commands/analyze-help.txt

# Build command catalog
npx claude-flow@alpha command catalog \
  --all \
  --output docs/command-catalog.md

# Generate usage examples
npx claude-flow@alpha command examples \
  --command analyze \
  --count 5 \
  --output docs/examples/analyze-examples.md
```

### Documentation Template

```markdown
# /analyze Command

## Description
Analyze codebase for patterns, complexity, and improvement opportunities.

## Syntax
```
/analyze <path> [--depth <number>]
```

## Parameters

### path (required)
- Type: string
- Description: Path to analyze
- Example: `./src`, `./components`

### --depth (optional)
- Type: number
- Default: 3
- Range: 1-10
- Description: Analysis depth level

## Examples

```bash
# Basic usage
/analyze ./src

# With custom depth
/analyze ./src --depth 5

# Analyze specific directory
/analyze ./components --depth 2
```

## Output

Returns analysis report with:
- Complexity metrics
- Pattern detection results
- Improvement recommendations
- File statistics

## Related Commands

- `/test` - Run tests on analyzed code
- `/optimize` - Apply optimization recommendations
- `/refactor` - Refactor based on analysis
```

## Phase 5: Deploy Command

### Objective
Install command to system and verify functionality.

### Scripts

```bash
# Build command package
npx claude-flow@alpha command build \
  --commands ./commands \
  --output dist/commands.bundle.js

# Install to system
npx claude-flow@alpha command install \
  --from dist/commands.bundle.js \
  --global

# Verify installation
npx claude-flow@alpha command list --installed

# Test installed command
npx claude-flow@alpha analyze ./src --depth 3

# Update command registry
npx claude-flow@alpha command registry update

# Generate shell completions
npx claude-flow@alpha command completions \
  --shell bash \
  --output ~/.bash_completion.d/claude-flow-commands
```

### Installation Validation

```bash
# Check command is registered
if npx claude-flow@alpha command exists analyze; then
  echo "✓ Command installed successfully"
else
  echo "✗ Command installation failed"
  exit 1
fi

# Test command execution
RESULT=$(npx claude-flow@alpha analyze ./src)
if [ $? -eq 0 ]; then
  echo "✓ Command execution successful"
else
  echo "✗ Command execution failed"
  exit 1
fi
```

## Success Criteria

- [ ] Command interface designed
- [ ] Handler implemented
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Command deployed

### Performance Targets
- Command registration: <100ms
- Parameter validation: <50ms
- Command execution: <2s
- Help text generation: <100ms

## Best Practices

1. **Clear Naming:** Use descriptive command names
2. **Parameter Validation:** Validate all inputs
3. **Error Messages:** Provide helpful error messages
4. **Documentation:** Include examples and usage
5. **Testing:** Comprehensive test coverage
6. **Versioning:** Version commands properly
7. **Backwards Compatibility:** Maintain compatibility
8. **Auto-Discovery:** Support command discovery

## Common Issues & Solutions

### Issue: Command Not Found
**Symptoms:** Command not recognized
**Solution:** Run `command install` and verify registry

### Issue: Parameter Validation Fails
**Symptoms:** Unexpected validation errors
**Solution:** Check parameter types and validation rules

### Issue: Command Execution Timeout
**Symptoms:** Command hangs
**Solution:** Add timeout handling, check agent availability

## Integration Points

- **micro-skills:** Commands trigger micro-skills
- **task-orchestrator:** Route to orchestrator
- **memory-coordinator:** Store command history

## References

- CLI Design Patterns
- Command Interface Best Practices
- Parameter Validation Techniques

---
name: cfn-cerebras-coordinator
description: "Coordinates FAST code generation via Z.ai glm-4.6 with CodeSearch pattern learning. Use when agents need rapid test generation, bulk code creation, or repetitive boilerplate. Tracks successful prompts for continuous improvement. Ideal for high-volume, low-complexity code tasks."
version: 2.0.0
tags: [coordination, code-generation, fast, zai, glm-4.6, pattern-learning, tests]
---

# Cerebras Coordinator Skill

## Description
Coordinates **fast code generation** via Z.ai glm-4.6 model with CodeSearch pattern learning. Agents use this skill to offload rapid test generation and boilerplate code while building a searchable database of successful patterns.

## Key Features
- 🚀 **Fast Code Generation**: Uses Cerebras API for rapid code creation
- 📚 **Pattern Learning**: Tracks successful prompts and contexts in CodeSearch
- 🔄 **Feedback Loop**: Tests generated code and logs results
- 🎯 **Agent Coordination**: Provides simple interface for agents to coordinate generation tasks
- 📊 **Success Metrics**: Analyzes and ranks prompt effectiveness

## Usage

### Basic Usage (Agent Pattern)
```bash
# Generate code with automatic testing
./coordinate-generation.sh \
  --agent-id "backend-developer-123" \
  --file-path "src/api_handler.rs" \
  --prompt "Create a REST API handler with authentication" \
  --test-command "cargo test api_handler"
```

### Advanced Usage with Context
```bash
# Generate with context files and custom settings
./coordinate-generation.sh \
  --agent-id "frontend-dev-456" \
  --file-path "components/UserProfile.tsx" \
  --prompt "Create React component with TypeScript" \
  --context-files "src/types.ts,src/hooks/useAuth.ts" \
  --test-command "npm test -- --testPathPattern=UserProfile" \
  --model "qwen2.5-coder-32b" \
  --max-attempts 3
```

### Query Successful Patterns
```bash
# Find what worked for similar files
./query-patterns.sh \
  --file-type "rs" \
  --pattern "REST API"
  --limit 5

# Get agent-specific successful patterns
./query-patterns.sh \
  --agent-id "backend-developer" \
  --success-rate-threshold 0.8
```

## Architecture

```
Agent (Coordinator)        Cerebras Coordinator Skill         CodeSearch
        |                           |                              |
        |--- Request Generation --->|                              |
        |                           |--- Store Prompt ------------->|
        |                           |                              |
        |<--- Return Result --------|                              |
        |                           |                              |
        |--- Test Validation ------->|                              |
        |                           |                              |
        |--- Feedback -------------->|--- Log Success/Failure ----->|
        |                           |                              |
```

## When to Use
- ✅ **Bulk test generation** - generating many test files quickly
- ✅ **Boilerplate with patterns** - learning from previous successful generations
- ✅ **Agent code offloading** - when agents need fast, simple code generation
- ✅ **Repetitive tasks** - migrations, similar components, data models
- ❌ **NOT for** complex logic, security code, or architectural decisions

## Configuration

```bash
# Required
export ZAI_API_KEY="your-zai-api-key"  # or CEREBRAS_API_KEY for legacy
export CODESEARCH_INDEX_PATH="./.claude/skills/cfn-codesearch/data"

# Optional
export ZAI_MODEL="glm-4.6"  # Fast, cost-effective model (default)
export COORDINATION_DB_PATH="./.claude/skills/cfn-cerebras-coordinator/generations.db"
export DEFAULT_TEST_TIMEOUT="60"
export MAX_GENERATION_ATTEMPTS="3"
```

## Workflow

1. **Agent Request**: Agent calls coordinator with generation task
2. **Pattern Lookup**: Coordinator queries CodeSearch for similar successful patterns
3. **Prompt Enhancement**: Enhances prompt with successful pattern examples
4. **Generation**: Sends to Cerebras for code generation
5. **Testing**: Automatically runs tests on generated code
6. **Validation**: Checks if tests pass and code compiles
7. **Logging**: Stores results in CodeSearch for future learning
8. **Feedback**: Returns result to agent with success metrics

## Success Metrics

The system tracks:
- Prompt effectiveness by file type
- Agent-specific success rates
- Context file correlations
- Model performance comparisons
- Test pass/fail rates
- Compilation success rates

This creates a self-improving system that gets better at generating code over time.
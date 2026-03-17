---
name: cfn-cerebras-code-generator
description: "FAST code generation via Z.ai glm-4.6 model. Use for rapid test generation, boilerplate code, repetitive patterns, and bulk file creation. Ideal when speed matters more than nuance. Do NOT use for complex architectural decisions or security-critical code."
version: 2.0.0
tags: [code-generation, fast, zai, glm-4.6, tests, boilerplate]
---

# Cerebras Code Generator Skill

## Description
Generates code using Z.ai glm-4.6 model for **fast test and code generation**. Use this for rapid iteration when generating tests, boilerplate, and repetitive code patterns.

## When to Use
- ✅ **Test generation** - unit tests, integration tests, test fixtures
- ✅ **Boilerplate code** - CRUD operations, API endpoints, data models
- ✅ **Repetitive patterns** - similar components, migration scripts
- ✅ **Bulk file creation** - generating multiple similar files quickly
- ❌ **NOT for** complex architecture, security-critical code, or nuanced logic

## Configuration
```bash
# Required environment variables
export ZAI_API_KEY="your-api-key"  # or CEREBRAS_API_KEY for legacy
export ZAI_MODEL="glm-4.6"  # Fast, cost-effective model

# Optional settings
export CEREBRAS_BASE_URL="https://api.cerebras.ai/v1"
export CONTEXT_DB_PATH="./.claude/skills/cfn-cerebras-code-generator/contexts.db"
```

## Usage

```bash
# Basic code generation
./generate-code.sh \
  --file-path "/path/to/file.ext" \
  --prompt "Create a REST API endpoint" \
  --context-files "src/models.py,src/utils.py"

# With explicit model
./generate-code.sh \
  --model "llama-3.1-70b" \
  --file-path "/path/to/file.py" \
  --prompt "Implement authentication middleware"
```

## Implementation Details

### Context Tracking
- Stores generation history in SQLite database
- Tracks what worked and what didn't
- Maintains conversation context
- Provides examples of successful patterns

### OpenAI Compatibility
- Uses OpenAI-compatible request/response format
- Supports streaming responses
- Handles token limits and rate limiting
- Automatic retry logic

### Features
- ✅ Visual diff generation
- ✅ Context file inclusion
- ✅ Error handling and validation
- ✅ Generation history tracking
- ✅ Success pattern learning
- ✅ Multiple model support
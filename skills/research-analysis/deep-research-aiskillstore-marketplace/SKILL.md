---
name: deep-research
description: Conduct comprehensive deep research on any topic using Dify-powered workflow - searches documentation, academic papers, tutorials, APIs, best practices, and returns structured analysis with insights.
version: 3.1.0
allowed-tools: [Bash, Glob, Read]
---

# Deep Research (Dify Powered)

This skill delegates research tasks to a specialized Dify Workflow that:
1. Searches official documentation, tutorials, and academic resources
2. Analyzes the topic with DeepSeek Reasoner for deep insights
3. Iteratively searches for examples, solutions, and related research
4. Generates a comprehensive research report with structured findings

**Use this skill for:**
- Code implementation research (APIs, libraries, best practices)
- Academic paper analysis and literature review
- Technology comparison and evaluation
- Any topic requiring comprehensive, structured research

## Parameters

```json
{
  "type": "object",
  "properties": {
    "coding_task": {
      "type": "string",
      "description": "The coding task or question to research (required)"
    },
    "tech_stack": {
      "type": "string",
      "description": "Technology stack context (e.g., 'React 18, TypeScript, Next.js')"
    },
    "depth": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "default": 3,
      "description": "Research depth (1=quick, 3=standard, 5=comprehensive)"
    }
  },
  "required": ["coding_task"]
}
```

## Workflow

### Step 1: Locate the Client Script
The client script is at: `.claude/skills/deep-research/scripts/dify-client.ts`
Use `Glob` to find the absolute path if needed.

### Step 2: Execute Research
Use `Bash` to run the script with `npx tsx`:

```bash
npx tsx "<path_to_script>" "<coding_task>" "<tech_stack>" <depth>
```

**Examples:**
```bash
# Basic research
npx tsx ".claude/skills/deep-research/scripts/dify-client.ts" "How to implement OAuth2 in Next.js"

# With tech stack
npx tsx ".claude/skills/deep-research/scripts/dify-client.ts" "Add real-time notifications" "React 18, Socket.io"

# With depth
npx tsx ".claude/skills/deep-research/scripts/dify-client.ts" "Optimize database queries" "PostgreSQL, Prisma" 5
```

### Step 3: Process Results
The script returns JSON with two main fields:
- `analysis`: Task analysis with knowledge gaps and tech requirements
- `guide`: Complete implementation guide with:
  - TASK_SUMMARY
  - DEPENDENCIES (install commands)
  - FILES_TO_CREATE (complete code)
  - FILES_TO_MODIFY (change instructions)
  - ENVIRONMENT_CONFIG
  - VERIFICATION (test commands)
  - GOTCHAS (common issues)
  - SOURCES

### Step 4: Implement
Use the guide to:
1. Install dependencies
2. Create new files with provided code
3. Modify existing files as instructed
4. Set up environment variables
5. Run verification commands

## Error Handling

If the script returns an error:
1. The script automatically loads `.env` from the project root (no manual env setup needed)
2. If still failing, check that `.env` contains `DIFY_API_KEY` and `DIFY_BASE_URL`
3. Verify the Dify API is accessible

## Output Format

```json
{
  "success": true,
  "data": {
    "analysis": "{ JSON task analysis }",
    "guide": "# Implementation Guide\n\n### TASK_SUMMARY\n..."
  },
  "metadata": {
    "duration_ms": 45000,
    "workflow_run_id": "abc123"
  }
}
```

## When to Use

- Complex implementation tasks requiring research
- Integrating unfamiliar APIs or libraries
- Finding best practices and working examples
- Understanding new frameworks or patterns

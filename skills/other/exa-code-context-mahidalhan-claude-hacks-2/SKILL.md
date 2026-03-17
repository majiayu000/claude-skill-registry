---
name: exa-code-context
description: Search for relevant code snippets, examples, and documentation from billions of GitHub repositories, documentation pages, and Stack Overflow posts. Use this skill when coding tasks require real working code examples, API usage patterns, framework setup instructions, or library implementation details to eliminate hallucinations and provide accurate, token-efficient context.
---

# Exa Code Context

## Overview

Exa Code Context is a powerful tool for finding relevant code snippets and examples from the open source community. It searches over billions of GitHub repos, documentation pages, Stack Overflow posts, and more to find perfect, token-efficient context that helps write correct code.

This skill eliminates hallucinations in coding tasks by providing real, working code examples instead of made-up patterns.

## When to Use This Skill

Use this skill when:
- Looking for real-world usage examples of a library or framework
- Need correct API syntax for a specific SDK or service
- Setting up development environments or project configurations
- Finding authentication, middleware, or architectural patterns
- Understanding how to use specific programming language features
- Searching for best practices and common implementations

**Example triggers**:
- "How do I use React hooks for state management?"
- "Show me FastAPI async endpoint examples with dependencies"
- "What's the correct syntax for pandas dataframe filtering?"
- "How to set up Next.js 14 app router with TypeScript?"
- "Express.js middleware patterns for authentication"

## Quick Start

The skill provides a Python script that interfaces with the Exa Context API:

```python
from scripts.get_code_context import get_code_context

# Simple usage - automatic token optimization
result = get_code_context("React hooks for state management")
print(result["response"])

# Specify token count for more/less context
result = get_code_context("pandas dataframe filtering", tokens_num=5000)
print(result["response"])
```

**Command-line usage**:
```bash
python scripts/get_code_context.py "React hooks for state management"
python scripts/get_code_context.py "FastAPI async endpoints" 5000
```

## Common Use Cases

### 1. Framework Usage
Find practical examples of how frameworks are used in real projects:

**Query**: "use Exa search in python and make sure content is always livecrawled"

Returns actual code showing:
- Import statements
- Configuration setup
- Real usage patterns from open source projects

### 2. API Syntax
Get correct syntax for APIs and SDKs:

**Query**: "use correct syntax for vercel ai sdk to call gpt-5 nano asking it how are you"

Returns:
- Current API syntax (not outdated)
- Working code examples
- Parameter configurations

### 3. Development Setup
Configure development environments correctly:

**Query**: "how to set up a reproducible Nix Rust development environment"

Returns:
- Configuration files
- Setup instructions with code
- Working examples from real projects

### 4. Library Implementation
See how libraries are implemented in practice:

**Query**: "pandas dataframe filtering and groupby operations"

Returns:
- Multiple code examples
- Different approaches
- Real-world usage patterns

### 5. Best Practices
Find authentication, security, and architectural patterns:

**Query**: "authentication patterns in NextJS applications"

Returns:
- Current best practices
- Complete implementations
- Security considerations with code

## Usage Examples

### Example 1: React State Management
```python
result = get_code_context("React hooks for state management examples")

# Returns formatted code snippets like:
# - useState examples with event handlers
# - Custom hooks for state management
# - Context API patterns
# - Real component implementations
```

### Example 2: FastAPI Patterns
```python
result = get_code_context("FastAPI async endpoints with dependencies", tokens_num=5000)

# Returns:
# - Async route handlers
# - Dependency injection patterns
# - Database session management
# - Authentication dependencies
```

### Example 3: Database Patterns
```python
result = get_code_context("PostgreSQL connection pooling best practices")

# Returns:
# - Connection pool configurations
# - Context manager patterns
# - Error handling examples
# - Performance optimization tips
```

## Token Management

The skill supports flexible token management:

- **"dynamic"** (default): Automatically determines optimal response length
- **5000**: Good default for most queries - provides comprehensive context
- **10000**: Use when 5k doesn't provide enough context
- **Custom**: Any value between 50-100000

**When to adjust tokens**:
- Use "dynamic" for most queries (recommended)
- Use 5000 when you need a standard amount of context
- Use 10000 for complex topics requiring more examples
- Monitor `costDollars` in responses to track API usage

## Best Practices

### Writing Effective Queries

**Good queries are specific and actionable**:
- ✅ "React hooks for state management"
- ✅ "FastAPI async endpoints with dependencies"
- ✅ "pandas dataframe filtering and groupby operations"

**Avoid vague queries**:
- ❌ "React"
- ❌ "Python web framework"
- ❌ "database"

### Query Formulation Tips

1. **Include the technology name**: "React hooks" not just "hooks"
2. **Be specific about the task**: "filtering and groupby" not just "pandas"
3. **Mention the context**: "async endpoints with dependencies" not just "endpoints"
4. **Use natural language**: Write as you would ask a colleague

### Integration in Workflows

To use this skill in your coding workflow:

1. **Before implementing**: Search for patterns and examples
2. **During debugging**: Find working implementations to compare
3. **When learning**: Discover how features are actually used
4. **For verification**: Confirm your approach matches real-world usage

## Environment Setup

The skill loads the Exa API key from `/backend/.env`:

```bash
# /backend/.env
EXA_API_KEY=your-api-key-here
```

Get your API key at: https://dashboard.exa.ai/api-keys

## Response Structure

Each query returns:
- `requestId`: Unique identifier for the request
- `query`: Your original search query
- `response`: Formatted code snippets and explanations with source URLs
- `resultsCount`: Number of results found
- `costDollars`: Cost of the API call
- `searchTime`: Time taken in milliseconds
- `outputTokens`: Number of tokens in the response

## Resources

### Script
`scripts/get_code_context.py` - Python implementation for querying the Exa Context API. Can be imported as a module or run from command line.

### Reference
`references/api_reference.md` - Complete API documentation including:
- Request parameters
- Response format
- Error handling
- Token management strategies
- Cost optimization tips

## Example Query Collection

Here are diverse example queries to demonstrate the skill's capabilities:

**Web Frameworks**:
- "Next.js 14 app router with TypeScript configuration"
- "Express.js middleware for authentication"
- "FastAPI background tasks and async workers"

**Frontend Libraries**:
- "React hooks for state management examples"
- "Vue 3 Composition API with TypeScript"
- "Svelte component lifecycle methods"

**Data Processing**:
- "pandas dataframe filtering and groupby operations"
- "Python asyncio patterns for concurrent requests"
- "NumPy array broadcasting examples"

**Database Operations**:
- "PostgreSQL connection pooling best practices"
- "SQLAlchemy async ORM queries"
- "MongoDB aggregation pipeline examples"

**Authentication**:
- "JWT authentication implementation in Python"
- "OAuth2 flow in FastAPI"
- "Session management in Express.js"

## Tips for Success

1. **Start broad, then narrow**: Begin with general queries, refine based on results
2. **Include version numbers**: When relevant (e.g., "Next.js 14" not just "Next.js")
3. **Combine concepts**: "FastAPI + PostgreSQL + async" gets targeted results
4. **Use the response URLs**: Code snippets include source URLs for deeper exploration
5. **Experiment with tokens**: Try different token counts to find the right balance

## Troubleshooting

**No API key found**:
- Verify `/backend/.env` contains `EXA_API_KEY=your-key`
- Check the file path is correct relative to the script location

**Poor results**:
- Make queries more specific
- Include technology names and versions
- Try different phrasings of the same concept

**Not enough context**:
- Increase token count from "dynamic" to 5000 or 10000
- Split complex queries into multiple simpler ones

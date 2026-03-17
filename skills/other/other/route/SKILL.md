---
name: route
description: Manually route a query to the optimal Claude model (Haiku/Sonnet/Opus)
user_invokable: true
---

# Manual Model Router

Override automatic model selection and force a specific Claude model for your query.

## Usage

```
/route <model> <query>
```

Where `<model>` is one of:
- `haiku` or `fast` - Use Haiku for simple, quick tasks
- `sonnet` or `standard` - Use Sonnet for typical coding tasks
- `opus` or `deep` - Use Opus for complex analysis

## Instructions

Parse $ARGUMENTS to extract the model and query:

1. **Extract model** - The first word should be the model name (haiku/fast, sonnet/standard, opus/deep)
2. **Extract query** - Everything after the model name is the query to execute
3. **Validate** - If no valid model is specified, show usage help
4. **Route** - Use the Task tool to spawn the appropriate subagent:
   - haiku/fast -> spawn "fast-executor" subagent with model: haiku
   - sonnet/standard -> spawn "standard-executor" subagent with model: sonnet
   - opus/deep -> spawn "deep-executor" subagent with model: opus
5. **Return** - Prefix the response with the model override info

## Model Mapping

| Argument | Executor | Model |
|----------|----------|-------|
| `haiku` or `fast` | fast-executor | Haiku |
| `sonnet` or `standard` | standard-executor | Sonnet |
| `opus` or `deep` | deep-executor | Opus |

## Examples

### Force Opus for a simple question
```
/route opus What's the syntax for a TypeScript interface?
```
Result: Routes to Opus (deep-executor) regardless of query complexity.

### Force Haiku for any task
```
/route haiku Fix the authentication bug in login.ts
```
Result: Routes to Haiku (fast-executor) for cost savings.

### Force Sonnet explicitly
```
/route sonnet Design a caching system
```
Result: Routes to Sonnet (standard-executor).

## Error Handling

If the user doesn't provide a valid model, respond with:

```
Usage: /route <model> <query>

Models:
  haiku, fast     - Quick, simple tasks (cheapest)
  sonnet, standard - Typical coding tasks (default)
  opus, deep      - Complex analysis (most capable)

Example: /route opus Analyze the security of this authentication flow
```

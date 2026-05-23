---
name: activities
description: Coding standards and best practices for Temporal activities.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: '**/*.go'
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
---

# Activities Skill

<identity>
You are a coding standards expert specializing in activities.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these guidelines:

This file provides rules and context for generating or understanding Go code related to Temporal activities within this project with the specific purpose of using a simple DSL to specify workflows.

**Activity Structure and Naming:**

- Activities should be methods on a struct (e.g., `SampleActivities`).
- Activity functions must accept `ctx context.Context` as the first argument.
- Use descriptive names for activities (e.g., `SampleActivity1`, `ProcessOrderActivity`).
- Follow the typical signature: `func (a *StructName) ActivityName(ctx context.Context, input ArgType) (ResultType, error)`.

**Accessing Activity Info:**

- Use `activity.GetInfo(ctx)` to retrieve activity metadata like its name.
- Example: `name := activity.GetInfo(ctx).ActivityType.Name`

**Logging:**

- You **must** use Temporal `activity.GetLogger(ctx)` for logging within activities.
- Always include the activity name in log messages for better context.

**Return Values:**

- Activities must return a result value and an error.
- Return `nil` for the error upon successful execution.
- Construct meaningful result values, potentially incorporating information derived during the activity's execution.

**Context Handling:**

- Ensure the `ctx context.Context` is propagated to any Temporal SDK calls or other functions that require context.

**Best Practices:**

- Strive to make activities idempotent.
- Keep activities focused on a single task and relatively short-lived.
- Avoid embedding complex business logic directly within activities. Orchestrate logic in workflows and utilize activities primarily for side effects or computations.

```go
package dsl

import (
	"context"
	"fmt"

	"go.temporal.io/sdk/activity"
)

type SampleActivities struct {
}

func (a *SampleActivities) SampleActivity1(ctx context.Context, input []string) (string, error) {
	name := activity.GetInfo(ctx).ActivityType.Name
	fmt.Printf("Run %s with input %v \n", name, input)
	return "Result_" + name, nil
}

func (a *SampleActivities) SampleActivity2(ctx context.Context, input []string) (string, error) {
	name := activity.GetInfo(ctx).ActivityType.Name
	fmt.Printf("Run %s with input %v \n", name, input)
	return "Result_" + name, nil
}

func (a *SampleActivities) SampleActivity3(ctx context.Context, input []string) (string, error) {
	name := activity.GetInfo(ctx).ActivityType.Name
	fmt.Printf("Run %s with input %v \n", name, input)
	return "Result_" + name, nil
}

func (a *SampleActivities) SampleActivity4(ctx context.Context, input []string) (string, error) {
	name := activity.GetInfo(ctx).ActivityType.Name
	fmt.Printf("Run %s with input %v \n", name, input)
	return "Result_" + name, nil
}

func (a *SampleActivities) SampleActivity5(ctx context.Context, input []string) (string, error) {
	name := activity.GetInfo(ctx).ActivityType.Name
	fmt.Printf("Run %s with input %v \n", name, input)
	return "Result_" + name, nil
}
</instructions>

<examples>
Example usage:
```

User: "Review this code for activities compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]

````
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**
```bash
cat .claude/context/memory/learnings.md
````

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

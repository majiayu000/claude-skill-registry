---
name: arch-patterns
cluster: se-architecture
description: "Design patterns: GoF 23 patterns, SOLID, DRY/YAGNI/KISS, composition vs inheritance, functional"
tags: ["patterns","solid","design","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "design patterns solid dry kiss factory singleton observer strategy"
---

# arch-patterns

## Purpose
This skill equips OpenClaw to assist in applying software architecture patterns, including the GoF 23 patterns (e.g., Factory, Singleton, Observer), SOLID principles (Single Responsibility, Open-Closed), and guidelines like DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), KISS (Keep It Simple, Stupid), composition over inheritance, and functional programming concepts. Use it to generate code snippets, suggest refactorings, or validate designs.

## When to Use
Apply this skill when structuring new codebases, refactoring legacy systems, or resolving design issues. For example, use it for object-oriented designs in languages like Java or Go, or when adopting functional styles in Python. Avoid it for trivial scripts; reserve for projects with >1000 lines or teams >5 members.

## Key Capabilities
- **GoF Patterns**: Suggest implementations like Factory Method (creates objects without specifying class) or Observer (notifies dependents of state changes).
- **SOLID Principles**: Enforce Single Responsibility (one class does one thing) or Dependency Inversion (depend on abstractions).
- **Best Practices**: Recommend DRY by extracting repeated code into functions, YAGNI by avoiding premature features, KISS by simplifying complex logic, and favoring composition (e.g., using interfaces) over inheritance.
- **Comparisons**: Provide code examples contrasting composition vs. inheritance, or functional vs. imperative approaches.
- **Validation**: Analyze user code for anti-patterns and suggest fixes, e.g., detecting God Objects.

## Usage Patterns
To use this skill, invoke OpenClaw via CLI or API with specific pattern queries. Start by providing context like language and problem. For CLI, pipe code snippets; for API, send JSON payloads. Always include the skill ID "arch-patterns" in requests. Example flow: Query a pattern, get a code snippet, then refine with follow-ups. Limit queries to one pattern per call for accuracy.

## Common Commands/API
Use the OpenClaw CLI with authentication via `$OPENCLAW_API_KEY` environment variable. Commands require the skill ID.
- **CLI Command**: `openclaw run arch-patterns --pattern factory --lang go --input "Create a car factory"`  
  This generates a Go struct for a Factory pattern.
- **API Endpoint**: POST /api/v1/skills/arch-patterns with JSON body:  
  ```json
  { "pattern": "singleton", "language": "java", "context": "Thread-safe logger" }
  ```
  Response includes a 2-4 line code snippet, e.g., a Java singleton class.
- **Config Format**: Use YAML for advanced configs, e.g.,  
  ```yaml
  skill: arch-patterns
  options:
    pattern: strategy
    validate: true
  ```
  Pass via `--config path/to/config.yaml` in CLI.
- **Flags**: Add `--validate` to check existing code, or `--refactor` to suggest changes.

## Integration Notes
Integrate this skill into workflows by wrapping it in scripts or IDE plugins. For example, in a CI/CD pipeline, call the API after code commits to enforce SOLID. Set `$OPENCLAW_API_KEY` for auth. If using with other skills (e.g., code-generation), chain requests: first query arch-patterns for design, then pass output to a compilation skill. Ensure inputs are under 500 characters; split larger codebases. For functional programming, specify paradigms like "fp" in queries to bias responses.

## Error Handling
Handle errors by checking response codes: HTTP 400 for invalid patterns (e.g., misspelled "singlton"), 401 for missing `$OPENCLAW_API_KEY`, or 429 for rate limits. In CLI, errors return as JSON with "error": "Pattern not found". Retry transient errors with exponential backoff. Validate inputs before sending; for example, if a query lacks --lang, OpenClaw defaults to English but errors on code gen. Log errors with timestamps and include full request payloads for debugging.

## Concrete Usage Examples
1. **Example 1: Implementing Factory Pattern in Go**  
   Command: `openclaw run arch-patterns --pattern factory --lang go --input "Vehicle creator"`  
   Output: A snippet like:  
   ```go
   type Factory interface { Create() Vehicle }
   func NewCarFactory() Factory { return &CarFactory{} }
   ```
   This creates a Factory for vehicles, ensuring DRY by centralizing object creation.

2. **Example 2: Refactoring for SOLID in Java**  
   API Call: POST /api/v1/skills/arch-patterns with body:  
   ```json
   { "pattern": "solid", "principle": "single-responsibility", "code": "public class UserService { /* handles users and logging */ }" }
   ```
   Response: Suggests splitting into:  
   ```java
   public class UserService { /* only user logic */ }
   public class Logger { /* logging logic */ }
   ```
   This applies Single Responsibility to improve maintainability.

## Graph Relationships
- Related to: se-architecture (parent cluster), patterns (tag overlap), solid (embedding hint), factory (specific pattern), singleton (pattern), observer (pattern), strategy (pattern).
- Connections: Links to code-generation for implementation, debugging for anti-pattern detection, and optimization for performance tweaks based on KISS/YAGNI.

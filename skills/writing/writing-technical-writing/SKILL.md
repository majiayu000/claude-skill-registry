---
name: writing-project-technical-writing
description: Writes technical prose (READMEs, ADRs, code comments) in the project's established human voice. Use when creating or editing .md files, writing Swift doc comments, authoring ADRs, or reviewing technical writing for voice consistency.
---

# Writing Project Technical Writing

This skill defines the voice, style, and structure for all technical writing in this project. The existing documentation is the gold standard — preserve and extend it.

## Voice

### Tone

- **Pragmatic and honest** — Acknowledge trade-offs, constraints, and downsides openly
- **Direct and declarative** — Use active voice and imperative mood for instructions
- **Confident without arrogance** — State positions clearly without hedging or dismissing alternatives
- **Developer-to-developer** — Speak as a peer, assume competence

### Pronoun Usage

Use "we" for the team voice:

```markdown
<!-- Correct -->
We use Homebrew to install dependencies.
We prefer value types for models.

<!-- Incorrect -->
You should use Homebrew to install dependencies.
Users must prefer value types for models.
```

### Tense

Use present tense to describe current state:

```markdown
<!-- Correct -->
This package defines the data layer.
The goal is to keep call sites stable.

<!-- Incorrect -->
This package will define the data layer.
The goal would be to keep call sites stable.
```

### Instructions

Use imperative mood for actionable steps:

```markdown
<!-- Correct -->
Run this command to install dependencies.
Add the secrets to 1Password.

<!-- Incorrect -->
You can run this command to install dependencies.
You should add the secrets to 1Password.
```

## Anti-Patterns

Never use these patterns — they sound like AI-generated content:

| Pattern | Example | Why It's Wrong |
|---------|---------|----------------|
| Enthusiasm markers | "This is great for debugging!" | Unprofessional, sounds like marketing |
| Filler words | "This basically reduces complexity" | Adds no information, hedges |
| AI-isms | "Let me explain...", "Here's how to...", "Sure!" | Sounds like chatbot output |
| Hedging | "This might help", "could potentially" | Lacks confidence |
| Over-qualification | "It should be noted that..." | Verbose, indirect |
| Exclamation points | "Install the dependencies!" | Overly casual in technical prose |

### Specific Words to Avoid

- "simply", "just", "basically", "essentially" (as filler)
- "Let me...", "I'll...", "Here's...", "Sure!", "Certainly!", "Great!", "Awesome!"
- "might", "could potentially", "may or may not"
- "It should be noted that...", "It is important to note that..."

## Document Structures

### READMEs

```markdown
# Package Name

One-line summary of what this package does.

## About

Explain purpose, context, and when to use this package.

### Capabilities

What this package enables (bullet list).

### Non-Goals

What this package intentionally does not do.

## Getting Started

Practical usage instructions with code examples.

### Design

Core patterns, concepts, and architectural decisions.

## Architecture

Detailed explanation of structure and concepts.

## Trade-Offs and Constraints

Honest discussion of limitations and design decisions.
```

### ADRs (Architecture Decision Records)

Location: `Documents/Decisions/NNNN Title.md`

```markdown
# Title

## Context and Problem Statement

Describe the situation and frame the problem as a question:
"How can we ensure that X while also Y?"

## Considered Options

- Option A description
- Option B description
- Option C description

## Decision Outcome

Chosen option: "Option B", because [rationale connecting back to the problem].

### Consequences

- Good, because [benefit].
- Good, because [another benefit].
- Bad, because [downside or trade-off].
```

The "Consequences" section must include at least one "Bad" item. Omitting downsides is dishonest.

### Code Documentation (Swift)

First line is a complete sentence describing purpose:

```swift
/// A single-result operation that produces a response from the GraphQL service.
public protocol CoastGraphQLRequest<Model>: Request { }
```

Multi-paragraph for complex concepts:

```swift
/// A pattern for managing hierarchical relationships among coordinators.
///
/// By adopting `Coordinating`, you can form intricate structures of nested objects
/// that manage their own child coordinators. This pattern facilitates clean separation
/// of responsibilities.
public protocol Coordinating: AnyObject { }
```

Use callouts for important notes:

```swift
/// - Note: This has a `Sendable` requirement because of constraints on `AnyAsyncSequence`.
/// - Important: "Subscription" refers to `Clients/Subscription`, not GraphQL subscriptions.
/// - Attention: Modifying this property outside the framework is a programming error.
```

Document parameters and returns for public APIs:

```swift
/// Create a new request.
///
/// - Parameter fileName: The name of the file to create.
/// - Parameter mimeType: The MIME type of the file.
/// - Returns: A configured request ready for execution.
/// - Throws: `ValidationError` if the MIME type is unsupported.
```

## Formatting

### Code Blocks

Always include language hints:

````markdown
```swift
let client = CoastGraphQLClient()
```

```sh
make build/app
```
````

### Inline Code

Use backticks for:
- File paths: `Packages/Common/README.md`
- Commands: `make build/app`
- Types and symbols: `CoastGraphQLRequest`, `execute(_:)`
- Values: `true`, `nil`, `"production"`

### Emphasis

Use **bold** for key terms and warnings, not ALL CAPS:

```markdown
<!-- Correct -->
**Use this package when** you need ergonomic data operations.

<!-- Incorrect -->
USE THIS PACKAGE WHEN you need ergonomic data operations.
```

### Asides

Use em-dashes for mid-sentence asides:

```markdown
<!-- Correct -->
The model layer — which sits above Apollo — keeps call sites stable.

<!-- Incorrect -->
The model layer (which sits above Apollo) keeps call sites stable.
```

### Callouts

For GitHub-rendered markdown, use:

```markdown
> [!NOTE]
> There are no requirements for running on Simulator.

> [!WARNING]
> This will delete all local data.
```

### Tables

Use tables for structured data like variables, options, or comparisons:

```markdown
| Variable | Required | Description |
|----------|:--------:|-------------|
| PACKAGE  | Yes      | Name of the package to build |
| CONFIG   | No       | Build configuration. Defaults to `Debug`. |
```

## Rationale

Always explain "why" after decisions:

```markdown
<!-- Correct -->
Chosen option: "Accept automatic behavior", because iOS enforces APNS
environment selection regardless of entitlements configuration.

<!-- Incorrect -->
Chosen option: "Accept automatic behavior".
```

The word "because" should appear after every decision statement.

## Examples

Use real code from the codebase, not contrived examples. If you must create an example, make it realistic and consistent with existing patterns.

```markdown
<!-- Correct: Real code -->
let response = try await client.execute(CreateMediaRequest(fileName: "a.jpg", mimeType: "image/jpeg"))

<!-- Incorrect: Contrived -->
let response = try await client.execute(MyRequest(foo: "bar"))
```

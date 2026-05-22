---
name: llm-application-patterns
description: This skill should be used when building production LLM applications in any language. It applies when implementing predictable AI features, creating structured interfaces for LLM operations, configuring language model providers, building agent systems with tools, optimizing prompts, or testing LLM-powered functionality. Covers language-agnostic patterns for type-safe contracts, modular composition, multi-provider support, and production deployment.
---

# LLM Application Patterns

## Overview

Build production LLM applications using structured, testable patterns. Instead of manually crafting prompts, define application requirements through type-safe, composable modules that can be tested, optimized, and version-controlled like regular code.

**Core principle: Program LLMs, don't prompt them.**

This skill provides language-agnostic guidance on:
- Creating type-safe signatures for LLM operations
- Building composable modules and workflows
- Configuring multiple LLM providers
- Implementing agents with tools
- Testing and optimizing LLM applications
- Production deployment patterns

## Core Concepts

### 1. Type-Safe Signatures

Define input/output contracts for LLM operations with runtime type checking.

**When to use**: Any LLM task, from simple classification to complex analysis.

**Pattern** (pseudo-code):
```
Signature: EmailClassification
  Description: "Classify customer support emails"

  Inputs:
    email_subject: String (required)
    email_body: String (required)

  Outputs:
    category: Enum["Technical", "Billing", "General"]
    priority: Enum["Low", "Medium", "High"]
    confidence: Float (0.0 to 1.0)
```

**Best practices**:
- Always provide clear, specific descriptions
- Use enums for constrained outputs
- Include field descriptions
- Prefer specific types over generic strings
- Define confidence scores when useful

See [signatures.md](./references/signatures.md) for detailed patterns.

### 2. Composable Modules

Build reusable, chainable modules that encapsulate LLM operations.

**Pattern** (pseudo-code):
```
Module: EmailProcessor
  Initialize:
    classifier = Predict(EmailClassificationSignature)

  Forward(email_subject, email_body):
    return classifier.forward(email_subject, email_body)
```

**Module composition** - chain modules for complex workflows:
```
Module: CustomerServicePipeline
  Initialize:
    classifier = EmailClassifier()
    router = TicketRouter()
    responder = AutoResponder()

  Forward(email):
    classification = classifier.forward(email)
    ticket = router.forward(classification)
    response = responder.forward(ticket)
    return response
```

See [modules.md](./references/modules.md) for detailed patterns.

### 3. Predictor Types

Choose the right predictor for your task:

| Predictor | Use Case | Output |
|-----------|----------|--------|
| **Predict** | Simple tasks, classification, extraction | Direct output |
| **ChainOfThought** | Complex reasoning, analysis | Reasoning + output |
| **ReAct** | Tasks requiring tools (search, APIs) | Action sequence + output |
| **CodeAct** | Tasks best solved with code | Generated code + execution |

**When to use each**:

- **Predict**: Classification, entity extraction, simple Q&A, summarization
- **ChainOfThought**: Math problems, logic puzzles, multi-step analysis, explanations
- **ReAct**: Research tasks, data gathering, calculator usage, API calls
- **CodeAct**: Data transformation, calculations, file manipulation

### 4. Provider Configuration

Support for multiple LLM providers with consistent interfaces.

**Provider compatibility matrix:**

| Feature | OpenAI | Anthropic | Gemini | Ollama |
|---------|--------|-----------|--------|--------|
| Structured Output | Yes | Yes | Yes | Yes |
| Vision (Images) | Yes | Yes | Yes | Limited |
| Image URLs | Yes | No | No | No |
| Tool Calling | Yes | Yes | Yes | Varies |
| Streaming | Yes | Yes | Yes | Yes |

**Cost optimization strategy:**
- **Development**: Ollama (free, local) or gpt-4o-mini (cheap)
- **Testing**: gpt-4o-mini with temperature=0.0 for determinism
- **Production (simple)**: gpt-4o-mini, claude-3-haiku, gemini-flash
- **Production (complex)**: gpt-4o, claude-3-5-sonnet, gemini-pro

See [providers.md](./references/providers.md) for configuration details.

## Common Patterns

### Multi-Step Pipeline

```
Pipeline: AnalysisWorkflow
  Steps:
    1. Extract → pull structured data from input
    2. Analyze → apply business logic / reasoning
    3. Summarize → produce final output

  Forward(input):
    extracted = extract.forward(input)
    analyzed = analyze.forward(extracted)
    return summarize.forward(analyzed)
```

### Agent with Tools

```
Agent: ResearchAgent
  Tools:
    - WebSearch: search the internet
    - DatabaseQuery: query internal data
    - Calculator: perform calculations

  MaxIterations: 10

  Forward(question):
    Loop until answer or max iterations:
      1. Think: what do I need to know?
      2. Act: call appropriate tool
      3. Observe: process tool result
    Return final answer
```

### Conditional Router

```
Router: SmartDispatcher
  Forward(input):
    classification = classifier.forward(input)

    if classification.complexity == "Simple":
      return simple_handler.forward(input)
    else:
      return complex_handler.forward(input)
```

### Retry with Fallback

```
RobustModule:
  MaxRetries: 3

  Forward(input):
    for attempt in range(MaxRetries):
      try:
        return predictor.forward(input)
      catch ValidationError:
        sleep(2 ** attempt)  # exponential backoff

    return fallback_response  # or raise
```

## Quick Start Workflow

### 1. Define Your Signature

What inputs do you need? What outputs do you expect?

```
Signature: YourTask
  Description: "What this task does"

  Inputs:
    input_field: Type

  Outputs:
    output_field: Type
```

### 2. Create a Module

Wrap the signature in a reusable module.

```
Module: YourModule
  Initialize:
    predictor = Predict(YourTaskSignature)

  Forward(input_field):
    return predictor.forward(input_field)
```

### 3. Configure Provider

Set up your LLM provider with appropriate settings.

```
Configure:
  provider: "openai/gpt-4o-mini"
  api_key: from environment
  temperature: 0.0 for determinism, 0.7 for creativity
```

### 4. Test

Write tests that verify the module's behavior.

```
Test: YourModule
  Given: known input
  When: module.forward(input)
  Then: output matches expected type and constraints
```

## Implementation Libraries

| Language | Libraries |
|----------|-----------|
| **Python** | DSPy, Instructor, Outlines, Marvin, Pydantic AI |
| **TypeScript** | Zod + OpenAI, Vercel AI SDK, LangChain.js |
| **Ruby** | DSPy.rb, Instructor-rb |
| **Go** | go-openai with struct validation |
| **Rust** | async-openai with serde |

## Reference Files

For detailed patterns, see:

| File | Topics |
|------|--------|
| [signatures.md](./references/signatures.md) | Type-safe contract patterns, field types, validation |
| [modules.md](./references/modules.md) | Module composition, pipelines, state management |
| [providers.md](./references/providers.md) | Provider configuration, switching, cost optimization |
| [testing.md](./references/testing.md) | Testing strategies, mocking, determinism |
| [optimization.md](./references/optimization.md) | Prompt optimization, few-shot learning, fine-tuning |

## When to Use This Skill

Trigger this skill when:
- Implementing LLM-powered features in applications
- Creating type-safe interfaces for AI operations
- Building agent systems with tool usage
- Setting up or troubleshooting LLM providers
- Optimizing prompts and improving accuracy
- Testing LLM functionality
- Adding observability to AI applications
- Converting from manual prompts to programmatic approach
- Debugging LLM application issues

---
name: code-summarizer
description: Generate concise summaries of source code at multiple scales. Use when users ask to summarize, explain, or understand code - whether it's a single function, a class, a module, or an entire codebase. Handles function-level code by explaining intention and core logic, and large codebases by providing high-level overviews with drill-down capabilities for specific modules.
---

# Code Summarizer

Generate clear, concise summaries of source code at any scale - from individual functions to entire codebases.

## Overview

This skill helps analyze and summarize code by adapting the level of detail to the code's scale:

- **Small-scale code** (functions, classes, small files): Provide focused summaries of intention and implementation
- **Large-scale code** (modules, packages, entire repositories): Provide hierarchical summaries with progressive drill-down

## Workflow Decision Tree

```
User provides code → Assess scale
    ├─ Small-scale (< 200 lines, single file/function)
    │   └─ Generate focused summary
    │
    └─ Large-scale (> 200 lines, multiple files/modules)
        ├─ Generate high-level overview
        ├─ List main modules/components
        └─ Prompt user to select specific parts for detailed analysis
```

## Small-Scale Code Summarization

For functions, classes, or small files (typically < 200 lines), provide a **focused summary** that includes:

### Summary Structure

1. **Purpose Statement** (1-2 sentences)
   - What does this code do?
   - What problem does it solve?

2. **Core Logic** (2-4 bullet points)
   - Key algorithms or approaches used
   - Important data transformations
   - Critical control flow decisions

3. **Key Details**
   - Input parameters and their purposes
   - Return values and their meaning
   - Important side effects or state changes
   - Dependencies on external libraries or modules

4. **Notable Patterns** (if applicable)
   - Design patterns used
   - Optimization techniques
   - Error handling approaches

### Example Format

```markdown
## Summary

**Purpose**: This function validates user email addresses and normalizes them to lowercase format before database storage.

**Core Logic**:
- Uses regex pattern matching to validate email format (RFC 5322 compliant)
- Strips whitespace and converts to lowercase for consistency
- Checks against a blocklist of disposable email domains
- Logs validation failures for security monitoring

**Key Details**:
- Input: `email` (string) - raw email address from user input
- Returns: `normalized_email` (string) or raises `ValidationError`
- Side effect: Logs to `security.log` on validation failure
- Dependencies: `re`, `logging`, custom `EmailBlocklist` class

**Notable Patterns**:
- Uses early return pattern for validation failures
- Implements defensive programming with input sanitization
```

## Large-Scale Code Summarization

For modules, packages, or entire repositories (typically > 200 lines or multiple files), use a **hierarchical approach**:

### Phase 1: High-Level Overview

Provide a concise overview that includes:

1. **Project Purpose** (2-3 sentences)
   - What does this codebase do?
   - What is its primary use case or domain?

2. **Architecture Overview**
   - Overall design pattern (MVC, microservices, layered, etc.)
   - Key architectural decisions
   - Technology stack

3. **Main Components** (list with brief descriptions)
   - List 5-10 major modules/packages
   - One-line description for each
   - Indicate relationships between components

4. **Entry Points**
   - Main execution files
   - Key API endpoints or interfaces
   - Configuration files

### Phase 2: Interactive Drill-Down

After providing the overview, **prompt the user** to select specific areas for detailed analysis:

```markdown
## Detailed Analysis Available

I can provide more detailed summaries of specific components:

1. **[Component Name]** - [Brief description]
2. **[Component Name]** - [Brief description]
3. **[Component Name]** - [Brief description]
...

Which component(s) would you like me to analyze in detail? You can:
- Select one or more by number
- Ask about specific functionality (e.g., "How does authentication work?")
- Request a specific file or module by name
```

### Phase 3: Detailed Component Analysis

When user selects a component, provide a **detailed summary** using the small-scale format adapted for the component:

- Purpose and responsibilities
- Key classes/functions within the component
- Interactions with other components
- Important algorithms or business logic
- Configuration and dependencies

## Best Practices

### Code Analysis Approach

1. **Read strategically**
   - Start with entry points (main files, __init__.py, index files)
   - Examine directory structure for organization patterns
   - Look for README, documentation, or comments
   - Identify configuration files

2. **Identify patterns**
   - Recognize common design patterns
   - Note architectural styles
   - Identify framework conventions

3. **Focus on intent over implementation**
   - Explain *what* and *why* before *how*
   - Highlight business logic over boilerplate
   - Emphasize key algorithms over routine operations

### Writing Style

- **Be concise**: Avoid unnecessary verbosity
- **Be specific**: Use concrete examples and actual names from the code
- **Be hierarchical**: Start broad, then drill down
- **Be actionable**: Help users understand how to use or modify the code

### Handling Different Languages

Adapt terminology and patterns to the language:

- **Python**: Modules, packages, decorators, list comprehensions
- **JavaScript**: Modules, components, promises, async/await
- **Java**: Packages, classes, interfaces, annotations
- **C/C++**: Headers, source files, namespaces, templates
- **Go**: Packages, goroutines, channels, interfaces

## Common Scenarios

### Scenario 1: Understanding a New Codebase

User: "Can you summarize this repository?"

**Response approach**:
1. Analyze directory structure
2. Read main entry points and README
3. Provide high-level overview with component list
4. Offer to drill down into specific areas

### Scenario 2: Explaining a Specific Function

User: "What does this function do?" [provides code]

**Response approach**:
1. Identify function purpose
2. Explain core logic step-by-step
3. Note inputs, outputs, and side effects
4. Highlight any notable patterns or concerns

### Scenario 3: Comparing Implementations

User: "Summarize these two implementations and compare them"

**Response approach**:
1. Summarize each implementation separately
2. Identify key differences in approach
3. Compare trade-offs (performance, readability, maintainability)
4. Recommend based on context if appropriate

### Scenario 4: Legacy Code Understanding

User: "Help me understand this old code"

**Response approach**:
1. Identify the era/style of the code
2. Explain outdated patterns or conventions
3. Summarize what it does in modern terms
4. Suggest modern equivalents if relevant

## Output Format Guidelines

### For Small-Scale Code

Use clear markdown with:
- Heading for the summary
- Bullet points for core logic
- Code blocks for examples if helpful
- Bold for emphasis on key terms

### For Large-Scale Code

Use structured markdown with:
- Clear section headings
- Numbered or bulleted lists for components
- Tables for comparing multiple items
- Collapsible sections for optional details (if supported)

### Code References

When referencing specific code elements:
- Use `backticks` for function/class/variable names
- Include file paths when relevant: `src/utils/validator.py:validate_email()`
- Use line numbers for large files: `lines 45-67`

## Limitations and Considerations

- **Context limits**: For very large codebases, may need to analyze in chunks
- **Missing context**: May need to ask clarifying questions about business logic
- **Language expertise**: Summaries are most accurate for well-known languages and frameworks
- **Dynamic behavior**: Cannot fully analyze runtime behavior without execution
- **External dependencies**: May not have full context for third-party libraries

When encountering limitations, acknowledge them and offer alternative approaches or ask for additional context.

---
name: ai-prompt-engineer
description: AI engineering skill for prompt optimization, context inference, and intelligent command routing across different models and use cases
version: 1.0.0
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch"
---

# AI Prompt Engineer

An AI engineering skill focused on optimizing prompts, improving context collection, and intelligently routing requests across different models, purposes, and layers of the agent loop.

## Purpose

This skill addresses the core challenge: **users shouldn't need to over-provide information**. Caro should infer context intelligently and serve users with minimal friction. This skill guides the systematic improvement of:

1. **Query Understanding** - Categorize and understand user intent from minimal input
2. **Context Inference** - Extract maximum signal from available cues (file types, platform, cwd, history)
3. **Tool Routing** - Map inferred context to appropriate tools and commands
4. **Prompt Optimization** - Craft prompts tailored to specific models and use cases

## When to Use This Skill

Invoke this skill when working on:

- Analyzing user query patterns to improve command generation
- Optimizing prompts for different model sizes (SmolLM, larger models)
- Building context inference logic that reduces user input requirements
- Creating file-type-to-tool mappings for intelligent recommendations
- Improving platform-aware command routing
- Designing prompt templates for specific use case categories
- Evaluating prompt effectiveness across different scenarios

## Core Concepts

### Query Taxonomy

User queries fall into distinct categories that require different handling:

| Category | Description | Examples | Key Signals |
|----------|-------------|----------|-------------|
| **Terminal Exploration** | Navigating, listing, searching the filesystem | "what's in this folder", "find large files" | Navigation verbs, location references |
| **Runbook Execution** | Project-specific workflows based on history | "run the build", "deploy to staging" | Project context, command history patterns |
| **Language Development** | Language-specific development tasks | "compile this", "run tests" | File extensions, project markers (Cargo.toml, package.json) |
| **DevOps Flow** | Deployment, CI/CD, infrastructure | "push to prod", "check k8s pods" | DevOps tools (docker, kubectl), env references |
| **Casual Scripting** | Quick one-off tasks | "unzip this file", "rename these files" | Simple verbs, single file/pattern references |
| **CLI Tool Interaction** | Using specific command-line tools | "git status", "npm install" | Tool names, tool-specific vocabulary |

### Context Inference Hierarchy

Extract context in priority order:

1. **Explicit Reference** - User mentions a file, tool, or path directly
2. **File Type Signals** - Extension hints at appropriate tools
3. **Platform Context** - OS determines available commands and conventions
4. **Working Directory** - Project type, available tools, recent activity
5. **Session History** - Patterns in previous commands suggest intent
6. **Default Conventions** - Platform/community standard practices

### The File Type Principle

> "The file type is the strongest hint for tool selection"

When a user references a file, the extension often determines the appropriate tool:

**Archive Example:**
- `.tar.gz`, `.tgz` → `tar -xzf` (Linux/macOS)
- `.zip` → `unzip` (macOS), `7z x` or `Expand-Archive` (Windows)
- `.rar` → `unrar` (requires installation)
- `.7z` → `7z x` (requires 7-zip)

**The Anti-Pattern:**
```
User on macOS: "extract this archive"
File: document.zip

BAD: tar -xzf document.zip  (wrong tool for file type)
GOOD: unzip document.zip    (matches file type + platform)
```

## Workflow

### Phase 1: Analyze Query Pattern

```
1. Read the user query
2. Identify category from Query Taxonomy
3. Extract explicit references (files, tools, paths)
4. Note implicit signals (verbs, modifiers, context words)
5. Document the analysis
```

### Phase 2: Gather Context Signals

```
1. Check if file reference exists → extract extension
2. Detect platform from ExecutionContext
3. Identify project type from cwd markers
4. Review session history for patterns
5. Build context signal map
```

### Phase 3: Map to Tool/Command Space

```
1. Use file-type-to-tool mappings (see references/file-tool-map.md)
2. Filter by platform availability
3. Consider user preferences if known
4. Rank options by confidence
5. If ambiguous, prepare clarifying question
```

### Phase 4: Optimize Prompt

```
1. Select appropriate prompt template for category
2. Inject inferred context
3. Constrain output space based on mappings
4. Add platform-specific rules
5. Format for target model (SmolLM ChatML, etc.)
```

### Phase 5: Evaluate & Iterate

```
1. Run against test cases in evaluation harness
2. Measure improvement vs baseline
3. Document patterns that work
4. Update mappings and templates
5. Create regression tests for fixed cases
```

## Reference Materials

| Document | Purpose |
|----------|---------|
| `references/query-taxonomy.md` | Detailed breakdown of query categories with detection signals |
| `references/file-tool-map.md` | File extension to tool mappings by platform |
| `references/context-inference.md` | Patterns for inferring context from minimal input |
| `references/prompt-templates.md` | Category-specific prompt optimization templates |
| `examples/case-studies.md` | Real-world optimization examples |

## Integration Points

This skill integrates with:

- **`/src/prompts/`** - Prompt building and capability profiling
- **`/src/context/mod.rs`** - Execution context detection
- **`/src/evaluation/`** - Testing improvements against baseline
- **`/tests/evaluation/dataset.yaml`** - Test case datasets

## Success Metrics

1. **Inference Accuracy** - Correct tool/command selection without explicit user specification
2. **Context Hit Rate** - Percentage of queries where useful context was inferred
3. **Clarification Rate** - Reduction in "what do you mean?" responses
4. **Cross-Platform Correctness** - Right tool for right platform

## Example Session

**Scenario:** User on macOS in a Rust project asks "extract the dependency archive"

```
Query Analysis:
- Category: Casual Scripting (simple verb, file reference)
- Explicit: "dependency archive"
- Implicit: extraction intent

Context Signals:
- Platform: macOS (BSD tools, unzip available)
- CWD: /Users/dev/myproject (Cargo.toml present → Rust project)
- Files matching "archive": vendor.tar.gz, deps.zip

Ambiguity Detection:
- Multiple archive files found
- Different formats require different tools

Resolution Options:
1. Ask: "Which archive? vendor.tar.gz or deps.zip?"
2. Or list both commands with explanations

If deps.zip selected:
- Tool: unzip (matches .zip + macOS)
- Command: unzip deps.zip
- NOT: tar -xzf deps.zip (wrong tool!)
```

## Anti-Patterns to Avoid

1. **Platform Mismatch** - Using GNU flags on BSD, tar for zip files
2. **Over-Assumption** - Guessing without sufficient signals
3. **Under-Inference** - Asking for info that's already determinable
4. **Tool Hallucination** - Suggesting tools not installed/available
5. **Context Blindness** - Ignoring obvious cues from file types, cwd

## Next Steps for Development

1. Expand `file-tool-map.md` with more file types and edge cases
2. Build query classifier that maps natural language to taxonomy categories
3. Create "context score" metric for measuring inference quality
4. Develop prompt templates optimized for each category
5. Add test cases to evaluation harness for new patterns

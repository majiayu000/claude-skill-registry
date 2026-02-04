---
name: engram-summarize
description: |
  Summarize coding sessions into structured learnings using LLM extraction.
  Use when: (1) distilling lessons from recent work, (2) creating reusable knowledge,
  (3) building a project knowledge base, (4) onboarding others to a codebase.
category: memory
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash, Write, Edit, Glob
---

# Engram Summarize

Extract structured learnings from Claude Code and OpenClaw session history using LLM-based summarization.

## When to Use

- After completing significant work on a project
- Before onboarding someone new to a codebase
- Periodically to capture accumulated knowledge
- When you want to distill decisions and patterns

## What It Extracts

| Category | Description | Example |
|----------|-------------|---------|
| **decision** | Architectural and design choices | "Chose SQLite over PostgreSQL for local CLI" |
| **pattern** | Code patterns and idioms | "Uses Result<T, E> for error handling" |
| **gotcha** | Things that went wrong and fixes | "index.json must sync with posts/" |
| **convention** | Project-specific norms | "Tests colocated with source files" |
| **context** | Background knowledge | "This is a Rust 2021 edition project" |

## Workflow

### Step 1: Set up API key

```bash
export ANTHROPIC_API_KEY=your-key
```

### Step 2: Summarize sessions

```bash
# Summarize last 30 days for current workspace
npx engram summarize --workspace . --days 30

# Save to file
npx engram summarize --workspace . -o learnings.json

# Higher confidence threshold
npx engram summarize --workspace . --min-confidence 0.7
```

### Step 3: Review learnings

The output includes:
- Session count processed
- Learnings by category
- Top learnings ranked by confidence

Example output:
```
📊 Summary:
  Sessions: 12
  Learnings: 23

  By category:
    Decisions:   5
    Patterns:    8
    Gotchas:     4
    Conventions: 3
    Context:     3

📝 Top learnings:
  [gotcha] Blog index.json must be updated when posts are renamed
  [pattern] All exports go through index.ts barrel files
  [decision] Used vitest over jest for faster test execution
```

### Step 4: Integrate with skill generation

Use summarized learnings to enhance generated skills:

```bash
# Generate skill with richer context
npx engram generate-skill --workspace . --days 30
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-w, --workspace <path>` | Workspace to filter sessions | `.` |
| `-d, --days <number>` | Days of history to analyze | `30` |
| `--no-openclaw` | Exclude OpenClaw sessions | include |
| `-a, --agent <id>` | OpenClaw agent ID filter | all |
| `-c, --min-confidence <n>` | Confidence threshold (0-1) | `0.5` |
| `-o, --output <path>` | Save learnings to JSON file | stdout |
| `--json` | Output as JSON | pretty print |

## Integration with Other Skills

| Skill | When to Combine |
|-------|-----------------|
| **engram-generate** | Summarize before generating for richer skills |
| **engram-recall** | Recall + summarize for full context |
| **describe-codebase** | Add summarized learnings to codebase description |

## Comparison: Generate vs Summarize

| Aspect | engram-generate | engram-summarize |
|--------|-----------------|------------------|
| Method | Pattern matching | LLM extraction |
| Output | Structural patterns | Semantic learnings |
| Cost | Free (local) | API tokens |
| Depth | File co-edits, commands | Decisions, rationale |

Use both together for best results:
1. `summarize` extracts the meaning
2. `generate` captures the structure

## Example Learnings

```json
{
  "learnings": [
    {
      "category": "gotcha",
      "summary": "Blog index.json must be updated when posts are renamed",
      "detail": "The blog uses a static index.json. Renaming a post without updating causes 404 errors.",
      "files": ["index.json", "posts/*.md"],
      "confidence": 0.95
    },
    {
      "category": "decision", 
      "summary": "Chose TypeScript for type safety",
      "confidence": 0.85
    }
  ]
}
```

## Important

- Requires `ANTHROPIC_API_KEY` environment variable
- Uses Claude Sonnet for extraction (cost-effective)
- Review learnings before sharing (may contain sensitive info)
- Higher confidence threshold reduces noise but may miss insights

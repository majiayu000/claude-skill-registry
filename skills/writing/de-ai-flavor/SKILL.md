---
name: de-ai-flavor
description: Remove AI-generated artifacts from documents, including tool names, boilerplate patterns, over-structuring.
allowed-tools: Read, Grep, Glob, Edit
---

# De-AI-Flavor Skill

## Trigger

- Keywords: de-ai, remove AI traces, humanize document, de-ai-flavor, humanize

## When NOT to Use

- Co-Authored-By in CHANGELOG (Git convention)
- Documents discussing AI technology (topic itself requires it)
- Quoting others' AI-related content
- Variable/function names in code

## Usage

```bash
/de-ai-flavor docs/xxx.md           # Process specified file
/de-ai-flavor docs/                 # Process all .md in directory
/de-ai-flavor                       # Process .md in git diff
```

## Detection Rules

| Type              | Pattern                                             | Action  |
| ----------------- | --------------------------------------------------- | ------- |
| Tool names        | Claude/Codex/GPT/AI assistant                       | Remove  |
| Boilerplate       | "Let me...", "First...then...", "In conclusion"      | Rewrite |
| Over-structuring  | One sentence per heading, too many #### levels       | Simplify|
| Service tone      | "Hope this helps", "If you have questions..."        | Remove  |
| Self-description  | "Next I will...", "I will proceed to..."             | Remove  |
| Iteration leaks   | "Round 1/Round 2/Round N"                            | Rewrite |

## Workflow

```
Scan file -> Mark AI traces -> Remove/Rewrite/Simplify -> Output summary
```

## Verification

- All tool names removed
- Boilerplate rewritten to natural tone
- Structure not overly flat or nested

## Output Format

```markdown
## De-AI-Flavor Results

**File**: `docs/xxx.md`

| Line | Original              | Change                  | Reason           |
| ---- | --------------------- | ----------------------- | ---------------- |
| 15   | Let me explain...     | Removed                 | AI self-description |
| 32   | Claude suggests...    | Changed to "Suggest..." | Tool name        |

**Stats**: Removed 3 tool names | Rewrote 5 boilerplate | Simplified 2 structures
```

## Examples

```
Input: /de-ai-flavor docs/tech-spec.md
Action: Scan -> Remove "Claude suggests" -> Rewrite "Let me explain" -> Output summary
```

```
Input: This document feels very AI-generated, please clean it up
Action: Detect git diff -> Mark AI traces -> Batch process -> Output stats
```

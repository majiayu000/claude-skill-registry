---
name: extract-skill-from-conversation
description: "This skill should be used when the user asks to 'extract a skill from a conversation', 'convert conversation to skill', 'create skill from chat history', 'generate skill from session', or mentions extracting reusable workflows from Claude Code conversations. Uses Fabric AI patterns to distill conversations into actionable skills."
---

# Extract Skill from Conversation

Transform Claude Code conversations into reusable skills by extracting wisdom, instructions, problems, and solutions using Fabric AI patterns.

## Core Concept

Conversations contain valuable workflows buried in noise (trial & error, exploration, backtracking). This skill extracts the **reusable essence** and converts it into a well-structured SKILL.md.

## When to Use

- Convert a debugging session into a reusable debugging skill
- Extract a feature implementation workflow
- Create skills from research/learning conversations
- Document tribal knowledge from past sessions

## Extraction Pipeline

### Step 1: Obtain the Conversation

Conversations are stored as JSONL in Claude Code project directories:

```
~/.claude/projects/{project-path-encoded}/{session-id}.jsonl
```

To find conversations:

```bash
# List recent conversations for a project
ls -lht ~/.claude/projects/{project-path}/*.jsonl | head -10

# Find today's conversations
find ~/.claude/projects/{project-path} -name "*.jsonl" -newermt "today"
```

### Step 2: Parse Conversation to Text

Convert JSONL to readable text using the parse script:

```bash
bash scripts/parse_conversation.sh /path/to/conversation.jsonl > /tmp/conversation.txt
```

The script extracts:
- User messages
- Assistant responses (truncated for context)
- Tool calls and results
- Summaries

### Step 3: Extract Value with Fabric Patterns

Apply multiple Fabric patterns in parallel to extract different aspects:

```bash
# Extract insights and wisdom
cat /tmp/conversation.txt | fabric -p extract_wisdom --stream > /tmp/wisdom.md

# Extract actionable steps
cat /tmp/conversation.txt | fabric -p extract_instructions --stream > /tmp/instructions.md

# Extract the core problem
cat /tmp/conversation.txt | fabric -p extract_primary_problem --stream > /tmp/problem.md

# Extract the solution that worked
cat /tmp/conversation.txt | fabric -p extract_primary_solution --stream > /tmp/solution.md
```

Run in parallel for speed:

```bash
cat /tmp/conversation.txt | fabric -p extract_wisdom > /tmp/wisdom.md &
cat /tmp/conversation.txt | fabric -p extract_instructions > /tmp/instructions.md &
cat /tmp/conversation.txt | fabric -p extract_primary_problem > /tmp/problem.md &
cat /tmp/conversation.txt | fabric -p extract_primary_solution > /tmp/solution.md &
wait
```

### Step 4: Combine into Skill Structure

Merge extractions into a SKILL.md template. The skill should include:

```markdown
---
name: [skill-name-from-problem]
description: "[One-line description of what this skill solves]"
---

# [Skill Title]

[Brief summary from extract_primary_problem]

## Problem Pattern

[When to use this skill - extracted from problem analysis]

## Steps

[Numbered steps from extract_instructions - filtered to critical path only]

## Key Insights

[Bullet points from extract_wisdom]

## Common Mistakes

[Gotchas identified during conversation]

## References

[Any URLs or files that were useful]
```

### Step 5: Refine and Validate

After generating the skill:

1. Remove trial-and-error content
2. Keep only the "recipe that worked"
3. Add imperative language (do X, not "I did X")
4. Verify all referenced files/commands exist
5. Test the skill on a similar problem

## Fabric Patterns Reference

| Pattern | Extracts | Use For |
|---------|----------|---------|
| `extract_wisdom` | Insights, learnings | Key Insights section |
| `extract_instructions` | Step-by-step procedures | Steps section |
| `extract_primary_problem` | Core problem statement | Problem Pattern section |
| `extract_primary_solution` | What actually worked | Solution summary |
| `create_recursive_outline` | Hierarchical breakdown | Complex workflows |
| `summarize` | Brief overview | Skill description |

## What to Include vs Exclude

### Include in Skill

- Commands that worked
- Decisions and why they were made
- Key insights discovered
- Pattern recognition (e.g., "this type of error usually means X")
- Useful references (URLs, files)
- Prerequisites not obvious

### Exclude from Skill

- Trial and error attempts
- Dead ends and backtracking
- Exploratory reads that didn't help
- Typos and corrections
- Social conversation ("thanks", "great")
- Verbose explanations (distill to essence)

## Quick Reference

Full extraction pipeline:

```bash
# 1. Parse conversation
bash scripts/parse_conversation.sh /path/to/session.jsonl > /tmp/conv.txt

# 2. Extract in parallel
cat /tmp/conv.txt | fabric -p extract_wisdom > /tmp/wisdom.md &
cat /tmp/conv.txt | fabric -p extract_instructions > /tmp/steps.md &
cat /tmp/conv.txt | fabric -p extract_primary_problem > /tmp/problem.md &
cat /tmp/conv.txt | fabric -p extract_primary_solution > /tmp/solution.md &
wait

# 3. Review extractions
cat /tmp/problem.md
cat /tmp/solution.md
cat /tmp/steps.md
cat /tmp/wisdom.md

# 4. Generate skill (manually combine or use template)
```

## Additional Resources

### Scripts

- **`scripts/parse_conversation.sh`** - Convert JSONL to readable text
- **`scripts/extract_skill.sh`** - Full extraction pipeline

### References

- **`references/fabric_patterns.md`** - Detailed guide to Fabric patterns
- **`references/skill_template.md`** - SKILL.md template with all sections

### Examples

- **`examples/example_extraction.md`** - Complete example of extraction process

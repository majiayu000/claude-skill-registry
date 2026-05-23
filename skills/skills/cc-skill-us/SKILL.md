---
name: cc-skill-us
description: "This skill should be used when the user asks to 'extract a skill from a debugging session', 'convert debugging session to skill', 'create skill from debug history', 'generate skill from troubleshooting', or mentions extracting reusable knowledge from Claude Code debugging conversations. Transforms conversation history into well-structured, reusable skills using conversation parsing and Fabric AI patterns."
---

# Extract Skill from Claude Code Debugging Session

Systematically extract reusable skills and knowledge from Claude Code debugging sessions using conversation history, Fabric AI patterns, and automated skill generation. Transform tribal knowledge buried in conversations into actionable, well-structured documentation.

## Core Concept

Debugging sessions contain valuable workflows hidden within exploration, trial-and-error, and backtracking. The working solution gets obscured by dead ends and failed attempts. This skill extracts the reusable essence—the recipe that actually worked—and transforms it into a well-structured, shareable skill.

Key principle: **Document the recipe, not the discovery journey.**

## When to Use This Skill

- Convert a debugging session into a reusable debugging skill
- Extract feature implementation workflows from conversations
- Document troubleshooting patterns discovered during problem-solving
- Create skills from research or learning conversations
- Preserve tribal knowledge from past sessions before it's forgotten
- Transform exploratory conversations into procedural guidance

## Steps

### Step 1: Locate the Conversation JSONL File

Claude Code stores conversations as JSONL (JSON Lines) in project-specific directories:

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

The project path is encoded as a directory name. For example, `/home/rcalleja/projects/claude-market-place` becomes `-home-rcalleja-projects-claude-market-place`.

### Step 2: Verify Dependencies

Ensure required tools are available:

```bash
# Check for Fabric (AI pattern extraction)
which fabric && fabric --version

# Check for jq (JSON parsing)
which jq --version
```

Install if missing:

```bash
# Install Fabric
go install github.com/danielmiessler/fabric@latest

# Install jq (via your package manager)
# macOS: brew install jq
# Linux: apt-get install jq (Ubuntu/Debian) or yum install jq (RHEL/CentOS)
```

### Step 3: Parse Conversation to Readable Text

Convert JSONL format to readable text using the parse script from skill-extractor:

```bash
bash plugins/skill-extractor/skills/extract-skill-from-conversation/scripts/parse_conversation.sh \
  /path/to/session.jsonl > /tmp/conversation.txt
```

This script extracts:
- User messages
- Assistant responses (with tool calls summarized)
- Tool execution results
- Conversation summaries

Result: A readable conversation transcript without JSONL formatting noise.

### Step 4: Extract Skill Components Using Fabric Patterns

Apply multiple Fabric patterns in parallel to extract different aspects of the conversation:

```bash
cat /tmp/conversation.txt | fabric -p extract_wisdom > /tmp/wisdom.md &
cat /tmp/conversation.txt | fabric -p extract_instructions > /tmp/instructions.md &
cat /tmp/conversation.txt | fabric -p extract_primary_problem > /tmp/problem.md &
cat /tmp/conversation.txt | fabric -p extract_primary_solution > /tmp/solution.md &
wait
```

**Fabric patterns explained:**

| Pattern | Extracts | Use For |
|---------|----------|---------|
| `extract_wisdom` | Key insights and learnings | "Key Insights" section in skill |
| `extract_instructions` | Step-by-step procedures | "Steps" section in skill |
| `extract_primary_problem` | Core problem statement | "Problem Pattern" section |
| `extract_primary_solution` | What actually worked | Solution summary |

Running in parallel significantly speeds up extraction compared to sequential processing.

### Step 5: Review the Extracted Components

Examine what each Fabric pattern extracted:

```bash
cat /tmp/problem.md
cat /tmp/solution.md
cat /tmp/instructions.md
cat /tmp/wisdom.md
```

This gives you the raw material for the skill. These extractions will be refined in the next steps.

### Step 6: Generate the Skill Using plugin-dev:skill-development

Instead of manually creating the SKILL.md file, use the `plugin-dev:skill-development` skill to generate it automatically.

Invoke the skill with the following prompt:

```
Create a new skill for Claude Code plugins based on this debugging session:

## Problem Summary
[Paste content from /tmp/problem.md]

## Solution That Worked
[Paste content from /tmp/solution.md]

## Actionable Steps
[Paste content from /tmp/instructions.md]

## Key Insights
[Paste content from /tmp/wisdom.md]

## Requirements
- Skill name: [skill-name-derived-from-problem]
- Write in imperative/infinitive form (not second person)
- Target 1,500-2,000 words for SKILL.md body
- Move detailed content to references/
- Include working examples in examples/
- Create utility scripts in scripts/ if applicable
- Focus on the "recipe that worked" without trial-and-error noise
```

This will guide you through:
1. Naming the skill appropriately
2. Writing effective trigger descriptions
3. Creating lean SKILL.md content with progressive disclosure
4. Organizing references, examples, and scripts
5. Following best practices for Claude Code skills

### Step 7: Refine and Remove Noise

After generating the skill structure with `plugin-dev:skill-development`, perform final refinement:

1. **Remove trial-and-error**: Delete mentions of attempts that failed. Keep only the working path.
2. **Distill explanations**: Convert verbose descriptions to concise instructions.
3. **Use imperative voice**: Change "I did X" or "you should do X" to "Do X".
4. **Verify commands**: Test each referenced command and file path exists.
5. **Check prerequisites**: Document assumptions about tools, credentials, or setup.
6. **Validate on fresh problem**: Use the extracted skill to solve a similar problem to verify completeness.

### Step 8: Store and Test the Generated Skill

Place the generated skill in your plugin:

```bash
# For plugins in development
cp -r /path/to/generated-skill plugins/your-plugin/skills/skill-name/

# Test by asking Claude a question that should trigger it
cc --plugin-dir /path/to/plugin
```

The skill will be discovered automatically when Claude Code scans the `skills/` directory.

## Key Insights

- **Conversations contain buried value**: Every debugging session includes exploration, dead ends, and backtracking that obscures the actual working solution.

- **JSONL format enables streaming**: Claude Code stores conversations as JSONL, allowing efficient parsing without loading entire conversations into memory.

- **Multiple Fabric patterns extract different aspects**: Running patterns in parallel extracts wisdom, instructions, problems, and solutions simultaneously for comprehensive coverage.

- **Parse-then-extract workflow separates concerns**: Converting JSONL to readable text first, then applying Fabric patterns, improves reusability and clarity.

- **Parallel extraction saves significant time**: Running multiple Fabric patterns simultaneously completes extraction much faster than sequential processing.

- **Curation is essential**: Fabric extractions provide raw material—synthesizing them into a skill requires deliberate curation to maintain focus and clarity.

- **Recipes matter more than stories**: Document what to do, not how you discovered it. The working solution stands alone without exploratory narrative.

- **Tool calls provide critical context**: Conversation tool calls and results show exactly what executed successfully, which is more reliable than narrative descriptions.

- **Prerequisites aren't always obvious**: Document assumptions, required tools, credentials, or setup steps that might not be clear to someone replicating the workflow later.

- **Pattern recognition is valuable knowledge**: Insights like "this error type usually means X" or "this tool is commonly mistaken for Y" are worth capturing in skills.

- **Skill validation prevents distribution of incomplete workflows**: Testing the extracted skill on a similar problem verifies completeness before sharing.

- **Progressive disclosure keeps skills focused**: Lean SKILL.md with detailed content in references/ means essential information loads immediately when needed.

- **Imperative language improves clarity**: Verb-first instructions are easier to follow than narrative explanations for procedural guidance.

- **Claude Code project paths are encoded**: Project paths are transformed to directory names in `~/.claude/projects/`, making conversations easy to locate programmatically.

- **Skill-extractor plugin is meta-documentation**: The plugin documents its own extraction process, serving as both a tool and example of skill extraction in action.

## Common Mistakes to Avoid

- **Including all exploration**: Including too much trial-and-error narrative. Edit ruthlessly; keep only the critical path to the solution.

- **Forgetting to verify commands**: Commands extracted from conversation may have changed or contain typos. Test each command before finalizing the skill.

- **Verbose explanations**: Converting verbose conversation explanations directly into skills. Distill to essence; remove redundancy.

- **Missing prerequisites**: Assuming readers share your context. Document required tools, versions, credentials, file paths, and dependencies explicitly.

- **Narrative voice in procedures**: Writing "I did X" or "You should do X" instead of "Do X". Use imperative voice for step-by-step instructions.

- **Retaining failed alternatives**: Including alternative approaches you tried but abandoned. Focus on the single best approach that worked.

- **Skipping validation**: Not testing the extracted skill on a fresh problem. Always validate completeness before distribution.

- **Dead-end references**: Including URLs or files that led nowhere. Reference only materials that directly contribute to the solution.

- **Losing context about tool dependencies**: Not documenting why specific tools are required or their role in the workflow.

- **Over-fitting to specific scenario**: Making the skill too specific to your exact situation instead of generalizable to similar problems.

## References

For detailed guidance on related topics, consult:

- **Fabric AI patterns**: `https://github.com/danielmiessler/fabric` - Documentation on pattern extraction
- **Claude Code conversation storage**: `~/.claude/projects/` - Where conversations are stored
- **skill-extractor plugin**: `plugins/skill-extractor/` - Pre-built scripts and templates
- **plugin-dev documentation**: Official Claude Code plugin development guides

## Bundled Resources

This skill leverages resources from the skill-extractor plugin:

- **Parse script**: `skills/extract-skill-from-conversation/scripts/parse_conversation.sh` - Converts JSONL to readable text
- **Fabric patterns reference**: `skills/extract-skill-from-conversation/references/fabric_patterns.md` - Detailed pattern documentation
- **Skill template**: `skills/extract-skill-from-conversation/references/skill_template.md` - SKILL.md template structure

When using this skill, refer to these bundled resources for detailed guidance on pattern extraction and skill structure.
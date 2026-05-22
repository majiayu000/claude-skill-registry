---
name: optimize-prompt-token-efficiency
description: 'Iteratively optimizes prompts for token efficiency by maximizing information density - reduces verbosity, removes redundancy, tightens phrasing while preserving semantic content. Use when asked to compress, shorten, reduce tokens, tighten, maximize density, increase information density, or make a prompt more concise.'
---

# Optimize Prompt Token Efficiency

Iteratively optimize prompt token efficiency by maximizing information density through verification loops. Primary goal: reduce token consumption while preserving all semantic content for AI-consumed prompts (CLAUDE.md, skills, agent prompts, specs).

## Overview

This skill transforms verbose prompts into token-efficient versions through:
1. **Verification First** - `prompt-token-efficiency-verifier` checks for inefficiencies before any changes
2. **Optimization** - Apply targeted compression based on verifier feedback
3. **Re-verification** - Verify compression is lossless, iterate if issues remain (max 5 iterations)
4. **Output** - Atomic replacement only after verification passes

**Loop**: Read → Verify → (Exit if efficient) → Optimize based on feedback → Re-verify → (Iterate if issues) → Output

**Key principle**: Don't try to optimize in one pass. The verifier drives all changes - if it finds no inefficiencies, the prompt is already token-efficient.

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases. List reflects areas of work, not fixed steps.

**Starter todos**:
```
- [ ] Input validation
- [ ] Initial verification
- [ ] (Expand: optimization iterations on INEFFICIENCIES_FOUND)
- [ ] Output optimized prompt
```

### Phase 1: Input Validation

**Mark "Input validation" todo `in_progress`.**

**Step 1.1: Parse arguments**

Extract file path from `$ARGUMENTS`. If no path provided, error with usage instructions.

**Step 1.2: Validate file**

- Check file exists using Read tool
- Verify supported type: `.md`, `.txt`, `.yaml`, `.json`
- If unsupported, error: "Unsupported file type. Supported: .md, .txt, .yaml, .json"

**Step 1.3: Read and measure original**

- Read file content
- Estimate token count: `Math.ceil(content.length / 4)` (approximate)
- Store original content and token count for comparison

**Step 1.4: Store metadata**

- `original_path`: Source file path
- `original_content`: Full prompt text
- `original_tokens`: Estimated token count
- `working_path`: `/tmp/optimized-efficiency-{timestamp}.{ext}` for iterations

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Verification

**Mark "Initial verification" todo `in_progress`.**

**Step 2.1: Copy to working path**

Copy original content to working_path using Write tool (verification needs a file path).

**Step 2.2: Run verifier first**

Launch prompt-token-efficiency-verifier agent via Task tool BEFORE any optimization:
- subagent_type: "prompt-engineering:prompt-token-efficiency-verifier"
- prompt: "Verify prompt token efficiency. File: {working_path}. Check for redundancy, verbose phrasing, filler words, structural inefficiencies, and compression opportunities. Report VERIFIED if already efficient, or INEFFICIENCIES_FOUND with specific details."

**Step 2.3: Handle verifier response**

- If "VERIFIED": Mark todo completed, proceed directly to Phase 4 (Output) with message: "Prompt is already token-efficient. No changes needed."
- If "INEFFICIENCIES_FOUND": Mark todo completed, save the issues list, add "Optimization iteration 1" todo and proceed to Phase 3
- If verifier fails or returns unexpected format: Retry once with identical parameters. If retry fails, report error: "Verification failed - cannot proceed without verifier."

**Step 2.4: Display verifier findings**

If inefficiencies found, show user summary and proceed:

```
Verifier found {count} token efficiency issues. Proceeding with optimization...
```

**Mark "Initial verification" todo `completed`.**

### Phase 3: Optimization Loop (Verifier-Driven)

**Mark "Optimization iteration 1" todo `in_progress`.**

**Key principle**: All fixes are driven by verifier feedback. Do NOT analyze the prompt independently - only fix the specific inefficiencies the verifier reported.

For each iteration from 1 to 5:

1. **Apply compressions from verifier feedback**: For each inefficiency in the verifier's report, apply the suggested compression. Write optimized version to working_path.
   - Only fix inefficiencies the verifier identified - do not add your own improvements

2. **Re-verify**: Launch prompt-token-efficiency-verifier agent via Task tool:
   - subagent_type: "prompt-engineering:prompt-token-efficiency-verifier"
   - prompt: "Verify compression is lossless. Original file: {original_path}. Compressed file: {working_path}. Compare semantic content - check for missing facts, altered meaning, lost emphasis, removed nuance. Report VERIFIED if lossless, or ISSUES_FOUND with specific gaps."

3. **Handle response**:
   - If "VERIFIED": mark todo completed, exit loop, proceed to Phase 4
   - If "ISSUES_FOUND" and iteration < 5: mark todo completed, save new issues list, add "Optimization iteration {next}" todo, continue to next iteration
   - If "ISSUES_FOUND" and iteration = 5: mark todo completed with note about unresolved issues, proceed to Phase 4 with warning
   - If verifier fails or returns unexpected format: display error to user, retry once with identical parameters. If retry fails, proceed to Phase 4 with warning: "Verification incomplete - manual review recommended."

### Compression Techniques

Apply these techniques to fix inefficiencies flagged by the verifier:

| Technique | Description | Before → After |
|-----------|-------------|----------------|
| **Redundancy removal** | Eliminate repeated concepts | "It is important to note that you should always remember to..." → "Always..." |
| **Terse phrasing** | Replace verbose constructions | "In order to accomplish this task, you will need to..." → "To do this:" |
| **Filler elimination** | Remove hedging, qualifiers, throat-clearing | "Make sure that you do not forget to include..." → "Include:" |
| **Structural optimization** | Merge/reorganize sections | "First X. After that Y. Then Z." → "Steps: X → Y → Z" |
| **Context-aware abbreviation** | Abbreviate terms after first mention | "Model Context Protocol server" (×10) → "MCP server" (after first) |
| **Dense formatting** | Use lists, tables, compact notation | Prose paragraphs → Tables, bullet lists |

**Transformation Rules**:

1. **Preserve ALL semantic information** - Every fact, instruction, constraint, and example must be present
2. **Preserve nuance and emphasis** - Bold, caps, repetition, ordering that signals priority; intentional hedging (uncertainty was meaningful)
3. **Restructuring allowed** - Reorder, merge sections if it increases density WITHOUT losing priority signals
4. **Format preservation** - Output must be same format as input (markdown stays markdown)
5. **No reduction target** - 10% reduction with nuance preserved > 40% reduction with nuance lost

**Avoid creating ambiguity**:
- Don't merge conditions with different triggers ("when A, do X; when B, do Y" ≠ "when A/B, do X/Y")
- Keep explicit referents (don't reduce "Use Read tool" to "Use the tool" if context is unclear)
- Don't flatten relationships ("A requires B, C requires D" ≠ "A, C require B, D")
- Ensure scope is clear (qualifier applies to which items?)

### Phase 4: Output

**Mark "Output optimized prompt" todo `in_progress`.**

**Step 4.1: Calculate metrics**

- Original token count (from Phase 1)
- Compressed token count: `Math.ceil(compressed_content.length / 4)`
- Reduction percentage: `((original - compressed) / original * 100).toFixed(0)`

**Step 4.2: Apply changes (atomic replacement)**

If verification passed:
```bash
# Replace original atomically
mv {working_path} {original_path}
```

**Step 4.3: Display results**

If verification passed:
```
Optimized: {path}
Iterations: {count}
Original:  {original_tokens} tokens
Optimized: {compressed_tokens} tokens
Reduction: {percentage}%

Changes applied:
- {summary of compressions}

Status: Token-efficient and lossless
```

If verification failed after 5 iterations:
```
Optimized with warnings: {path}
Iterations: 5
Original:  {original_tokens} tokens
Optimized: {compressed_tokens} tokens
Reduction: {percentage}%

Unresolved issues:
- {list from last verification}

Review the changes manually.
```

**Mark "Output optimized prompt" todo `completed`. Mark all todos complete.**

## Key Principles

| Principle | Rule |
|-----------|------|
| **Verify first** | Always run verifier before any optimization; maybe prompt is already efficient |
| **Verifier-driven** | Only fix inefficiencies the verifier identifies - no independent analysis or improvements |
| **Track progress** | TodoWrite to track phases; expand todos on iteration |
| **Losslessness** | Never sacrifice semantic information for density; every fact must be preserved |
| **Nuance preservation** | Keep emphasis, intentional hedging, priority signals; 10% with nuance > 40% without |
| **No ambiguity** | Compressed must be as unambiguous as original |
| **Verification required** | Never output without verifier checking |
| **Atomic output** | Original untouched until verification passes |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Error: "Usage: /optimize-prompt-token-efficiency <file-path>" |
| File not found | Error: "File not found: {path}" |
| Unsupported type | Error: "Unsupported file type. Supported: .md, .txt, .yaml, .json" |
| Already efficient | Verifier returns VERIFIED on first check → Report: "Prompt is already token-efficient. No changes needed." |
| Initial verifier fails | Retry once; if still fails, Error: "Verification failed - cannot proceed without verifier." |
| Re-verification fails | Display error, retry once; if retry fails, output with warning |
| YAML/JSON structure | Preserve structure validity, compress string values only |
| Very large file (>50KB) | Process as single unit |
| 0-10% reduction | Success: "Content was already near-optimal density" |
| Verification fails 5x | Output best attempt with warning |

## Example Usage

```bash
# Optimize a verbose CLAUDE.md
/optimize-prompt-token-efficiency CLAUDE.md

# Optimize a skill file
/optimize-prompt-token-efficiency claude-plugins/my-plugin/skills/my-skill/SKILL.md

# Optimize an agent prompt
/optimize-prompt-token-efficiency agents/code-reviewer.md
```

## Example Output

```
Optimized: docs/README.md
Iterations: 2
Original:  4,250 tokens
Optimized: 3,612 tokens
Reduction: 15%

Changes applied:
- Removed redundant intro section
- Consolidated overlapping examples
- Tersified verbose instructions
- Preserved emphasis markers and conditional logic

Status: Token-efficient and lossless
```

```
Prompt is already token-efficient. No changes needed.
Original: 1,995 tokens
```

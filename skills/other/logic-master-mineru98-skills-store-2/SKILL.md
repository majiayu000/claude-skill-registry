---
name: logic-master
description: Logic optimization and image-based code tasks with Codex CLI in --yolo mode. Use when (1) optimizing code logic or algorithms, (2) processing image inputs (screenshots, diagrams, mockups) to generate or modify code, (3) refactoring business logic, (4) debugging complex logic issues, (5) code generation from visual references, or (6) any task requiring image attachment for context.
---

# Codex Logic Skill

Execute logic optimization and image-based code tasks using Codex CLI in `--yolo` mode.

## When to Use

- Logic optimization: algorithm improvements, performance tuning
- Image-based tasks: generate code from screenshots, mockups, diagrams
- Refactoring: extract functions, simplify conditionals, reduce complexity
- Business logic: validation rules, data transformations, state machines
- Debugging: fix complex logic bugs, race conditions

## When NOT to Use

- Visual/styling changes (use `frontend-master` skill instead)
- CSS, layout, colors, typography, animations

## Execution Pattern

### Basic Command Structure

```bash
# Direct prompt
codex exec --yolo "<instruction>"

# With file context via stdin
cat <file> | codex exec --yolo -

# With image attachment
codex exec --yolo --image <path-to-image> "<instruction>"

# With directory context
codex exec --yolo -C <directory> "<instruction>"
```

### Required Flags

| Flag | Purpose |
|------|---------|
| `--yolo` | **MANDATORY** - Auto-approve and bypass sandbox |
| `--image` or `-i` | Attach image files for visual context |
| `--json` | Get JSONL event stream for parsing |
| `-o` or `--output-last-message` | Save final output to file |
| `-C` or `--cd` | Change working directory |
| `--sandbox` | Set access level (workspace-write recommended) |
| `--model` or `-m` | Override model selection |

### Workflow

1. **Identify task type**: logic optimization or image-based
2. **Prepare inputs**: file content or image path
3. **Construct Codex command** with `--yolo` flag
4. **Execute** via bash tool
5. **Capture output** and delegate to subagent for implementation
6. **Verify results** with `lsp_diagnostics`

## Image-Based Tasks

### Generate Code from Screenshot

```bash
# UI mockup to component
codex exec --yolo --image mockup.png "Generate React component matching this design"

# Diagram to code
codex exec --yolo --image architecture.png "Implement the data flow shown in this diagram"

# Error screenshot to fix
codex exec --yolo --image error-screenshot.png "Analyze this error and provide fix"
```

### Multiple Images

```bash
codex exec --yolo --image before.png --image after.png "Generate code to transform UI from before to after state"
```

## Logic Optimization Tasks

### Algorithm Optimization

```bash
# Optimize function
cat src/utils/sort.ts | codex exec --yolo - "Optimize this sorting algorithm for large datasets"

# Reduce complexity
cat src/services/parser.ts | codex exec --yolo - "Refactor to reduce cyclomatic complexity"
```

### Refactoring

```bash
# Extract functions
cat src/handlers/user.ts | codex exec --yolo - "Extract reusable validation logic into separate functions"

# Simplify conditionals
cat src/logic/pricing.ts | codex exec --yolo - "Simplify nested conditionals using early returns"
```

### Performance Tuning

```bash
# Memory optimization
cat src/data/processor.ts | codex exec --yolo - "Optimize memory usage, avoid unnecessary allocations"

# Async optimization
codex exec --yolo -C src/services "Identify and fix N+1 query patterns"
```

## Output Handling

### JSON Output for Parsing

```bash
codex exec --yolo --json "Generate utility function" | jq -r '.content'
```

### Save to File

```bash
codex exec --yolo -o result.ts "Generate TypeScript interface from this JSON schema"
```

### Resume Session

```bash
# Continue previous work
codex exec resume --last "Apply the suggested changes"
```

## Integration with Subagents

After Codex CLI provides analysis/suggestions, delegate implementation:

```
1. TASK: Implement logic changes based on Codex analysis
2. EXPECTED OUTCOME: Optimized code matching Codex recommendations
3. REQUIRED SKILLS: logic-master
4. REQUIRED TOOLS: Bash (for codex CLI), Read, Edit, lsp_diagnostics
5. MUST DO:
   - Execute codex exec with --yolo flag first
   - Parse Codex output for implementation steps
   - Apply changes using Edit tool
   - Verify with lsp_diagnostics
   - Run tests if available
6. MUST NOT DO:
   - Modify styling/visual elements
   - Skip verification step
   - Ignore Codex warnings or caveats
7. CONTEXT: [file paths, performance requirements, constraints]
```

### Image-Based Workflow Example

```
1. TASK: Generate component from design mockup
2. EXPECTED OUTCOME: Working React component matching mockup
3. REQUIRED SKILLS: logic-master
4. REQUIRED TOOLS: Bash (for codex CLI), Write, lsp_diagnostics
5. MUST DO:
   - Use codex exec --yolo --image <path> to analyze mockup
   - Create component based on Codex output
   - Match existing component patterns in codebase
   - Verify types with lsp_diagnostics
6. MUST NOT DO:
   - Generate inline styles (use existing CSS framework)
   - Create new dependencies without approval
7. CONTEXT: [mockup path, component location, existing patterns]
```

## Example Complete Workflow

```bash
# Step 1: Analyze image and get code suggestion
codex exec --yolo --image ui-mockup.png "Analyze this mockup and describe the React component structure needed" -o analysis.md

# Step 2: Generate implementation
codex exec --yolo --image ui-mockup.png "Generate React component code for this mockup using Tailwind CSS" -o Component.tsx

# Step 3: Verify and integrate
# (delegate to subagent to place file, add imports, run diagnostics)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Image not recognized | Use absolute path or ensure file exists |
| Command hangs | Ensure `--yolo` flag is present |
| Sandbox errors | Add `--sandbox workspace-write` |
| Large output truncated | Use `-o <file>` to save full output |
| Model unavailable | Try `--model gpt-4o` or check API key |

## Security Note

`--yolo` mode bypasses approval and sandbox restrictions. Use only when:
- Working in version-controlled directories
- Changes can be easily reverted
- No sensitive operations or credentials involved
- Running in isolated development environment

---
name: frontend-master
description: Frontend UI/UX work with Gemini CLI in --yolo mode. Use when (1) modifying visual/styling elements in frontend files (.tsx, .jsx, .vue, .svelte, .css), (2) implementing UI components, (3) adjusting layout, colors, spacing, typography, or animations, (4) creating responsive designs, or (5) any frontend task involving how things LOOK rather than how they WORK.
---

# Gemini Frontend Skill

Execute frontend UI/UX tasks using Gemini CLI in `--yolo` mode for automatic approval.

## When to Use

- Visual changes: colors, backgrounds, borders, shadows
- Layout: flexbox, grid, margins, padding, positioning
- Typography: font sizes, weights, line heights
- Animation: transitions, keyframes, hover states
- Responsive design: breakpoints, media queries
- Component styling: Tailwind, CSS-in-JS, styled-components

## When NOT to Use

- Pure logic changes (API calls, state management, event handlers)
- Type definitions, utility functions, business logic
- Use `logic-master` skill for logic optimization or image-based tasks

## Execution Pattern

### Basic Command Structure

```bash
# With file context
cat <frontend-file> | gemini --yolo --prompt "<instruction>"

# With directory context
gemini --yolo --prompt "<instruction>" --include-directories <dirs>

# With all project files
gemini --yolo --prompt "<instruction>" --all-files
```

### Required Flags

| Flag | Purpose |
|------|---------|
| `--yolo` | **MANDATORY** - Auto-approve all changes |
| `--prompt` or `-p` | Specify the task |
| `--include-directories` | Add specific folders to context |
| `--all-files` or `-a` | Include full project context |
| `--output-format json` | Get structured output for parsing |

### Workflow

1. **Identify frontend file(s)** to modify
2. **Construct Gemini command** with `--yolo` flag
3. **Execute** via bash tool
4. **Verify results** with `lsp_diagnostics`
5. **Apply changes** if output is satisfactory

## Example Commands

### Modify Component Styling

```bash
# Update button styles
cat src/components/Button.tsx | gemini --yolo -p "Change button color to blue-500, add hover:scale-105 transition"

# Responsive navbar
gemini --yolo -p "Make the navbar responsive with hamburger menu on mobile" --include-directories src/components
```

### Layout Changes

```bash
# Convert to grid layout
cat src/pages/Dashboard.tsx | gemini --yolo -p "Convert this layout to CSS Grid with 3 columns"

# Add spacing
gemini --yolo -p "Add consistent spacing between cards using gap-4" --include-directories src/components/cards
```

### Animation & Effects

```bash
# Add transitions
cat src/components/Modal.tsx | gemini --yolo -p "Add fade-in animation when modal opens"

# Hover effects
gemini --yolo -p "Add subtle shadow and scale effect on card hover" --include-directories src/components
```

### Full Project Changes

```bash
# Theme update
gemini --yolo -p "Update all components to use dark mode color palette" --all-files

# Design system alignment
gemini --yolo -p "Align all buttons to use design system tokens" --all-files
```

## Output Handling

### Get JSON Output for Scripting

```bash
gemini --yolo -p "List all CSS classes used in this component" --output-format json | jq '.response'
```

### Save Changes to File

```bash
cat src/styles/main.css | gemini --yolo -p "Add responsive utilities" > src/styles/main.css.new
```

## Integration with Subagents

When delegating to `frontend-ui-ux-engineer`:

```
1. TASK: Execute Gemini CLI to update component styling
2. EXPECTED OUTCOME: Component with updated visual styles
3. REQUIRED SKILLS: frontend-master
4. REQUIRED TOOLS: Bash (for gemini CLI), Read, lsp_diagnostics
5. MUST DO: 
   - Use --yolo flag for auto-approval
   - Verify changes with lsp_diagnostics after execution
   - Match existing Tailwind/CSS patterns in codebase
6. MUST NOT DO:
   - Modify logic or event handlers
   - Remove existing functionality
   - Use --approval-mode (use --yolo instead)
7. CONTEXT: [file paths, design requirements, existing patterns]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command hangs | Ensure `--yolo` flag is present |
| No changes made | Check file is in context (use `--include-directories`) |
| Unexpected changes | Add more specific constraints in prompt |
| Build errors | Run `lsp_diagnostics` and fix type issues |

## Security Note

`--yolo` mode auto-approves ALL actions. Use only when:
- Working in version-controlled directories
- Changes can be easily reverted
- No sensitive operations involved

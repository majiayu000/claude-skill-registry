---
name: ui-implementer
description: Implements UI components from scratch based on design references (Figma, screenshots, mockups) with intelligent validation and adaptive agent switching. Use when user provides a design and wants pixel-perfect UI implementation with design fidelity validation. Triggers automatically when user mentions Figma links, design screenshots, or wants to implement UI from designs.
allowed-tools: Task, AskUserQuestion, Bash, Read, TodoWrite, Glob, Grep
---

# UI Implementer

This Skill implements UI components from scratch based on design references using specialized UI development agents with intelligent validation and adaptive agent switching for optimal results.

## When to use this Skill

Claude should invoke this Skill when:

**Design References Provided:**
- User shares a Figma URL (e.g., "Here's the Figma design: https://figma.com/...")
- User provides a screenshot/mockup path (e.g., "I have a design at /path/to/design.png")
- User mentions a design URL they want to implement

**Intent to Implement UI:**
- "Implement this UI design"
- "Create components from this Figma file"
- "Build this interface from the mockup"
- "Make this screen match the design"

**Pixel-Perfect Requirements:**
- "Make it look exactly like the design"
- "Implement pixel-perfect from Figma"
- "Match the design specifications exactly"

**Examples of User Messages:**
- "Here's a Figma link, can you implement the UserProfile component?"
- "I have a design screenshot, please create the dashboard layout"
- "Implement this navbar from the mockup at designs/navbar.png"
- "Build the product card to match this Figma: https://figma.com/..."

## DO NOT use this Skill when:

- User just wants to validate existing UI (use browser-debugger or /validate-ui instead)
- User wants to fix existing components (use regular developer agent)
- User wants to implement features without design reference (use regular implementation flow)

## Instructions

This Skill implements the same workflow as the `/implement-ui` command. Follow these phases:

### PHASE 0: Initialize Workflow

Create a global todo list to track progress:

```
TodoWrite with:
- PHASE 1: Gather inputs (design reference, component description, preferences)
- PHASE 1: Validate inputs and find target location
- PHASE 2: Launch UI Developer for initial implementation
- PHASE 3: Start validation and iterative fixing loop
- PHASE 3: Quality gate - ensure design fidelity achieved
- PHASE 4: Generate final implementation report
- PHASE 4: Present results and complete handoff
```

### PHASE 1: Gather User Inputs

**Step 1: Extract Design Reference**

Check if user already provided design reference in their message:
- Scan for Figma URLs: `https://figma.com/design/...` or `https://figma.com/file/...`
- Scan for file paths: `/path/to/design.png`, `~/designs/mockup.jpg`
- Scan for remote URLs: `http://example.com/design.png`

If design reference found in user's message:
- Extract and store as `design_reference`
- Log: "Design reference detected: [design_reference]"

If NOT found, ask:
```
I'd like to implement UI from your design reference.

Please provide the design reference:
1. Figma URL (e.g., https://figma.com/design/abc123.../node-id=136-5051)
2. Screenshot file path (local file on your machine)
3. Remote URL (live design reference)

What is your design reference?
```

**Step 2: Extract Component Description**

Check if user mentioned what to implement:
- Look for component names: "UserProfile", "navbar", "dashboard", "ProductCard"
- Look for descriptions: "implement the header", "create the sidebar", "build the form"

If found:
- Extract and store as `component_description`

If NOT found, ask:
```
What UI component(s) should I implement from this design?

Examples:
- "User profile card component"
- "Navigation header with mobile menu"
- "Product listing grid with filters"
- "Dashboard layout with widgets"

What component(s) should I implement?
```

**Step 3: Ask for Target Location**

Ask:
```
Where should I create this component?

Options:
1. Provide a specific directory path (e.g., "src/components/profile/")
2. Let me suggest based on component type
3. I'll tell you after seeing the component structure

Where should I create the component files?
```

Store as `target_location`.

**Step 4: Ask for Application URL**

Ask:
```
What is the URL where I can preview the implementation?

Examples:
- http://localhost:5173 (Vite default)
- http://localhost:3000 (Next.js/CRA default)
- https://staging.yourapp.com

Preview URL?
```

Store as `app_url`.

**Step 5: Ask for UI Developer Codex Preference**

Use AskUserQuestion:
```
Enable intelligent agent switching with UI Developer Codex?

When enabled:
- If UI Developer struggles (2 consecutive failures), switches to UI Developer Codex
- If UI Developer Codex struggles (2 consecutive failures), switches back
- Provides adaptive fixing with both agents for best results

Enable intelligent agent switching?
```

Options:
- "Yes - Enable intelligent agent switching"
- "No - Use only UI Developer"

Store as `codex_enabled` (boolean).

**Step 6: Validate Inputs**

Validate all inputs using the same logic as /implement-ui command:
- Design reference format (Figma/Remote/Local)
- Component description not empty
- Target location valid
- Application URL valid

### PHASE 2: Initial Implementation from Scratch

Launch UI Developer agent using Task tool with `subagent_type: frontend:ui-developer`:

```
Implement the following UI component(s) from scratch based on the design reference.

**Design Reference**: [design_reference]
**Component Description**: [component_description]
**Target Location**: [target_location]
**Application URL**: [app_url]

**Your Task:**

1. **Analyze the design reference:**
   - If Figma: Use Figma MCP to fetch design screenshot and specs
   - If Remote URL: Use Chrome DevTools MCP to capture screenshot
   - If Local file: Read the file to view design

2. **Plan component structure:**
   - Determine component hierarchy
   - Identify reusable sub-components
   - Plan file structure (atomic design principles)

3. **Implement UI components from scratch using modern best practices:**
   - React 19 with TypeScript
   - Tailwind CSS 4 (utility-first, static classes only, no @apply)
   - Mobile-first responsive design
   - Accessibility (WCAG 2.1 AA, ARIA attributes)
   - Use existing design system components if available

4. **Match design reference exactly:**
   - Colors (Tailwind theme or exact hex)
   - Typography (families, sizes, weights, line heights)
   - Spacing (Tailwind scale: p-4, p-6, etc.)
   - Layout (flexbox, grid, alignment)
   - Visual elements (borders, shadows, border-radius)
   - Interactive states (hover, focus, active, disabled)

5. **Create component files in target location:**
   - Use Write tool to create files
   - Follow project conventions
   - Include TypeScript types
   - Add JSDoc comments

6. **Ensure code quality:**
   - Run typecheck: `npx tsc --noEmit`
   - Run linter: `npm run lint`
   - Run build: `npm run build`
   - Fix any errors

7. **Provide implementation summary:**
   - Files created
   - Components implemented
   - Key decisions
   - Any assumptions

Return detailed implementation summary when complete.
```

Wait for UI Developer to complete.

### PHASE 3: Validation and Adaptive Fixing Loop

Initialize loop variables:
```
iteration_count = 0
max_iterations = 10
previous_issues_count = None
current_issues_count = None
last_agent_used = None
ui_developer_consecutive_failures = 0
codex_consecutive_failures = 0
design_fidelity_achieved = false
```

**Loop: While iteration_count < max_iterations AND NOT design_fidelity_achieved**

**Step 3.1: Launch Designer for Validation**

Use Task tool with `subagent_type: frontend:designer`:

```
Review the implemented UI component against the design reference.

**Iteration**: [iteration_count + 1] / 10
**Design Reference**: [design_reference]
**Component Description**: [component_description]
**Implementation Files**: [List of files]
**Application URL**: [app_url]

**Your Task:**
1. Fetch design reference screenshot
2. Capture implementation screenshot at [app_url]
3. Perform comprehensive design review:
   - Colors & theming
   - Typography
   - Spacing & layout
   - Visual elements
   - Responsive design
   - Accessibility (WCAG 2.1 AA)
   - Interactive states

4. Document ALL discrepancies
5. Categorize by severity (CRITICAL/MEDIUM/LOW)
6. Provide actionable fixes with code snippets
7. Calculate design fidelity score (X/60)

8. **Overall assessment:**
   - PASS ✅ (score >= 54/60)
   - NEEDS IMPROVEMENT ⚠️ (score 40-53/60)
   - FAIL ❌ (score < 40/60)

Return detailed design review report.
```

**Step 3.2: Check if Design Fidelity Achieved**

Extract from designer report:
- Overall assessment
- Issue count
- Design fidelity score

If assessment is "PASS":
- Set `design_fidelity_achieved = true`
- Exit loop (success)

**Step 3.3: Determine Fixing Agent (Smart Switching Logic)**

```javascript
function determineFix ingAgent() {
  // If Codex not enabled, always use UI Developer
  if (!codex_enabled) return "ui-developer"

  // Smart switching based on consecutive failures
  if (ui_developer_consecutive_failures >= 2) {
    // UI Developer struggling - switch to Codex
    return "ui-developer-codex"
  }

  if (codex_consecutive_failures >= 2) {
    // Codex struggling - switch to UI Developer
    return "ui-developer"
  }

  // Default: UI Developer (or continue with last successful)
  return last_agent_used || "ui-developer"
}
```

**Step 3.4: Launch Fixing Agent**

If `fixing_agent == "ui-developer"`:
- Use Task with `subagent_type: frontend:ui-developer`
- Provide designer feedback
- Request fixes

If `fixing_agent == "ui-developer-codex"`:
- Use Task with `subagent_type: frontend:ui-developer-codex`
- Prepare complete prompt with designer feedback + current code
- Request expert fix plan

**Step 3.5: Update Metrics and Loop**

```javascript
// Check if progress was made
const progress_made = (current_issues_count < previous_issues_count)

if (progress_made) {
  // Success! Reset counters
  ui_developer_consecutive_failures = 0
  codex_consecutive_failures = 0
} else {
  // No progress - increment failure counter
  if (last_agent_used === "ui-developer") {
    ui_developer_consecutive_failures++
  } else if (last_agent_used === "ui-developer-codex") {
    codex_consecutive_failures++
  }
}

// Update for next iteration
previous_issues_count = current_issues_count
iteration_count++
```

Continue loop until design fidelity achieved or max iterations reached.

### PHASE 4: Final Report & Completion

Generate comprehensive implementation report:

```markdown
# UI Implementation Report

## Component Information
- Component: [component_description]
- Design Reference: [design_reference]
- Location: [target_location]
- Preview: [app_url]

## Implementation Summary
- Files Created: [count]
- Components: [list]

## Validation Results
- Iterations: [count] / 10
- Final Status: [PASS/NEEDS IMPROVEMENT/FAIL]
- Design Fidelity Score: [score] / 60
- Issues: [count]

## Agent Performance
- UI Developer: [iterations, successes]
- UI Developer Codex: [iterations, successes] (if enabled)
- Agent Switches: [count] times

## Quality Metrics
- Design Fidelity: [Pass/Needs Improvement]
- Accessibility: [WCAG compliance]
- Responsive: [Mobile/Tablet/Desktop]
- Code Quality: [TypeScript/Lint/Build status]

## How to Use
[Preview instructions]
[Component location]
[Example usage]

## Outstanding Items
[List any remaining issues or recommendations]
```

Present results to user and offer next actions.

## Orchestration Rules

### Smart Agent Switching:
- Track consecutive failures independently for each agent
- Switch after 2 consecutive failures (no progress)
- Reset counters when progress is made
- Log all switches with reasons
- Balance UI Developer (speed) with UI Developer Codex (expertise)

### Loop Prevention:
- Maximum 10 iterations before asking user
- Track progress at each iteration (issue count)
- Ask user for guidance if limit reached

### Quality Gates:
- Design fidelity score >= 54/60 for PASS
- All CRITICAL issues must be resolved
- Accessibility compliance required

## Success Criteria

Complete when:
1. ✅ UI component implemented from scratch
2. ✅ Designer validated against design reference
3. ✅ Design fidelity score >= 54/60
4. ✅ All CRITICAL issues resolved
5. ✅ Accessibility compliant (WCAG 2.1 AA)
6. ✅ Responsive (mobile/tablet/desktop)
7. ✅ Code quality passed (typecheck/lint/build)
8. ✅ Comprehensive report provided
9. ✅ User acknowledges completion

## Notes

- This Skill wraps the `/implement-ui` command workflow
- Use proactively when user provides design references
- Implements from scratch (not for fixing existing UI)
- Smart switching maximizes success rate
- All work on unstaged changes until user approves
- Maximum 10 iterations with user escalation

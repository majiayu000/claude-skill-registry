---
name: Design to Code
description: This skill should be used when the user asks to "convert a design to code", "implement this UI", "build from Figma", "create component from screenshot", "one-shot UI generation", "generate code from design", or provides a design image (Figma export, Google Stitch output, screenshot) for implementation. Provides a structured multi-step workflow for translating visual designs into production-ready React components.
version: 1.1.0
title: "Design To Code"
status: active
---

# Design to Code Workflow

Transform design mockups into production-ready React components through a structured, research-informed workflow.

## Workflow Overview

This skill follows a 4-step process with explicit user approval:

```
Step 1: Image → Brief (PRD)           [User Approval Required]
Step 2: Brief → Component Research    [MCP tools + codebase patterns]
Step 3: Research → JSONC Spec         [Detailed specification]
Step 4: JSONC → Implementation        [Code generation]
```

Each step produces an artifact that feeds into the next, ensuring alignment with user expectations and optimal component selection.

## Step 1: Generate Brief from Design

### Input
- Design image (Figma export, Stitch screenshot, Gemini mockup, manual screenshot)
- HTML/CSS code file (when source is Stitch MCP -- `{section}-code.html`)
- Optional: `stitch-project.json` manifest (for iteration via edit_screens)

### Stitch-Aware Input Detection

When the design source includes HTML/CSS files (from Stitch MCP):
- Read BOTH the HTML file AND the screenshot
- Brief is derived from actual code structure (DOM elements, CSS classes) -- not visual interpretation
- Component identification from HTML tags, not guessing from pixels
- Set `source.tool = "GoogleStitch"` and `source.hasHtmlCss = true` in JSONC metadata

When source is screenshot-only (Gemini, Figma, manual screenshot):
- Use existing visual analysis path (unchanged)
- Set `source.hasHtmlCss = false`

### Process

1. **Analyze the design image** thoroughly:
   - Layout structure and hierarchy
   - Component identification
   - Color palette and typography
   - Responsive behavior indicators
   - Interactive elements

2. **Generate a Product Requirements Document (Brief)** covering:
   - **Overview**: What the component/page does
   - **Layout Structure**: Main sections and their relationships
   - **Components List**: Each UI element identified
   - **Responsive Behavior**: How layout adapts across breakpoints
   - **Interactivity**: Hover states, animations, user actions
   - **Data Requirements**: What data the UI displays/manages
   - **Integration Points**: APIs, state management, navigation

3. **Present brief to user** and explicitly ask:
   > "Does this brief accurately capture your design intent? Please review and let me know if any adjustments are needed before I research the best components to use."

### Output
A human-readable brief (markdown) validated by the user.

## Step 2: Research Components and Patterns

### Input
- Approved brief from Step 1
- Component list extracted from brief

### Process

Execute research in parallel using MCP tools and Explore agents:

#### 2a. Search Existing Codebase Patterns
Use **Task tool with Explore agent** to find:
```
- Existing similar components in components/
- Patterns used for comparable UI elements
- Zustand slice patterns for similar state needs
- Animation patterns already in use
```

#### 2b. Query Magic UI Components
Use **mcp__@magicuidesign/mcp** tools:
```
- mcp__@magicuidesign/mcp__getUIComponents - Browse component catalog
- mcp__@magicuidesign/mcp__getAnimations - Find animation options
- mcp__@magicuidesign/mcp__getButtons - Button variants
- mcp__@magicuidesign/mcp__getBackgrounds - Background effects
- mcp__@magicuidesign/mcp__getSpecialEffects - Visual effects
```

#### 2c. Check Shadcn Availability
Use **mcp__shadcn** to verify:
```
- Which required components are already installed
- Which need to be added via `npx shadcn@latest add`
- Component variants available
```

#### 2d. Research UI Patterns (if needed)
Use **Perplexity tools** for UI research:
```
- mcp__perplexity__perplexity_ask — quick pattern lookups
- mcp__perplexity__perplexity_reason — comparing UI framework approaches
```

#### 2e. Framework Documentation (if needed)
Use **mcp__context7** for:
```
- mcp__context7__resolve-library-id - Identify framework
- mcp__context7__get-library-docs - Get specific docs
```

### Output
Component Research Report including:
- **Existing patterns to reuse** (from codebase)
- **Recommended components** (shadcn + Magic UI)
- **Components to install** (shadcn add commands)
- **Animation recommendations** (Magic UI)
- **Pattern references** (from research)

## Step 3: Generate JSONC Specification

### Input
- Approved brief from Step 1
- Component Research Report from Step 2

### Process

1. **Transform brief into structured JSONC** following the schema in `references/jsonc-schema.md`

2. **Map components to researched options**:
   - Use existing codebase components where available
   - Select shadcn components (note any to install)
   - Add Magic UI components for animations/effects

3. **Map colors to AgenCheck design tokens**:
   ```
   primary: #1E3A8A (dark blue)
   secondary: #3B82F6 (blue)
   accent: #1E3A8A
   muted: #F8FAFC
   destructive: #EF4444
   ```

4. **Include component sources** in JSONC:
   ```jsonc
   {
     "components": [
       {
         "name": "MetricCard",
         "source": "existing", // existing | shadcn | magicui | custom
         "path": "@/components/ui/card", // for existing/shadcn
         "install": null // or "npx shadcn@latest add card"
       }
     ]
   }
   ```

5. **Include accessibility annotations** from research

### Output
Complete JSONC specification with component sourcing.

## Step 4: Implement from JSONC

### Input
- JSONC specification from Step 3
- Route/location for the new component

### Pre-Implementation
1. **Install missing components**:
   ```bash
   # From JSONC install commands
   npx shadcn@latest add [components...]
   ```

2. **Create file structure**:
   ```
   app/{route}/
   ├── page.tsx
   └── _components/
       ├── ComponentA.tsx
       └── ComponentB.tsx
   ```

### Implementation
Generate components following:
- Next.js 15 App Router conventions
- React 19 patterns
- Sourced component imports (shadcn/Magic UI/existing)
- Tailwind CSS 4 with CSS variables
- Zustand integration where needed

### Rules
- Use design tokens, never hardcoded hex values
- Include dark mode classes (`dark:`)
- Responsive classes at each breakpoint
- Split complex UI into maintainable components
- Place sample data in separate files

### Output
Production-ready React components with proper typing.

## MCP Tool Quick Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `mcp__@magicuidesign/mcp__getUIComponents` | Browse Magic UI catalog | Finding animation/effect components |
| `mcp__@magicuidesign/mcp__getAnimations` | Animation library | Adding motion to UI |
| `mcp__shadcn` | Component CLI | Check/install shadcn components |
| `mcp__perplexity__perplexity_ask` | Quick pattern lookups | UI patterns, accessibility |
| `mcp__perplexity__perplexity_reason` | Compare approaches | UI framework tradeoffs |
| `mcp__context7__get-library-docs` | Framework docs | Next.js/React/Tailwind specifics |

## Invocation Patterns

### Full Workflow
```
User: "Convert this Figma design to code" [attaches image]
→ Step 1: Generate brief, ask for approval
→ Step 2: Research components (parallel MCP + Explore)
→ Step 3: Create JSONC spec with component sources
→ Step 4: Install + implement components
```

### Resume from Brief
```
User: "Here's my approved brief, find the right components"
→ Skip to Step 2
```

### Resume from Research
```
User: "Generate the JSONC using these components"
→ Skip to Step 3
```

### Resume from JSONC
```
User: "Implement this JSONC specification"
→ Skip to Step 4
```

## Additional Resources

### Reference Files
- **`references/brief-template.md`** - Template for Step 1 brief generation
- **`references/research-workflow.md`** - Detailed research step guide
- **`references/jsonc-schema.md`** - Complete JSONC schema for Step 3
- **`references/implementation-rules.md`** - Detailed implementation guidelines

### Examples
- **`examples/voice-dashboard.jsonc`** - Complete voice agent dashboard example

## Critical Checkpoints

1. **After Step 1**: ALWAYS pause and ask user to validate the brief
2. **After Step 2**: Present component recommendations for complex UIs
3. **After Step 3**: Optionally present JSONC for review
4. **After Step 4**: Run type-check and build validation

## Error Handling

If component research finds conflicts:
- Prefer existing codebase patterns over new components
- Check shadcn component compatibility with React 19
- Verify Magic UI components work with Tailwind 4

If implementation hits blockers:
- Fallback to simpler shadcn components
- Check existing patterns in `components/ui/`
- Suggest design adjustments if needed

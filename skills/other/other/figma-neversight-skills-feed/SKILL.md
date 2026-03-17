---
name: figma
description: |
  Implement UI directly from Figma designs using the Figma MCP with pixel-perfect fidelity.
  Use when given a Figma URL, asked to "implement from Figma", "match the design",
  or when building UI that needs to precisely match design specs.
license: MIT
argument-hint: <figma-url-or-description>
metadata:
  author: howells
website:
  order: 9
  desc: Figma → code
  summary: Implement UI from Figma designs. Requires the Figma MCP server—install via `npx @anthropic/create-mcp@latest`.
  what: |
    Figma reads your design file via the Figma MCP server, extracts layout structure, colors, typography, and spacing, then generates React components. It's not magic—expect some nudging to get things right—but it beats eyeballing a screenshot. Install the MCP with `npx @anthropic/create-mcp@latest` and select Figma.
  why: |
    Design-to-code handoff usually means eyeballing a mockup and guessing at spacing. Figma reads the actual design file, so you're working from real values. It's not perfect, but it gets you 80% there and you can refine from a working baseline.
  decisions:
    - Requires Figma MCP. Run `npx @anthropic/create-mcp@latest` and select Figma to install.
    - Works best with clean Figma files. Auto-layout and named layers help.
    - Expect iteration. It gets you close, then you refine.
  agents:
    - figma-implement
---

# Figma Implementation Workflow

Implement UI components directly from Figma designs using the Figma MCP.

<required_reading>
**Load interface rules for UI implementation:**
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/design.md — Visual principles
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/colors.md — Color methodology
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/spacing.md — Spacing system
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/typography.md — Typography rules
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/layout.md — Layout patterns
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/animation.md — If implementing motion
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/forms.md — If implementing forms
- ${CLAUDE_PLUGIN_ROOT}/rules/interface/interactions.md — Touch, keyboard, hover
- ${CLAUDE_PLUGIN_ROOT}/references/frontend-design.md — Fonts and anti-patterns
- ${CLAUDE_PLUGIN_ROOT}/references/component-design.md — React component patterns
</required_reading>

## Prerequisites — CHECK FIRST

**Before doing anything else, verify Figma MCP is available:**

1. **Check MCP Server Installation**
   - Look for `mcp__figma__*` tools in your available tools
   - If no Figma MCP tools exist, **STOP** and notify the user:
     > "The Figma MCP server is not installed. To use /arc:figma, you need to install the Figma MCP server. See: https://github.com/figma/figma-mcp"

2. **Check Authentication**
   - Attempt a simple Figma MCP call (e.g., `mcp__figma__get_design_context` with the provided file)
   - If you receive an authentication error, **STOP** and notify the user:
     > "The Figma MCP server needs authentication. Please configure your Figma access token in the MCP server settings."

3. **Do NOT proceed** if either check fails
   - Do not attempt to implement designs without Figma access
   - Do not guess at design specs
   - Simply halt and inform the user what's needed

## Process

**Only proceed with the following if Figma MCP is available and authenticated.**

Follow the instructions in `${CLAUDE_PLUGIN_ROOT}/agents/design/figma-implement.md`:

1. **Extract Design Intent** — Use Figma MCP to get specs (colors, typography, spacing, shadows, component hierarchy)

2. **Understand Codebase Context** — Find existing design system, component patterns, styling methodology

3. **Implement with Fidelity** — Write code using existing tokens, get padding/spacing right (most commonly missed)

4. **Review and Compare** — Screenshot the result, compare against Figma, fix discrepancies, iterate until matching

## Required Input

- Figma URL (file or specific node)
- OR description of what to find in an already-shared Figma file

## Usage

```
/arc:figma https://figma.com/design/xxx/yyy?node-id=123-456
```

Or if Figma file already shared:
```
/arc:figma "the header component"
```

## Figma MCP Commands

**Get design context:**
```
mcp__figma__get_design_context: fileKey, nodeId
```

**Get screenshot for comparison:**
```
mcp__figma__get_screenshot: fileKey, nodeId
```

**Extract specific values:**
- Colors, gradients
- Typography (font, size, weight, line-height)
- Spacing (padding, margins, gaps)
- Shadows, borders, radii
- Component structure

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check for related prior UI/design work.
</progress_context>

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:figma — [Component/screen] implemented from Figma`
</arc_log>

<success_criteria>
Figma implementation is complete when:
- [ ] Design specs extracted via Figma MCP (colors, typography, spacing, shadows)
- [ ] Component implemented using existing design system tokens
- [ ] Screenshots compared against Figma design
- [ ] Responsive states handled (mobile, tablet, desktop)
- [ ] Discrepancies identified and fixed
- [ ] Progress journal updated
</success_criteria>

## Interop

- Use **/arc:design** if you need to create a design from scratch (no Figma reference)
- Use **/arc:implement** for planned multi-step implementations

---
name: ui-handler
description: Implement UI using Shadcn MCP (atoms/theme) and 21st.dev MCP (complex sections). Use when adding buttons, layouts, or generating landing pages.
tools: Read, Write, Edit, mcp_shadcn, mcp_21st_dev
model: inherit
---

# UI Handler

## Instructions

### 1. Installing Standard Components (Atoms)
Use the **Shadcn MCP** for foundational UI elements (buttons, inputs, dialogs).
1.  **Action**: Ask the Shadcn MCP to add the component.
    > "Add the button and dialog components using Shadcn MCP."
2.  **Manual Fallback**: `pnpm dlx shadcn@latest add {component}`

### 2. Generating Complex Sections (Blocks)
Use the **21st.dev Magic MCP** for high-level sections (Landing pages, Heros, Dashboards).
1.  **Action**: Prompt the 21st.dev MCP with a description.
    > "Generate a modern SaaS hero section with a dark gradient background and email capture form."
2.  **Location**: Place generated files in `src/components/sections/` or `src/components/website/`.
3.  **Integration**: Import and use in your `page.tsx`.

### 3. Theming & Styling
Use **Shadcn MCP** or edit `src/app/globals.css` directly.
-   **Theme Updates**: Ask Shadcn MCP to apply a specific theme or color palette.
    > "Update the app theme to use a 'zinc' neutral base with 'blue' primary color."
-   **CSS Variables**: We use CSS variables (often OKLCH) in `src/app/globals.css`. Ensure any new styles use these variables (e.g., `bg-background`, `text-primary`).

### 4. Creating Layouts
1.  **Identify**: Header, Sidebar, Content Area.
2.  **Compose**: Use atoms from `@/components/ui` and sections from `@/components/sections`.
3.  **Co-location**: If a component is unique to a page, put it in `_components/` next to the page.

## Reference
For detailed architecture and best practices, see [reference.md](reference.md).

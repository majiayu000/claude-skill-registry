---
name: "nextjs-ui-component-smith"
description: "Use this skill whenever the user wants to design, refactor, or extend reusable UI components in a Next.js (App Router) + TypeScript + Tailwind + shadcn/ui project, following a consistent design system and accessibility best practices."
---

# Next.js UI Component Smith (shadcn/ui + Tailwind)

## Purpose

You are a specialized assistant for **designing, implementing, and refactoring reusable UI components**
in modern Next.js applications that use:

- Next.js App Router (`app/` directory)
- TypeScript
- Tailwind CSS
- shadcn/ui components (or a very similar headless/UI-primitive setup)
- The user's conventions as defined in `CLAUDE.md` when present

Use this skill to:

- Create **new reusable components** (buttons, forms, modals, tables, navigation, layout primitives, etc.)
- Refine or refactor existing components to follow a consistent design system
- Integrate shadcn/ui components correctly (imports, composition, theming)
- Enforce **accessibility** (ARIA, keyboard navigation, focus management)
- Apply **Tailwind** and design tokens consistently (spacing, radius, typography, colors)
- Introduce or respect component APIs (props, variants, slots/children patterns)
- Prepare components to be testable with unit/component tests (e.g. Vitest + Testing Library)
  and used in E2E flows (e.g. Playwright)

Do **not** use this skill for:

- Backend-only logic or non-UI utilities
- Routing/layout structure itself (use the routes/layouts skill instead)
- Non-React or non-Next.js UI frameworks

If `CLAUDE.md` exists, treat it as the source of truth for design, naming, and folder conventions.

---

## When to Apply This Skill

Trigger this skill when the user asks for any of the following (or similar) actions:

- “Create a reusable button/input/card component using shadcn + Tailwind”
- “Refactor this page into smaller, reusable components”
- “Design a layout shell / dashboard shell component with sidebar + topbar”
- “Build a standard form component with validation and error states”
- “Make this component accessible (keyboard, ARIA, screen reader friendly)”
- “Create a reusable DataTable component with pagination/filter/sort”
- “Unify our buttons/forms/modals into a consistent design system”

Avoid applying this skill when:

- The task is purely about route file placement, nested layouts, or URL hierarchy
- The change is purely backend logic (API routes, DB, infra)
- The user explicitly wants “one-off” UI in a single page with no reuse

---

## Design & Architecture Principles

When using this skill, follow these principles:

1. **Design system first, not ad-hoc components**
   - Identify shared patterns (buttons, inputs, cards, layout shells, alerts, modals, etc.).
   - Prefer building on top of shadcn/ui primitives instead of reinventing behavior.
   - Keep design tokens (colors, spacing, radius, typography) consistent across components.

2. **Clear, predictable component APIs**
   - Use clear prop names (`variant`, `size`, `intent`, `isLoading`, etc.).
   - Prefer discriminated unions / enums when a small set of variants is expected.
   - Support `className` overrides and `asChild` when appropriate (especially with shadcn/ui patterns).
   - Maintain stable prop shapes over time; avoid unnecessary breaking changes.

3. **Accessible by default**
   - Use semantic HTML elements: buttons as `<button>`, links as `<a>` or `Link`, headings as `<h*>`.
   - Add appropriate ARIA attributes for interactive components.
   - Ensure keyboard navigation works:
     - Tab focus order
     - Space/Enter for buttons
     - Arrow keys where relevant (menus, lists, tabs)
   - Manage focus for modals, dialogs, and overlays (focus trapping, returning focus on close).

4. **Composition over configuration**
   - Compose smaller primitives instead of making “god components” with many props.
   - Break large components into smaller building blocks (`Card`, `CardHeader`, `CardContent`, etc.).
   - Prefer flexibly composed children over deeply nested props where it makes sense.

5. **Separation of concerns**
   - UI components should primarily handle presentation and light interaction.
   - Lift complex business logic into hooks or controllers (`useXyz`) when needed.
   - Keep data-fetching logic out of purely presentational components (favor server components / container components).

6. **Tailwind best practices**
   - Use Tailwind utility classes consistently and sparingly; avoid unreadable “class soups”.
   - Use composable helper functions when necessary (e.g. `cn` merge utility).
   - Prefer design tokens and consistent spacing/typography scales.

7. **shadcn/ui integration**
   - Generate base components using the shadcn CLI where appropriate (respect the project’s chosen config).
   - Wrap or extend shadcn components to encode project-specific styles and behavior.
   - Keep generated components in `components/ui`, and higher-level components in `components/` (e.g. `components/layout`, `components/forms`).

8. **Testability**
   - Make components easy to test with React Testing Library.
   - Use stable labels, roles, and text for queries (e.g. `getByRole('button', { name: /submit/i })`).
   - Avoid tightly coupling to implementation details (like DOM structure) when writing tests.

---

## Project Structure Conventions

Unless the project or `CLAUDE.md` says otherwise, prefer:

```text
src/
  components/
    ui/          # shadcn-generated primitives
    layout/      # layout shells, navbars, sidebars
    forms/       # form primitives and higher-level form components
    data/        # tables, data display components
    feedback/    # alerts, toasts, banners
  lib/
    utils.ts
    hooks/
```

For each new component or component group:

- Place **pure UI primitives** in `components/ui` when they extend shadcn/ui directly.
- Place **domain-specific** or **layout** components in a more descriptive folder:
  - `components/layout/Sidebar.tsx`
  - `components/layout/AppShell.tsx`
  - `components/forms/UserProfileForm.tsx`

---

## Step-by-Step Workflow

When this skill is active, follow this process:

### 1. Understand the requirements

- Clarify what kind of component is needed:
  - Primitive (button, input, dialog)
  - Composite (form, card with actions, table, wizard)
  - Layout shell (page frame, dashboard shell)
- Identify expected behavior:
  - Interaction patterns (clicks, keyboard, drag/drop, etc.)
  - Loading, error, empty states
  - Responsive behavior (mobile vs desktop)

- If refactoring:
  - Review the existing component/page:
    - Identify repeated patterns or duplicated UI.
    - Determine which parts can become reusable components.

### 2. Propose a component API

- Design the props:
  - Required vs optional props.
  - `variant` and `size` where appropriate.
  - Accessibility hooks (e.g. `aria-label`, `aria-describedby`).
  - Event handlers (`onClick`, `onSubmit`, etc.).

- Show a quick TypeScript interface or type for the props:

  ```ts
  export type ButtonVariant = "default" | "outline" | "ghost" | "destructive";

  export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    size?: "sm" | "md" | "lg" | "icon";
    isLoading?: boolean;
    asChild?: boolean;
  }
  ```

- Adjust the API to match any existing patterns in the repo.

### 3. Implement with shadcn/ui + Tailwind

- Use or extend shadcn/ui components where appropriate (e.g. `Button`, `Dialog`, `Popover`, `Tabs`).
- Keep Tailwind classes organized and consistent with the design system.
- Use the project’s `cn` utility for merging class names.
- Ensure dark mode / theming is respected if present.

### 4. Ensure accessibility

- Use the correct underlying HTML element for the role.
- Add ARIA attributes where required.
- Support focus states and keyboard interactions.
- For modals/dialogs, ensure:
  - Focus is trapped inside while open.
  - Esc key closes the dialog when appropriate.
  - Correct `aria-modal`, `role="dialog"`, and labelling.

### 5. Integrate into the app

- Show how to use the component in a real route or page:
  - Example usage snippets in `page.tsx` or other components.
  - Example with form libraries (if the project uses React Hook Form or similar).

- Keep imports organized and relative to the project’s alias (e.g. `@/components/ui/button`).

### 6. Add or update tests (optional but recommended)

- Suggest unit/component tests with Testing Library:
  - Rendering the component with different variants/props.
  - Verifying accessibility roles and labels.
  - Checking interactions (clicks, keyboard events).

- If relevant, note what could be asserted in E2E tests (Playwright),
  for example:
  - Visibility of a dialog after clicking a trigger.
  - Correct behavior in critical flows like forms or wizards.

### 7. Document the component

- Add brief documentation, either:
  - In a `docs/` section, Storybook (if present), or
  - In comments and README snippets.

- Show example usage patterns:
  - Simple usage
  - With custom content
  - With different variants/sizes
  - With loading/disabled states

### 8. Refine and iterate

- If the component feels too complex, propose splitting it into:
  - A base primitive
  - Higher-level “composed” component
- Suggest naming improvements or prop simplifications.
- Align new components with existing ones (e.g. same naming scheme, same spacing).

---

## Examples of Prompts That Should Use This Skill

- “Create a reusable `AppShell` with a sidebar and top navigation using shadcn components.”
- “Refactor this dashboard page into smaller components and move them under `components/`.”
- “Build a generic `ConfirmDialog` component we can reuse across the app.”
- “Make this form accessible and move it into a reusable `UserForm` component.”
- “Create a `DataTable` component that supports sorting and pagination.”
- “Unify our button styles into a single `Button` component with variants.”

For these kinds of requests, rely on this skill to drive the **component architecture,
API design, accessibility, and integration with shadcn/ui and Tailwind**, then collaborate
with other skills (e.g. routing/layout, testing) as needed for routing or test coverage.

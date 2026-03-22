---
name: new-component
description: Creates a new Astro component with typed props, Tailwind styling, and dark mode support following project conventions. Use when building a new UI component.
argument-hint: "<ComponentName>"
disable-model-invocation: true
---

Create a new Astro component in the `src/components/` directory.

## Steps

1. Take the component name from the user's argument. If not provided, ask for one.
2. Ensure the name is PascalCase (e.g., `FeatureCard`, `PricingTable`). Convert if needed.
3. Ask the user what the component should do and what props it needs.
4. Create `src/components/<ComponentName>.astro`:

```astro
---
interface Props {
  // Add typed props based on user requirements
  title: string;
  variant?: "default" | "highlighted";
}
const { title, variant = "default" } = Astro.props;
---

<div class:list={[
  "rounded-2xl p-6 shadow-sm ring-1",
  variant === "highlighted"
    ? "bg-gray-900 text-white ring-gray-700 dark:bg-gray-100 dark:text-gray-900 dark:ring-gray-300"
    : "bg-white ring-gray-200 dark:bg-gray-900 dark:ring-gray-800",
]}>
  <h3 class="text-lg font-semibold">{title}</h3>
  <slot />
</div>
```

5. Follow these project conventions:
   - Use `interface Props` for type safety
   - Destructure props with defaults in the frontmatter
   - Use Tailwind utility classes — no custom CSS
   - Always include `dark:` variants for colors and backgrounds
   - Use the standard card pattern: `rounded-2xl bg-white shadow-sm ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800`
   - Use `<slot />` for child content where appropriate
   - Use `class:list` for conditional classes

6. Tell the user:
   - The component was created at `src/components/<ComponentName>.astro`
   - How to import and use it: `import ComponentName from "../components/ComponentName.astro";`

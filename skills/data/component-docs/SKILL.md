---
name: component-docs
description: Generate or update component documentation with usage examples, props tables, and Storybook stories. Use when documenting new components, creating usage examples, or setting up Storybook stories.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Component Documentation Skill

Documentation lives in `packages/ui/`.

## Component Documentation Template

```markdown
# Button

A customizable button component built with Radix UI primitives.

## Usage

\`\`\`tsx
import { Button } from "@sgcarstrends/ui";

<Button variant="default">Click me</Button>
\`\`\`

## Variants

\`\`\`tsx
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
\`\`\`

## Sizes

\`\`\`tsx
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | `"default" \| "destructive" \| "outline"` | `"default"` | Visual style |
| size | `"default" \| "sm" \| "lg" \| "icon"` | `"default"` | Button size |
| asChild | `boolean` | `false` | Render as child element |

## Accessibility

- Uses semantic `<button>` element
- Supports keyboard navigation (Enter, Space)
- Proper focus states
```

## JSDoc Comments

```typescript
/**
 * A customizable button component.
 *
 * @example
 * <Button variant="default">Click me</Button>
 */
export interface ButtonProps {
  /** Visual style variant @default "default" */
  variant?: "default" | "destructive" | "outline";
  /** Button size @default "default" */
  size?: "default" | "sm" | "lg" | "icon";
}
```

## Storybook Stories

```typescript
// packages/ui/src/components/button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

const meta = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["default", "destructive", "outline"] },
    size: { control: "select", options: ["default", "sm", "lg", "icon"] },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = { args: { children: "Button" } };
export const Destructive: Story = { args: { variant: "destructive", children: "Delete" } };
```

## Documentation Checklist

- [ ] JSDoc comments on component and props
- [ ] Markdown documentation with usage examples
- [ ] Props table included
- [ ] Variants documented
- [ ] Accessibility notes
- [ ] Storybook stories (if using Storybook)
- [ ] Exported from package index

## Best Practices

1. **Clear Examples**: Provide complete, working code
2. **Props Documentation**: Document every prop with type and description
3. **Accessibility**: Include a11y notes
4. **Keep Updated**: Update docs when components change

## References

- `packages/ui/CLAUDE.md` for package details
- shadcn/ui: https://ui.shadcn.com

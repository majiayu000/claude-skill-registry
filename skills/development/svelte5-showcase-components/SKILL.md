---
name: svelte5-showcase-components
description: |
  Provides Comprehensive guide to the Svelte 5 Showcase component library with 49 production-ready
  components organized into 7 categories. Use when you need to discover available components,
  understand component usage patterns, integrate components into new projects, or reference
  best practices for Svelte 5 development. Triggers on "what components are available",
  "how to use [component name]", "integrate showcase components", "copy component from showcase",
  "Svelte 5 component examples", or "showcase component library". Works with shadcn-svelte,
  Bits UI, TailwindCSS v4, sveltekit-superforms, and Svelte 5 runes.

---

# Svelte 5 Showcase Components

## Quick Start

The Svelte 5 Showcase is a production-ready component library with **49 components** organized into **7 categories**, built with Svelte 5 runes, TypeScript strict mode, and TailwindCSS v4.

**Showcase Location:** `/Users/dawiddutoit/projects/play/svelte`

**Component Categories:**
1. **Primitives** (24) - Core UI primitives (buttons, inputs, forms, dialogs)
2. **Navigation** (6) - Navigation patterns (tabs, breadcrumbs, pagination, menus)
3. **Data Display** (6) - Display components (tables, accordions, avatars, carousels)
4. **Overlays** (5) - Modal dialogs and overlays (popovers, sheets, drawers)
5. **Feedback** (2) - User feedback (progress bars, toast notifications)
6. **Layout** (2) - Layout primitives (aspect ratio, resizable panels)
7. **Custom** (4) - Brand-specific components (hero sections, service cards)

**Quick Component Lookup:**

```bash
# Browse all components at:
/Users/dawiddutoit/projects/play/svelte/src/lib/components/ui/

# Example showcase pages:
/Users/dawiddutoit/projects/play/svelte/src/routes/showcase/primitives/button/+page.svelte
/Users/dawiddutoit/projects/play/svelte/src/routes/showcase/primitives/form/+page.svelte
```

---

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [Component Inventory](#2-component-inventory)
3. [Quick Integration](#3-quick-integration)
4. [Common Usage Patterns](#4-common-usage-patterns)
5. [Form Handling](#5-form-handling)
6. [Supporting Files](#6-supporting-files)
7. [Expected Outcomes](#7-expected-outcomes)
8. [Requirements](#8-requirements)
9. [Red Flags to Avoid](#9-red-flags-to-avoid)

---

## When to Use This Skill

### Explicit Triggers

Invoke this skill when the user explicitly asks for:
- "What components are available in the showcase?"
- "How do I use the [component name] component?"
- "Show me examples of [component type]"
- "How to integrate showcase components into my project?"
- "Copy [component] from showcase to my project"
- "What's the difference between Dialog and Drawer?"
- "Showcase component documentation"

### Implicit Triggers

Invoke when the user's task involves:
- Building UI with Svelte 5 and needs component references
- Looking for form validation examples with sveltekit-superforms
- Needing accessible component patterns
- Asking about Svelte 5 runes usage in components
- Requesting Tailwind CSS component styling patterns
- Exploring shadcn-svelte implementation examples

### Debugging Triggers

Invoke when troubleshooting:
- Import errors with showcase components
- Svelte 5 runes syntax issues in components
- Form validation not working with superforms
- Tailwind classes not applying to components
- TypeScript errors in component props
- Component styling inconsistencies

---

## Component Inventory

### Complete Component List (49 Total)

#### Primitives (24 components)

**Form Controls:**
- `Button` - Clickable button with variants (default, destructive, outline, ghost, link)
- `Input` - Text input field with type variants
- `Textarea` - Multi-line text input
- `Checkbox` - Boolean checkbox with label
- `Switch` - Toggle switch component
- `Radio Group` - Radio button group
- `Select` - Dropdown selection menu
- `Slider` - Range slider input
- `Label` - Accessible form label
- `Input OTP` - One-time password input

**Form Components:**
- `Form Field` - Form field wrapper with context
- `Form Label` - Accessible form label
- `Form Description` - Helper text for fields
- `Form Field Errors` - Validation error display
- `Form Fieldset` - Group related fields
- `Form Button` - Form submit button

**Feedback & Display:**
- `Alert` - Alert messages with variants
- `Alert Dialog` - Modal confirmation dialog
- `Badge` - Status badge with variants
- `Card` - Container card with header/footer
- `Dialog` - Modal dialog overlay
- `Skeleton` - Loading skeleton placeholder
- `Tooltip` - Hover tooltip
- `Toggle` - Toggle button
- `Toggle Group` - Toggle button group

**Date Inputs:**
- `Calendar` - Date picker calendar
- `Range Calendar` - Date range picker

#### Navigation (6 components)

- `Breadcrumb` - Breadcrumb navigation trail
- `Command` - Command palette / search
- `Menubar` - Menu bar navigation
- `Navigation Menu` - Dropdown navigation menu
- `Pagination` - Page navigation
- `Tabs` - Tabbed interface

#### Data Display (6 components)

- `Accordion` - Collapsible content sections
- `Avatar` - User avatar with fallback
- `Carousel` - Image/content carousel (Embla)
- `Collapsible` - Single collapsible section
- `Scroll Area` - Custom scrollbar area
- `Table` - Data table with header/footer

#### Overlays (5 components)

- `Context Menu` - Right-click context menu
- `Drawer` - Bottom drawer overlay (Vaul)
- `Hover Card` - Hover card overlay
- `Popover` - Popover overlay
- `Sheet` - Side sheet overlay

#### Feedback (2 components)

- `Progress` - Progress bar indicator
- `Sonner` - Toast notification system

#### Layout (2 components)

- `Aspect Ratio` - Aspect ratio container
- `Resizable` - Resizable panel layout (Paneforge)

#### Custom Components (4 components)

- `Feature Card` - Branded feature card
- `Hero Section` - Landing page hero
- `Loading Spinner` - Custom loading animation
- `Service Card` - Expandable service card with credentials

**Location:** `/Users/dawiddutoit/projects/play/svelte/src/lib/components/ui/`

---

## Quick Integration

### Method 1: Using shadcn-svelte CLI (Recommended)

```bash
# Install CLI and add components
npx shadcn-svelte@latest add button
npx shadcn-svelte@latest add card
npx shadcn-svelte@latest add form
```

**What this does:**
1. Installs required dependencies
2. Copies component files to `src/lib/components/ui/`
3. Updates barrel exports in `index.ts`

### Method 2: Manual Copy from Showcase

**Step 1: Copy component directory**

```bash
# Copy button component
cp -r /Users/dawiddutoit/projects/play/svelte/src/lib/components/ui/button \
  ./src/lib/components/ui/

# Copy multiple components
cp -r /Users/dawiddutoit/projects/play/svelte/src/lib/components/ui/{button,card,input} \
  ./src/lib/components/ui/
```

**Step 2: Update barrel exports**

```typescript
// src/lib/components/index.ts
export { Button, buttonVariants } from './ui/button';
export { Card, CardHeader, CardTitle, CardContent, CardFooter } from './ui/card';
export { Input } from './ui/input';
```

**Step 3: Install dependencies**

```bash
npm install bits-ui clsx tailwind-merge tailwind-variants lucide-svelte
```

**Step 4: Copy utilities**

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & { ref?: U | null };
```

### Method 3: Read from Showcase

```svelte
<script lang="ts">
  // Read showcase implementation for reference
  // Location: /Users/dawiddutoit/projects/play/svelte/src/lib/components/ui/[component]/
</script>
```

**View showcase examples:**
```
/Users/dawiddutoit/projects/play/svelte/src/routes/showcase/primitives/[component]/+page.svelte
```

---

## Common Usage Patterns

### Svelte 5 Runes (Required Syntax)

All components use Svelte 5 runes:

```svelte
<script lang="ts">
  // ✅ Svelte 5 (REQUIRED)
  let count = $state(0);
  let doubled = $derived(count * 2);

  $effect(() => {
    console.log('count changed:', count);
  });

  // ❌ Svelte 4 (DO NOT USE)
  // let count = 0;
  // $: doubled = count * 2;
  // $: console.log(count);
</script>
```

### Props Pattern

```svelte
<script lang="ts">
  interface Props {
    title: string;
    count?: number;
    variant?: 'default' | 'destructive';
    onUpdate?: (value: number) => void;
  }

  let { title, count = 0, variant = 'default', onUpdate }: Props = $props();
</script>
```

### Bindable Props

```svelte
<script lang="ts">
  // Component with bindable value
  interface Props {
    value: string;
    onChange?: (value: string) => void;
  }

  let { value = $bindable(), onChange }: Props = $props();
</script>

<input bind:value oninput={() => onChange?.(value)} />

<!-- Parent usage -->
<script lang="ts">
  let searchQuery = $state('');
</script>

<MyComponent bind:value={searchQuery} />
```

### Component Composition

```svelte
<script lang="ts">
  import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '$lib/components';
  import { Button } from '$lib/components';
</script>

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Card content goes here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Tailwind Class Merging

```svelte
<script lang="ts">
  import { cn } from '$lib/utils';

  interface Props {
    class?: string;
  }

  let { class: className }: Props = $props();
</script>

<div class={cn('default-bg-white p-4 rounded', className)}>
  Content
</div>
```

### Icon Integration

```svelte
<script lang="ts">
  import { Button } from '$lib/components';
  import { Mail, Loader2 } from 'lucide-svelte';
</script>

<Button>
  <Mail class="mr-2 h-4 w-4" />
  Login with Email
</Button>

<Button disabled>
  <Loader2 class="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>
```

---

## Form Handling

### Complete Form Integration

**1. Create Zod Schema:**

```typescript
// schema.ts
import { z } from 'zod';

export const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
  newsletter: z.boolean().default(false)
});

export type ContactForm = z.infer<typeof contactSchema>;
```

**2. Server-Side Validation:**

```typescript
// +page.server.ts
import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { contactSchema } from './schema';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
  const form = await superValidate(zod(contactSchema));
  return { form };
};

export const actions: Actions = {
  default: async ({ request }) => {
    const form = await superValidate(request, zod(contactSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    // Process form data
    console.log('Form submitted:', form.data);

    return { form };
  }
};
```

**3. Client-Side Component:**

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';
  import { zodClient } from 'sveltekit-superforms/adapters';
  import {
    FormField,
    FormLabel,
    FormDescription,
    FormFieldErrors,
    Input,
    Textarea,
    Checkbox,
    Button
  } from '$lib/components';
  import { contactSchema } from './schema';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  const { form, errors, enhance, delayed } = superForm(data.form, {
    validators: zodClient(contactSchema)
  });
</script>

<form method="POST" use:enhance class="space-y-6 max-w-2xl">
  <FormField name="name" {form}>
    {#snippet children({ value })}
      <FormLabel>Full Name</FormLabel>
      <Input bind:value={$form.name} placeholder="John Doe" />
      <FormFieldErrors />
    {/snippet}
  </FormField>

  <FormField name="email" {form}>
    {#snippet children({ value })}
      <FormLabel>Email</FormLabel>
      <FormDescription>We'll never share your email</FormDescription>
      <Input type="email" bind:value={$form.email} placeholder="you@example.com" />
      <FormFieldErrors />
    {/snippet}
  </FormField>

  <FormField name="message" {form}>
    {#snippet children({ value })}
      <FormLabel>Message</FormLabel>
      <Textarea bind:value={$form.message} rows={5} placeholder="Your message..." />
      <FormFieldErrors />
    {/snippet}
  </FormField>

  <FormField name="newsletter" {form}>
    {#snippet children({ value })}
      <div class="flex items-center space-x-2">
        <Checkbox id="newsletter" bind:checked={$form.newsletter} />
        <FormLabel for="newsletter">Subscribe to newsletter</FormLabel>
      </div>
      <FormFieldErrors />
    {/snippet}
  </FormField>

  <Button type="submit" disabled={$delayed}>
    {$delayed ? 'Submitting...' : 'Send Message'}
  </Button>
</form>
```

**Example Location:** `/Users/dawiddutoit/projects/play/svelte/src/routes/showcase/primitives/form/+page.svelte`

---

## Supporting Files

### examples/component-examples.md

Comprehensive usage examples for all 49 components organized by category:

- **Primitives** - All 24 primitive components with props and usage
- **Navigation** - 6 navigation components with real-world examples
- **Data Display** - 6 display components with data binding patterns
- **Overlays** - 5 overlay components with trigger/content patterns
- **Feedback** - 2 feedback components with state management
- **Layout** - 2 layout components with responsive patterns
- **Custom** - 4 custom components with brand-specific examples

**Use when:** You need copy-paste-ready code examples for specific components.

### references/integration-guide.md

Complete integration guide covering:

1. **Quick Setup** - Install dependencies, configure Vite, create utilities
2. **Component Architecture** - shadcn-svelte philosophy, structure patterns
3. **Required Dependencies** - Complete dependency table with versions
4. **Configuration Files** - TypeScript config, path aliases, Vite setup
5. **Copy/Paste Integration** - Three methods for integrating components
6. **Common Patterns** - Svelte 5 runes, props, bindable values, composition
7. **Form Integration** - Complete form example with Zod + superforms
8. **Styling Customization** - Variant customization, CSS variables, dark mode
9. **Troubleshooting** - Common issues and solutions

**Use when:** You're setting up a new project or debugging integration issues.

---

## Expected Outcomes

### Successful Component Discovery

```
✅ Component Found

Component: Button
Category: Primitives
Location: /Users/dawiddutoit/projects/play/svelte/src/lib/components/ui/button/

Variants: default, destructive, outline, secondary, ghost, link
Sizes: sm, default, lg, icon, icon-sm, icon-lg

Dependencies:
- tailwind-variants (variants)
- lucide-svelte (icons, optional)

Example Location:
/Users/dawiddutoit/projects/play/svelte/src/routes/showcase/primitives/button/+page.svelte

Integration Command:
npx shadcn-svelte@latest add button
```

### Successful Component Integration

```
✅ Component Integrated Successfully

Component: Button
Copied to: ./src/lib/components/ui/button/
Barrel export: Updated index.ts

Dependencies installed:
✓ tailwind-variants@^3.2.2
✓ clsx@^2.1.1
✓ tailwind-merge@^3.4.0

Next steps:
1. Import: import { Button } from '$lib/components';
2. Use: <Button>Click me</Button>
3. Customize variants as needed in button.svelte

Component ready to use!
```

### Integration Failure

```
❌ Integration Failed

Component: Button
Error: Missing required dependencies

Missing packages:
- tailwind-variants
- clsx
- tailwind-merge

Fix:
npm install tailwind-variants clsx tailwind-merge

Also check:
1. Vite config has Tailwind plugin BEFORE SvelteKit
2. utils.ts exists with cn() function
3. TypeScript strict mode is enabled

Retry integration after installing dependencies.
```

---

## Requirements

### Environment

- **Node.js:** v18+ or v20+
- **Package Manager:** npm, pnpm, or yarn
- **TypeScript:** v5.x with strict mode
- **Svelte:** v5.2.0+
- **SvelteKit:** v2.9.0+

### Core Dependencies

**Framework:**
- `svelte@^5.2.0` - Svelte 5 with runes
- `@sveltejs/kit@^2.9.0` - SvelteKit framework
- `typescript@^5.7.2` - Type safety

**UI Primitives:**
- `bits-ui@^2.14.4` - Headless components
- `lucide-svelte@^0.562.0` - Icons

**Styling:**
- `@tailwindcss/vite@^4.0.0-beta.3` - Tailwind CSS v4
- `tailwindcss@^4.0.0-beta.3`
- `clsx@^2.1.1` - Class utility
- `tailwind-merge@^3.4.0` - Class merging
- `tailwind-variants@^3.2.2` - Variants

**Forms:**
- `sveltekit-superforms@^2.29.1` - Form handling
- `formsnap@^2.0.1` - Form primitives
- `zod@^3.24.1` - Validation

### Configuration Files Required

1. **vite.config.ts** - Tailwind plugin before SvelteKit
2. **src/lib/utils.ts** - cn() utility function
3. **src/routes/+layout.svelte** - Import Tailwind CSS
4. **tsconfig.json** - Strict mode enabled

### Knowledge Required

- Svelte 5 runes syntax ($state, $derived, $effect, $props)
- TypeScript interfaces and type inference
- Tailwind CSS utility classes
- Component composition patterns
- Form validation with Zod schemas

---

## Red Flags to Avoid

**❌ Using Svelte 4 Syntax**

Never use Svelte 4 reactive declarations in Svelte 5 projects:

```svelte
<!-- ❌ WRONG -->
<script>
  let count = 0;
  $: doubled = count * 2;
</script>

<!-- ✅ CORRECT -->
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
</script>
```

**❌ Wrong Vite Plugin Order**

Tailwind MUST come before SvelteKit:

```typescript
// ❌ WRONG
plugins: [sveltekit(), tailwindcss()]

// ✅ CORRECT
plugins: [tailwindcss(), sveltekit()]
```

**❌ Disabling TypeScript Strict Mode**

Components rely on strict type checking:

```json
// ❌ WRONG
{ "strict": false }

// ✅ CORRECT
{ "strict": true }
```

**❌ Using `any` Type**

Never use `any` without justification:

```typescript
// ❌ WRONG
let data: any = {};

// ✅ CORRECT
interface Data {
  name: string;
  count: number;
}
let data: Data = { name: 'test', count: 0 };
```

**❌ Missing Form Adapters**

Always use correct adapter for client/server:

```typescript
// ❌ WRONG (server-side)
import { zodClient } from 'sveltekit-superforms/adapters';
await superValidate(request, zodClient(schema));

// ✅ CORRECT (server-side)
import { zod } from 'sveltekit-superforms/adapters';
await superValidate(request, zod(schema));

// ✅ CORRECT (client-side)
import { zodClient } from 'sveltekit-superforms/adapters';
superForm(data.form, { validators: zodClient(schema) });
```

**❌ Installing Components via NPM**

Components are copy/paste, not NPM packages:

```bash
# ❌ WRONG
npm install @shadcn-svelte/button

# ✅ CORRECT
npx shadcn-svelte@latest add button
```

**❌ Using Inline Styles**

Use Tailwind classes instead:

```svelte
<!-- ❌ WRONG -->
<div style="background-color: #4f46e5; padding: 1rem;">Content</div>

<!-- ✅ CORRECT -->
<div class="bg-indigo-600 p-4">Content</div>
```

**❌ Skipping Component Examples**

Always check showcase examples before implementing:

```
✅ CORRECT Workflow:
1. Check /Users/dawiddutoit/projects/play/svelte/src/routes/showcase/[category]/[component]/+page.svelte
2. Read component implementation
3. Copy relevant patterns
4. Customize for your use case
```

**❌ Mixing Component Libraries**

Don't mix shadcn-svelte with other UI libraries:

```svelte
<!-- ❌ WRONG -->
<script>
  import { Button as ShadcnButton } from '$lib/components';
  import { Button as MaterialButton } from '@material/svelte';
</script>

<!-- ✅ CORRECT -->
<script>
  import { Button } from '$lib/components';
</script>
```

**❌ Not Using Barrel Exports**

Always export components through index.ts:

```typescript
// ❌ WRONG
import { Button } from '$lib/components/ui/button/button.svelte';

// ✅ CORRECT
import { Button } from '$lib/components';
```

---

## Notes

- **Showcase is a reference, not a package** - Copy components into your project
- **All components use Svelte 5 runes** - No Svelte 4 syntax allowed
- **TypeScript strict mode required** - Components rely on type safety
- **Tailwind CSS is mandatory** - Components are styled with Tailwind
- **shadcn-svelte philosophy** - Own the code, customize freely
- **Examples are production-ready** - Copy/paste and customize as needed
- **Form handling uses superforms** - Best-in-class validation and DX
- **Icons use lucide-svelte** - 1,666 icons, tree-shakeable
- **Dark mode supported** - Use mode-watcher for automatic theming
- **Accessibility built-in** - Components follow WAI-ARIA patterns

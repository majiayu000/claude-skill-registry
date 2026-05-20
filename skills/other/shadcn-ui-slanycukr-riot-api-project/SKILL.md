---
name: shadcn/ui
description: A collection of beautifully designed, accessible UI components built with Radix UI and Tailwind CSS
when_to_use: When building modern React applications with customizable, copy-pasteable components that can be easily themed and composed
requirements:
  - React 16.8 or higher
  - Tailwind CSS 2.0 or higher
  - TypeScript recommended
  - Node.js 12.x or higher
---

# shadcn/ui

shadcn/ui is a collection of accessible and customizable UI components that you can copy and paste into your applications. It's built on top of Radix UI and Tailwind CSS, allowing you to build your own component library with beautiful defaults and complete customization.

## Quick Start

### Installation

```bash
# Initialize your project
npx shadcn@latest init

# Add components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
```

### Configuration

Create a `components.json` file to customize your setup:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/styles/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui"
  }
}
```

### Basic Usage

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Example() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Get Started</Button>
      </CardContent>
    </Card>
  );
}
```

## Common Patterns

### Component Installation

```bash
# Add single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button card input

# Add from custom registry
npx shadcn@latest add @v0/dashboard
```

### Component Customization

Components use Class Variance Authority (CVA) for variants:

```tsx
// Button with variants
<Button variant="destructive" size="sm">
  Delete
</Button>

<Card className="shadow-lg">
  <CardHeader>
    <CardTitle>Custom Card</CardTitle>
  </CardHeader>
</Card>
```

### Theme Customization

Add CSS variables for theming:

```css
@layer base {
  :root {
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 47.4% 11.2%;
  }

  .dark {
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}
```

### Form Patterns

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

function FormField({ label, ...props }) {
  return (
    <div className="space-y-2">
      <Label htmlFor={props.id}>{label}</Label>
      <Input {...props} />
    </div>
  );
}
```

### Component Composition

```tsx
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
} from "@/components/ui/alert-dialog";

function ConfirmDialog() {
  return (
    <AlertDialog>
      <AlertDialogContent>
        <AlertDialogAction>Confirm</AlertDialogAction>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

## Popular Components

### Navigation

- `breadcrumb` - Navigation breadcrumb
- `navigation-menu` - Dropdown navigation
- `menubar` - Application menu bar

### Forms

- `input` - Text input field
- `button` - Action button
- `select` - Dropdown select
- `checkbox` - Checkbox input
- `radio-group` - Radio button group

### Layout

- `card` - Content container
- `dialog` - Modal dialog
- `sheet` - Slide-out panel
- `tabs` - Tabbed content

### Data Display

- `table` - Data table
- `badge` - Status indicator
- `avatar` - User avatar
- `separator` - Visual divider

### Feedback

- `toast` - Notification message
- `alert` - Alert message
- `progress` - Progress indicator
- `spinner` - Loading indicator

## Manual Installation

For projects not using the CLI:

1. **Install dependencies**:

```bash
npm install class-variance-authority clsx tailwind-merge lucide-react
```

2. **Create utils file**:

```tsx
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

3. **Copy component code** from the shadcn/ui documentation into your project.

## Best Practices

- Use TypeScript for better type safety
- Customize components by copying and modifying the source code
- Leverage CSS variables for consistent theming
- Compose components to build complex UI patterns
- Follow accessibility guidelines built into Radix UI primitives

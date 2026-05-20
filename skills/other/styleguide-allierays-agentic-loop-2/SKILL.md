---
description: Generate a complete HTML/React styleguide page for your project based on your design preferences.
---

# Styleguide Generator

Generate a complete HTML/React styleguide page for your project based on your design preferences.

## Instructions

This skill creates a `/styleguide` route that displays all your UI components, making it easy for AI to understand and replicate your design system.

### Phase 1: Discovery

First, understand the project:

**Check the tech stack:**
- Look for `package.json` to identify the framework (React, Vue, Next.js, etc.)
- Check for existing styling solution (Tailwind, CSS Modules, styled-components, etc.)
- Find the components directory structure
- Look for any existing design tokens or theme files

**Check for existing components:**
- Search for `components/` or `src/components/`
- Look for existing Button, Input, Card components
- Note any UI library usage (shadcn, MUI, Chakra, etc.)

### Phase 2: Interview the User

Ask these questions to understand their design vision. Present them as a friendly conversation:

**1. "What's the vibe you're going for?"**

Offer examples:
- **Clean & Minimal** - Lots of whitespace, subtle shadows, muted colors
- **Bold & Vibrant** - Saturated colors, strong contrasts, energetic
- **Dark & Moody** - Dark backgrounds, neon accents, atmospheric
- **Soft & Friendly** - Rounded corners, pastels, warm feeling
- **Professional & Corporate** - Conservative, trustworthy, structured
- **Playful & Fun** - Bright colors, animations, personality
- **Neon Glass** - Glassmorphism, glows, futuristic
- **Other** - Let them describe it

**2. "What are your brand colors?"**

Ask for:
- **Primary color** - Main brand color (buttons, links, accents)
- **Secondary color** - Supporting color
- **Accent color** - For highlights and CTAs (optional)

If they don't have colors, suggest palettes based on their vibe:
- Clean: Blue (#3B82F6) + Gray
- Bold: Orange (#F97316) + Purple (#8B5CF6)
- Dark: Cyan (#06B6D4) + Purple (#A855F7)
- Soft: Pink (#EC4899) + Lavender (#A78BFA)
- Professional: Navy (#1E40AF) + Gold (#F59E0B)

**3. "Light mode, dark mode, or both?"**

- Light mode only
- Dark mode only
- Both (with toggle)

**4. "What's your border radius preference?"**

- **Sharp** - 0px (modern, editorial)
- **Subtle** - 4px (clean, professional)
- **Rounded** - 8px (friendly, approachable)
- **Pill** - 9999px for buttons (playful)
- **Mixed** - Rounded cards, pill buttons

**5. "Any specific components you need?"**

Common ones to include:
- Buttons (primary, secondary, ghost, destructive)
- Form inputs (text, select, checkbox, radio, toggle)
- Cards
- Modals/Dialogs
- Alerts/Toasts
- Navigation
- Tables
- Badges/Tags

### Phase 3: Generate the Styleguide

Create a styleguide page at `/styleguide` (or their preferred route).

**File structure for React/Next.js:**
```
src/
├── pages/styleguide.tsx (or app/styleguide/page.tsx for Next.js App Router)
└── styles/
    └── design-tokens.css (optional CSS variables)
```

**Include these sections:**

#### 1. Design Tokens
```tsx
<section id="tokens">
  <h2>Design Tokens</h2>

  {/* Colors */}
  <div className="grid grid-cols-5 gap-4">
    <div className="h-20 rounded-lg bg-primary" title="Primary" />
    <div className="h-20 rounded-lg bg-secondary" title="Secondary" />
    <div className="h-20 rounded-lg bg-accent" title="Accent" />
    <div className="h-20 rounded-lg bg-background" title="Background" />
    <div className="h-20 rounded-lg bg-foreground" title="Foreground" />
  </div>

  {/* Typography Scale */}
  <div className="space-y-2 mt-8">
    <p className="text-xs">xs - 12px</p>
    <p className="text-sm">sm - 14px</p>
    <p className="text-base">base - 16px</p>
    <p className="text-lg">lg - 18px</p>
    <p className="text-xl">xl - 20px</p>
    <p className="text-2xl">2xl - 24px</p>
    <p className="text-3xl">3xl - 30px</p>
    <p className="text-4xl">4xl - 36px</p>
  </div>

  {/* Spacing */}
  <div className="flex items-end gap-2 mt-8">
    <div className="w-1 h-1 bg-primary" title="1 - 4px" />
    <div className="w-2 h-2 bg-primary" title="2 - 8px" />
    <div className="w-3 h-3 bg-primary" title="3 - 12px" />
    <div className="w-4 h-4 bg-primary" title="4 - 16px" />
    <div className="w-6 h-6 bg-primary" title="6 - 24px" />
    <div className="w-8 h-8 bg-primary" title="8 - 32px" />
  </div>
</section>
```

#### 2. Buttons
```tsx
<section id="buttons">
  <h2>Buttons</h2>

  {/* Variants */}
  <div className="flex flex-wrap gap-4">
    <Button variant="primary">Primary</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="ghost">Ghost</Button>
    <Button variant="destructive">Destructive</Button>
    <Button variant="link">Link</Button>
  </div>

  {/* Sizes */}
  <div className="flex items-center gap-4 mt-4">
    <Button size="sm">Small</Button>
    <Button size="md">Medium</Button>
    <Button size="lg">Large</Button>
  </div>

  {/* States */}
  <div className="flex flex-wrap gap-4 mt-4">
    <Button>Default</Button>
    <Button disabled>Disabled</Button>
    <Button loading>Loading</Button>
  </div>

  {/* With Icons */}
  <div className="flex gap-4 mt-4">
    <Button><PlusIcon /> Add Item</Button>
    <Button>Next <ArrowRightIcon /></Button>
    <Button size="icon"><SearchIcon /></Button>
  </div>
</section>
```

#### 3. Form Inputs
```tsx
<section id="forms">
  <h2>Form Inputs</h2>

  {/* Text Inputs */}
  <div className="space-y-4 max-w-md">
    <Input label="Default" placeholder="Enter text..." />
    <Input label="With value" value="Hello world" />
    <Input label="Disabled" disabled value="Can't edit" />
    <Input label="With error" error="This field is required" />
    <Input label="With helper" helper="We'll never share your email" />
  </div>

  {/* Select */}
  <Select label="Choose option">
    <option>Option 1</option>
    <option>Option 2</option>
    <option>Option 3</option>
  </Select>

  {/* Checkbox & Radio */}
  <div className="space-y-2 mt-4">
    <Checkbox label="Accept terms" />
    <Checkbox label="Checked" checked />
    <Checkbox label="Disabled" disabled />
  </div>

  {/* Toggle */}
  <div className="flex gap-4 mt-4">
    <Toggle label="Off" />
    <Toggle label="On" checked />
  </div>
</section>
```

#### 4. Cards
```tsx
<section id="cards">
  <h2>Cards</h2>

  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
    {/* Basic Card */}
    <Card>
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card description goes here</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Card content with some text.</p>
      </CardContent>
    </Card>

    {/* Card with Image */}
    <Card>
      <img src="/placeholder.jpg" className="w-full h-40 object-cover" />
      <CardContent>
        <h3>Image Card</h3>
        <p>Card with image header</p>
      </CardContent>
    </Card>

    {/* Interactive Card */}
    <Card hover clickable>
      <CardContent>
        <h3>Interactive</h3>
        <p>Hover and click states</p>
      </CardContent>
    </Card>
  </div>
</section>
```

#### 5. Feedback Components
```tsx
<section id="feedback">
  <h2>Feedback</h2>

  {/* Alerts */}
  <div className="space-y-4">
    <Alert variant="info">This is an info message</Alert>
    <Alert variant="success">Success! Your changes were saved.</Alert>
    <Alert variant="warning">Warning: This action cannot be undone.</Alert>
    <Alert variant="error">Error: Something went wrong.</Alert>
  </div>

  {/* Badges */}
  <div className="flex gap-2 mt-6">
    <Badge>Default</Badge>
    <Badge variant="success">Success</Badge>
    <Badge variant="warning">Warning</Badge>
    <Badge variant="error">Error</Badge>
  </div>

  {/* Loading States */}
  <div className="flex gap-4 mt-6">
    <Spinner size="sm" />
    <Spinner size="md" />
    <Spinner size="lg" />
    <Skeleton className="h-4 w-32" />
    <Skeleton className="h-10 w-full" />
  </div>
</section>
```

### Phase 4: Generate Component Files

If components don't exist yet, create them based on the user's preferences.

**Example Button component (Tailwind + React):**
```tsx
// src/components/ui/Button.tsx
import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive' | 'link';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          // Base styles
          'inline-flex items-center justify-center font-medium transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',

          // Variants (customize based on user's vibe)
          {
            'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'primary',
            'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary',
            'hover:bg-accent hover:text-accent-foreground': variant === 'ghost',
            'bg-destructive text-destructive-foreground hover:bg-destructive/90': variant === 'destructive',
            'text-primary underline-offset-4 hover:underline': variant === 'link',
          },

          // Sizes
          {
            'h-8 px-3 text-sm rounded-md': size === 'sm',
            'h-10 px-4 text-sm rounded-md': size === 'md',
            'h-12 px-6 text-base rounded-lg': size === 'lg',
            'h-10 w-10 rounded-md': size === 'icon',
          },

          className
        )}
        {...props}
      >
        {loading ? <Spinner className="mr-2" size="sm" /> : null}
        {children}
      </button>
    );
  }
);
```

### Phase 5: Add CSS Variables

Create design tokens as CSS variables for easy theming:

```css
/* src/styles/design-tokens.css */
:root {
  /* Colors - Light Mode */
  --color-primary: 59 130 246;      /* blue-500 */
  --color-secondary: 100 116 139;   /* slate-500 */
  --color-accent: 168 85 247;       /* purple-500 */
  --color-background: 255 255 255;  /* white */
  --color-foreground: 15 23 42;     /* slate-900 */
  --color-muted: 241 245 249;       /* slate-100 */
  --color-border: 226 232 240;      /* slate-200 */

  /* Feedback Colors */
  --color-success: 34 197 94;       /* green-500 */
  --color-warning: 234 179 8;       /* yellow-500 */
  --color-error: 239 68 68;         /* red-500 */
  --color-info: 59 130 246;         /* blue-500 */

  /* Spacing */
  --spacing-unit: 4px;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px rgb(0 0 0 / 0.1);
}

/* Dark Mode */
.dark {
  --color-background: 15 23 42;     /* slate-900 */
  --color-foreground: 248 250 252;  /* slate-50 */
  --color-muted: 30 41 59;          /* slate-800 */
  --color-border: 51 65 85;         /* slate-700 */
}
```

### Phase 6: Update CLAUDE.md

Add the styleguide reference to the project's CLAUDE.md:

```markdown
## Design System

Reference `/styleguide` for all UI components and design tokens.

### Quick Reference
- Primary: [color]
- Border Radius: [preference]
- Mode: [light/dark/both]

### Components
Use components from `@/components/ui`:
- Button, Input, Select, Checkbox, Toggle
- Card, Alert, Badge, Modal
- All variants shown in /styleguide
```

### Vibe-Specific Templates

**Neon Glass:**
```tsx
// Dark background with glassmorphism
<div className="bg-black min-h-screen">
  <Card className="
    bg-white/5 backdrop-blur-xl
    border border-white/10
    shadow-[0_0_30px_rgba(0,255,255,0.1)]
  ">
    <h2 className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">
      Neon Glass
    </h2>
  </Card>
</div>
```

**Clean & Minimal:**
```tsx
// Lots of whitespace, subtle shadows
<div className="bg-gray-50 min-h-screen p-12">
  <Card className="bg-white shadow-sm border border-gray-100 rounded-lg">
    <h2 className="text-gray-900 font-light tracking-tight">
      Clean & Minimal
    </h2>
  </Card>
</div>
```

**Bold & Vibrant:**
```tsx
// Strong colors, high contrast
<div className="bg-gradient-to-br from-orange-500 to-pink-600 min-h-screen">
  <Card className="bg-white rounded-2xl shadow-2xl">
    <h2 className="text-3xl font-black text-gray-900">
      Bold & Vibrant
    </h2>
  </Card>
</div>
```

## Notes

- Always create components that match the user's chosen vibe
- Include all states (hover, active, focus, disabled, loading)
- Make the styleguide itself match the design system
- Add code snippets so developers can copy usage examples
- Test in both light and dark mode if applicable

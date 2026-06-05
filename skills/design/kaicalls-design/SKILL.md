---
name: kaicalls-design
description: Build KaiCalls-compliant UI components and pages using the KaiCalls design system. Use when creating new dashboard pages, components, forms, tables, cards, badges, or any UI within the KaiCalls admin panel. Ensures dark-first aesthetic, proper color tokens, typography classes, motion standards, and B2B SaaS best practices. Triggers on "build a page", "create a component", "add a dashboard", "design a form", or any frontend work in the adminpanelnew codebase.
---

Build KaiCalls-compliant UI using the dark-first design system, shadcn/ui components, and B2B SaaS best practices.

## Design Philosophy

KaiCalls follows "Minimum Lovable Product" (MLP) principles:
- **Zero Support Required**: UI so intuitive users never need docs
- **Every Click Invokes Emotion**: Button clicks should feel satisfying with visual/motion feedback
- **Micro-Celebrations**: Reward actions with delightful feedback (confetti, checkmarks, sounds)
- **Software Teammate**: Humanize through conversational copy and helpful empty states
- **Dark-First**: Premium aesthetic inspired by Linear, Notion, Stripe

**CRITICAL**: Every interactive element should provide emotional feedback. Users should *feel* their actions.

**IMPORTANT**: Keep feedback subtle and gentle. No harsh flashing, strobing, or high-contrast animations that strain eyes. Our users include older professionals who spend long hours on screen.

## Quick Reference

### Core Colors (CSS Variables)

```css
/* Backgrounds */
--background: #12121A      /* Main background */
--card: #181B23            /* Card surfaces */
--secondary: #23263B       /* Secondary surfaces, inputs */
--surface-elevated: #2A2D3E

/* Brand */
--kai-blue: #5C8CFF        /* Primary brand */
--kai-purple: #C68BF8      /* Accent */
--kai-btn-primary: #3575F6 /* Primary button */

/* Text */
--foreground: #F7F7FA      /* Primary text */
--muted-foreground: #A7A9BE /* Secondary text */
--kai-text-placeholder: #6B6D76

/* Status */
--kai-success-text: #34D399
--kai-error-text: #FF4B4B
--kai-warning-text: #FFC04B
--kai-info-text: #5C8CFF
```

### Tailwind Classes

Use `kai-*` prefix for brand colors:
```tsx
// Backgrounds
className="bg-background"      // Main page
className="bg-card"            // Cards
className="bg-secondary"       // Inputs, secondary surfaces

// Text
className="text-foreground"    // Primary text (white)
className="text-muted-foreground" // Secondary text
className="text-kai-blue"      // Brand blue
className="text-kai-purple"    // Accent purple

// Borders
className="border-border"      // Standard borders
className="border-kai-table-border" // Table borders
```

### Typography Classes

```tsx
// Headings (use semantic classes)
<h1 className="heading-xl">Page Title</h1>      // 2xl bold white
<h2 className="heading-lg">Section Title</h2>  // xl semibold white
<h3 className="heading-md">Card Title</h3>     // lg semibold white
<h4 className="heading-sm">Subsection</h4>     // base semibold white

// Body text
<p className="text-body-primary">Main content</p>    // white
<p className="text-body-secondary">Helper text</p>   // slate-400
<p className="text-body-tertiary">Timestamp</p>      // slate-500

// Labels
<span className="label-uppercase">SECTION</span>     // xs uppercase tracking-wide slate-400
<label className="label-default">Field</label>       // sm medium slate-400
<span className="stat-label">METRIC</span>           // xs uppercase slate-400
```

## Component Patterns

### Cards

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>Title Here</CardTitle>
    <CardDescription>Description text</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
</Card>

// Card base: rounded-lg border-slate-700/50 bg-slate-800/60 text-white shadow-sm
```

### Buttons

```tsx
import { Button } from "@/components/ui/button";

<Button>Default (Primary)</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
```

### Badges (Status & Temperature)

```tsx
// Temperature badges (lead scoring)
<span className="badge-hot">Hot</span>    // Red: #FF4B4B33 bg, #FF6B6B text
<span className="badge-warm">Warm</span>  // Yellow: #FFC04B33 bg, #FFD76B text
<span className="badge-cold">Cold</span>  // Blue: #4B7BFF33 bg, #6B93FF text

// Status badges
<span className="status-success">Active</span>   // Green
<span className="status-error">Failed</span>     // Red
<span className="status-warning">Pending</span>  // Yellow
<span className="status-info">Info</span>        // Blue

// All badges: rounded-full px-2.5 py-0.5 font-semibold
```

### Tables

```tsx
// Table row with hover
<tr className="table-row hover:bg-kai-hover-row">
  <td className="px-4 py-3">Content</td>
</tr>

// Selected row
<tr className="table-row-selected">
  <td>Selected content</td>
</tr>

// Table headers: text-kai-text-table-heading (#B0B2C3)
```

### Forms & Inputs

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" placeholder="Enter email" />
</div>

// Input base: bg-secondary border-border text-foreground
// Focus: ring-kai-blue
```

### Dialogs/Modals

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

<Dialog>
  <DialogContent className="bg-modal-bg border-modal-border">
    <DialogHeader>
      <DialogTitle>Modal Title</DialogTitle>
      <DialogDescription>Description here</DialogDescription>
    </DialogHeader>
    {/* Content */}
  </DialogContent>
</Dialog>
```

## Emotional Interactions

**Every button click should invoke emotion.** Users perform tedious tasks; reward them.

**Keep it subtle.** Feedback should be felt, not seen. Avoid:
- Bright flashes or strobing effects
- High-contrast color pops (white on dark)
- Large, jarring movements
- Animations longer than 300ms
- Anything that draws attention away from the task

Prefer: soft glows, gentle scale changes (1.02-1.05x), muted color transitions, spring physics with high damping.

### Micro-Celebration Triggers

| Action | Feedback | Implementation |
|--------|----------|----------------|
| Task complete | Soft checkmark fade-in | Icon opacity 0→1 over 200ms |
| Form submit | Gentle green tint, quiet toast | Subtle bg-color shift, no flash |
| Delete/Archive | Smooth slide away | Slide-out 250ms with opacity fade |
| Toggle on | Soft snap into place | Spring with damping 0.8 |
| Save success | Soft glow around button | Box-shadow fade in/out over 400ms |
| Error | Gentle wobble + muted red | 2-3px horizontal shake, soft red |

**Eye comfort guidelines:**
- Use muted success green (#34D399 at 60% opacity) not bright green
- Error red should be soft (#FF4B4B with transparency), never pure red
- Confetti/particles should be sparse and low-contrast
- Prefer opacity transitions over color flashes

### Button Feedback Patterns

```tsx
// Success button with feedback
<Button
  onClick={async () => {
    await action();
    // Show success state briefly
    setSuccess(true);
    setTimeout(() => setSuccess(false), 1500);
  }}
  className={cn(
    "transition-all duration-150",
    success && "bg-kai-success-text scale-105"
  )}
>
  {success ? <Check className="h-4 w-4" /> : "Save Changes"}
</Button>

// Loading state with anticipation
<Button disabled={loading}>
  {loading ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Saving...
    </>
  ) : (
    "Save"
  )}
</Button>
```

### Toast Celebrations

```tsx
import { toast } from "sonner";

// Success with personality
toast.success("Agent created!", {
  description: "Your AI assistant is ready to take calls."
});

// Milestone celebration
toast("Deal closed!", {
  icon: "🎉",
  description: "Great work! $50,000 added to pipeline."
});
```

### High-Anxiety Moment Patterns

Identify moments where users feel nervous and provide reassurance:

```tsx
// Before destructive action - confirm with clear consequences
<AlertDialog>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Delete this agent?</AlertDialogTitle>
      <AlertDialogDescription>
        This will permanently remove "Sales Assistant" and all its call history.
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Keep Agent</AlertDialogCancel>
      <AlertDialogAction className="bg-destructive">
        Yes, Delete Agent
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>

// After scary action - immediate reassurance
toast.success("Agent deleted", {
  description: "Don't worry, your leads are still safe."
});
```

### Hover & Focus States

Every interactive element needs visible feedback (keep it gentle):

```tsx
// Button hover: tiny scale, subtle brighten
className="hover:scale-[1.02] hover:brightness-105 transition-all duration-150"

// Card hover: slight lift with soft shadow
className="hover:shadow-elevation-md hover:-translate-y-0.5 transition-all duration-200"

// Link hover: gentle color shift
className="hover:text-kai-purple/80 transition-colors duration-150"
```

### Reduced Motion Support

Respect users who prefer reduced motion:

```tsx
// Use Tailwind's motion-safe/motion-reduce
className="motion-safe:hover:scale-[1.02] motion-reduce:hover:opacity-80"

// Or check in JS
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

## Motion Standards

All animations must run at 60fps.

| Interaction | Duration | Easing |
|------------|----------|--------|
| Micro (toggles, buttons) | 120-160ms | ease-out |
| Small transitions | 200-240ms | ease-out |
| Screen transitions | 300-400ms | cubic-bezier(0.4, 0, 0.2, 1) |

```css
/* Use design system tokens */
--transition-fast: 150ms
--transition-normal: 200ms
--transition-slow: 300ms
```

### Animation Classes

```tsx
// Skeleton loading (use instead of spinners)
<div className="skeleton-shimmer h-4 w-32 rounded" />

// Collapsible
<CollapsibleContent className="collapsible-content">
  <ChevronIcon className="collapsible-chevron" />
</CollapsibleContent>
```

## Elevation & Shadows

```tsx
// Shadow utilities
className="shadow-elevation-sm"  // Subtle
className="shadow-elevation-md"  // Cards
className="shadow-elevation-lg"  // Dropdowns
className="shadow-elevation-xl"  // Modals

// Z-index scale
className="z-dropdown"  // 50
className="z-modal"     // 100
className="z-toast"     // 150
```

## Empty States

Never show "No data found." Always provide:
1. Helpful illustration (optional)
2. Encouraging copy explaining what goes here
3. Clear CTA to populate data

```tsx
<div className="text-center py-12">
  <Illustration className="mx-auto mb-4 h-24 w-24 text-muted-foreground" />
  <h3 className="heading-md mb-2">No leads yet</h3>
  <p className="text-body-secondary mb-4">
    Leads will appear here when callers reach your AI assistant.
  </p>
  <Button>Create Your First Agent</Button>
</div>
```

## Loading States

Use skeleton loaders that match content shape:

```tsx
// Card skeleton
<Card>
  <CardHeader>
    <Skeleton className="h-6 w-48" />
    <Skeleton className="h-4 w-32 mt-2" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-24 w-full" />
  </CardContent>
</Card>

// Table skeleton
{Array.from({ length: 5 }).map((_, i) => (
  <tr key={i}>
    <td><Skeleton className="h-4 w-24" /></td>
    <td><Skeleton className="h-4 w-32" /></td>
    <td><Skeleton className="h-4 w-16" /></td>
  </tr>
))}
```

## Gradient Utilities

```tsx
// Brand gradient background
<div className="bg-gradient-kai">Gradient bg</div>

// Gradient text
<span className="text-gradient-kai">Gradient text</span>

// The gradient: linear-gradient(90deg, #5C8CFF 0%, #C68BF8 100%)
```

## Page Layout Template

```tsx
export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="heading-xl">Page Title</h1>
          <p className="text-body-secondary mt-1">
            Brief description of this page
          </p>
        </div>
        <Button>Primary Action</Button>
      </div>

      {/* Content cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Card Title</CardTitle>
          </CardHeader>
          <CardContent>
            {/* Content */}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

## Stat Card Pattern

```tsx
<Card>
  <CardContent className="p-6">
    <div className="flex items-center justify-between">
      <span className="stat-label">Total Calls</span>
      <Phone className="h-4 w-4 text-muted-foreground" />
    </div>
    <div className="mt-2">
      <span className="data-value">1,234</span>
      <span className="text-kai-success-text text-sm ml-2">+12%</span>
    </div>
  </CardContent>
</Card>
```

## Error Handling

Humanize errors with conversational copy:

```tsx
// Instead of "Error 500"
<Alert variant="destructive">
  <AlertTitle>Something went wrong</AlertTitle>
  <AlertDescription>
    We're looking into it. Try refreshing the page.
  </AlertDescription>
</Alert>
```

## Checklist Before Shipping

- [ ] **Every button has emotional feedback** (hover, active, success states)
- [ ] **Feedback is subtle** (no flashing, strobing, or harsh contrast)
- [ ] Uses design system color tokens (not hardcoded hex)
- [ ] Typography uses semantic classes (heading-*, text-body-*)
- [ ] Loading states use skeletons (not spinners)
- [ ] Empty states have helpful copy and CTAs
- [ ] Success actions show micro-celebrations (toast, animation, color change)
- [ ] Destructive actions have confirmation + reassurance
- [ ] Animations run at 60fps and are under 300ms
- [ ] Respects prefers-reduced-motion (use motion-safe/motion-reduce)
- [ ] Dark mode compatible (no light-only colors)
- [ ] Mobile responsive (min-width 375px)
- [ ] Uses shadcn/ui components where available

## Reference Documentation

For detailed information, see:
- [Full Color Tokens](references/full-color-tokens.md) - Complete list of all CSS variables and Tailwind classes
- [Component Examples](references/component-examples.md) - Real-world patterns for dashboards, tables, forms, and more

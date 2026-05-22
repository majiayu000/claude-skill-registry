---
name: design
description: Auto-activates when user mentions UI design, design systems, or component design. Expert in design principles, accessibility, and component architecture.
category: design
---

# UI/UX Design Guidelines

## Core Principles

1. **User-Centered Design** - Always design for the user's needs, not your preferences
2. **Consistency** - Maintain consistent patterns across the entire interface
3. **Accessibility First** - Design for all users, including those with disabilities
4. **Progressive Disclosure** - Show only what's needed, when it's needed
5. **Feedback & Affordance** - Make interactions clear and provide immediate feedback

## Design System Foundations

### Design Tokens
Use design tokens for all visual properties to ensure consistency and enable theming:

```css
/* ✅ Good: Use design tokens */
:root {
  /* Colors */
  --color-primary: #0066ff;
  --color-secondary: #6b7280;
  --color-success: #10b981;
  --color-error: #ef4444;
  --color-warning: #f59e0b;
  
  /* Spacing (8px grid) */
  --space-xs: 0.25rem;  /* 4px */
  --space-sm: 0.5rem;   /* 8px */
  --space-md: 1rem;     /* 16px */
  --space-lg: 1.5rem;   /* 24px */
  --space-xl: 2rem;     /* 32px */
  --space-2xl: 3rem;    /* 48px */
  
  /* Typography */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "SF Mono", Monaco, "Cascadia Code", monospace;
  
  --text-xs: 0.75rem;   /* 12px */
  --text-sm: 0.875rem;  /* 14px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.125rem;  /* 18px */
  --text-xl: 1.25rem;   /* 20px */
  --text-2xl: 1.5rem;   /* 24px */
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

### ❌ Bad: Hardcoded values
```css
.button {
  padding: 12px 20px;  /* Should use design tokens */
  background: #0066ff; /* Should use --color-primary */
  font-size: 14px;     /* Should use --text-sm */
}
```

## Component Design Patterns

### Buttons

```tsx
// ✅ Good: Comprehensive button with states
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ 
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  leftIcon,
  rightIcon,
  children,
  onClick,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        "inline-flex items-center justify-center gap-2",
        "font-semibold rounded-md transition-all",
        "focus:outline-none focus:ring-2 focus:ring-offset-2",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        
        // Variants
        variant === 'primary' && "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
        variant === 'secondary' && "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500",
        variant === 'ghost' && "bg-transparent hover:bg-gray-100 focus:ring-gray-500",
        variant === 'danger' && "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
        
        // Sizes
        size === 'sm' && "px-3 py-1.5 text-sm",
        size === 'md' && "px-4 py-2 text-base",
        size === 'lg' && "px-6 py-3 text-lg"
      )}
      disabled={disabled || loading}
      onClick={onClick}
      aria-busy={loading}
      {...props}
    >
      {loading && <Spinner size={size} />}
      {!loading && leftIcon}
      {children}
      {!loading && rightIcon}
    </button>
  );
}
```

### Form Inputs

```tsx
// ✅ Good: Accessible form input with error states
interface InputProps {
  label: string;
  id: string;
  type?: string;
  error?: string;
  hint?: string;
  required?: boolean;
  disabled?: boolean;
}

export function Input({ 
  label, 
  id, 
  type = 'text',
  error,
  hint,
  required = false,
  disabled = false,
  ...props 
}: InputProps) {
  return (
    <div className="space-y-1">
      <label 
        htmlFor={id}
        className="block text-sm font-medium text-gray-700 dark:text-gray-300"
      >
        {label}
        {required && <span className="text-red-500 ml-1" aria-label="required">*</span>}
      </label>
      
      <input
        id={id}
        type={type}
        disabled={disabled}
        required={required}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : hint ? `${id}-hint` : undefined}
        className={cn(
          "w-full px-3 py-2 rounded-md",
          "border border-gray-300 dark:border-gray-600",
          "bg-white dark:bg-gray-800",
          "text-gray-900 dark:text-gray-100",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
          "disabled:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-60",
          error && "border-red-500 focus:ring-red-500"
        )}
        {...props}
      />
      
      {hint && !error && (
        <p id={`${id}-hint`} className="text-sm text-gray-500">
          {hint}
        </p>
      )}
      
      {error && (
        <p id={`${id}-error`} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

## Accessibility (a11y) Requirements

### Semantic HTML
```tsx
// ✅ Good: Semantic HTML
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/home">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
      <time dateTime="2025-01-15">January 15, 2025</time>
    </header>
    <p>Article content...</p>
  </article>
</main>

// ❌ Bad: Non-semantic divs
<div className="nav">
  <div className="nav-item" onClick={...}>Home</div>
</div>
```

### ARIA Labels & Roles
```tsx
// ✅ Good: Proper ARIA usage
<button 
  aria-label="Close dialog"
  aria-expanded={isOpen}
  onClick={handleClose}
>
  <XIcon aria-hidden="true" />
</button>

<div role="status" aria-live="polite">
  {message}
</div>

// Screen reader only text
<span className="sr-only">Loading...</span>
```

### Keyboard Navigation
```tsx
// ✅ Good: Full keyboard support
function Dropdown() {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Escape':
        close();
        break;
      case 'ArrowDown':
        focusNextItem();
        break;
      case 'ArrowUp':
        focusPreviousItem();
        break;
      case 'Enter':
      case ' ':
        selectItem();
        break;
    }
  };
  
  return (
    <div 
      role="listbox"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      aria-activedescendant={activeId}
    >
      {/* Items */}
    </div>
  );
}
```

### Color Contrast (WCAG AA)
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- UI components & graphics: 3:1 minimum

```tsx
// ✅ Good: Sufficient contrast
<p className="text-gray-900 dark:text-white">
  Primary text with high contrast
</p>

// ❌ Bad: Insufficient contrast
<p className="text-gray-400 dark:text-gray-500">
  Low contrast text (hard to read)
</p>
```

## Layout & Spacing

### 8px Grid System
Always use multiples of 8 for spacing and dimensions:

```tsx
// ✅ Good: 8px grid
<div className="p-4 gap-2">    {/* 16px, 8px */}
  <div className="h-12 w-32" /> {/* 48px, 128px */}
</div>

// ❌ Bad: Random values
<div className="p-3 gap-5">
  <div className="h-17 w-45" />
</div>
```

### Responsive Breakpoints (Mobile-First)
```tsx
// ✅ Good: Mobile-first responsive
<div className="
  grid grid-cols-1          /* Mobile: 1 column */
  sm:grid-cols-2            /* Tablet: 2 columns */
  lg:grid-cols-3            /* Desktop: 3 columns */
  xl:grid-cols-4            /* Wide: 4 columns */
  gap-4 sm:gap-6 lg:gap-8   /* Progressive spacing */
">
```

### Whitespace & Hierarchy
```tsx
// ✅ Good: Clear visual hierarchy
<section className="space-y-8">
  <div className="space-y-2">
    <h2 className="text-2xl font-bold">Section Title</h2>
    <p className="text-gray-600">Section description</p>
  </div>
  
  <div className="space-y-6">
    <Card /> {/* Related content grouped together */}
    <Card />
  </div>
</section>
```

## Typography

### Type Scale
```tsx
// ✅ Good: Consistent type scale
<h1 className="text-4xl md:text-5xl font-bold">Main Heading</h1>
<h2 className="text-3xl md:text-4xl font-bold">Section Heading</h2>
<h3 className="text-2xl md:text-3xl font-semibold">Subsection</h3>
<p className="text-base md:text-lg leading-relaxed">Body text</p>
<small className="text-sm text-gray-600">Helper text</small>
```

### Line Height & Letter Spacing
```css
/* ✅ Good: Readable typography */
.text-display {
  font-size: 3rem;
  line-height: 1.2;      /* Tight for headings */
  letter-spacing: -0.02em;
}

.text-body {
  font-size: 1rem;
  line-height: 1.6;      /* Relaxed for body text */
  letter-spacing: 0;
}
```

## Color System

### Semantic Colors
```tsx
// ✅ Good: Semantic color usage
<div className="
  bg-blue-50 dark:bg-blue-950     /* Informational */
  border-l-4 border-blue-500
  text-blue-900 dark:text-blue-100
">

<div className="
  bg-red-50 dark:bg-red-950       /* Error */
  border-l-4 border-red-500
  text-red-900 dark:text-red-100
">

<div className="
  bg-green-50 dark:bg-green-950   /* Success */
  border-l-4 border-green-500
  text-green-900 dark:text-green-100
">
```

### Dark Mode
```tsx
// ✅ Good: Always include dark mode
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-white
  border-gray-200 dark:border-gray-800
">
  <h1 className="text-gray-900 dark:text-white">
    Title
  </h1>
  <p className="text-gray-600 dark:text-gray-400">
    Description
  </p>
</div>
```

## User Feedback & States

### Loading States
```tsx
// ✅ Good: Clear loading indication
{isLoading ? (
  <div className="flex items-center gap-2" role="status">
    <Spinner aria-hidden="true" />
    <span>Loading data...</span>
  </div>
) : (
  <DataTable data={data} />
)}
```

### Empty States
```tsx
// ✅ Good: Helpful empty state
function EmptyState() {
  return (
    <div className="text-center py-12">
      <EmptyIcon className="mx-auto h-12 w-12 text-gray-400" aria-hidden="true" />
      <h3 className="mt-2 text-sm font-semibold text-gray-900">No projects</h3>
      <p className="mt-1 text-sm text-gray-500">
        Get started by creating a new project.
      </p>
      <Button className="mt-6">
        <PlusIcon className="mr-2" aria-hidden="true" />
        New Project
      </Button>
    </div>
  );
}
```

### Error States
```tsx
// ✅ Good: Actionable error message
{error && (
  <div className="rounded-md bg-red-50 p-4" role="alert">
    <div className="flex">
      <ErrorIcon className="h-5 w-5 text-red-400" aria-hidden="true" />
      <div className="ml-3">
        <h3 className="text-sm font-medium text-red-800">
          Error loading data
        </h3>
        <p className="mt-1 text-sm text-red-700">
          {error.message}
        </p>
        <Button 
          variant="ghost" 
          size="sm"
          onClick={retry}
          className="mt-2"
        >
          Try again
        </Button>
      </div>
    </div>
  </div>
)}
```

## Micro-interactions

### Hover & Focus States
```tsx
// ✅ Good: Clear interactive states
<button className="
  transition-all duration-200
  hover:scale-105
  hover:shadow-md
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
  active:scale-95
">
  Click me
</button>
```

### Animations (Subtle & Purposeful)
```tsx
// ✅ Good: Smooth entrance animation
<div className="
  animate-in fade-in slide-in-from-bottom-4
  duration-300 ease-out
">
  Content appears smoothly
</div>

// Respect prefers-reduced-motion
<div className="
  motion-safe:animate-bounce
  motion-reduce:animate-none
">
```

## Mobile-First Considerations

### Touch Targets
```tsx
// ✅ Good: Minimum 44x44px touch targets
<button className="min-h-[44px] min-w-[44px] px-4">
  Tap
</button>

// Increase tap area without visual size
<button className="relative p-2">
  <span className="absolute inset-0 -m-2" />
  <Icon />
</button>
```

### Safe Areas (iOS/Android)
```css
/* ✅ Good: Respect device safe areas */
.container {
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
}
```

## Design-to-Code Workflow

When converting designs to code:

1. **Analyze the Design**
   - Identify reusable components
   - Note color palette and typography
   - Map out spacing system

2. **Build from Atoms to Organisms**
   - Start with design tokens
   - Create base components (buttons, inputs)
   - Compose into larger patterns
   - Build full layouts

3. **Ensure Responsiveness**
   - Mobile-first approach
   - Test at all breakpoints
   - Progressive enhancement

4. **Add Interactivity**
   - Hover/focus states
   - Loading/error states
   - Smooth transitions
   - Keyboard navigation

5. **Accessibility Audit**
   - Semantic HTML
   - ARIA labels
   - Color contrast
   - Keyboard navigation
   - Screen reader testing

## Common Patterns

### Card Component
```tsx
// ✅ Good: Flexible card component
<Card className="overflow-hidden">
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description goes here</CardDescription>
  </CardHeader>
  <CardContent>
    Main content
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="ghost">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

### Modal/Dialog
```tsx
// ✅ Good: Accessible modal
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent aria-describedby="dialog-description">
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
    </DialogHeader>
    
    <p id="dialog-description">
      Dialog content goes here
    </p>
    
    <DialogFooter>
      <Button variant="ghost" onClick={close}>Cancel</Button>
      <Button onClick={confirm}>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## Advanced ARIA Patterns

### ✅ Good: Accessible Dialog/Modal
```tsx
import * as React from 'react';
import * as Dialog from '@radix-ui/react-dialog';

function AccessibleModal() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="btn">Open Dialog</button>
      </Dialog.Trigger>
      
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        
        <Dialog.Content
          className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6 shadow-xl max-w-md w-full"
          aria-describedby="dialog-description"
        >
          <Dialog.Title className="text-xl font-bold mb-4">
            Delete Account
          </Dialog.Title>
          
          <Dialog.Description id="dialog-description" className="text-gray-600 mb-4">
            This action cannot be undone. This will permanently delete your account.
          </Dialog.Description>
          
          <div className="flex gap-2 justify-end">
            <Dialog.Close asChild>
              <button className="btn btn-secondary">Cancel</button>
            </Dialog.Close>
            <button className="btn btn-danger">Delete</button>
          </div>
          
          <Dialog.Close asChild>
            <button 
              className="absolute top-2 right-2 p-1"
              aria-label="Close dialog"
            >
              <XIcon aria-hidden="true" />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### ✅ Good: Accessible Dropdown Menu
```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

function AccessibleDropdown() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button className="btn" aria-label="Open menu">
          <MenuIcon aria-hidden="true" />
        </button>
      </DropdownMenu.Trigger>
      
      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="bg-white rounded-md shadow-lg p-1"
          sideOffset={5}
        >
          <DropdownMenu.Item className="dropdown-item">
            <EditIcon aria-hidden="true" />
            Edit
            <DropdownMenu.Shortcut>⌘E</DropdownMenu.Shortcut>
          </DropdownMenu.Item>
          
          <DropdownMenu.Item className="dropdown-item">
            <DuplicateIcon aria-hidden="true" />
            Duplicate
            <DropdownMenu.Shortcut>⌘D</DropdownMenu.Shortcut>
          </DropdownMenu.Item>
          
          <DropdownMenu.Separator className="h-px bg-gray-200 my-1" />
          
          <DropdownMenu.Item className="dropdown-item text-red-600">
            <DeleteIcon aria-hidden="true" />
            Delete
            <DropdownMenu.Shortcut>⌘⌫</DropdownMenu.Shortcut>
          </DropdownMenu.Item>
          
          <DropdownMenu.Arrow className="fill-white" />
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
```

### ✅ Good: Accessible Tabs Pattern
```tsx
import * as Tabs from '@radix-ui/react-tabs';

function AccessibleTabs() {
  return (
    <Tabs.Root defaultValue="tab1">
      <Tabs.List 
        className="flex border-b border-gray-200"
        aria-label="Manage your account"
      >
        <Tabs.Trigger
          value="tab1"
          className="px-4 py-2 data-[state=active]:border-b-2 data-[state=active]:border-blue-500"
        >
          Profile
        </Tabs.Trigger>
        <Tabs.Trigger
          value="tab2"
          className="px-4 py-2 data-[state=active]:border-b-2 data-[state=active]:border-blue-500"
        >
          Settings
        </Tabs.Trigger>
        <Tabs.Trigger
          value="tab3"
          className="px-4 py-2 data-[state=active]:border-b-2 data-[state=active]:border-blue-500"
        >
          Billing
        </Tabs.Trigger>
      </Tabs.List>
      
      <Tabs.Content value="tab1" className="p-4">
        <h2 className="text-xl font-bold mb-2">Profile</h2>
        <p>Manage your profile settings here.</p>
      </Tabs.Content>
      
      <Tabs.Content value="tab2" className="p-4">
        <h2 className="text-xl font-bold mb-2">Settings</h2>
        <p>Configure your application settings.</p>
      </Tabs.Content>
      
      <Tabs.Content value="tab3" className="p-4">
        <h2 className="text-xl font-bold mb-2">Billing</h2>
        <p>Manage your billing information.</p>
      </Tabs.Content>
    </Tabs.Root>
  );
}
```

### ✅ Good: Accessible Accordion
```tsx
import * as Accordion from '@radix-ui/react-accordion';

function AccessibleAccordion() {
  return (
    <Accordion.Root type="multiple" className="space-y-2">
      <Accordion.Item value="item-1" className="border rounded-lg">
        <Accordion.Header>
          <Accordion.Trigger className="flex w-full items-center justify-between p-4 font-medium">
            What is accessibility?
            <ChevronDownIcon 
              aria-hidden="true"
              className="transition-transform data-[state=open]:rotate-180"
            />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="px-4 pb-4">
          Accessibility ensures that people with disabilities can perceive, understand, navigate, and interact with websites and tools.
        </Accordion.Content>
      </Accordion.Item>
      
      <Accordion.Item value="item-2" className="border rounded-lg">
        <Accordion.Header>
          <Accordion.Trigger className="flex w-full items-center justify-between p-4 font-medium">
            Why is WCAG important?
            <ChevronDownIcon 
              aria-hidden="true"
              className="transition-transform data-[state=open]:rotate-180"
            />
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content className="px-4 pb-4">
          WCAG (Web Content Accessibility Guidelines) provides a standard for making web content accessible to all users, including those with disabilities.
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  );
}
```

### ✅ Good: Toast Notifications with Live Regions
```tsx
import * as Toast from '@radix-ui/react-toast';

function ToastNotifications() {
  const [open, setOpen] = React.useState(false);
  
  return (
    <Toast.Provider swipeDirection="right">
      <button onClick={() => setOpen(true)}>Show notification</button>
      
      <Toast.Root
        open={open}
        onOpenChange={setOpen}
        className="bg-white rounded-lg shadow-lg p-4 flex items-start gap-3"
      >
        <InfoIcon aria-hidden="true" className="text-blue-500" />
        
        <div className="flex-1">
          <Toast.Title className="font-semibold">
            Update available
          </Toast.Title>
          <Toast.Description className="text-gray-600 text-sm">
            A new version of the app is ready to install.
          </Toast.Description>
        </div>
        
        <Toast.Action asChild altText="Install update">
          <button className="btn btn-sm">Install</button>
        </Toast.Action>
        
        <Toast.Close aria-label="Close notification">
          <XIcon aria-hidden="true" />
        </Toast.Close>
      </Toast.Root>
      
      <Toast.Viewport className="fixed bottom-0 right-0 p-6 flex flex-col gap-2 max-w-md" />
    </Toast.Provider>
  );
}
```

## Complete Keyboard Navigation Guide

### ✅ Good: Focus Management in Modals
```tsx
import { useEffect, useRef } from 'react';

function FocusTrappedModal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  
  useEffect(() => {
    if (isOpen) {
      // Store currently focused element
      previousFocusRef.current = document.activeElement as HTMLElement;
      
      // Focus first focusable element in modal
      const firstFocusable = modalRef.current?.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) as HTMLElement;
      firstFocusable?.focus();
      
      // Trap focus within modal
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key !== 'Tab') return;
        
        const focusableElements = Array.from(
          modalRef.current?.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          ) || []
        ) as HTMLElement[];
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      };
      
      document.addEventListener('keydown', handleKeyDown);
      
      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        // Restore focus when modal closes
        previousFocusRef.current?.focus();
      };
    }
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50"
    >
      {children}
    </div>
  );
}
```

### ✅ Good: Skip Links
```tsx
// At the top of your app
function App() {
  return (
    <>
      <a 
        href="#main-content" 
        className="sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0 focus:z-50 focus:p-4 focus:bg-white"
      >
        Skip to main content
      </a>
      
      <Header />
      
      <main id="main-content" tabIndex={-1}>
        {/* Main content */}
      </main>
    </>
  );
}
```

### ✅ Good: Keyboard Shortcuts
```tsx
import { useEffect } from 'react';

function useKeyboardShortcut(
  key: string,
  callback: () => void,
  modifiers: { ctrl?: boolean; shift?: boolean; alt?: boolean } = {}
) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const matchesModifiers =
        (modifiers.ctrl ? e.ctrlKey || e.metaKey : !e.ctrlKey && !e.metaKey) &&
        (modifiers.shift ? e.shiftKey : !e.shiftKey) &&
        (modifiers.alt ? e.altKey : !e.altKey);
      
      if (e.key === key && matchesModifiers) {
        e.preventDefault();
        callback();
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [key, callback, modifiers]);
}

// Usage
function Editor() {
  useKeyboardShortcut('s', handleSave, { ctrl: true });
  useKeyboardShortcut('k', openSearch, { ctrl: true });
  useKeyboardShortcut('/', focusSearch);
  
  return <div>...</div>;
}
```

## Responsive Design Complete Guide

### ✅ Good: Mobile-First Breakpoint Strategy
```tsx
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',   // Small devices (phones, 640px and up)
      'md': '768px',   // Medium devices (tablets, 768px and up)
      'lg': '1024px',  // Large devices (desktops, 1024px and up)
      'xl': '1280px',  // Extra large devices (large desktops, 1280px and up)
      '2xl': '1536px', // 2X large devices (larger desktops, 1536px and up)
    }
  }
};

// Mobile-first component
function ResponsiveGrid() {
  return (
    <div className="
      grid grid-cols-1     /* Mobile: 1 column */
      sm:grid-cols-2       /* Small: 2 columns */
      md:grid-cols-3       /* Medium: 3 columns */
      lg:grid-cols-4       /* Large: 4 columns */
      gap-4 sm:gap-6 md:gap-8  /* Progressive spacing */
    ">
      {items.map(item => <Card key={item.id} {...item} />)}
    </div>
  );
}
```

### ✅ Good: Container Queries (Modern Approach)
```tsx
// Use container queries for truly responsive components
function ProductCard() {
  return (
    <div className="@container">
      <div className="
        flex flex-col         /* Mobile: stack vertically */
        @md:flex-row          /* When container > md, switch to row */
        gap-4
      ">
        <img className="
          w-full @md:w-48     /* Full width on mobile, fixed on larger */
          aspect-square
          object-cover
        " />
        <div className="flex-1">
          <h3 className="text-lg @md:text-xl">Product Name</h3>
          <p className="text-sm @md:text-base">Description</p>
        </div>
      </div>
    </div>
  );
}
```

### ✅ Good: Responsive Typography
```tsx
// Fluid typography using clamp()
const styles = {
  heading: {
    fontSize: 'clamp(1.5rem, 5vw, 3rem)',  // Min 24px, scales with viewport, max 48px
    lineHeight: '1.2',
  },
  body: {
    fontSize: 'clamp(1rem, 2.5vw, 1.125rem)',  // Min 16px, max 18px
    lineHeight: '1.6',
  }
};

// Or with Tailwind
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">
  Responsive Heading
</h1>
```

### ✅ Good: Touch-Friendly Interfaces
```tsx
// Minimum touch target: 44x44px (iOS), 48x48px (Android)
function TouchFriendlyButton() {
  return (
    <button className="
      min-h-[44px] min-w-[44px]  /* Meet minimum touch target */
      px-6 py-3                   /* Comfortable spacing */
      text-base                   /* Readable text */
      rounded-lg
      active:scale-95             /* Visual feedback on tap */
      transition-transform
    ">
      Tap Me
    </button>
  );
}

// Increase tap area without changing visual size
function IconButton() {
  return (
    <button className="relative p-2">
      {/* Extend tap area beyond visual bounds */}
      <span className="absolute inset-0 -m-2" />
      <Icon className="w-6 h-6" />
    </button>
  );
}
```

### ✅ Good: iOS/Android Safe Areas
```css
/* Respect device safe areas (notches, rounded corners) */
.app-container {
  padding-top: env(safe-area-inset-top);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
}

/* Fixed header accounting for safe areas */
.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding-top: calc(1rem + env(safe-area-inset-top));
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

## Design Tokens & Design Systems

### ✅ Good: Comprehensive Design Token System
```typescript
// design-tokens.ts
export const tokens = {
  colors: {
    // Brand colors
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      500: '#3b82f6',
      600: '#2563eb',
      900: '#1e3a8a',
    },
    // Semantic colors
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
    // Neutrals
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      500: '#6b7280',
      900: '#111827',
    }
  },
  
  spacing: {
    0: '0',
    1: '0.25rem',  // 4px
    2: '0.5rem',   // 8px
    3: '0.75rem',  // 12px
    4: '1rem',     // 16px
    6: '1.5rem',   // 24px
    8: '2rem',     // 32px
    12: '3rem',    // 48px
    16: '4rem',    // 64px
  },
  
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace'],
    },
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],      // 12px
      sm: ['0.875rem', { lineHeight: '1.25rem' }],  // 14px
      base: ['1rem', { lineHeight: '1.5rem' }],     // 16px
      lg: ['1.125rem', { lineHeight: '1.75rem' }],  // 18px
      xl: ['1.25rem', { lineHeight: '1.75rem' }],   // 20px
      '2xl': ['1.5rem', { lineHeight: '2rem' }],    // 24px
    },
    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    }
  },
  
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
  },
  
  animation: {
    duration: {
      fast: '150ms',
      base: '200ms',
      slow: '300ms',
    },
    easing: {
      linear: 'linear',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    }
  },
  
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    modal: 1040,
    popover: 1050,
    toast: 1060,
  }
} as const;
```

### ✅ Good: Component Variant System
```tsx
// Using class-variance-authority (CVA)
import { cva, type VariantProps } from 'class-variance-authority';

const button = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
        ghost: 'hover:bg-gray-100',
        danger: 'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-12 px-6 text-lg',
      },
      disabled: {
        true: 'opacity-50 cursor-not-allowed pointer-events-none',
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    }
  }
);

type ButtonProps = VariantProps<typeof button> & 
  React.ButtonHTMLAttributes<HTMLButtonElement>;

export function Button({ variant, size, disabled, className, ...props }: ButtonProps) {
  return (
    <button
      className={button({ variant, size, disabled, className })}
      disabled={disabled}
      {...props}
    />
  );
}
```

## Liquid Glass Effects (Advanced)

Apple's Liquid Glass UI from WWDC 2025 uses physics-based refraction for premium glass effects.

### Core Physics

**Refraction** = Light bending through materials (Snell's Law)
- **Convex surfaces** (dome) - Push rays inward, keep content inside
- **Concave surfaces** (bowl) - Push rays outward, divergence
- **Squircle** (Apple's choice) - Smoother transitions, softer refraction edges

### ✅ Good: Basic Glass Panel (Cross-Browser)
```css
.glass-panel {
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

/* Specular highlight */
.glass-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.4) 0%,
    transparent 50%
  );
  pointer-events: none;
}
```

### ✅ Good: SVG Displacement Maps (Chrome Only)
```html
<svg colorInterpolationFilters="sRGB">
  <filter id="glass-distortion">
    <feImage href={displacementMapDataUrl} result="displacement_map"/>
    <feDisplacementMap 
      in="SourceGraphic" 
      in2="displacement_map"
      scale="77"
      xChannelSelector="R"
      yChannelSelector="G" 
    />
    <feImage href={specularHighlightUrl} result="specular"/>
    <feBlend in="SourceGraphic" in2="specular" mode="screen"/>
  </filter>
</svg>
```

```css
.liquid-glass {
  backdrop-filter: blur(3px) url(#glass-distortion);
  overflow: hidden;
}

/* Layer structure */
.liquid-glass-filter { z-index: 0; filter: url(#glass-distortion); }
.liquid-glass-tint { z-index: 1; background: rgba(255, 255, 255, 0.25); }
.liquid-glass-specular { z-index: 2; box-shadow: inset 2px 2px 1px rgba(255, 255, 255, 0.5); }
.liquid-glass-content { z-index: 3; position: relative; }
```

### ✅ Good: Interactive Glass with Mouse Tracking
```tsx
function InteractiveGlass() {
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const specular = e.currentTarget.querySelector('.glass-specular') as HTMLElement;
    if (specular) {
      specular.style.background = `radial-gradient(
        circle at ${x}px ${y}px,
        rgba(255, 255, 255, 0.15) 0%,
        rgba(255, 255, 255, 0.05) 30%,
        rgba(255, 255, 255, 0) 60%
      )`;
    }
  };
  
  return (
    <div className="glass-button" onMouseMove={handleMouseMove}>
      <div className="glass-filter" />
      <div className="glass-tint" />
      <div className="glass-specular" />
      <div className="glass-content">Premium Button</div>
    </div>
  );
}
```

### Design Parameters
- **Bezel Width**: 10-30px (edge refraction intensity)
- **Glass Thickness**: 50-150px (displacement magnitude)
- **Surface Shape**: Squircle for Apple-like smoothness
- **Specular Opacity**: 0.2-0.5 (highlight intensity)
- **Blur Level**: 3-20px (background blur strength)

### Browser Support
| Feature | Chrome | Safari | Firefox |
|---------|--------|--------|---------|
| `backdrop-filter` | ✅ | ✅ | ✅ |
| SVG as `backdrop-filter` | ✅ | ❌ | ❌ |
| Basic glass | ✅ | ✅ | ✅ |
| Advanced refraction | ✅ | ❌ | ❌ |

**Strategy**: Use basic glass for cross-browser, advanced SVG refraction as progressive enhancement for Chrome.

### Use Cases
**✅ When to use:**
- Premium UI (cards, panels, modals)
- Hero sections with depth
- Navigation bars with transparency
- Music/media player controls

**❌ When to avoid:**
- Text-heavy content (readability)
- High-contrast backgrounds (effect less visible)
- Mobile (performance concerns)
- Accessibility-critical UI

### Performance
✅ **Use CSS transforms** (hardware accelerated)
✅ **Limit blur radius** (smaller = faster)
✅ **Use `will-change`** for animations
❌ **Don't nest glass effects** (compounds cost)
❌ **Don't animate displacement maps** (pre-calculate)

### References
- [Liquid Glass CSS/SVG](https://kube.io/blog/liquid-glass-css-svg/) - Complete physics guide
- [Apple WWDC 2025](https://www.youtube.com/watch?v=jGztGfRujSE) - Official introduction
- [Glassmorphism UI](https://liquidglassui.org/) - Library & components

---

## Accessibility Testing Tools

### ✅ Good: Automated Testing with axe-core
```typescript
// __tests__/accessibility.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('should not have any accessibility violations', async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### ✅ Good: Manual Testing Checklist
```markdown
## Accessibility Testing Checklist

### Keyboard Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Focus is visible on all focusable elements
- [ ] Tab order is logical
- [ ] No keyboard traps
- [ ] Skip links work correctly

### Screen Reader
- [ ] All images have alt text
- [ ] ARIA labels are present where needed
- [ ] Form inputs have associated labels
- [ ] Headings follow proper hierarchy (h1 → h2 → h3)
- [ ] Live regions announce dynamic content

### Visual
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text)
- [ ] Content is readable when zoomed to 200%
- [ ] No information conveyed by color alone
- [ ] Focus indicators are visible

### Forms
- [ ] All form fields have labels
- [ ] Error messages are descriptive
- [ ] Required fields are indicated
- [ ] Validation errors are announced to screen readers
```

**ALWAYS follow these design principles and patterns to create accessible, consistent, and user-friendly interfaces. Test with real screen readers (NVDA, JAWS, VoiceOver) and keyboard-only navigation to ensure true accessibility. For premium effects, consider liquid glass techniques with proper cross-browser fallbacks.**

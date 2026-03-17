---
name: shadcn-ui
description: shadcn/ui component patterns. Component installation, customization, theming, accessibility. Use when building UI with shadcn components.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# shadcn/ui - Component Library Patterns

## Purpose

Expert guidance for shadcn/ui:

- **Component Usage** - Proper component implementation
- **Customization** - Tailwind-based styling
- **Theming** - Dark mode, colors, variants
- **Accessibility** - Radix UI primitives
- **Best Practices** - Composition patterns

---

## Installation

### Initial Setup

```bash
# Initialize shadcn/ui
bunx --bun shadcn@latest init

# Install components
bunx --bun shadcn@latest add button
bunx --bun shadcn@latest add card
bunx --bun shadcn@latest add dialog
bunx --bun shadcn@latest add form
bunx --bun shadcn@latest add input
bunx --bun shadcn@latest add toast
```

### Project Structure

```
components/
├── ui/                    # shadcn components (auto-generated)
│   ├── button.tsx
│   ├── card.tsx
│   ├── dialog.tsx
│   └── ...
├── features/              # Feature-specific components
│   └── user-card.tsx
└── layouts/               # Layout components
    └── main-layout.tsx
```

---

## Core Components

### Button

```tsx
import { Button } from '@/components/ui/button';

// Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><IconComponent /></Button>

// With loading state
<Button disabled={isPending}>
  {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Submit
</Button>
```

### Card

```tsx
import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';

<Card>
	<CardHeader>
		<CardTitle>Card Title</CardTitle>
		<CardDescription>Card description text</CardDescription>
	</CardHeader>
	<CardContent>
		<p>Card content here</p>
	</CardContent>
	<CardFooter>
		<Button>Action</Button>
	</CardFooter>
</Card>;
```

### Dialog

```tsx
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from '@/components/ui/dialog';

<Dialog>
	<DialogTrigger asChild>
		<Button variant="outline">Open Dialog</Button>
	</DialogTrigger>
	<DialogContent className="sm:max-w-[425px]">
		<DialogHeader>
			<DialogTitle>Edit Profile</DialogTitle>
			<DialogDescription>Make changes to your profile here.</DialogDescription>
		</DialogHeader>
		<div className="grid gap-4 py-4">{/* Form fields */}</div>
		<DialogFooter>
			<Button type="submit">Save changes</Button>
		</DialogFooter>
	</DialogContent>
</Dialog>;
```

### Form (with react-hook-form + zod)

```tsx
'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const formSchema = z.object({
	username: z.string().min(2).max(50),
	email: z.string().email(),
});

type FormValues = z.infer<typeof formSchema>;

export function ProfileForm() {
	const form = useForm<FormValues>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			username: '',
			email: '',
		},
	});

	function onSubmit(values: FormValues) {
		console.log(values);
	}

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
				<FormField
					control={form.control}
					name="username"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Username</FormLabel>
							<FormControl>
								<Input placeholder="johndoe" {...field} />
							</FormControl>
							<FormDescription>This is your public display name.</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="email"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Email</FormLabel>
							<FormControl>
								<Input type="email" placeholder="john@example.com" {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<Button type="submit">Submit</Button>
			</form>
		</Form>
	);
}
```

---

## Toast Notifications

### Setup

```tsx
// app/layout.tsx
import { Toaster } from '@/components/ui/toaster';

export default function RootLayout({ children }) {
	return (
		<html>
			<body>
				{children}
				<Toaster />
			</body>
		</html>
	);
}
```

### Usage

```tsx
import { useToast } from '@/hooks/use-toast';

export function MyComponent() {
	const { toast } = useToast();

	return (
		<Button
			onClick={() => {
				toast({
					title: 'Success!',
					description: 'Your changes have been saved.',
				});
			}}
		>
			Save
		</Button>
	);
}

// With variants
toast({
	variant: 'destructive',
	title: 'Error',
	description: 'Something went wrong.',
});
```

---

## Theming

### CSS Variables

```css
/* globals.css */
@layer base {
	:root {
		--background: 0 0% 100%;
		--foreground: 222.2 84% 4.9%;
		--card: 0 0% 100%;
		--card-foreground: 222.2 84% 4.9%;
		--popover: 0 0% 100%;
		--popover-foreground: 222.2 84% 4.9%;
		--primary: 222.2 47.4% 11.2%;
		--primary-foreground: 210 40% 98%;
		--secondary: 210 40% 96.1%;
		--secondary-foreground: 222.2 47.4% 11.2%;
		--muted: 210 40% 96.1%;
		--muted-foreground: 215.4 16.3% 46.9%;
		--accent: 210 40% 96.1%;
		--accent-foreground: 222.2 47.4% 11.2%;
		--destructive: 0 84.2% 60.2%;
		--destructive-foreground: 210 40% 98%;
		--border: 214.3 31.8% 91.4%;
		--input: 214.3 31.8% 91.4%;
		--ring: 222.2 84% 4.9%;
		--radius: 0.5rem;
	}

	.dark {
		--background: 222.2 84% 4.9%;
		--foreground: 210 40% 98%;
		/* ... dark mode values */
	}
}
```

### Dark Mode Toggle

```tsx
'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';

export function ThemeToggle() {
	const { theme, setTheme } = useTheme();

	return (
		<Button
			variant="ghost"
			size="icon"
			onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
		>
			<Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
			<Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
			<span className="sr-only">Toggle theme</span>
		</Button>
	);
}
```

---

## Customization Patterns

### Extend Variants

```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
	'inline-flex items-center justify-center rounded-md text-sm font-medium ...',
	{
		variants: {
			variant: {
				default: 'bg-primary text-primary-foreground hover:bg-primary/90',
				destructive: 'bg-destructive text-destructive-foreground ...',
				outline: 'border border-input bg-background hover:bg-accent ...',
				// Add custom variants
				success: 'bg-green-600 text-white hover:bg-green-700',
				warning: 'bg-yellow-500 text-black hover:bg-yellow-600',
			},
			size: {
				default: 'h-10 px-4 py-2',
				sm: 'h-9 rounded-md px-3',
				lg: 'h-11 rounded-md px-8',
				icon: 'h-10 w-10',
				// Add custom sizes
				xl: 'h-14 rounded-lg px-10 text-lg',
			},
		},
	}
);
```

### Composition

```tsx
// Wrap shadcn components with project-specific defaults
import { Button as ShadcnButton } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';

interface LoadingButtonProps extends React.ComponentProps<typeof ShadcnButton> {
	isLoading?: boolean;
}

export function LoadingButton({ children, isLoading, disabled, ...props }: LoadingButtonProps) {
	return (
		<ShadcnButton disabled={disabled || isLoading} {...props}>
			{isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
			{children}
		</ShadcnButton>
	);
}
```

---

## Accessibility

### Keyboard Navigation

```tsx
// All shadcn components support keyboard navigation by default
// Dialog: Escape to close, Tab to navigate
// Dropdown: Arrow keys to navigate, Enter to select
// Command: Type to search, arrows to navigate

// Ensure proper focus management
<Dialog>
	<DialogContent>
		{/* First focusable element receives focus */}
		<Input autoFocus />
	</DialogContent>
</Dialog>
```

### Screen Reader

```tsx
// Always include sr-only labels for icon-only buttons
<Button variant="ghost" size="icon">
  <Sun className="h-5 w-5" />
  <span className="sr-only">Toggle theme</span>
</Button>

// Use proper ARIA attributes
<Button aria-label="Close dialog" aria-pressed={isOpen}>
  <X className="h-4 w-4" />
</Button>
```

---

## Common Patterns

### Skeleton Loading

```tsx
import { Skeleton } from '@/components/ui/skeleton';

export function CardSkeleton() {
	return (
		<Card>
			<CardHeader>
				<Skeleton className="h-4 w-[250px]" />
				<Skeleton className="h-4 w-[200px]" />
			</CardHeader>
			<CardContent>
				<Skeleton className="h-[125px] w-full rounded-xl" />
			</CardContent>
		</Card>
	);
}
```

### Data Table

```tsx
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table';

<Table>
	<TableHeader>
		<TableRow>
			<TableHead>Name</TableHead>
			<TableHead>Email</TableHead>
			<TableHead className="text-right">Actions</TableHead>
		</TableRow>
	</TableHeader>
	<TableBody>
		{users.map((user) => (
			<TableRow key={user.id}>
				<TableCell className="font-medium">{user.name}</TableCell>
				<TableCell>{user.email}</TableCell>
				<TableCell className="text-right">
					<Button variant="ghost" size="sm">
						Edit
					</Button>
				</TableCell>
			</TableRow>
		))}
	</TableBody>
</Table>;
```

---

## Agent Integration

This skill is used by:

- **ui-mobile/tablet/desktop** agents
- **skeleton-generator** agent
- **design-system-enforcer** agent
- **accessibility-auditor** agent

---

## FORBIDDEN

1. **Override component internals** - Extend, don't modify
2. **Skip accessibility labels** - Always add sr-only/aria
3. **Inline styles over Tailwind** - Use className
4. **Ignore keyboard navigation** - Test all interactions
5. **Custom form validation** - Use react-hook-form + zod

---

## Version

- **v1.0.0** - Initial implementation based on shadcn/ui patterns

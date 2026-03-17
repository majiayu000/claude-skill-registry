---
name: shadcn
displayName: shadcn/ui
description: shadcn/ui component library patterns
version: 1.0.0
---

# shadcn/ui Development Guidelines

Best practices for using shadcn/ui components with Tailwind CSS and Radix UI primitives.

## Core Principles

1. **Copy, Don't Install**: Components are copied to your project, not installed as dependencies
2. **Customizable**: Modify components directly in your codebase
3. **Accessible**: Built on Radix UI primitives with ARIA support
4. **Type-Safe**: Full TypeScript support
5. **Composable**: Build complex UIs from simple primitives

## Installation

### Initial Setup

```bash
npx shadcn@latest init
```

### Add Components

```bash
# Add individual components
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add dialog

# Add multiple
npx shadcn@latest add button card dialog
```

### Troubleshooting

#### npm Cache Errors (ENOTEMPTY)

If `npx shadcn@latest add` fails with npm cache errors like `ENOTEMPTY` or `syscall rename`:

**Solution 1: Clear npm cache**
```bash
npm cache clean --force
npx shadcn@latest add table
```

**Solution 2: Use pnpm (recommended)**
```bash
pnpm dlx shadcn@latest add table
```

**Solution 3: Use yarn**
```bash
yarn dlx shadcn@latest add table
```

**Solution 4: Manual component installation**

Visit the [shadcn/ui documentation](https://ui.shadcn.com/docs/components) for the specific component and copy the code directly into your project.

## Component Usage

### Button & Card

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';

// Variants
<Button>Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>

// Card
<Card>
  <CardHeader>
    <CardTitle>{post.title}</CardTitle>
    <CardDescription>{post.author}</CardDescription>
  </CardHeader>
  <CardContent>
    <p>{post.excerpt}</p>
  </CardContent>
</Card>
```

### Dialog

```typescript
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

export function CreatePostDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Create Post</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Post</DialogTitle>
          <DialogDescription>
            Fill in the details below to create a new post.
          </DialogDescription>
        </DialogHeader>
        <PostForm />
      </DialogContent>
    </Dialog>
  );
}
```

## Forms

### Basic Form with react-hook-form

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

const formSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  content: z.string().min(10, 'Content must be at least 10 characters')
});

export function PostForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: '',
      content: ''
    }
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    console.log(values);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input placeholder="Post title" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="content"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Content</FormLabel>
              <FormControl>
                <Textarea placeholder="Write your post..." {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit">Create Post</Button>
      </form>
    </Form>
  );
}
```

### Select Field

```typescript
<FormField
  control={form.control}
  name="category"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Category</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select a category" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="tech">Technology</SelectItem>
          <SelectItem value="design">Design</SelectItem>
          <SelectItem value="business">Business</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Data Display

### Table

```typescript
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

export function PostsTable({ posts }: { posts: Post[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Title</TableHead>
          <TableHead>Author</TableHead>
          <TableHead>Status</TableHead>
          <TableHead className="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {posts.map((post) => (
          <TableRow key={post.id}>
            <TableCell className="font-medium">{post.title}</TableCell>
            <TableCell>{post.author.name}</TableCell>
            <TableCell>
              <Badge variant={post.published ? 'default' : 'secondary'}>
                {post.published ? 'Published' : 'Draft'}
              </Badge>
            </TableCell>
            <TableCell className="text-right">
              <Button variant="ghost" size="sm">Edit</Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

## Navigation

### Badge & Dropdown Menu

```typescript
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

export function UserMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost">
          <User className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>My Account</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem>Profile</DropdownMenuItem>
        <DropdownMenuItem>Settings</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem>Log out</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

### Tabs

```typescript
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export function PostTabs() {
  return (
    <Tabs defaultValue="published">
      <TabsList>
        <TabsTrigger value="published">Published</TabsTrigger>
        <TabsTrigger value="drafts">Drafts</TabsTrigger>
        <TabsTrigger value="archived">Archived</TabsTrigger>
      </TabsList>
      <TabsContent value="published">
        <PublishedPosts />
      </TabsContent>
      <TabsContent value="drafts">
        <DraftPosts />
      </TabsContent>
      <TabsContent value="archived">
        <ArchivedPosts />
      </TabsContent>
    </Tabs>
  );
}
```

## Feedback

### Toast

```typescript
'use client';

import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';

export function ToastExample() {
  const { toast } = useToast();

  return (
    <Button
      onClick={() => {
        toast({
          title: 'Post created',
          description: 'Your post has been published successfully.'
        });
      }}
    >
      Create Post
    </Button>
  );
}

// With variant
toast({
  variant: 'destructive',
  title: 'Error',
  description: 'Failed to create post. Please try again.'
});
```

### Alert

```typescript
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

export function AlertExample() {
  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>Error</AlertTitle>
      <AlertDescription>
        Your session has expired. Please log in again.
      </AlertDescription>
    </Alert>
  );
}
```

## Loading States

### Skeleton

```typescript
import { Skeleton } from '@/components/ui/skeleton';

export function PostCardSkeleton() {
  return (
    <div className="flex flex-col space-y-3">
      <Skeleton className="h-[125px] w-full rounded-xl" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-[250px]" />
        <Skeleton className="h-4 w-[200px]" />
      </div>
    </div>
  );
}
```

## Customization

### Modifying Components

Components are in your codebase - edit them directly:

```typescript
// components/ui/button.tsx
export const buttonVariants = cva(
  "inline-flex items-center justify-center...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        // Add custom variant
        brand: "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
      }
    }
  }
);
```

### Using Custom Variant

```typescript
<Button variant="brand">Custom Brand Button</Button>
```

## Theming

### CSS Variables (OKLCH Format)

shadcn/ui now uses OKLCH color format for better color accuracy and perceptual uniformity:

```css
/* app/globals.css */
@layer base {
  :root {
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --primary: oklch(0.205 0 0);
    --primary-foreground: oklch(0.985 0 0);
    /* ... */
  }

  .dark {
    --background: oklch(0.145 0 0);
    --foreground: oklch(0.985 0 0);
    --primary: oklch(0.598 0.15 264);
    --primary-foreground: oklch(0.205 0 0);
    /* ... */
  }
}
```

### Dark Mode

```typescript
// components/theme-toggle.tsx
'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { setTheme, theme } = useTheme();

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

## Composition Patterns

### Combining Components

```typescript
export function CreatePostCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Post</CardTitle>
        <CardDescription>Share your thoughts with the world</CardDescription>
      </CardHeader>
      <CardContent>
        <PostForm />
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline">Save Draft</Button>
        <Button>Publish</Button>
      </CardFooter>
    </Card>
  );
}
```

### Modal with Form

```typescript
export function CreatePostModal() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>New Post</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Create Post</DialogTitle>
        </DialogHeader>
        <PostForm onSuccess={() => setOpen(false)} />
      </DialogContent>
    </Dialog>
  );
}
```

## Additional Resources

For detailed information, see:
- [Component Catalog](resources/component-catalog.md)
- [Form Patterns](resources/form-patterns.md)
- [Theming Guide](resources/theming.md)

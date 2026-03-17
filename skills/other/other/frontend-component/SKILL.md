---
name: frontend-component
description: Generate React components for IntelliFill following patterns (forwardRef, CVA variants, Radix UI, TailwindCSS). Use when creating UI components, forms, or pages.
---

# Frontend Component Development Skill

This skill provides comprehensive guidance for creating React components in the IntelliFill frontend (`quikadmin-web/`).

## Table of Contents

1. [Component Architecture](#component-architecture)
2. [UI Component Pattern](#ui-component-pattern)
3. [CVA Variants](#cva-variants)
4. [Form Components](#form-components)
5. [Page Components](#page-components)
6. [Radix UI Integration](#radix-ui-integration)
7. [Styling with TailwindCSS](#styling-with-tailwindcss)
8. [Testing Components](#testing-components)

## Component Architecture

IntelliFill follows a clear component organization:

```
quikadmin-web/src/
├── components/
│   ├── ui/                    # Base UI components (shadcn-style)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── forms/                 # Form-specific components
│   │   ├── LoginForm.tsx
│   │   ├── RegistrationForm.tsx
│   │   └── ...
│   ├── layout/                # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── ...
│   └── [domain]/              # Feature-specific components
│       ├── DocumentCard.tsx
│       ├── TemplateList.tsx
│       └── ...
└── pages/                     # Page-level components
    ├── Dashboard.tsx
    ├── Documents.tsx
    └── ...
```

## UI Component Pattern

IntelliFill uses the shadcn/ui pattern for base components.

### Base Component Template

```tsx
// quikadmin-web/src/components/ui/button.tsx
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive:
          'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline:
          'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary:
          'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
```

### Input Component

```tsx
// quikadmin-web/src/components/ui/input.tsx
import * as React from 'react';
import { cn } from '@/lib/utils';

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  label?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, label, id, ...props }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-gray-700"
          >
            {label}
          </label>
        )}
        <input
          id={inputId}
          type={type}
          className={cn(
            'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
            error && 'border-red-500 focus-visible:ring-red-500',
            className
          )}
          ref={ref}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : undefined}
          {...props}
        />
        {error && (
          <p id={`${inputId}-error`} className="text-sm text-red-500">
            {error}
          </p>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input };
```

## CVA Variants

IntelliFill uses class-variance-authority (CVA) for variant management.

### CVA Pattern

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const cardVariants = cva(
  // Base styles (always applied)
  'rounded-lg border bg-card text-card-foreground shadow-sm',
  {
    variants: {
      // Variant definitions
      variant: {
        default: 'border-gray-200',
        elevated: 'border-gray-300 shadow-md',
        outlined: 'border-2 border-primary',
      },
      size: {
        sm: 'p-4',
        md: 'p-6',
        lg: 'p-8',
      },
      interactive: {
        true: 'cursor-pointer hover:shadow-lg transition-shadow',
        false: '',
      },
    },
    // Compound variants (combinations)
    compoundVariants: [
      {
        variant: 'elevated',
        interactive: true,
        class: 'hover:shadow-xl',
      },
    ],
    // Default values
    defaultVariants: {
      variant: 'default',
      size: 'md',
      interactive: false,
    },
  }
);

interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

export function Card({ className, variant, size, interactive, ...props }: CardProps) {
  return (
    <div
      className={cn(cardVariants({ variant, size, interactive }), className)}
      {...props}
    />
  );
}
```

### Using CVA in Components

```tsx
// Document card with variants
const documentCardVariants = cva(
  'flex flex-col gap-4 rounded-lg border p-4',
  {
    variants: {
      status: {
        pending: 'border-yellow-500 bg-yellow-50',
        processing: 'border-blue-500 bg-blue-50',
        completed: 'border-green-500 bg-green-50',
        failed: 'border-red-500 bg-red-50',
      },
      selected: {
        true: 'ring-2 ring-primary ring-offset-2',
        false: '',
      },
    },
    defaultVariants: {
      status: 'pending',
      selected: false,
    },
  }
);

interface DocumentCardProps extends VariantProps<typeof documentCardVariants> {
  document: Document;
  onClick?: () => void;
}

export function DocumentCard({ document, status, selected, onClick }: DocumentCardProps) {
  return (
    <div
      className={cn(documentCardVariants({ status, selected }))}
      onClick={onClick}
    >
      <h3>{document.name}</h3>
      <p>{document.description}</p>
    </div>
  );
}
```

## Form Components

IntelliFill forms use controlled components with validation.

### Form Pattern with React Hook Form

```tsx
// quikadmin-web/src/components/forms/DocumentUploadForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useDocumentStore } from '@/stores/documentStore';
import { toast } from 'sonner';

const formSchema = z.object({
  name: z.string().min(1, 'Name is required').max(255),
  description: z.string().max(1000).optional(),
  file: z.instanceof(File).refine((file) => file.size <= 10 * 1024 * 1024, {
    message: 'File must be less than 10MB',
  }),
});

type FormData = z.infer<typeof formSchema>;

export function DocumentUploadForm({ onSuccess }: { onSuccess?: () => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const { uploadDocument } = useDocumentStore();

  const onSubmit = async (data: FormData) => {
    try {
      await uploadDocument({
        name: data.name,
        description: data.description,
        file: data.file,
      });

      toast.success('Document uploaded successfully');
      reset();
      onSuccess?.();
    } catch (error) {
      toast.error('Failed to upload document');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Document Name"
        {...register('name')}
        error={errors.name?.message}
        placeholder="Enter document name"
      />

      <Input
        label="Description"
        {...register('description')}
        error={errors.description?.message}
        placeholder="Optional description"
      />

      <div>
        <label className="text-sm font-medium text-gray-700">File</label>
        <input
          type="file"
          {...register('file')}
          accept=".pdf,.png,.jpg,.jpeg"
          className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-primary-foreground hover:file:bg-primary/90"
        />
        {errors.file && (
          <p className="mt-1 text-sm text-red-500">{errors.file.message}</p>
        )}
      </div>

      <Button type="submit" disabled={isSubmitting} className="w-full">
        {isSubmitting ? 'Uploading...' : 'Upload Document'}
      </Button>
    </form>
  );
}
```

### Form with Custom Validation

```tsx
import { useState } from 'react';

export function LoginForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);
    try {
      // Your login logic
      await login(formData);
    } catch (error) {
      setErrors({ submit: 'Login failed. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        error={errors.email}
      />

      <Input
        label="Password"
        type="password"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        error={errors.password}
      />

      {errors.submit && <p className="text-sm text-red-500">{errors.submit}</p>}

      <Button type="submit" disabled={isLoading} className="w-full">
        {isLoading ? 'Signing in...' : 'Sign In'}
      </Button>
    </form>
  );
}
```

## Page Components

Page components are route-level components that compose smaller components.

### Page Template

```tsx
// quikadmin-web/src/pages/Documents.tsx
import { useEffect } from 'react';
import { useDocumentStore } from '@/stores/documentStore';
import { DocumentCard } from '@/components/documents/DocumentCard';
import { DocumentUploadForm } from '@/components/forms/DocumentUploadForm';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog';
import { Loader2 } from 'lucide-react';

export function DocumentsPage() {
  const { documents, loading, error, fetchDocuments } = useDocumentStore();
  const [uploadOpen, setUploadOpen] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Documents</h1>
        <Dialog open={uploadOpen} onOpenChange={setUploadOpen}>
          <DialogTrigger asChild>
            <Button>Upload Document</Button>
          </DialogTrigger>
          <DialogContent>
            <DocumentUploadForm onSuccess={() => setUploadOpen(false)} />
          </DialogContent>
        </Dialog>
      </div>

      {/* Document Grid */}
      {documents.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No documents yet. Upload your first one!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {documents.map((doc) => (
            <DocumentCard key={doc.id} document={doc} />
          ))}
        </div>
      )}
    </div>
  );
}
```

## Radix UI Integration

IntelliFill uses Radix UI primitives for accessible components.

### Dialog Component

```tsx
// quikadmin-web/src/components/ui/dialog.tsx
import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogPortal = DialogPrimitive.Portal;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      'fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg',
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = DialogPrimitive.Content.displayName;

export { Dialog, DialogTrigger, DialogContent };
```

### Dropdown Menu

```tsx
import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';
import { MoreVertical } from 'lucide-react';

export function DocumentActions({ document }) {
  return (
    <DropdownMenuPrimitive.Root>
      <DropdownMenuPrimitive.Trigger asChild>
        <button className="rounded p-2 hover:bg-gray-100">
          <MoreVertical className="h-4 w-4" />
        </button>
      </DropdownMenuPrimitive.Trigger>

      <DropdownMenuPrimitive.Portal>
        <DropdownMenuPrimitive.Content
          className="min-w-[220px] rounded-md border bg-white p-1 shadow-md"
          sideOffset={5}
        >
          <DropdownMenuPrimitive.Item
            className="cursor-pointer rounded px-3 py-2 text-sm hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
            onSelect={() => handleEdit(document)}
          >
            Edit
          </DropdownMenuPrimitive.Item>
          <DropdownMenuPrimitive.Item
            className="cursor-pointer rounded px-3 py-2 text-sm hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
            onSelect={() => handleDownload(document)}
          >
            Download
          </DropdownMenuPrimitive.Item>
          <DropdownMenuPrimitive.Separator className="my-1 h-px bg-gray-200" />
          <DropdownMenuPrimitive.Item
            className="cursor-pointer rounded px-3 py-2 text-sm text-red-500 hover:bg-red-50 focus:bg-red-50 focus:outline-none"
            onSelect={() => handleDelete(document)}
          >
            Delete
          </DropdownMenuPrimitive.Item>
        </DropdownMenuPrimitive.Content>
      </DropdownMenuPrimitive.Portal>
    </DropdownMenuPrimitive.Root>
  );
}
```

## Styling with TailwindCSS

IntelliFill uses TailwindCSS 4.0 with custom design tokens.

### Design Tokens

```typescript
// quikadmin-web/tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
      },
    },
  },
};
```

### cn() Utility

```typescript
// quikadmin-web/src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge class names with Tailwind CSS conflict resolution
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Responsive Patterns

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols */}
</div>

<div className="flex flex-col lg:flex-row gap-4">
  {/* Mobile: vertical, Desktop: horizontal */}
</div>

<button className="w-full sm:w-auto">
  {/* Full width on mobile, auto on larger screens */}
</button>
```

## Testing Components

### Vitest Component Test

```tsx
// quikadmin-web/src/components/__tests__/DocumentCard.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DocumentCard } from '../documents/DocumentCard';

describe('DocumentCard', () => {
  const mockDocument = {
    id: '1',
    name: 'Test Document',
    description: 'Test description',
    status: 'completed',
  };

  it('renders document information', () => {
    render(<DocumentCard document={mockDocument} />);

    expect(screen.getByText('Test Document')).toBeInTheDocument();
    expect(screen.getByText('Test description')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const onClick = vi.fn();
    render(<DocumentCard document={mockDocument} onClick={onClick} />);

    fireEvent.click(screen.getByText('Test Document'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('applies correct status variant', () => {
    const { container } = render(
      <DocumentCard document={mockDocument} status="completed" />
    );

    const card = container.firstChild;
    expect(card).toHaveClass('border-green-500');
  });
});
```

## Best Practices

1. **Use forwardRef for UI components** - Enables ref forwarding and composition
2. **Type all props** - Use TypeScript interfaces for all component props
3. **Use CVA for variants** - Consistent variant management
4. **Accessibility first** - Use Radix UI primitives and ARIA attributes
5. **Responsive by default** - Design for mobile first
6. **Use cn() utility** - Merge class names safely
7. **Error boundaries** - Wrap components in error boundaries
8. **Loading states** - Always show loading indicators
9. **Empty states** - Handle empty data gracefully
10. **Test interactivity** - Test user interactions and edge cases

## References

- [React Documentation](https://react.dev/)
- [Radix UI](https://www.radix-ui.com/)
- [TailwindCSS](https://tailwindcss.com/)
- [CVA Documentation](https://cva.style/docs)
- [React Hook Form](https://react-hook-form.com/)
- [Vitest](https://vitest.dev/)

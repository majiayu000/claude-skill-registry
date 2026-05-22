---
name: frontend-design-systems
description: Systematic approach to building consistent, maintainable frontend UI components with design systems and component libraries
license: MIT
metadata:
  adapted-by: ai-skills
  category: frontend-development
---

# Frontend Design Systems

Build consistent, scalable UI components with systematic design patterns.

## Design Token System

### Color Tokens

```typescript
// tokens/colors.ts
export const colors = {
  primary: {
    50: '#e3f2fd',
    100: '#bbdefb',
    500: '#2196f3',
    900: '#0d47a1',
  },
  neutral: {
    50: '#fafafa',
    100: '#f5f5f5',
    500: '#9e9e9e',
    900: '#212121',
  },
  semantic: {
    success: '#4caf50',
    warning: '#ff9800',
    error: '#f44336',
    info: '#2196f3',
  }
};
```

### Spacing Scale

```typescript
export const spacing = {
  xs: '0.25rem',  // 4px
  sm: '0.5rem',   // 8px
  md: '1rem',     // 16px
  lg: '1.5rem',   // 24px
  xl: '2rem',     // 32px
  '2xl': '3rem',  // 48px
};
```

### Typography System

```typescript
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['Fira Code', 'monospace'],
  },
  fontSize: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  }
};
```

## Component Patterns

### Base Button Component

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  children,
  onClick,
}: ButtonProps) {
  const variants = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600',
    secondary: 'bg-neutral-200 text-neutral-900 hover:bg-neutral-300',
    outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50',
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button
      className={`rounded-lg font-medium transition-colors ${variants[variant]} ${sizes[size]}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
}
```

### Compound Components

```typescript
// Card compound component pattern
export function Card({ children }: { children: React.ReactNode }) {
  return <div className="rounded-lg border shadow-sm">{children}</div>;
}

Card.Header = function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="px-6 py-4 border-b">{children}</div>;
};

Card.Body = function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="px-6 py-4">{children}</div>;
};

Card.Footer = function CardFooter({ children }: { children: React.ReactNode }) {
  return <div className="px-6 py-4 border-t bg-neutral-50">{children}</div>;
};

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

## Layout Patterns

### Responsive Grid System

```typescript
function GridLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {children}
    </div>
  );
}
```

### Container Pattern

```typescript
function Container({ children }: { children: React.ReactNode }) {
  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
      {children}
    </div>
  );
}
```

## State Management Patterns

### Form State

```typescript
function useForm<T>(initialValues: T) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  
  const handleChange = (name: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: undefined }));
  };
  
  const validate = (schema: z.ZodSchema<T>) => {
    const result = schema.safeParse(values);
    if (!result.success) {
      const fieldErrors = result.error.formErrors.fieldErrors;
      setErrors(fieldErrors as any);
      return false;
    }
    return true;
  };
  
  return { values, errors, handleChange, validate };
}
```

## Accessibility Patterns

```typescript
// Focus management
function Dialog({ open, onClose, children }: DialogProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (open) {
      dialogRef.current?.focus();
    }
  }, [open]);
  
  return (
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={(e) => {
        if (e.key === 'Escape') onClose();
      }}
    >
      {children}
    </div>
  );
}
```

## Integration Points

Complements:
- **canvas-design**: For design integration
- **accessibility-patterns**: For ARIA/WCAG
- **responsive-design-patterns**: For mobile-first
- **testing-patterns**: For component testing

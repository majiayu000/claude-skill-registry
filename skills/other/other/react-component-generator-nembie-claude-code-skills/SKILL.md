---
name: react-component-generator
description: Generate modern React components with TypeScript, hooks, and accessibility. Use when asked to create React components, UI components, scaffold frontend elements, or build reusable UI.
---

# React Component Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Generation Process

1. Determine component type and requirements
2. Generate TypeScript props interface
3. Create functional component with hooks
4. Add accessibility attributes
5. Include keyboard navigation where applicable

## Component Types

### Data Display Component
```typescript
interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  onRowClick?: (item: T) => void;
  loading?: boolean;
  emptyMessage?: string;
}

function DataTable<T extends { id: string | number }>({
  data,
  columns,
  onRowClick,
  loading = false,
  emptyMessage = 'No data available',
}: DataTableProps<T>) {
  if (loading) {
    return <div role="status" aria-busy="true">Loading...</div>;
  }

  if (data.length === 0) {
    return <div role="status">{emptyMessage}</div>;
  }

  return (
    <table role="grid" aria-rowcount={data.length}>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} scope="col">{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr
            key={item.id}
            onClick={() => onRowClick?.(item)}
            onKeyDown={(e) => e.key === 'Enter' && onRowClick?.(item)}
            tabIndex={onRowClick ? 0 : undefined}
            role={onRowClick ? 'button' : undefined}
            aria-rowindex={index + 1}
          >
            {columns.map((col) => (
              <td key={col.key}>{col.render(item)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Form Component
```typescript
interface FormFieldProps {
  label: string;
  name: string;
  type?: 'text' | 'email' | 'password' | 'number';
  value: string;
  onChange: (value: string) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

function FormField({
  label,
  name,
  type = 'text',
  value,
  onChange,
  error,
  required = false,
  disabled = false,
  placeholder,
}: FormFieldProps) {
  const id = `field-${name}`;
  const errorId = `${id}-error`;

  return (
    <div className="form-field">
      <label htmlFor={id}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
      </label>
      <input
        id={id}
        name={name}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder={placeholder}
        required={required}
        aria-required={required}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
      />
      {error && (
        <span id={errorId} role="alert" className="error">
          {error}
        </span>
      )}
    </div>
  );
}
```

### Modal/Dialog Component
```typescript
interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
}

function Modal({ open, onClose, title, children, actions }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (open) {
      previousFocus.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [open]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && open) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal"
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
      >
        <header>
          <h2 id="modal-title">{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close dialog"
            className="close-button"
          >
            ×
          </button>
        </header>
        <div className="modal-content">{children}</div>
        {actions && <footer className="modal-actions">{actions}</footer>}
      </div>
    </div>
  );
}
```

### Layout Component
```typescript
interface PageLayoutProps {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
}

function PageLayout({ children, sidebar, header, footer }: PageLayoutProps) {
  return (
    <div className="page-layout">
      {header && <header role="banner">{header}</header>}
      <div className="page-body">
        {sidebar && <aside role="complementary">{sidebar}</aside>}
        <main role="main">{children}</main>
      </div>
      {footer && <footer role="contentinfo">{footer}</footer>}
    </div>
  );
}
```

### Button Component
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      leftIcon,
      rightIcon,
      disabled,
      children,
      className,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={`btn btn-${variant} btn-${size} ${className ?? ''}`}
        disabled={disabled || loading}
        aria-busy={loading}
        {...props}
      >
        {loading ? (
          <span aria-hidden="true" className="spinner" />
        ) : (
          leftIcon
        )}
        <span>{children}</span>
        {!loading && rightIcon}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

## Composable Patterns

### Compound Components
```typescript
interface SelectContextValue {
  value: string;
  onChange: (value: string) => void;
}

const SelectContext = createContext<SelectContextValue | null>(null);

function Select({ value, onChange, children }: {
  value: string;
  onChange: (value: string) => void;
  children: React.ReactNode;
}) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div role="listbox">{children}</div>
    </SelectContext.Provider>
  );
}

function Option({ value, children }: { value: string; children: React.ReactNode }) {
  const ctx = useContext(SelectContext);
  if (!ctx) throw new Error('Option must be used within Select');

  const selected = ctx.value === value;

  return (
    <div
      role="option"
      aria-selected={selected}
      onClick={() => ctx.onChange(value)}
      onKeyDown={(e) => e.key === 'Enter' && ctx.onChange(value)}
      tabIndex={0}
    >
      {children}
    </div>
  );
}

Select.Option = Option;
```

### Render Props
```typescript
interface ToggleRenderProps {
  on: boolean;
  toggle: () => void;
  setOn: () => void;
  setOff: () => void;
}

interface ToggleProps {
  initialOn?: boolean;
  children: (props: ToggleRenderProps) => React.ReactNode;
}

function Toggle({ initialOn = false, children }: ToggleProps) {
  const [on, setOn] = useState(initialOn);

  const renderProps: ToggleRenderProps = {
    on,
    toggle: () => setOn((prev) => !prev),
    setOn: () => setOn(true),
    setOff: () => setOn(false),
  };

  return <>{children(renderProps)}</>;
}
```

## Accessibility Checklist

- [ ] Semantic HTML elements (button, nav, main, etc.)
- [ ] ARIA roles where semantic HTML insufficient
- [ ] aria-label or aria-labelledby for non-text content
- [ ] aria-describedby for error messages
- [ ] Focus management (modals, dynamic content)
- [ ] Keyboard navigation (Enter, Escape, Arrow keys)
- [ ] Visible focus indicators
- [ ] Color contrast (don't rely on color alone)
- [ ] Loading states announced (aria-busy, role="status")
- [ ] Error states announced (role="alert")

## Completeness Check

After generating a component, verify completeness: does it export a TypeScript props interface? Does it handle the loading/error/empty states if it fetches data? Do interactive elements have keyboard handlers and aria attributes? If any check fails, fix the component before delivering.

## Asset

See `assets/component-template/Component.tsx` for a minimal starter template.

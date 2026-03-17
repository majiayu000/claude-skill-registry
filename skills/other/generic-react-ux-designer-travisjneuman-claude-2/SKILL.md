---
name: generic-react-ux-designer
description: Professional UI/UX design expertise for React applications. Covers design thinking, user psychology (Hick's/Fitts's/Jakob's Law), visual hierarchy, interaction patterns, accessibility, performance-driven design, and design critique. Use when designing features, improving UX, solving user problems, or conducting design reviews.
---

# React UX Designer

Professional UX expertise for React/TypeScript applications.

**Extends:** [Generic UX Designer](../generic-ux-designer/SKILL.md) - Read base skill for design thinking process, user psychology, heuristic evaluation, and research methods.

## React Interaction Patterns

### Micro-interactions with Framer Motion

```tsx
// Checkbox animation
<motion.div
  animate={{ scale: checked ? 1 : 0 }}
  transition={{ type: "spring", stiffness: 500 }}
>
  <Check className="w-4 h-4" />
</motion.div>

// Button press feedback
<motion.button
  whileTap={{ scale: 0.98 }}
  whileHover={{ scale: 1.02 }}
  transition={{ type: "spring", stiffness: 400 }}
>
  Click me
</motion.button>

// Toast notification
<motion.div
  initial={{ opacity: 0, y: 50 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: 50 }}
>
  <Toast message={message} />
</motion.div>
```

### Loading States

```tsx
// Skeleton (preferred over spinners)
<div className="animate-pulse space-y-4">
  <div className="h-8 bg-slate-200 rounded w-3/4" />
  <div className="h-4 bg-slate-200 rounded" />
</div>

// Progress indicator for long operations
<div className="relative w-full h-2 bg-slate-200 rounded">
  <motion.div
    className="absolute h-full bg-primary rounded"
    initial={{ width: 0 }}
    animate={{ width: `${progress}%` }}
  />
</div>
```

### Optimistic UI Pattern

```tsx
const handleLike = async () => {
  // Update UI immediately
  setLiked(true);
  setCount((c) => c + 1);

  try {
    await api.like(id);
  } catch {
    // Rollback on error
    setLiked(false);
    setCount((c) => c - 1);
    toast.error("Failed to save");
  }
};
```

## React Accessibility Patterns

### Focus Management

```tsx
// Modal focus trap
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      const firstFocusable = modalRef.current?.querySelector(
        "button, [href], input, select, textarea",
      ) as HTMLElement;
      firstFocusable?.focus();
    }
  }, [isOpen]);

  // Trap focus within modal
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Tab") {
      const focusables = modalRef.current?.querySelectorAll(
        "button, [href], input, select, textarea",
      );
      // Handle tab cycling...
    }
    if (e.key === "Escape") onClose();
  };

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
```

### Keyboard Navigation

```tsx
// Custom keyboard shortcut
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {
      e.preventDefault();
      openCommandPalette();
    }
  };
  window.addEventListener("keydown", handleKeyDown);
  return () => window.removeEventListener("keydown", handleKeyDown);
}, []);

// Arrow key navigation in list
const handleKeyDown = (e: KeyboardEvent, index: number) => {
  switch (e.key) {
    case "ArrowDown":
      e.preventDefault();
      focusItem(index + 1);
      break;
    case "ArrowUp":
      e.preventDefault();
      focusItem(index - 1);
      break;
  }
};
```

### Motion Accessibility

```tsx
// Respect prefers-reduced-motion
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)",
).matches;

<motion.div
  initial={{ opacity: 0, y: prefersReducedMotion ? 0 : 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
/>;
```

## Form UX Patterns

### React Hook Form Integration

```tsx
function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-1">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          {...register("email", { required: "Email is required" })}
          aria-invalid={errors.email ? "true" : "false"}
          aria-describedby={errors.email ? "email-error" : undefined}
          className={cn("input", errors.email && "border-red-500")}
        />
        {errors.email && (
          <p id="email-error" className="text-sm text-red-500">
            {errors.email.message}
          </p>
        )}
      </div>
    </form>
  );
}
```

### Inline Validation

```tsx
// Validate on blur, show on focus
const [touched, setTouched] = useState(false);
const [error, setError] = useState("");

<input
  onBlur={() => {
    setTouched(true);
    setError(validate(value));
  }}
  onFocus={() => setError("")} // Clear while editing
  className={touched && error ? "border-red-500" : ""}
/>;
```

## Modal/Dialog Patterns

### Confirmation Dialog

```tsx
function ConfirmDialog({ isOpen, onConfirm, onCancel, title, message }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    >
      <motion.div
        initial={{ scale: 0.95 }}
        animate={{ scale: 1 }}
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        aria-describedby="dialog-desc"
        className="bg-white rounded-xl p-6 max-w-md"
      >
        <h2 id="dialog-title" className="text-lg font-semibold">
          {title}
        </h2>
        <p id="dialog-desc" className="mt-2 text-muted">
          {message}
        </p>
        <div className="mt-4 flex gap-3 justify-end">
          <button onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
          <button onClick={onConfirm} className="btn-primary">
            Confirm
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}
```

### Command Palette (⌘K Pattern)

```tsx
function CommandPalette({ isOpen, onClose }: Props) {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) inputRef.current?.focus();
  }, [isOpen]);

  const filtered = useMemo(
    () =>
      commands.filter((c) =>
        c.label.toLowerCase().includes(query.toLowerCase()),
      ),
    [query],
  );

  return (
    <div role="dialog" aria-label="Command palette">
      <input
        ref={inputRef}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type a command..."
        aria-autocomplete="list"
      />
      <ul role="listbox">
        {filtered.map((cmd) => (
          <li key={cmd.id} role="option">
            {cmd.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Empty & Error States

```tsx
// Empty state with action
function EmptyState({ title, description, action }: Props) {
  return (
    <div className="text-center py-12">
      <Icon className="mx-auto h-12 w-12 text-muted" />
      <h3 className="mt-4 text-lg font-medium">{title}</h3>
      <p className="mt-2 text-muted">{description}</p>
      <button onClick={action.onClick} className="mt-4 btn-primary">
        {action.label}
      </button>
    </div>
  );
}

// Error state with retry
function ErrorState({ error, onRetry }: Props) {
  return (
    <div className="text-center py-12" role="alert">
      <AlertCircle className="mx-auto h-12 w-12 text-red-500" />
      <h3 className="mt-4 text-lg font-medium">Something went wrong</h3>
      <p className="mt-2 text-muted">{error.message}</p>
      <button onClick={onRetry} className="mt-4 btn-primary">
        Try again
      </button>
    </div>
  );
}
```

## React UX Checklist

**Interaction Quality:**

- [ ] Immediate feedback on user actions
- [ ] Loading states for async operations
- [ ] Optimistic updates where appropriate
- [ ] Smooth animations (60fps)

**Accessibility:**

- [ ] Keyboard navigation complete
- [ ] Focus management in modals
- [ ] Motion respects prefers-reduced-motion
- [ ] ARIA labels on interactive elements

**Forms:**

- [ ] Inline validation
- [ ] Clear error messages
- [ ] Smart defaults
- [ ] Progress indication for multi-step

## See Also

- [Generic UX Designer](../generic-ux-designer/SKILL.md) - Design thinking, psychology
- [UX Principles](../_shared/UX_PRINCIPLES.md) - Research methods, heuristics
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual patterns

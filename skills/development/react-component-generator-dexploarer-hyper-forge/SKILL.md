---
name: react-component-generator
description: Generates modern React components with TypeScript, hooks, proper props typing, and best practices. Use when creating React components or scaffolding UI elements.
---

# React Component Generator Skill

You are an expert at creating modern React components following current best practices.

## When to Activate

- User asks to "create a React component"
- User says "generate a [ComponentName] component"
- User requests "scaffold React UI for [feature]"
- User wants to "build a [component type] in React"

## Component Generation Process

### 1. Gather Requirements

Ask clarifying questions if not provided:
- Component name (PascalCase)
- Component purpose and functionality
- Props needed and their types
- State requirements
- Side effects or data fetching
- Styling approach (CSS Modules, Styled Components, Tailwind)
- Testing requirements

### 2. Create Component File Structure

```typescript
// ComponentName.tsx
import React, { useState, useEffect, useCallback } from 'react';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  title: string;
  onAction?: () => void;
  items?: Item[];
  className?: string;
  children?: React.ReactNode;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  onAction,
  items = [],
  className = '',
  children,
}) => {
  // State
  const [isLoading, setIsLoading] = useState(false);

  // Effects
  useEffect(() => {
    // Side effects here
  }, [dependencies]);

  // Handlers
  const handleClick = useCallback(() => {
    if (onAction) {
      onAction();
    }
  }, [onAction]);

  // Render
  return (
    <div className={`${styles.container} ${className}`}>
      <h2 className={styles.title}>{title}</h2>
      {isLoading ? (
        <div className={styles.loading}>Loading...</div>
      ) : (
        <div className={styles.content}>
          {children}
        </div>
      )}
    </div>
  );
};

ComponentName.displayName = 'ComponentName';
```

### 3. Create Associated Files

**Styles File (ComponentName.module.css):**
```css
.container {
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: var(--background);
}

.title {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.content {
  /* Content styles */
}

.loading {
  display: flex;
  justify-content: center;
  padding: 2rem;
}
```

**Test File (ComponentName.test.tsx):**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders with required props', () => {
    render(<ComponentName title="Test Title" />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('calls onAction when clicked', () => {
    const handleAction = jest.fn();
    render(<ComponentName title="Test" onAction={handleAction} />);

    fireEvent.click(screen.getByRole('button'));
    expect(handleAction).toHaveBeenCalledTimes(1);
  });
});
```

**Barrel Export (index.ts):**
```typescript
export { ComponentName } from './ComponentName';
export type { ComponentNameProps } from './ComponentName';
```

### 4. Best Practices to Follow

**TypeScript:**
- Use proper prop types with interface
- Export prop types for reusability
- Use React.FC for type safety
- Define event handler types correctly

**Component Structure:**
- Props destructuring with defaults
- Hooks at top (useState, useEffect, etc.)
- Helper functions and handlers
- Return JSX
- Set displayName for debugging

**Performance:**
- Use useCallback for functions passed as props
- Use useMemo for expensive calculations
- Implement proper dependency arrays
- Consider React.memo for expensive components

**Accessibility:**
- Use semantic HTML elements
- Add ARIA labels where needed
- Ensure keyboard navigation works
- Maintain proper heading hierarchy

**File Organization:**
```
ComponentName/
├── ComponentName.tsx       # Component logic
├── ComponentName.module.css # Styles
├── ComponentName.test.tsx  # Tests
├── ComponentName.stories.tsx # Storybook (optional)
└── index.ts               # Barrel export
```

## Component Patterns

### Simple Presentational Component
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false,
}) => (
  <button
    className={styles[variant]}
    onClick={onClick}
    disabled={disabled}
  >
    {label}
  </button>
);
```

### Container with Data Fetching
```typescript
export const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('/api/users');
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <ul>
      {users.map(user => (
        <UserListItem key={user.id} user={user} />
      ))}
    </ul>
  );
};
```

### Form Component with Validation
```typescript
interface FormData {
  email: string;
  password: string;
}

export const LoginForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Partial<FormData>>({});

  const validate = (): boolean => {
    const newErrors: Partial<FormData> = {};

    if (!formData.email.includes('@')) {
      newErrors.email = 'Invalid email';
    }

    if (formData.password.length < 8) {
      newErrors.password = 'Password too short';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      // Submit form
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
      />
      {errors.email && <span className={styles.error}>{errors.email}</span>}

      <button type="submit">Login</button>
    </form>
  );
};
```

## Output Format

After creating component, provide:
1. ✅ Component file created at [path]
2. ✅ Styles file created at [path]
3. ✅ Test file created at [path]
4. ✅ Index export created at [path]
5. 📝 Usage example
6. 🔍 Next steps (add to parent, style further, etc.)

## Remember

- Always use TypeScript
- Include proper prop types
- Add basic tests
- Follow React best practices
- Use hooks correctly
- Make components reusable
- Consider accessibility
- Keep components focused and single-purpose

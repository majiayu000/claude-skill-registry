---
name: react-typescript
description: TypeScript expertise for React/Next.js development. Use when writing React components with strict typing, fixing TypeScript errors, handling generic components, or working with TanStack Query types. Focuses on common pitfalls and advanced patterns.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [frontend-development, test-writer, code-review]
  must_serialize_with: []
  preferred_batch_size: 5
context_hints:
  max_file_context: 60
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "module.*augmentation"
    reason: "Module augmentation has global impact"
  - pattern: "third-party.*conflict"
    reason: "Third-party library type conflicts need investigation"
  - keyword: ["complex generic", "performance"]
    reason: "Complex type patterns may need expert review"
---

# React TypeScript Skill

Expert TypeScript patterns for React and Next.js development, focusing on strict type safety, common error resolutions, and advanced patterns used in this project.

## When This Skill Activates

- TypeScript compilation errors in React components
- Writing new React components with proper typing
- Handling generic components and hooks
- Working with TanStack Query type inference
- Fixing `any` type issues
- JSX-specific TypeScript patterns

## Project Context

This project uses:
- Next.js 14.x with App Router
- React 18.x
- TypeScript 5.x (strict mode)
- TanStack Query 5.x
- TailwindCSS 3.x
- lucide-react for icons

## Common TypeScript Errors & Fixes

### 1. Cannot Find Module 'react'

**Error:**
```
error TS2307: Cannot find module 'react' or its corresponding type declarations.
```

**Cause:** Missing `@types/react` or corrupted `node_modules`

**Fix:**
```bash
cd /home/user/Autonomous-Assignment-Program-Manager/frontend
rm -rf node_modules package-lock.json
npm install
```

### 2. Parameter Implicitly Has 'any' Type

**Error:**
```
error TS7006: Parameter 'e' implicitly has an 'any' type.
```

**Bad:**
```typescript
const handleChange = (e) => {
  setValue(e.target.value);
};
```

**Good:**
```typescript
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// For form submissions
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

// For keyboard events
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') submit();
};
```

### 3. JSX Element Implicitly Has 'any' Type

**Error:**
```
error TS7026: JSX element implicitly has type 'any' because no interface 'JSX.IntrinsicElements' exists.
```

**Cause:** Missing React types or incorrect tsconfig

**Fix:** Ensure `tsconfig.json` includes:
```json
{
  "compilerOptions": {
    "jsx": "preserve",
    "lib": ["dom", "dom.iterable", "esnext"]
  }
}
```

### 4. Type 'unknown' Not Assignable to 'ReactNode'

**Error:**
```
error TS2322: Type 'unknown' is not assignable to type 'ReactNode'.
```

**Bad:**
```typescript
const data = useQuery(...);
return <div>{data.value}</div>; // value is unknown
```

**Good:**
```typescript
interface ResponseData {
  value: string;
}

const { data } = useQuery<ResponseData>({
  queryKey: ['key'],
  queryFn: fetchData,
});

return <div>{data?.value}</div>;
```

### 5. Property Does Not Exist on Type

**Error:**
```
error TS2339: Property 'role' does not exist on type 'Person'.
```

**Fix:** Extend the type or use type assertion:
```typescript
// Option 1: Extend the interface
interface Person {
  id: string;
  name: string;
}

interface PersonWithRole extends Person {
  role: string;
}

// Option 2: Use intersection type
type PersonWithRole = Person & { role: string };

// Option 3: Add to original interface (if you control it)
interface Person {
  id: string;
  name: string;
  role?: string; // Optional if not always present
}
```

### 6. Generic Component Type Issues

**Error:**
```
error TS2322: Type 'NoInfer<TQueryFnData>' is not assignable to type...
```

**Bad:**
```typescript
const { data } = useQuery({
  queryKey: ['residents'],
  queryFn: async () => {
    const res = await fetch('/api/residents');
    return res.json(); // Returns unknown
  },
});

// data is TQueryFnData, not your type
```

**Good:**
```typescript
interface Resident {
  id: string;
  name: string;
  specialty: string;
}

const { data } = useQuery<Resident[]>({
  queryKey: ['residents'],
  queryFn: async (): Promise<Resident[]> => {
    const res = await fetch('/api/residents');
    return res.json();
  },
});

// data is now Resident[] | undefined
```

### 7. Index Signature Issues

**Error:**
```
error TS7053: Element implicitly has an 'any' type because expression of type 'string' can't be used to index type
```

**Bad:**
```typescript
interface Metrics {
  cpu: number;
  memory: number;
}

const metrics: Metrics = { cpu: 80, memory: 60 };
const key = 'cpu';
const value = metrics[key]; // Error: string can't index Metrics
```

**Good:**
```typescript
// Option 1: Use keyof
const key: keyof Metrics = 'cpu';
const value = metrics[key]; // Works

// Option 2: Add index signature
interface Metrics {
  cpu: number;
  memory: number;
  [key: string]: number;
}

// Option 3: Type assertion (last resort)
const value = metrics[key as keyof Metrics];
```

## Component Patterns

### Typed Component Props

```typescript
// Always define explicit interfaces
interface ScheduleViewProps {
  scheduleId: string;
  onUpdate?: (schedule: Schedule) => void;
  className?: string;
  children?: React.ReactNode;
}

// Use React.FC or explicit return type
export const ScheduleView: React.FC<ScheduleViewProps> = ({
  scheduleId,
  onUpdate,
  className,
  children,
}) => {
  // ...
};

// Alternative: function declaration with explicit types
export function ScheduleView({
  scheduleId,
  onUpdate,
  className,
  children,
}: ScheduleViewProps): React.ReactElement {
  // ...
}
```

### Generic Components

```typescript
// For reusable components with type parameters
interface SelectProps<T> {
  options: T[];
  value: T | null;
  onChange: (value: T) => void;
  getLabel: (option: T) => string;
  getValue: (option: T) => string;
}

// Use trailing comma to disambiguate from JSX in .tsx files
export function Select<T,>({
  options,
  value,
  onChange,
  getLabel,
  getValue,
}: SelectProps<T>): React.ReactElement {
  return (
    <select
      value={value ? getValue(value) : ''}
      onChange={(e) => {
        const selected = options.find(o => getValue(o) === e.target.value);
        if (selected) onChange(selected);
      }}
    >
      {options.map((option) => (
        <option key={getValue(option)} value={getValue(option)}>
          {getLabel(option)}
        </option>
      ))}
    </select>
  );
}
```

### Discriminated Unions for Props

```typescript
// Use discriminated unions for mutually exclusive props
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; onClick: () => void; href?: never };

interface BaseButtonProps {
  children: React.ReactNode;
  className?: string;
}

export function Button(props: BaseButtonProps & ButtonProps) {
  if (props.variant === 'link') {
    return <a href={props.href} className={props.className}>{props.children}</a>;
  }
  return <button onClick={props.onClick} className={props.className}>{props.children}</button>;
}
```

## Hook Patterns

### Typed useState

```typescript
// Explicit type when inference isn't enough
const [schedule, setSchedule] = useState<Schedule | null>(null);

// For arrays, be explicit
const [items, setItems] = useState<Assignment[]>([]);

// For objects with nullable fields
interface FormState {
  name: string;
  date: Date | null;
  error?: string;
}
const [form, setForm] = useState<FormState>({
  name: '',
  date: null,
});
```

### Typed useRef

```typescript
// For DOM elements
const inputRef = useRef<HTMLInputElement>(null);

// For mutable values
const timerRef = useRef<NodeJS.Timeout | null>(null);

// For imperative handles
interface ScheduleHandle {
  refresh: () => void;
  scrollToDate: (date: Date) => void;
}
const scheduleRef = useRef<ScheduleHandle>(null);
```

### Typed Custom Hooks

```typescript
interface UseScheduleOptions {
  autoRefresh?: boolean;
  refreshInterval?: number;
}

interface UseScheduleReturn {
  schedule: Schedule | null;
  isLoading: boolean;
  error: Error | null;
  refresh: () => void;
}

export function useSchedule(
  scheduleId: string,
  options: UseScheduleOptions = {}
): UseScheduleReturn {
  const { autoRefresh = false, refreshInterval = 30000 } = options;

  // Implementation...

  return { schedule, isLoading, error, refresh };
}
```

## TanStack Query Patterns

### Typed Queries

```typescript
// Define return types explicitly
interface ScheduleResponse {
  id: string;
  assignments: Assignment[];
  metadata: ScheduleMetadata;
}

export function useScheduleQuery(scheduleId: string) {
  return useQuery<ScheduleResponse, Error>({
    queryKey: ['schedule', scheduleId],
    queryFn: async (): Promise<ScheduleResponse> => {
      const res = await fetch(`/api/schedules/${scheduleId}`);
      if (!res.ok) throw new Error('Failed to fetch schedule');
      return res.json();
    },
    staleTime: 5 * 60 * 1000,
  });
}
```

### Typed Mutations

```typescript
interface UpdateScheduleVariables {
  scheduleId: string;
  data: Partial<Schedule>;
}

export function useUpdateSchedule() {
  const queryClient = useQueryClient();

  return useMutation<Schedule, Error, UpdateScheduleVariables>({
    mutationFn: async ({ scheduleId, data }) => {
      const res = await fetch(`/api/schedules/${scheduleId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Update failed');
      return res.json();
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['schedule', variables.scheduleId] });
    },
  });
}
```

## Type Utilities

### Useful Built-in Types

```typescript
// Partial - make all properties optional
type PartialSchedule = Partial<Schedule>;

// Required - make all properties required
type RequiredSchedule = Required<Schedule>;

// Pick - select specific properties
type ScheduleSummary = Pick<Schedule, 'id' | 'name' | 'startDate'>;

// Omit - exclude specific properties
type ScheduleInput = Omit<Schedule, 'id' | 'createdAt'>;

// Record - create object type with specific keys
type StatusColors = Record<ScheduleStatus, string>;

// Extract/Exclude for union types
type ValidStatus = Exclude<ScheduleStatus, 'deleted'>;
```

### Custom Type Guards

```typescript
// Type guard function
function isSchedule(value: unknown): value is Schedule {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'assignments' in value
  );
}

// Usage
const data: unknown = await fetchData();
if (isSchedule(data)) {
  // TypeScript knows data is Schedule here
  console.log(data.assignments);
}
```

## Running Type Checks

```bash
cd /home/user/Autonomous-Assignment-Program-Manager/frontend

# Type check only (no emit)
npm run type-check

# Type check all files (including tests)
npm run type-check:all

# Watch mode for development
npx tsc --noEmit --watch

# Check specific file
npx tsc --noEmit src/components/MyComponent.tsx
```

## Integration with Other Skills

### With test-writer
When writing tests for typed components:
1. Use proper mock types
2. Test type narrowing paths
3. Verify discriminated union handling

### With code-review
TypeScript-specific review points:
1. No `any` types
2. Proper null handling
3. Exhaustive type checks
4. Correct generic usage

### With automated-code-fixer
For TypeScript errors:
1. Identify error category
2. Apply pattern fix
3. Verify with `npm run type-check`
4. Check for cascading type issues

## Escalation Rules

**Escalate to human when:**

1. Complex generic type constraints needed
2. Module augmentation required
3. Type conflicts with third-party libraries
4. Performance issues from excessive type checking
5. Need to modify shared type definitions

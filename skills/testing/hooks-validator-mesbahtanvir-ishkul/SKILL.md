---
name: hooks-validator
description: Validates React code for Rules of Hooks violations. Catches issues like hooks called after conditional returns that cause production crashes (React error #310). Use when creating or modifying screens, components, or custom hooks.
---

# React Hooks Validator

This skill analyzes React code to detect Rules of Hooks violations that cause production crashes.

## Background

The Ishkul codebase experienced a production crash (React error #310) in LessonScreen where hooks were called after conditional returns. This skill prevents similar issues.

## Rules of Hooks

React hooks must:
1. **Always be called at the top level** - Never inside loops, conditions, or nested functions
2. **Always be called in the same order** - On every render
3. **Only be called from React functions** - Components or custom hooks

## Validation Checklist

When analyzing React code, check for these violations:

### Critical Violations (Will Crash)

1. **Hooks after conditional returns**
   ```typescript
   // BAD - Hook called after conditional return
   export const Component = () => {
     if (loading) return <Spinner />;

     const [state, setState] = useState(null); // Will crash!
     return <Content />;
   };

   // GOOD - All hooks at top
   export const Component = () => {
     const [state, setState] = useState(null);

     if (loading) return <Spinner />;
     return <Content />;
   };
   ```

2. **Hooks inside conditionals**
   ```typescript
   // BAD
   if (user) {
     const [data, setData] = useState(null);
   }

   // GOOD
   const [data, setData] = useState(user ? null : undefined);
   ```

3. **Hooks inside loops**
   ```typescript
   // BAD
   items.forEach(() => {
     const [itemState] = useState({});
   });

   // GOOD - Single state for all items
   const [itemStates, setItemStates] = useState({});
   ```

4. **Hooks inside callbacks**
   ```typescript
   // BAD
   const handleClick = () => {
     const [state] = useState(null);
   };

   // GOOD - Hook outside callback
   const [state, setState] = useState(null);
   const handleClick = () => {
     setState(newValue);
   };
   ```

### Ishkul-Specific Patterns

From the codebase patterns, ensure:

1. **Zustand store hooks at top**
   ```typescript
   export const Screen = () => {
     // All Zustand hooks first
     const { lesson, isLoading, error } = useLessonStore();
     const { courses } = useCoursesStore();

     // Then other hooks
     const { colors } = useTheme();
     const navigation = useNavigation();

     // Extract state used in multiple render paths BEFORE conditionals
     const completedBlocks = lesson?.completedBlocks ?? [];

     // Callbacks with useCallback BEFORE conditionals
     const handleSubmit = useCallback(() => {
       // ...
     }, [dependencies]);

     // NOW safe to have conditional returns
     if (isLoading) return <LoadingState />;
     if (error) return <ErrorState error={error} />;
     if (!lesson) return <NotFoundState />;

     return <SuccessState lesson={lesson} />;
   };
   ```

2. **Custom hooks must follow same rules**
   ```typescript
   // Custom hook in frontend/src/hooks/
   export function useLesson(options: UseLessonOptions) {
     // All hooks at top
     const prevLessonIdRef = useRef<string | null>(null);
     const { currentLesson, fetchLesson } = useLessonStore();
     const { getNextLesson } = useCoursesStore();

     // Effects after hooks
     useEffect(() => {
       // ...
     }, [deps]);

     // Never return early before all hooks are called
     return {
       lesson: currentLesson,
       // ...
     };
   }
   ```

## How to Analyze

When reviewing a file:

1. **List all hook calls** in order of appearance
2. **Check for early returns** that could cause hooks to be skipped
3. **Verify hooks are not inside**:
   - if/else blocks
   - for/while loops
   - forEach/map callbacks
   - Event handlers
   - try/catch blocks (hooks should be outside)
4. **Check custom hooks** call other hooks at the top level

## Output Format

When violations are found, report:

```markdown
## Hooks Violations Found

### File: `path/to/file.tsx`

**Violation #1** (Critical)
- **Type**: Hook after conditional return
- **Line**: 45
- **Hook**: `useState`
- **Issue**: `useState` is called after `if (loading) return <Spinner />`
- **Fix**: Move `useState` before the conditional return

```typescript
// Current (line 42-48)
if (loading) return <Spinner />;

const [data, setData] = useState(null);

// Fixed
const [data, setData] = useState(null);

if (loading) return <Spinner />;
```
```

## Integration with Testing

After fixing hooks violations, ensure state transition tests exist:

```typescript
describe('State Transitions (Rules of Hooks)', () => {
  it('should handle transition from loading to success', async () => {
    const { rerender } = render(<Component />);

    // Initially loading
    mockState.loading = true;
    rerender(<Component />);

    // Then success
    mockState.loading = false;
    mockState.data = { ... };
    rerender(<Component />);

    // Should not crash!
  });
});
```

## When to Use

- When creating new screens in `frontend/src/screens/`
- When creating new components with state in `frontend/src/components/`
- When modifying existing components with hooks
- When creating custom hooks in `frontend/src/hooks/`
- During code review before merging PRs

---
name: [PROJECT]-component-patterns
description: [PROJECT] frontend component architecture and patterns
globs: ["**/*.{tsx,jsx,ts,js,vue,svelte}"]
---

# Component Architecture Patterns

> **Template for project-specific component patterns skill**
> Fill in [CUSTOMIZE] sections with your project's detected or chosen patterns

**Project**: [PROJECT NAME]
**Framework**: [CUSTOMIZE: React / Angular / Vue / Svelte / SolidJS]
**Language**: [CUSTOMIZE: TypeScript / JavaScript]
**Last Updated**: [DATE]

---

## Component Structure

### File Organization

**Location**: [CUSTOMIZE: src/components / app/components / src/ui]

**Directory Pattern**: [CUSTOMIZE: Flat / By-feature / Atomic design / Nested]

**Example Structure**:
```
[CUSTOMIZE: Show your actual directory structure]

Examples:
- React: src/components/UserList/UserList.tsx, UserList.module.css, UserList.test.tsx
- Angular: src/app/components/user-list/user-list.component.ts, .html, .css
- Vue: src/components/UserList.vue
```

### Component Type

**Primary Pattern**: [CUSTOMIZE: Functional components / Class components / Composition API / Components]

**Example - Simple Component**:
```[language]
[CUSTOMIZE: Show basic component pattern]

Examples:
- React: export const UserCard: React.FC<Props> = ({ user }) => {...}
- Angular: @Component({...}) export class UserCardComponent {...}
- Vue: <script setup lang="ts">...</script>
```

---

## Props / Inputs

### Definition Pattern

**[CUSTOMIZE WITH YOUR PROJECT PATTERN]**

**Example - Props Interface**:
```[language]
[CUSTOMIZE: How props/inputs are defined]

Examples:
- React: interface UserListProps { users: User[]; onSelect: (u: User) => void }
- Angular: @Input() users: User[] = []; @Output() select = new EventEmitter<User>()
- Vue: defineProps<{ users: User[] }>()
```

### Naming Conventions

**Props**: [CUSTOMIZE: camelCase / kebab-case / PascalCase]
**Event Handlers**: [CUSTOMIZE: onAction / handleAction / @action]
**Callbacks**: [CUSTOMIZE: onUserClick / handleUserClick / userClick]

---

## State Management

### Local State

**Pattern**: [CUSTOMIZE: useState / reactive / ref / createSignal]

**Example**:
```[language]
[CUSTOMIZE: Show local state pattern]

Examples:
- React: const [users, setUsers] = useState<User[]>([])
- Angular: users: User[] = []
- Vue: const users = ref<User[]>([])
```

### Computed/Derived State

**Pattern**: [CUSTOMIZE: useMemo / computed / $: / createMemo]

**Example**:
```[language]
[CUSTOMIZE: Show computed values]
```

### Global State

**Approach**: [CUSTOMIZE: Context API / Redux / NgRx / Pinia / Zustand / Signals]

**When to Use**: [CUSTOMIZE: Authentication / Theme / Cached data / User preferences]

**Pattern**:
```[language]
[CUSTOMIZE: Show global state usage]
```

---

## Side Effects / Lifecycle

### Pattern

**Hooks/Lifecycle**: [CUSTOMIZE: useEffect / ngOnInit / onMounted / onMount]

**Example - Data Loading**:
```[language]
[CUSTOMIZE: Show data fetching pattern]
```

**Example - Cleanup**:
```[language]
[CUSTOMIZE: Show cleanup pattern]
```

---

## Event Handling

### Naming Convention

**Event Handlers**: [CUSTOMIZE: handleClick / onClick / onButtonClick]

**Example**:
```[language]
[CUSTOMIZE: Show event handler pattern]

Examples:
- React: const handleUserClick = (user: User) => {...}
- Angular: onUserClick(user: User): void {...}
- Vue: const handleUserClick = (user: User) => {...}
```

---

## API Integration

### Service Layer

**Location**: [CUSTOMIZE: src/services / src/api / app/services]

**Pattern**: [CUSTOMIZE: Class / Functions / Composables / Custom hooks]

**Example**:
```[language]
[CUSTOMIZE: Show API service pattern]

Examples:
- React: export class UserService { static async getUsers() {...}}
- Angular: @Injectable() export class UserService {...}
- Vue: export function useUsers() {...}
```

### HTTP Client

**Library**: [CUSTOMIZE: fetch / axios / Angular HttpClient / ky]

**Error Handling**:
```[language]
[CUSTOMIZE: Show error handling pattern]
```

### Loading States

**Pattern**: [CUSTOMIZE: Boolean / Enum / Status object]

**Example**:
```[language]
[CUSTOMIZE: Show loading state pattern]

Examples:
- const [loading, setLoading] = useState(false)
- loading: boolean = false
- const loading = ref(false)
```

---

## Styling Approach

### Method

**Primary**: [CUSTOMIZE: CSS Modules / styled-components / Tailwind / SCSS / Vanilla CSS / Vue scoped]

**File Extension**: [CUSTOMIZE: .module.css / .styled.ts / .css / .scss]

**Class Naming**: [CUSTOMIZE: BEM / camelCase / kebab-case / Utility classes]

### Example

```[language/css]
[CUSTOMIZE: Show styling pattern]

Examples:
- CSS Modules: import styles from './UserList.module.css'; <div className={styles.container}>
- styled-components: const Container = styled.div`...`
- Tailwind: <div className="p-4 bg-white rounded-lg">
```

---

## Form Handling

### Form Library

**Library**: [CUSTOMIZE: React Hook Form / Formik / Angular Reactive Forms / VeeValidate / None]

**Pattern**:
```[language]
[CUSTOMIZE: Show form handling pattern]
```

### Validation

**Approach**: [CUSTOMIZE: Schema-based / Inline / Custom validators]

**Example**:
```[language]
[CUSTOMIZE: Show validation pattern]
```

### Error Display

**Pattern**: [CUSTOMIZE: Inline / Toast / Modal / Field-specific]

---

## Component Testing

### Testing Framework

**Framework**: [CUSTOMIZE: Jest + React Testing Library / Vitest / Jasmine/Karma / Vue Test Utils]

**Pattern**: [CUSTOMIZE: Behavior-driven / Implementation / Integration]

### Test Structure

**Example**:
```[language]
[CUSTOMIZE: Show component test pattern]

Examples:
- React: render(<Component />); expect(screen.getByText('...')).toBeInTheDocument()
- Angular: TestBed.configureTestingModule({...}); expect(compiled.querySelector('...')).toBeTruthy()
```

### What to Test

**[CUSTOMIZE WITH PROJECT GUIDELINES]**

Always test:
- [ ] Component renders with props
- [ ] User interactions (clicks, typing)
- [ ] Loading states
- [ ] Error states
- [ ] Empty states
- [ ] [PROJECT-SPECIFIC REQUIREMENT]

---

## Performance Patterns

### Rendering Optimization

**Techniques**: [CUSTOMIZE: useMemo / React.memo / OnPush / v-memo / createMemo]

**When to Use**: [CUSTOMIZE: Expensive calculations / Large lists / Frequent re-renders]

### Code Splitting

**Approach**: [CUSTOMIZE: React.lazy / loadChildren / defineAsyncComponent]

**Example**:
```[language]
[CUSTOMIZE: Show lazy loading pattern]
```

---

## Accessibility Patterns

### Semantic HTML

**Approach**: [CUSTOMIZE: Use semantic tags / ARIA / Both]

**Required Elements**:
- [ ] Proper heading hierarchy (h1, h2, h3)
- [ ] Semantic tags (header, nav, main, section, article)
- [ ] Form labels with `for` attribute
- [ ] Button vs anchor usage
- [ ] [PROJECT-SPECIFIC REQUIREMENT]

### ARIA Attributes

**When to Use**: [CUSTOMIZE: Custom components / Non-semantic elements / Complex widgets]

**Common Patterns**:
```html
[CUSTOMIZE: Show ARIA usage]

Examples:
- aria-label, aria-describedby
- role="button", role="dialog"
- aria-live for dynamic content
```

---

## Component Checklist

When generating components, always include:

- [ ] Proper TypeScript types for props
- [ ] Loading state handling
- [ ] Error state handling
- [ ] Empty state handling
- [ ] Accessible markup (semantic HTML, ARIA)
- [ ] Responsive design (mobile breakpoint)
- [ ] Component tests (>80% coverage)
- [ ] [PROJECT-SPECIFIC REQUIREMENT]

---

## Project-Specific Patterns

**[CUSTOMIZE - ADD DETECTED OR CHOSEN PATTERNS]**

### Custom Hooks / Composables
- [CUSTOMIZE: List reusable hooks/composables]

### Higher-Order Components
- [CUSTOMIZE: If using HOCs, describe pattern]

### Render Props
- [CUSTOMIZE: If using render props, describe pattern]

### Context Usage
- [CUSTOMIZE: When and how to use Context]

---

**Customization Complete**: Replace all [CUSTOMIZE] sections with project-detected or chosen patterns.

**Auto-generated by**: `/add-skill component-architecture` command

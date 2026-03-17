# 🔄 Migration Assistant Skill

---
name: migration-assistant
description: Assist with migrating frameworks, libraries, and language versions with automated refactoring
---

## 🎯 Purpose

ช่วย migrate ระหว่าง frameworks, libraries, และ versions อย่างปลอดภัย พร้อม automated refactoring

## 📋 When to Use

- อัพเกรด framework version
- เปลี่ยน libraries (e.g., Redux → Zustand)
- เปลี่ยนภาษา (e.g., JavaScript → TypeScript)
- Migrate architecture patterns
- Update API versions

## 🔧 Common Migrations

### Framework Migrations

#### React Class → Hooks
```jsx
// Before: Class Component
class Counter extends React.Component {
  state = { count: 0 };
  
  increment = () => {
    this.setState({ count: this.state.count + 1 });
  };
  
  render() {
    return (
      <button onClick={this.increment}>
        Count: {this.state.count}
      </button>
    );
  }
}

// After: Function Component with Hooks
function Counter() {
  const [count, setCount] = useState(0);
  
  const increment = () => {
    setCount(count + 1);
  };
  
  return (
    <button onClick={increment}>
      Count: {count}
    </button>
  );
}
```

#### Next.js Pages → App Router
```jsx
// Before: pages/about.tsx
export default function About() {
  return <h1>About</h1>;
}

export async function getServerSideProps() {
  const data = await fetch('...');
  return { props: { data } };
}

// After: app/about/page.tsx
async function getData() {
  const res = await fetch('...');
  return res.json();
}

export default async function About() {
  const data = await getData();
  return <h1>About</h1>;
}
```

### Library Migrations

#### Redux → Zustand
```typescript
// Before: Redux Slice
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
  },
});

// After: Zustand Store
const useCounterStore = create((set) => ({
  value: 0,
  increment: () => set((state) => ({ value: state.value + 1 })),
  decrement: () => set((state) => ({ value: state.value - 1 })),
}));
```

#### Moment → date-fns
```typescript
// Before: Moment.js
import moment from 'moment';
moment().format('YYYY-MM-DD');
moment().add(1, 'days');
moment('2024-01-15').isAfter('2024-01-01');

// After: date-fns
import { format, addDays, isAfter, parseISO } from 'date-fns';
format(new Date(), 'yyyy-MM-dd');
addDays(new Date(), 1);
isAfter(parseISO('2024-01-15'), parseISO('2024-01-01'));
```

### Language Migrations

#### JavaScript → TypeScript
```javascript
// Before: JavaScript
function greet(name) {
  return `Hello, ${name}!`;
}

const user = {
  name: 'John',
  age: 30
};

// After: TypeScript
interface User {
  name: string;
  age: number;
}

function greet(name: string): string {
  return `Hello, ${name}!`;
}

const user: User = {
  name: 'John',
  age: 30
};
```

## 📝 Migration Process

```
1. ANALYZE current state
   - Current version/library
   - Usage patterns
   - Breaking changes list

2. PLAN migration
   - Create migration checklist
   - Identify high-risk areas
   - Plan rollback strategy

3. SETUP coexistence (if needed)
   - Install new version alongside
   - Create adapters/wrappers
   - Gradual migration path

4. MIGRATE incrementally
   - Start with low-risk files
   - Migrate one pattern at a time
   - Test after each change

5. VERIFY
   - Run all tests
   - Manual testing
   - Performance comparison

6. CLEANUP
   - Remove old dependencies
   - Remove adapters
   - Update documentation
```

## 📋 Migration Checklist Template

```markdown
## Migration: {From} → {To}

### Pre-Migration
- [ ] Read changelog and breaking changes
- [ ] Create branch for migration
- [ ] Document current state
- [ ] Ensure tests are passing

### During Migration
- [ ] Install new version/library
- [ ] Update imports
- [ ] Fix breaking changes
- [ ] Update configuration files
- [ ] Run tests after each change

### Post-Migration
- [ ] All tests passing
- [ ] Manual QA complete
- [ ] Performance verified
- [ ] Documentation updated
- [ ] Old dependencies removed
```

## ⚠️ Common Migration Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Big bang migration | Migrate incrementally |
| No rollback plan | Create backup branch |
| Skipping tests | Run tests frequently |
| Ignoring warnings | Address all deprecations |
| Rushing | Take time, be thorough |

## 🔍 Migration Commands

```bash
# Check for breaking changes
npm info package-name changelog

# Codemods (automated refactoring)
npx jscodeshift -t transform.js ./src

# TypeScript migration
npx typescript --init
npx ts-migrate

# React upgrade
npx react-codemod
```

## ✅ Verification Checklist

- [ ] All imports updated
- [ ] No deprecation warnings
- [ ] All tests passing
- [ ] No runtime errors
- [ ] Performance acceptable
- [ ] Documentation updated

## 🔗 Related Skills

- `legacy-modernization` - Modernize old code
- `refactoring` - Improve code structure
- `testing` - Ensure migration safety

# 🌐 Code Translation Skill

---
name: code-translation
description: Translate code between programming languages while preserving logic and idioms
---

## 🎯 Purpose

แปลง code ระหว่างภาษา programming ต่างๆ โดยรักษา logic และใช้ idioms ที่เหมาะสมกับภาษาปลายทาง

## 📋 When to Use

- Port code to new language
- Convert legacy code
- Learn new language syntax
- Compare implementations
- Migrate projects

## 🔧 Translation Pairs

### JavaScript ↔ TypeScript
```javascript
// JavaScript
function add(a, b) {
  return a + b;
}

const user = {
  name: 'John',
  age: 30
};
```

```typescript
// TypeScript
function add(a: number, b: number): number {
  return a + b;
}

interface User {
  name: string;
  age: number;
}

const user: User = {
  name: 'John',
  age: 30
};
```

### Python ↔ JavaScript
```python
# Python
def greet(name):
    return f"Hello, {name}!"

numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
filtered = list(filter(lambda x: x > 10, squares))
```

```javascript
// JavaScript
function greet(name) {
  return `Hello, ${name}!`;
}

const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(x => x ** 2);
const filtered = squares.filter(x => x > 10);
```

### React ↔ Vue
```jsx
// React
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

```vue
<!-- Vue 3 -->
<template>
  <button @click="count++">
    Count: {{ count }}
  </button>
</template>

<script setup>
import { ref } from 'vue';
const count = ref(0);
</script>
```

## 📊 Translation Table

| Concept | JavaScript | Python | Go |
|---------|------------|--------|-----|
| Variables | `let/const` | `=` | `var/:=` |
| Functions | `function/=>` | `def` | `func` |
| Arrays | `[]` | `[]` | `[]type` |
| Objects | `{}` | `dict/class` | `struct` |
| Async | `async/await` | `async/await` | goroutines |
| Classes | `class` | `class` | `struct+methods` |

## 📝 Translation Process

```
1. UNDERSTAND source code
   - Logic flow
   - Data structures
   - Dependencies

2. IDENTIFY equivalents
   - Language constructs
   - Standard library
   - Idioms

3. TRANSLATE structure
   - Maintain logic
   - Adapt syntax
   - Use target idioms

4. ADAPT patterns
   - Error handling
   - Async patterns
   - Type systems

5. VERIFY
   - Same output
   - Same behavior
   - No logic changes
```

## ⚠️ Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Direct syntax translation | Use target idioms |
| Ignoring type systems | Add proper types |
| Missing error handling | Adapt error patterns |
| Breaking async model | Match async patterns |

## ✅ Translation Checklist

- [ ] Logic preserved
- [ ] Idioms used correctly
- [ ] Types correct (if typed)
- [ ] Error handling adapted
- [ ] Dependencies mapped
- [ ] Tests still pass
- [ ] Performance acceptable

## 🔗 Related Skills

- `migration-assistant` - Full project migration
- `legacy-modernization` - Modernize old code
- `refactoring` - Improve structure

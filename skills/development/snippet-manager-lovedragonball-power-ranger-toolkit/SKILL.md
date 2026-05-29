# 📦 Snippet Manager Skill

---
name: snippet-manager
description: Manage, organize, and quickly access reusable code snippets
---

## 🎯 Purpose

จัดการ, จัดระเบียบ, และเข้าถึง code snippets ที่ใช้บ่อยอย่างรวดเร็ว

## 📋 When to Use

- ต้องการ code pattern ที่ใช้บ่อย
- Save code สำหรับใช้ซ้ำ
- Share code กับ team
- Build component library

## 🔧 Snippet Structure

### Snippet Format
```markdown
## Snippet: {name}

**Tags**: {tag1}, {tag2}
**Language**: {language}
**Category**: {category}

### Description
{what this snippet does}

### Code
```{language}
{code}
```

### Usage
{how to use this snippet}
```

## 📊 Snippet Categories

### React Patterns
```typescript
// Custom Hook Template
function useCustomHook<T>(initialValue: T) {
  const [value, setValue] = useState<T>(initialValue);
  
  const update = useCallback((newValue: T) => {
    setValue(newValue);
  }, []);
  
  return { value, update };
}
```

### API Patterns
```typescript
// Fetch with Error Handling
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}
```

### Form Patterns
```typescript
// React Hook Form + Zod
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
});

type FormData = z.infer<typeof schema>;

function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Utility Functions
```typescript
// Debounce
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// Throttle
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

## 📁 Snippet Organization

```
snippets/
├── react/
│   ├── hooks/
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   └── useFetch.ts
│   └── components/
│       ├── LoadingSpinner.tsx
│       └── ErrorBoundary.tsx
├── utils/
│   ├── array.ts
│   ├── string.ts
│   └── date.ts
├── api/
│   ├── fetch.ts
│   └── axios.ts
└── patterns/
    ├── singleton.ts
    └── observer.ts
```

## 🔧 Quick Access Snippets

### Array Utilities
```typescript
// Unique values
const unique = [...new Set(array)];

// Group by key
const grouped = array.reduce((acc, item) => {
  const key = item[keyField];
  (acc[key] = acc[key] || []).push(item);
  return acc;
}, {});

// Chunk array
const chunk = (arr, size) => 
  Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
    arr.slice(i * size, i * size + size)
  );
```

### String Utilities
```typescript
// Capitalize
const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

// Truncate
const truncate = (s, length) => 
  s.length > length ? s.slice(0, length) + '...' : s;

// Slug
const slug = (s) => 
  s.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
```

### Date Utilities
```typescript
// Format date
const formatDate = (date) => 
  new Intl.DateTimeFormat('th-TH').format(new Date(date));

// Relative time
const relativeTime = (date) => {
  const rtf = new Intl.RelativeTimeFormat('th');
  const diff = Date.now() - new Date(date).getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  return rtf.format(-days, 'day');
};
```

## 📝 Snippet Template

```markdown
## {Snippet Name}

**Tags**: #{tag1} #{tag2}
**Created**: {date}
**Updated**: {date}

### Description
{Brief description of what this snippet does}

### Dependencies
- {dependency 1}
- {dependency 2}

### Code
```{language}
{snippet code}
```

### Example Usage
```{language}
{example of how to use}
```

### Notes
- {important note 1}
- {important note 2}
```

## 🔍 Finding Snippets

### By Tag
```
#react #hook #typescript
```

### By Category
```
react/hooks
utils/string
patterns/singleton
```

### By Keyword
```
Search: "debounce"
Results: utils/debounce.ts, react/hooks/useDebounce.ts
```

## ✅ Snippet Best Practices

- [ ] Clear naming
- [ ] Complete typing
- [ ] Include usage example
- [ ] Add JSDoc comments
- [ ] Keep focused (one purpose)
- [ ] Test before saving
- [ ] Tag appropriately
- [ ] Update when improved

## 🔗 Related Skills

- `code-search` - Find existing snippets
- `code-generation` - Generate new code
- `documentation` - Document snippets

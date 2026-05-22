---
name: Frontend Development
description: พัฒนา Frontend ด้วย Angular, React, Vue, Next.js อย่างมืออาชีพ
---

# Frontend Development Skill

## Overview

Skill สำหรับพัฒนา Frontend applications ครอบคลุม 4 frameworks หลัก พร้อม best practices

---

## Angular

### Project Structure

```
src/
├── app/
│   ├── core/              # Singleton services, guards, interceptors
│   │   ├── services/
│   │   ├── guards/
│   │   └── interceptors/
│   ├── shared/            # Shared components, pipes, directives
│   │   ├── components/
│   │   ├── pipes/
│   │   └── directives/
│   ├── features/          # Feature modules
│   │   ├── auth/
│   │   ├── dashboard/
│   │   └── users/
│   └── app.component.ts
├── assets/
└── environments/
```

### Best Practices

1. **Standalone Components** - ใช้ standalone components (Angular 15+)
2. **Signals** - ใช้ Signals สำหรับ reactivity (Angular 16+)
3. **Smart vs Dumb Components** - แยก container และ presentational
4. **OnPush Change Detection** - ใช้เพื่อ performance
5. **Lazy Loading** - Load modules ตามต้องการ

### Common Patterns

```typescript
// Standalone Component with Signals (Angular 17+)
import { toSignal } from "@angular/core/rxjs-interop";

@Component({
  selector: "app-user-list",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (user of users(); track user.id) {
      <div>{{ user.name }}</div>
    }
  `,
})
export class UserListComponent {
  private userService = inject(UserService);

  // ใช้ toSignal() แทน effect() + subscribe
  users = toSignal(this.userService.getUsers(), { initialValue: [] });
}
```

---

## React

### Project Structure

```
src/
├── components/          # Shared/reusable components
│   ├── ui/              # Basic UI components
│   └── layout/          # Layout components
├── features/            # Feature-based modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api.ts
│   └── users/
├── hooks/               # Shared custom hooks
├── lib/                 # Utilities, helpers
├── services/            # API services
└── stores/              # State management (Zustand/Redux)
```

### Best Practices

1. **Functional Components** - ใช้ functional components เสมอ
2. **Custom Hooks** - Extract logic ออกเป็น hooks
3. **React Query/SWR** - สำหรับ data fetching
4. **Zustand/Jotai** - สำหรับ simple state management
5. **Error Boundaries** - Handle errors gracefully

### Common Patterns

```tsx
// Custom Hook Pattern
function useUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { users, loading, error };
}

// React Query Pattern
function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000,
  });
}
```

---

## Vue 3

### Project Structure

```
src/
├── components/          # Shared components
│   ├── ui/
│   └── layout/
├── composables/         # Composition API functions
├── views/               # Page components
├── stores/              # Pinia stores
├── services/            # API services
├── router/
└── assets/
```

### Best Practices

1. **Composition API** - ใช้ `<script setup>` syntax
2. **Pinia** - สำหรับ state management
3. **Composables** - Extract reusable logic
4. **defineProps/defineEmits** - Type-safe props and events
5. **Suspense** - สำหรับ async components

### Common Patterns

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useUserStore } from "@/stores/user";

// Props & Emits
const props = defineProps<{
  userId: number;
}>();

const emit = defineEmits<{
  (e: "select", user: User): void;
}>();

// Composables
const userStore = useUserStore();

// Reactive State
const searchQuery = ref("");

// Computed
const filteredUsers = computed(() =>
  userStore.users.filter((u) => u.name.includes(searchQuery.value)),
);

// Lifecycle
onMounted(() => {
  userStore.fetchUsers();
});
</script>
```

---

## Next.js (App Router)

### Project Structure

```
src/
├── app/                   # App Router
│   ├── (auth)/            # Route groups
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── loading.tsx
│   ├── api/               # API Routes
│   │   └── users/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   └── features/
├── lib/                   # Utilities
└── services/              # API services
```

### Best Practices

1. **Server Components** - Default, ใช้สำหรับ data fetching
2. **Client Components** - เฉพาะเมื่อต้องการ interactivity
3. **Route Groups** - จัดกลุ่ม routes
4. **Parallel Routes** - Render multiple pages
5. **Server Actions** - สำหรับ form submissions

### Common Patterns

```tsx
// Server Component (default)
async function UsersPage() {
  const users = await fetchUsers(); // Server-side

  return (
    <div>
      <UserList users={users} />
      <AddUserButton /> {/* Client Component */}
    </div>
  );
}

// Client Component
("use client");

function AddUserButton() {
  const [open, setOpen] = useState(false);

  return <button onClick={() => setOpen(true)}>Add User</button>;
}

// Server Action
async function createUser(formData: FormData) {
  "use server";

  const name = formData.get("name");
  await db.users.create({ name });
  revalidatePath("/users");
}
```

---

## Shared Best Practices

### CSS/Styling

1. **CSS Modules** หรือ **Tailwind CSS**
2. **CSS Variables** สำหรับ theming
3. **Mobile-first** responsive design
4. **Consistent spacing** (8px grid system)

### Performance

1. **Lazy loading** components และ routes
2. **Image optimization** (next/image, @angular/common)
3. **Code splitting**
4. **Memoization** (useMemo, React.memo, computed)

### Accessibility

1. **Semantic HTML**
2. **ARIA labels**
3. **Keyboard navigation**
4. **Color contrast**
5. **Focus management**

---

## Frontend Checklist

- [ ] ใช้ TypeScript
- [ ] Folder structure ที่เหมาะสม
- [ ] Component composition ที่ดี
- [ ] State management ที่เหมาะสม
- [ ] Error handling
- [ ] Loading states
- [ ] Responsive design
- [ ] Accessibility
- [ ] Performance optimization
- [ ] Testing coverage

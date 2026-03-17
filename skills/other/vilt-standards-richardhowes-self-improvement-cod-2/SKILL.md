---
name: vilt-coding-standards
description: Apply VILT stack coding standards when writing Vue, Laravel, or TypeScript code. Automatically enforces patterns for Composition API, Form Requests, Inertia navigation, and component hierarchy. Activates when creating or modifying Vue components, Laravel controllers, services, or models.
---

# VILT Coding Standards

Apply these standards when writing code in ResRequest projects.

## Vue Components

### Script Setup Syntax
Always use `<script setup lang="ts">`:

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useForm } from '@inertiajs/vue3'
import { Button } from '@/components/ui/button'

interface Props {
    items: Item[]
}

const props = defineProps<Props>()
</script>
```

### TypeScript Interfaces
Define interfaces for all props and emits:

```typescript
interface Props {
    user: User
    isEditing?: boolean
}

interface Emits {
    (e: 'saved', user: User): void
    (e: 'cancelled'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
```

### Composition API Only
Never use Options API. Always use Composition API:

```typescript
// CORRECT: Composition API
const count = ref(0)
const doubleCount = computed(() => count.value * 2)

function increment() {
    count.value++
}

// WRONG: Options API
export default {
    data() {
        return { count: 0 }
    },
    computed: {
        doubleCount() { return this.count * 2 }
    }
}
```

### Form Handling
Always use `useForm()` from Inertia for forms:

```typescript
import { useForm } from '@inertiajs/vue3'

const form = useForm({
    name: '',
    email: '',
})

function submit() {
    form.post(route('users.store'), {
        preserveScroll: true,
        onSuccess: () => form.reset(),
    })
}
```

## Laravel Controllers

### Form Request Validation
Always use Form Request classes:

```php
// CORRECT: Form Request
public function store(CreateUserRequest $request): RedirectResponse
{
    User::create($request->validated());
    return redirect()->back();
}

// WRONG: Inline validation
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([...]);
}
```

### Resource Transformation
Use Resources for API/Inertia responses:

```php
public function index(): Response
{
    return Inertia::render('Users/Index', [
        'users' => UserResource::collection(User::all()),
    ]);
}
```

### Happy Path Last
Handle errors first, success case last:

```php
public function store(CreateUserRequest $request): RedirectResponse
{
    if (! $request->user()->canCreateUsers()) {
        abort(403);
    }

    if (User::where('email', $request->email)->exists()) {
        return redirect()->back()->withErrors(['email' => 'Email already exists']);
    }

    // Happy path last
    User::create($request->validated());
    return redirect()->route('users.index');
}
```

### Authorization First
Always authorize before action:

```php
public function destroy(User $user): RedirectResponse
{
    $this->authorize('delete', $user);

    $user->delete();

    return redirect()->route('users.index');
}
```

## Laravel Services

### Typed Properties
Use typed properties, not docblocks:

```php
class UserService
{
    public function __construct(
        private UserRepository $repository,
        private EmailService $emailService,
    ) {}
}
```

### Return Types
Always specify return types including void:

```php
public function createUser(array $data): User
{
    return User::create($data);
}

public function sendNotification(User $user): void
{
    // ...
}
```

## Laravel Models

### Typed Casts
Use typed casts array:

```php
protected $casts = [
    'is_active' => 'boolean',
    'metadata' => 'array',
    'published_at' => 'datetime',
];
```

### Relationship Return Types
Type hint relationships:

```php
public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}

public function profile(): HasOne
{
    return $this->hasOne(Profile::class);
}
```

## TypeScript Conventions

### No any Type
Never use `any`. Use proper types or `unknown`:

```typescript
// WRONG
function process(data: any) { }

// CORRECT
function process(data: unknown) { }
function process(data: Record<string, string>) { }
```

### Interface Over Type
Prefer interfaces for object shapes:

```typescript
// CORRECT
interface User {
    id: number
    name: string
}

// Less preferred (but OK for unions/intersections)
type UserId = number | string
```

## Code Quality

### No Debugging Code
Never commit:
- `console.log()`, `console.debug()`
- `dd()`, `dump()`, `ray()`
- `debugger` statements

### No Unnecessary Comments
Write self-documenting code. Only comment WHY, not WHAT:

```php
// WRONG: Comment explains what code does
// Get the user
$user = User::find($id);

// CORRECT: Comment explains why
// Using findOrFail would throw before we can show custom error
$user = User::find($id);
if (! $user) {
    return $this->userNotFoundResponse($id);
}
```

### Translations
All user-facing strings must use translations:

```vue
<!-- Vue -->
<Button>{{ $t('common.save') }}</Button>
```

```php
// Laravel
return redirect()->back()->with('success', __('users.created'));
```

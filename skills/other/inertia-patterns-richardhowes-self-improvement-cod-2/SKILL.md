---
name: inertia-patterns
description: Enforce Inertia.js patterns in Vue components. Prevents axios usage, ensures proper form handling, and guides navigation patterns. Activates when working with data fetching, form submissions, or page navigation in Vue components.
---

# Inertia.js Patterns

Inertia is the ONLY acceptable way to handle data fetching and navigation in VILT stack.

## CRITICAL: No HTTP Clients

**NEVER import or use:**
- `axios`
- `fetch` (for API calls)
- Any HTTP client library

Inertia handles all server communication.

```typescript
// WRONG - Will be flagged as CRITICAL issue
import axios from 'axios'
const response = await axios.get('/api/users')

// WRONG
const response = await fetch('/api/users')

// CORRECT - Use Inertia
import { router } from '@inertiajs/vue3'
router.reload({ only: ['users'] })
```

## Data Fetching

### Props from Controller
Data comes from controller props, not API calls:

```typescript
// Props are passed by the Laravel controller
interface Props {
    users: User[]
    filters: Filters
}

const props = defineProps<Props>()

// Use props directly
const userCount = computed(() => props.users.length)
```

### Reloading Data
Use `router.reload()` to refresh specific props:

```typescript
import { router } from '@inertiajs/vue3'

// Reload only 'users' prop
router.reload({ only: ['users'] })

// Reload with new filters
router.reload({
    only: ['users'],
    data: {
        search: searchQuery.value,
        status: selectedStatus.value,
    },
})

// Reload preserving scroll position
router.reload({
    only: ['users'],
    preserveScroll: true,
})
```

### Partial Reloads
Be specific about what data to reload:

```typescript
// CORRECT: Only reload what changed
router.reload({ only: ['bookings'] })

// AVOID: Full page reload
router.reload()  // Reloads all props
```

## Form Handling

### useForm Hook
Always use `useForm()` for forms:

```typescript
import { useForm } from '@inertiajs/vue3'

const form = useForm({
    name: '',
    email: '',
    role: 'user',
})

function submit() {
    form.post(route('users.store'), {
        preserveScroll: true,
        onSuccess: () => {
            form.reset()
        },
        onError: (errors) => {
            // Handle validation errors
            console.error(errors)
        },
    })
}
```

### Form Methods
Use appropriate HTTP methods:

```typescript
// Create
form.post(route('users.store'))

// Update
form.put(route('users.update', user.id))
form.patch(route('users.update', user.id))

// Delete
form.delete(route('users.destroy', user.id))
```

### Form State
Access form state properties:

```typescript
// Processing state (for loading indicators)
<Button :disabled="form.processing">
    {{ form.processing ? 'Saving...' : 'Save' }}
</Button>

// Validation errors
<FloatingLabelInput
    v-model="form.name"
    :error="form.errors.name"
/>

// Check if form has been modified
const hasChanges = computed(() => form.isDirty)

// Reset form
form.reset()
form.reset('name', 'email')  // Reset specific fields

// Clear errors
form.clearErrors()
form.clearErrors('name')
```

### Transform Data
Transform data before sending:

```typescript
const form = useForm({
    startDate: null as Date | null,
    amount: '',
})

function submit() {
    form.transform((data) => ({
        ...data,
        startDate: data.startDate?.toISOString(),
        amount: parseFloat(data.amount),
    })).post(route('bookings.store'))
}
```

## Navigation

### Programmatic Navigation
Use `router` for navigation:

```typescript
import { router } from '@inertiajs/vue3'

// Simple visit
router.visit('/users')

// Visit with method
router.visit('/users', { method: 'post', data: {} })

// Replace history (no back)
router.visit('/dashboard', { replace: true })

// Preserve state
router.visit('/users', {
    preserveState: true,
    preserveScroll: true,
})
```

### Link Component
Use Inertia's Link for navigation links:

```vue
<script setup lang="ts">
import { Link } from '@inertiajs/vue3'
</script>

<template>
    <!-- Basic link -->
    <Link :href="route('users.index')">Users</Link>

    <!-- With method -->
    <Link :href="route('logout')" method="post" as="button">
        Logout
    </Link>

    <!-- Preserve scroll -->
    <Link :href="route('users.show', user.id)" preserve-scroll>
        {{ user.name }}
    </Link>
</template>
```

## Shared Data

### usePage Hook
Access shared data from HandleInertiaRequests middleware:

```typescript
import { usePage } from '@inertiajs/vue3'

const page = usePage()

// Access auth user
const user = computed(() => page.props.auth.user)

// Access flash messages
const flash = computed(() => page.props.flash)

// Access any shared prop
const appName = computed(() => page.props.appName)
```

### Type Safety
Type the page props:

```typescript
interface PageProps {
    auth: {
        user: User | null
    }
    flash: {
        success?: string
        error?: string
    }
}

const page = usePage<PageProps>()
```

## Events

### Before/After Events
Handle navigation events:

```typescript
import { router } from '@inertiajs/vue3'

// Before navigation starts
router.on('before', (event) => {
    // Return false to cancel
    if (!confirm('Leave page?')) {
        return false
    }
})

// Navigation started
router.on('start', (event) => {
    showLoadingIndicator()
})

// Navigation finished
router.on('finish', (event) => {
    hideLoadingIndicator()
})

// Successful response
router.on('success', (event) => {
    console.log('Page loaded')
})

// Error response
router.on('error', (errors) => {
    console.error(errors)
})
```

## Common Patterns

### Search/Filter
Implement search with debounce:

```typescript
import { watch, ref } from 'vue'
import { router } from '@inertiajs/vue3'
import { useDebounceFn } from '@vueuse/core'

const search = ref('')

const debouncedSearch = useDebounceFn(() => {
    router.reload({
        only: ['users'],
        data: { search: search.value },
        preserveState: true,
    })
}, 300)

watch(search, debouncedSearch)
```

### Pagination
Handle pagination:

```typescript
function changePage(page: number) {
    router.reload({
        only: ['users'],
        data: { page },
        preserveState: true,
        preserveScroll: true,
    })
}
```

### Confirmation Dialogs
Handle destructive actions:

```typescript
function deleteUser(user: User) {
    if (confirm(`Delete ${user.name}?`)) {
        router.delete(route('users.destroy', user.id), {
            preserveScroll: true,
        })
    }
}
```

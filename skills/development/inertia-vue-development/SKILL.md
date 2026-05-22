---
name: inertia-vue-development
description: >-
  Develops Inertia.js v2 Vue client-side applications. Activates when creating
  Vue pages, forms, or navigation; using <Link>, <Form>, useForm, or router;
  working with deferred props, prefetching, or polling; or when user mentions
  Vue with Inertia, Vue pages, Vue forms, or Vue navigation.
---

# Inertia Vue Development

## When to Apply

Activate this skill when:

- Creating or modifying Vue page components for Inertia
- Working with forms in Vue (using `<Form>` or `useForm`)
- Implementing client-side navigation with `<Link>` or `router`
- Using v2 features: deferred props, prefetching, or polling
- Building Vue-specific features with the Inertia protocol

## Documentation

Use `search-docs` for detailed Inertia v2 Vue patterns and documentation.

## Basic Usage

### Page Components Location

Vue page components should be placed in the `resources/js/Pages` directory.

### Page Component Structure

Important: Vue components must have a single root element.

<code-snippet name="Basic Vue Page Component" lang="vue">

<script setup>
defineProps({
    users: Array
})
</script>

<template>
    <div>
        <h1>Users</h1>
        <ul>
            <li v-for="user in users" :key="user.id">
                {{ user.name }}
            </li>
        </ul>
    </div>
</template>

</code-snippet>

## Client-Side Navigation

### Basic Link Component

Use `<Link>` for client-side navigation instead of traditional `<a>` tags:

<code-snippet name="Inertia Vue Navigation" lang="vue">

<script setup>
import { Link } from '@inertiajs/vue3'
</script>

<template>
    <div>
        <Link href="/">Home</Link>
        <Link href="/users">Users</Link>
        <Link :href="`/users/${user.id}`">View User</Link>
    </div>
</template>

</code-snippet>

### Link with Method

<code-snippet name="Link with POST Method" lang="vue">

<script setup>
import { Link } from '@inertiajs/vue3'
</script>

<template>
    <Link href="/logout" method="post" as="button">
        Logout
    </Link>
</template>

</code-snippet>

### Prefetching

Prefetch pages to improve perceived performance:

<code-snippet name="Prefetch on Hover" lang="vue">

<script setup>
import { Link } from '@inertiajs/vue3'
</script>

<template>
    <Link href="/users" prefetch>
        Users
    </Link>
</template>

</code-snippet>

### Programmatic Navigation

<code-snippet name="Router Visit" lang="vue">

<script setup>
import { router } from '@inertiajs/vue3'

function handleClick() {
    router.visit('/users')
}

// Or with options
function createUser() {
    router.visit('/users', {
        method: 'post',
        data: { name: 'John' },
        onSuccess: () => console.log('Done'),
    })
}
</script>

<template>
    <Link href="/users">Users</Link>
    <Link href="/logout" method="post" as="button">Logout</Link>
</template>

</code-snippet>

## Form Handling

### Form Component (Recommended)

The recommended way to build forms is with the `<Form>` component:

<code-snippet name="Form Component Example" lang="vue">

<script setup>
import { Form } from '@inertiajs/vue3'
</script>

<template>
    <Form action="/users" method="post" #default="{ errors, processing, wasSuccessful }">
        <input type="text" name="name" />
        <div v-if="errors.name">{{ errors.name }}</div>

        <input type="email" name="email" />
        <div v-if="errors.email">{{ errors.email }}</div>

        <button type="submit" :disabled="processing">
            {{ processing ? 'Creating...' : 'Create User' }}
        </button>

        <div v-if="wasSuccessful">User created!</div>
    </Form>
</template>

</code-snippet>

### Form Component With All Props

<code-snippet name="Form Component Full Example" lang="vue">

<script setup>
import { Form } from '@inertiajs/vue3'
</script>

<template>
    <Form
        action="/users"
        method="post"
        #default="{
            errors,
            hasErrors,
            processing,
            progress,
            wasSuccessful,
            recentlySuccessful,
            setError,
            clearErrors,
            resetAndClearErrors,
            defaults,
            isDirty,
            reset,
            submit
        }"
    >
        <input type="text" name="name" :value="defaults.name" />
        <div v-if="errors.name">{{ errors.name }}</div>

        <button type="submit" :disabled="processing">
            {{ processing ? 'Saving...' : 'Save' }}
        </button>

        <progress v-if="progress" :value="progress.percentage" max="100">
            {{ progress.percentage }}%
        </progress>

        <div v-if="wasSuccessful">Saved!</div>
    </Form>
</template>

</code-snippet>

### Form Component Reset Props

The `<Form>` component supports automatic resetting:

- `resetOnError` - Reset form data when the request fails
- `resetOnSuccess` - Reset form data when the request succeeds
- `setDefaultsOnSuccess` - Update default values on success

Use the `search-docs` tool with a query of `form component resetting` for detailed guidance.

<code-snippet name="Form with Reset Props" lang="vue">

<script setup>
import { Form } from '@inertiajs/vue3'
</script>

<template>
    <Form
        action="/users"
        method="post"
        reset-on-success
        set-defaults-on-success
        #default="{ errors, processing, wasSuccessful }"
    >
        <input type="text" name="name" />
        <div v-if="errors.name">{{ errors.name }}</div>

        <button type="submit" :disabled="processing">
            Submit
        </button>
    </Form>
</template>

</code-snippet>

Forms can also be built using the `useForm` composable for more programmatic control. Use the `search-docs` tool with a query of `useForm helper` for guidance.

### `useForm` Composable

For more programmatic control or to follow existing conventions, use the `useForm` composable:

<code-snippet name="useForm Composable Example" lang="vue">

<script setup>
import { useForm } from '@inertiajs/vue3'

const form = useForm({
    name: '',
    email: '',
    password: '',
})

function submit() {
    form.post('/users', {
        onSuccess: () => form.reset('password'),
    })
}
</script>

<template>
    <form @submit.prevent="submit">
        <input type="text" v-model="form.name" />
        <div v-if="form.errors.name">{{ form.errors.name }}</div>

        <input type="email" v-model="form.email" />
        <div v-if="form.errors.email">{{ form.errors.email }}</div>

        <input type="password" v-model="form.password" />
        <div v-if="form.errors.password">{{ form.errors.password }}</div>

        <button type="submit" :disabled="form.processing">
            Create User
        </button>
    </form>
</template>

</code-snippet>

## Inertia v2 Features

### Deferred Props

Use deferred props to load data after initial page render:

<code-snippet name="Deferred Props with Empty State" lang="vue">

<script setup>
defineProps({
    users: Array
})
</script>

<template>
    <div>
        <h1>Users</h1>
        <div v-if="!users" class="animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <ul v-else>
            <li v-for="user in users" :key="user.id">
                {{ user.name }}
            </li>
        </ul>
    </div>
</template>

</code-snippet>

### Polling

Automatically refresh data at intervals:

<code-snippet name="Polling Example" lang="vue">

<script setup>
import { router } from '@inertiajs/vue3'
import { onMounted, onUnmounted } from 'vue'

defineProps({
    stats: Object
})

let interval

onMounted(() => {
    interval = setInterval(() => {
        router.reload({ only: ['stats'] })
    }, 5000) // Poll every 5 seconds
})

onUnmounted(() => {
    clearInterval(interval)
})
</script>

<template>
    <div>
        <h1>Dashboard</h1>
        <div>Active Users: {{ stats.activeUsers }}</div>
    </div>
</template>

</code-snippet>

### WhenVisible (Infinite Scroll)

Load more data when user scrolls to a specific element:

<code-snippet name="Infinite Scroll with WhenVisible" lang="vue">

<script setup>
import { WhenVisible } from '@inertiajs/vue3'

defineProps({
    users: Object
})
</script>

<template>
    <div>
        <div v-for="user in users.data" :key="user.id">
            {{ user.name }}
        </div>

        <WhenVisible
            v-if="users.next_page_url"
            data="users"
            :params="{ page: users.current_page + 1 }"
        >
            <template #fallback>
                <div>Loading more...</div>
            </template>
        </WhenVisible>
    </div>
</template>

</code-snippet>

## Server-Side Patterns

Server-side patterns (Inertia::render, props, middleware) are covered in inertia-laravel guidelines.

## Common Pitfalls

- Using traditional `<a>` links instead of Inertia's `<Link>` component (breaks SPA behavior)
- Forgetting that Vue components must have a single root element
- Forgetting to add loading states (skeleton screens) when using deferred props
- Not handling the `undefined` state of deferred props before data loads
- Using `<form>` without preventing default submission (use `<Form>` component or `@submit.prevent`)
- Forgetting to check if `<Form>` component is available in your Inertia version
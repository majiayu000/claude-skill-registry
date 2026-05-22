---
name: alpine-js
description: Adds reactive and declarative behavior to HTML with minimal JavaScript using Alpine.js directives. Use when adding lightweight interactivity to server-rendered pages, building interactive components without a build step, or when user mentions Alpine.js, x-data, or Tailwind-style reactivity.
---

# Alpine.js

Lightweight JavaScript framework for adding reactive behavior directly in HTML markup.

## Quick Start

```html
<!-- Include Alpine -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Basic counter -->
<div x-data="{ count: 0 }">
  <button @click="count++">Increment</button>
  <span x-text="count"></span>
</div>
```

## Core Directives

### x-data

```html
<!-- Inline data -->
<div x-data="{ open: false, count: 0, name: '' }">
  <!-- Children can access open, count, name -->
</div>

<!-- With methods -->
<div x-data="{
  count: 0,
  increment() { this.count++ },
  decrement() { this.count-- }
}">
  <button @click="decrement">-</button>
  <span x-text="count"></span>
  <button @click="increment">+</button>
</div>

<!-- Reusable component -->
<script>
  document.addEventListener('alpine:init', () => {
    Alpine.data('dropdown', () => ({
      open: false,
      toggle() {
        this.open = !this.open
      },
      close() {
        this.open = false
      }
    }))
  })
</script>

<div x-data="dropdown">
  <button @click="toggle">Menu</button>
  <ul x-show="open" @click.outside="close">
    <li>Option 1</li>
    <li>Option 2</li>
  </ul>
</div>

<!-- With initial data from server -->
<div x-data="{ user: $el.dataset.user ? JSON.parse($el.dataset.user) : null }"
     data-user='{"name": "Alice", "email": "alice@example.com"}'>
  <span x-text="user?.name"></span>
</div>
```

### x-bind

```html
<!-- Bind attributes -->
<button x-data="{ disabled: true }" x-bind:disabled="disabled">
  Can't click
</button>

<!-- Shorthand -->
<img :src="imageUrl" :alt="imageAlt">

<!-- Bind classes -->
<div :class="{ 'active': isActive, 'hidden': !isVisible }"></div>

<!-- Conditional classes -->
<div :class="isRed ? 'text-red-500' : 'text-blue-500'"></div>

<!-- Object syntax -->
<div x-data="{ classes: { 'font-bold': true, 'italic': false } }"
     :class="classes">
  Styled text
</div>

<!-- Bind styles -->
<div :style="{ color: textColor, fontSize: size + 'px' }"></div>

<!-- Bind multiple attributes -->
<input x-bind="inputAttrs">
<script>
  Alpine.data('form', () => ({
    inputAttrs: {
      type: 'text',
      placeholder: 'Enter value',
      required: true,
      '@input'() { this.validate() }
    }
  }))
</script>
```

### x-on

```html
<!-- Click handler -->
<button x-on:click="open = !open">Toggle</button>

<!-- Shorthand -->
<button @click="handleClick">Click</button>

<!-- Pass event -->
<input @input="search($event.target.value)">

<!-- Modifiers -->
<button @click.prevent="submit">Submit (prevent default)</button>
<button @click.stop="action">Action (stop propagation)</button>
<a @click.prevent.stop="navigate">Link</a>

<!-- Keyboard events -->
<input @keydown.enter="submit">
<input @keydown.escape="cancel">
<input @keydown.arrow-down="nextItem">
<input @keyup.shift.enter="submitWithShift">

<!-- Keyboard combos -->
<div @keydown.ctrl.s.prevent="save">Press Ctrl+S to save</div>

<!-- Mouse modifiers -->
<button @click.left="leftClick">Left Click</button>
<button @click.right.prevent="contextMenu">Right Click</button>

<!-- Event modifiers -->
<div @click.outside="close">Click outside to close</div>
<div @scroll.window="handleScroll">Listen to window scroll</div>
<button @click.once="initOnce">Only fires once</button>
<form @submit.prevent.throttle.500ms="submit">Throttled submit</form>

<!-- Debounce -->
<input @input.debounce.300ms="search">

<!-- Self (only if clicked element is the target) -->
<div @click.self="closeModal">
  <div>Clicking here won't trigger closeModal</div>
</div>

<!-- Capture phase -->
<div @click.capture="captureClick">Capture phase</div>

<!-- Passive (for scroll performance) -->
<div @scroll.passive="handleScroll">Passive scroll</div>
```

### x-text & x-html

```html
<!-- Text content -->
<span x-text="message"></span>
<span x-text="user.name"></span>
<span x-text="count + ' items'"></span>

<!-- HTML content (be careful with XSS) -->
<div x-html="richContent"></div>
```

### x-model

```html
<!-- Two-way binding -->
<input type="text" x-model="name">
<p>Hello, <span x-text="name"></span>!</p>

<!-- With modifiers -->
<input x-model.lazy="name">      <!-- Updates on change, not input -->
<input x-model.number="age">     <!-- Casts to number -->
<input x-model.debounce="search"> <!-- Debounces updates -->
<input x-model.debounce.500ms="query">
<input x-model.trim="username">  <!-- Trims whitespace -->

<!-- Checkbox -->
<input type="checkbox" x-model="isChecked">

<!-- Multiple checkboxes (array) -->
<input type="checkbox" x-model="selectedItems" value="item1">
<input type="checkbox" x-model="selectedItems" value="item2">

<!-- Radio buttons -->
<input type="radio" x-model="choice" value="a">
<input type="radio" x-model="choice" value="b">

<!-- Select -->
<select x-model="selected">
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</select>

<!-- Multiple select -->
<select x-model="selectedMultiple" multiple>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</select>

<!-- Custom component binding -->
<div x-data="{ color: '#000000' }">
  <input type="color" x-model="color">
  <div :style="{ backgroundColor: color }">Preview</div>
</div>
```

### x-show & x-if

```html
<!-- Show/hide with CSS -->
<div x-show="isVisible">
  Visible when isVisible is true
</div>

<!-- With transition -->
<div x-show="open" x-transition>
  Fades in/out
</div>

<!-- Custom transitions -->
<div x-show="open"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="opacity-0 transform scale-90"
     x-transition:enter-end="opacity-100 transform scale-100"
     x-transition:leave="transition ease-in duration-200"
     x-transition:leave-start="opacity-100 transform scale-100"
     x-transition:leave-end="opacity-0 transform scale-90">
  Animated panel
</div>

<!-- Conditional rendering (removes from DOM) -->
<template x-if="showForm">
  <form>
    <input type="text" name="email">
    <button type="submit">Submit</button>
  </form>
</template>
```

### x-for

```html
<!-- Basic loop -->
<ul x-data="{ items: ['Apple', 'Banana', 'Cherry'] }">
  <template x-for="item in items">
    <li x-text="item"></li>
  </template>
</ul>

<!-- With index -->
<template x-for="(item, index) in items">
  <li>
    <span x-text="index + 1"></span>.
    <span x-text="item"></span>
  </li>
</template>

<!-- With key (required for proper reactivity) -->
<template x-for="user in users" :key="user.id">
  <div x-text="user.name"></div>
</template>

<!-- Object iteration -->
<template x-for="(value, key) in object">
  <div>
    <span x-text="key"></span>: <span x-text="value"></span>
  </div>
</template>

<!-- Nested loops -->
<template x-for="category in categories" :key="category.id">
  <div>
    <h3 x-text="category.name"></h3>
    <template x-for="product in category.products" :key="product.id">
      <p x-text="product.name"></p>
    </template>
  </div>
</template>
```

### x-init

```html
<!-- Run on initialization -->
<div x-data="{ posts: [] }"
     x-init="posts = await (await fetch('/api/posts')).json()">
  <template x-for="post in posts">
    <article x-text="post.title"></article>
  </template>
</div>

<!-- With loading state -->
<div x-data="{ loading: true, data: null }"
     x-init="
       data = await fetchData();
       loading = false;
     ">
  <div x-show="loading">Loading...</div>
  <div x-show="!loading" x-text="data"></div>
</div>
```

### x-effect

```html
<!-- Reactive side effects -->
<div x-data="{ count: 0, doubled: 0 }"
     x-effect="doubled = count * 2">
  <button @click="count++">Increment</button>
  <p x-text="count"></p>
  <p x-text="doubled"></p>
</div>

<!-- Log changes -->
<div x-data="{ search: '' }"
     x-effect="console.log('Search:', search)">
  <input x-model="search">
</div>

<!-- Sync to localStorage -->
<div x-data="{ theme: 'light' }"
     x-init="theme = localStorage.getItem('theme') || 'light'"
     x-effect="localStorage.setItem('theme', theme)">
  <select x-model="theme">
    <option value="light">Light</option>
    <option value="dark">Dark</option>
  </select>
</div>
```

### x-ref

```html
<!-- Reference DOM elements -->
<div x-data="{ focus() { $refs.input.focus() } }">
  <input x-ref="input" type="text">
  <button @click="focus">Focus Input</button>
</div>

<!-- Multiple refs -->
<div x-data>
  <canvas x-ref="canvas"></canvas>
  <button @click="$refs.canvas.getContext('2d').fillRect(0, 0, 100, 100)">
    Draw
  </button>
</div>
```

### x-cloak

```html
<!-- Hide until Alpine initializes -->
<style>
  [x-cloak] { display: none !important; }
</style>

<div x-data="{ ready: false }" x-cloak x-init="ready = true">
  <!-- Hidden until Alpine processes this -->
  <span x-text="message"></span>
</div>
```

### x-ignore

```html
<!-- Skip Alpine processing for subtree -->
<div x-data="{ name: 'Alpine' }">
  <p x-text="name"></p> <!-- Processed -->

  <div x-ignore>
    <p x-text="name"></p> <!-- NOT processed, shows "name" literally -->
  </div>
</div>
```

## Magic Properties

### $el

```html
<!-- Reference to current element -->
<button @click="$el.classList.toggle('active')">
  Toggle Class
</button>

<div x-init="console.log($el.offsetWidth)">
  Log width on init
</div>
```

### $refs

```html
<div x-data>
  <input x-ref="email" type="email">
  <button @click="$refs.email.select()">Select All</button>
</div>
```

### $store

```html
<script>
  document.addEventListener('alpine:init', () => {
    Alpine.store('user', {
      name: 'Guest',
      loggedIn: false,

      login(name) {
        this.name = name
        this.loggedIn = true
      },

      logout() {
        this.name = 'Guest'
        this.loggedIn = false
      }
    })
  })
</script>

<!-- Access from any component -->
<div x-data>
  <template x-if="$store.user.loggedIn">
    <p>Welcome, <span x-text="$store.user.name"></span>!</p>
    <button @click="$store.user.logout()">Logout</button>
  </template>
  <template x-if="!$store.user.loggedIn">
    <button @click="$store.user.login('Alice')">Login</button>
  </template>
</div>
```

### $watch

```html
<div x-data="{ count: 0 }"
     x-init="$watch('count', (value, oldValue) => console.log(value, oldValue))">
  <button @click="count++">Increment</button>
</div>

<!-- Watch nested properties -->
<div x-data="{ user: { name: '' } }"
     x-init="$watch('user.name', value => console.log('Name:', value))">
  <input x-model="user.name">
</div>
```

### $dispatch

```html
<!-- Dispatch custom events -->
<div @notify="alert($event.detail.message)">
  <button @click="$dispatch('notify', { message: 'Hello!' })">
    Notify Parent
  </button>
</div>

<!-- Bubble up with window -->
<button @click="$dispatch('custom-event', { data: 'value' })">
  Dispatch
</button>

<div @custom-event.window="handleEvent($event.detail)">
  Listens to window events
</div>
```

### $nextTick

```html
<div x-data="{ items: [] }">
  <button @click="
    items.push('new');
    $nextTick(() => {
      // DOM is now updated
      $refs.list.scrollTop = $refs.list.scrollHeight
    })
  ">Add Item</button>

  <ul x-ref="list">
    <template x-for="item in items">
      <li x-text="item"></li>
    </template>
  </ul>
</div>
```

### $root

```html
<div x-data="{ message: 'Hello' }">
  <div x-data="{ other: 'data' }">
    <!-- Access root component's data -->
    <span x-text="$root.message"></span>
  </div>
</div>
```

### $data

```html
<div x-data="{ a: 1, b: 2 }">
  <button @click="console.log($data)">
    Log all data: { a: 1, b: 2 }
  </button>
</div>
```

### $id

```html
<!-- Generate unique IDs -->
<div x-data x-id="['input']">
  <label :for="$id('input')">Email</label>
  <input :id="$id('input')" type="email">
</div>
```

## Complete Examples

### Dropdown Menu

```html
<div x-data="{ open: false }" class="relative">
  <button @click="open = !open" class="btn">
    Menu
  </button>

  <div x-show="open"
       x-transition
       @click.outside="open = false"
       @keydown.escape.window="open = false"
       class="absolute mt-2 bg-white shadow-lg rounded">
    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Profile</a>
    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Settings</a>
    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Logout</a>
  </div>
</div>
```

### Modal

```html
<div x-data="{ open: false }">
  <button @click="open = true">Open Modal</button>

  <div x-show="open"
       x-transition:enter="transition ease-out duration-300"
       x-transition:enter-start="opacity-0"
       x-transition:enter-end="opacity-100"
       x-transition:leave="transition ease-in duration-200"
       x-transition:leave-start="opacity-100"
       x-transition:leave-end="opacity-0"
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
       @keydown.escape.window="open = false">

    <div x-show="open"
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0 scale-90"
         x-transition:enter-end="opacity-100 scale-100"
         x-transition:leave="transition ease-in duration-200"
         x-transition:leave-start="opacity-100 scale-100"
         x-transition:leave-end="opacity-0 scale-90"
         @click.stop
         class="bg-white p-6 rounded-lg max-w-md w-full">
      <h2>Modal Title</h2>
      <p>Modal content here...</p>
      <button @click="open = false">Close</button>
    </div>
  </div>
</div>
```

### Tabs

```html
<div x-data="{ activeTab: 'tab1' }">
  <div class="flex border-b">
    <button @click="activeTab = 'tab1'"
            :class="{ 'border-b-2 border-blue-500': activeTab === 'tab1' }"
            class="px-4 py-2">
      Tab 1
    </button>
    <button @click="activeTab = 'tab2'"
            :class="{ 'border-b-2 border-blue-500': activeTab === 'tab2' }"
            class="px-4 py-2">
      Tab 2
    </button>
    <button @click="activeTab = 'tab3'"
            :class="{ 'border-b-2 border-blue-500': activeTab === 'tab3' }"
            class="px-4 py-2">
      Tab 3
    </button>
  </div>

  <div class="p-4">
    <div x-show="activeTab === 'tab1'">Content for Tab 1</div>
    <div x-show="activeTab === 'tab2'">Content for Tab 2</div>
    <div x-show="activeTab === 'tab3'">Content for Tab 3</div>
  </div>
</div>
```

### Fetch Data

```html
<div x-data="{
  loading: false,
  error: null,
  users: [],

  async fetchUsers() {
    this.loading = true
    this.error = null
    try {
      const response = await fetch('/api/users')
      if (!response.ok) throw new Error('Failed to fetch')
      this.users = await response.json()
    } catch (e) {
      this.error = e.message
    } finally {
      this.loading = false
    }
  }
}" x-init="fetchUsers()">

  <button @click="fetchUsers" :disabled="loading">
    <span x-show="loading">Loading...</span>
    <span x-show="!loading">Refresh</span>
  </button>

  <div x-show="error" class="text-red-500" x-text="error"></div>

  <ul x-show="users.length > 0">
    <template x-for="user in users" :key="user.id">
      <li x-text="user.name"></li>
    </template>
  </ul>
</div>
```

## Reference Files

- [plugins.md](references/plugins.md) - Alpine.js plugins (Mask, Intersect, Persist, etc.)
- [patterns.md](references/patterns.md) - Common patterns and best practices

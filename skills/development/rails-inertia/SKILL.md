---
name: rails-inertia
description: Specialized skill for building modern SPAs with Inertia.js, React/Vue/Svelte, and Rails. Use when creating Inertia pages, handling forms, implementing client-side routing, managing shared data, or building interactive frontends. Alternative to traditional Rails views or full API approach.
---

# Rails + Inertia.js Specialist

Build modern single-page applications using Inertia.js with React/Vue/Svelte and Rails backend.

## When to Use This Skill

- Setting up Inertia.js with Rails
- Creating Inertia pages (React, Vue, or Svelte components)
- Handling forms with Inertia
- Client-side routing without full SPA complexity
- Managing shared props and flash messages
- File uploads and form submissions
- Authentication and authorization with Inertia

## What is Inertia.js?

**Inertia.js allows you to build SPAs using classic server-side routing and controllers.**

### Why Inertia?

**Traditional Rails Views:**
- ❌ Limited interactivity
- ❌ Full page reloads

**Rails API + React SPA:**
- ❌ Duplicated routing (backend + frontend)
- ❌ Complex state management

**Inertia.js (Best of both):**
- ✅ SPA experience with no page reloads
- ✅ Server-side routing (Rails routes only)
- ✅ No API layer needed
- ✅ Use React/Vue/Svelte for views
- ✅ Simple mental model

## Quick Setup

```ruby
# Gemfile
gem 'inertia_rails'
gem 'vite_rails'
```

```bash
bundle install
rails inertia:install  # Choose: React, Vue, or Svelte
```

```ruby
# config/initializers/inertia_rails.rb
InertiaRails.configure do |config|
  config.version = ViteRuby.digest

  config.share do |controller|
    {
      auth: {
        user: controller.current_user&.as_json(only: [:id, :name, :email])
      },
      flash: controller.flash.to_hash
    }
  end
end
```

## Basic Controller Pattern

```ruby
class ArticlesController < ApplicationController
  def index
    articles = Article.published.order(created_at: :desc)

    render inertia: 'Articles/Index', props: {
      articles: articles.as_json(only: [:id, :title, :excerpt])
    }
  end

  def create
    outcome = Articles::Create.run(article_params)

    if outcome.valid?
      redirect_to article_path(outcome.result),
        notice: 'Article created'
    else
      redirect_to new_article_path,
        inertia: { errors: outcome.errors }
    end
  end
end
```

## Page Components

### React

```jsx
// app/frontend/pages/Articles/Index.jsx
import { Link } from '@inertiajs/react'

export default function Index({ articles }) {
  return (
    <div>
      <h1>Articles</h1>
      {articles.map(article => (
        <Link key={article.id} href={`/articles/${article.id}`}>
          <h2>{article.title}</h2>
        </Link>
      ))}
    </div>
  )
}
```

### Vue

```vue
<!-- app/frontend/pages/Articles/Index.vue -->
<script setup>
import { Link } from '@inertiajs/vue3'

defineProps({
  articles: Array
})
</script>

<template>
  <div>
    <h1>Articles</h1>
    <Link
      v-for="article in articles"
      :key="article.id"
      :href="`/articles/${article.id}`"
    >
      <h2>{{ article.title }}</h2>
    </Link>
  </div>
</template>
```

### Svelte

```svelte
<!-- app/frontend/pages/Articles/Index.svelte -->
<script>
  import { Link } from '@inertiajs/svelte'
  export let articles = []
</script>

<div>
  <h1>Articles</h1>
  {#each articles as article (article.id)}
    <Link href="/articles/{article.id}">
      <h2>{article.title}</h2>
    </Link>
  {/each}
</div>
```

## Forms with useForm

### React

```jsx
import { useForm } from '@inertiajs/react'

export default function New() {
  const { data, setData, post, processing, errors } = useForm({
    title: '',
    body: ''
  })

  function handleSubmit(e) {
    e.preventDefault()
    post('/articles')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={data.title}
        onChange={e => setData('title', e.target.value)}
      />
      {errors.title && <div>{errors.title}</div>}

      <textarea
        value={data.body}
        onChange={e => setData('body', e.target.value)}
      />
      {errors.body && <div>{errors.body}</div>}

      <button disabled={processing}>
        {processing ? 'Creating...' : 'Create'}
      </button>
    </form>
  )
}
```

### Svelte

```svelte
<script>
  import { useForm } from '@inertiajs/svelte'

  let form = useForm({
    title: '',
    body: ''
  })
</script>

<form on:submit|preventDefault={() => $form.post('/articles')}>
  <input bind:value={$form.title} />
  {#if $form.errors.title}
    <div>{$form.errors.title}</div>
  {/if}

  <textarea bind:value={$form.body} />
  {#if $form.errors.body}
    <div>{$form.errors.body}</div>
  {/if}

  <button disabled={$form.processing}>
    {$form.processing ? 'Creating...' : 'Create'}
  </button>
</form>
```

## Key Patterns

### Shared Layout

```jsx
// app/frontend/layouts/AppLayout.jsx
import { Link, usePage } from '@inertiajs/react'

export default function AppLayout({ children }) {
  const { auth, flash } = usePage().props

  return (
    <div>
      <nav>
        <Link href="/">Home</Link>
        {auth.user ? (
          <Link href="/logout" method="delete">Logout</Link>
        ) : (
          <Link href="/login">Login</Link>
        )}
      </nav>

      {flash.success && <div>{flash.success}</div>}
      {flash.error && <div>{flash.error}</div>}

      <main>{children}</main>
    </div>
  )
}

// Use in page:
Index.layout = page => <AppLayout>{page}</AppLayout>
```

### File Upload

```jsx
import { useForm } from '@inertiajs/react'

const { data, setData, post, progress } = useForm({
  avatar: null
})

<input
  type="file"
  onChange={e => setData('avatar', e.target.files[0])}
/>

{progress && <progress value={progress.percentage} max="100" />}

<button onClick={() => post('/profile/avatar', { forceFormData: true })}>
  Upload
</button>
```

### Authorization

```jsx
import { usePage } from '@inertiajs/react'

export default function Show({ article }) {
  const { auth } = usePage().props

  return (
    <div>
      <h1>{article.title}</h1>

      {auth.can('update', article) && (
        <Link href={`/articles/${article.id}/edit`}>Edit</Link>
      )}

      {auth.can('destroy', article) && (
        <Link href={`/articles/${article.id}`} method="delete">
          Delete
        </Link>
      )}
    </div>
  )
}
```

## Testing

### Component Test

```javascript
import { render, screen } from '@testing-library/react'
import Index from '@/pages/Articles/Index'

test('renders articles', () => {
  const articles = [
    { id: 1, title: 'First Article' }
  ]

  render(<Index articles={articles} />)
  expect(screen.getByText('First Article')).toBeInTheDocument()
})
```

### System Test

```ruby
RSpec.describe "Articles", type: :system do
  it "creates article" do
    visit new_article_path

    fill_in "Title", with: "New Article"
    click_button "Create Article"

    expect(page).to have_text("Article created")
  end
end
```

## Best Practices

### ✅ Do

- **Use Inertia links** - `<Link>` instead of `<a>`
- **Share common data** - via InertiaRails.configure
- **Validate on server** - Never trust client alone
- **Handle loading states** - Show spinners when `processing`
- **Use layouts** - DRY up navigation

### ❌ Don't

- **Don't use `window.location`** - Use Inertia router
- **Don't fetch data client-side** - Server provides props
- **Don't create API endpoints** - Use regular Rails routes
- **Don't bypass Inertia links** - Breaks SPA behavior

---

## Reference Documentation

For comprehensive examples and advanced patterns:
- Full Inertia guide: `inertia-reference.md` (detailed setup, SSR, modals, pagination, all frameworks)

---

**Remember**: Inertia.js is glue between Rails and React/Vue/Svelte. Think of it as rendering React/Vue/Svelte views from Rails controllers instead of ERB templates.

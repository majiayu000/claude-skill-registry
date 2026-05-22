---
name: qwik
description: Builds instant-loading web applications with Qwik's resumable architecture and fine-grained lazy loading. Use when creating highly performant sites, when user mentions Qwik, resumability, zero hydration, or O(1) startup time.
---

# Qwik

Framework that delivers instant-loading applications through resumability - apps boot with ~1kb JS regardless of complexity.

## Quick Start

```bash
# Create new project
npm create qwik@latest

# Options:
# - Empty App
# - QwikCity App (recommended)
# - Playground

cd my-qwik-app
npm run dev
```

## Core Concepts

### Resumability vs Hydration

Traditional frameworks hydrate (re-execute all code on client). Qwik resumes (continues where server left off):

- **No hydration** - App state serialized in HTML
- **O(1) startup** - Constant time regardless of app size
- **Lazy execution** - Code loads only when needed

### The $ Convention

The `$` suffix marks serialization boundaries for the optimizer:

```tsx
import { component$, useSignal, $ } from '@builder.io/qwik';

// component$ - Lazy-loaded component
export default component$(() => {
  const count = useSignal(0);

  // $() - Lazy-loaded callback
  const handleClick = $(() => {
    count.value++;
  });

  return <button onClick$={handleClick}>Count: {count.value}</button>;
});
```

## Components

### Basic Component

```tsx
import { component$ } from '@builder.io/qwik';

export const Greeting = component$(() => {
  return <h1>Hello, Qwik!</h1>;
});
```

### Props

```tsx
import { component$ } from '@builder.io/qwik';

interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button = component$<ButtonProps>((props) => {
  return (
    <button
      class={`btn btn-${props.variant ?? 'primary'}`}
      disabled={props.disabled}
    >
      {props.label}
    </button>
  );
});

// Usage
<Button label="Click me" variant="primary" />
```

### Slots (Content Projection)

```tsx
import { component$, Slot } from '@builder.io/qwik';

export const Card = component$(() => {
  return (
    <div class="card">
      <div class="card-header">
        <Slot name="header" />
      </div>
      <div class="card-body">
        <Slot /> {/* Default slot */}
      </div>
      <div class="card-footer">
        <Slot name="footer" />
      </div>
    </div>
  );
});

// Usage
<Card>
  <div q:slot="header">Card Title</div>
  <p>Card content goes here</p>
  <button q:slot="footer">Action</button>
</Card>
```

## State Management

### Signals (Primitives)

```tsx
import { component$, useSignal } from '@builder.io/qwik';

export default component$(() => {
  const count = useSignal(0);
  const name = useSignal('');

  return (
    <div>
      <p>Count: {count.value}</p>
      <button onClick$={() => count.value++}>Increment</button>

      <input
        value={name.value}
        onInput$={(e) => (name.value = (e.target as HTMLInputElement).value)}
      />
      <p>Hello, {name.value}!</p>
    </div>
  );
});
```

### Stores (Objects)

```tsx
import { component$, useStore } from '@builder.io/qwik';

interface TodoItem {
  id: number;
  text: string;
  completed: boolean;
}

export default component$(() => {
  const state = useStore({
    todos: [] as TodoItem[],
    newTodo: '',
  });

  const addTodo = $(() => {
    if (state.newTodo.trim()) {
      state.todos.push({
        id: Date.now(),
        text: state.newTodo,
        completed: false,
      });
      state.newTodo = '';
    }
  });

  return (
    <div>
      <input
        value={state.newTodo}
        onInput$={(e) => (state.newTodo = (e.target as HTMLInputElement).value)}
      />
      <button onClick$={addTodo}>Add</button>

      <ul>
        {state.todos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange$={() => (todo.completed = !todo.completed)}
            />
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  );
});
```

### Computed Values

```tsx
import { component$, useSignal, useComputed$ } from '@builder.io/qwik';

export default component$(() => {
  const price = useSignal(100);
  const quantity = useSignal(2);

  const total = useComputed$(() => {
    return price.value * quantity.value;
  });

  return (
    <div>
      <p>Price: ${price.value}</p>
      <p>Quantity: {quantity.value}</p>
      <p>Total: ${total.value}</p>
    </div>
  );
});
```

### Context

```tsx
import {
  component$,
  createContextId,
  useContextProvider,
  useContext,
  useStore,
} from '@builder.io/qwik';

// Define context
interface UserContext {
  name: string;
  isLoggedIn: boolean;
}

export const UserContextId = createContextId<UserContext>('user-context');

// Provider component
export const App = component$(() => {
  const userState = useStore<UserContext>({
    name: 'Guest',
    isLoggedIn: false,
  });

  useContextProvider(UserContextId, userState);

  return <UserProfile />;
});

// Consumer component
export const UserProfile = component$(() => {
  const user = useContext(UserContextId);

  return (
    <div>
      <p>Welcome, {user.name}!</p>
      {!user.isLoggedIn && (
        <button onClick$={() => {
          user.name = 'John';
          user.isLoggedIn = true;
        }}>
          Log In
        </button>
      )}
    </div>
  );
});
```

## Tasks & Lifecycle

### useTask$ (Reactive Side Effects)

```tsx
import { component$, useSignal, useTask$ } from '@builder.io/qwik';

export default component$(() => {
  const query = useSignal('');
  const results = useSignal<string[]>([]);

  // Runs on server and client, tracks dependencies
  useTask$(async ({ track, cleanup }) => {
    const searchQuery = track(() => query.value);

    if (!searchQuery) {
      results.value = [];
      return;
    }

    // Debounce
    const controller = new AbortController();
    cleanup(() => controller.abort());

    const timer = setTimeout(async () => {
      const res = await fetch(`/api/search?q=${searchQuery}`, {
        signal: controller.signal,
      });
      results.value = await res.json();
    }, 300);

    cleanup(() => clearTimeout(timer));
  });

  return (
    <div>
      <input
        value={query.value}
        onInput$={(e) => (query.value = (e.target as HTMLInputElement).value)}
      />
      <ul>
        {results.value.map((r) => (
          <li key={r}>{r}</li>
        ))}
      </ul>
    </div>
  );
});
```

### useVisibleTask$ (Client-Only)

```tsx
import { component$, useSignal, useVisibleTask$ } from '@builder.io/qwik';

export default component$(() => {
  const canvasRef = useSignal<HTMLCanvasElement>();
  const mousePos = useSignal({ x: 0, y: 0 });

  // Only runs on client when component is visible
  useVisibleTask$(({ cleanup }) => {
    const canvas = canvasRef.value;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    const handleMouseMove = (e: MouseEvent) => {
      mousePos.value = { x: e.clientX, y: e.clientY };
    };

    window.addEventListener('mousemove', handleMouseMove);
    cleanup(() => window.removeEventListener('mousemove', handleMouseMove));
  });

  return (
    <div>
      <canvas ref={canvasRef} width={400} height={300} />
      <p>Mouse: {mousePos.value.x}, {mousePos.value.y}</p>
    </div>
  );
});
```

## Event Handling

```tsx
import { component$, useSignal, $ } from '@builder.io/qwik';

export default component$(() => {
  const message = useSignal('');

  // Inline handler
  const handleClick = $(() => {
    message.value = 'Button clicked!';
  });

  // With event parameter
  const handleInput = $((event: Event) => {
    const target = event.target as HTMLInputElement;
    message.value = target.value;
  });

  // Prevent default
  const handleSubmit = $((event: SubmitEvent) => {
    event.preventDefault();
    // Handle form submission
  });

  return (
    <form preventdefault:submit onSubmit$={handleSubmit}>
      <input onInput$={handleInput} />
      <button onClick$={handleClick}>Click</button>
      <p>{message.value}</p>
    </form>
  );
});
```

## Qwik City (Routing)

### File-Based Routes

```
src/routes/
  layout.tsx           # Root layout
  index.tsx            # /
  about/
    index.tsx          # /about
  blog/
    index.tsx          # /blog
    [slug]/
      index.tsx        # /blog/:slug
  api/
    users/
      index.ts         # API endpoint: /api/users
```

### Page Component

```tsx
// src/routes/index.tsx
import { component$ } from '@builder.io/qwik';
import type { DocumentHead } from '@builder.io/qwik-city';

export default component$(() => {
  return (
    <div>
      <h1>Welcome to Qwik</h1>
    </div>
  );
});

export const head: DocumentHead = {
  title: 'Home | My App',
  meta: [
    { name: 'description', content: 'Welcome to my Qwik application' },
  ],
};
```

### Layout

```tsx
// src/routes/layout.tsx
import { component$, Slot } from '@builder.io/qwik';
import { Link } from '@builder.io/qwik-city';

export default component$(() => {
  return (
    <div class="app">
      <nav>
        <Link href="/">Home</Link>
        <Link href="/about">About</Link>
        <Link href="/blog">Blog</Link>
      </nav>
      <main>
        <Slot />
      </main>
    </div>
  );
});
```

### Data Loading (routeLoader$)

```tsx
// src/routes/blog/[slug]/index.tsx
import { component$ } from '@builder.io/qwik';
import { routeLoader$ } from '@builder.io/qwik-city';

export const usePost = routeLoader$(async ({ params, status }) => {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`);

  if (!res.ok) {
    status(404);
    return null;
  }

  return res.json();
});

export default component$(() => {
  const post = usePost();

  if (!post.value) {
    return <p>Post not found</p>;
  }

  return (
    <article>
      <h1>{post.value.title}</h1>
      <div dangerouslySetInnerHTML={post.value.content} />
    </article>
  );
});

export const head: DocumentHead = ({ resolveValue }) => {
  const post = resolveValue(usePost);
  return {
    title: post?.title ?? 'Not Found',
  };
};
```

### Server Actions (routeAction$)

```tsx
// src/routes/contact/index.tsx
import { component$ } from '@builder.io/qwik';
import { routeAction$, zod$, z, Form } from '@builder.io/qwik-city';

export const useContactForm = routeAction$(
  async (data, { fail }) => {
    const result = await sendEmail({
      to: 'contact@example.com',
      from: data.email,
      subject: data.subject,
      body: data.message,
    });

    if (!result.success) {
      return fail(500, { message: 'Failed to send message' });
    }

    return { success: true };
  },
  zod$({
    email: z.string().email(),
    subject: z.string().min(1),
    message: z.string().min(10),
  })
);

export default component$(() => {
  const action = useContactForm();

  return (
    <Form action={action}>
      <input name="email" type="email" placeholder="Your email" />
      {action.value?.fieldErrors?.email && (
        <span class="error">{action.value.fieldErrors.email}</span>
      )}

      <input name="subject" placeholder="Subject" />
      <textarea name="message" placeholder="Message" />

      <button type="submit" disabled={action.isRunning}>
        {action.isRunning ? 'Sending...' : 'Send'}
      </button>

      {action.value?.success && <p class="success">Message sent!</p>}
      {action.value?.message && <p class="error">{action.value.message}</p>}
    </Form>
  );
});
```

### API Endpoints

```typescript
// src/routes/api/users/index.ts
import type { RequestHandler } from '@builder.io/qwik-city';

export const onGet: RequestHandler = async ({ json }) => {
  const users = await db.users.findMany();
  json(200, users);
};

export const onPost: RequestHandler = async ({ request, json, status }) => {
  const body = await request.json();

  const user = await db.users.create({
    data: body,
  });

  status(201);
  json(201, user);
};

// src/routes/api/users/[id]/index.ts
export const onGet: RequestHandler = async ({ params, json, status }) => {
  const user = await db.users.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    status(404);
    json(404, { error: 'User not found' });
    return;
  }

  json(200, user);
};
```

### Middleware

```typescript
// src/routes/admin/layout.tsx
import { component$, Slot } from '@builder.io/qwik';
import type { RequestHandler } from '@builder.io/qwik-city';

export const onRequest: RequestHandler = async ({ cookie, redirect }) => {
  const session = cookie.get('session');

  if (!session) {
    throw redirect(302, '/login');
  }
};

export default component$(() => {
  return (
    <div class="admin-layout">
      <Slot />
    </div>
  );
});
```

## Styling

### Scoped CSS

```tsx
// src/routes/index.tsx
import { component$, useStylesScoped$ } from '@builder.io/qwik';

export default component$(() => {
  useStylesScoped$(`
    .hero {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 4rem;
      color: white;
    }
    .hero h1 {
      font-size: 3rem;
    }
  `);

  return (
    <section class="hero">
      <h1>Welcome</h1>
    </section>
  );
});
```

### Global Styles

```tsx
import { component$, useStyles$ } from '@builder.io/qwik';
import globalStyles from './global.css?inline';

export default component$(() => {
  useStyles$(globalStyles);

  return <div>...</div>;
});
```

## Deployment

```bash
# Add deployment adapter
npm run qwik add

# Available adapters:
# - Cloudflare Pages
# - Netlify Edge
# - Vercel Edge
# - Node.js
# - AWS Lambda
# - Azure Functions
# - Deno
# - Bun
# - Static (SSG)

# Build
npm run build

# Preview
npm run preview
```

## Performance Tips

1. **Use routeLoader$** for data that should be preloaded
2. **Avoid useVisibleTask$** unless absolutely necessary (client-only)
3. **Keep components small** - optimizer works better with granular code
4. **Use signals over stores** for simple state
5. **Leverage serialization** - avoid closures that capture complex objects

## Reference Files

- [advanced-patterns.md](references/advanced-patterns.md) - Resource management, streaming, prefetching
- [optimization.md](references/optimization.md) - Bundle analysis, code splitting strategies

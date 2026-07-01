---
name: frontend-ui
description: Build production-quality user-facing interfaces. Use when creating or modifying components, implementing layouts, managing state, or when the output must look hand-crafted rather than AI-generated.
---

# Frontend UI Engineering

## Overview

Build UIs that read as hand-crafted production work, not machine output. The failure mode is the generic "AI aesthetic": default palettes, oversized cards, template layouts with no tie to the content. Conform to the project's real design system, meet WCAG 2.1 AA, and handle every interaction state.

Examples below pair a JavaScript component framework (React) with a server-rendered template stack (Django/Python); CSS and HTML examples are framework-neutral. The patterns hold across frameworks — apply the equivalent in whatever stack the project uses.

## When to Use

- Building new UI components or pages
- Modifying existing user-facing interfaces
- Implementing responsive layouts
- Adding interactivity or state management
- Fixing visual or UX issues

## Component Architecture

### File Structure

Colocate everything that changes together with the component. The principle is stack-independent:

```
# JavaScript component framework (React)
src/components/TaskList/
  TaskList.tsx          # Component implementation
  TaskList.test.tsx     # Tests
  TaskList.stories.tsx  # Stories (if using a component workbench)
  use-task-list.ts      # Custom hook (when state is non-trivial)
  types.ts              # Component-local types
```

```
# Server-rendered templates (Django)
app/components/task_list/
  task_list.html        # Template — presentation
  task_list.py          # View / component logic
  task_list_test.py     # Tests
  task_list.css         # Component-local styles
```

### Component Patterns

**Prefer composition over configuration.** Expose regions as slots/children, not a wall of props.

```tsx
// React — composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// React — over-configured (avoid)
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

```django
{# Django — composable: a card shell that yields named regions #}
{% component "card" %}
  {% fill "header" %}<h2 class="card-title">Tasks</h2>{% endfill %}
  {% fill "body" %}{% include "task_list.html" with tasks=tasks %}{% endfill %}
{% endcomponent %}

{# Django — over-configured (avoid) #}
{% component "card" title="Tasks" header_variant="large" body_padding="md" content=task_list %}
```

**Keep components focused.** One responsibility per component.

```tsx
// React — renders a single task row, nothing else
export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center gap-3 p-3">
      <Checkbox checked={task.done} onChange={() => onToggle(task.id)} />
      <span className={task.done ? 'line-through text-muted' : ''}>{task.title}</span>
      <Button variant="ghost" size="sm" onClick={() => onDelete(task.id)}>
        <TrashIcon />
      </Button>
    </li>
  );
}
```

```django
{# Django — task_item.html: renders a single task row, nothing else #}
<li class="task-item">
  <input type="checkbox" name="toggle" value="{{ task.id }}"
         {% if task.done %}checked{% endif %}
         aria-label="Complete: {{ task.title }}">
  <span class="{% if task.done %}done{% endif %}">{{ task.title }}</span>
  <button type="submit" name="delete" value="{{ task.id }}"
          class="btn-ghost" aria-label="Delete task">
    {% include "icons/trash.svg" %}
  </button>
</li>
```

**Separate data fetching from presentation.** The data owner picks the state to render (loading, error, empty, populated); the presentation component only renders.

```tsx
// React — container owns data
export function TaskListContainer() {
  const { tasks, isLoading, error, refetch } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />;

  return <TaskList tasks={tasks} />;
}

// React — presentation owns rendering
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </ul>
  );
}
```

```python
# Django — the view owns data and chooses which state to render (MVT)
def task_list(request):
    try:
        tasks = Task.objects.for_user(request.user)
    except DataError:
        return render(request, "errors/load_failed.html",
                      {"retry_url": request.path}, status=503)
    template = "task_list.html" if tasks else "empty_state.html"
    return render(request, template, {"tasks": tasks})
```

```django
{# Django — task_list.html owns rendering only #}
<ul role="list" class="divide-y">
  {% for task in tasks %}{% include "task_item.html" with task=task %}{% endfor %}
</ul>
```

## State Management

Pick the narrowest scope that holds the state. Categories, narrowest to widest:

```
Local state    → component-specific UI state           React: useState · Vue: ref/reactive
Lifted state   → shared between 2-3 components in the same hierarchy  props + change handlers
Context        → theme, auth, locale (read-heavy,       React: Context · Vue: provide/inject
                 write-rare)
URL state      → filters, pagination, shareable UI      router/searchParams (any stack)
                 state
Server state   → remote data with caching              React Query, SWR; Vue: TanStack Query
Global store   → complex client state shared app-wide   Zustand, Redux; Vue: Pinia
```

Server-rendered stacks map the same categories onto request/session/query-param/database state — the categories hold; only the storage moves to the server.

**Avoid prop drilling deeper than 3 levels.** If you pass props through components that don't use them, introduce context or restructure the component tree.

## Design System Adherence

### Avoid the AI Aesthetic

Machine-generated UI has recognizable tells. Reject each:

| AI Default | Why It Is a Problem | Production Quality |
|---|---|---|
| Purple/indigo everything | Models default to visually "safe" palettes, making every app look identical | Use the project's actual color palette |
| Excessive gradients | Gradients add visual noise and clash with most design systems | Flat or subtle gradients matching the design system |
| Rounded everything (rounded-2xl) | Maximum rounding signals "friendly" but ignores the hierarchy of corner radii in real designs | Consistent border-radius from the design system |
| Generic hero sections | Template-driven layout with no connection to the actual content or user need | Content-first layouts |
| Lorem ipsum-style copy | Placeholder text hides layout problems that real content reveals (length, wrapping, overflow) | Realistic placeholder content |
| Oversized padding everywhere | Equal generous padding destroys visual hierarchy and wastes screen space | Consistent spacing scale |
| Stock card grids | Uniform grids are a layout shortcut that ignores information priority and scanning patterns | Purpose-driven layouts |
| Shadow-heavy design | Layered shadows add depth that competes with content and slows rendering on low-end devices | Subtle or no shadows unless the design system specifies |

### Spacing and Layout

Use the project's spacing scale. Do not invent off-scale values:

```css
/* Use the scale: 0.25rem increments (or whatever the project uses) */
/* Good */  padding: 1rem;      /* 16px */
/* Good */  gap: 0.75rem;       /* 12px */
/* Bad */   padding: 13px;      /* Not on any scale */
/* Bad */   margin-top: 2.3rem; /* Not on any scale */
```

### Typography

Keep the heading hierarchy:

```
h1 → Page title (one per page)
h2 → Section title
h3 → Subsection title
body → Default text
small → Secondary/helper text
```

Do not skip heading levels. Do not borrow heading styles for non-heading content.

### Color

- Use semantic color tokens: `text-primary`, `bg-surface`, `border-default` — not raw hex values
- Ensure sufficient contrast (4.5:1 for normal text, 3:1 for large text)
- Do not rely solely on color to convey information (use icons, text, or patterns too)

## Accessibility (WCAG 2.1 AA)

Every component meets these standards. Use the native element first; reach for ARIA only when no native element fits.

### Keyboard Navigation

The native element is focusable and operable in any stack:

```html
<button>Click me</button>          <!-- focusable + keyboard-activatable by default -->
<div onclick="handleClick()">Click me</div>   <!-- NOT focusable; avoid -->
```

When a custom widget is unavoidable, restore the keyboard contract. Add `tabindex`, a role, and the Enter/Space handling the native control gives for free:

```tsx
// React
<div role="button" tabIndex={0} onClick={handleClick}
     onKeyDown={e => {
       if (e.key === 'Enter') handleClick();
       if (e.key === ' ') e.preventDefault();
     }}
     onKeyUp={e => {
       if (e.key === ' ') handleClick();
     }}>
  Click me
</div>
```

```html
<!-- Server-rendered / progressive enhancement (vanilla JS) -->
<div role="button" tabindex="0" id="action">Click me</div>
<script>
  const el = document.getElementById('action');
  el.addEventListener('click', handleClick);
  el.addEventListener('keydown', e => {
    if (e.key === 'Enter') handleClick();
    if (e.key === ' ') e.preventDefault();
  });
  el.addEventListener('keyup', e => { if (e.key === ' ') handleClick(); });
</script>
```

### ARIA Labels

Label every interactive element that lacks visible text. The markup is stack-neutral (React uses `htmlFor` where plain HTML uses `for`):

```html
<!-- Icon-only control needs an accessible name -->
<button aria-label="Close dialog"><!-- X icon --></button>

<!-- Associate a label with its input -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- Or label inline when no visible label exists -->
<input aria-label="Search tasks" type="search" />
```

### Focus Management

Move focus when content appears, and trap it inside modal surfaces until they close:

```tsx
// React
function Dialog({ isOpen, onClose }: DialogProps) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) closeRef.current?.focus();
  }, [isOpen]);

  // Trap focus inside the dialog while open
  return (
    <dialog open={isOpen}>
      <button ref={closeRef} onClick={onClose}>Close</button>
      {/* dialog content */}
    </dialog>
  );
}
```

```html
<!-- Server-rendered / vanilla JS: move focus when the dialog opens -->
<dialog id="confirm">
  <button id="confirm-close">Close</button>
  <!-- dialog content -->
</dialog>
<script>
  function openDialog() {
    const dialog = document.getElementById('confirm');
    dialog.showModal();                                  // native modal traps focus
    document.getElementById('confirm-close').focus();    // move focus in
  }
</script>
```

### Meaningful Empty and Error States

Never render a blank screen. Give the empty state a purpose and a next action:

```tsx
// React
function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <div role="status" className="text-center py-12">
        <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
        <h3 className="mt-2 text-sm font-medium">No tasks</h3>
        <p className="mt-1 text-sm text-muted">Get started by creating a new task.</p>
        <Button className="mt-4" onClick={onCreateTask}>Create Task</Button>
      </div>
    );
  }

  return <ul role="list">...</ul>;
}
```

```django
{# Django — empty_state.html rendered when the view finds no tasks #}
<div role="status" class="text-center py-12">
  {% include "icons/tasks_empty.svg" %}
  <h3 class="mt-2 text-sm font-medium">No tasks</h3>
  <p class="mt-1 text-sm text-muted">Get started by creating a new task.</p>
  <a href="{% url 'task_create' %}" class="btn mt-4">Create Task</a>
</div>
```

## Responsive Design

Build mobile-first, then widen. Express breakpoints with utility classes or plain CSS — both are framework-neutral:

```html
<!-- Utility CSS (Tailwind) -->
<div class="
  grid grid-cols-1      /* Mobile: single column */
  sm:grid-cols-2        /* Small: 2 columns */
  lg:grid-cols-3        /* Large: 3 columns */
  gap-4
">
```

```css
/* Plain CSS, mobile-first */
.grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 768px)  { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .grid { grid-template-columns: repeat(3, 1fr); } }
```

Test at these breakpoints: 320px, 768px, 1024px, 1440px.

## Loading and Transitions

Use skeletons for content, not spinners. The skeleton markup is stack-neutral:

```html
<div class="space-y-3" aria-busy="true" aria-label="Loading tasks">
  <div class="h-12 bg-muted animate-pulse rounded"></div>
  <div class="h-12 bg-muted animate-pulse rounded"></div>
  <div class="h-12 bg-muted animate-pulse rounded"></div>
</div>
```

Apply optimistic updates so the UI responds before the server confirms. Cache mutation is a client-side pattern; the shape is identical in React Query and Vue's TanStack Query — snapshot, apply, roll back on error:

```tsx
// React (TanStack Query)
function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      );

      return { previous };
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous);
    },
  });
}
```

```js
// Vue (@tanstack/vue-query) — same snapshot/apply/rollback contract
function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);
      queryClient.setQueryData(['tasks'], (old) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      );
      return { previous };
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context.previous);
    },
  });
}
```

## See Also

Detailed WCAG checks and testing tools are in `references/accessibility-checklist.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Accessibility is a nice-to-have" | It's a legal requirement in many jurisdictions and an engineering quality standard. |
| "We'll make it responsive later" | Retrofitting responsive design is 3x harder than building it from the start. |
| "The design isn't final, so I'll skip styling" | Use the design system defaults. Unstyled UI creates a broken first impression for reviewers. |
| "This is just a prototype" | Prototypes become production code. Build the foundation right. |
| "The AI aesthetic is fine for now" | It signals low quality. Use the project's actual design system from the start. |

## Red Flags

- Components with more than 200 lines (split them)
- Inline styles or arbitrary pixel values
- Missing error states, loading states, or empty states
- No keyboard navigation testing
- Color as the sole indicator of state (red/green without text or icons)
- Generic "AI look" (purple gradients, oversized cards, stock layouts)

## Verification

After building UI:

- [ ] Component renders without console errors
- [ ] All interactive elements are keyboard accessible (Tab through the page)
- [ ] Screen reader can convey the page's content and structure
- [ ] Responsive: works at 320px, 768px, 1024px, 1440px
- [ ] Loading, error, and empty states all handled
- [ ] Follows the project's design system (spacing, colors, typography)
- [ ] No accessibility warnings in dev tools or axe-core

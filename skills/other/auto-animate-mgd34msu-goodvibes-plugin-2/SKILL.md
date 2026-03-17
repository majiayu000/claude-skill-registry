---
name: auto-animate
description: Adds automatic animations to DOM changes with zero configuration using FormKit's AutoAnimate. Use when adding smooth transitions for list reordering, adding/removing elements, or quick UI polish.
---

# AutoAnimate

Zero-config, drop-in animation utility that adds smooth transitions to any web app. 1.9KB, works with React, Vue, Svelte, Solid, and vanilla JS.

## Quick Start

```bash
npm install @formkit/auto-animate
```

```javascript
import autoAnimate from '@formkit/auto-animate';

// Apply to any parent element
autoAnimate(document.getElementById('list'));
```

That's it. Children added, removed, or moved will animate automatically.

## What It Animates

AutoAnimate triggers on three DOM events:
1. **Child added** - fade in
2. **Child removed** - fade out
3. **Child moved** - smooth position change

## React

### useAutoAnimate Hook

```jsx
import { useAutoAnimate } from '@formkit/auto-animate/react';

function TodoList() {
  const [items, setItems] = useState(['Item 1', 'Item 2', 'Item 3']);
  const [parent] = useAutoAnimate();

  const addItem = () => setItems([...items, `Item ${items.length + 1}`]);
  const removeItem = (index) => setItems(items.filter((_, i) => i !== index));

  return (
    <div>
      <button onClick={addItem}>Add Item</button>
      <ul ref={parent}>
        {items.map((item, index) => (
          <li key={item}>
            {item}
            <button onClick={() => removeItem(index)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Enable/Disable Animation

```jsx
function ToggleableAnimation() {
  const [parent, enableAnimations] = useAutoAnimate();
  const [isEnabled, setIsEnabled] = useState(true);

  const toggle = () => {
    setIsEnabled(!isEnabled);
    enableAnimations(!isEnabled);
  };

  return (
    <>
      <button onClick={toggle}>
        {isEnabled ? 'Disable' : 'Enable'} Animations
      </button>
      <ul ref={parent}>
        {/* items */}
      </ul>
    </>
  );
}
```

### With Custom Options

```jsx
function CustomAnimations() {
  const [parent] = useAutoAnimate({
    duration: 250,
    easing: 'ease-in-out'
  });

  return <ul ref={parent}>{/* items */}</ul>;
}
```

## Vue

### Directive (Global Registration)

```javascript
// main.js
import { autoAnimatePlugin } from '@formkit/auto-animate/vue';

app.use(autoAnimatePlugin);
```

```vue
<template>
  <ul v-auto-animate>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
</template>
```

### With Options

```vue
<template>
  <ul v-auto-animate="{ duration: 300 }">
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
</template>
```

### Composable

```vue
<script setup>
import { ref } from 'vue';
import { useAutoAnimate } from '@formkit/auto-animate/vue';

const [parent] = useAutoAnimate();
const items = ref(['One', 'Two', 'Three']);
</script>

<template>
  <ul ref="parent">
    <li v-for="item in items" :key="item">{{ item }}</li>
  </ul>
</template>
```

## Svelte

```svelte
<script>
  import autoAnimate from '@formkit/auto-animate';

  let items = ['One', 'Two', 'Three'];

  function addItem() {
    items = [...items, `Item ${items.length + 1}`];
  }
</script>

<button on:click={addItem}>Add</button>

<ul use:autoAnimate>
  {#each items as item (item)}
    <li>{item}</li>
  {/each}
</ul>
```

### With Options

```svelte
<ul use:autoAnimate={{ duration: 300, easing: 'ease-out' }}>
  {#each items as item (item)}
    <li>{item}</li>
  {/each}
</ul>
```

## Solid

```jsx
import { createAutoAnimate } from '@formkit/auto-animate/solid';
import { createSignal, For } from 'solid-js';

function List() {
  const [parent] = createAutoAnimate();
  const [items, setItems] = createSignal(['One', 'Two', 'Three']);

  return (
    <ul ref={parent}>
      <For each={items()}>
        {(item) => <li>{item}</li>}
      </For>
    </ul>
  );
}
```

## Vanilla JavaScript

```javascript
import autoAnimate from '@formkit/auto-animate';

const list = document.getElementById('my-list');
autoAnimate(list);

// Add items dynamically - they'll animate in
const newItem = document.createElement('li');
newItem.textContent = 'New Item';
list.appendChild(newItem);
```

### Toggle Animation

```javascript
import autoAnimate from '@formkit/auto-animate';

const list = document.getElementById('my-list');
const controller = autoAnimate(list);

// Disable
controller.disable();

// Re-enable
controller.enable();

// Check state
console.log(controller.isEnabled());
```

## Configuration Options

```javascript
autoAnimate(element, {
  // Duration in milliseconds (default: 250)
  duration: 300,

  // Easing function (default: 'ease-in-out')
  easing: 'ease-out',

  // Disable respecting prefers-reduced-motion
  disrespectUserMotionPreference: false
});
```

## Custom Animations

For full control, provide a function that returns a KeyframeEffect.

```javascript
import autoAnimate from '@formkit/auto-animate';

autoAnimate(element, (el, action, oldCoords, newCoords) => {
  let keyframes;

  // action: 'add' | 'remove' | 'remain'

  if (action === 'add') {
    keyframes = [
      { transform: 'scale(0)', opacity: 0 },
      { transform: 'scale(1)', opacity: 1 }
    ];
  } else if (action === 'remove') {
    keyframes = [
      { transform: 'scale(1)', opacity: 1 },
      { transform: 'scale(0)', opacity: 0 }
    ];
  } else {
    // 'remain' - element moved position
    const deltaX = oldCoords.left - newCoords.left;
    const deltaY = oldCoords.top - newCoords.top;

    keyframes = [
      { transform: `translate(${deltaX}px, ${deltaY}px)` },
      { transform: 'translate(0, 0)' }
    ];
  }

  return new KeyframeEffect(el, keyframes, {
    duration: 300,
    easing: 'ease-out'
  });
});
```

### Custom Animation Examples

#### Slide from Left
```javascript
autoAnimate(element, (el, action) => {
  if (action === 'add') {
    return new KeyframeEffect(el, [
      { transform: 'translateX(-100%)', opacity: 0 },
      { transform: 'translateX(0)', opacity: 1 }
    ], { duration: 300, easing: 'ease-out' });
  }

  if (action === 'remove') {
    return new KeyframeEffect(el, [
      { transform: 'translateX(0)', opacity: 1 },
      { transform: 'translateX(100%)', opacity: 0 }
    ], { duration: 300, easing: 'ease-in' });
  }

  // Use default for 'remain'
  return new KeyframeEffect(el, [], { duration: 0 });
});
```

#### Flip Animation
```javascript
autoAnimate(element, (el, action, oldCoords, newCoords) => {
  if (action === 'remain') {
    const deltaX = oldCoords.left - newCoords.left;
    const deltaY = oldCoords.top - newCoords.top;
    const deltaW = oldCoords.width / newCoords.width;
    const deltaH = oldCoords.height / newCoords.height;

    return new KeyframeEffect(el, [
      {
        transform: `translate(${deltaX}px, ${deltaY}px) scale(${deltaW}, ${deltaH})`
      },
      { transform: 'translate(0, 0) scale(1, 1)' }
    ], { duration: 300, easing: 'ease-out' });
  }

  // Default for add/remove
  return new KeyframeEffect(el, [
    { opacity: action === 'add' ? 0 : 1 },
    { opacity: action === 'add' ? 1 : 0 }
  ], { duration: 200, easing: 'ease-out' });
});
```

## Common Patterns

### Animated Todo List

```jsx
function TodoList() {
  const [parent] = useAutoAnimate();
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    if (!input.trim()) return;
    setTodos([...todos, { id: Date.now(), text: input }]);
    setInput('');
  };

  const removeTodo = (id) => {
    setTodos(todos.filter(t => t.id !== id));
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && addTodo()}
      />
      <ul ref={parent}>
        {todos.map(todo => (
          <li key={todo.id}>
            {todo.text}
            <button onClick={() => removeTodo(todo.id)}>X</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Sortable List

```jsx
function SortableList() {
  const [parent] = useAutoAnimate();
  const [items, setItems] = useState([
    { id: 1, name: 'First' },
    { id: 2, name: 'Second' },
    { id: 3, name: 'Third' }
  ]);

  const moveUp = (index) => {
    if (index === 0) return;
    const newItems = [...items];
    [newItems[index - 1], newItems[index]] = [newItems[index], newItems[index - 1]];
    setItems(newItems);
  };

  const moveDown = (index) => {
    if (index === items.length - 1) return;
    const newItems = [...items];
    [newItems[index], newItems[index + 1]] = [newItems[index + 1], newItems[index]];
    setItems(newItems);
  };

  return (
    <ul ref={parent}>
      {items.map((item, index) => (
        <li key={item.id}>
          {item.name}
          <button onClick={() => moveUp(index)}>Up</button>
          <button onClick={() => moveDown(index)}>Down</button>
        </li>
      ))}
    </ul>
  );
}
```

### Filter/Search Results

```jsx
function FilterableList() {
  const [parent] = useAutoAnimate();
  const [query, setQuery] = useState('');

  const allItems = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'];
  const filtered = allItems.filter(item =>
    item.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Filter..."
      />
      <ul ref={parent}>
        {filtered.map(item => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Accordion

```jsx
function Accordion({ items }) {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <div>
      {items.map((item, index) => (
        <AccordionItem
          key={item.id}
          item={item}
          isOpen={openIndex === index}
          onToggle={() => setOpenIndex(openIndex === index ? null : index)}
        />
      ))}
    </div>
  );
}

function AccordionItem({ item, isOpen, onToggle }) {
  const [parent] = useAutoAnimate();

  return (
    <div ref={parent}>
      <button onClick={onToggle}>
        {item.title}
      </button>
      {isOpen && <div className="content">{item.content}</div>}
    </div>
  );
}
```

## Accessibility

AutoAnimate automatically respects `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  /* AutoAnimate will disable animations */
}
```

To override this behavior:

```javascript
autoAnimate(element, {
  disrespectUserMotionPreference: true
});
```

## Limitations

- Only animates **direct children** of the parent element
- Elements need stable keys/identity for move detection
- CSS animations on children may conflict
- Very rapid DOM changes may cause visual glitches

## Tips

1. **Always use keys** in React/Vue/Svelte for proper element tracking
2. **Apply to parent**, not individual items
3. **Keep durations short** (200-300ms) for snappy feel
4. **Disable when needed** for performance-critical operations
5. **Combine with CSS** for hover/focus states (AutoAnimate handles layout changes)
